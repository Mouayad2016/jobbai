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
        Analyze it and determine whether this website is where users should apply for the job, 
        or if the website directs users to another website to apply for the job. 
        If the HTML contains a text field for a job application form, 
        set is_application_form to true and application_link to None. 
        Otherwise, set is_application_form to false and application_link to true
         '''
        },
        return_only_outputs=True,
    )
    return ai_generated_email_with_title;


