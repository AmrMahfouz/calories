from django.conf.urls import url
from django.contrib.auth.models import User
from tastypie.bundle import Bundle
from tastypie_oauth.authentication import OAuth20Authentication
from tastypie.authentication import SessionAuthentication, MultiAuthentication
from tastypie.resources import ModelResource
from tastypie.authorization import Authorization
from tastypie import fields
from .models import UserProfile


class CustomUserResourceAuthorization(Authorization):

    def read_list(self, object_list, bundle):
        # This assumes a ``QuerySet`` from ``ModelResource``.
        return object_list.filter(username=bundle.request.user.username)

    def read_detail(self, object_list, bundle):
        # Is the requested object owned by the user?
        return bundle.obj.username == bundle.request.user.username

    def create_list(self, object_list, bundle):
        # Assuming they're auto-assigned to ``user``.
        return object_list

    def create_detail(self, object_list, bundle):
        return bundle.obj.username == bundle.request.user.username

    def update_list(self, object_list, bundle):
        allowed = []

        # Since they may not all be saved, iterate over them.
        for obj in object_list:
            if obj.username == bundle.request.user.username:
                allowed.append(obj)

        return allowed

    def update_detail(self, object_list, bundle):
        return bundle.obj.username == bundle.request.user.username

    def delete_list(self, object_list, bundle):
        allowed = []

        # Since they may not all be saved, iterate over them.
        for obj in object_list:
            if obj.username == bundle.request.user.username:
                allowed.append(obj)

        return allowed

    def delete_detail(self, object_list, bundle):
        return bundle.obj.username == bundle.request.user.username


class CustomAuthorization(Authorization):

    def read_list(self, object_list, bundle):
        # This assumes a ``QuerySet`` from ``ModelResource``.
        return object_list.filter(user=bundle.request.user)

    def read_detail(self, object_list, bundle):
        # Is the requested object owned by the user?
        return bundle.obj.user == bundle.request.user

    def create_list(self, object_list, bundle):
        # Assuming they're auto-assigned to ``user``.
        return object_list

    def create_detail(self, object_list, bundle):
        return bundle.obj.user == bundle.request.user

    def update_list(self, object_list, bundle):
        allowed = []

        # Since they may not all be saved, iterate over them.
        for obj in object_list:
            if obj.user == bundle.request.user:
                allowed.append(obj)

        return allowed

    def update_detail(self, object_list, bundle):
        return bundle.obj.user == bundle.request.user

    def delete_list(self, object_list, bundle):
        allowed = []

        # Since they may not all be saved, iterate over them.
        for obj in object_list:
            if obj.user == bundle.request.user:
                allowed.append(obj)

        return allowed

    def delete_detail(self, object_list, bundle):
        return bundle.obj.user == bundle.request.user


class UserResource(ModelResource):
    expected_calories = fields.IntegerField()

    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'
        excludes = ['password', 'is_active', 'is_staff', 'is_superuser', 'id']
        allowed_methods = ['get', 'post', 'put', 'delete']
        authorization = CustomUserResourceAuthorization()
        authentication = MultiAuthentication(SessionAuthentication(), OAuth20Authentication())

    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/(?P<username>[\w\d_.-]+)/$" % self._meta.resource_name, self.wrap_view('dispatch_detail'), name="api_dispatch_detail"),
        ]

    def dehydrate(self, bundle):
        clients = [{'name': ak.name,
                    'url': ak.url,
                    'client_id': ak.client_id,
                    'client_secret': ak.client_secret} for ak in bundle.obj.oauth2_client.all()]

        bundle.data['clients'] = clients
        bundle.data['expected_calories'] = bundle.obj.userprofile.expected_calories
        return bundle

    def hydrate(self, bundle):
        return bundle

    def get_object_list(self, request):
        return super(UserResource, self).get_object_list(request).filter(username=request.user.username)

    def detail_uri_kwargs(self, bundle_or_obj):
        if isinstance(bundle_or_obj, Bundle):
            return {'username': bundle_or_obj.obj.username}
        else:
            return {'username': bundle_or_obj.username}

    def obj_get_list(self, bundle, **kwargs):
        # Filtering disabled for brevity...
        return self.get_object_list(bundle.request)

    def obj_create(self, bundle, **kwargs):
        super(UserResource, self).obj_create(bundle, **kwargs)
        userprofile = UserProfile.objects.get(user=bundle.request.user)
        userprofile.expected_calories = bundle.data.get('expected_calories',
                                                        userprofile.expected_calories)
        userprofile.save()

        return bundle

    def obj_update(self, bundle, **kwargs):
        super(UserResource, self).obj_update(bundle, **kwargs)
        userprofile = UserProfile.objects.get(user=bundle.request.user)
        userprofile.expected_calories = bundle.data.get('expected_calories',
                                                        userprofile.expected_calories)
        userprofile.save()
        return self.obj_create(bundle, **kwargs)

    def rollback(self, bundles):
        pass
