from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView


from . import serializers, permissions, authenticators
from .. import models


class UserView(viewsets.ModelViewSet):
    serializer_class = serializers.UserSerializer
    model = User

    def get_permissions(self):
        # allow non-authenticated user to create
        return (AllowAny() if self.request.method == 'POST'
                else permissions.IsStaffOrTargetUser()),


class AuthView(APIView):
    authentication_classes = (authenticators.QuietBasicAuthentication,)

    def post(self, request, *args, **kwargs):
        login(request, request.user)
        return Response(serializers.UserSerializer(request.user).data)

    def delete(self, request, *args, **kwargs):
        logout(request)
        return Response()


class PostView(viewsets.ModelViewSet):
    """view that serves posts"""
    model = models.PostModel
    serializer_class = serializers.PostSerializer
    permission_classses = (permissions.IsOwner,)

    def pre_save(self, obj):
        # add user to object if user is logged in
        if isinstance(self.request.user, User):
            obj.user = self.request.user
