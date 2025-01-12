import pycountry

def GetCountryNames():
    countryNames= []
    countries = pycountry.countries
    for country in countries:
        countryNames.append(country.name)
    return countryNames