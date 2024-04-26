from httpcore import TimeoutException
from job_scrapper import doScaping
from helper import adScrapper, extract_and_convert_dict
from selenium_driver.driver_interactor import *
from data_process.html_sanitizer import handle_embedded_html_in_iframe
from ai.agents.job_post_analyzer.agent import analyize;
from ai.agents.email_writer.agent import generate_email;
from ai.agents.website_analyzer.agent import web_analize;
from ai.agents.web_form_answerer.pydantic.agent import web_form_answerer
from ai.agents.determine_file_upload.pydantic.agent import determin_file_upload
import ast

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import Select

from data_process.html_processor import clean_html
from data_process.form_processor import clean_from
import json
from data_process.html_sanitizer import extract_forms

from automation.form_automation import fill_form

from automation.form_automation import find_file_inputs, handle_cookie_popups,click_cookie_accept_buttons
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


driver = create_selenium_driver()
driver.get("https://team.nytida.se/jobs/3656333-timvikarier-till-varnhem-s-a-norlings-gruppboende-lss?promotion=930622-arbetsformedlingen")
# wait_for_angular_ready(driver)
# wait_for_document_complete(driver)
# scroll_to_bottom(driver)

if wait_for_document_complete(driver):
    # Check if Angular is ready
    if wait_for_angular_ready(driver):
        # Perform the scrolling
        scroll_to_bottom(driver)
    else:
        print("Angular did not finish loading.")
else:
    print("Document did not finish loading.")
wait_for_lazy_loaded_elements(driver, "loading", "lazy")

# handle_cookie_popups(driver)
click_cookie_accept_buttons(driver)

iframe_html_contents = handle_embedded_html_in_iframe(driver)

# # Fetch main page body content
body_content = driver.find_element(By.CSS_SELECTOR, "body").get_attribute('innerHTML')

# # Combine main body content with iframe contents
full_content = body_content
for iframe_html in iframe_html_contents:
    full_content += iframe_html  # Append each iframe's HTML to the main body content



# result = web_analize(cleaned_links_html+cleaned_input_fields_html)
# print(result);

# print(body_content)

# def clean_html_and_save(html_content, output_file):
#     """Clean the HTML content and save it to a local HTML file."""
#     cleaned_html = clean_html(html_content)
#     with open(output_file, 'w', encoding='utf-8') as file:
#         file.write(cleaned_html)
#     return cleaned_html

# output_file = "cleaned_html_output.html"
# print(body_content)
# processed_html_body = clean_html_and_save(full_content, output_file)
# result = web_analize(processed_html_body)  # type: ignore




# result_to_json_string = json.dumps(result)
# result_to_json = json.loads(result_to_json_string)

# # print(result_to_json) # type: ignore
# if result['is_application_form']:

extracted_form = extract_forms(full_content)
processed_form = clean_from(extracted_form)
with open("html_form.html", 'w', encoding='utf-8') as file:
    file.write(str(processed_form))
    is_file_inputs =  find_file_inputs(processed_form)
    form_answers = web_form_answerer(processed_form)
    extracted_dict = extract_and_convert_dict(str(form_answers))
    fill_form(driver, extracted_dict)
    time.sleep(300)
    # how_to_file_upload= determin_file_upload(processed_form)
    # form_answers = web_form_answerer(processed_form)
    # print(how_to_file_upload)
 
            
# fill_form(driver, application_answers)
            
# time.sleep(300)
driver.quit()

application_answers={'boolean-4217160-true': 'random', 'boolean-4217180-true': 'random', 'boolean-4217200-true': 'random', 'boolean-4217220-true': 'random', 'boolean-4217240-true': 'random', 'boolean-4217260-true': 'random', 'candidate_answers_attributes_6_text': 'random', 'candidate_first_name': 'Mouayad', 'candidate_last_name': 'Mouayad', 'candidate_email': 'mouayad1998@hotmail.com', 'candidate_phone': '+46 733 524 957', 'candidate_resume_remote_url': '/Users/mouayadmouayad/Desktop/jobbAI/ai/agents/web_form_answerer/pydantic/Arbetsgivarintyg.pdf', 'candidate_file_remote_url': '/Users/mouayadmouayad/Desktop/jobbAI/ai/agents/web_form_answerer/pydantic/Arbetsgivarintyg.pdf', 'candidate_job_applications_attributes_0_cover_letter': '/Users/mouayadmouayad/Desktop/jobbAI/ai/agents/web_form_answerer/pydantic/Arbetsgivarintyg.pdf', 'candidate_consent_given': 'checkbox', 'candidate_consent_given_future_jobs': 'checkbox', 'submit': 'submit'}