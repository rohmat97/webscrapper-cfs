  
import requests
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def getListMenu(driver):
    list_id = []
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'treeview-1012-body'))
        )
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        table = soup.find('tbody', {By.ID: 'treeview-1012-body'})
        all_tr= table.find_all('tr')
        # all_td = all_tr.find('td')
        print(len(all_tr))
        # for row in table.find_all('tr'):
        #     for cell in row.find_all('td'):

        #         li_count = len(li_elements)
        #         list_id.append(cell_id)
        return len(all_tr)
    except Exception as e:
        print(f"An error occurred: {e}")
        
   
