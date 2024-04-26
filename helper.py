from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from selenium.common.exceptions import TimeoutException
import time

def adScrapper(url):
    driver = webdriver.Chrome()
    driver.get(url)
    job_info = {}
    
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.jobb-container"))
        )
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.ng-star-inserted"))
        )
        
        job_info['job_title'] = driver.find_element(By.CSS_SELECTOR, "h1.break-title").text        
        job_info['company_name'] = driver.find_element(By.CSS_SELECTOR, "h2#pb-company-name").text
        job_info['job_role'] = driver.find_element(By.CSS_SELECTOR, "h3#pb-job-role").text
        job_info['job_location'] = driver.find_element(By.CSS_SELECTOR, "h3#pb-job-location").text
        job_info['job_scope'] = driver.find_element(By.CSS_SELECTOR, "span:nth-of-type(2)").text
        job_info['employment_type'] = driver.find_element(By.CSS_SELECTOR, "div.ng-star-inserted > span:nth-last-child(1)").text
        job_info['job_count'] = driver.find_element(By.CSS_SELECTOR, "span#antal-jobb").text
        job_info['job_description'] = driver.find_element(By.CSS_SELECTOR, "div.job-description").text

        
        apply_element = driver.find_elements(By.CSS_SELECTOR, "div.apply-wrapper.print-break-inside")
       
        
        link_a_tags = apply_element[0].find_elements(By.CSS_SELECTOR, "a.btn.btn-primary[data-event-category='AS - Platsbanken']");
        mailto_a_tags = apply_element[0].find_elements(By.CSS_SELECTOR, "a[data-mail-application");
        
        # Check if the application is via a extern website
        if link_a_tags:
            job_info['application_link'] = link_a_tags[0].get_attribute('href')

        # Check if the application is via mail
        if mailto_a_tags:
            mail_a_tag = apply_element[0].get_attribute('outerHTML')
            soup = BeautifulSoup(mail_a_tag, 'html.parser') # type: ignore
            extracted_text = soup.get_text(separator=' ', strip=True)
            job_info['mail_applicaiton_info'] = extracted_text
        return job_info

    except Exception as e:
        print(f"An error occurred: {e}")
        return job_info
    
    finally:
        driver.quit()






        
        
        
import re
import ast


def extract_and_convert_dict(output_string):
    print("My out put",output_string)
    # Regex to extract the dictionary part
    match = re.search(r"application_answers=(\{.*\})", output_string)
    if match:
        dict_string = match.group(1)
        try:
            # Safely convert string representation to dictionary
            application_answers = ast.literal_eval(dict_string)
            return application_answers;
        except ValueError as e:
            print(f"Error converting string to dictionary: {e}")
            return {};
    else:
        print("No dictionary found in the output")
        return {};
