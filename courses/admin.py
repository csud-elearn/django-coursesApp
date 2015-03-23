from django.contrib import admin
from courses.models import Course, Page, Section, Status, Chapter, Theme

# ajoute des modèles à la zone admin
admin.site.register(Course)
admin.site.register(Page)
admin.site.register(Section)
admin.site.register(Status)
admin.site.register(Chapter)
admin.site.register(Theme)