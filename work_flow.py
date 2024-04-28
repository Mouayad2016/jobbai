from ai.agents.web_form_answerer.pydantic.agent import web_form_answerer
from automation.form_automation import fill_form
from data_process.html_sanitizer import find_submit_elements
from helper import extract_and_convert_dict, process_form, html_form_processing_workflow
from data_process.html_sanitizer import  find_new_selects


def from_ready_and_contain_inputs_with_file_inputs(driver, processed_form):
    
        submit_elements = find_submit_elements(processed_form, ['submit', 'send', 'confirm', 'ansökan', 'skicka' ])
        
        form_answers = web_form_answerer(processed_form)
        print("My form aswers: ",form_answers)
        extracted_dict = extract_and_convert_dict(str(form_answers))
        fill_form(driver, extracted_dict)
        
        
        # Reapeat workfolw
        new_processed_form = html_form_processing_workflow(driver)
        new_select_tags_in_body=  find_new_selects(str(process_form), str(new_processed_form))
        if(new_select_tags_in_body): 
            print("New select tag in the from body")
            with open("html_form.html", 'w', encoding='utf-8') as file:
                file.write(str(new_processed_form))  
            form_answers = web_form_answerer(new_processed_form)
            extracted_dict = extract_and_convert_dict(str(form_answers))
            fill_form(driver, extracted_dict)   
        
        # click_elements_by_selectors(driver, submit_elements)
        print("Form ready")
