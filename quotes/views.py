from django.shortcuts import render, redirect
import requests
import json
from .models import Stock
from django.contrib import messages

from .forms import StockForm

# Create your views here.

def index(request):
    if request.method == 'POST':
        ticker = request.POST['ticker']

        api_request = requests.get(
            "https://cloud.iexapis.com/stable/stock/"+ticker+"/quote?token=pk_0ce135799e0e4ee788f156cb6f0b3e15")

        try:
            api = json.loads(api_request.content)
        except Exception as e:
            api = "Error ... "

        return render(request, 'quotes/home.html', {'api': api})

    else:
        return render(request, 'quotes/home.html', {'ticker': "Enter a stock symbol in the search to get the current quote for the stock"})



def about(request):
    return render(request,'quotes/about.html', {})


def add_stock(request):
    if request.method == 'POST':
        form = StockForm(request.POST or None)

        if form.is_valid():
            form.save()
            messages.success(request, ("Stock has been added"))
            return redirect('/add_stock', None, None)
    else:
        ticker = Stock.objects.all()
        results = []
        for ticker_item in ticker:
            api_request = requests.get(
                "https://cloud.iexapis.com/stable/stock/" + str(ticker_item) + "/quote?token=pk_0ce135799e0e4ee788f156cb6f0b3e15")

            try:
                api = json.loads(api_request.content)

                results.append(api)
            except Exception as e:
                api = "Error ... "

        return render(request,'quotes/add_stock.html', {'ticker':ticker, 'results':results})



def delete(request, stock_id):
    item = Stock.objects.get(pk=stock_id)
    item.delete()
    messages.success(request, ("Stock has been deleted"))
    return redirect('/delete_stock', None, None)


def delete_stock(request):
    ticker = Stock.objects.all()
    results = []
    for ticker_item in ticker:
        api_request = requests.get(
            "https://cloud.iexapis.com/stable/stock/" + str(
                ticker_item) + "/quote?token=pk_0ce135799e0e4ee788f156cb6f0b3e15")

        try:
            api = json.loads(api_request.content)
            api['id'] = ticker_item.id

            results.append(api)
        except Exception as e:
            api = "Error ... "

    return render(request,'quotes/delete_stock.html', {'ticker':ticker, 'results':results})

#pk_0ce135799e0e4ee788f156cb6f0b3e15