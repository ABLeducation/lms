from django.shortcuts import render
from curriculum.models import *

# Create your views here.
def display_kits(request):
    kits=Mechanzo_kit_name.objects.all()
    return render (request,'curriculum/kits_display.html',{"kits":kits})

def display_models(request,slug):
    kit_name=Mechanzo_kit_name.objects.get(slug=slug)
    models_name=Mechanzo_model_name.objects.filter(kit=kit_name).order_by('model_id')
    return render (request,'curriculum/models_display.html',{'models':models_name, 'kits':kit_name})