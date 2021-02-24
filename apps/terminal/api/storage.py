# coding: utf-8
#

from rest_framework import viewsets, generics, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.utils.translation import ugettext_lazy as _

from common.const.http import GET
from common.permissions import IsSuperUser
from terminal.filters import CommandStorageFilter
from ..models import CommandStorage, ReplayStorage
from ..serializers import CommandStorageSerializer, ReplayStorageSerializer


__all__ = [
    'CommandStorageViewSet', 'CommandStorageTestConnectiveApi',
    'ReplayStorageViewSet', 'ReplayStorageTestConnectiveApi'
]


class BaseStorageViewSetMixin:

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.type_null_or_server:
            data = {'msg': _('Deleting the default storage is not allowed')}
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
        if instance.is_use():
            data = {'msg': _('Cannot delete storage that is being used')}
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
        return super().destroy(request, *args, **kwargs)


class CommandStorageViewSet(BaseStorageViewSetMixin, viewsets.ModelViewSet):
    search_fields = ('name', 'type',)
    queryset = CommandStorage.objects.all()
    serializer_class = CommandStorageSerializer
    permission_classes = (IsSuperUser,)
    filterset_class = CommandStorageFilter

    @action(methods=[GET], detail=False)
    def tree(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        queryset = queryset.exclude(name='null')

        root = {
            'id': 'root',
            'name': _('Command storages'),
            'title': _('Command storages'),
            'pId': '',
            'isParent': True,
            'open': True,
        }

        nodes = [
            {
                'id': storage.id,
                'name': storage.name,
                'title': f'{storage.name}({storage.type})',
                'pId': 'root',
                'isParent': False,
                'open': False,
            } for storage in queryset
        ]
        nodes.append(root)
        return Response(data=nodes)


class ReplayStorageViewSet(BaseStorageViewSetMixin, viewsets.ModelViewSet):
    filterset_fields = ('name', 'type',)
    search_fields = filterset_fields
    queryset = ReplayStorage.objects.all()
    serializer_class = ReplayStorageSerializer
    permission_classes = (IsSuperUser,)


class BaseStorageTestConnectiveMixin:
    permission_classes = (IsSuperUser,)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        try:
            is_valid = instance.is_valid()
        except Exception as e:
            is_valid = False
            msg = _("Test failure: {}".format(str(e)))
        else:
            if is_valid:
                msg = _("Test successful")
            else:
                msg = _("Test failure: Account invalid")
        data = {
            'is_valid': is_valid,
            'msg': msg
        }
        return Response(data)


class CommandStorageTestConnectiveApi(BaseStorageTestConnectiveMixin, generics.RetrieveAPIView):
    queryset = CommandStorage.objects.all()


class ReplayStorageTestConnectiveApi(BaseStorageTestConnectiveMixin, generics.RetrieveAPIView):
    queryset = ReplayStorage.objects.all()
