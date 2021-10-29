from datetime import datetime
from django.core.paginator import Paginator
from random import shuffle
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect
from django.views import View
from jedzonko.models import *
from django.core.paginator import Paginator


class IndexView(View):
    def get(self, request):
        ctx = {"actual_date": datetime.now()}
        return render(request, "test.html", ctx)


def index(request):
    przepisy = Recipe.objects.all()
    przepisy = list(przepisy)
    shuffle(przepisy)
    a = przepisy[0]
    b = przepisy[1]
    c = przepisy[2]
    return render(request, "index.html", {'a': a, 'b': b, 'c': c})


def dashboard(request):
    recipes = Recipe.objects.all()
    num_of_recipes = recipes.count()
    plans = Plan.objects.all()
    num_of_plans = plans.count()
    return render(request, 'dashboard.html', {"num_of_recipes": num_of_recipes, "num_of_plans": num_of_plans})


def recipe(request):
    list_of_recipes = Recipe.objects.all().order_by('votes').order_by('created')
    list_of_recipes = list_of_recipes[::-1]
    paginator = Paginator(list_of_recipes, 50)
    page = request.GET.get('page')
    recipes = paginator.get_page(page)
    return render(request, 'app-recipes.html', {'recipes': recipes})


def plan(request):
    plan_list = Plan.objects.all().order_by('name')
    paginator = Paginator(plan_list, 50)
    page = request.GET.get('page')
    plans = paginator.get_page(page)
    return render(request, 'app-schedules.html', {'plans': plans})


def add_recipe(request):
    if request.method == 'GET':
        return render(request, 'app-add-recipe.html')
    else:
        recipe_name = request.POST.get('recipe_name')
        recipe_description = request.POST.get('recipe_description')
        prep_time = request.POST.get('prep_time')
        preparation_method = request.POST.get('preparation_method')
        ingredients = request.POST.get('ingredients')
        if recipe_name and recipe_description and preparation_method and ingredients and prep_time:
            new_recipe = Recipe()
            new_recipe.name = recipe_name
            new_recipe.description = recipe_description
            new_recipe.preparation_time = prep_time
            new_recipe.ingredients = ingredients
            new_recipe.preparation_method = preparation_method
            new_recipe.save()
            return redirect(f'/recipe/list/')
        else:
            communique = "Wypełnij poprawnie wszystkie pola !!!"
            return render(request, 'app-add-recipe.html', {'communique': communique})


def add_plan(request):
    if request.method == 'GET':
        return render(request, 'app-add-schedules.html')

    else:
        plan_name = request.POST.get('planName')
        plan_description = request.POST.get('planDescription')
        if plan_name and plan_description:
            new_plan = Plan()
            new_plan.name = plan_name
            new_plan.description = plan_description
            new_plan.save()
            id = new_plan.id
            return redirect(f'/plan/{id}/')
        else:
            communique = "Wypełnij poprawnie wszystkie pola !!!"
            return render(request, 'app-add-schedules.html', {'communique': communique})


def add_recipe_to_plan(request):

    plan_name = list(Plan.objects.all())
    recipe_name = list(Recipe.objects.all())
    day = list(DayName.objects.all())
    if request.method == 'GET':
        return render(request, 'app-schedules-meal-recipe.html', {'plan_name': plan_name, 'recipe_name': recipe_name, 'day': day})

    else:
        meal = request.POST.get('meal')
        order_num = request.POST.get('order_number')
        plan_name_2 = request.POST.get('choosePlan')
        recipe_name_2 = request.POST.get('recipe')
        day_2 = request.POST.get('day')
        if meal and order_num and plan_name_2 and recipe_name_2 and day_2:
            new_recipe_to_plan = RecipePlan()
            new_recipe_to_plan.meal_name = meal
            new_recipe_to_plan.order = order_num
            new_recipe_to_plan.plan_id = plan_name_2
            new_recipe_to_plan.recipe_id = recipe_name_2
            new_recipe_to_plan.day_name_id = day_2
            new_recipe_to_plan.save()
            id = plan_name_2
            return redirect(f'/plan/{id}/')
        else:
            communique = "Wypełnij poprawnie wszystkie pola !!!"
            return render(request, 'app-schedules-meal-recipe.html', {'plan_name': plan_name, 'recipe_name': recipe_name, 'day': day, 'communique': communique})


def show_plan_id(request, id):
    plan_id = Plan.objects.get(pk=id)
    return render(request, 'app-details-schedules.html', {'plan_id': plan_id})


def show_recipe_id(request, id):
    recipe_id = Recipe.objects.get(pk=id)


    if request.method == 'GET':
        return render(request, 'app-recipe-details.html', {'recipe_id': recipe_id})


    if request.POST.get('add') is not None:
        recipe_id.votes += 1
        recipe_id.save()
        return render(request, 'app-recipe-details.html', {'recipe_id': recipe_id})

















