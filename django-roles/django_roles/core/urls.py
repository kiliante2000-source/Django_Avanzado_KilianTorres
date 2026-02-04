from django.urls import path
from .views import (
    HomeView,
    PricingView,
    RegisterView,
    ProfileView,
    CustomLoginView,
    CourseListView,
    RegistrationListView,
    AttendanceListView,
    MarkListView,
)

urlpatterns = [
    # Página de inicio
    path("", HomeView.as_view(), name="home"),
    
    # Página de precios
    path("pricing/", PricingView.as_view(), name="pricing"),
    
    # Páginas de login y registro 
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", CustomLoginView.as_view(), name="custom_login"),
    
    # Página de perfil
    path("profile/", ProfileView.as_view(), name="profile"),
    
    # 📚 Páginas que administran los cursos
    path("courses/", CourseListView.as_view(), name="course_list"),
    
    # 📝 Inscripciones
    path("registrations/", RegistrationListView.as_view(), name="registration_list"),
    
    # 🕒 Asistencias
    path("attendance/", AttendanceListView.as_view(), name="attendance_list"),
    
    # 📊 Calificaciones
    path("marks/", MarkListView.as_view(), name="mark_list"),
]
