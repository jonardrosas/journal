from django.contrib import admin

# Register your models here.


from models import Journal, Journal_entry

admin.site.site_header = 'W.E.D Administration'

class JournalAdmin(admin.ModelAdmin):
    search_fields = ('name', 'description')
    list_display = ['__unicode__','created_by_field', 'date_created_field']

class JournalEntryAdmin(admin.ModelAdmin):
    search_fields = ('title', 'description')
    list_display = ['__unicode__','entry_date_created','get_journal','get_user']

    def get_user(self, obj):
        return obj.journal_id.created_by
    get_user.short_description = 'Created by'
    get_user.admin_order_field = 'journal_id__created_by'

    def get_journal(self, obj):
        return obj.journal_id.name
    get_journal.short_description = 'Journal'
    get_journal.admin_order_field = 'journal_id__name'

admin.site.register(Journal, JournalAdmin)
admin.site.register(Journal_entry, JournalEntryAdmin)



