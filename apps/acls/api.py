from orgs.mixins.api import OrgGenericViewSet,OrgBulkModelViewSet
from common.permissions import IsOrgAdminOrAppUser
from . import models
from . import serializers

class AssetACLViewSet(OrgBulkModelViewSet):
    model = models.AssetACLPolicy
    serializer_class = serializers.AssetACLPolicySerializer
