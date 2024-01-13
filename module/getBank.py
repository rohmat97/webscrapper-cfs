  


import time
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def getBank(driver):
    list_id= []
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'BankCode-inputEl'))
        )
        try:
            time.sleep(1)
            dropdownBank = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, 'BankCode-inputEl'))
            )
            dropdownBank.click()
            page_source = driver.page_source
            soup = BeautifulSoup(page_source, 'html.parser')
            table = soup.find('tbody', {By.ID: 'treeview-1022-body'})
            for row in table.find_all('tr'):
                for cell in row.find_all('td'):
                    name_element = cell.find('span', class_='x-tree-node-text')
                    list_id.append(name_element.text)
        finally:
            dropdownBank.click()
            return list_id
    except Exception as e:
        print(f"An error occurred: {e}")
        
   
