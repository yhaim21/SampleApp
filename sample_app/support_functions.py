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



def get_stock_list():
    stock_list = list()
    import requests
    from bs4 import BeautifulSoup
    from string import ascii_lowercase
    from time import sleep
    from random import randint
    for c in ascii_lowercase:
        sleep(randint(1,2))
        response = requests.get("https://www.advfn.com/nyse/newyorkstockexchange.asp?companies="+c.upper())
        soup = BeautifulSoup(response.content, 'html.parser')
        table = soup.find_all('table')[3]
        rows = table.find_all('tr')
        for i in range(3, len(rows)):
            details = rows[i].find_all('td')
            try:
                company_name = details[0].get_text()
                ticker = details[1].get_text()
                stock_list.append((company_name, ticker))
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