from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('', views.PhotoList.as_view()),
    path('add/', views.PhotoAdd.as_view()),
    path('filter/', views.Filter.as_view()),
    path('<str:image_id>/', views.GetPhoto.as_view()),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
