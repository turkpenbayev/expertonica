from django.contrib.auth import get_user_model
from django.core.exceptions import ImproperlyConfigured
from django.shortcuts import render, redirect
from django.utils import timezone
from django.db.models import Count, Q
from django.http import HttpResponse
import json

from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets, status, mixins
from rest_framework.decorators import action

from .serializers import *
from .utils import *
from .forms import *
from .tasks import *

User = get_user_model()


class AuthViewSet(viewsets.GenericViewSet):
    permission_classes = [AllowAny, ]
    serializer_class = EmptySerializer
    serializer_classes = {
        'login': UserLoginSerializer,
        'register': UserRegisterSerializer,
        'password_change': PasswordChangeSerializer,
    }

    @action(methods=['POST', ], detail=False)
    def login(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_and_authenticate_user(**serializer.validated_data)
        data = AuthUserSerializer(user).data
        return Response(data=data, status=status.HTTP_200_OK)

    @action(methods=['POST', ], detail=False)
    def register(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = create_user_account(**serializer.validated_data)
        data = AuthUserSerializer(user).data
        return Response(data=data, status=status.HTTP_201_CREATED)

    @action(methods=['POST', ], detail=False)
    def logout(self, request):
        logout(request)
        data = {'success': 'Sucessfully logged out'}
        return Response(data=data, status=status.HTTP_200_OK)

    @action(methods=['POST'], detail=False, permission_classes=[IsAuthenticated, ])
    def password_change(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        request.user.set_password(serializer.validated_data['new_password'])
        request.user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_serializer_class(self):
        if not isinstance(self.serializer_classes, dict):
            raise ImproperlyConfigured(
                "serializer_classes should be a dict mapping.")

        if self.action in self.serializer_classes.keys():
            return self.serializer_classes[self.action]
        return super().get_serializer_class()


def home(request):
    if request.method == 'POST':
        form = SessionForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save()
            count = count_sites_from_file(instance)
            return redirect('home')
    else:
        form = SessionForm()

    sessions = Session.objects.annotate(checked_count=Count(
        'sites', filter=Q(sites__is_checked=True))).all()
    return render(request, 'home.html', {
        'form': form,
        'sessions': sessions
    })


def session(request, pk=None):
    session_name = Session.objects.get(pk=pk).filename()
    site_infos = SiteInfo.objects.filter(session__pk=pk)
    return render(request, 'session.html', {
        'site_infos': site_infos,
        'session_name': session_name
    })


class SiteCheckAPIView(APIView):
    """
    View to check site.

    * All users are able to access this view.
    """
    permission_classes = [AllowAny]

    def get(self, request, format=None):
        """
        Return a info about site.
        """
        try:
            url = request.query_params.get('url')
            ip = get_site_ip(domain=url)
            status, responce_time = get_site_info(domain=url)
            data = {
                'url': url,
                'ip': ip,
                'status': status,
                'responce_time': responce_time
            }
            return Response(data, status=200)
        except Exception as ex:
            return Response({'error': str(ex)}, status=400)
