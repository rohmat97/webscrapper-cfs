import time
from selenium import webdriver

# Replace 'path/to/geckodriver' with the actual path to your GeckoDriver executable
executable_path = './geckodriver'

# Set GeckoDriver executable path using executable_path parameter in options
options = webdriver.FirefoxOptions()
options.add_argument(f"marionette;executable_path={executable_path}")

# Open Firefox WebDriver with specified options
driver = webdriver.Firefox(options=options)

# Open the webpage
driver.get('https://google.com/')

time.sleep(2)

driver.quit()
