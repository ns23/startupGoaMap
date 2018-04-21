from requests import get
from bs4 import BeautifulSoup
from utility import format_company_name,empty_file
import googlemaps
import pandas
import math
from folium import Map, FeatureGroup, CircleMarker
import math
import webbrowser

key = None # replace key with actual key for script to get data from google geocode API

if key != None:
    gmaps = googlemaps.Client(key=key)

data_filename="data.csv"
map_name = 'index.html'

def scarp_company_data():
    htmlcontent = get("http://startupgoa.org/companies/#.WtoXUXVubZu")
    soup = BeautifulSoup(htmlcontent.text,"lxml")
    companies = soup.findAll("li", {"class": "company-name"})

    empty_file(data_filename)
    data_file = open(data_filename,'w+')
    data_file.write("company_name|startup_goa_link\n")
    for company in companies:
        link = company.find('a')
        data_file.write(format_company_name(link.getText()) + '|' + link.get('href')+ '\n')
    data_file.close()

    print("data scrapped from startupgoa.org")    


def gmaps_wrapper(address):
    address = address + ',goa'
    google_res = gmaps.geocode(address, region='IN')
    
    if len(google_res) == 0:
        return None
    else:
        return google_res    
    
def get_google_geo():
    df = pandas.read_csv('data.csv', delimiter='|')
    df['gmap'] = df['company_name'].apply(gmaps_wrapper)

    df["lat"] = df.gmap.apply(
        lambda s: s[0]['geometry']['location']['lat'] if s != None else None)
    df["lng"] = df.gmap.apply(
        lambda s: s[0]['geometry']['location']['lng'] if s != None else None)
    df["place_id"] = df.gmap.apply(
        lambda s: s[0]['place_id'] if s != None else None)
    df["formatted_address"] = df.gmap.apply(
        lambda s: s[0]['formatted_address'] if s != None else None)

    empty_file('op.csv')    
    df.to_csv(path_or_buf='op.csv', sep='|')
    return df   

def compute_map(df):
    lat = list(df['lat'])
    lng = list(df['lng'])
    company_name = list(df['company_name'])

    map = Map(location=[15.2993, 74.1240], zoom_start=10)
    fgv = FeatureGroup()
    for lt, ln, name in zip(lat, lng, company_name):
        if not math.isnan(lt):
            fgv.add_child(CircleMarker(location=[lt, ln], radius=6, popup=
                name, fill_color="green", fill=True,  color='grey', fill_opacity=0.7))
    pass

    map.add_child(fgv)
    map.save(map_name)


def main():
    if key != None:
        scarp_company_data()
        df = get_google_geo()
    else:
        df = pandas.read_csv('op.csv',delimiter='|')

    compute_map(df)
    webbrowser.open(map_name,new=2)

if __name__ == '__main__':
    main()
