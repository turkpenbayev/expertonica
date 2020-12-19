from django.contrib.auth import authenticate
from django.utils import timezone
from rest_framework import serializers
import csv
import requests
import socket
import pandas as pd

from django.contrib.auth import get_user_model
from .models import SiteInfo, Session
from .tasks import queue_site_info


def get_and_authenticate_user(username, password):
    user = authenticate(username=username, password=password)
    if user is None:
        raise serializers.ValidationError(
            "Invalid username/password. Please try again!")
    return user


def create_user_account(username, password, first_name="",
                        last_name="", **extra_fields):
    user = get_user_model().objects.create_user(
        username=username, password=password, first_name=first_name,
        last_name=last_name, **extra_fields)
    return user


def count_sites_from_file(instance=None):
    """
    saves all site info of session
    """
    print('saves all site info of session')
    try:
        instance.start_date = timezone.now()
        instance.status = Session.PENDING
        excel_data_df = pd.read_excel(instance.sites_file.path)
        instance.sites_counter = len(excel_data_df.index)
        instance.save()
        for index, row in excel_data_df.iterrows():
            domain = row["url"]
            site_info = SiteInfo.objects.create(session=instance, name=domain)
            # set task
            queue_site_info.delay(site_info.pk)
    except Exception as ex:
        print(ex)
        pass
