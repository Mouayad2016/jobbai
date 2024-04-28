from httpcore import TimeoutException
from job_scrapper import doScaping
from selenium_driver.driver_interactor import *
from ai.agents.job_post_analyzer.agent import analyize;
from ai.agents.email_writer.agent import generate_email;
from ai.agents.website_analyzer.pydantic.agent import web_analize;
from ai.agents.determine_file_upload.pydantic.agent import determin_file_upload
import ast
from helper import wait_for_page_load, html_form_processing_workflow, html_body_processing_workflow

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import Select

from data_process.html_processor import clean_html


import json


from automation.form_automation import find_file_inputs, handle_cookie_popups,click_cookie_accept_buttons, fill_form,click_elements_by_selectors
from work_flow import *

# url = "https://arbetsformedlingen.se/platsbanken/annonser/28730687" # This is a mail link
url = "https://epidemic-sound.teamtailor.com/jobs/3545361-senior-fullstack-engineer?promotion=909809-arbetsformedlingen" # This is a mail link

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

# * Apply button 
exmple_1_url= "https://www.jobseurope.io/jobs/Recruiter-with-English-(mfd)+4160" 

# * Apply link
apply_link_exmple_1_url= "https://www.jobseurope.io/jobs/Kundenbetreuung-im-Bereich-Telekommunikation-(mwd)+5500" 
apply_link_exmple_2_url= "https://vwr.wd1.myworkdayjobs.com/en-US/avantorJobs/job/Mlndal-SWE/Research-Technician-Imaging--M-F-D-_R-156727-1?source=Governmental_Labour_Agency" 
apply_link_exmple_3_url= "https://jobb.bravura.se/lediga-jobb/fullstackutvecklare-till-ciko-4918001/" 
apply_link_exmple_4_url= "https://web103.reachmee.com/ext/I021/1690/job?site=7&lang=UK&validator=9c16162aeec1b1c78db51d0c3e4163a1&ref=https%3A%2F%2Farbetsformedlingen.se%2Fplatsbanken%2F&job_id=109&utm_medium=talentech_publishing&utm_source=platsbanken" 

# * Ready form 
form_exmple_1_url= "https://jobs.gigstep.se/jobs/4083469-fullstackutvecklare-se-hit?promotion=992424-arbetsformedlingen" 
form_exmple_2_url= "https://jobs.cruitive.com/job/cluthrxmf00w2s60ozvpj6g4y/apply" 
form_exmple_2_url= "https://emp.jobylon.com/applications/jobs/231995/create/?utm_source=ams&utm_medium=promotionserializer" 

# * Log in page 
log_in_exmple_1_url= "https://www.jobseurope.io/jobs/Recruiter-with-English-(mfd)+4160" 
log_in_exmple_2_url= "https://arbetsformedlingen.varbi.com/what:job/jobID:713502/type:job/where:1/apply:1" 


driver.get(apply_link_exmple_3_url)
# driver.get("https://team.nytida.se/jobs/3656333-timvikarier-till-varnhem-s-a-norlings-gruppboende-lss?promotion=930622-arbetsformedlingen")
# wait_for_angular_ready(driver)
# wait_for_document_complete(driver)
# scroll_to_bottom(driver)



    # wait_for_lazy_loaded_elements(driver, "loading", "lazy")

wait_for_page_load(driver)
click_cookie_accept_buttons(driver)





process_html_body = html_body_processing_workflow(driver)

with open("html_form.html", 'w', encoding='utf-8') as file:
    file.write(str(process_html_body))
    
# for i in range(100):

#     result = web_analize(process_html_body)  # type: ignore
#     driver.quit()
#     print(result)

# processed_form = html_form_processing_workflow(driver)

# result_to_json_string = json.dumps(result)
# result_to_json = json.loads(result_to_json_string)

# # print(result_to_json) # type: ignore
# if result['is_application_form']:




# with open("html_form.html", 'w', encoding='utf-8') as file:
#     file.write(str(processed_form))
    
# is_file_inputs =  find_file_inputs(processed_form)

# if is_file_inputs: 
#     from_ready_and_contain_inputs_with_file_inputs(driver, processed_form);



    # how_to_file_upload= determin_file_upload(processed_form)
    # form_answers = web_form_answerer(processed_form)
    # print(how_to_file_upload)
 
            
# fill_form(driver, application_answers)
            
# time.sleep(300)


