from django.shortcuts import render
from sample_app import support_functions
from sample_app.models import Country, Currency, Rates, Stock, Company, Exchange
from django.contrib.auth.forms import UserCreationForm
# Create your views here.

def home(request):
    data = dict()
    import datetime
    date = datetime.datetime.now()
    data['now'] = date
    data['city'] = "New York"
    print(data)
    #return render(request,"home.html",context=data)
    return render(request, "home.html")

def show3divs(request):
    data = dict()

    return render(request,"div_test.html",context=data)

def showform(request):
    data=dict()
    return render(request,"form_test.html",context=data)

def form_results(request):
    data=dict()
    username = request.GET['name']
    stock = request.GET['stock']
    amount = float(request.GET['dollars'])
    print("data test:", username, stock, amount)
    commission = amount*0.20
    returned_amount = amount-commission
    data['person'] = username
    data['selected_stock'] = stock
    data['amount'] = returned_amount
    return render(request,"form_results.html",context=data)

def maintenance(request):
    data = dict()
    try:
        form_submitted = request.GET['form_submitted']
        choice = request.GET['selection']
        if choice == "currencies":
            support_functions.add_countries_and_currencies(support_functions.get_currency_list())
    except:
        pass
    return render(request,"maintenance.html",context=data)


#Make sure you’ve imported Country from models.py!
def currency_selection(request):
    data = dict()
    countries = Country.objects.all()
    data['countries'] = countries

    return render(request,"country_selector1.html",context=data)

def exch_rate(request):
    data=dict()
    try:
        country1 = request.GET['country_from']
        country2 = request.GET['country_to']
        data['country1'] = Country.objects.get(id=country1)
        data['country2'] = Country.objects.get(id=country2)
        currency1 = Country.objects.get(id=country1).currency
        currency2 = Country.objects.get(id=country2).currency
        support_functions.update_xrates(currency1)
        data['currency1'] = currency1
        data['currency2'] = currency2
        try:
            rate = currency1.rates_set.get(x_currency=currency2.symbol).rate
            data['rate'] = rate
        except:
            pass
    except:
        pass
    return render(request,"exchange_detail.html",context=data)


def company_selection(request):
    data= dict()
    try:
        support_functions.read_function()
    except:
        print("error in company selection!")
    companies= Stock.objects.all().values('name')
    id=Stock.objects.all().values('id')
    url= Stock.objects.all().values('url')
    ticker= Stock.objects.all().values('ticker')
    data['companies']= companies
    data['urls']= url
    data['tickers']= ticker
    data['id']= id
    return render(request, "company_selector.html", context=data)

def register_new_user(request):
    context = dict()
    form = UserCreationForm(request.POST)
    if form.is_valid():
        new_user = form.save()
        dob = request.POST["dob"]
        acct_holder = AccountHolder(user=new_user,date_of_birth=dob)
        acct_holder.save()
        return render(request,"entry.html",context=dict())
    else:
        form = UserCreationForm()
        context['form'] = form
        return render(request, "registration/register.html", context)

def entry(request):
    data = dict()
    return render(request, "entry.html", context=data)

def ticker_sel(request):
    data=dict()
    try:
        ticker1 = request.GET['c_name']
        data['url']=Stock.objects.get(name=ticker1).url
        data['ticker']=Stock.objects.get(name=ticker1).ticker
        data['name']=Stock.objects.get(name=ticker1).name
    except:
        ticker="AHC"
        data['ticker']=ticker
        print("fuck")
    #url = Stock.objects.all(id=ticker).url
    #data['url']= url
    #print(url)
    return render(request,"company_details.html",data)

def form_results2(request):
    data=dict()
    username = request.GET['name']
    stock = request.GET['stock']
    amount = float(request.GET['dollars'])
    print("data test:", username, stock, amount)
    commission = amount*0.20
    returned_amount = amount-commission
    data['person'] = username
    data['selected_stock'] = stock
    data['amount'] = returned_amount
    return render(request,"form_results.html",context=data)

