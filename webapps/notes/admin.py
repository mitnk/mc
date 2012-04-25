from django.contrib import admin
from mitnkcom.webapps.notes.models import Note, Word


class NoteAdmin(admin.ModelAdmin):
    search_fields = ['text', 'remark', 'book', 'author']
    list_display = ("text", "added")

class WordAdmin(admin.ModelAdmin):
    search_fields = ['word']
    list_display = ("word", "added")

admin.site.register(Note, NoteAdmin)
admin.site.register(Word, WordAdmin)
