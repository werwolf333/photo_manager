from django.shortcuts import render, redirect
from django.template.context_processors import csrf
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm
from django.contrib import auth
from django.views.generic import View


class RegistrationFormView(FormView):
    form_class = UserCreationForm
    template_name = "login_and_registration/registration.html"
    success_url = "/login/?registration_completed"

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


@method_decorator(csrf_exempt, name='dispatch')
class LoginFormView(FormView):

    def get(self, request):
        args = {}

        if 'registration_completed' in request.GET:
            args['success_register'] = 'успешная регистрация'
        return render(request, 'login_and_registration/login.html', args)

    def post(self, request):
        args = {}
        args.update(csrf(request))
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        if username == '' and password == '':
            args['login_error'] = "Не введён логин и пароль"
            return render(request, 'login_and_registration/login.html', args)

        elif username == '':
            args['login_error'] = "Неввведён логин"
            return render(request, 'login_and_registration/login.html', args)

        elif password == '':
            args['login_error'] = "Невведён пароль"
            return render(request, 'login_and_registration/login.html', args)

        else:
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                auth.login(request, user)
                return redirect('/photo_manager/')
            else:
                args['login_error'] = "Неверен логин или пароль"
                return render(request, 'login_and_registration/login.html', args)

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class Logout(View):
    def get(self, request):
        auth.logout(request)
        return redirect('/login/')
