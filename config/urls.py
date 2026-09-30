from django.contrib import admin
from django.contrib.auth import views as auth
from django.urls import path, include
urlpatterns = [
    path('admin/', admin.site.urls),
    path('masuk/', auth.LoginView.as_view(), name='login'),
    path('keluar/', auth.LogoutView.as_view(), name='logout'),
    path('', include('docs.urls')),
]
