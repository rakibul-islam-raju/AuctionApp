from django.contrib.admin.sites import AlreadyRegistered
from django.contrib import admin
from django.apps import apps

""" 
    register all the models from this app
"""
app_models = apps.get_app_config("core").get_models()
for model in app_models:
    try:
        admin.site.register(model)
    except AlreadyRegistered:
        pass
