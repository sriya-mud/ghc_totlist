from django.db import models

class Task(models.Model):
    task = models.TextField()
    date = models.DateField()

    def __str__(self):
        return self.task

