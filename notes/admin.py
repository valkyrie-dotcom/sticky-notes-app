# notes/admin.py
from django.contrib import admin
from .models import Note

# Note model
admin.site.register(Note)
