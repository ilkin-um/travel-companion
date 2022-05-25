from django.urls import path
from .views import TripList, TripDetail,CreateTrip,CreateCity,UpdateTrip,CityDetail,DeleteTrip,DeleteCity,TripLogin,UpdateCity,RegisterView
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', TripList.as_view(), name='trips'),
    path('login/', TripLogin.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('register/',RegisterView.as_view(),name='register'),
    path('trip/<int:pk>/',TripDetail.as_view(),name='trip'),
    path('trip-create/', CreateTrip.as_view(), name='trip-create'),
    path('trip-update/<int:pk>/', UpdateTrip.as_view(), name='trip-update'),
    path('trip-delete/<int:pk>/', DeleteTrip.as_view(), name='trip-delete'),
    path('city-update/<int:pk>/', UpdateCity.as_view(), name='city-update'),
    path('city-delete/<int:pk>/', DeleteCity.as_view(), name='city-delete'),
    path('city-create/<int:pk>', CreateCity.as_view(), name='city-create'),

    path('city/<int:pk>/', CityDetail.as_view(), name='city'),

]