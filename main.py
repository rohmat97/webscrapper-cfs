# main.py
import os
import time
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from weasyprint import HTML
from module.getBank import getBank
from module.getKota import getKota
import pandas as pd

from module.getListOption import getListMenu
from module.getListPeriod import getListPeriod
from module.getProvince import getListProvincePeriod
from module.renameFile import copy_and_rename_xlsx

# Replace 'path/to/geckodriver' with the actual path to your GeckoDriver executable
executable_path = './geckodriver'

# Set GeckoDriver executable path using executable_path parameter in options
options = webdriver.FirefoxOptions()
options.add_argument(f"marionette;executable_path={executable_path}")

# Open Firefox WebDriver with specified options
driver = webdriver.Firefox(options=options)
# Open the webpage
driver.get('https://cfs.ojk.go.id/cfs/Report.aspx?BankTypeCode=BPK&BankTypeName=BPR%20Konvensional')

period_year = ["2023"]
periods_month = getListPeriod(driver)
provincePeriod = getListProvincePeriod(driver)
len_menu = getListMenu(driver)
for iy in period_year:
    # Wait for the checkbox element to be clickable
    driver.get('https://cfs.ojk.go.id/cfs/Report.aspx?BankTypeCode=BPK&BankTypeName=BPR%20Konvensional')
    input_element_year = driver.find_element("id", "Year-inputEl")
    input_element_year.clear()
    # Type the new value into the input field
    input_element_year.send_keys(iy)  # Change this to the desired value
    
    # check all option
    for i in range(len_menu):
        try:
            checkbox_xpath = "//tr["+str(i+1)+"]//input[@class=' x-tree-checkbox']"
            checkbox = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, checkbox_xpath))
            )
            checkbox.click()
        except: print('something problem checkbox')
    for im in periods_month:
        input_element_month = driver.find_element("id", "Month-inputEl")
        input_element_month.clear()
        # Type the new value into the input field
        input_element_month.send_keys(im)  # Change this to the desired value
        time.sleep(2)
        
    
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
                        EC.element_to_be_clickable((By.ID, 'ext-gen1069'))
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
                    time.sleep(10)
                    
                    # Locate the div with ID 'ReportViewerArea'
                    report_viewer_div = driver.find_element(By.ID, 'ReportViewerArea')

                    # Find all iframes within the div
                    iframes_within_div = report_viewer_div.find_elements(By.TAG_NAME, 'iframe')

                    # Get the count of iframes
                    iframe_count = len(iframes_within_div)
                    if iframe_count:
                        for ic in range(iframe_count):
                            
                            # Locate the iframe using its ID, name, or any other applicable method
                            iframe_element = driver.find_element(By.ID, f'BPK-901-00000{ic+1}')

                            # Get the src attribute of the iframe
                            iframe_src = iframe_element.get_attribute("src")

                            # Print or use the iframe src as needed
                            print(f"Iframe src: {iframe_src}")
                            # Process the content of the iframe using BeautifulSoup
                            response = requests.get(iframe_src)
                             # Parse the HTML content of the page
                            soup = BeautifulSoup(response.text, 'html.parser')

                            # Find the table within the HTML content
                            table = soup.find('table', {'id': 'CFSReportViewer_fixedTable'})
                            selected_rows = table.select('tr')
                            
                            for index, row in enumerate(selected_rows, 1):
                                if index in (28, 50):
                                    # print(f"{index}. {row}")
                                    if index == 28:
                                        # Find the span element with the specified class
                                        span_element = row.find('span', class_='A035263adf76445558c7cad71aae10adf15')

                                        # Extract the value
                                        if span_element:
                                            value = span_element.text.strip()
                                            print(f"Value: {value}")
                                        else:
                                            print("Value not found in the HTML.")
                                        
                                    with open(f'./html/table{index}.html', 'w', encoding='utf-8') as file:
                                        file.write(str(row))
                                    HTML(string=str(row)).write_pdf(f'./pdf/output{index}.pdf', margin_top='10mm', margin_bottom='10mm', margin_left='10mm', margin_right='10mm')
                            # Save HTML to a file
                            # with open('table.html', 'w', encoding='utf-8') as file:
                            #     file.write(str(table))

                            # # Convert HTML to PDF
                            # pdfkit.from_file('table.html', 'output.pdf')
                            # selected_rows = soup.select('table tr')
                            # # Check if the table element is found
                            # if selected_rows:
                            #     # Process the table content as needed
                            #     index = 1
                            #     for iTab in selected_rows:
                            #         print("table index", str(index) + ".   " + iTab.get_text())
                            #         index += 1
                            #     # Add your further processing logic here
                            # else:
                            #     print("Table not found.")
                            print("thanks ++++++++++++++++++++++++++++++++")
                            driver.quit()
                            
                            # try:
                            #     iframe_id = f'BPK-901-00000'+ str(ic+1)
                            #     driver.switch_to.frame(iframe_id)
                            #     # try to download
                            #     time.sleep(5)
                            #     try:
                            #         WebDriverWait(driver, 10).until(
                            #             EC.element_to_be_clickable((By.XPATH, "//table[@id='CFSReportViewer_fixedTable']//img[1]"))
                            #         ).click()
                            #         wait = WebDriverWait(driver, 20)  # Adjust the timeout as needed

                            #         button = wait.until(EC.element_to_be_clickable((By.ID, 'CFSReportViewer_ctl05_ctl04_ctl00_ButtonImgDown')))
                            #         button.click()
                                    
                            #         button = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[.='PDF']")))
                            #         button.click()
                            #         time.sleep(10)
                                    
                            #         source_file = '/Users/rohmatdasuki/Downloads/CFS1LevelGroupingWithOutNumber_2020.pdf'
                            #         destination_folder = './file'
                            #         new_filename = f"{bank}.pdf"
                            #         copy_and_rename_xlsx(source_file, destination_folder, new_filename)
                            #         handles = driver.window_handles
                            #         for handle in handles[1:]:
                            #             driver.switch_to.window(handle)
                            #             driver.close()
                            #         driver.switch_to.window(handle[0])
                            #         driver.switch_to.default_content()
                            #         # convert_iframe_to_pdf(driver.page_source, "./output.pdf")
                            #     except Exception as e:
                            #         print(f"An error occurred: {e}")
                                   
                            # except:
                            #     # Handle the case when the iframe is not found
                            #     print(f"Could not find iframe with ID: {iframe_id}")
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
