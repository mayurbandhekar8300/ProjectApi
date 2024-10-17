
from django.http import JsonResponse  
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from .serializers import *
from firmadmin.models import *

from django.contrib.auth import authenticate
from django.contrib.auth.models import Group
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


# For Customizing JWT Token
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims
        token['username'] = user.username
        try:
            group = user.groups.get(name="firmadmin")
            admin = FirmAdminMOdel.objects.get(user_id=user.id)
            token['instituteName'] = admin.name
            return token
        except Exception as e:
            token['message'] = "Error 404"
            return token
                
                    
                        

        # ...

        

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
    
    
    

@api_view(['POST'])
@permission_classes([AllowAny])
def userLogin(request):
    serializer = UserLoginSerilizer(data=request.data)
    if serializer.is_valid():
        username = serializer.data.get('username')
        password = serializer.data.get('password')
        user = authenticate(username=username,password=password)
        if user is not None:
            serializer = UserProfileSerilizer(user,many=False)
            token = get_tokens_for_user(user)
            return Response({
                'statusCode':"01",
                'msg':'Login Successful',
                'token':token,
                'userProfile':serializer.data,
                })
        else:
            return Response({
                "statusCode":"00",
                'message':{
                    'non_field_errors':['Username Or Password is Not Valid']
                    },
                })
    else:
        return Response({
            "statusCode":"00",
            "message":serializer.errors,
            })




@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getAllItem(request):
    try:
        firmAdmin = FirmAdminMOdel.objects.get(user_id=request.user.id)
    except FirmAdminMOdel.DoesNotExist:
        return Response({
            "statusCode":"00",
            "data":[],
            "message":"user is not a allowed for this API!",
            })
    items = InventroyItemModel.objects.filter(
        is_deleted = 0,
        firmAdmin_id = firmAdmin.id
    )
    if items:
        serializer = InventroySerializer(items,many=True)
        return Response({
            "statusCode":"01",
            "data":serializer.data,
            "message":"success"
            })
    else:
        return Response({
            "statusCode":"00",
            "data":"No Item yet!",
            "message":"failed"
            })

        
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getItem(request,id):
    try:
        firmAdmin = FirmAdminMOdel.objects.get(user_id=request.user.id)
    except FirmAdminMOdel.DoesNotExist:
        return Response({
            "statusCode":"00",
            "data":[],
            "message":"user is not a allowed for this API!",
            })
    
    try:
        item = InventroyItemModel.objects.get(id=id)
        serializer = InventroySerializer(item,many=False)
        return Response({
            "statusCode":"01",
            "data":serializer.data,
            "message":"success"
            })
    except InventroyItemModel.DoesNotExist:
        return Response({
            "statusCode":"00",
            "data":"no data",
            "message":f"No Item with id {id}!"
            })



        

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createItem(request):
    try:
        firmAdmin = FirmAdminMOdel.objects.get(user_id=request.user.id)
    except FirmAdminMOdel.DoesNotExist:
        return Response({
            "statusCode":"00",
            "data":[],
            "message":"user is not a allowed for this API!",
            })
    data = request.data
    serializer = CreateItemSerializer(data=data)
    if serializer.is_valid():
        item,created = InventroyItemModel.objects.get_or_create(
            itemName = str(data['itemName']).strip(),
            firmAdmin_id = firmAdmin.id
            )
        if created:
            item.quantity = data['quantity']
            item.description = data['description']
            item.save()
            return Response({
                "statusCode":"01",
                "data":serializer.data,
                "message":"success"
                })
        else:
            item.is_deleted = 0
            item.save()
            return Response({
                "statusCode":"01",
                "data":serializer.data,
                "message":"success"
                })

    else:
        return Response({
            "statusCode":"00",
            "data": "",
            "message":serializer.errors
            })

        

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def updateItem(request,id):
    try:
        firmAdmin = FirmAdminMOdel.objects.get(user_id=request.user.id)
    except FirmAdminMOdel.DoesNotExist:
        return Response({
            "statusCode":"00",
            "data":[],
            "message":"user is not a allowed for this API!",
            })
    data = request.data
    try:
        item = InventroyItemModel.objects.get(id=id) 
    except InventroyItemModel.DoesNotExist:
        return Response({
            "statusCode":"00",
            "data": "",
            "message":f"no item with id {id}!"
            })
    serializer = CreateItemSerializer(instance=item,data=data)
    if serializer.is_valid():
        serializer.save()
        return Response({
            "statusCode":"01",
            "data":serializer.data,
            "message":"success"
            })
    else:
        return Response({
            "statusCode":"00",
            "data": "",
            "message":serializer.errors
            })


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def deleteItem(request,id):
    try:
        firmAdmin = FirmAdminMOdel.objects.get(user_id=request.user.id)
    except FirmAdminMOdel.DoesNotExist:
        return Response({
            "statusCode":"00",
            "data":[],
            "message":"user is not a allowed for this API!",
            })
    
    try:
        item = InventroyItemModel.objects.get(id=id)
        item.delete()
        return Response({
            "statusCode":"01",
            "message":"Item deleted successfully!",
            })

    except InventroyItemModel.DoesNotExist:
        return Response({
            "statusCode":"00",
            "data": "",
            "message":f"no item with id {id}!"
            })
   

        
