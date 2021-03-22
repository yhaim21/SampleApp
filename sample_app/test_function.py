

def get_capitals():
    import pandas as pd
    df = pd.read_html("https://en.wikipedia.org/wiki/List_of_national_capitals")[1]
    df.set_index('Country/Territory', inplace=True)
    return df

x = get_capitals()
print(x.loc['Armenia']['City/Town'])