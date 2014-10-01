from tastypie_oauth.authentication import OAuth20Authentication
from tastypie.authentication import SessionAuthentication, MultiAuthentication
from tastypie.authorization import Authorization
from tastypie.resources import ModelResource
from tastypie.paginator import Paginator
from .models import Meal


class MealResource(ModelResource):
    class Meta:
        queryset = Meal.objects.all()
        resource_name = 'meal'
        allowed_methods = ['get', 'post', 'put', 'delete']
        authorization = Authorization()
        authentication = MultiAuthentication(SessionAuthentication(), OAuth20Authentication())

        paginator = Paginator

    def hydrate(self, bundle):
            if bundle.request.user.is_authenticated():
                user = bundle.request.user
            else:
                bundle.errors

            bundle.obj.user = user
            return bundle

    def dehydrate(self, bundle):
        bundle.data['username'] = bundle.obj.user.username
        return bundle

    def get_object_list(self, request):
        return super(MealResource, self).get_object_list(request).filter(user__username=request.user.username).order_by('date')
