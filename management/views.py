from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Prefetch
import json
from dateutil import parser
from rest_framework import status
from rest_framework.response import Response
from rest_framework.parsers import JSONParser


from .models import *
from .serializers import *

# Create your views here.




class ConferenceDetails(APIView):
    
    def get(self,request):
        
        conferences = Conference.objects.all()
        serializer = ConferenceSerializers(conferences, many=True)
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    
    def post(self,request):
        data = JSONParser().parse(request)
        serializer = ConferenceSerializers(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self,request):
        
        try:
            data = JSONParser().parse(request)
            id = data.pop('id')
            update_congerence = Conference.objects.filter(
                id = id).update(
                    **data
                )
            
            data_ = {"update" :data }
            return Response(data_, status = status.HTTP_202_ACCEPTED)
        except:
            return Response({"message" : "failed"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class TalkDetails(APIView):

    def get(self,request):
        try:
            conference_id = request.data['conference_id'] 
            
            talks = Talk.objects.filter(
                conference_id__id = conference_id).prefetch_related(
                Prefetch(
                'public',
                to_attr='publics'
            )
                
            )
            serializer = TalksSerializers(talks, many=True)        
            
            data_ =[]
            for book in talks:
                temp_new =[]
                for i in range(len(book.publics)):
                    temp ={
                        'id' : book.publics[i].id,
                        'email_id' : book.publics[i].email_id,
                        'username' : book.publics[i].username,
                        'type' : book.publics[i].type
                    }
                    temp_new.append(temp)
                data_.append(temp_new)
            
            
            serializer = TalksSerializers(talks, many=True)
            for i in range(len(serializer.data)):

                serializer.data[i]['people'] = data_[i]      

            return Response(serializer.data,status=status.HTTP_202_ACCEPTED)
        except:
            return Response({"message" : "failed"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    def post(self,request):
        try:
            data = {
                'conference_id' : Conference.objects.get(id = request.data['conference_id']),
                'title' : request.data['title'],
                'description' : request.data['description'],
                
                'date_time' : parser.parse(request.data['date_time']),

            }
            talks = Talk.objects.create(**data)
            talks.save()
            for i in request.data['people']:
                p = People.objects.get(id=i)
                talks.public.add(p)

            talks.save()
            return Response({"message" : "created"},status=status.HTTP_201_CREATED)
        except:
            return Response({"message" : "failed"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class AddRemovePublic(APIView):

    def post(self,request):
        
        talk_id = request.data['talk']
        try:
            talk = Talk.objects.get(id = talk_id)

            if 'remove' in request.data:
                for i in request.data['remove']:
                    try:
                        talk.public.remove(People.objects.get(id=i))
                    except Exception as e:
                        return Response({"message" : f"not found {i} user"},status=status.HTTP_404_NOT_FOUND)


            if 'add' in request.data:
                for i in request.data['add']:
                    try:
                        people = People.objects.get(id=int(i))
                        talk.public.add(people)
                    except Exception as e:
                        print(e)
                        return Response({"message" : f"not found {i} user"},status=status.HTTP_404_NOT_FOUND)
            
        except:         
            return Response({"message" : f"not found {talk_id}"},status=status.HTTP_404_NOT_FOUND)
        
        return Response({"message" : "success"},status=status.HTTP_202_ACCEPTED)

class EditTalk(APIView):

    def put(self,request):
        
        data = JSONParser().parse(request)
        talk_id = data.pop('talk')
        data = Talk.objects.filter(
            id = talk_id
        ).update(
            **data
        )

        if data:
            return Response({"message" : "success"},status=status.HTTP_202_ACCEPTED)
        else:
            return Response({"message" : f"not found {talk_id}"},status=status.HTTP_404_NOT_FOUND)
