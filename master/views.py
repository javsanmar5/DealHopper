from django.shortcuts import redirect, render

from master.models import Smartphone

from .recommendation.recommendation import recommend_similar_smartphones
from .scrapping.fetch_data import scrap_data
from .search.search import search_products


def home(request):
    phone_names = Smartphone.objects.values_list('name', flat=True).distinct()
    return render(request, "home.html", {'phones': phone_names})


def about(request):
    return render(request, "about.html")

def contact(request):
    return render(request, "contact.html")
    
    
def search_view(request):
    query = request.GET.get("search", "")
    results = search_products(query) if query else []
    recommendations = []
    if results: 
        smartphone_vector = _get_smartphone_vector(results[0])
        recommendations = recommend_similar_smartphones(smartphone_vector)
        
    return render(request, "search_results.html", {"results": results, "query": query, "recommendations": recommendations})

def _get_smartphone_vector(smartphone: dict) -> list:
    return [
        float(smartphone.get("smartphone_ram", 0) or 0),
        float(smartphone.get("smartphone_screen_size", 0) or 0),
        float(smartphone.get("smartphone_storage", 0) or 0),
        float(smartphone.get("smartphone_battery", 0) or 0),
    ]
    

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

