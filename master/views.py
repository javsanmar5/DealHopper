from django.shortcuts import redirect, render

from master.models import Smartphone

from .scrapping.fetch_data import scrap_data
from .search.search import search_products


def home(request):
    phones = Smartphone.objects.all()
    return render(request, "home.html", {'phones': phones})

def about(request):
    return render(request, "about.html")
    
def search_view(request):
    query = request.GET.get("search", "")
    results = search_products(query) if query else []
    return render(request, "search_results.html", {"results": results})

    
def fetch_data(request):

    if request.method == "GET" and request.GET.keys():
        print("Redirecting to /fetch-data without parameters...")
        return redirect('fetch_data') 

    shop = request.GET.get('shop', None)
    message = ""

    if request.method == "POST" and shop:
        try:
            scrap_data(shop) 
            message = f"Data fetched successfully for {shop}."
        except Exception as e:
            message = f"Error: {str(e)}"

        request.session['message'] = message
        return redirect('fetch_data')

    message = request.session.pop('message', None)

    return render(request, "fetch_data.html", {'message': message})

