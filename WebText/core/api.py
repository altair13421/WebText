"""
This file is used to define the generic views for the game

This File Does:

1. Defines the CoreViewSet class
2. Defines the get_user and get_decoded_token methods
3. Defines the get_queryset method
4. Defines the perform_create method
5. Defines the paginate_this_response method

"""

# type: ignore
from rest_framework import status, viewsets, exceptions, serializers  # type: ignore
from rest_framework.response import Response  # type: ignore
from rest_framework.decorators import action  # type: ignore
from rest_framework.permissions import AllowAny  # type: ignore

from rest_framework_simplejwt.views import TokenObtainPairView  # type: ignore
from rest_framework_simplejwt.authentication import JWTAuthentication, api_settings
from rest_framework_simplejwt.exceptions import (  # type: ignore
    AuthenticationFailed,
    InvalidToken,  # type: ignore
    TokenError,  # type: ignore
)
import jwt

from django.apps import apps
from django.contrib.auth.models import AbstractBaseUser
from django.db.models.query import QuerySet
from django.db.models import Q
from django.core import exceptions


studentuser_model = apps.get_model("codera_schools", "StudentUser")
adminuser_model = apps.get_model("codera_schools", "AdminUser")
teacheruser_model = apps.get_model("codera_schools", "TeacherUser")


class CoreViewSet(viewsets.ModelViewSet):
    serializer_class = None
    queryset = None
    permission_classes = (AllowAny,)
    model = None

    @classmethod
    def get_serializer_class(
        cls,
    ):
        return cls.serializer_class

    @classmethod
    def get_model(cls):
        if cls.model:
            return cls.model
        return cls.get_serializer_class().get_model()  # type: ignore

    def get_user(self, decoded):
        user_id = decoded.get("user_id", None)
        user_type = decoded.get("user_type", None)
        user: AbstractBaseUser
        if user_type == "admin":
            user = adminuser_model.objects.get(id=user_id)
        if user_type == "teacher":
            user = teacheruser_model.objects.get(id=user_id)
        if user_type == "student":
            user = studentuser_model.objects.get(id=user_id)
        if user.is_onboarded:
            return user
        else:
            raise exceptions.PermissionDenied("You are on waitlist", "access_denied")

    def get_decoded_token(self, request):
        if "HTTP_AUTHORIZATION" in request.META.keys():
            try:
                raw_token = request.META["HTTP_AUTHORIZATION"].split()[-1]
                _decoded = jwt.decode(
                    raw_token,
                    options={"verify_signature": False},
                )
                return self.get_user(_decoded), _decoded
            except Exception as E:
                raise AuthenticationFailed("User Not Authenticated for This Action")
        return None, None

    def get_queryset(self):
        return self.get_model().objects.all()

    def perform_create(self, serializer):
        return serializer.create(serializer.validated_data)

    def paginate_this_response(
        self,
        queryset: QuerySet,
        serializer: serializers.Serializer = None,
    ):
        page = self.paginate_queryset(queryset)
        if page is not None:
            if serializer is None:
                serialized = self.serializer_class(page, many=True)  # type: ignore
            else:
                serialized = serializer(page, many=True)  # type: ignore
            return self.get_paginated_response(serialized.data)
        return None


class ReadOnlyCoreViewSet(CoreViewSet):

    def create(self, request, *args, **kwargs):
        raise exceptions.PermissionDenied("Not Allowed")

    def update(self, request, *args, **kwargs):
        raise exceptions.PermissionDenied("Not Allowed")

    def destroy(self, request, *args, **kwargs):
        raise exceptions.PermissionDenied("Not Allowed")
