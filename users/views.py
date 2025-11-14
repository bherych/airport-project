from .models import User
from .serializers import UserSerializer
from rest_framework import viewsets
import logging
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django_filters.rest_framework import DjangoFilterBackend
from airport_project.permissions import IsOwnerOrAdmin

logger = logging.getLogger(__name__)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['username', 'country', 'is_active', 'is_staff']

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return User.objects.all()
        return User.objects.filter(id=user.id)

    def get_permissions(self):
        if self.action == 'create':
            return []
        elif self.action in ['list', 'retrieve', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsOwnerOrAdmin()]
        return super().get_permissions()

    def list(self, request, *args, **kwargs):
        logger.info("Getting all users request")
        try:
            return super().list(request, *args, **kwargs)
        except Exception as e:
            logger.error(f"Error retrieving users: {e}")
            raise

    def retrieve(self, request, *args, **kwargs):
        logger.info(f"Retrieving details of user with id={kwargs.get('pk')}")
        try:
            return super().retrieve(request, *args, **kwargs)
        except Exception as e:
            logger.error(f"Error retrieving user with id={kwargs.get('pk')}: {e}")
            raise

    def create(self, request, *args, **kwargs):
        logger.info(f"Creating new user: {request.data}")
        try:
            return super().create(request, *args, **kwargs)
        except Exception as e:
            logger.error(f"Error creating user: {e}")
            raise

    def update(self, request, *args, **kwargs):
        logger.info(f"Updating user with id={kwargs.get('pk')}: {request.data}")
        try:
            return super().update(request, *args, **kwargs)
        except Exception as e:
            logger.error(f"Error updating user with id={kwargs.get('pk')}: {e}")
            raise

    def destroy(self, request, *args, **kwargs):
        logger.warning(f"Deleting user with id={kwargs.get('pk')}")
        try:
            return super().destroy(request, *args, **kwargs)
        except Exception as e:
            logger.error(f"Error deleting user with id={kwargs.get('pk')}: {e}")
            raise