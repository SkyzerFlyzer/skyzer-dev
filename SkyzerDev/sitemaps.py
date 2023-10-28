from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse


class StaticViewSitemap(Sitemap):
    def items(self):
        return ['index', 'about', 'nitrado_server_guardian', 'robots']

    def location(self, item):
        return reverse(item)
