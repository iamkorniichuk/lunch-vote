from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwner(BasePermission):
    def __init__(self, field_name="created_by"):
        self.message = {field_name: "You need to be owner of this object."}
        self.field_name = field_name

    def has_object_permission(self, request, view, obj):
        obj_profile = obj
        for field in self.field_name.split("."):
            obj_profile = getattr(obj_profile, field)

        return obj_profile == request.user


class IsOwnerOrReadOnly(IsOwner):
    def has_object_permission(self, request, view, obj):
        return request.method in SAFE_METHODS or super().has_object_permission(
            request, view, obj
        )
