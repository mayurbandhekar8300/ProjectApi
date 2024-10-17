from rest_framework import  serializers
from firmadmin.models import *


    
class UserLoginSerilizer(serializers.ModelSerializer):
    username = serializers.EmailField(max_length=250)
    class Meta:
        model = User
        fields = ['username','password']


class UserProfileSerilizer(serializers.ModelSerializer):
    userDetails = serializers.SerializerMethodField('get_details')
    class Meta:
        model = User
        fields = ['userDetails']
    def get_details(self,user):
        try:
            admin = FirmAdminMOdel.objects.get(user_id=user.id)
            name = admin.name
            email=admin.email
            return{
                "email":email,
                "id":admin.id,
                "name":name
            }
        except Exception as exp:
            print(exp)



class CreateItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventroyItemModel
        fields = ["id","itemName","description",'quantity']

class InventroySerializer(serializers.ModelSerializer):
    details = serializers.SerializerMethodField('get_details')
    class Meta:
        model = InventroyItemModel
        fields = ["details"]
    def get_details(self,item):
        id = item.id
        if item.itemName:
            itemName = item.itemName
        else:
            itemName = "NA" 
        
        if item.description:      
            description = item.description
        else:   
            description = "NA"
        
        if item.quantity:     
            quantity = item.quantity 
        else:
            quantity=0
            
        
        return {
            "id":id,
            "itemName":itemName,
            "description":description,
            "quantity":quantity,
            
        }



