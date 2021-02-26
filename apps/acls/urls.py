from django.urls import path
from rest_framework_bulk.routes import BulkRouter
from . import api

app_name = 'acls'

router = BulkRouter()

urlpatterns = [
    path(r'asset/', api.AssetACLViewSet.as_view({'get': 'list'}), name='acl-asset'),
]

urlpatterns += router.urls
