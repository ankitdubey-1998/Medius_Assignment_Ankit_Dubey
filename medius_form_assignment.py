from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time, os


data = {
    "Full Name": "Ankit Dubey",
    "Contact Number": "7275665438",
    "Email ID": "ankdev1998@gmail.com",
    "Full Address": "Plot No. 1, Mangla Vihar 2, Trianga Chauraha, Kanpur",
    "Pin Code": "208021",
    "Date of Birth": "1998-01-05",  
    "Gender": "Male",
    "Type this code": "GNFPYC"
}


FORM_URL = "https://forms.gle/WT68aV5UnPajeoSc8"

# ---- STEP 3: ChromeDriver Path ----
service = Service("C:\\Users\\Amitd\\OneDrive\\Downloads\\selenium4\\chromedriver.exe")


options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--disable-extensions")
options.add_argument("--disable-infobars")

driver = webdriver.Chrome(service=service, options=options)

try:
   
    driver.get(FORM_URL)
    WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.TAG_NAME, "form")))
    print("Form opened successfully.")
    time.sleep(2)

    # ---- STEP 6: Field Finder ----
    def find_input(label_text):
        """Finds the input/textarea/date field near the given label."""
        try:
            container = driver.find_element(
                By.XPATH,
                f"//div[contains(@class,'Qr7Oae')][.//span[contains(normalize-space(text()),'{label_text}')]]"
            )
            for xpath in [".//input[@type='text']", ".//input[@type='date']", ".//textarea", ".//div[@role='textbox']"]:
                try:
                    return container.find_element(By.XPATH, xpath)
                except:
                    continue
            return None
        except Exception as e:
            print(f"Could not find label '{label_text}' → {e}")
            return None

    
    for label, value in data.items():
        element = find_input(label)
        if element:
            try:
                driver.execute_script("arguments[0].scrollIntoView(true);", element)
                time.sleep(0.5)

                if element.get_attribute("type") == "date":
                   
                    driver.execute_script("""
                        arguments[0].value = arguments[1];
                        arguments[0].dispatchEvent(new Event('input', { bubbles: true }));
                        arguments[0].dispatchEvent(new Event('change', { bubbles: true }));
                    """, element, value)
                else:
                    element.click()
                    element.send_keys(value)

                print(f"Filled: {label}")
                time.sleep(0.5)

            except Exception as e:
                print(f" Couldn't fill '{label}' → {e}")
        else:
            print(f" Skipped: {label}")

    
    try:
        submit_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//span[text()='Submit']/ancestor::div[@role='button']"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", submit_button)
        time.sleep(1)
        submit_button.click()
        print("Form submitted successfully!")

    except Exception as e:
        print(f"Could not find or click Submit → {e}")
        driver.switch_to.active_element.send_keys(Keys.ENTER)

    
    time.sleep(4)
    os.makedirs("output", exist_ok=True)
    screenshot_path = os.path.join("output", "confirmation.png")
    driver.save_screenshot(screenshot_path)
    print(f"Screenshot saved at: {screenshot_path}")

except Exception as e:
    print(f"Unexpected Error: {e}")

finally:
    time.sleep(2)
    driver.quit()
    print("Process completed and browser closed.")
