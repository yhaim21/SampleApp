from django.contrib import admin

# Register your models here.
from sample_app.models import Currency, Country, Rates

class CountryInLine(admin.TabularInline):
    fields = ('name','capital','wiki_link')
    model = Country
    extra = 0

class CurrencyAdmin(admin.ModelAdmin):
    fields = ('name','symbol')
    inlines = [CountryInLine]

admin.site.register(Currency,CurrencyAdmin)
