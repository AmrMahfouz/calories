from django.contrib.auth.models import User
from tastypie_oauth.authentication import OAuth20Authentication
from tastypie.authentication import SessionAuthentication, MultiAuthentication
from tastypie.resources import ModelResource
from tastypie.authorization import DjangoAuthorization
from tastypie import fields
from base.models import UserProfile


class UserProfileResource(ModelResource):
    class Meta:
        queryset = UserProfile.objects.all()
        resource_name = 'profile'
        authorization = DjangoAuthorization()
        authentication = MultiAuthentication(SessionAuthentication(), OAuth20Authentication())


class UserResource(ModelResource):
    userprofile = fields.OneToOneField(UserProfile, 'userprofile', full=True)

    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'
        excludes = ['password', 'is_active', 'is_staff', 'is_superuser']
        authorization = DjangoAuthorization()
        authentication = MultiAuthentication(SessionAuthentication(), OAuth20Authentication())

    def hydrate(self, bundle):
        import ipdb; ipdb.set_trace()

    def dehydrate(self, bundle):
        clients = [{'name': ak.name,
                    'url': ak.url,
                    'client_id': ak.client_id,
                    'client_secret': ak.client_secret} for ak in bundle.obj.oauth2_client.all()]

        bundle.data['clients'] = clients
        import ipdb; ipdb.set_trace()
        return bundle

    def get_object_list(self, request):
        return super(UserResource, self).get_object_list(request).filter(username=request.user.username)

    def obj_update(self, bundle, skip_errors=False, **kwargs):
        import ipdb; ipdb.set_trace()