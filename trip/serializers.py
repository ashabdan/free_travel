
from rest_framework import serializers
from trip.models import TripDetail, Trip


class TripDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = TripDetail
        fields = ('post',)


class TripSerializer(serializers.ModelSerializer):
    items = TripDetailSerializer(many=True, write_only=True)

    class Meta:
        model = Trip
        fields = ('id', 'items', )

    def create(self, validated_data):
        request = self.context.get('request')
        items = validated_data.pop('items')
        user = request.user.owner
        trip = Trip.objects.create(user=user)
        for item in items:
            TripDetail.objects.create(trip=trip,
                                    post=item['post'])
        return trip


    def to_representation(self, instance):
        representation = super(TripSerializer, self).to_representation(instance)
        representation['user'] = instance.user.email
        representation['posts'] = TripDetailSerializer(instance.tripdetail.all(), many=True).data
        return representation
