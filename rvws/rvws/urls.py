from django.conf.urls import patterns, include, url
from tastypie.api import Api
from wordof.api import *

from django.contrib import admin
admin.autodiscover()


v1_api = Api(api_name='v1')
for resource in [ArtistResource(), ArtifactResource(), CriticResource(), CategoryResource(), ReviewResource()]:
    v1_api.register(resource)

artist_resource = ArtistResource()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include(v1_api.urls)),
)
