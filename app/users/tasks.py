from celery import shared_task
from django.utils import timezone
from django.db.models import Count, Q
import requests
import socket
from .models import SiteInfo, Session


def get_site_info(domain: str = None):
    """
    return status and responce time of domain
    """
    try:
        r = requests.get(f'http://{domain}')
        status_code = r.status_code
        responce_time = r.elapsed.total_seconds()
        return status_code, responce_time
    except Exception as ex:
        return 'error', 'error'


def get_site_ip(domain: str = None) -> str:
    """
    return ip of domain
    """
    try:
        return socket.gethostbyname(domain)
    except Exception as ex:
        return 'error'


@shared_task
def queue_site_info(site_info_id, timeout=None):
    """
    This task saves info aboot site
    """
    instance = SiteInfo.objects.get(pk=site_info_id)
    ip = get_site_ip(domain=instance.name)
    status, responce_time = get_site_info(domain=instance.name)
    instance.ip = ip
    instance.check_time = timezone.now()
    instance.status = status
    instance.responce_time = responce_time
    instance.is_checked = True
    instance.save()

    session = Session.objects.annotate(checked_count=Count(
        'sites', filter=Q(sites__is_checked=True))).get(pk=instance.session.pk)
    if session.sites_counter == session.checked_count:
        session.status = Session.SUCCESS
        session.end_date = timezone.now()
        session.save()
