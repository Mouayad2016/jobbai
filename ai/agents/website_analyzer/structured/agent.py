from langchain.agents.format_scratchpad.openai_tools import (
    format_to_openai_tool_messages,
)
from langchain.agents.output_parsers.openai_tools import OpenAIToolsAgentOutputParser
from .llm import prompt, llm_with_tools, tools
from langchain.agents import AgentExecutor
from .output_parser import parse


def web_analize(html_tag):
    agent = (
        {
            "input": lambda x: x["input"],
            "agent_scratchpad": lambda x: format_to_openai_tool_messages(
                x["intermediate_steps"]
            ),
        }
        | prompt
        | llm_with_tools
        | parse
    )

    agent_executor = AgentExecutor(agent= agent, tools= [], verbose=True)  # type: ignore
    
    ai_generated_email_with_title = agent_executor.invoke(
        {"input": 
         f'''
        This is an HTML tag {html_tag} from a website. 
        Analyze it and determine whether this website is one of the following:
        (A) - Job application form where users submit their CVs and information seeking employment.
        (B) - A preliminary step in the job application process where users are asked to submit an email, or to login or create an account.
        (C) - A website with information about the job, including a link to direct users to the application website.
        
        Respond as follows based on your conclusions. You can only have one conclusion; choose the one that best suits this case: 
        
        If (A) set is_application_form to true. Set is_pre_step to false. Set application_link to ''
        If (B) set is_application_form to false. Set is_pre_step to true. Set application_link to ''.
        If (C) set is_application_form to false. Set is_pre_step to false. Set the application_link.
        If none of (A) or (B) or (C) Set is_application_form to false. Set is_pre_step to false. Set the application_link to ''.
        
        '''
        },
        return_only_outputs=True,
    )
    return ai_generated_email_with_title;


        # - If the tag contains a job application form with minimum input fields for name, email, and a file upload for a CV.
        # Set is_application_form to true. Set is_pre_step to false. Set application_link to None. 
        
        # - If the tag contains a form or inputs for only email och login and not input fields for name, and a file upload for a CV.
        # Set is_application_form to false. Set is_pre_step to true. Set application_link to the link if it exist. 

        # - If the tag dont contains any application form or text fields and has link to apply for the job application.
        # Set is_application_form to false. Set is_pre_step to true. Set the application_link.
        
        # The role is application_link cannot exist if is_application_form is set to true. 
        # If there is an application link, then is_application_form must be set to false and is_pre_step must be set to false.
        # application_link cannot exist if is_pre_step is set to true. 
        # is_application_form can not be ture if is_pre_step is set to true only one of them can be ture. Never break this rule.