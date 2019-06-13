from django.contrib import admin
from . import models as m


@admin.register(m.Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text',)


@admin.register(m.Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ('choice_text', 'votes')
