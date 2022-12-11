from django.shortcuts import render, redirect
from django.views import View
from core.models import Photo, Person
from exif import Image


class PhotoList(View):

    def get(self, request):
        args = {}
        args['photos'] = Photo.objects.filter(user_id=request.user.id)
        args['username'] = request.user.username
        return log_in(request, 'core/photos.html', args)


class GetPhoto(View):

    def get(self, request, image_id):
        args = {}
        args['photo'] = Photo.objects.filter(user_id=request.user.id).filter(id=image_id)[0]
        args['persons'] = Person.objects.filter(photo_id=args['photo'].id)
        args['username'] = request.user.username
        return log_in(request, 'core/photo.html', args)


class PhotoAdd(View):

    def get(self, request):
        args = {}
        args['username'] = request.user.username
        return log_in(request, 'core/add_photo.html', args)

    def post(self, request):
        args = {}
        args['username'] = request.user.username
        args['photo_error'] = 'необходимо фото'
        image = request.FILES.get('image', None)
        if image == None:
            return log_in(request, 'core/add_photo.html', args)
        list_name = request.POST.getlist("name", None)
        list_surname = request.POST.getlist("surname", None)
        description = request.POST['description']
        geo_longitude = request.POST['geo_longitude']
        geo_latitude = request.POST['geo_latitude']
        geo_altitude = request.POST['geo_altitude']
        if request.POST.get('auto_geo') == None:
            args = get_gps(image)
            geo_longitude = args["longitude"]
            geo_latitude = args["latitude"]
            geo_altitude = args["altitude"]
        photo = Photo(
            user=request.user,
            description=description,
            geo_longitude=geo_longitude,
            geo_latitude=geo_latitude,
            geo_altitude=geo_altitude,
            image=request.FILES.get('image', None)
        )
        photo.save()
        for i in range(0, len(list_name)):
            person = Person(
                first_name=list_name[i],
                last_name=list_surname[i],
                photo=photo
            )
            person.save()
        return redirect("/photo_manager/")


class Filter(View):

    def get(self, request):
        args = {}
        args['username'] = request.user.username
        return log_in(request, 'core/filter.html', args)

    def post(self, request):
        args = {}
        args['data_start'] = request.POST.get('data_start')
        args['data_finish'] = request.POST.get('data_finish')
        args['start_geo_longitude'] = request.POST.get('start_geo_longitude')
        args['end_geo_longitude'] = request.POST.get('end_geo_longitude')
        args['start_geo_latitude'] = request.POST.get('start_geo_latitude')
        args['end_geo_latitude'] = request.POST.get('end_geo_latitude')
        args['start_geo_altitude'] = request.POST.get('start_geo_altitude')
        args['end_geo_altitude'] = request.POST.get('end_geo_altitude')
        args['first_name'] = request.POST.get('first_name')
        args['last_name'] = request.POST.get('last_name')
        args['username'] = request.user.username
        args['photos'] = Photo.objects.filter(user_id=request.user.id)
        if args['first_name']:
            persons = Person.objects.filter(first_name=args['first_name'])
            person_list = []
            for person in persons:
                person_list.append(person.photo.id)
            args['photos'] = args['photos'].filter(id__in=person_list)
        if args['last_name']:
            persons = Person.objects.filter(last_name=args['last_name'])
            person_list = []
            for person in persons:
                person_list.append(person.photo.id)
            args['photos'] = args['photos'].filter(id__in=person_list)
        if args['data_start']:
            args['photos'] = args['photos'].filter(date_of_download__gt=args['data_start'])
        if args['data_finish']:
            args['photos'] = args['photos'].filter(date_of_download__lt=args['data_finish'])
        if args['start_geo_longitude']:
            args['photos'] = args['photos'].filter(geo_longitude__gt=args['start_geo_longitude'])
        if args['end_geo_longitude']:
            args['photos'] = args['photos'].filter(geo_longitude__lt=args['end_geo_longitude'])
        if args['start_geo_latitude']:
            args['photos'] = args['photos'].filter(geo_latitude__gt=args['start_geo_latitude'])
        if args['end_geo_latitude']:
            args['photos'] = args['photos'].filter(geo_latitude__lt=args['end_geo_latitude'])
        if args['start_geo_altitude']:
            args['photos'] = args['photos'].filter(geo_altitude__gt=args['start_geo_altitude'])
        if args['end_geo_altitude']:
            args['photos'] = args['photos'].filter(geo_altitude__lt=args['end_geo_altitude'])
        return log_in(request, 'core/filter.html', args)


def log_in(request, template, args):
    if args['username'] != "":
        return render(request, template, args)
    else:
        return render(request, 'core/log_in.html', args)


def get_gps(file):
    image = Image(file)
    args = {}
    if image.has_exif:
        if image.gps_latitude_ref == 'N':
            args['latitude'] = image.gps_latitude[0] + image.gps_latitude[1] / 100 + image.gps_latitude[2] / 10000
        if image.gps_latitude_ref == 'S':
            args['latitude'] = (image.gps_latitude[0] + image.gps_latitude[1] / 100 + image.gps_latitude[
                2] / 10000) * -1
        if image.gps_longitude_ref == 'E':
            args['longitude'] = image.gps_longitude[0] + image.gps_longitude[1] / 100 + image.gps_longitude[2] / 10000
        if image.gps_longitude_ref == 'W':
            args['longitude'] = (image.gps_longitude[0] + image.gps_longitude[1] / 100 + image.gps_longitude[
                2] / 10000) * -1
        args['altitude'] = image.gps_altitude + image.gps_altitude_ref
    else:
        args['latitude'] = None
        args['longitude'] = None
        args['altitude'] = None
    return args
