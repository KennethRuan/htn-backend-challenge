from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseBadRequest
from rest_framework import viewsets, generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Count

from .models import Hacker, Skill
from .serializers import HackerSerializer, SkillSerializer, SkillAggregationSerializer

import json

# Create your views here.
class HackerView(APIView):
    serializer_class = HackerSerializer

    def get_queryset(self):
        queryset = Hacker.objects.prefetch_related('skill_set')
        return queryset
    
    def list(self, request):
        queryset = self.get_queryset()
        serializer = HackerSerializer(queryset, many=True)
        return Response(serializer.data)

    def get(self, request, *args, **kwargs):
        '''
        The /users endpoint returns a list of all user data in JSON format
        The /users/<pk> endpoint returns a detail view of the specified user
        '''
        # If a primary key is provided in the request, a detail view will be provided
        if 'pk' in kwargs:
            hacker_obj = get_object_or_404(Hacker, pk=kwargs['pk'])
            serializer = HackerSerializer(hacker_obj)
            return Response(serializer.data)

        # If there are no parameters passed, the GET method will default to a list view
        return self.list(request)
        
    def put(self, request, *args, **kwargs):
        '''
        The /users/<pk> endpoint updates user data using the JSON in the PUT request
        If a user has new skills, they are added to the database
        '''
        
        try:
            data = json.loads(str(request.body, encoding='utf-8'))
            id = kwargs['pk']
            update_fields = {}

            # Parses JSON request to extract update fields
            for field, value in data.items():
                # If skills are provided they will be updated/created in the 'skills' table through the Skill model
                if field == 'skills':
                    for skill in data['skills']:
                        Skill.objects.update_or_create(
                            hacker_id=id,
                            name=skill['name'],
                            defaults={'rating':skill['rating']},
                        )
                # Otherwise, the fields will be processed to update the 'hacker' table
                else:
                    update_fields[field] = value

            # Unpacks the dictionary and updates the object, avoiding the need to query multiple times
            Hacker.objects.filter(pk=id).update(**update_fields)

            # Serialize data to JSON and return
            hacker_obj = Hacker.objects.get(pk=id)
            serializer = HackerSerializer(hacker_obj)
            return Response(serializer.data)

        except:
            return HttpResponseBadRequest()

class SkillView(APIView):
    def get_queryset(self):
        # Creates a queryset containing the skill name and its count, sorted in descending order
        queryset = Skill.objects.values('name').annotate(count=Count('name')).order_by('-count')
        return queryset

    def get(self, request, *args, **kwargs):
        '''
        The /skills endpoint shows a list of aggregate skills data with counts for each skill
        The /skills/?min_frequency={}&max_frequency={} endpoint allows for filtering of the results through query parameters
        '''

        # Extract query parameters from the request
        min_freq = request.GET.get('min_frequency')
        max_freq = request.GET.get('max_frequency')
        filter_fields = {}

        # Builds the filter fields, if both min_freq and max_freq are None, then no filtering is done
        if min_freq:
            filter_fields['count__gte'] = min_freq
        if max_freq:
            filter_fields['count__lte'] = max_freq
        
        # The filter fields are unpacked and applied to the queryset
        queryset = self.get_queryset()
        queryset = queryset.filter(**filter_fields)

        # Serialize data to JSON and return
        serializer = SkillAggregationSerializer(queryset, many=True)
        return Response(serializer.data)




