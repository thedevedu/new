import hashlib
from django.core import paginator
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.http.response import HttpResponseForbidden, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Network
from .forms import NetworkForm
from ratelimit.decorators import ratelimit
from ratelimit.exceptions import Ratelimited
from django.conf import settings
from hitcount.utils import get_hitcount_model
from hitcount.views import HitCountMixin

from nanoid import generate

from django.core.cache import cache
from ipware import get_client_ip

CACHE_TTL = getattr(settings,'CACHE_TTL', DEFAULT_TIMEOUT)

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

@ratelimit(key='ip', rate='1/5s', block=True)
def rate_limiting(request):
    current_ip = get_client_ip(request)
    return (HttpResponse(current_ip))

def handler403(request, exception=None):
    if isinstance(exception, Ratelimited):
        return HttpResponse('Sorry you are blocked', status=429)
    return HttpResponseForbidden('Forbidden')


def rate_limitingx(request):
    current_ip = get_client_ip(request)
    if cache.get(current_ip):
        total_calls=cache.get(current_ip)
        if total_calls >=5:
            return(JsonResponse({'status': 501,'message':'You have exahusted the limit', 'time':f'You can try after{cache.ttl(total_calls)} seconds'}))
        else:
            cache.set(current_ip, total_calls +1)
            return(JsonResponse({'status': 200,'message':'You have exahusted the limit', 'time':f'You can try after{cache.ttl(total_calls)} seconds'}))

def networks(request):
    context = {'networks': networks, 'ip': get_client_ip(request)}
    return render(request, 'networks/gift.html', context)

def languages(request):
    context = {'networks': networks, 'ip': get_client_ip(request)}
    return render(request, 'networks/language.html', context)

def network(request, pk):
    gift_data = Network.objects.get(id=pk)
    return render(request, 'networks/gift.html', {'network': gift_data})
    
@login_required(login_url="login")
def createNetwork(request):

    profile = request.user
    form = NetworkForm()
    if request.method == 'POST':
        form = NetworkForm(request.POST, request.FILES)
        if form.is_valid():
            network = form.save(commit=False)
            network.owner = profile
            network.id = generate(size=12)
            network.save()

            return redirect('account')

    context = {'form': form}
    return render(request, "networks/network_form.html", context)

@login_required(login_url="login")
def createNetwork(request):

    profile = request.user
    form = NetworkForm()
    if request.method == 'POST':
        form = NetworkForm(request.POST, request.FILES)
        if form.is_valid():
            network = form.save(commit=False)
            network.owner = profile
            network.id = generate(size=12)
            network.save()

            return redirect('account')

    context = {'form': form}
    return render(request, "networks/network_form.html", context)

def handler403(request, exception=None):
    if isinstance(exception, Ratelimited):
        return HttpResponse('Sorry you are blocked', status=429)
    return HttpResponse('Forbidden')

@login_required(login_url="login")
def updateNetwork(request, pk):
    network = Network.objects.get(id=pk)
    form = NetworkForm(instance=network)

    if request.method == 'POST':
        form = NetworkForm(request.POST, instance=network)
        if form.is_valid():
            form.save()
            return redirect('account')

    context = {'form': form}
    return render(request, "networks/network_form.html", context)


@login_required(login_url="login")
def deleteNetwork(request, pk):
    profile = request.user
    network = profile.network_set.get(id=pk)
    if request.method == 'POST':
        network.delete()
        return redirect('account')
    context = {'object': network}
    return render(request, 'delete_it.html', context)
