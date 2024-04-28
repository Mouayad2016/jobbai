import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException, ElementNotSelectableException
import subprocess
import time
from bs4 import BeautifulSoup

def find_element(driver, key):
    """
    Attempts to find an element first by ID, then by name if the ID fails.

    Args:
    driver: The Selenium WebDriver instance.
    key: The identifier used to find the element (ID or name).

    Returns:
    The WebElement if found, None otherwise.
    """
    try:
        # Try finding by ID
        element = driver.find_element(By.ID, key)
        return element
    except NoSuchElementException:
        # If not found by ID, try finding by name
        try:
            element = driver.find_element(By.NAME, key)
            print(key)
            return element
        except NoSuchElementException:
            return None
        
        
def try_select_option(element, value):
    """
    Attempts to select an option from a dropdown by visible text, and by value if the first fails.

    Args:
    element: The <select> WebElement.
    value: The visible text or value of the option to select.

    Returns:
    None
    """
    select = Select(element)
    try:
        select.select_by_visible_text(value)
    except NoSuchElementException:
        try:
            select.select_by_value(value)
        except NoSuchElementException:
            print(f"Option {value} not found in select element.")


def handle_button(driver, element):
    if element.get_attribute('type') != "submmit":
        element.click()
        time.sleep(1)
        script_path = '/Users/mouayadmouayad/Desktop/jobbAI/automation/auto.scpt'
        try:
            result = subprocess.run(['osascript', script_path], check=True, text=True, capture_output=True)
            print("Script output:", result.stdout)
        except subprocess.CalledProcessError as e:
            print("Error running script:", e)
            
def find_file_inputs(html_content):

    soup = BeautifulSoup(html_content, 'html.parser')
    # Find all form tags to scope the search specifically to forms (optional)
    forms = soup.find_all('form')
    if not forms:
        print("No forms found in the HTML content.")
        return False

    file_inputs_found = False
    for form in forms:
        # Find all input elements with type 'file' within each form
        file_inputs = form.find_all('input', {'type': 'file'})
        if file_inputs:
            file_inputs_found = True
            print(f"Found {len(file_inputs)} input(s) with type 'file' in a form.")
            return True
    if not file_inputs_found:
        print("No input with type 'file' found in any form.")
        return False
    

  # # element.click()
                # script = """ultimateFileUpload(cv_and_pl_update, false, 'prof_cvdocument', 'doc|docx|rtf|pdf|jpg|gif');"""   
                # driver.execute_script(script)
                # time.sleep(4)
                # script_path = '/Users/mouayadmouayad/Desktop/jobbAI/automation/auto.scpt'
                # try:
                #     result = subprocess.run(['osascript', script_path], check=True, text=True, capture_output=True)
                #     print("Script output:", result.stdout)
                # except subprocess.CalledProcessError as e:
                #     print("Error running script:", e)

from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC

def wait_for_text_in_body(driver, text, timeout=30):
    """
    Wait until the specified text appears anywhere in the body of the webpage.

    Args:
        driver (webdriver): The WebDriver instance for Selenium.
        text (str): The text to wait for.
        timeout (int): How long to wait for the text to appear, in seconds.
    """
    try:
        # Use WebDriverWait to wait until the text appears in the body element
        WebDriverWait(driver, timeout).until(
            EC.text_to_be_present_in_element((By.TAG_NAME, "body"), text)
        )
        print(f"Text '{text}' has been successfully found in the body.")
    except TimeoutException:
        print(f"Failed to find the text '{text}' in the body within {timeout} seconds.")
  
import os
from selenium.webdriver.common.action_chains import ActionChains

def calculate_offset(slider_element, desired_value, min_value, max_value):
    """
    Calculate pixel offset to drag the slider handle based on the desired value.

    Args:
    slider_element: The WebElement of the slider track.
    desired_value: The target value to set on the slider.
    min_value: The minimum value of the slider.
    max_value: The maximum value of the slider.

    Returns:
    The pixel offset to move the slider handle.
    """
    desired_value = int(desired_value)  # Convert desired_value to an integer
    length = slider_element.size['width']  # Get the width of the slider element
    scale = (desired_value - min_value) / (max_value - min_value)
    return int(scale * length)

def generate_attribute_modification_script(element_id, new_value):
    """
    Generate a JavaScript snippet to update attributes containing the word 'value'
    by modifying only the numeric part and preserving any trailing text like 'år'.

    Args:
        element_id: The ID of the HTML element.
        new_value: The new numeric value to set.

    Returns:
        A JavaScript string that can be executed to perform the update.
    """
    script = f"""
    var element = document.getElementById('{element_id}');
    Array.from(element.attributes).forEach(attr => {{
        if (attr.name.includes('value') && attr.value.includes('år')) {{
            var numericPart = attr.value.match(/\\d+/); // Matches the numeric part of the value
            if (numericPart) {{
                element.setAttribute(attr.name, '{new_value} ' + attr.value.replace(numericPart[0], '').trim());
            }}
        }}
    }});
    """
    return script


def simulate_slider_drag(driver, element, value):
    """
    Attempt to interact with a slider, whether it's a standard HTML input or a custom-styled component.

    Args:
        driver: The Selenium WebDriver instance.
        slider_element_id: The ID of the slider element or its container.
    """
    try:
        
        slider_element_id =  element.get_attribute('id')
        generate_attribute_modification_script(slider_element_id, value)
        # Try to locate the standard input range slider
        slider_input = driver.find_element(By.ID,  slider_element_id)
        min_value = int(slider_input.get_attribute('min'))
        max_value = int(slider_input.get_attribute('max'))
        desired_value = (min_value + max_value) // 2  # Example: Set to midpoint for demonstration

        # Check if the slider is visible and interactable directly
        if slider_input.is_displayed() and slider_input.tag_name == "input" and slider_input.get_attribute("type") == "range":
            print("First IFFF")
            track_width = slider_input.size['width']
            move_distance = ((desired_value - min_value) / (max_value - min_value)) * track_width
            ActionChains(driver) \
                .click_and_hold(slider_input) \
                .move_by_offset(move_distance - (track_width / 2), 0) \
                .release() \
                .perform()
        else:
            print("Secound Else")

            # If not directly interactable, attempt to interact with custom components
            handle = driver.find_element(By.CSS_SELECTOR, f"#{slider_element_id} .rangeslider__handle")
            track = driver.find_element(By.CSS_SELECTOR, f"#{slider_element_id} .rangeslider__fill__bg")
            track_width = track.size['width']
            move_distance = ((desired_value - min_value) / (max_value - min_value)) * track_width
            ActionChains(driver) \
                .click_and_hold(handle) \
                .move_by_offset(move_distance - handle.size['width'] / 2, 0) \
                .release() \
                .perform()
    except NoSuchElementException:
        # If element structures are not found, fallback to JavaScript to force the value change
        driver.execute_script(f"document.getElementById('{slider_element_id}').value = {desired_value};")
        driver.execute_script(f"document.getElementById('{slider_element_id}').dispatchEvent(new Event('input'));")
        driver.execute_script(f"document.getElementById('{slider_element_id}').dispatchEvent(new Event('change'));")







def handle_cookie_popups(driver, timeout=10):
    """
    Attempts to close cookie consent popups by clicking on common consent buttons and specific buttons based on provided page structures.

    Args:
        driver (webdriver): The WebDriver instance for Selenium.
        timeout (int): How long to wait for the cookie button to appear, in seconds.
    """
    # Expanded list of selectors to include specific data-action attributes
    consent_button_selectors = [
        "button[aria-label='Accept cookies']",       # Common for aria-labels
        "button[data-accept='all']",                # Data attributes for accepting
        "button.cookie-consent__accept",            # Class-based selectors
        "div#cookie-consent button.accept",         # Specific ID and button combo
        "button#accept-cookies",                    # Specific ID for buttons
        "button.accept",                            # Generic class names
        "button.consent",                           # Another common class name
        ".cookiebanner .accept",                    # Common structure in class-based layouts
        "[data-action='click->common--cookies--alert#acceptAll']",  # Specific data-action for accepting all cookies
        "[data-action='click->common--cookies--alert#disableAll']", # Specific data-action for disabling non-necessary cookies
        "[data-action='click->common--cookies--alert#openPreferences']"  # Preferences button
    ]
    
    for selector in consent_button_selectors:
        try:
            # Wait for the cookie consent button to be clickable
            cookie_button = WebDriverWait(driver, timeout).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
            )
            cookie_button.click()
            print(f"Clicked cookie consent button with selector: {selector}")
            return True  # Return True if a button was successfully clicked
        except TimeoutException:
            print(f"No clickable cookie button found with selector: {selector}")
        except NoSuchElementException:
            print(f"No element found with selector: {selector}")

    print("No cookie consent buttons were found or clickable.")
    return False  # Return False if no button was clicked

def click_cookie_accept_buttons(driver, timeout=10):
    """
    Searches through the webpage and attempts to click any button that could be related to accepting cookies.

    Args:
        driver (webdriver): The WebDriver instance for Selenium.
        timeout (int): How long to wait for elements to become visible and interactable, in seconds.
    """
    # Define common phrases that are likely to be found on cookie acceptance buttons
    accept_phrases = [
        'Accept', 'Agree', 'Consent', 'OK', 'Yes', 'Continue',  # English
        'Acceptera', 'Godkänn', 'Samtycke', 'Ja', 'Fortsätt',  'Godkänn alla'  # Swedish
    ]
    try:
        # Wait for the page to load and any cookie buttons to become visible
        WebDriverWait(driver, timeout).until(
            EC.visibility_of_any_elements_located((By.TAG_NAME, "button"))
        )

        # Get all buttons on the page
        buttons = driver.find_elements(By.TAG_NAME, "button")
        print(f"Found {len(buttons)} buttons on the page.")

        # Attempt to click buttons based on common accept phrases
        clicked = False
        for button in buttons:
            if any(phrase in button.text for phrase in accept_phrases):
                if button.is_displayed() and button.is_enabled():
                    button.click()
                    print(f"Clicked button with text: {button.text}")
                    clicked = True
                    break  # Stop after the first successful click to avoid multiple acceptances

        if not clicked:
            print("No suitable cookie acceptance button was clicked.")
    except TimeoutException:
        print("Timeout: No buttons became visible or interactable within the given time.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        
        
        
def click_elements_by_selectors(driver, selectors):
    for selector in selectors:
        try:
            # Find the element using CSS selector
            element = driver.find_element(By.CSS_SELECTOR, selector)
            # Perform action, e.g., clicking the element
            element.click()
        except Exception as e:
            print(f"Failed to interact with element using selector {selector}: {str(e)}")
            
            
def set_false_attributes_to_true(driver):
    """
    This function takes a Selenium WebDriver object and sets all attributes with a value of 'false' to 'true'
    within forms and their child elements in the document body.

    Args:
    driver: The Selenium WebDriver instance.
    """
    script = """
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        const traverseAndModifyAttributes = (element) => {
            Array.from(element.attributes).forEach(attr => {
                if (attr.value === "false") {
                    element.setAttribute(attr.name, "true");
                }
            });
            Array.from(element.children).forEach(child => traverseAndModifyAttributes(child));
        };
        traverseAndModifyAttributes(form);
    });
    """
    driver.execute_script(script)



def fill_form(driver, data):
    """
    Fills out a web form based on provided data including uploading files and handling hidden inputs.

    Args:
    driver: The Selenium WebDriver instance.
    data: A dictionary where keys are HTML tag IDs or names, and values are the values to enter or select.

    Returns:
    None
    """
    set_false_attributes_to_true(driver)
    
    for key, value in data.items():
        element = find_element(driver, key)
        if element:
            if element.tag_name == 'button':
                pass
                # handle_button(driver, element)
                                
            if element.tag_name == 'input':
                input_type = element.get_attribute('type')
                if input_type in ['checkbox', 'radio']:
                    try:
                        # Attempt to click the actual checkbox
                        if not element.is_selected():
                            element.click()
                    except Exception as e:
                        # Fallback to clicking the label or the styled element
                        try:
                            label = driver.find_element(By.CSS_SELECTOR, f"label[for='{key}']")
                            label.click()
                        except Exception as e:
                            print(f"Could not interact with the checkbox or its label {key}: {str(e)}")
                            
                elif input_type == 'file':
                    if not (element.is_displayed() and element.is_enabled()):

                        driver.execute_script("arguments[0].style.opacity = 1; arguments[0].style.display = 'block';", element)
                        element.send_keys(value)
                        wait_for_text_in_body(driver, os.path.basename(value))
                elif input_type == 'range':
                  
                    simulate_slider_drag(driver, element, value)
                else:
                    if element.is_enabled() and element.is_displayed():
                        try:
                            element.clear()
                            element.send_keys(value)
                        except Exception as e:
                            print(f"Could not interact with {key}: {str(e)}")
            elif element.tag_name == 'select':
                if element.is_displayed():
                    try_select_option(element, value)
            elif element.tag_name == 'textarea':
                if element.is_displayed():
                    try:
                        element.clear()
                        element.send_keys(value)
                    except Exception as e:
                        print(f"Could not interact with {key}: {str(e)}")
        else:
            print(f"Element with ID or name {key} not found.")