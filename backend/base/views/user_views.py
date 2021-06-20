from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from django.contrib.auth.models import User
from base.serializers import ProductSerializer, UserSerializer, UserSerializerWithToken
# Create your views here.
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from django.contrib.auth.hashers import make_password
from rest_framework import status


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    # @classmethod
    # def get_token(cls, user):
    #     # it gets data from the user object
    #     token = super().get_token(user)

    #     # Add custom claims
    #     token['username'] = user.username
    #     token['msg'] = 'hello world!'
    #     token['password']=user.password
    #     # ...

    #     return token


    # in this we can directly get credentials of user without decoding the token
    def validate(self, attrs):
        data = super().validate(attrs)
        print(data)

        serializer=UserSerializerWithToken(self.user).data
        for k,v in serializer.items():
            data[k]=v


        # this below one is same as the above

        # refresh = self.get_token(self.user)
        # data['refresh'] = str(refresh)
        # data['access'] = str(refresh.access_token)
        # data['username']=self.user.username
        # data['email']=self.user.email
        # data['isAdmin']=self.user.is_staff
        return data

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer




"""For user Registration"""
serializer_class=UserSerializerWithToken
@api_view(['POST'])
def registerUser(request):
    data=request.data
    try:
        user=User.objects.create(
            first_name=data['name'],
            username=data['email'],
            email=data['email'],
            password=make_password(data['password'])
        )

        serializer=UserSerializerWithToken(user,many=False)
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    except:
        message = {'detail': 'User with this email already exists'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)






"""For admin to see all the user details and only in restricted mode"""
# /api/users/profile/
# it will get data from the token sent back from client
#this view can be seen by both admin and authenticated user
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUserProfile(request):
    user=request.user
    serializer=UserSerializer(user,many=False)
    return Response(serializer.data)


"""update the user profile by authenticated user"""
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateUserProfile(request):
    user = request.user
    serializer = UserSerializerWithToken(user, many=False)

    data = request.data
    user.first_name = data['name']
    user.username = data['email']
    user.email = data['email']

    if data['password'] != '':
        user.password = make_password(data['password'])

    user.save()

    return Response(serializer.data)




#see all the users
#restricted only see by admin
serializer_class=UserSerializer
@api_view(['GET'])
@permission_classes([IsAdminUser])
def getUsers(request):
    users=User.objects.all()
    serializer=UserSerializer(users,many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def getUserById(request,pk):
    user=User.objects.get(id=pk)
    serializer=UserSerializer(user,many=False)
    return Response(serializer.data)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateUser(request,pk):
    user=User.objects.get(id=pk)


    data = request.data

    user.first_name = data['name']
    user.username = data['email']
    user.email = data['email']
    user.is_staff=data['isAdmin']

    user.save()
    serializer = UserSerializer(user, many=False)

    return Response(serializer.data)





@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def deleteUser(request,pk):
    userForDeletion=User.objects.get(id=pk)
    userForDeletion.delete()
    return Response('User was deleted')

