from django.contrib.auth.models import User
from rest_auth.serializers import UserDetailsSerializer
from rest_framework import serializers
from .models import UserProfile, Apartment, ApartmentImages, Roomie
from django.contrib.auth import get_user_model
from rest_framework_gis.serializers import GeoFeatureModelSerializer


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        from django.core.files.base import ContentFile
        import base64
        import six
        import uuid

        # Check if this is a base64 string
        if isinstance(data, six.string_types):
            # Check if the base64 string is in the "data:" format
            if 'media' in data:
                prefix, suffix = data.split('/media/')
                return suffix

            if 'data:' in data and ';base64,' in data:
                # Break out the header from the base64 content
                header, data = data.split(';base64,')

            # Try to decode the file. Return validation error if it fails.
            try:
                decoded_file = base64.b64decode(data)
            except TypeError:
                self.fail('invalid_image')

            # Generate file name:
            file_name = str(uuid.uuid4())[:12]  # 12 characters are more than enough.
            # Get the file name extension:
            file_extension = self.get_file_extension(file_name, decoded_file)

            complete_file_name = "%s.%s" % (file_name, file_extension,)

            data = ContentFile(decoded_file, name=complete_file_name)

        return super(Base64ImageField, self).to_internal_value(data)

    def get_file_extension(self, file_name, decoded_file):
        import imghdr

        extension = imghdr.what(file_name, decoded_file)
        extension = "jpg" if extension == "jpeg" else extension

        return extension


class UserProfileSerializer(serializers.ModelSerializer):
    profileImg = Base64ImageField(max_length=None, use_url=True)

    class Meta:
        model = UserProfile
        fields = ('id', 'age', 'gender', 'cooking', 'cleanliness', 'smoking', 'alcohol', 'noise',
                  'socializing', 'uPets','sleep', 'foodPreference', 'profileImg', 'user')


class UserSerializer(serializers.ModelSerializer):
    uProfile = UserProfileSerializer()

    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'uProfile')


class AptImagesSerializer(serializers.ModelSerializer):
    image = Base64ImageField(max_length=None, use_url=True)

    class Meta:
        model = ApartmentImages
        fields = '__all__'


class ApartmentSerializer(serializers.ModelSerializer):
    aptImages = AptImagesSerializer(many=True)
    user = UserSerializer()

    class Meta:
        model = Apartment
        fields = ('id', 'address', 'desc', 'rooms', 'rent', 'utilities',  'vacancy', 'internet', 'gym',
                  'pets', 'smoking', 'dateMovin', 'duration', 'placeType', 'pool', 'wifi', 'location', 'gender', 'ageMin',
                  'ageMax','deposit', 'music', 'guests', 'drugs', 'lateNights', 'washer', 'dryer', 'furnished', 'kitchen',
                  'closet', 'airConditioner', 'heater', 'hasPet', 'aptImages','user')


class RoomieSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.id')

    class Meta:
        model = Roomie
        fields = ('id', 'dateMovin', 'otherRoomie', 'duration', 'roomie','user', 'roomieDesc', 'preferredLocation', 'uCost',
                  'roomieGender','roomieAgeMin','roomieAgeMax','roomieGenderOther')


class RoomieListSerializer(serializers.ModelSerializer):#GeoFeatureModelSerializer):#serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Roomie
        fields = ('id', 'dateMovin', 'otherRoomie', 'duration', 'roomieDesc', 'roomie','user', 'uCost','preferredLocation',
                  'roomieGender','roomieAgeMin','roomieAgeMax','roomieGenderOther')


class AddApartmentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.id')

    class Meta:
        model = Apartment
        fields = ('id','address', 'desc', 'rooms', 'rent', 'utilities',  'vacancy','internet','gym',
                  'pets','smoking', 'dateMovin','duration', 'placeType','pool', 'wifi','location','gender','ageMin','ageMax',
                  'deposit', 'music','guests', 'drugs', 'lateNights','washer', 'dryer','furnished' ,'kitchen',
                  'closet', 'airConditioner','heater','hasPet','user')


class UserCompleteSerializer(serializers.ModelSerializer):
    uProfile = UserProfileSerializer()
    roomie = RoomieSerializer()
    uApartments = ApartmentSerializer(many=True)

    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'last_login', 'date_joined', 'uProfile','roomie'
                  ,     'uApartments')


class UserUpdateSerializer(UserDetailsSerializer):
    age = serializers.IntegerField(source='uProfile.age')
    gender = serializers.CharField(source='uProfile.gender')
    profileImg = Base64ImageField(source='uProfile.profileImg', allow_empty_file=True, allow_null=True, use_url=True)
    # uCost = serializers.IntegerField(source='uProfile.uCost')
    cooking = serializers.IntegerField(source='uProfile.cooking')
    foodPreference = serializers.CharField(source='uProfile.foodPreference')
    # roomie = serializers.BooleanField(source='uProfile.roomie')
    cleanliness = serializers.CharField(source='uProfile.cleanliness')
    smoking = serializers.BooleanField(source='uProfile.smoking')
    alcohol = serializers.BooleanField(source='uProfile.alcohol')
    noise = serializers.CharField(source='uProfile.noise')
    socializing = serializers.CharField(source='uProfile.socializing')
    uPets = serializers.BooleanField(source='uProfile.uPets')
    sleep = serializers.CharField(source='uProfile.sleep')

    # dateMovin = serializers.DateField(source='uProfile.dateMovin', allow_null=True)
    # otherRoomie = serializers.BooleanField(source='uProfile.otherRoomie')
    # duration = serializers.CharField(source='uProfile.duration')

    class Meta(UserDetailsSerializer.Meta):
        fields = UserDetailsSerializer.Meta.fields + (
            'age', 'gender', 'profileImg', 'cooking', 'foodPreference', 'cleanliness', 'smoking', 'alcohol',
            'noise', 'socializing', 'uPets', 'sleep')
        # removed roomie details from the old setup
        # Added sleep to UserProfile

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('uProfile', {})
        age = profile_data.get('age')
        gender = profile_data.get('gender')
        profileimg = profile_data.get('profileImg')
        # uCost = profile_data.get('uCost')
        cooking = profile_data.get('cooking')
        foodPreference = profile_data.get('foodPreference')
        # roomie = profile_data.get('roomie')
        cleanliness = profile_data.get('cleanliness')
        smoking = profile_data.get('smoking')
        alcohol = profile_data.get('alcohol')
        noise = profile_data.get('noise')
        socializing = profile_data.get('socializing')
        uPets = profile_data.get('uPets')
        sleep = profile_data.get('sleep')
        # dateMovin = profile_data.get('dateMovin')
        # otherRoomie = profile_data.get('otherRoomie')
        # duration = profile_data.get('duration')

        instance = super(UserUpdateSerializer, self).update(instance, validated_data)
        profile = instance.uProfile

        profile.age = age
        profile.gender = gender
        profile.profileImg = profileimg
        # profile.uCost = uCost
        profile.cooking = cooking
        profile.foodPreference = foodPreference
        # profile.roomie = roomie
        profile.cleanliness = cleanliness
        profile.smoking = smoking
        profile.alcohol = alcohol
        profile.noise = noise
        profile.socializing = socializing
        profile.uPets = uPets
        profile.sleep = sleep
        # profile.dateMovin = dateMovin
        # profile.otherRoomie = otherRoomie
        # profile.duration = duration

        profile.save()
        return instance
