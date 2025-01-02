from django.shortcuts import redirect, render
from .scrapping.fetch_data import scrap_data 

# Create your views here.
def home(request):
    return render(request, "home.html")

def about(request):
    return render(request, "about.html")
    
def fetch_data(request):

    if request.method == "GET" and request.GET.keys():
        print("Redirecting to /fetch-data without parameters...")
        return redirect('fetch_data')  # Replace 'fetch_data' with your URL pattern name

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

