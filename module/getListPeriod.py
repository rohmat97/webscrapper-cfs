
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def getListPeriod(driver):
    period = 0
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'Month-triggerWrap'))
        )
        try:
            button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID,"ext-gen1050"))
            )
            button.click()
            page_source = driver.page_source
            soup = BeautifulSoup(page_source, 'html.parser')
            div_element = soup.find('div', class_='x-boundlist')
            li_elements = div_element.find_all('li')
            li_count = len(li_elements)
            period = li_count
            
        finally:
            return period
    except Exception as e:
        print(f"An error occurred: {e}")
        
   
