from journal_app.forms import *
import datetime
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
from .models import Journal_entry, Journal
import json
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.forms.models import model_to_dict


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
        response_data ={}
        post_body = json.loads(self.request.body)
        name = post_body['name']
        description = post_body['description']
        if not name or not description:
            response_data = {'msg': 'Name cannot be empty', 'status': 'error'}
        else:
            journal_qlist = Journal.objects.create(
                created_by=self.request.user,
                name=name,
                description = description
            )
            response_data = {'msg': 'Successfully Created', 'status': 'success'}
        return self.render_to_json_response(dict(response_data))


class JournalEntryDetailView(JSONResponseMixin, View):

    def post(self, request, *args, **kwargs):
        context_dict = {}
        post_body = json.loads(self.request.body)
        journal_id = post_body['journal_id']
        journal_ins = Journal.objects.get(id=int(journal_id))
        entries = journal_ins.journal_entry.values()
        final_list = []
        for entry in entries:
            initial_data = {}
            for k, v in entry.items():
                if k in ['date_created', 'date_modified']:
                    initial_data[k] = str(datetime.datetime.strftime(v, '%c'))
                else:
                    initial_data[k] = str(v)
            final_list.append(initial_data)
        context_dict['data'] = final_list
        context_dict['journal_name'] = journal_ins.name;
        context_dict['journal_date_created'] = str(datetime.datetime.strftime(journal_ins.date_created, '%c'));
        return self.render_to_json_response(context_dict)


class JournalEntryCreateView(JSONResponseMixin, View):

    def post(self, request, *args, **kwargs):
        context_dict = {}
        post_body = json.loads(self.request.body)
        journal_id = post_body['journal_id']
        title = post_body['title']
        description = post_body['description']
        data = None
        status = 'error'
        try:
            journal_ins = Journal.objects.get(id=int(journal_id))
        except Journal.DoesNotExist:
            msg = "The Entry Does Exists!"
        else:
            if journal_ins.journal_entry.filter(title=title).exists():
                msg = "The entry title already exists!"
            else:
                entry_ins = journal_ins.journal_entry.create(
                    title=title,
                    description=description
                )
                data = model_to_dict(entry_ins)
                msg = 'Successfully Created Entry'
                status = 'success'
        context_dict['data'] = {
            'msg': msg,
            'data': data,
            'status': status
        }
        return self.render_to_json_response(context_dict)


class JournalEntryEditView(JSONResponseMixin, View):

    def get(self, request, *args, **kwargs):
        context_dict = {}
        status = "error"
        entry_id = self.request.GET['entry_id']
        try:
            entry_ins = Journal_entry.objects.get(id=int(entry_id))
        except Journal_entry.DoesNotExist:
            msg = 'The Entry was already deleted!'
        else:
            msg = "Pulled succesfully!"
            status = "error"
        context_dict['data'] = {
            'data': model_to_dict(entry_ins),
            'msg': msg,
            'status': status

        }
        return self.render_to_json_response(context_dict)

    def post(self, request, *args, **kwargs):
        context_dict = {}
        status = 'error'
        post_body = json.loads(self.request.body)
        entry_id = post_body['entry_id']
        print entry_id
        title = post_body['title']
        description = post_body['description']
        try:
            entry_ins = Journal_entry.objects.get(id=int(entry_id))
        except Journal_entry.DoesNotExist:
            msg = 'The Entry was already deleted!'
        else:

                entry_ins.title = title
                entry_ins.description = description
                entry_ins.save()
                msg = "Successfully updated!"
                status = 'success'
        context_dict['data'] = {
            'data': model_to_dict(entry_ins),
            'msg': msg,
            'status': status
        }
        return self.render_to_json_response(context_dict)


class JournalEntryDeleteView(JSONResponseMixin, View):

    def post(self, request, *args, **kwargs):
        context_dict = {}
        msg = ""
        print "this is a delete"
        post_body = json.loads(self.request.body)
        entry_list = post_body['entry_id']
        entry_list = [int(entry_id) for entry_id in entry_list]
        entry_qset = Journal_entry.objects.filter(id__in=entry_list)
        if entry_qset:
            entry_qset.delete()
            msg = "Successfully Deleted."
        context_dict['data'] = {
            'msg': msg
        }
        return self.render_to_json_response(context_dict)


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
