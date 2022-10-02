from django.db import models
from django.contrib.auth.models import User



class Project(models.Model):
    """ Project, so a set of user that works together to build things by buying,
    using or consuming elements """
    name = models.CharField("name", max_length=40, blank=False, null=False)
    description = models.CharField("description", max_length=300, blank=True, null=False)
    image = models.ImageField(upload_to='project_images', blank=True, null=True)
    manager = models.ForeignKey(User, on_delete=models.PROTECT, null=True, related_name="managed_projects")
    users = models.ManyToManyField(User, related_name="projects")

    def __str__(self):
        return self.name