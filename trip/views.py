from rest_framework import viewsets
from rest_framework import permissions

from post.permissions import IsOwnerOrReadOnly
from trip.models import Trip
from trip.serializers import TripSerializer


class TripViewSet(viewsets.ModelViewSet):
    queryset = Trip.objects.all()
    serializer_class = TripSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly)

    def get_queryset(self):
        qs = self.request.user
        queryset = super().get_queryset()
        queryset = queryset.filter(user=qs)
        return queryset
