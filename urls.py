from django.contrib import admin

from django.urls import path
from jedzonko.views import *



urlpatterns = [
    path('index/', IndexView.as_view()),
    path('', index),
    path('main/', dashboard),
    path('recipe/list/', recipe),
    path('plan/list/', plan),
    path('recipe/add/', add_recipe),
    path('plan/add/', add_plan),
    path('plan/add-recipe/', add_recipe_to_plan),
    path('plan/<id>/', show_plan_id),
    path('recipe/<id>/', show_recipe_id),
]
