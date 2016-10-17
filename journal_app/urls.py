from django.conf.urls import url, include
from .views import (
    SaveJournalView, JournalView, JournalEntryDetailView, JournalEntryCreateView,
    JournalEntryEditView, JournalEntryDeleteView, EditJournalView, DeleteJournalView
)

urlpatterns = [
    url(r'^create_journal/', SaveJournalView.as_view(), name='create_journal'),
    url(r'^edit_journal/', EditJournalView.as_view(), name='edit_journal'),
    url(r'^delete_journal/', DeleteJournalView.as_view(), name='delete_journal'),
    url(r'^journal_entry/', JournalEntryDetailView.as_view(), name='journal_entry'),
    url(r'^journal_create_entry/', JournalEntryCreateView.as_view(), name='journal_create_entry'),
    url(r'^journal_edit_entry/', JournalEntryEditView.as_view(), name='journal_edit_entry'),
    url(r'^journal_view/', JournalView.as_view(), name = 'journal_vew'),
    url(r'^delete_entry_url/', JournalEntryDeleteView.as_view(), name='delete_entry_url'),
]