"""Views implementation"""

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import requests
from django.http import HttpResponse
from django.shortcuts import render, redirect

import configuration
import os


def index(request):
    """Render the home page"""
    meals = []
    for _ in range(5):
        random_meal = requests.get(
            'https://www.themealdb.com/api/json/v2/' + os.environ.get('API_KEY', configuration.API_KEY) + '/random.php')
        if random_meal.status_code == 200:
            meals.append(random_meal.json()['meals'][0])
    first_recipe = requests.get(
        'https://www.themealdb.com/api/json/v2/' + os.environ.get('API_KEY', configuration.API_KEY) + '/random.php')
    if first_recipe.status_code != 200:
        first_recipe = None
    context = {
        'first_recipe': first_recipe.json()['meals'][0],
        'recipes': meals
    }
    return render(request, 'index.html', context)


def recipe(request, recipe_id):
    """Render the specific recipe page"""
    meal = requests.get(
        'https://www.themealdb.com/api/json/v2/' + os.environ.get('API_KEY', configuration.API_KEY) + '/lookup.php?i=' + str(
            recipe_id))
    if meal.status_code == 200:
        address = meal.json()["meals"][0]['strYoutube']
        embed_address = address.replace("watch?v=", "embed/")
        context = {
            "meal": meal.json()["meals"][0],
            "yt_url": embed_address,
        }
        return render(request, 'recipe.html', context)
    return HttpResponse("No such recipe")


def sign_in(request):
    # pylint: disable=unused-argument
    """Render the sign in page"""
    response = redirect('accounts/signup')
    return response


def log_in(request):
    # pylint: disable=unused-argument
    """Render the log in page"""
    response = redirect('accounts/login')
    return response


def search(request):
    """Render the search page"""
    return render(request, 'search.html')


def favorites(request):
    """Render the favourites page"""
    return render(request, 'favorites.html')


def search_results(request):
    """Render the search result page"""
    if 'q' in request.GET:
        ingredients = request.GET['q']
        if 'q/' in request.GET:
            if isinstance(request.GET['q/'], list):
                for ingredient in request.GET['q/']:
                    ingredients += ',' + ingredient
            else:
                ingredients += ',' + request.GET['q/']
        meal = requests.get(
            'https://www.themealdb.com/api/json/v2/' + os.environ.get('API_KEY', configuration.API_KEY) + '/filter.php?i='
            + ingredients)
        if meal.status_code == 200:
            context = {
                "meals": meal.json()["meals"]
            }

            return render(request, "search_results.html", context)
        return HttpResponse(meal.status_code)
    message = 'You submitted an empty form.'
    return HttpResponse(message)
