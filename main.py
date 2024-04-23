from httpcore import TimeoutException
from job_scrapper import doScaping
from helper import adScrapper, wait_for_lazy_loaded_elements,scroll_to_bottom
from ai.agents.job_post_analyzer.agent import analyize;
from ai.agents.email_writer.agent import generate_email;
from ai.agents.website_analyzer.agent import web_analize;

from services.stmp import create_email , send_email
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

from selenium.webdriver.support.ui import WebDriverWait
from data_process.html_processor import clean_html
# url = "https://arbetsformedlingen.se/platsbanken/annonser/28730687" # This is a mail link
url = "https://www.randstad.se/mitt-randstad/ansok/d242f1e7-fe46-4e57-8cd5-e759dd2e72c3/" # This is a mail link

# jobs= doScaping(url)
# for job in jobs:

# data = adScrapper(url);
# job_title= data['job_title']
# company_name= data['company_name']
# job_role= data['job_role']
# job_location =data['job_location']
# job_scope= data['job_scope']
# employment_type= data['employment_type']
# job_count= data['job_count']
# job_description = data['job_description']

# if data.get('mail_application_info') is not None: 
#     applicaiotn_info = data['mail_applicaiton_info']
#     start_time = time.time()
    
#     email_title_and_body = analyize(applicaiotn_info)

#     send_to = email_title_and_body['e_mail'];
#     email_reference = email_title_and_body['reference'];

#     email_body= generate_email(job_description, email_reference, send_to)

#     print(email_title_and_body)
#     print(email_body)

#     email_title = email_body['title']
#     email_body = email_body['mail']

#     files_to_attach = ['./test.pdf', './cover.txt']

#     email_message = create_email(email_title,"test@enormt.se", "mouayad1998@hotmail.com", files_to_attach, email_body);

#     send_email("smtp.titan.email", 465, "test@enormt.se", "Test123@","mouayad1998@hotmail.com", email_message);
        
#     end_time = time.time()
#     total_time = end_time - start_time
#     print(total_time)
    
# if data.get('application_link') is not None:

# applicaiton_link = data['application_link']

def check_document_ready(driver):
    """Check if the document is fully loaded."""
    return driver.execute_script("return document.readyState") == 'complete'
    
driver = webdriver.Chrome()
driver.get("https://sollentuna.varbi.com/what:job/jobID:719501/type:job/where:1/apply:1")

ready_state = driver.execute_script("return document.readyState")
bindings_ready = driver.execute_script("return typeof angular !== 'undefined' && angular.element(document.body).injector().get('$http').pendingRequests.length === 0")
scroll_to_bottom(driver)
# lazy_elements = wait_for_lazy_loaded_elements(driver, "loading", "lazy")

driver.execute_script("""
var scripts = document.body.getElementsByTagName('script');
while (scripts.length > 0) {
scripts[0].parentNode.removeChild(scripts[0]);
}

var footer = document.getElementById('footer');
if (footer) {
footer.parentNode.removeChild(footer);
}

// Optionally remove any other elements identified as a footer by a different method
var footerElements = document.querySelectorAll('.footer, footer');
footerElements.forEach(function(element) {
element.parentNode.removeChild(element);
});
""")

body_content = driver.find_element(By.CSS_SELECTOR, "body").get_attribute('innerHTML')
# print(body_content)
# input_elements = driver.find_elements(By.CSS_SELECTOR, "input[type='text'], input[type='file']")

# links = driver.find_elements(By.TAG_NAME, "a")
# form_elements = driver.find_elements(By.CSS_SELECTOR, "input, textarea, select")

# cleaned_links_html = []
# cleaned_input_fields_html = []
# # Iterate over each link and print the href attribute
# for link in links:
#     href = link.get_attribute('href')
#     text = link.text.strip()
#     label = link.get_attribute('aria-label')
#     print("---------------Link-----------------")
#     print("Tag Name: a")
#     print("Link:", href)
#     print("Text:", text)
#     a_tag={"Tag Name": "a","Link": href,"Text": text}
#     cleaned_links_html.append(a_tag)
    
#     # soup = BeautifulSoup(link_html, 'html.parser') # type: ignore
#     # for svg in soup.find_all('svg'):
#     #     svg.decompose()
#     # for img in soup.find_all('img'):
#     #     img.decompose()
    
#     # cleaned_links_html.append(str(soup))
#     # print(f"Link: {soup}")

# # Iterate over each text input element and print relevant details
# for element in form_elements:
#     input_type = element.get_attribute('type')
#     input_name = element.get_attribute('name')
#     input_placeholder = element.get_attribute('placeholder')
#     input_value = element.get_attribute('value')
#     print("Tag Name: input")
#     print("Type:", input_type)
#     print("Name:", input_name)
#     print("Placeholder:", input_placeholder)
#     print("Value:", input_value)
#     input_field={"Tag Name": element.tag_name, "Type": input_type, "Name": input_name, "Placeholder": input_placeholder, "Value": input_value, }
#     cleaned_input_fields_html.append(input_field)
    
#     label_text = None
#     # 1. Direct Containment
#     try:
#         parent_label = element.find_element(By.XPATH, "./ancestor::label") # type: ignore
#         label_text = parent_label.text
#         print("Direct Containment")
#     except Exception:
#         pass

#     # 2. Sibling Elements
#     if not label_text:
#         try:
#             label = element.find_element(By.XPATH, "preceding-sibling::label[1]") # type: ignore
#             label_text = label.text
#             print("Sibling Elements")

#         except Exception:
#             pass

#     # 3. Closest Matching Text
#     if not label_text:
#         try:
#             possible_label = element.find_element(By.XPATH, "preceding::node()[1]/self::label | following::node()[1]/self::label")# type: ignore
#             label_text = possible_label.text
#             print("Closest Matching Text")

#         except Exception:
#             pass
#     # 4. Use aria-labelledby
#     if not label_text:
#         labelledby_id = element.get_attribute('aria-labelledby') # type: ignore
#         if labelledby_id:
#             try:
#                 label = driver.find_element(By.ID, labelledby_id)
#                 label_text = label.text
#                 print("aria-labelledby")
#             except Exception:
#                 pass

#     # 5. Check aria-label as a last resort
#     if not label_text:
#         label_text = element.get_attribute('aria-label')
            
    

#     print("Associated Label:", label_text if label_text else "No label found")
#     # input_html = input_field.get_attribute('outerHTML')
#     # soup = BeautifulSoup(input_html, 'html.parser') # type: ignore
#     # for svg in soup.find_all('svg'):
#     #     svg.decompose()
#     # for img in soup.find_all('img'):
#     #     img.decompose()
#     print("---------------input_field-----------------")
    # print("Input Field HTML:", str(soup))
    
    # cleaned_input_fields_html.append(str(soup))
    
# print(cleaned_links_html+cleaned_input_fields_html)

    
# soup = BeautifulSoup(body_content, 'html.parser') # type: ignore
# a_tags = soup.find_all('a')
# for tag in a_tags:
#     print(tag)
#     print("URL:", tag.get('href'))
# result = web_analize(cleaned_links_html+cleaned_input_fields_html)
# print(result);





# print(body_content)

def clean_html_and_save(html_content, output_file):
    """Clean the HTML content and save it to a local HTML file."""
    cleaned_html = clean_html(html_content)
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(cleaned_html)

output_file = "cleaned_html_output.html"
clean_html_and_save(body_content, output_file)

# print(clean_html(body_content))
driver.quit()
