# main.py
from asyncio import wait
import json
import shutil
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from module.convert_iframe_to_pdf import convert_iframe_to_pdf
from module.getBank import getBank
from module.getKota import getKota

from module.getListOption import getListMenu
from module.getListPeriod import getListPeriod
from module.getProvince import getListProvincePeriod

# Replace 'path/to/geckodriver' with the actual path to your GeckoDriver executable
gecko_path = './geckodriver'

# Set GeckoDriver executable path using executable_path argument in options
options = webdriver.FirefoxOptions()
options.binary_location = '/Applications/Firefox.app/Contents/MacOS/firefox-bin'  # Update with your Firefox binary location
options.add_argument(f"marionette;executable_path={gecko_path}")

# Open Firefox WebDriver with specified options
driver = webdriver.Firefox(options=options)
# Open the webpage
driver.get('https://cfs.ojk.go.id/cfs/Report.aspx?BankTypeCode=BPK&BankTypeName=BPR%20Konvensional')

periods = getListPeriod(driver)
len_menu = getListMenu(driver)
provincePeriod = getListProvincePeriod(driver)
for i in range(len_menu):
    # Wait for the checkbox element to be clickable
    driver.get('https://cfs.ojk.go.id/cfs/Report.aspx?BankTypeCode=BPK&BankTypeName=BPR%20Konvensional')
    button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID,"ext-gen1050"))
            )
    button.click()
    checkbox_xpath = "//tr["+str(i+1)+"]//input[@class=' x-tree-checkbox']"
    checkbox = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, checkbox_xpath))
    )
    checkbox.click()
    # set province
    for province in provincePeriod:
        dropdownProvince = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH,"//table[@id='ProvinceCode-triggerWrap']//div[@class='x-trigger-index-0 x-form-trigger x-form-arrow-trigger x-form-trigger-first']"))
        )
        dropdownProvince.click()
        option_xpath = f'//li[.="{province}"]'
        buttonChooseProvince = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, option_xpath))
        )
        buttonChooseProvince.click()
        # set city 
        cityPeriod = getKota(driver)
        for city in cityPeriod: 
            dropdownKota = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "ext-gen1064"))
            )
            dropdownKota.click()
            
            option_xpath = f"//li[.='{city}']"

            button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, option_xpath))
            )
            button.click()
            # set bank 
            list_bank = getBank(driver)
            for bank in list_bank: 
                dropdownBank = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.ID, 'BankCode-inputEl'))
                )
                dropdownBank.click()
                
                option_xpath = f"//div[.='{bank}']"
                
                button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, option_xpath))
                )
                button.click()
                # submit action
                WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.ID, 'ShowReportButton-btnWrap'))
                        )
                button = WebDriverWait(driver, 10).until(
                            EC.element_to_be_clickable((By.ID, 'ShowReportButton-btnWrap'))
                        )
                button.click()

                iframe_id = 'BPK-901-00000'+ str(i+1)
                driver.switch_to.frame(iframe_id)
                
                # try to download
                time.sleep(5)
                try:
                    driver.find_element(By.XPATH, '//table[@id="CFSReportViewer_ctl05_ctl04_ctl00_Button"]//img[1]')
                    WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, '//table[@id="CFSReportViewer_ctl05_ctl04_ctl00_Button"]//img[1]'))
                    ).click()
                    wait = WebDriverWait(driver, 20)  # Adjust the timeout as needed

                    button = wait.until(EC.element_to_be_clickable((By.ID, 'CFSReportViewer_ctl05_ctl04_ctl00_ButtonImgDown')))
                    button.click()
                    
                    button = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[.='PDF']")))
                    button.click()
                    time.sleep(10)
                    # convert_iframe_to_pdf(driver.page_source, "./output.pdf")
                except Exception as e:
                    print(f"An error occurred: {e}")
                finally:
                    driver.switch_to.window(driver.window_handles[0])
    
# provincePeriod = getListProvincePeriod(driver)
# kotaPeriod = getKota(driver)
# list_bank = getBank(driver)
# for menu in list_menu:
#     WebDriverWait(driver, 10).until(
#             EC.element_to_be_clickable((By.XPATH,'//table[@class="x-treeview-1012-table x-grid-table"]//tr[1]//input[@class=" x-tree-checkbox"]'))
#         ).click()
#     print(menu)
    
    
time.sleep(2)
driver.quit()
# WebDriverWait(driver, 10).until(
#             EC.presence_of_element_located((By.ID, 'ShowReportButton-btnWrap'))
#         )
# button = WebDriverWait(driver, 10).until(
#             EC.element_to_be_clickable((By.ID, 'ShowReportButton-btnWrap'))
#         )
# button.click()

# iframe_id = 'BPK-901-000001'
# driver.switch_to.frame(iframe_id)


# time.sleep(5)
# try:
#     WebDriverWait(driver, 10).until(
#         EC.element_to_be_clickable((By.XPATH, '//table[@id="CFSReportViewer_ctl05_ctl04_ctl00_Button"]//img[1]'))
#     ).click()
#     wait = WebDriverWait(driver, 20)  # Adjust the timeout as needed

#     button = wait.until(EC.element_to_be_clickable((By.ID, 'CFSReportViewer_ctl05_ctl04_ctl00_ButtonImgDown')))
#     button.click()
    
#     button = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[.='PDF']")))
#     button.click()
#     time.sleep(10)
#     # convert_iframe_to_pdf(driver.page_source, "./output.pdf")
#     print('finish')
# except Exception as e:
#     print(f"An error occurred: {e}")
