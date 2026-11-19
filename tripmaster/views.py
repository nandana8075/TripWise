from django.shortcuts import render,get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from tripmaster.serializers import UserSerializer,TripSerializer,TripMemberSerializer
from tripmaster.models import TripDb,TripMemberDb
from rest_framework import authentication,permissions
from tripmaster.permissions import OwnerOnly
from rest_framework.exceptions import PermissionDenied


class SignUpView(APIView):
    def post(self,request):
        form_data=request.data
        serializer_instance=UserSerializer(data=form_data)
        if serializer_instance.is_valid():
            serializer_instance.save()
            return Response({"message":"user created successfully"},status=400)
        return Response ({"message":"Invalid data provided"},status=400)

class UserListView(APIView):
    def get(self,request):
        users=User.objects.all()
        serializer_instance=UserSerializer(users,many=True)
        return Response(serializer_instance.data,status=200)

class TripListCreateView(APIView):
    authentication_classes=[authentication.BasicAuthentication]
    permission_classes=[permissions.IsAuthenticated]


    def get(self,request):
        qs=TripDb.objects.filter(created_by=request.user)
        serializer_instance=TripSerializer(qs,many=True)
        return Response(data=serializer_instance.data)

    def post(self,request):
        form_data=request.data
        serializer_instance=TripSerializer(data=form_data)
        if serializer_instance.is_valid():
            serializer_instance.save(created_by=request.user)
            return Response(data={
                "message":"trip created successfully",
                "trip details":serializer_instance.data
            })
        else:
            return Response(data=serializer_instance.errors)

class TripRetriveUpdateDelete(APIView):
    authentication_classes=[authentication.BasicAuthentication]
    permission_classes=[OwnerOnly]

    def get(self,request,pk):
        trip_object=get_object_or_404(TripDb,id=pk)
        if trip_object.created_by==request.user:
            serializer_instance=TripSerializer(trip_object)
            return Response(data=serializer_instance.data,status=200)
        else:
            return Response(data={
                "Message":"Access Denied"
            })

    def put(self,request,pk):
        trip_object=get_object_or_404(TripDb,id=pk)
        if trip_object.created_by==request.user:
            form_data=request.data
            serializer_instance=TripSerializer(data=form_data,instance=trip_object)
            if serializer_instance.is_valid():
                serializer_instance.save()
                return Response(data={
                    "message":"Trip details updated successfully"
                     })
            else:
                return Response(data=serializer_instance.errors)
        else:
            return Response({"message":"you are not allowed to access this"})
                    
        
    def delete(self,request,pk):
        trip_object=get_object_or_404(TripDb,id=pk)

        if trip_object.created_by==request.user:
            trip_object.delete()
            return Response({
                "message":"deleted successfully"
                 })
        else:
            return Response({"message":"you are not allowed to access this"})
        

class TripMemberListCreateView(APIView):
    authentication_classes=[authentication.BasicAuthentication]
    permission_classes=[OwnerOnly]
    def get(self,request,trip_id):
        trip_object=get_object_or_404(TripDb,id=trip_id)
        is_owner=trip_object.created_by==request.user
        is_member=TripMemberDb.objects.filter(trip=trip_object,user=request.user).exists()
        if not(is_owner or is_member):
            raise PermissionDenied("you are not allowed to access this trip...!")
        else:
            members=TripMemberDb.objects.filter(trip=trip_object)
            serializer_instance=TripMemberSerializer(members,many=True)
            return Response (data=serializer_instance.data,status=200)

    def post(self,request,trip_id):
        trip_object=get_object_or_404(TripDb,id=trip_id)
        if trip_object.created_by!=request.user:
            raise PermissionDenied("only trip owner can add memebers....!")
        else:
            form_data=request.data
            serializer_instance=TripMemberSerializer(data=form_data,context={'trip':trip_object})
            if serializer_instance.is_valid():
                serializer_instance.save()
                return Response(data={
                    "messgae":"member added successfully...!"
                })
            else:
                return Response(data=serializer_instance.errors)
class MemberDeleteView(APIView):
    authentication_classes=[authentication.BasicAuthentication]
    permission_classes=[OwnerOnly]

    def delete(self,request,trip_id,member_id):
        trip_object=get_object_or_404(TripDb,id=trip_id)
        if trip_object.created_by!=request.user:
            raise PermissionDenied("only trip owner can remove members..!")
        else:
            member_object=get_object_or_404(TripMemberDb,id=member_id)
            member_object.delete()
            return Response (data={
                "message":"member deleted successfully..!"
            })
    
    
        

            
            
            


    



        
        

        







