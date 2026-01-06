from django.contrib import admin
from .models import Question, Choice  # Импортируйте вашу модель

class QuestionAdmin(admin.ModelAdmin):
    list_display = ["question_text", "pub_date", "was_published_recently"]
    list_filter = ["pub_date"]
    search_fields = ["question_text"]

class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 3

# Зарегистрируйте модель, чтобы она появилась в админке
admin.site.register(Question, QuestionAdmin)