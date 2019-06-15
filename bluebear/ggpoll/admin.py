from django.contrib import admin

from .models import Question, Answer, GGUser

class AnswerInLine(admin.TabularInline):
    model = Answer

class QuestionAdmin(admin.ModelAdmin):
    inlines = [ AnswerInLine, ]

class GGUserAdmin(admin.ModelAdmin):
    model = GGUser


admin.site.register(Question, QuestionAdmin)
admin.site.register(GGUser, GGUserAdmin)
