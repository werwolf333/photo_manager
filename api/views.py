from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from core.models import Photo, Person


class MyList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, name):
        photos = Photo.objects.filter(user_id=request.user.id)
        photo_list = []
        for photo in photos:
            photo_list.append(photo.id)
        persons = Person.objects.filter(photo_id__in=photo_list).filter(first_name__contains=name)[:5]
        person_list = []
        for person in persons:
            person_list.append(person.first_name)
        person_list = set(person_list)
        return Response({'message': person_list}, status=201)
