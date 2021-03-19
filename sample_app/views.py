from django.shortcuts import render
from sample_app import support_functions
from sample_app.models import Country, Currency, Rates, Stock, Company, Exchange, AccountHolder
from django.contrib.auth.forms import UserCreationForm

# Create your views here.

def home(request):
    data = dict()
    user = request.user
    if user.is_superuser:
        return render(request, "maintenance.html", context=data)
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
    date = request.GET['date']
    amount = float(request.GET['dollars'])
    print("data test:", username, date, amount)
    commission = amount*0.20
    returned_amount = amount-commission
    data['person'] = username
    data['selected_date'] = date
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
        list = support_functions.get_stock_list()
        support_functions.add_exchange()
        support_functions.add_stocks(list)
        support_functions.add_company(list)
    except:
        print("error!")
    companies= Company.objects.all()
    print(companies)
    data['companies']= companies
    return render(request, "company_selector.html", data)

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

    return render(request,"entry.html",context=data)

#I am testing if i can successfully make a new branch (RL)