import secrets

from rest_framework.serializers import (
    ModelSerializer,
    CharField,
    ValidationError,
    Serializer,
    SerializerMethodField,
)

from account.models import Account, ProfilePicture


class RegistrationSerializer(ModelSerializer):
    password2 = CharField(style={"input_type": 'password'}, write_only=True)

    class Meta:
        model = Account
        fields = ["first_name", "last_name", "email", "username", "password", "password2"]
        extra_kwargs = {"password2": {"write_only": True}}

    def validate(self, data):
        if not data.get('first_name'):
            raise ValidationError({'first_name': 'This field is required.'})
        if not data.get('last_name'):
            raise ValidationError({'last_name': 'This field is required.'})
        if not data.get('email'):
            raise ValidationError({'email': 'This field is required.'})
        if not data.get('username'):
            raise ValidationError({'username': 'This field is required.'})
        if not data.get('password'):
            raise ValidationError({'password': 'This field is required.'})
        if not data.get('password2'):
            raise ValidationError({'password2': 'This field is required.'})

        return data

    def save(self, **kwargs):

        first_name = self.validated_data["first_name"]
        last_name = self.validated_data["last_name"]
        email = self.validated_data["email"]
        username = self.validated_data["username"]
        password = self.validated_data["password"]
        password2 = self.validated_data["password2"]

        account = Account(
            first_name=first_name,
            last_name=last_name,
            email=email,
            username=username,
            about="Hello there, I am {f_name} {l_name}.".format(f_name=first_name, l_name=last_name)
        )

        if not secrets.compare_digest(password, password2):
            raise ValidationError({
                'response': 'error',
                "message": "Password doesn't matched."
            })
        account.set_password(password)
        account.save()
        return account


class LoginSerializer(Serializer):
    username = CharField(required=True)
    password = CharField(required=True)


class ProfilePictureSerializer(ModelSerializer):
    class Meta:
        model = ProfilePicture
        fields = ['image']


class ProfilePictureUploadSerializer(ModelSerializer):
    class Meta:
        model = ProfilePicture
        fields = ['user', 'image', 'timestamp']

    def save(self):

        try:
            image = self.validated_data['image']
            timestamp = self.validated_data['timestamp']

            profile_pic = ProfilePicture(
                user=self.validated_data['user'],
                image=image,
                timestamp=timestamp,
            )

            profile_pic.save()
            return profile_pic

        except KeyError:
            raise ValidationError({
                "response": "You must have all the fields not null."
            })


class AccountDetailSerializer(ModelSerializer):
    profile_picture = SerializerMethodField()

    class Meta:
        model = Account
        fields = [
            'id', 'first_name', 'last_name', 'phone', 'username', 'email', 'about',
            'dob', 'gender', "followers", "following", 'profile_picture', 'account_type'
        ]

    def get_profile_picture(self, obj):
        try:
            image = ProfilePicture.objects.filter(user=obj.id).order_by('-uploaded_at')[0]
        except (ProfilePicture.DoesNotExist, IndexError):
            image = ""

        serializer = ProfilePictureSerializer(image)

        return serializer.data


class AccountPropertiesSerializer(ModelSerializer):
    class Meta:
        model = Account
        fields = [
            "first_name", "last_name", "phone", "dob", 'gender',
            "account_type", "timestamp", "followers", "following", "about"
        ]

    # def validate(self, account):
    #     try:
    #         dob = account['dob']
    #
    #         diff = abs(datetime.date.today() - dob)
    #
    #         if (diff.days / 365) < 6:
    #             raise ValidationError({
    #                 'detail': "You are too young. Your age should be more than 6 years."
    #             })
    #
    #     except (KeyError, ValueError):
    #         raise ValidationError("An error occurred.")
    #     return account


class ChangePasswordSerializer(Serializer):
    old_password = CharField(required=True)
    new_password = CharField(required=True)
    confirm_new_password = CharField(required=True)
