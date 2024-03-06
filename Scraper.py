import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.common.exceptions import TimeoutException
import datetime

def get_offline_devices():
    print(f"{datetime.datetime.now()} - Starting get_offline_devices...")
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    browser = webdriver.Chrome(options=options)
    print(f"{datetime.datetime.now()} - Browser opened.")

    browser.get('https://unifi.ui.com/dashboard')
    print(f"{datetime.datetime.now()} - Navigated to dashboard.")

    # Wait for the email and password
    wait = WebDriverWait(browser, 3)
    email_label = wait.until(EC.presence_of_element_located((By.NAME, "username")))
    email_field = browser.find_element(By.NAME, "username")
    password_label = wait.until(EC.presence_of_element_located((By.NAME, "password")))
    password_field = browser.find_element(By.NAME, "password")

    time.sleep(3)
    email_field.send_keys('UNIFI PORTAL USERNAME')
    password_field.send_keys('PASSWORD')

    wait = WebDriverWait(browser, 10)  # Increase the timeout here
    signin_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'button__DHfWZixG'))) #this might need to be updated

    signin_button.click()
    time.sleep(10)

    # ...
    offline_device_labels = []

    try:
        offline_elems = browser.find_elements(By.XPATH,
                                              '//a[@data-variant="console" and not(contains(@class, "success__aKo0oiiz"))]')
        for elem in offline_elems:
            try:
                link_elem = elem.find_element(By.CSS_SELECTOR, 'a[href]')
                href = link_elem.get_attribute('href')

                # Check if the href matches the excluded URL
                if href == #'You can list old HREF's here to exlcude:
                    continue  # Skip this link

                label_elem = elem.find_element(By.CSS_SELECTOR, 'span[data-label]')
                label = label_elem.get_attribute('data-label')
                offline_device_labels.append(label)
            except NoSuchElementException:
                print("Could not find label element for offline element")
    except NoSuchElementException:
        pass
    # ...

    browser.quit()
    print(f"{datetime.datetime.now()} - Browser closed.")
    return offline_device_labels

def login_to_teams():
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(options=options)

    driver.get('https://teams.microsoft.com/')

    wait = WebDriverWait(driver, 5)  # Wait for a maximum of 5 seconds

    # Sign in
    print("Waiting for email field...")
    email_field = wait.until(EC.presence_of_element_located((By.NAME, 'loginfmt')))
    print("Email field found.")
    time.sleep(7)
    email_field.send_keys(#'ENTER TEAMS EMAIL HERE')  # replace with your Teams email
    time.sleep(7)
    driver.find_element(By.ID, 'idSIButton9').click()
    time.sleep(7)
    wait = WebDriverWait(driver, 5)

    # Wait for password field to load
    print("Waiting for password field...")
    password_field = wait.until(EC.presence_of_element_located((By.NAME, 'passwd')))
    print("Password field found.")
    password_field.send_keys('ENTER PASSWORD HERE')  # replace with your Teams password
    time.sleep(7)

    # Click the sign-in button using JavaScript
    signin_button = wait.until(EC.element_to_be_clickable((By.ID, 'Whatever teams chat ID category you want')))
    time.sleep(7)
    driver.execute_script("arguments[0].click();", signin_button)
    wait = WebDriverWait(driver, 5)
    # Handle "Stay signed in" section
    try:
        stay_signed_in_checkbox = wait.until(EC.element_to_be_clickable((By.ID, 'KmsiCheckboxField')))
        stay_signed_in_checkbox.click()
        time.sleep(3)
        driver.find_element(By.ID, 'Whatever teams chat ID category you want').click()
    except TimeoutException:
        pass

    # Wait for chat to load
    time.sleep(20)

    return driver

def send_message_to_teams(message, driver):
    try:

        chat_category_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div[2]/div[1]/app-bar/nav/ul/li[2]/button'))
        )
        chat_category_button.click()
        time.sleep(2)

        try:
            # Type the message into the chat box
            chat_input_field = WebDriverWait(driver, 3)
            chat_input_field = driver.switch_to.active_element
            chat_input_field.send_keys(message)

            # Send the message by pressing Enter
            chat_input_field.send_keys(Keys.RETURN)

            time.sleep(2)

            print("Message sent to Microsoft Teams chat.")
        except Exception as e:
            print("Failed to send message to Microsoft Teams chat:", str(e))
        finally:
            # Switch back to the default content
            driver.switch_to.default_content()

    except Exception as e:
        print("Failed to locate chat category button:", str(e))

offline_device_labels_prev = set()
first_run = True  # Flag for the first run
# Flags for controlling the loop and status updates
first_run = True
status_update_sent = False

while True:
    time.sleep(0)
    now = time.localtime()

    if 6 <= now.tm_hour < 20:
        offline_device_labels = set(get_offline_devices())
        new_offline_devices = offline_device_labels - offline_device_labels_prev

        # 6 am status update
        if now.tm_hour == 6 and not status_update_sent:
            if offline_device_labels:
                message = f"6am status: Devices offline: {', '.join(offline_device_labels)}"
            else:
                message = "6am status: Hooray! All UNVR's are online."
            driver = login_to_teams()
            send_message_to_teams(message, driver)
            driver.quit()
            status_update_sent = True
        elif now.tm_hour != 6:
            status_update_sent = False

        # Checking for new offline devices
        if new_offline_devices:
            message = f"Offline devices: {', '.join(new_offline_devices)}"
            driver = login_to_teams()
            send_message_to_teams(message, driver)
            driver.quit()
        elif first_run and not offline_device_labels:
            message = "Hooray! All UNVR's and networks are online."
            driver = login_to_teams()
            send_message_to_teams(message, driver)
            driver.quit()
        elif not new_offline_devices and not offline_device_labels_prev and offline_device_labels:
            message = "All devices are back online."
            driver = login_to_teams()
            send_message_to_teams(message, driver)
            driver.quit()

        offline_device_labels_prev = offline_device_labels
        first_run = False

    time.sleep(600)  # Wait for 5 minutes
