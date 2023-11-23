from rest_framework import serializers
from .models import User, UserProfile

class UserProfileSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)
    email = serializers.CharField(source='user.email', read_only=True)

    class Meta:
        model = UserProfile
        fields = (
            'first_name',
            'last_name',
            'email',
            'address',
            'addressline2',
            'phone_number',
            'city_or_town',
            'state_province_region',
            'zip_code',
            'age_range',
            'profession',
            'dress_code',
            'dress_code_description',
            'upcoming_events',
            'upcoming_events_description',
            'activity',
            'activity_items',
            'activity_frequency',
            'sports_fan',
            'sports_team',
            'description_items',
            'outdoor_activities',
            'fashion_goals',
            'attention_points',
            'image_base64',
        )

class UserSerializer(serializers.ModelSerializer):
    userprofile = UserProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password', 'userprofile']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = self.Meta.model(**validated_data)
        if password is not None:
            user.set_password(password)
        user.save()
        return user

class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()