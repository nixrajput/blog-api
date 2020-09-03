from rest_framework.serializers import (
    ModelSerializer,
    CharField,
    ValidationError,
)

from account.models import Account


class RegistrationSerializer(ModelSerializer):
    password2 = CharField(style={"input_type": 'password'}, write_only=True)

    class Meta:
        model = Account
        fields = ["email", "username", "password", "password2"]
        extra_kwargs = {"password2": {"write_only": True}}

    def save(self, **kwargs):
        account = Account(
            email=self.validated_data["email"],
            username=self.validated_data["username"],
        )
        password = self.validated_data["password"]
        password2 = self.validated_data["password2"]

        if password != password2:
            raise ValidationError({"password": "password must match."})
        account.set_password(password)
        account.save()
        return account


class AccountPropertiesSerializer(ModelSerializer):
    class Meta:
        model = Account
        fields = "__all__"