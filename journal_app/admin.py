from django.contrib import admin

# Register your models here.


from models import Journal, Journal_entry


class JournalAdmin(admin.ModelAdmin):
    search_fields = ('name', 'description')

class JournalEntryAdmin(admin.ModelAdmin):
    search_fields = ('title', 'description')

admin.site.register(Journal, JournalAdmin)
admin.site.register(Journal_entry, JournalEntryAdmin)



