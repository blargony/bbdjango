from django.contrib import admin

from .models import GGQuestion, GGAnswer, GGUser

class GGAnswerInLine(admin.TabularInline):
    model = GGAnswer

class QuestionAdmin(admin.ModelAdmin):
    inlines = [ GGAnswerInLine, ]

class GGUserAdmin(admin.ModelAdmin):
    model = GGUser


admin.site.register(GGQuestion, QuestionAdmin)
admin.site.register(GGUser, GGUserAdmin)
