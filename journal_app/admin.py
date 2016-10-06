from django.contrib import admin

# Register your models here.


from models import Journal, Journal_entry


# class JournalAdmin(admin.ModelAdmin):
# 	"""docstring for JournalAdmin"""
# 	class meta:
# 		model = Journal

admin.site.register(Journal)
admin.site.register(Journal_entry)
			



