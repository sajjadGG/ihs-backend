from rest_framework import authentication , permissions

from django.contrib.auth import get_user_model


User = get_user_model()

#TODO : username to USERNAME

class IsOwnerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        serializer = view.get_serializer(obj)
        return serializer.data['owner'] == request.user.username

class DefaultsMixin():
    """Default settings for view authentication , permissions , filtering and pagination"""

    authentication_classes = (
        authentication.BasicAuthentication,
        authentication.TokenAuthentication,
    )

    permission_classes = (
        permissions.IsAuthenticated,
    )

    paginate_by = 25
    paginate_by_param = 'page_size'
    max_paginate_by = 100

class OwnerMixin():

    authentication_classes = (
        authentication.BasicAuthentication,
        authentication.TokenAuthentication,
    )

    permission_classes = (
        permissions.IsAuthenticated,
        IsOwnerOrReadOnly,
    )

    paginate_by = 25
    paginate_by_param = 'page_size'
    max_paginate_by = 100