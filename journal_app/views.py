from journal_app.forms import *
import datetime
import pdb
from django.db.models import Q
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
        return self.render_to_json_response(dict(response_data))


# To display all the journals created by the user logged in
class SaveJournalView(JSONResponseMixin, View):
    response_data ={}



    def post(self, request, *args, **kwargs):
        response_data ={}
        status = "error"
        post_body = json.loads(self.request.body)
        name = post_body['name']
        description = post_body['description']
        if not name or not description:
            response_data = {'msg': 'Name cannot be empty', 'status': 'error'}
        else:
            if Journal.objects.filter(name=name, created_by=self.request.user).exists():
                msg = "Journal Already Exists!"
            else:
                journal_qlist = Journal.objects.create(
                    created_by=self.request.user,
                    name=name,
                    description = description
                )
                msg = "Successfully Created"
                status = "success"
            response_data = {'msg': msg, 'status': status}
        return self.render_to_json_response(dict(response_data))


class EditJournalView(JSONResponseMixin, View):
    response_data ={}

    def get(self, request, *args, **kwargs):
        response_data ={}
        status = "error"
        data = None
        journal_id = self.request.GET['journal_id']
        try:
            journal_ins = Journal.objects.get(id=int(journal_id))
        except Journal.DoesNotExist:
            msg = "Journal Already Exists!"
        else:
            msg = "Successfully Retreived!"
            status = "success"
            data = model_to_dict(journal_ins)
        response_data = {'msg': msg, 'status': status, 'data': data}
        return self.render_to_json_response(dict(response_data))


    def post(self, request, *args, **kwargs):
        response_data ={}
        status = "error"
        post_body = json.loads(self.request.body)
        journal_id = post_body['journal_id']
        name = post_body['name']
        description = post_body['description']
        if not name or not description:
            response_data = {'msg': 'Name cannot be empty', 'status': 'error'}
        else:
            try:
                journal_ins = Journal.objects.get(id=int(journal_id))
            except Journal.DoesNotExist:
                msg = "Journal Does not exist!"
            else:
                journal_ins.name = name
                journal_ins.description = description
                journal_ins.save()
                msg = "Successfully Updated!"
                status = "success"
            response_data = {'msg': msg, 'status': status}
        return self.render_to_json_response(dict(response_data))


class DeleteJournalView(JSONResponseMixin, View):
    response_data ={}

    def post(self, request, *args, **kwargs):
        response_data ={}
        status = "error"
        post_body = json.loads(self.request.body)
        journal_id = post_body['journal_id']
        try:
            journal_ins = Journal.objects.get(id=int(journal_id))
        except Journal.DoesNotExist:
            msg = "Journal Does not exist!"
        else:
            journal_ins.delete()
            msg = "Successfully Deleted!"
            status = "success"
        response_data = {'msg': msg, 'status': status}
        return self.render_to_json_response(dict(response_data))


class JournalEntryDetailView(JSONResponseMixin, View):

    def post(self, request, *args, **kwargs):
        context_dict = {'status': 'error'}
        status = 'error'
        post_body = json.loads(self.request.body)
        journal_id = post_body['journal_id']
        date_created = post_body.get('date_created')
        date_modified = post_body.get('date_modified')
        keyword_search = post_body.get('keyword_search')
        today = datetime.datetime.today().replace(hour=0, minute=0, second=0)

        try:
            journal_ins = Journal.objects.get(id=int(journal_id))
        except Journal.DoesNotExist:
            context_dict['msg'] = "Journal Does not exists!"
        else:
            if journal_ins.created_by != self.request.user:
                context_dict['msg'] = "Not allowed to view other users journal!"
            else:
                entries = journal_ins.journal_entry.all()
                if keyword_search:
                    entries = entries.filter(Q(title__icontains=keyword_search) | Q(description__icontains=keyword_search))
                if date_created:
                    from_data = today - datetime.timedelta(days=int(date_created))
                    entries = entries.filter(date_created__gte=from_data)
                entries = entries.values()
                final_list = []
                for entry in entries:
                    initial_data = {}
                    for k, v in entry.items():
                        if k in ['date_created', 'date_modified']:
                            initial_data[k] = str(datetime.datetime.strftime(v, '%c'))
                        else:
                            initial_data[k] = str(v)
                    final_list.append(initial_data)
                context_dict['status'] = 'success'
                context_dict['data'] = final_list
                context_dict['msg'] = "Successfully Pulled Entries!"
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
        if not self.request.user.is_authenticated():
            msg = "Please login!"
        else:
            try:
                journal_ins = Journal.objects.get(id=int(journal_id))
            except Journal.DoesNotExist:
                msg = "The Journal Does Exists!"
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
        data = None
        entry_id = self.request.GET['entry_id']
        if not self.request.user.is_authenticated():
            msg = "Please login!"
        else:
            try:
                entry_ins = Journal_entry.objects.get(id=int(entry_id))
            except Journal_entry.DoesNotExist:
                msg = 'The entry is either deleted or does not exists!'
            else:
                if entry_ins.journal_id.created_by != self.request.user:
                    msg = "Not Authorized!"
                else:
                    msg = "Pulled succesfully!"
                    status = "success"
                    data = model_to_dict(entry_ins)
        context_dict['data'] = {
            'data': data,
            'msg': msg,
            'status': status

        }
        return self.render_to_json_response(context_dict)

    def post(self, request, *args, **kwargs):
        context_dict = {}
        status = 'error'
        data = None
        post_body = json.loads(self.request.body)

        if not self.request.user.is_authenticated():
            msg = "Please login!"
        else:
            entry_id = post_body.get('entry_id')
            if not entry_id:
                msg = "Entry Id does not exists!"
            else:
                title = post_body['title']
                description = post_body['description']
                try:
                    entry_ins = Journal_entry.objects.get(id=int(entry_id))
                except Journal_entry.DoesNotExist:
                    msg = 'You are editing an invalid entry!'
                else:
                    if entry_ins.journal_id.created_by != self.request.user:
                        msg = "Not Authorized!"
                    elif entry_ins.title != title and Journal_entry.objects.filter(title=title).exists():
                        msg = "The entry title already exists!"
                    else:
                        entry_ins.title = title
                        entry_ins.description = description
                        entry_ins.save()
                        data = model_to_dict(entry_ins)
                        msg = "Successfully updated!"
                        status = 'success'
        context_dict['data'] = {
            'data': data,
            'msg': msg,
            'status': status
        }
        return self.render_to_json_response(context_dict)


class JournalEntryDeleteView(JSONResponseMixin, View):

    def post(self, request, *args, **kwargs):
        context_dict = {}
        msg = ""
        post_body = json.loads(self.request.body)
        entry_list = post_body['entry_id']
        status = "error"
        if not self.request.user.is_authenticated():
            msg = "Please login!"
        else:
            entry_list = [int(entry_id) for entry_id in entry_list]
            entry_qset = Journal_entry.objects.filter(id__in=entry_list)
            if entry_qset:
                entry_qset.delete()
                msg = "Successfully Deleted."
                status = "success"
        context_dict['data'] = {
            'msg': msg,
            'status': status
        }
        return self.render_to_json_response(context_dict)

