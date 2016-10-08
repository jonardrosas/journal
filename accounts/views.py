import json
import pdb
import re
import string

from django.shortcuts import render
from django.views.generic import TemplateView, View
from django.contrib.auth.views import login as django_login
from django.contrib.auth.forms import authenticate
from django.contrib.auth import get_user_model
from django.contrib.auth import login as login3

import enchant

from utils.views import JSONResponseMixin


def login(request):
    extra_context = {
        'ngapp': 'loginMod'
    }
    return django_login(request, template_name="login.html", extra_context=extra_context)


class HomePage(TemplateView):
    template_name = "login.html"

    def get_context_data(self, **kwargs):
        context = super(HomePage, self).get_context_data(**kwargs)
        context['ngapp'] = "homeMod"
        return context


class SignUp(TemplateView):
    template_name = "sign_up.html"

    def get_context_data(self, **kwargs):
        context = super(SignUp, self).get_context_data(**kwargs)
        context['ngapp'] = "SignUpMod"
        return context


class AuthenticationBase(JSONResponseMixin, View):
    process_create = False
    METER = {
        1: 'Too Short',
        2: 'Weak',
        3: 'Good',
        4: 'Strong',
    }
    HACKERS_LIST = [
        'password',
        '123456',
        '12345678',
        '1234',
        'qwerty',
        '12345',
        'dragon',
        'pussy',
        'baseball',
        'football',
        'letmein',
        'monkey',
        '696969',
        'abc123',
        'mustang',
        'michael',
        'shadow',
        'master',
        'jennifer',
        '111111',
    ]

    def password_validation_criteria(self, password):
        context_dict = {}
        dictionary_ins = enchant.Dict("en_US")
        points = 0

        if not dictionary_ins.check(password):
            context_dict['dictionary_word'] = {
                'status': 'pass',
                'cls': 'glyphicon-ok',
                'points': 1
            }

        if not password in self.HACKERS_LIST:
            context_dict['hacker_list'] = {
                'status': 'pass',
                'cls': 'glyphicon-ok',
                'points': 1
            }


        if len(password) > 8:
            context_dict['length'] = {
                'status': 'pass',
                'cls': 'glyphicon-ok',
                'points': 1
            }
        if len(set(string.ascii_lowercase).intersection(password)) > 0:
            context_dict['lower'] = {
                'status': 'pass',
                'cls': 'glyphicon-ok',
                'points': 1
            }
            points+= 1
        if len(set(string.ascii_uppercase).intersection(password)) > 0:
            context_dict['upper'] = {
                'status': 'pass',
                'cls': 'glyphicon-ok',
                'points': 1
            }
        if len(set(string.digits).intersection(password)) > 0:
            context_dict['number'] = {
                'status': 'pass',
                'cls': 'glyphicon-ok',
                'points': 1
            }
        if len(set(string.punctuation).intersection(password)) > 0:
            context_dict['special'] = {
                'status': 'pass',
                'cls': 'glyphicon-ok',
                'points': 1
            }

        return context_dict

    def password_strength(self, password):
        context_dict = self.password_validation_criteria(password)
        if 'length' not in context_dict:
            context_dict['msg'] = {
                'status': 'error',
                'type': self.METER[1],
                'cls': 'danger',
                'percent': '20%',
                'msg': 'Too short',
            }
        elif 'lower' in context_dict and 'upper' in context_dict and 'number' in context_dict and 'special' in context_dict:
            context_dict['msg'] = {
                'status': 'success',
                'type': self.METER[4],
                'cls': 'success',
                'percent': '100%',
                'msg': 'Srong Password',
            }
            self.process_create = True
        elif 'upper' in context_dict and ('lower' in context_dict or 'number' in context_dict or 'special' in context_dict):
            context_dict['msg'] = {
                'status': 'success',
                'type': self.METER[3],
                'cls': 'info',
                'percent': '60%',
                'msg': 'Good Password',
            }
        elif 'number' in context_dict and ('upper' in context_dict or 'lower' in context_dict or 'special' in context_dict):
            context_dict['msg'] = {
                'status': 'success',
                'type': self.METER[3],
                'cls': 'info',
                'percent': '60%',
                'msg': 'Good Password',
            }
        elif 'lower' in context_dict and ('upper' in context_dict or 'number' in context_dict or 'special' in context_dict):
            context_dict['msg'] = {
                'status': 'success',
                'type': self.METER[3],
                'cls': 'info',
                'percent': '60%',
                'msg': 'Good Password',
            }
        elif 'special' in context_dict and ('upper' in context_dict or 'number' in context_dict or 'lower' in context_dict):
            context_dict['msg'] = {
                'status': 'success',
                'type': self.METER[3],
                'cls': 'info',
                'percent': '60%',
                'msg': 'Good Password',
            }
        else:
            context_dict['msg'] = {
                'status': 'success',
                'type': self.METER[2],
                'cls': 'warning',
                'percent': '40%',
                'msg': 'Weak Password',
            }
        return context_dict

    def is_valid_email(self, email):
        context_dict = {}
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            context_dict['email'] = {
                'status': 'error',
                'msg': 'Invalid email address'
            }
        return context_dict

    def has_empty_fields(self, **kwargs):
        context_dict = {}
        for f, val in kwargs.items():
            if not kwargs[f]:
                context_dict[f] = {
                    'status': 'error',
                    'msg': '%s is required!' % f,
                }
        return context_dict

    def create_user(self, username, email, password, **kwargs):
        user = get_user_model().objects.create_user(
            username,
            email,
            password,
            last_name=kwargs.get('last_name'),
            first_name=kwargs.get('first_name'),
        )

    def is_password_match(self, password, confirm_password):
        context_dict = {}
        if password != confirm_password:
            context_dict['confirm_password'] = {
                'status': 'error',
                'msg': 'Your password does not match!',
            }
        return context_dict

    def is_exist_user(self, username):
        context_dict = {}
        if get_user_model().objects.filter(username__iexact=username).exists():
            context_dict['username'] = {
                'status': 'error',
                'msg': 'Username already exists!',
            }
        return context_dict


class Authentincate(AuthenticationBase):

    def post(self, request, *args, **kwargs):
        context_dict = {}
        status = 'error'
        post_body = json.loads(self.request.body)
        username = post_body['username']
        email = post_body['email']
        password = post_body['password']
        confirm_password = post_body['confirm_password']
        last_name = post_body['last_name']
        first_name = post_body['first_name']

        if self.has_empty_fields(**post_body):
            context_dict.update(self.has_empty_fields(**post_body))
        elif self.is_password_match(password, confirm_password):
            context_dict.update(self.is_password_match(password, confirm_password))
        elif self.is_valid_email(email):
            print "ere"
            context_dict.update(self.is_valid_email(email))
        elif self.is_exist_user(username):
            context_dict.update(self.is_exist_user(username))
        else:
            self.create_user(username, email, password, last_name=last_name, first_name=first_name)
            context_dict['msg'] = {
                'status': 'success',
                'cls': 'success',
                'msg': 'Successfully Create Username %s' % username,
                'type': 'Successfully Create Username %s' % username,
            }
        print context_dict
        return self.render_to_json_response(context_dict)


class Authentincate2(AuthenticationBase):

    def post(self, request, *args, **kwargs):
        context_dict = {}
        status = 'error'
        post_body = json.loads(self.request.body)
        username = post_body['username']
        email = post_body['email']
        password = post_body['password']
        confirm_password = post_body['confirm_password']
        last_name = post_body['last_name']
        first_name = post_body['first_name']

        if self.has_empty_fields(**post_body):
            context_dict.update(self.has_empty_fields(**post_body))
        elif self.is_password_match(password, confirm_password):
            context_dict.update(self.is_password_match(password, confirm_password))
        elif self.is_valid_email(email):
            context_dict.update(self.is_valid_email(email))
        elif self.is_exist_user(username):
            context_dict.update(self.is_exist_user(username))
        elif self.password_strength(password) and not self.process_create:
            context_dict.update(self.password_strength(password))
        else:
            self.create_user(username, email, password, last_name=last_name, first_name=first_name)
            context_dict['msg'] = {
                'status': 'success',
                'cls': 'success',
                'msg': 'Successfully Create Username %s' % username,
                'type': 'Successfully Create Username %s' % username,
            }
        return self.render_to_json_response(context_dict)


class Authentincate3(AuthenticationBase):

    def post(self, request, *args, **kwargs):
        post_body = json.loads(self.request.body)
        context_dict = {}
        status = 'error'
        post_body = json.loads(self.request.body)
        password = post_body['password']
        # if self.password_validation_criteria(password):
        context_dict.update(self.password_validation_criteria(password))
        context_dict.update(self.password_strength(password))
        return self.render_to_json_response(context_dict)


class UserLoginView(JSONResponseMixin, View):

    def post(self, request, *args, **kwargs):
        post_body = json.loads(self.request.body)
        username = post_body['username']
        password = post_body['password']

        if not password:
            context_dict = {
                'status': 'success',
                'msg': 'Password is Required',
            }

        u = authenticate(username=username, password=password)
        if u is not None:
            login3(request, u)
            context_dict = {
                'status': 'success',
                'msg': 'User logged in',
                'username': username
            }
        else:
            context_dict = {
                'status': 'error',
                'msg': 'Please enter a correct username and password',
                'username': username
            }
        return self.render_to_json_response(context_dict)
