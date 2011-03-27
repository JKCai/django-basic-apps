from basic.blog.models import Settings, Post
from basic.blog.signals import invalidate_settings_cache, update_settings
from django.db.models import signals
from django.contrib.sites.models import Site

signals.post_save.connect(update_settings, Site, True)
signals.post_save.connect(invalidate_settings_cache, Settings, True)
