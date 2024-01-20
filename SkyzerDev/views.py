import json
import os
import re
import time
import stripe
import boto3

import requests
from django.http import HttpResponse
from django.shortcuts import redirect, render
from fusionauth.fusionauth_client import FusionAuthClient

from . import settings
from .modules import Database
from datetime import datetime

from .modules.commands import load_commands


def index(request):
    return render(request, 'index.html')


def server_guardian(request):
    return render(request, 'server_guardian.html')


def robots(request):
    robots_text = """User-agent: *
"""
    return HttpResponse(robots_text, content_type="text/plain")


def about(request):
    return render(request, 'about.html')


def account(request):
    if not request.user.is_authenticated:
        return redirect('oidc_authentication_init')
    request.user.email = request.user.email.replace("%40", "@")
    user = {}
    try:
        client = FusionAuthClient(
            settings.OIDC_RP_APIKEY, settings.OIDC_OP_ISSUER
        )
        r = client.retrieve_user_by_email(request.user.email)

        if r.was_successful():
            user = r.success_response
        else:
            print(r.error_response)
    except Exception as e:
        print(e)
    user_data = user.get("user", {})
    full_name = user_data.get("fullName", "")
    discord_id = user_data.get("data", {}).get("discord_id", "")
    response = requests.get(f"https://dashboard.botghost.com/api/public/tools/user_lookup/{discord_id}", timeout=30)
    discord_username = False
    if response.status_code == 200:
        discord_username = response.json().get("username", False)
    if not discord_username:
        discord_username = "Not linked"
    if discord_username != "Not linked":
        request.session['discord_id'] = str(discord_id)
        request.session.modified = True
    last_login = user_data.get("lastLoginInstant", False)
    if last_login:
        last_login = datetime.fromtimestamp(last_login / 1000).strftime("%d/%m/%Y %H:%M:%S")
    else:
        last_login = "Never"
    return render(request, 'account.html', {'email': request.user.email, 'full_name': full_name,
                                            'last_login': last_login, 'discord_username': discord_username,
                                            'user_data': user_data,
                                            'stripe_billing_portal': os.environ.get("STRIPE_BILLING_PORTAL_URL", ""),
                                            'stripe_subscribe_url': os.environ.get("STRIPE_SUBSCRIBE_URL", ""), })


def nitrado_login(request):
    state = os.urandom(32).hex()
    request.session['state'] = state
    request.session.modified = True
    discord_id_param = request.GET.get('discord_id', None)
    if discord_id_param is not None:
        request.session['discord_id'] = str(discord_id_param)
        request.session.modified = True
    if request.session.get('discord_id', None) is None:
        return render(request, 'error.html',
                      context={"error": "Error: Please login or get the link from the Discord bot"})
    url = (f"https://oauth.nitrado.net/oauth/v2/auth?client_id={os.environ['NITRADO_CLIENT_ID']}"
           f"&redirect_uri={os.environ['NITRADO_REDIRECT_URI']}&response_type=code"
           f"&scope=service%20user_info&state={state}")
    return redirect(url)


def nitrado_callback(request):
    code = request.GET.get('code')
    state = request.GET.get('state')
    if state != request.session['state']:
        return render(request, 'error.html', context={"error": "Error: State mismatch"})
    url = "https://oauth.nitrado.net/oauth/v2/token"
    headers = {'Content-Type': 'application/x-www-form-urlencoded',
               }
    data = {'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': os.environ.get('NITRADO_REDIRECT_URI'),
            'client_id': os.environ.get('NITRADO_CLIENT_ID'),
            'client_secret': os.environ.get('NITRADO_CLIENT_SECRET')
            }
    response = requests.post(url, headers=headers, data=data, timeout=30)
    token = response.json()
    discord_id = request.session['discord_id']
    # Add to oracle nosql table
    user_data = requests.get("https://api.nitrado.net/user",
                             headers={"Authorization": f"Bearer {token['access_token']}"}, timeout=30)
    try:
        user_data = user_data.json()
    except Exception as e:
        return render(request, 'error.html', context={"error": f"Error: Nitrado API returned invalid JSON: {e}"})
    user_data = user_data.get("data", {}).get("user", {})
    if user_data == {}:
        return render(request, 'error.html', context={"error": "Error: Nitrado API returned empty user data"})
    document = {
        "access_token": token["access_token"],
        "refresh_token": token["refresh_token"],
        "expires_at": token["expires_in"] + int(time.time()),
        "email": user_data["email"],
        "discord_id": discord_id
    }
    lambda_client = boto3.client(
        'lambda',
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_REGION")
    )
    # TODO: Chane this to wait for the response to be returned to check for errors
    _ = lambda_client.invoke(
        FunctionName="upload_nitrado_tokens",
        InvocationType='Event',
        Payload=json.dumps(document)
    )
    return render(request, 'nitrado_success.html')


def update_stripe_email(request):
    if request.method != "POST" or not request.user.is_authenticated or request.session.get('discord_id', None) is None:
        return redirect('account')
    email = request.POST.get("email", None)
    if email is None:
        return render(request, 'error.html', context={"error": "Error: No email provided"})
    email = email.lower()
    email_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    if not re.match(email_regex, email):
        return render(request, 'error.html', context={"error": "Error: Invalid email provided"})
    stripe.api_key = os.environ.get("STRIPE_API_KEY")
    subs = stripe.Subscription.query(f'email:"{email}"')
    if len(subs.get('data', [])) == 0:
        return render(request, 'error.html', context={"error": "Error: No subscription found for that email"})
    couch_database = Database(os.environ["COUCHBASE_USERNAME"], os.environ["COUCHBASE_PASSWORD"],
                              os.environ["COUCHBASE_HOST"])
    # Set the bucket
    couch_database.set_bucket(os.environ["COUCHBASE_BUCKET"])
    # Set the scope
    couch_database.set_scope(os.environ["COUCHBASE_SCOPE"])
    # Set the collection to stripe
    couch_database.set_collection('stripe')
    # Upsert the data
    couch_database.upsert_document(request.session['discord_id'], {"email": email})
    return render(request, 'stripe_email_success.html')


def premium_features(request):
    return render(request, 'coming_soon.html')


def logout(request):
    request.session.flush()
    request.session.modified = True
    url = f"{settings.OIDC_OP_ISSUER}/oauth2/logout?client_id={settings.OIDC_RP_CLIENT_ID}"
    return redirect(url)


def commands(request):
    command_data = load_commands()
    return render(request, 'commands.html', context={"command_data": command_data})


def premium_commands(request):
    return render(request, 'coming_soon.html')


def terms_of_service(request):
    return render(request, 'terms.html')


def privacy_policy(request):
    return render(request, 'privacy.html')


def cookies(request):
    return render(request, 'cookies.html')
