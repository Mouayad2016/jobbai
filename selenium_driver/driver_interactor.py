from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException 
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


def scroll_to_bottom(driver, scroll_pause_time=1.0):
    """
    Scrolls the web page till the end.
    
    Args:
    driver: Selenium WebDriver.
    scroll_pause_time: Time to wait for the page to load more contents.
    """
    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to the bottom of the page
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load the page
        time.sleep(scroll_pause_time)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            # If heights are the same, it is likely that the bottom has been reached
            break
        last_height = new_height
        
        

def wait_for_angular_ready(driver, timeout=10):
    """Wait for AngularJS to finish all HTTP requests, if AngularJS is present.
    
    Args:
        driver: The Selenium WebDriver instance.
        timeout: Maximum time in seconds to wait for AngularJS to become ready, if used.

    Returns:
        bool: True if AngularJS finishes all HTTP requests or if AngularJS is not used, False if the timeout is reached.
    """
    try:
        # Check first if Angular is defined on the page
        angular_defined = driver.execute_script("return window.angular !== undefined;")
        if not angular_defined:
            print("AngularJS is not used on this page.")
            return True  # Angular is not used on the page, so skip waiting for Angular requests.
        
        WebDriverWait(driver, timeout).until(
            lambda x: driver.execute_script(
                "return typeof angular !== 'undefined' && "
                "angular.element(document.body).injector().get('$http').pendingRequests.length === 0")
        )
        return True
    except TimeoutException:
        return False
    
def wait_for_document_complete(driver, timeout=10):
    """Wait until the document's readyState becomes 'complete'.
    
    Args:
        driver: The Selenium WebDriver instance.
        timeout: Maximum time in seconds to wait for the document to be fully loaded.

    Returns:
        bool: True if the document state becomes 'complete', False if the timeout is reached.
    """
    try:
        WebDriverWait(driver, timeout).until(
            lambda x: driver.execute_script("return document.readyState") == "complete"
        )
        return True
    except TimeoutException:
        return False


def create_selenium_driver():
    return webdriver.Chrome();


def wait_for_lazy_loaded_elements(driver, attribute="loading", attribute_value="lazy", wait_time=30):
    """
    Efficiently waits for elements that are expected to be lazy-loaded. If no such elements are present,
    the function returns immediately without waiting.

    Args:
        driver (webdriver): The WebDriver instance for Selenium.
        attribute (str): The attribute to look for in elements, default is "loading".
        attribute_value (str): The value of the attribute indicating lazy loading, default is "lazy".
        wait_time (int): Maximum time to wait for each element to become visible, in seconds.

    Returns:
        list: A list of WebElement found, or an empty list if none are found or if a timeout occurs.
    """
    # First, quickly check if there are any lazy-loaded elements on the page
    lazy_elements = driver.find_elements(By.XPATH, f"//*[@{attribute}='{attribute_value}']")
    if not lazy_elements:
        print("No lazy-loaded elements found.")
        return []

    # If elements are present, wait for each to be visible
    visible_lazy_elements = []
    for element in lazy_elements:
        try:
            WebDriverWait(driver, wait_time).until(EC.visibility_of(element))
            visible_lazy_elements.append(element)
        except TimeoutException:
            print(f"Timed out waiting for an element with {attribute}='{attribute_value}' to become visible.")

    return visible_lazy_elements