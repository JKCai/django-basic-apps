from django.core.cache import cache
from django.core.urlresolvers import reverse
from django.contrib.sites.models import Site

from basic.blog.models import Settings
from sugar.cache.utils import create_cache_key


def update_settings(sender=None, instance=None, isnew=False, **kwargs):

    if isnew:
        return

    try:
        settings = Settings.objects.get(site=instance)
        #save updates cached values
        settings.save()
    except:
        """
        Refactor maybe - this signal is being called during `syncdb` and 
        failing because Settings don't exist yet. So we `pass` but it feels 
        like there could be a better solution.
        """
        pass
        

def invalidate_settings_cache(sender=None, instance=None, isnew=False, **kwargs):

    if isnew:
        return

    site_id = instance.site.id        
    key = create_cache_key(Settings, field='site__id', field_value=site_id)
    
    """
    Invalidate cache, set to None for 5 seconds to safegaurd
    against race condition; concept borrowed from mmalone's django-caching
    """
    cache.set(key, None, 5)
