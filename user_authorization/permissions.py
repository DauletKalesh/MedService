from rest_framework.permissions import BasePermission

class IsProfileOwner(BasePermission):

    def has_object_permission(self, request, view, obj):

        return request.user.id == obj.user.id
    # def has_permission(self, request, view):

    #     # queryset = getattr(view, 'get_queryset', None)
    #     queryset = self._queryset(view)
    #     return request.user.id == queryset.user.id