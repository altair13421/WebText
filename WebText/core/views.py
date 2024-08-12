"""
This file is used to define the views for the game

This File Does:

1. Defines the BaseFormView class
2. Defines the BaseDeleteFormView class
3. Defines the BaseDetailView class
4. Defines the BaseListView class

"""

import json
from typing import Any

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import redirect_to_login
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.forms import Form
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import FormView, ListView, UpdateView, DetailView, DeleteView

from core.mixins import UserRequiredMixin


class BasePermissionMixin(UserRequiredMixin, UserPassesTestMixin):
    def test_func(self) -> bool | None:
        """
        The function `test_func` returns `True` if the user making the request is a superuser,
        otherwise it
        returns `None`.
        :return: The function `test_func` is returning the result of the logical `and`
        operation between the
        return value of `super().test_func()` and the check if `self.request.user` is a superuser.
        """
        return self.request.user.is_superuser  # type: ignore


class BaseFormView(FormView, BasePermissionMixin):
    form_class: Form = Form
    success_url: str = ""
    template_name: str = ""

    def get(self, request, *args, **kwargs):
        if not self.test_func():
            return redirect_to_login(next=request.path)
        return super().get(request, *args, **kwargs)

    def get_object(self):
        id = self.kwargs.get("pk", None)
        if id:
            return get_object_or_404(self.form_class.get_model, pk=id)
        return None

    def get_initial(self) -> dict[str, Any]:
        initial = super().get_initial()
        obj = self.get_object()
        if obj:
            for key, val in self.form_class().get_initial(instance=obj).items():
                initial[key] = val
        return initial

    def get_form(self, form_class=None):
        obj = self.get_object()
        form = super().get_form(form_class)
        form.instance = obj
        return form

    def form_valid(self, form):
        form_data = form.cleaned_data
        if form.instance != None:
            obj = self.get_object()
            if obj:
                for field in self.form_fields():
                    setattr(obj, field, form_data.get(field, getattr(obj, field)))
                obj.save()
            else:
                raise ValueError("Object not found")
        else:
            obj = self.form_class.get_model(**form_data)
            obj.save()
        return super().form_valid(form)


class BaseDeleteFormView(DeleteView, BasePermissionMixin):

    def get_object(self):
        id = self.kwargs.get("pk", None)
        if id:
            return get_object_or_404(self.form_class.get_model, pk=id)
        return None

    def form_valid(self, form):
        self.get_object().delete()
        return super().form_valid(form)

    def get(self, request, *args, **kwargs):
        if not self.test_func():
            return redirect_to_login(next=request.path)
        return super().get(request, *args, **kwargs)


class BaseDetailView(DetailView, BasePermissionMixin):
    def get(self, request, *args, **kwargs):
        if not self.test_func():
            return redirect_to_login(next=request.path)
        return super().get(request, *args, **kwargs)


class BaseListView(ListView, BasePermissionMixin):
    def get(self, request, *args, **kwargs):
        if not self.test_func():
            return redirect_to_login(next=request.path)
        return super().get(request, *args, **kwargs)

    paginate_by = 10


class UserCreateView(UserRequiredMixin, SuccessMessageMixin, CreateView):
    """Mixin for creating a user."""

    model = User
    fields = ["username", "email", "password"]
    success_url = reverse_lazy("user_list")
    success_message = "User created successfully."


class UserUpdateView(UserRequiredMixin, SuccessMessageMixin, UpdateView):
    """Mixin for updating a user."""

    model = User
    fields = ["username", "email"]
    success_url = reverse_lazy("user_list")
    success_message = "User updated successfully."
