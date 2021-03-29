from sample_app.models import Currency, Country, Rates, Company, Exchange, Stock
def get_currency_list():
    currency_list = list()
    import requests
    from bs4 import BeautifulSoup
    response = requests.get("https://thefactfile.org/countries-currencies-symbols/")
    soup = BeautifulSoup(response.content)
    table = soup.find('table')
    rows = table.find_all('tr')
    for row in rows:
        details = row.find_all('td')
        try:
            country_name = details[1].get_text()
            currency_name = details[2].get_text()
            currency_symbol = details[3].get_text()
            if currency_name == "Currency":
                continue
            currency_list.append((country_name,currency_name,currency_symbol))
        except:
            continue
    return currency_list
def get_capitals():
    import pandas as pd
    df = pd.read_html("https://en.wikipedia.org/wiki/List_of_national_capitals")[1]
    df.set_index('Country/Territory', inplace=True)
    return df
def add_countries_and_currencies(currency_list):
    capitals_df = get_capitals()
    for currency in currency_list:
        country_name = currency[0]
        currency_name = currency[1]
        currency_symbol = currency[2]
        wiki_link = "https://en.wikipedia.org/wiki/"+country_name.replace(" ","_")
        print(country_name)
        if country_name == "Israel":
            capital_city = "Jerusalem"
        else:
            try:
                capital_city = capitals_df.loc[country_name]['City/Town']
            except:
                capital_city = ""
        print(country_name,capital_city)
        try:
            c = Currency.objects.get(symbol=currency_symbol)
        except:
            c = Currency(name=currency_name, symbol=currency_symbol)
        c.name = currency_name
        c.save()
        try:
            #print("Trying country stuff")
            cy = Country.objects.get(name=country_name)
            cy.name = country_name
            cy.wiki_link = wiki_link
            cy.capital = capital_city
            cy.currency = c
            #print("Updating existing country object", cy)
        except:
            cy = Country(name=country_name, capital=capital_city, wiki_link=wiki_link, currency=c)
            #print("Creating new country object", cy)
        cy.save()
def get_currency_rates(iso_code):
    url = "http://www.xe.com/currencytables/?from=" + iso_code
    import requests
    from bs4 import BeautifulSoup
    x_rate_list = list()
    try:
        page_source = BeautifulSoup(requests.get(url).content)
    except:
        return x_rate_list
    data = page_source.find('tbody')
    data_lines = data.find_all('tr')
    for line in data_lines:
        data=line.find_all('td')
        try:
            x_currency = data[0].get_text().strip()
            x_rate = float(data[2].get_text().strip())
            x_rate_list.append((x_currency,x_rate))
        except:
            continue
    return x_rate_list
def update_xrates(currency):
    try:
        new_rates = get_currency_rates(currency.symbol)
        for new_rate in new_rates:
            from datetime import datetime, timezone
            time_now = datetime.now(timezone.utc)
            try:
                rate_object = Rates.objects.get(currency=currency, x_currency=new_rate[0])
                rate_object.rate = new_rate[1]
                rate_object.last_update_time = time_now
            except:
                rate_object = Rates(currency=currency, x_currency=new_rate[0], rate=new_rate[1],
                                    last_update_time=time_now)
            rate_object.save()
    except:
        pass
def get_stock_list():
    stock_list = list()
    import requests
    from bs4 import BeautifulSoup
    from string import ascii_lowercase
    from time import sleep
    from random import randint
    for c in ascii_lowercase:
        sleep(randint(2,4))
        response = requests.get("https://www.advfn.com/nyse/newyorkstockexchange.asp?companies="+c.upper())
        soup = BeautifulSoup(response.content, 'html.parser')
        table = soup.find_all('table')[3]
        rows = table.find_all('tr')
        for i in range(3, len(rows)):
            details = rows[i].find_all('td')
            try:
                company_name = details[0].get_text()
                ticker = details[1].get_text()
                company_url = rows[i].find('a', href=True)['href']
                stock_list.append((company_name, ticker, company_url))
            except:
                continue
    return stock_list
def add_exchange():
    NYSE = Exchange(name="New York Stock Exchange")
    NYSE.save()
def add_stocks(stock_list):
    for stock in stock_list:
        stock_ticker = stock[1]
        s = Stock(ticker=stock_ticker)
        s.save()
def add_company(stock_list):
    NYSE = Exchange.objects.get(name="New York Stock Exchange")
    for company in stock_list:
        company_name = company[0]
        company_ticker = Stock.objects.get(ticker=company[1])
        c = Company(name=company_name, stock=company_ticker, exchange=NYSE)
        c.save()

def get_stock_details(url):
    stock_details = list()
    import requests
    from bs4 import BeautifulSoup
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    table1 = soup.find_all('table')[2]
    table2 = soup.find_all('table')[3]
    table3 = soup.find_all('table')[4]
    table4 = soup.find_all('table')[7]
    rows1 = table1.find_all('td')
    rows2 = table2.find_all('td')
    rows3 = table3.find_all('td')
    rows4 = table4.find_all('td')
    price_change = rows1[1].get_text()
    change_percent = rows1[2].get_text()
    stock_price = rows1[3].get_text()
    market_cap = rows4[0].get_text()
    shares_in_issue = rows4[1].get_text()
    revenue = rows4[3].get_text()
    profit_loss = rows4[4].get_text()
    EPS = rows4[5].get_text()
    PE_ratio = rows4[6].get_text()
    stock_details = (price_change, change_percent, stock_price, market_cap, shares_in_issue, revenue, profit_loss, EPS, PE_ratio)
    return stock_details

def read_function():
    import pandas as pd
    df=pd.read_csv("./static/stocks_list.csv")
    stock_list=df.values.tolist()
    if (Stock.objects.count() == 0):
        for stock in stock_list:
            stock_name = stock[0]
            stock_ticker = stock[1]
            stock_url =stock[2]
            s = Stock(name=stock_name, ticker=stock_ticker, url=stock_url)
            #print(stock_name, stock_url, stock_ticker)
            s.save()
    #print("worked")
    return

# javascript for auto refresh
#file upload by user