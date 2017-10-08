from tastypie.resources import ModelResource
from tastypie.constants import ALL

from service.models import Theaterservice


class TheaterResource(ModelResource):
    class Meta:
        queryset = Theaterservice.objects.all()
        resource_name = 'service'
        limit = 100
        filtering = {'title': ALL}
