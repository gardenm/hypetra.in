from django.conf.urls import patterns, include, url
from wordof.api import ArtifactResource

from django.contrib import admin
admin.autodiscover()

artifact_resource = ArtifactResource()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'rvws.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include(artifact_resource.urls)),
)
