# needed for any cluster connection
from datetime import timedelta

import couchbase
from couchbase.auth import PasswordAuthenticator
from couchbase.cluster import Cluster
from couchbase.bucket import Bucket
from couchbase.scope import Scope
from couchbase.collection import Collection
# needed for options -- cluster, timeout, SQL++ (N1QL) query, etc.
from couchbase.options import (ClusterOptions, ClusterTimeoutOptions,
                               QueryOptions)
from couchbase.subdocument import Spec


class Database:

    def __init__(self, username, password, server):
        self.bucket: Bucket = None
        self.scope: Scope = None
        self.collection: Collection = None
        self.username = username
        self.password = password
        options = ClusterOptions(
            PasswordAuthenticator(self.username, self.password))
        options.apply_profile('wan_development')
        self.cluster = Cluster(f'couchbase://{server}', options)
        self.cluster.wait_until_ready(timedelta(seconds=5))
        
    def set_bucket(self, bucket):
        self.bucket = self.cluster.bucket(bucket)
    
    def set_scope(self, scope):
        if self.bucket is None:
            raise Exception("bucket is not set")
        self.scope = self.bucket.scope(scope)
        
    def set_collection(self, collection):
        if self.scope is None:
            raise Exception("scope is not set")
        self.collection = self.scope.collection(collection)

    def read_document(self, document_id):
        if self.collection is None:
            raise Exception("collection is not set")
        try:
            return self.collection.get(document_id)
        except couchbase.exceptions.DocumentNotFoundException:
            return None

    def upsert_document(self, document_id, document):
        """
        Making changes to the entire document (will replace)
        :param document_id:
        :param document:
        :return:
        """
        if self.collection is None:
            raise Exception("collection is not set")
        return self.collection.upsert(document_id, document)

    def update_document(self, document_id: str, key: str, value):
        if self.collection is None:
            raise Exception("collection is not set")
        self.collection.mutate_in(document_id, [Spec(['upsert', key, value])])
    