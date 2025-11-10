"""
URL configuration for airport_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from airlines.views import (
    AirlineListCreateView,
    AirplaneListCreateView,
    AirportListCreateView,
    CountryListCreateView,
    AirlineDetailView,
    AirplaneDetailView,
    AirportDetailView,
    CountryDetailView,
)   
from flights.views import (
    FlightListCreateView,
    FlightDetailView,
    TicketListCreateView,
    TicketDetailView,
)
from users.views import (
    UserListCreateView,
    UserDetailView,
)

schema_view = get_schema_view(
    openapi.Info(
        title="airport_project API",
        default_version='v1',
        description="API documentation for the airport_project",
        contact=openapi.Contact(email="mail@example.com"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny, ),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('admin/', admin.site.urls),
    path('airlines/', AirlineListCreateView.as_view(), name='airline-list-create'),
    path('airlines/<int:pk>/', AirlineDetailView.as_view(), name='airline-detail'),
    path('airplanes/', AirplaneListCreateView.as_view(), name='airplane-list-create'),
    path('airplanes/<int:pk>/', AirplaneDetailView.as_view(), name='airplane-detail'),
    path('airports/', AirportListCreateView.as_view(), name='airport-list-create'),
    path('airports/<int:pk>/', AirportDetailView.as_view(), name='airport-detail'),
    path('countries/', CountryListCreateView.as_view(), name='country-list-create'),
    path('countries/<int:pk>/', CountryDetailView.as_view(), name='country-detail'),
    path('flights/', FlightListCreateView.as_view(), name='flight-list-create'),
    path('flights/<int:pk>/', FlightDetailView.as_view(), name='flight-detail'),
    path('tickets/', TicketListCreateView.as_view(), name='ticket-list-create'),
    path('tickets/<int:pk>/', TicketDetailView.as_view(), name='ticket-detail'),
    path('users/', UserListCreateView.as_view(), name='user-list-create'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
]
