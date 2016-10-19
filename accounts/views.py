import json
import pdb
import re
import string

from django.shortcuts import render
from django.core.mail import EmailMultiAlternatives
from django.core.mail import send_mail
from django.views.generic import TemplateView, View
from django.contrib.auth.views import login as django_login, logout
from django.contrib.auth.forms import authenticate
from django.contrib.auth import get_user_model
from django.contrib.auth import login as login3
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import get_template
from django.core.urlresolvers import reverse
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes


import enchant

from utils.views import JSONResponseMixin


class HomePage(TemplateView):
    template_name = "login.html"

    def get_context_data(self, **kwargs):
        print "it goues to home"
        uid64 = self.request.GET.get('uid64')
        token = self.request.GET.get('token')
        context = super(HomePage, self).get_context_data(**kwargs)
        logout(self.request)
        context['ngapp'] = "homeMod"
        if uid64 and token:
            context['uid64'] = uid64
            context['token'] = token
            context['reset_password_confirm'] = reverse('reset_password_confirm', args=[uid64, token])
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
                'percent': '50%',
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
                'percent': '80%',
                'msg': 'Good Password',
            }
        elif 'number' in context_dict and ('upper' in context_dict or 'lower' in context_dict or 'special' in context_dict):
            context_dict['msg'] = {
                'status': 'success',
                'type': self.METER[3],
                'cls': 'info',
                'percent': '80%',
                'msg': 'Good Password',
            }
        elif 'lower' in context_dict and ('upper' in context_dict or 'number' in context_dict or 'special' in context_dict):
            context_dict['msg'] = {
                'status': 'success',
                'type': self.METER[3],
                'cls': 'info',
                'percent': '80%',
                'msg': 'Good Password',
            }
        elif 'special' in context_dict and ('upper' in context_dict or 'number' in context_dict or 'lower' in context_dict):
            context_dict['msg'] = {
                'status': 'success',
                'type': self.METER[3],
                'cls': 'info',
                'percent': '80%',
                'msg': 'Good Password',
            }
        else:
            context_dict['msg'] = {
                'status': 'success',
                'type': self.METER[2],
                'cls': 'warning',
                'percent': '60%',
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

    def is_email_taken(self, email):
        context_dict = {}
        if get_user_model().objects.filter(email__icontains=email).exists():
            context_dict['email'] = {
                'status': 'error',
                'msg': 'Email address already in use!',
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
        elif self.is_email_taken(email):
            context_dict.update(self.is_email_taken(email))
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
        elif self.is_email_taken(email):
            context_dict.update(self.is_email_taken(email))
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
        context_dict = {'msg': ''}
        status = 'error'
        post_body = json.loads(self.request.body)
        password = post_body.get('password', None)
        if password:
            # if self.password_validation_criteria(password):
            context_dict.update(self.password_validation_criteria(password))
            context_dict.update(self.password_strength(password))
        return self.render_to_json_response(context_dict)


class PasswordResetConfirmView(JSONResponseMixin, View):

    def post(self, request, *args, **kwargs):
        """
        View that checks the hash in a password reset link and presents a
        form for entering a new password.
        """
        context_dict = {}
        post_body = json.loads(self.request.body)
        uidb64 = post_body['uid64']
        new_password = post_body['new_password']
        confirm_password = post_body['confirm_password']
        token = post_body['token']
        data = None
        status = 'error'
        UserModel = get_user_model()
        print post_body
        #form = self.form_class(request.POST)
        assert uidb64 is not None and token is not None  # checked by URLconf
        try:
            uid = urlsafe_base64_decode(uidb64)
            user = UserModel._default_manager.get(pk=uid)
        except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            if new_password == confirm_password:
                user.set_password(new_password)
                user.save()
                status = 'success'
                msg = 'Password has been reset!'
            else:
                msg = 'Password reset has not been successful!'
        else:
            msg = 'The reset password link is no longer valid.'

        context_dict = {
            'data': data,
            'msg': msg,
            'status': status
        }
        return self.render_to_json_response(context_dict)


class ResetPasswordView(JSONResponseMixin, View):

    def send_email(self, to_email):
        uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        token = default_token_generator.make_token(self.user)

        data = {
            'site_name': 'testasite',
            'domain': self.request.META['HTTP_HOST'],
            'url': "%s?uid64=%s&token=%s#/confirm_reset" % (reverse('login'), uid, token),
            'user': self.user,
        }
        subject, from_email, to = 'hello', '',  to_email
        template = """
                <p>
                You're receiving this email because you requested a
                password reset for your user account at {site_name}.

                Please go to the following page and choose a new password:
                </p><br/>
                {domain}{url}
        """.format(**data)
        msg = EmailMultiAlternatives(subject, template, from_email, [to])
        msg.attach_alternative(template, "text/html")
        msg.send()

    def post(self, request, *args, **kwargs):
        post_body = json.loads(self.request.body)
        email = post_body.get('email')
        status = "error"
        context_dict = {}
        data = None
        print email
        if not email:
            msg = "Valid email address is required!"
        else:
            try:
                user_ins = get_user_model().objects.get(email__icontains=email)
            except ObjectDoesNotExist:
                msg = "We could not find a user with that email address. Please try again."
            except MultipleObjectsReturned:
                msg = "The email address have multiple username"
            else:
                self.user = user_ins
                msg = """
                      We've e-mailed you instructions for setting your password to the e-mail address
                      you submitted. You should be receiving it shortly"""
                status = "success"
                email = user_ins.email
                self.send_email(email)
        context_dict = {
            'data': data,
            'msg': msg,
            'status': status
        }
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
