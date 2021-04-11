import os

from django.shortcuts import render
from sample_app import support_functions
from sample_app.models import Country, Currency, Rates, Stock, Company, Exchange, AccountHolder, Portfolio, UploadedFiles
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
from .forms import UploadFileForm

# Create your views here.
def home(request):
    data = dict()
    user =request.user
    if user.is_superuser:
        return render(request,"maintenance.html",context=data)
    import datetime
    date = datetime.datetime.now()
    data['now'] = date
    data['city'] = "New York"
    return render(request, "home.html",context=data)
def show3divs(request):
    data = dict()
    return render(request,"div_test.html",context=data)
def showform(request):
    data=dict()
    return render(request,"form_test.html",context=data)

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
#Make sure you've imported Country from models.py!
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
        stock_details = support_functions.get_stock_details(data['url'])
        data['price_chance'] = stock_details[0]
        data['change_percent'] = stock_details[1]
        data['stock_price'] = stock_details[2]
        data['market_cap'] = stock_details[3]
        data['shares_in_issue'] = stock_details[4]
        data['revenue'] = stock_details[5]
        data['profit_loss'] = stock_details[6]
        data['EPS'] = stock_details[7]
        data['PE_ratio'] = stock_details[8]
    except:
        ticker="AHC"
        data['ticker']=ticker
        print("error")
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

def upload_file(request):
    data = {}
    form = UploadFileForm(request.POST, request.FILES)
    if form.is_valid():
        file = request.FILES['myfile']
        handle_uploaded_file(request, file)
    else:
        print(form.errors)
    account_holder = AccountHolder.objects.get(user=request.user)
    data["UploadedFiles"] = UploadedFiles.objects.filter(user_account=account_holder)
    return render(request, 'view_file_list.html', context=data)

def handle_uploaded_file(request, f):
    user = request.user
    account_holder = AccountHolder.objects.get(user=user)
    try:
        f1=UploadedFiles.objects.create(user_account=account_holder, user_uploaded_file=f)
        f1.save()
        print("Working")
    except Exception as error:
       xprint(error)

def form_results(request):
    data = dict()
    user = request.user
    account_holder = AccountHolder.objects.get(user=user)
    ticker = request.GET['ticker']
    quantity = request.GET['quantity']
    try:
        p1 = Portfolio.objects.get(user_account=account_holder, user_stock_ticker=ticker)
        p1.user_stock_quantity = quantity
        p1.save()
    except:
        p1 = Portfolio(user_account=account_holder, user_stock_ticker=ticker, user_stock_quantity=quantity)
        p1.save()
    print("this is the line printed before p1")
    p_list= list(Portfolio.objects.filter(user_account=account_holder).values())
    q_list=list()
    t_list=list()
    for l in p_list:
        q_list.append(l.get('user_stock_quantity'))
        t_list.append(l.get('user_stock_ticker'))

    data["Portfolio"] = Portfolio.objects.filter(user_account=account_holder)
    result_list = Portfolio.objects.filter(user_account=account_holder)
    price_list = list()
    for entry in result_list:
        price_list.append(support_functions.get_latest_price(entry.user_stock_ticker))
    data["price_list"] = price_list
    value=list()
    for i in range(0, len(price_list)):
        value.append(float(price_list[i])*float(q_list[i]))
    data["quantity_list"]=q_list
    data["values"]=value
    zipped_list = zip(t_list,q_list,price_list,value)
    data = {'zipped_list': zipped_list}

    return render(request, "form_results.html", context=data)
