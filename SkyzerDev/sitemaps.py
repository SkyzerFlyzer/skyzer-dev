from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse


class StaticViewSitemap(Sitemap):
    protocol = 'https'
    changefreq = "weekly"

    def items(self):
        return ['index', 'about', 'nitrado_server_guardian', 'robots', 'premium_features', 'commands',
                'premium_commands', 'terms_of_service', 'privacy_policy', 'cookies', 'lotus:article-index']

    def location(self, item):
        return reverse(item)
