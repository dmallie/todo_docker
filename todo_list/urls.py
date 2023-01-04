# -*- coding: utf-8 -*-
"""
Created on Sat Dec 24 19:24:51 2022

@author: mrdag
"""

from django.urls import path
from . import views

app_name = 'todo_list'

urlpatterns = [
       path('', views.index, name="index"),
       path('schedule/<slug:slug>', views.todo_list, name="todo_list"),
       path('create_event/<slug:slug>', views.create_event, name="create_event"),
       path('edit_event/<int:id>', views.edit_events, name="edit_event"),
       path('details/<int:id>', views.details_page, name="details"),
       path('delete/<int:id>', views.delete_events, name="delete_event"),
       path('next_month/<slug:slug>', views.next_month, name="next_month"),
       path('prev_month/<slug:slug>', views.prev_month, name="prev_month"),
]
