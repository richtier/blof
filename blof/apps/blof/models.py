#!/usr/bin/env python

from django.db import models
from django.contrib.auth.models import User


class PostModel(models.Model):    
    body = models.CharField(max_length=500)
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        User,
        blank = True,
        null = True,
        related_name='posts'
    )

    class Meta:
        ordering = ['-date']
        app_label = 'blof'