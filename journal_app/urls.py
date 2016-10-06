from django.conf.urls import url, include
from .views import (
    get_all_journal_entries, get_journal_entry,
    create_journal_entry, JournalView, JournalEntryUpdateView, search_titles
)

urlpatterns = [
    url(r'^entry/', get_all_journal_entries, name='journal_entry'),
    url(r'^journal_entries/get/(?P<journal_id>\d+)/$', get_all_journal_entries),
    url(r'^journal_entry/get/(?P<journal_entry_id>\d+)/$', get_journal_entry),
    url(r'^journal_entries/create/', create_journal_entry, name='create_journal_entry'),
    url(r'^journal_view/', JournalView.as_view(), name = 'journal_vew'),
    url(r'^journal_entry_update/', JournalEntryUpdateView.as_view(), name='journal_entry_update'),
    url(r'^search/$', search_titles, name = 'journal_vew'),
]