from orgs.mixins.api import OrgBulkModelViewSet
from orgs.mixins.serializers import BulkOrgResourceModelSerializer
from . import models


class AssetACLPolicySerializer(BulkOrgResourceModelSerializer):
    class Meta:
        model = models.AssetACLPolicy
        mini_fields = ['id', 'name']
        m2m_fields = ['reviewers', ]
        fields = mini_fields + m2m_fields
