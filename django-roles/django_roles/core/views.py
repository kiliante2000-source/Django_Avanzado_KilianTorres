from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views.generic import TemplateView, ListView, DetailView
from .models import Course, Registration, Attendance, Mark
from django.contrib.auth.models import Group
from .forms import RegistrationForm as RegisterForm 
from django.views import View   

class CustomLoginView(TemplateView):
    group_name = None
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if user.is_authenticated:
            group = Group.objects.filter(user=user).first()
            if group:
                self.group_name = group.name
        context['group_name'] = self.group_name
        return context
    
# Página de inicio
class HomeView(TemplateView):
    template_name = 'home.html'

# Página de precios
class PricingView(TemplateView):
    template_name = 'pricing.html'
    
# Registro de usuario
class RegisterView(View):

    def get(self, request):
        data = {
            'form': RegisterForm()
        }
        return render(request, 'registration/register.html', data)

    def post(self, request):
        user_creation_form = RegisterForm(data=request.POST)

        if user_creation_form.is_valid():
            user_creation_form.save()

            user = authenticate(
                username=user_creation_form.cleaned_data['username'],
                password=user_creation_form.cleaned_data['password1']
            )
            login(request, user)
            return redirect('home')

        data = {
            'form': user_creation_form
        }
        return render(request, 'registration/register.html', data)
    
#     # Página de perfil
# class ProfileView(TemplateView):
#     template_name = 'profile/profile.html'
        
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         user = self.request.user

#         return context

class ProfileView(TemplateView):
    template_name = 'profile/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        if user.is_authenticated and user.groups.exists():
            group = user.groups.first()
            context["group_name"] = group.name
            context["group_name_singular"] = group.name[:-1] if group.name.endswith("s") else group.name
        else:
            context["group_name"] = None
            context["group_name_singular"] = None

        return context
    
class CourseListView(ListView):
    model = Course
    template_name = "courses/course_list.html"
    context_object_name = "courses"


class RegistrationListView(ListView):
    model = Registration
    template_name = "registrations/registration_list.html"
    context_object_name = "registrations"


class AttendanceListView(ListView):
    model = Attendance
    template_name = "attendance/attendance_list.html"
    context_object_name = "attendances"


class MarkListView(ListView):
    model = Mark
    template_name = "marks/mark_list.html"
    context_object_name = "marks"
