from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer, UserSerializer as BaseUserSerializer

class UserSerializer(BaseUserSerializer):  # this is for 'me' route like getting current user
    class Meta(BaseUserCreateSerializer.Meta):
        fields = ['id','username','email','first_name','last_name']


class UserCreateSerializer(BaseUserCreateSerializer):  # this is for creating new user
    # birth_date = serializers.DateField()
    class Meta(BaseUserCreateSerializer.Meta):
        fields = ['id','username','email','password','first_name','last_name']   # 'birth_date'