from journal_app.forms import *
import pdb
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from journal_app.models import Journal,Journal_entry
from django.contrib import auth
from django.core.context_processors import csrf
from django.contrib.auth.models import User
from forms import JournalEntryForm
from .models import Journal_entry, Journal
import json
from django.http import JsonResponse
from django.shortcuts import get_object_or_404


from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, permission_required
from django.views.generic import View, TemplateView

from utils.views import JSONResponseMixin


class JournalHomveView(TemplateView):
    template_name = "home.html"

    @method_decorator(login_required())
    def dispatch(self, *args, **kwargs):
        return super(JournalHomveView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(JournalHomveView, self).get_context_data(**kwargs)
        context['ngapp'] = "homeMod"
        return context


# To display all the journals created by the user logged in
class JournalView(JSONResponseMixin, View):
    response_data ={}

    def get(self, request, *args, **kwargs):
        response_data ={}
        journal_list = []
        journal_qlist = Journal.objects.filter(created_by=self.request.user).values()
        for journal in journal_qlist:
            journal_list.append(journal)
        response_data['data'] = journal_list
        print response_data
        return self.render_to_json_response(dict(response_data))


# To display all the journals created by the user logged in
class SaveJournalView(JSONResponseMixin, View):
    response_data ={}

    def post(self, request, *args, **kwargs):
        print "fff"
        response_data ={}
        post_body = json.loads(self.request.body)
        name = post_body['name']
        journal_type = post_body['type']
        if not name or not journal_type:
            response_data = {'msg': 'Name cannot be empty', 'status': 'error'}
        else:
            journal_qlist = Journal.objects.create(
                created_by=self.request.user,
                name=name
            )
            response_data = {'msg': 'Successfully Created', 'status': 'success'}
        return self.render_to_json_response(dict(response_data))
# To get all journal entries
@login_required
def get_all_journal_entries(request, journal_id=1):
    x=''
    journal = Journal.objects.filter(id=journal_id).values_list('name', flat=True).distinct()
    for journal_name in journal:
        x = journal_name

    args = {'journal_entries':Journal_entry.objects.distinct().filter(journal_id__created_by=request.user, journal_id_id=journal_id).order_by('-date_modified')
                      , 'user': request.user,
                    'journal_name':x}

    args.update(csrf(request))

    return render_to_response('journal_entries.html', args)


# To get one single journal entry
@login_required
def get_journal_entry(request, journal_entry_id=1):
    return render_to_response('update_journal_entry.html',
                              {'journal_entry':Journal_entry.objects.get(id=journal_entry_id),
                               'user': request.user})


@login_required
def create_journal_entry(request, journal_id=None):
    if request.POST:
        form = JournalEntryForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/home/') #Should redirect to entries page
    else:
        form = JournalEntryForm(request.POST)
    args = {'user': request.user,}
    args.update(csrf(request))
    args['form']=form

    return render_to_response('create_journal_entry.html', args)


class JournalEntryUpdateView(JSONResponseMixin, View):

    def post(self, request, *args, **kwargs):
        post_body= json.loads(self.request.body)
        title = post_body['title']
        description = post_body['description']
        journal_entry_id = post_body['journal_id']

        try:
            journal_entry_object = Journal_entry.objects.get(id=journal_entry_id)
        except:
            journal_entry_object=[]
        else:
            journal_entry_object.title = title
            journal_entry_object.description=description
            journal_entry_object.save()


@login_required
def search_titles(request):
    if request.method == "POST":
        search_text = request.POST['search_text']
    else:
        search_text = ''
    journal_entries = Journal_entry.objects.filter(title__contains=search_text)

    return render_to_response('ajax_search.html', {'journal_entries': journal_entries})
