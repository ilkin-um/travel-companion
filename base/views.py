from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView, FormView
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import redirect, reverse, get_object_or_404
from django.urls import reverse_lazy
from .models import Trip, City
from extra_views import CreateWithInlinesView, UpdateWithInlinesView, InlineFormSetFactory


'''
Login and registration views
'''


# Inherits default LoginView of Django
class TripLogin(LoginView):
    fields = '__all__'
    redirect_authenticated_user = True
    template_name = 'base/login.html'

    # When user logged in, redirects them to main page
    def get_success_url(self):
        return reverse_lazy('trips')


# Inherits default FormView of Django
class RegisterView(FormView):
    template_name = 'base/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('trips')

    # After registering, user is logged in automatically.

    def form_valid(self, form):
        user = form.save()
        if user:
            login(self.request, user)
        return super(RegisterView, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('trips')
        return super(RegisterView, self).get(*args, **kwargs)


# Inline view to display/edit Trip and City models together.
class CityInline(InlineFormSetFactory):
    model = City
    fields = ["city_name"]


'''
CRUD operations on Trip model. 
'''


# Returns list of all trips
class TripList(LoginRequiredMixin, ListView):
    model = Trip
    context_object_name = "trips"

    # Ensures that user sees only their own trips.

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['trips'] = context['trips'].filter(user=self.request.user)
        context['count'] = context['trips'].filter(user=self.request.user).count()
        return context


# Displays a single Trip.
class TripDetail(LoginRequiredMixin, DetailView):
    model = Trip
    context_object_name = "trip"
    template_name = 'base/trip.html'

    # User can only see their own trips.
    def get_queryset(self):
        user = self.request.user
        queryset = Trip.objects.filter(user=user)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cities'] = City.objects.filter(trip_id=self.object.trip_id)
        return context


class CreateTrip(LoginRequiredMixin, CreateWithInlinesView):
    model = Trip
    fields = ["trip_title", "people_included", "start_date",
              "end_date", "cost", "currency", "description"]
    success_url = reverse_lazy('trips')
    inlines = [CityInline]
    context_object_name = "whole_trip"

    # User can only create their own trips.
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(CreateTrip, self).form_valid(form)


class UpdateTrip(LoginRequiredMixin, UpdateWithInlinesView):
    model = Trip
    fields = ["trip_title", "people_included", "start_date",
              "end_date", "cost", "currency", "description"]
    inlines = [CityInline]
    success_url = reverse_lazy('trips')


class DeleteTrip(LoginRequiredMixin, DeleteView):
    model = Trip
    context_object_name = "trip"
    success_url = reverse_lazy('trips')


'''
CRUD operations on City model in order to manage it separately.
'''


class CityDetail(LoginRequiredMixin, DetailView):
    model = City
    context_object_name = "city"
    template_name = 'base/city.html'

    # Ensuring that user sees only their own trips.
    def get_queryset(self):
        user = self.request.user
        queryset = Trip.objects.filter(user=user)
        return queryset


class CreateCity(LoginRequiredMixin, CreateView):
    model = City
    fields = ["city_name"]
    success_url = reverse_lazy('trips')
    context_object_name = "city"

    # New city is bound to its trip by trip_id.
    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.trip_id = self.kwargs.get('pk')
        return super(CreateCity, self).form_valid(form)


class UpdateCity(LoginRequiredMixin, UpdateView):
    model = City
    fields = ["city_name"]
    success_url = reverse_lazy('trips')


class DeleteCity(LoginRequiredMixin, DeleteView):
    model = City
    context_object_name = "city"
    success_url = reverse_lazy('trips')
