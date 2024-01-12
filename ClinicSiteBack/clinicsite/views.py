from django.shortcuts import render

def login_view(request):
    return render(request, 'login.html')

def market_view(request):
    return render(request, 'market.html')