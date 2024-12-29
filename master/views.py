from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, "home.html")

def database(request):
    return render(request, "database.html")
