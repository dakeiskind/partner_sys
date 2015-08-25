from django.db import models
from viewflow.models import Process, Task
from django.contrib.auth.models import User

class HelloWorldProcess(Process):
    text = models.CharField(max_length=150)
    approved = models.BooleanField(default=False)
