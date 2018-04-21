from requests import get
from bs4 import BeautifulSoup
from utility import *

data_filename="data.csv"


def scarp_company_data():
    htmlcontent = get("http://startupgoa.org/companies/#.WtoXUXVubZu")
    soup = BeautifulSoup(htmlcontent.text,"lxml")
    companies = soup.findAll("li", {"class": "company-name"})

    empty_file(data_filename)
    data_file = open(data_filename,'w+')
    data_file.write("company_name,startup_goa_link\n")
    for company in companies:
        link = company.find('a')
        data_file.write(format_company_name(link.getText()) + ',' + link.get('href')+ '\n')
    data_file.close()

    print("data scrapped from startupgoa.org")    


def main():
    scarp_company_data()
    pass

if __name__ == '__main__':
    main()
