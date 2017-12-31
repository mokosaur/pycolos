from django.contrib import admin

# Register your models here.
from pycolos.pycolos.models import Test, Question, Answer

admin.site.register(Test)
admin.site.register(Question)
admin.site.register(Answer)
