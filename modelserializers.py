from server import ma
from custommodels import UserModel

class UserModelSerializer(ma.ModelSchema):
  class Meta:
    model = UserModel