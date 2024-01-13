  


from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def getKota(driver):
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'ProvinceCode-inputCell'))
        )
        try:
            dropdownKota = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "ext-gen1064"))
            )
            dropdownKota.click()
            page_source = driver.page_source
            soup = BeautifulSoup(page_source, 'html.parser')
            li_elements = soup.select('#boundlist-1019-listEl ul.x-list-plain li.x-boundlist-item')
            names = [li.text for li in li_elements]
            dropdownKota.click()
            # li_elements = div_element.find_all('li')
            # li_count = len(li_elements)
            # period = li_count
          
        finally:
            return names
    except Exception as e:
        print(f"An error occurred: {e}")
        
   
