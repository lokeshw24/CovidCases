from bs4 import BeautifulSoup
import urllib.request
import pandas as pd

from datetime import date
today = str( date.today().strftime('%d_%m_%Y'))

import ssl
ssl._create_default_https_context = ssl._create_unverified_context


IndiaGovtWebsite = 'https://www.mygov.in/covid-19'

content = urllib.request.urlopen(IndiaGovtWebsite)

soup = BeautifulSoup(content, 'html.parser')

stateNames = soup.find_all("span", {"class" : "st_name"})              #List of all the state-names from the website
confirmedCases =  soup.find_all("div", {"class" : "tick-confirmed"})   #List of all CC for every state
activeCases = soup.find_all("div", {"class" : "tick-active"})          #List of all AC for every state
deaths = soup.find_all( "div", {"class" : "tick-death"})               #List of all DC for every state

totalEntries = len(stateNames)

dict_CC = {}        #Create a dict of state-name vs Confirmed Cases
dict_AC = {}        #Create a dict of state-name vs Active Cases
dict_DC = {}        #Create a dict of state-name vs Death Cases

for pos in range( 0, totalEntries ) :
    currStateName = stateNames[pos].text

    confirmCase = confirmedCases[pos].text.split(' ')[1]
    confirmCase = confirmCase.replace(",", "")   #Remove commas from the numbers
    dict_CC[ currStateName ] = int(confirmCase)

    activeCase = activeCases[pos].text.split(' ')[1]
    activeCase = activeCase.replace(",", "")
    dict_AC[ currStateName ] = int(activeCase )

    deathCase = deaths[pos].text.split(' ')[1]
    deathCase = deathCase.replace(",", "")
    dict_DC[ currStateName ] = int(deathCase)

#Use pandas to write the above data in a spreadsheet.
ExcelSheetPath = "/Users/loki/Desktop/CovidCases/" +  today + ".xlsx"
writer = pd.ExcelWriter(ExcelSheetPath, engine='xlsxwriter')


#Convert the dict into a DataFrame.
df_CC = pd.DataFrame( dict_CC, index=[today] )        #Here first-row = StateNames (Keys of the Dict)
                                                      #and second-row = Confirmed Cases (Values of the Dict)
                                                      #While writing to the excel sheet, we will transpose this data frame.
                                                      #That way we get first-col = StateNames & second-col = Confirmed Cases.


df_CC.transpose().to_excel(writer, sheet_name='ConfirmedCases', index_label=True)

df_AC = pd.DataFrame( dict_AC, index=[today] )
df_AC.transpose().to_excel(writer, sheet_name='ActiveCases', index_label=True)

df_DC = pd.DataFrame( dict_DC, index=[today] )
df_DC.transpose().to_excel( writer, sheet_name='DeathCases', index_label=True )

writer.save()
