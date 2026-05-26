from django.contrib import admin
from .models import Question, Exam, Answer
# Register your models here.

@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'duration',
        'start_time',
        'entry_window'
    )

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'exam',
        'question',
        'correct_answer'
    )

    search_fields = (
        'question',
    )

    list_filter = (
        'exam',
    )

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'exam',
        'question',
        'selected_option',
        'selected_answer'
    )

    search_fields = (
        'user_username',
        'question_question'
    )

    list_filter = (
        'exam',
        'user'
    )