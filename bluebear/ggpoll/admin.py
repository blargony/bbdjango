from django.contrib import admin
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.safestring import mark_safe


from .models import GGQuestion, GGAnswer, GGUser, GGGroup, GGGroupWeight

class EditLinkToInlineObject():
    def link(self, instance):
        url = reverse('admin:%s_%s_change' % (
            instance._meta.app_label, instance._meta.model_name), args=[instance.pk])
        if instance.pk:
            return mark_safe(u'<a href="{u}">edit</a>'.format(u=url))
        else:
            return ''


class ManytoManyToInlineList():
    def list(self, instance):
        groups = instance.groups.all()
        if groups:
            summary = ', '.join([g.name for g in groups])
        else:
            summary = ''
        return summary


class GGAnswerInLine(EditLinkToInlineObject, ManytoManyToInlineList, admin.StackedInline):
    model = GGAnswer
    readonly_fields = ('link', 'list')


class GGGroupWeightInLine(admin.TabularInline):
    model = GGGroupWeight


class QuestionAdmin(admin.ModelAdmin):
    inlines = [GGAnswerInLine, ]


class GGAnswerAdmin(admin.ModelAdmin):
    inlines = [GGGroupWeightInLine, ]

    def response_post_save_change(self, request, obj):
        question_id = GGAnswer.objects.get(pk=obj.pk).question.id
        return redirect("/admin/ggpoll/ggquestion/%s/change/" % (question_id))


class GGUserAdmin(admin.ModelAdmin):
    model = GGUser


class GGGroupAdmin(admin.ModelAdmin):
    model = GGGroup


admin.site.register(GGQuestion, QuestionAdmin)
admin.site.register(GGAnswer, GGAnswerAdmin)
admin.site.register(GGUser, GGUserAdmin)
admin.site.register(GGGroup, GGGroupAdmin)
