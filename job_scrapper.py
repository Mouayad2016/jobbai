from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def doScaping(url):
    driver = webdriver.Chrome()  
    driver.get(url)
    jobs = []
    
    try:
        # Wait until at least one card-container element is loaded
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".card-container"))
        )
        # Find all div elements with the class 'card-container'
        card_containers = driver.find_elements(By.CSS_SELECTOR, "div.card-container")
        # Loop through each card-container and extract information
        for card in card_containers:
            # Extract the job title and link
            title_element = card.find_element(By.CSS_SELECTOR, "h3 > a")
            job_title = title_element.text
            job_link = title_element.get_attribute('href')
            
            # Extract the company name and location
            company_info = card.find_element(By.CSS_SELECTOR, "strong.pb-company-name").text
            
            # Extract job position if available
            job_position = card.find_element(By.CSS_SELECTOR, "div.pb-job-role").text if card.find_elements(By.CSS_SELECTOR, "div.pb-job-role") else "No position listed"
            
            # Extract publication time
            publication_time = card.find_element(By.CSS_SELECTOR, "div.ng-star-inserted").text
            jobs.append({
                'title': job_title,
                'link': job_link,
                'Info': company_info,
                'position': job_position,
                'date': publication_time
            })
        return jobs
    except Exception as e:
        print(e)

    finally:
        driver.quit()
