from bs4 import BeautifulSoup as soup
import requests
import pytz
import datetime
import csv

page_url = "https://en.wikipedia.org/wiki/2019_in_spaceflight#Orbital_launches"
date_time_str = 'Dec 31 2019'
numdays=365
query_strings = {"Operational","En route","Successful"}

#creating dates dictionary with all the dates from 2019
date_dict = {}
base_obj = datetime.datetime.strptime(date_time_str,'%b %d %Y')
date_list = [base_obj - datetime.timedelta(days=x) for x in range(numdays)]
date_list.reverse()
for i in date_list:
    date_dict[i]=0

#reading the website and storing as a BeautifulSoup object
try:
    website_url = requests.get(page_url).text
except:
    print("Unable to connect to the given URL. Check Internet Connection/URL")
    exit(0)

page_soup = soup(website_url,"lxml")

#finding all tables with the relevant class
My_table = page_soup.find_all('table',{'class':'wikitable collapsible'})

#keeping only the first table a.k.a. table for Orbital Launches
table = My_table[0]

#storing all rows in table_rows
table_rows = table.find_all("tr")


row_index = 3 #ignoring the header rows

while row_index<len(table_rows):
    row = table_rows[row_index]
    row_items = row.find_all("td")
    if len(row_items)==5: #head of the launch line
        main_item = row_items[0] #line with date of launch and number of rows this launch spans
        day_month = main_item.span.text

        #cleaning day_month
        if "[" in day_month:
            day_month=day_month[:day_month.find("[")]
        if "(" in day_month:
            day_month=day_month[:day_month.find("(")]
        day_month = day_month.strip() + " 2019"

        curr_obj = datetime.datetime.strptime(day_month, '%d %B %Y')
        row_span = int(main_item.get("rowspan")) #stores the number of rows this launch spans

        i = 0
        flag = False #true only if a payload is operational,Successful or en route
        while i<(row_span-1):
            row_index+=1
            r = table_rows[row_index]
            r_items = r.find_all("td")
            if len(r_items)==6:
                status = (r_items[-1].text).strip()
                if "[" in status:
                    status = status[:status.find("[")]
                if status in query_strings:
                    flag = True
            i+=1
        if flag:
            date_dict[curr_obj]+=1
    row_index+=1

#writing to csv file
with open('output.csv', mode='w') as op:
    op_writer = csv.writer(op)
    op_writer.writerow(["date","value"])
    for d in date_list:
        op_writer.writerow([d.isoformat(),date_dict[d]])
