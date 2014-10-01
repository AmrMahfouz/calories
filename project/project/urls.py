from django.conf.urls import patterns, include, url
from django.contrib import admin
from tastypie.api import Api
from calories.api import MealResource
from base.api import UserResource, UserProfileResource

v1_api = Api(api_name='v1')
v1_api.register(UserResource())
v1_api.register(UserProfileResource())
v1_api.register(MealResource())

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'project.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', 'base.views.home', name='home'),
    url(r'^admin/', include(admin.site.urls)),
    (r'^api/', include(v1_api.urls)),
    url(r'^oauth2/', include('provider.oauth2.urls', namespace='oauth2')),
    (r'^accounts/', include('allauth.urls')),
)
