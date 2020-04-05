#!/usr/bin/env python
# coding: utf-8

#################################################################################################
#                                                                                               #
#   Routine for scraping Iredell County's dashboard to construct a covid19 time series          #
#   by municipalities                                                                           #
#                                                                                               #                                                                     #
# Author:  Michael J. P. Morse                                                                  #
# License: file 'LICENSE.txt'                                                                   #
# Date: 04/04/2020                                                                              #
#                                                                                               #
#################################################################################################


import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
from selenium import webdriver
#from webdriver_manager.chrome import ChromeDriverManager
#from datetime import date
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options





# In[ ]:


# Load the Iredell dashboard and embededd map
my_url_map = 'https://iredell.maps.arcgis.com/apps/Embed/index.html?webmap=cd6e8cd90b014a4aa9a624079d15dc71&extent=-81.4946,35.4204,-79.8769,36.1024&zoom=true&previewImage=false&scale=true&disable_scroll=true&theme=light'
my_url='https://nc-iredellcounty.civicplus.com/1392/Iredell-County-COVID-19-Data'


# In[ ]:
options = Options()
options.headless = True
driver = webdriver.Chrome(options=options)

#options = webdriver.ChromeOptions()
#options.add_argument('headless')
#driver = webdriver.Chrome(ChromeDriverManager().install(),options=options)

#driver.implicitly_wait(20) # seconds

driver.get(my_url_map)

#extract the text overlay from map with covid cases in South - Central - North

wait = WebDriverWait(driver, 10)
p_element_map = wait.until(EC.presence_of_element_located((By.ID, 'labels_layer')))


cases = p_element_map.text.split("\n")


#extract date of last update
driver.get(my_url)
p_element_date = driver.find_elements_by_css_selector('h3.subhead2')


# In[ ]:


date = p_element_date[1].text.split(' ')[2]

# quit the webdriver
driver.quit()

last_update = datetime.strptime(date, "%m/%d/%y")
last_update = datetime.strftime(last_update,'%m/%d')


# In[ ]:


# Make a dictonary out of the elements
todays_cases = {}
todays_cases['South'] = cases[0]
todays_cases['Central'] = cases[1]
todays_cases['North'] = cases[2]

# make a dateframe out of todays cases
df_today = pd.DataFrame(todays_cases.values(),index=todays_cases.keys())
df_today.rename(columns={0:last_update},inplace=True)


# In[ ]:


## Load the time series
df_time_series = pd.read_csv('iredell_time_series.csv',index_col=0)
## Add todays cases to the dataframe
df_time_series[last_update] = df_today[last_update]
## Save the new data
df_time_series.to_csv(r'iredell_time_series.csv', index = True)
