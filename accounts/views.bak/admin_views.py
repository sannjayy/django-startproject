
from ..serializers import AdminLoginSerializer
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from rest_framework import permissions, status, generics, views
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle

from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListAPIView, RetrieveAPIView, GenericAPIView, ListCreateAPIView, CreateAPIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import response, status, mixins, parsers
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.throttling import AnonRateThrottle
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.filters import SearchFilter, OrderingFilter
from ..serializers import UserAccountSerializer, MinimalUserDataSerializer

from django.contrib.auth import get_user_model
User = get_user_model()


class AdminLoginAPIView(generics.GenericAPIView):
    serializer_class = AdminLoginSerializer
    throttle_classes = [AnonRateThrottle]
    def post(self, request):
        serializer = self.serializer_class(data = request.data)
        data = serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



class UsersListView(ListAPIView):
    permission_classes = (IsAuthenticated, )
    queryset = User.objects.all()
    serializer_class = UserAccountSerializer
    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    search_fields = ['full_name','email', 'mobile', 'referral_id']
    filterset_fields = ['gender']
    ordering_fields = ['updated_at', 'created_at']

    def get_queryset(self):
        queryset = self.queryset.filter(is_superuser=False)
        return queryset.order_by('-created_at')

class UserDetailAPIView(RetrieveAPIView):
    permission_classes = (IsAuthenticated, )
    queryset = User.objects.all()
    serializer_class = UserAccountSerializer
    lookup_field = 'username'

    def get(self, request, username):
        user = get_object_or_404(self.get_queryset(), username=username)
        # trans = user.stroke_transactions.all()
        # print(trans)
        serializer = self.serializer_class(user)
        return Response({
            'success': True,
            'user': serializer.data,
        })


class AdminUserReferralListAPIView(ListAPIView):
    model = User
    queryset = User.objects.all()
    serializer_class = MinimalUserDataSerializer
    permission_classes = (IsAuthenticated, )

    def list(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        obj = self.get_queryset().filter(referral_code=user.referral_id)
        serializer = self.serializer_class(obj, many=True)
        if obj:
            return Response({'success': True, 'detail': f'Found {obj.count()} referrals.', 'data': serializer.data}, status=status.HTTP_200_OK)
        return Response({'success': False, 'detail': 'No referral found...'}, status=status.HTTP_404_NOT_FOUND)
    
