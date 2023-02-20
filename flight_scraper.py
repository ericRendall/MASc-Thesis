#this scripty script will be for trying to scrape all the best g damn flights to yaurope

#notes
    #good thing is that the airport codes in the site are not case sensitive no no need to convert all strings into uppercase letters
    #CANNOT search more than ten airports at the same time, need to break up EU list into groups of 10
    #also, all airport codes entered must be separated by a comma or wont work
    
    #ok for the button issue, lamba method gives function memory as to what index in the loop should be called by what function 
        #instead of just looking it up at run time it remembers what index it was assigned in the loop
        #this is good cause now each button opens a unique link instead of just the last link
        #but problem is it only calls it from the last list_of_links list created 
        #so all buttons are linked in order but only to last created list_of_links list which is a problem when searching more than one date
        #i think the soln is to append each list_of_links list to another list so list within a list or nested list 
        #then use same lambda method to remember both the index within the list but also the index of the list itself - kinda confusing
            #IT WORKED LETS FUCKING GO
            
    #STALE ELEMENT ERRORS:
        #occurs when element requested isnt attached to the page
        #i think shorter delays cause this to occur more frequently cause the page isnt fully loaded and its trying to pull all 15 flight cards
        #longer delay after giving the driver the URL but before requesting the elements will give it time to load and will probably fix the problem
        #only thing is that delay may be dependent on the users wifi speed and with slow ass wifi may not be sufficient

from glob import glob
from time import sleep
from urllib import request
from venv import create
import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup
import os 
from tkinter import *

from webdriver_manager.chrome import ChromeDriverManager

from tkcalendar import Calendar
from datetime import datetime

from datetime import timedelta, date
import webbrowser
import requests

#this package is for pulling out substring between two strings lol
import re
from tkinter import ttk

import unidecode #this is for getting rid of those weird \xa characters in the price data

#first thing to do is get current date to set on calendar widget
date_time = datetime.today()
year = date_time.year
month = date_time.month
day = date_time.day

#IMPORT ALL EU AIRPORTS
EU_airport_list = ['TIA', 'EVN', 'GRZ', 'INN', 'KLU', 'LNZ', 'SZG', 'VIE', 'GYD', 'MSQ', 'ANR', 'BRU', 'CRL',
'LGG', 'OST', 'SJJ', 'TZL', 'BOJ', 'SOF', 'VAR', 'DBV', 'PUY', 'SPU', 'ZAD', 'ZAG', 'LCA', 'PFO', 'BRQ', 'PRG',
'AAL', 'AAR', 'BLL', 'CPH', 'FAE', 'TLL', 'HEL', 'OUL', 'RVN', 'TMP', 'TKU', 'VAA', 'AJA', 'BIA', 'EGC', 'BIQ',
'BOD', 'BES', 'FSC', 'LIL', 'LYS', 'MRS', 'MPL', 'NTE', 'NCE', 'BVA', 'CDG', 'ORY', 'SXB', 'RNS', 'RUN', 'TLN',
'TLS', 'KUT', 'TBS', 'FMM', 'BER', 'SXF', 'TXL', 'BRE', 'CGN', 'DTM', 'DRS', 'DUS', 'FRA', 'HHN', 'FDH', 'HAM',
'HAJ', 'FKB', 'LEJ', 'MUC', 'FMO', 'NUE', 'PAD', 'STR', 'NRN', 'ATH', 'CHQ', 'CFU', 'HER', 'KGS', 'JMK', 'RHO',
'JTR', 'SKG', 'ZTH', 'BUD', 'DEB', 'KEF', 'ORK', 'DUB', 'NOC', 'KIR', 'SNN', 'AHO', 'AOI', 'BRI', 'BGY', 'BLQ',
'BDS', 'CAG', 'CTA', 'CIY', 'FLR', 'GOA', 'SUF', 'LIN', 'MXP', 'NAP', 'OLB', 'PMO', 'PEG', 'PSR', 'PSA', 'CIA', 
'FCO', 'TPS', 'TSF', 'TRN', 'VCE', 'VRN', 'ALA', 'TSE', 'PRN', 'RIX', 'KUN', 'VNO', 'LUX', 'MLA', 'KIV', 'TGD',
'TIV', 'AMS', 'EIN', 'GRQ', 'MST', 'RTM', 'SKP', 'AES', 'BGO', 'BOO', 'HAU', 'KRS', 'OSL', 'TRF', 'SVG', 'TOS',
'TRD', 'GDN', 'KTW', 'KRK', 'POZ', 'SZZ', 'WAW', 'WMI', 'WRO', 'FAO', 'LIS', 'FNC', 'PDL', 'OPO', 'OTP', 'CLJ', 
'IAS', 'TSR', 'SVX', 'KRR', 'DME', 'SVO', 'VKO', 'ZIA', 'OVB', 'LED', 'AER', 'BEG', 'INI', 'BTS', 'KSC', 'LJU', 
'ALC', 'LEI', 'OVD', 'BCN', 'BIO', 'FUE', 'GRO', 'LPA', 'GRX', 'IBZ', 'XRY', 'SPC', 'ACE', 'MAD', 'AGP', 'MAH', 
'PMI', 'RMU', 'REU', 'SDR', 'SCQ', 'SVQ', 'TFN', 'TFS', 'VLC', 'ZAZ', 'GOT', 'MMX', 'ARN', 'BMA', 'NYO', 'VST', 
'BSL', 'BRN', 'GVA', 'ZRH', 'ADA', 'ESB', 'AYT', 'DLM', 'IST', 'SAW', 'ADB', 'BJV', 'TZX', 'HRK', 'KBP', 'IEV', 
'LWO', 'ODS', 'ABZ', 'BHD', 'BFS', 'BHX', 'BRS', 'CWL', 'DSA', 'EMA', 'EDI', 'EXT', 'GLA', 'PIK', 'HUY', 'JER',
'LBA', 'LPL', 'LCY', 'LGW', 'LHR', 'LTN', 'SEN', 'STN', 'MAN', 'NCL', 'SOU']

#because there are two options for arrival airports (all EU, or typed response), use booleans to figure out which one was used 

arrivals_were_typed = FALSE

arrivals_were_not_typed = FALSE

#######################################################CREATE ROOT WINDOW###########################################################
#make this into a GUI and then an executable 
#create root app
root = Tk()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
adjusted_width = screen_width/1.3
adjusted_height = screen_height/1.3
screenWidth_int = int(adjusted_width)
screenHeight_int = int(adjusted_height)
screenWidth_String = str(screenWidth_int)
screenHeight_String = str(screenHeight_int)
gui_size = screenWidth_String + "x" + screenHeight_String
root.geometry(gui_size) #allows x,y size of GUI window to be set in terms of pixel number
root.resizable(True, True)
root.configure(background = 'old lace')

masterNotebook = ttk.Notebook(root)
masterNotebook.grid(row = 0, column = 0)
style = ttk.Style()
style.theme_use('default')
style.configure('TNotebook.Tab', background="gray70", font=('Helvetica','14'))
style.map("TNotebook", background= [("selected", "gray70")])

#now create the initial page
search_page = Frame(masterNotebook, width = adjusted_width, height = adjusted_height, bg = 'old lace')
search_page.pack(fill = "both", expand = 1)
masterNotebook.add(search_page, text= "SEARCH FLIGHTS")

#########################################################START BUILDING FRONT END###################################################
#need to have option for selecting date range, also airport (either all or space to type in specific ones)

################DATE SELECT################################################################
date_range_label = Label(search_page, text = "select date range", font = (40), bg = 'old lace')
date_range_label.place(relx = 0.15, rely = 0.15, anchor = "center")

#create calendar to select from
start_cal = Calendar(search_page, selectmode = 'day', year = year, month = month, day = day)
start_cal.place(relx = 0.15, rely = 0.3, anchor = "center")

def getStart():
    
    global start_date
    
    start_date = start_cal.get_date() #this is string type 
    start_cal_button['state'] = DISABLED
    end_cal_button['state'] = NORMAL


start_cal_button = Button(search_page, text = "select start date", bg = 'cornflower blue', command = getStart)
start_cal_button.place(relx = 0.15, rely = 0.45, anchor = "center")

#NOW CREATE END CALENDAR
end_cal = Calendar(search_page, selectmode = 'day', year = year, month = month, day = day)
end_cal.place(relx = 0.15, rely = 0.6, anchor = "center")

def getEnd():
    end_date = end_cal.get_date() #this is string type
    end_cal_button['state'] = DISABLED
    departure_entry['state'] = NORMAL
    
    confirm_departure['state'] = NORMAL
    
    #in here want to properly strucutre travel date data so that it can be fed into the URL later on
    new_start_date = start_date.split('/')
    new_end_date = end_date.split('/')
    #now pull out day month year data
    start_month = int(new_start_date[0])
    start_day = int(new_start_date[1])
    start_year = int(new_start_date[2]) + 2000 
    
    end_month = int(new_end_date[0])
    end_day = int(new_end_date[1])
    end_year = int(new_end_date[2]) + 2000
    
    #random method for day difference
    def daterange(date1, date2):
        for n in range(int((date2 - date1).days) + 1):
            yield date1 + timedelta(n)

    start_dt = date(start_year, start_month, start_day)
    end_dt = date(end_year, end_month, end_day)
    
    global formatted_dates_array #this will be accessed later
    
    formatted_dates_array = [] #this array will now contain all properly formatted strings for date in URL
    
    for dt in daterange(start_dt, end_dt):
        formatted_dates_array.append(dt.strftime("%Y-%m-%d")) 
    
    
end_cal_button = Button(search_page, text = "select end date", bg = 'cornflower blue', command = getEnd)
end_cal_button.place(relx = 0.15, rely = 0.75, anchor = "center")
end_cal_button['state'] = DISABLED
###############################################################################################

#################DEPARTURE AIRPORTS################################################################
departure_airport_label = Label(search_page, text = "type departure airport code(s) - separate with ,", font = (40), bg = 'old lace')
departure_airport_label.place(relx = 0.5, rely = 0.22, anchor = "center")

departure_entry = Entry(search_page)
departure_entry.place(relx = 0.5, rely = 0.28, height = 30, width = 400, anchor = "center")
departure_entry['state'] = DISABLED

#now create button for submitting departure options 
def submitDeparture():
    departure_entry['state'] = DISABLED
    confirm_departure['state'] = DISABLED
    
    arrival_entry['state'] = NORMAL
    #all_airports_button['state'] = NORMAL #haven't built this function yet, leave this disabled for now
    confirm_arrival['state'] = NORMAL
    
    global DEPARTURE_AIRPORTS
    
    #now get entry as string for IATA codes
    DEPARTURE_AIRPORTS = departure_entry.get()
    

confirm_departure = Button(search_page, text = "confirm departure airports", bg = 'cornflower blue', command = submitDeparture)
confirm_departure.place(relx = 0.5, rely = 0.35, anchor = "center")
confirm_departure['state'] = DISABLED

#also maybe create button to database to search airport codes
def searchIATA():
    webbrowser.open('https://www.iata.org/en/publications/directories/code-search/')

IATA_button = Button(search_page, text = "search IATA codes", command = searchIATA)
IATA_button.place(relx = 0.5, rely = 0.15, anchor = "center")
#####################################################################################################

################ARRIVAL AIRPORTS####################################################################
arrival_airport_label = Label(search_page, text = "type arrival airport code(s) - separate with ,", font = (40), bg = 'old lace')
arrival_airport_label.place(relx = 0.8, rely = 0.29, anchor = "center")

arrival_entry = Entry(search_page)
arrival_entry.place(relx = 0.8, rely = 0.35, height = 30, width = 400, anchor = "center")
arrival_entry['state'] = DISABLED

def submitArrival():
    confirm_arrival['state'] = DISABLED
    all_airports_button['state'] = DISABLED
    arrival_entry['state'] = DISABLED
    
    cheapest_button['state'] = NORMAL
    fastest_button['state'] = NORMAL
    best_button['state'] = NORMAL
    
    global ARRIVAL_AIRPORTS
    
    #grab entry as string
    ARRIVAL_AIRPORTS = arrival_entry.get()
    #now set the boolean true
    global arrivals_were_typed
    arrivals_were_typed = TRUE
    
    
confirm_arrival = Button(search_page, text = "confirm arrival airports", bg = 'cornflower blue', command = submitArrival)
confirm_arrival.place(relx = 0.8, rely = 0.42, anchor = "center")
confirm_arrival['state'] = DISABLED

def allAirports(): #pretty obvious whats gonna happen in here
    confirm_arrival['state'] = DISABLED
    all_airports_button['state'] = DISABLED
    arrival_entry['state'] = DISABLED
    
    #search_button['state'] = NORMAL
    
    global ARRIVAL_AIRPORTS
    
    global ARRIVAL_AIRPORTS_0
    global ARRIVAL_AIRPORTS_1
    global ARRIVAL_AIRPORTS_2
    global ARRIVAL_AIRPORTS_3
    global ARRIVAL_AIRPORTS_4
    global ARRIVAL_AIRPORTS_5
    global ARRIVAL_AIRPORTS_6
    global ARRIVAL_AIRPORTS_7
    global ARRIVAL_AIRPORTS_8
    global ARRIVAL_AIRPORTS_9
    global ARRIVAL_AIRPORTS_10
    global ARRIVAL_AIRPORTS_11
    global ARRIVAL_AIRPORTS_12
    global ARRIVAL_AIRPORTS_13
    global ARRIVAL_AIRPORTS_14
    global ARRIVAL_AIRPORTS_15
    global ARRIVAL_AIRPORTS_16
    global ARRIVAL_AIRPORTS_17
    global ARRIVAL_AIRPORTS_18
    global ARRIVAL_AIRPORTS_19
    global ARRIVAL_AIRPORTS_20
    global ARRIVAL_AIRPORTS_21
    global ARRIVAL_AIRPORTS_22
    global ARRIVAL_AIRPORTS_23
    global ARRIVAL_AIRPORTS_24
    global ARRIVAL_AIRPORTS_25
    global ARRIVAL_AIRPORTS_26
    
    #now set arrival airports to all EU airports
    ARRIVAL_AIRPORTS = EU_airport_list
    #need to split into groups of 10 to search with
    ARRIVAL_AIRPORTS_0 = ARRIVAL_AIRPORTS[0:10]
    ARRIVAL_AIRPORTS_1 = ARRIVAL_AIRPORTS[10:20]
    ARRIVAL_AIRPORTS_2 = ARRIVAL_AIRPORTS[20:30]
    ARRIVAL_AIRPORTS_3 = ARRIVAL_AIRPORTS[30:40]
    ARRIVAL_AIRPORTS_4 = ARRIVAL_AIRPORTS[40:50]
    ARRIVAL_AIRPORTS_5 = ARRIVAL_AIRPORTS[50:60]
    ARRIVAL_AIRPORTS_6 = ARRIVAL_AIRPORTS[60:70]
    ARRIVAL_AIRPORTS_7 = ARRIVAL_AIRPORTS[70:80]
    ARRIVAL_AIRPORTS_8 = ARRIVAL_AIRPORTS[80:90]
    ARRIVAL_AIRPORTS_9 = ARRIVAL_AIRPORTS[90:100]
    ARRIVAL_AIRPORTS_10 = ARRIVAL_AIRPORTS[100:110]
    ARRIVAL_AIRPORTS_11 = ARRIVAL_AIRPORTS[110:120]
    ARRIVAL_AIRPORTS_12 = ARRIVAL_AIRPORTS[120:130]
    ARRIVAL_AIRPORTS_13 = ARRIVAL_AIRPORTS[130:140]
    ARRIVAL_AIRPORTS_14 = ARRIVAL_AIRPORTS[140:150]
    ARRIVAL_AIRPORTS_15 = ARRIVAL_AIRPORTS[150:160]
    ARRIVAL_AIRPORTS_16 = ARRIVAL_AIRPORTS[160:170]
    ARRIVAL_AIRPORTS_17 = ARRIVAL_AIRPORTS[170:180]
    ARRIVAL_AIRPORTS_18 = ARRIVAL_AIRPORTS[180:190]
    ARRIVAL_AIRPORTS_19 = ARRIVAL_AIRPORTS[190:200]
    ARRIVAL_AIRPORTS_20 = ARRIVAL_AIRPORTS[200:210]
    ARRIVAL_AIRPORTS_21 = ARRIVAL_AIRPORTS[210:220]
    ARRIVAL_AIRPORTS_22 = ARRIVAL_AIRPORTS[220:230]
    ARRIVAL_AIRPORTS_23 = ARRIVAL_AIRPORTS[230:240]
    ARRIVAL_AIRPORTS_24 = ARRIVAL_AIRPORTS[240:250]
    ARRIVAL_AIRPORTS_25 = ARRIVAL_AIRPORTS[250:260]
    ARRIVAL_AIRPORTS_26 = ARRIVAL_AIRPORTS[260:270]
    
    #now set boolean true
    global arrivals_were_not_typed
    arrivals_were_not_typed = TRUE

all_airports_button = Button(search_page, text = "all EU airports", bg = 'cornflower blue', command = allAirports)
all_airports_button.place(relx = 0.8, rely = 0.5, anchor = "center")
all_airports_button['state'] = DISABLED #this should be unlocked after the other two things are dealt with

or_label = Label(search_page, text = "OR", font = (50), bg = 'old lace')
or_label.place(relx = 0.8, rely = 0.46, anchor = "center")

#CREATE BUTTONS TO SELECT BETWEEN CHEAPEST, FASTEST, AND BEST FLIGHTS
def cheapestFunction():
    cheapest_button['state'] = DISABLED
    fastest_button['state'] = DISABLED
    best_button['state'] = DISABLED
    
    search_button['state'] = NORMAL
    
    global search_type
    search_type = 'price_a'

cheapest_button = Button(search_page, text = "cheapest", bg = 'cornflower blue', command = cheapestFunction)
cheapest_button.place(relx = 0.43, rely = 0.6, anchor = "center")
cheapest_button['state'] = DISABLED

def fastestFunction():
    cheapest_button['state'] = DISABLED
    fastest_button['state'] = DISABLED
    best_button['state'] = DISABLED
    
    search_button['state'] = NORMAL
    
    global search_type
    search_type = 'duration_a'

fastest_button = Button(search_page, text = "fastest", bg = 'cornflower blue', command = fastestFunction)
fastest_button.place(relx = 0.5, rely = 0.6, anchor = "center")
fastest_button['state'] = DISABLED

def bestFunction():
    cheapest_button['state'] = DISABLED
    fastest_button['state'] = DISABLED
    best_button['state'] = DISABLED
    
    search_button['state'] = NORMAL
    
    global search_type
    search_type = 'bestflight_a'

best_button = Button(search_page, text = "best", bg = 'cornflower blue', command = bestFunction)
best_button.place(relx = 0.57, rely = 0.6, anchor = "center")
best_button['state'] = DISABLED
########################################################################################################

###############################################START BUILDING BACKEND########################################################################

#scrape price, departure and arrival location, trip time, and link to offer

all_links = [] #defined outside the function so the data in this array doesn't get overwritten

list_of_lists = []

def searchFlights():
    search_button['state'] = DISABLED
    
    #THERE ARE TWO POSSIBLE CASES IN HERE
        #one is where arrivals_were_typed = TRUE
        #the other is where arrivals_were_not_typed = TRUE
        #searching will be different for these two methods
    #now here do all the scraping shyte
    
    dates_iterator = 0
    
    while dates_iterator <= len(formatted_dates_array) - 1:
        
        travel_date = formatted_dates_array[dates_iterator] #this will be stuffed into the link
        
        try: #to handle the stupid element is not attached to the page error        
        
            if arrivals_were_typed == TRUE:
            
                driver = webdriver.Chrome(ChromeDriverManager().install())
                url = f'https://www.ca.kayak.com/flights/{DEPARTURE_AIRPORTS}-{ARRIVAL_AIRPORTS}/{travel_date}?sort={search_type}'

                driver.get(url)
                sleep(5) #the smaller the delay, seems like more stale element errors occur, with 5 seconds they occur every time. With 10 seconds only sometimess
            
                #now can begin to pull out flight info 
                flight_rows = driver.find_elements("xpath", '//div[@class="inner-grid keel-grid"]') #comes from inspecting the element of the flight card on the website
                #print(flight_rows) #sweet it works and is pulling the web elements out on the page
            
                global list_prices
                global start_and_end_location
                global trip_time
                global offer_link
            
                list_prices = []
                start_and_end_location = []
                trip_time = []
                offer_link = []
            
                for WebElement in flight_rows:
                    elementHTML = WebElement.get_attribute('outerHTML')
                    elementSoup = BeautifulSoup(elementHTML, 'html.parser')
                
                    #extract prices
                    temp_price = elementSoup.find("div", {"class": "col-price result-column js-no-dtog"}) #again from inspecting the element
                    price = temp_price.find("span", {"class": "price option-text"})
                    #this could be confusing but basically this span tag price thing is statically created whereas the actualy price text is dynamically created 
                        #cant automate the dynamically created extraction so went up one element within the element heirarchy 
                        #this element is statically created but is used all across the page on every flight card 
                        #howeveer, since we are laready working within an element, this should only exist once within this element and so we can call it and extract the data i think
                
                    list_prices.append(price.text) #so append to the price list and pull out the text
                
                    #departure and arrival location
                    location = elementSoup.find("div", {"class": "bottom"})
                    start_and_end_location.append(location.text)
                
                    #trip time
                    time = elementSoup.find("div", {"class": "section duration allow-multi-modal-icons"})
                    trip_time.append(time.text)
                
                    #finally, try to get link to offer so user can click from results, for this need the HREF i think but not sure how to get it 
                    #use xpath of button?, in the HTML look for the object that says role = button since thats the actual button
                    #sleep(5)
                    #view_deal_button = '//*[@id="c4wGi-mb-bE-130ff2b47dc"]' #right click copy xpath to get this
                
                    #offer_link.append(elementSoup.find_all(['a'],{'class':['booking-link']}))
                    offer_link.append(elementSoup.find_all(href = True)) #this method is way better and actually pulls out the correct number of href links unlike the other one that pulls out 45 ish
                    #links embedded in the output
                        #need to have kayak.,com or whatever added to the string. 
                        #also, every & symbol in the link gets an added 'amp;' for some weird reason
                        #so that needs to be .replace("amp;", "") before the link can be clickable by the user
                    
                        #since there are 15 objects per page, the length of offer_link is 15, can loop through each index and then figure out how to pull out the link somehow 
                            #maybe step one is to convert each index into text or string somehow then do the string search to find the link
            
            
                #before converting to string, need to separate out all indeces from the object
                #maybe just append to a list of strings
            
                list_of_strings = []
                i = 0
            
                while i <= len(offer_link) - 1:
                
                    list_of_strings.append(str(offer_link[i]))
                
                    i = i + 1

                #now with list of strings all categorized can loop through the new list and pull out the links
                list_of_links = []
                k = 0
            
                kayak_string = 'https://www.ca.kayak.com'
            
                while k <= len(list_of_strings) - 1: #LETS FUCKING GO THIS SHIT WORKS
                
                    #use the re library to syphon out the links lol
                    temp_link = re.search('href="(.*)" id="', list_of_strings[k])
                
                    temp_flight_link = kayak_string + temp_link.group(1)
                    #now remove all the amperand crap
                    flight_link = temp_flight_link.replace('amp;', '') #replace amp; with nothing to take it out of link
                
                    list_of_links.append(flight_link)
                    
                    all_links.append(flight_link) #this list will contain every link from the whole search and will be used to generate the buttons
                
                    k = k + 1
                    
                #now append the list of links to the list of lists
                list_of_lists.append(list_of_links) #now each index of this should contain an entire list of links...i think
            
                #need to clean the outputs - links are good but the other three are full of junk
                    #then maybe can write to a file or something, still not sure how the data should be presented to the user
                #list_prices
                #start_and_end_location
                #trip_time 
            
                list_prices_cleaned = []
                derp = 0
            
                while derp <= len(list_prices) - 1:
                
                    temp_val = list_prices[derp]
                    temp_val_0 = temp_val.replace('\n', '')
                    temp_val_0 = unidecode.unidecode(temp_val_0) #gets rid of the \xa character
                    
                    list_prices_cleaned.append(temp_val_0)
                
                    derp = derp + 1
            
            
                list_locations_cleaned = []
                derpderp = 0
            
                while derpderp <= len(start_and_end_location) - 1:
                
                    temp_val = start_and_end_location[derpderp]
                    list_locations_cleaned.append(temp_val.replace('\n', ''))
                
                    derpderp = derpderp + 1
                
            
                list_trip_time_cleaned = []
                derpderpderp = 0
            
                while derpderpderp <= len(trip_time) - 1:
                
                    temp_val = trip_time[derpderpderp]
                    list_trip_time_cleaned.append(temp_val.replace('\n',''))
                
                    derpderpderp = derpderpderp + 1
                
                #now should have all cleaned strings
                #NEED TO ADD IN DATE FOR THESE FLIGHTS BUT THIS CAN COME FROM USER SELECTION ON CALENDAR AS NOT ON FLIGHT CARD ON SITE
                    #now need to figure out how to display data
                    #maybe make a pop up window with an option to export to csv
                
                create_new_page = Frame(masterNotebook, width = adjusted_width, height = adjusted_height, bg = 'old lace')
                create_new_page.pack(fill = "both", expand = 1)
                masterNotebook.add(create_new_page, text= f"{formatted_dates_array[dates_iterator]}") #now this should create new tab w title of each date selected in the date range picker
                root.update() #push the update onto the screen
                
                ###########NOW CAN START ADDING IN EACH FLIGHT RESULT INTO THE PAGE###############
                #results_iterator = 0
                y_start_val = 0.15
                
                for i in range(len(list_of_links)): #the list could be any of them just chose links arbitrarily 
                    
                    #FIRST SHOW DEPARTING AND ARRIVING AIRPORT
                    location_label = Label(create_new_page, text = f"{list_locations_cleaned[i]}", bg = 'old lace')
                    location_label.place(relx = 0.2, rely = y_start_val, anchor = "center")
                    
                    #NOW DO PRICE
                    price_label = Label(create_new_page, text = f"{list_prices_cleaned[i]}", bg = 'old lace')
                    price_label.place(relx = 0.4, rely = y_start_val, anchor = "center")
                    
                    #NOW TRIP TIME
                    trip_time_label = Label(create_new_page, text = f"{list_trip_time_cleaned[i]}", bg = 'old lace')
                    trip_time_label.place(relx = 0.6, rely = y_start_val, anchor = "center")
                    
                    #try again the button crap lol
                    def linkFunction(var, new_var):
                        #pull out list from list of lists
                        temp_list = list_of_lists[new_var]
                        webbrowser.open(temp_list[var])
                    
                    link_button = Button(create_new_page, text = "Link to Offer", bg = 'cornflower blue', command = lambda var = i, new_var = dates_iterator: linkFunction(var, new_var))
                    link_button.place(relx = 0.8, rely = y_start_val, anchor = "center")
                    
                    #results_iterator = results_iterator + 1
                    y_start_val = y_start_val + 0.05
                
                    
                dates_iterator = dates_iterator + 1 #i think this goes here but not sure tbh lol
                    
            else: #this is then the case where all EU airports were selected as arrivals which the code is gonna be harder for this section
                #for now just work on the typed arrivals section
                pass
            
        except Exception as e:
            pass #since the stale element error occurs before the iterator is reached, it never actually increments up 
            #so when the computer passes through the exception it goes back to start of while loop and the iterator it reads is the same as before
            #so it just keeps retrying until it passes which is what was desired
            print("error occured") #doesn't really do anything, just to see how many errors occur
        
    #buttons have to be created outside the while loop otherwise they keep getting overwritten
    #here create buttons based on filled list of all links pulled across all pages and dates
    
            
search_button = Button(search_page, text = "search flights", fg = 'blue', bg = 'dark goldenrod', font = 'bold', command = searchFlights)
search_button.place(relx = 0.5, rely = 0.7, anchor = 'center', height = 40, width = 100)
search_button['state'] = DISABLED

#add in reset page button
def resetSearch():
    #in here would reset all buttons and such to make another search without having to quit the app
    
    global arrivals_were_typed
    global arrivals_were_not_typed
    
    arrivals_were_typed = FALSE
    arrivals_were_not_typed = FALSE

reset_button = Button(search_page, text = "reset search parameters", command = resetSearch)
reset_button.place(relx = 0.5, rely = 0.8, anchor = "center")

#############################################################END LOOP##############################################################################
root.mainloop()