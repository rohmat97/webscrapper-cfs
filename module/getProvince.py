  


from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def getListProvincePeriod(driver):
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'ProvinceCode-inputCell'))
        )
        try:
            dropdownProvince = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH,"//table[@id='ProvinceCode-triggerWrap']//div[@class='x-trigger-index-0 x-form-trigger x-form-arrow-trigger x-form-trigger-first']"))
            )
            dropdownProvince.click()
            page_source = driver.page_source
            soup = BeautifulSoup(page_source, 'html.parser')
            names = [li.text for li in soup.select('ul.x-list-plain li.x-boundlist-item')]
            names_after_removal = names[4:]
            # dropdown1 = WebDriverWait(driver, 10).until(
            #     EC.element_to_be_clickable((By.ID, 'ext-gen1065'))
            # )
            # dropdown1.click()            
            # option_xpath = '//*[@id="boundlist-1018-listEl"]/ul/li[1]'
            # button = WebDriverWait(driver, 10).until(
            #     EC.element_to_be_clickable((By.XPATH, option_xpath))
            # )
            # button.click()
          
        finally:
            return names_after_removal
    except Exception as e:
        print(f"An error occurred: {e}")
        
   
