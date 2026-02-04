from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver    

# Cursos
class Course(models.Model):
    name = models.CharField(max_length=90, verbose_name='Nombre del curso')
    description = models.TextField(blank=True, null=True, verbose_name='Descripción del curso')
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'groups__name': 'Profesores'}, verbose_name='Profesor')
    class_quantity = models.PositiveIntegerField(default=0, verbose_name='Cantidad de clases')

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Curso'
        verbose_name_plural = 'Cursos'
        
# Incripciones
class Registration(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='students_registration',limit_choices_to={'groups__name': 'Estudiantes'}, verbose_name='Estudiante')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Curso')
    registration_date = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de inscripción')
    enabled = models.BooleanField(default=True, verbose_name='Alumno regular')

    def __str__(self):
        return f"{self.student.username} - {self.course.name}"
    
    class Meta:
        verbose_name = 'Inscripción'
        verbose_name_plural = 'Inscripciones'
        
# Asistencias
class Attendance(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Curso')
    student = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'groups__name': 'Estudiantes'},
    verbose_name = 'Estudiante')
    registration = models.ForeignKey(Registration, on_delete=models.CASCADE, verbose_name='Inscripción')
    date = models.DateField(verbose_name='Fecha de asistencia')
    present = models.BooleanField(default=False, verbose_name='Presente')

    def __str__(self):
        return f"{self.registration.student.username} - {self.date} - {'Presente' if self.present else 'Ausente'}"
    
    #lógica para generar el estado del alumno regular / irregular (enabled)
    # total-asistencias == total-clases => class_quantity del modelo Course
    # total-inasistencias => attendance -> present = False
    # porcentaje-inasistencias = (total-inasistencias / total-clases) * 100 --------> >20 (20%) => alumno es irregular => enabled = False
    # total-clases = 10
    # total-inasistencias = 4
    # porcentaje-inasistencias = (4 / 10) * 100 = 40% => alumno es irregular => enabled = False
    
    def update_registration_status(self):
        course_instance = Course.objects.get(id=self.course.id)
        total_classes = course_instance.class_quantity
        total_absences = Attendance.objects.filter(
            registration__student=self.student,
            course=self.course,
            present=False
        ).count()
        absences_present = (total_absences / total_classes) * 100
        
        registration = Registration.objects.get(student=self.student, course=self.course)
        
        if absences_present > 20:
            registration.enabled = False
        else:
            registration.enabled = True
            
        registration.save()
        
    class Meta:
        verbose_name = 'Asistencia'
        verbose_name_plural = 'Asistencias'
        
# Calificaciones
class Mark(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'groups__name': 'Estudiantes'}, verbose_name='Estudiante')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Curso')
    mark_1 = models.PositiveIntegerField(null=True, blank=True, verbose_name='Calificación 1')
    mark_2 = models.PositiveIntegerField(null=True, blank=True, verbose_name='Calificación 2')
    mark_3 = models.PositiveIntegerField(null=True, blank=True, verbose_name='Calificación 3')
    # average = models.FloatField(max_digits=3, decimal_places=1, null=True, blank=True, verbose_name='Promedio')
    average = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True, verbose_name='Promedio')
    

    def __str__(self):
        return str(self.course)
    
    # Calcular el promedio (llamo a una función)
    def calculate_average(self):
        marks = [self.mark_1, self.mark_2, self.mark_3]
        valid_marks = [mark for mark in marks if mark is not None]
        if valid_marks:
            return sum(valid_marks) / len(valid_marks)
        return None
    
    def save(self, *args, **kwargs):
        # Verifico si alguna nota cambió para recalcular el promedio
        if self. mark_1 or self.mark_2 or self.mark_3:
            self.average = self.calculate_average()
        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name = 'Calificación'
        verbose_name_plural = 'Calificaciones'
        
@receiver(post_save, sender=Attendance)
# @receiver(post_delete, sender=Attendance)
def update_registration_status_on_attendance_change(sender, instance, **kwargs):
    instance.update_registration_status()