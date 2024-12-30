""""
main.py
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from locators import TestLocators
from data import WebData
from excel_functions import Sujatha_Excel_Functions

excel_file = WebData().EXCEL_FILE
sheet_number = WebData().SHEET_NUMBER

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

driver.maximize_window()
driver.get(WebData().URL)

# WebDriverWait for Explicit Wait
wait = WebDriverWait(driver, 10)  # Timeout of 10 seconds


# Read the row count from the Excel file
rows = Sujatha_Excel_Functions(excel_file, sheet_number).row_count()

# Read the row count from the Excel file
rows = 19  # Set the number of rows to 19

for row in range(2, rows + 1):
    username = Sujatha_Excel_Functions(excel_file, sheet_number).read_data(row, 6)
    password = Sujatha_Excel_Functions(excel_file, sheet_number).read_data(row, 7)

    # Wait for email field to be clickable, then enter the username
    emailLocator_field = wait.until(EC.element_to_be_clickable((By.XPATH, TestLocators().emailLocator)))
    emailLocator_field.send_keys(emailLocator)

    # Wait for password field to be clickable, then enter the password
    password_field = wait.until(EC.element_to_be_clickable((By.ID, TestLocators().passwordLocator)))
    password_field.send_keys(password)

    # Wait for LOGIN button to be clickable, then click the button
    login_Button_Locator = wait.until(EC.element_to_be_clickable((By.XPATH, TestLocators().login_Button_Locator)))
    login_Button_Locator.click()

    #wait for search keyword button to be clickable
    search_keyword = wait.until(EC.element_to_be_clickable((By.ID, TestLocators().search_keyword)))
    search_keyword.click()

    # Wait for the page to load and check if login is successful
    try:
        # Wait for the dashboard URL to appear after login (success condition)
        wait.until(EC.url_contains(WebData().DASHBOARD_URL))
        print(f"SUCCESS : Login success with loginbutton = {'submit'} and PASSWORD = {password}")

        Sujatha_Excel_Functions(excel_file, sheet_number).write_data(row, 8, "TEST PASS")

        # Perform logout after successful login
        logout_button = wait.until(EC.element_to_be_clickable((By.XPATH, TestLocators().logoutButton)))
        action = ActionChains(driver)
        action.click(on_element=logout_button)
        action.perform()

        # Wait for the logout link and click it
        logout_link = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Logout")))
        logout_link.click()

    except Exception as e:
        print(f"FAIL : Login failed with USERNAME = {username} and PASSWORD = {password}")
        Sujatha_Excel_Functions(excel_file, sheet_number).write_data(row, 8, "TEST FAIL")


#quit the program
driver.quit()