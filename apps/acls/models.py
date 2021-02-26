from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.db.models import TextChoices
import uuid
from orgs.mixins.models import OrgModelMixin
from common.validators import alphanumeric


class ACLAction:
    DENY = 0b1
    CONFIRM = 0b1 << 1

    CHOICES = (
        (DENY, _('Deny')),
        (CONFIRM, _('Confirm'))
    )


class PolicyType(TextChoices):
    asset = 'assetACL', 'AssetACL'


class BaseACLPolicy(OrgModelMixin):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    name = models.CharField(max_length=128, verbose_name=_('Name'))
    policy_type = models.CharField(max_length=32, choices=PolicyType.choices, verbose_name=_('Policy Type'))
    action = models.IntegerField(choices=ACLAction.CHOICES, default=ACLAction.DENY, verbose_name=_("Action"))
    created_by = models.CharField(max_length=128, blank=True, verbose_name=_('Created by'))
    date_created = models.DateTimeField(auto_now_add=True, verbose_name=_('Date created'))
    comment = models.TextField(verbose_name=_('Comment'), blank=True)
    # * 代表所有用户
    user = models.CharField(max_length=128, verbose_name=_('User'))

    class Meta:
        abstract = True


class AssetACLPolicy(BaseACLPolicy):
    ip_start = models.GenericIPAddressField(verbose_name=_('IP Start'))
    ip_end = models.GenericIPAddressField(verbose_name=_('IP End'))
    port = models.IntegerField(default=22, verbose_name=_('Port'))
    # * 代表所有系统用户
    system_user = models.CharField(max_length=128, verbose_name=_('System User'), validators=[alphanumeric])
    need_review = models.BooleanField(default=False, verbose_name=_('need review'))
    reviewers = models.ManyToManyField('users.User', verbose_name=_("Reviewers"), related_name='%(class)ss')
