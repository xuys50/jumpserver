from django_filters import rest_framework as filters

from orgs.utils import current_org
from terminal.models import Command


class CommandFilter(filters.FilterSet):
    date_from = filters.DateTimeFilter()
    date_to = filters.DateTimeFilter()
    session_id = filters.CharFilter(field_name='session')
    command_storage_id = filters.UUIDFilter(method='filter_by_command_storage_id')

    class Meta:
        model = Command
        fields = [
            'asset', 'system_user', 'user', 'session', 'risk_level', 'input',
            'date_from', 'date_to', 'session_id', 'risk_level', 'command_storage_id',
        ]

    def filter_by_command_storage_id(self, queryset, name, value):
        return queryset

    @property
    def qs(self):
        qs = super().qs
        qs = qs.filter(org_id=self.get_org_id())
        return qs

    @staticmethod
    def get_org_id():
        if current_org.is_default():
            org_id = ''
        else:
            org_id = current_org.id
        return org_id
