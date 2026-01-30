from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

# PERFIL DE USUARIO

class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile",
        verbose_name="Usuario"
    )
    image = models.ImageField(
        default="user/usuario_defecto.jpg",
        upload_to="user/",
        verbose_name="Imagen de perfil"
    )
    address = models.CharField(max_length=150, null=True, blank=True, verbose_name="Dirección")
    location = models.CharField(max_length=150, null=True, blank=True, verbose_name="Localidad")
    telephone = models.CharField(max_length=50, null=True, blank=True, verbose_name="Teléfono")

    class Meta:
        verbose_name = "Perfil"
        verbose_name_plural = "Perfiles"
        ordering = ["-id"]

    def __str__(self):
        return self.user.username


# -------- SIGNALS (MISMA LÓGICA, BIEN DEFINIDOS) --------

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


def save_user_profile(sender, instance, **kwargs):
    try:
        instance.profile.save()
    except Profile.DoesNotExist:
        pass


post_save.connect(create_user_profile, sender=User)
post_save.connect(save_user_profile, sender=User)
