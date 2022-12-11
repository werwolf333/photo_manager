from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('registration/', views.RegistrationFormView.as_view(), name='Registration'),
    path('login/', views.LoginFormView.as_view(), name='Login'),
    path('login/logout/', views.Logout.as_view(), name='Logout'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
