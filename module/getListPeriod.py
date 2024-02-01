
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def getListPeriod(driver):
    period = []
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'Month-triggerWrap'))
        )
        try:
            button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID,"ext-gen1050"))
            )
            button.click()
            # soup = BeautifulSoup(page_source, 'html.parser')
            # div_element = soup.find('div', class_='x-boundlist')

            boundlist = driver.find_element(By.CLASS_NAME, "x-boundlist-list-ct")
            list_items = boundlist.find_elements(By.CLASS_NAME, "x-boundlist-item")
            # Extract and print the text content of each <li> element
            for item in list_items:
                period.append(item.text)
            
        finally:
            return period
    except Exception as e:
        print(f"An error occurred: {e}")
        
   
