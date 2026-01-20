from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView, RedirectView, TemplateView
from django.urls import reverse_lazy
from django.contrib import messages
from django_htmx.http import HttpResponseClientRedirect
from django.contrib.auth import get_user_model
from ..forms import CustomUserCreationForm

User = get_user_model()


class RegisterView(CreateView):
    """
    Class-based view for user registration
    """
    form_class = CustomUserCreationForm
    template_name = 'user/register.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        # Save the user
        user = form.save()
        username = form.cleaned_data.get('username')
        messages.success(self.request, f'Аккаунт создан для {username}!')

        # Authenticate and login the user
        username_or_email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username_or_email, password=password)
        if user is not None:
            login(self.request, user)

        # Handle HTMX request
        if self.request.htmx:
            response = HttpResponseClientRedirect(self.success_url)
            return response

        return super().form_valid(form)

    def form_invalid(self, form):
        # Handle HTMX partial response
        if self.request.htmx:
            return render(self.request, 'user/partials/register_form.html', {'form': form})
        return super().form_invalid(form)


class CustomLoginView(LoginView):
    """
    Class-based view for user login with HTMX support
    """
    template_name = 'user/login.html'
    next_page = reverse_lazy('home')

    def form_valid(self, form):
        # Call parent form_valid to perform login
        response = super().form_valid(form)
        messages.success(self.request, 'Вы успешно вошли в систему!')

        # Handle HTMX request
        if self.request.htmx:
            return HttpResponseClientRedirect(self.get_success_url())

        return response

    def form_invalid(self, form):
        # Handle HTMX partial response
        if self.request.htmx:
            # Prepare form errors in a format similar to the original function-based view
            form_errors = {}
            for field, errors in form.errors.items():
                if field == '__all__':
                    form_errors[field] = errors
                else:
                    form_errors[field] = [str(error) for error in errors]
            return render(self.request, 'user/partials/login_form.html', {'form_errors': form_errors})
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add any additional context if needed
        return context


class CustomLogoutView(LoginRequiredMixin, RedirectView):
    """
    Class-based view for user logout
    """
    url = reverse_lazy('login')

    def get(self, request, *args, **kwargs):
        logout(request)
        messages.info(request, 'Вы вышли из системы.')

        # Handle HTMX request
        if request.htmx:
            return HttpResponseClientRedirect(self.url)

        return super().get(request, *args, **kwargs)


class HomeView(LoginRequiredMixin, TemplateView):
    """
    Home view that shows different content based on authentication status
    """
    template_name = 'user/home.html'
    login_url = reverse_lazy('login')