from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Search
from .forms import SearchForm
import folium
import geocoder

# Create your views here.

def index(request):
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')

    else:
        form = SearchForm()
    address = Search.objects.all().last()
    # address = request.POST.get('address')
    location = geocoder.osm(address)
    print(location.osm)

    lat = location.lat
    lng = location.lng
    country = location.country
    print(f" Longitude: {lng} - Latitude: {lat} <--> {country}")

    if (lat == None) or (lng == None):
        address.delete()
        return HttpResponse('Address is not valid!')

    # Create map object
    mapObj = folium.Map(location=[44.0, 50.0], zoom_start=2)

    folium.Marker([lat, lng], tooltip="Click for more", popup=country).add_to(mapObj)
    
    # Get HTML Representation of Map Object
    mapObj = mapObj._repr_html_()
    context = {
        'mapObj': mapObj,
        'form': form,
    }
    return render(request, 'index.html', context)