from django.contrib import admin

# Register your models here.
from scoretracker.models import Game, Score, Row, Column
from django.contrib.auth.models import User


class GameAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
admin.site.register(Game, GameAdmin)
admin.site.register(Score)
admin.site.register(Row)
admin.site.register(Column)
# admin.site.register(User)