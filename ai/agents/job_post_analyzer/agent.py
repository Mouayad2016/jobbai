from langchain.agents.format_scratchpad.openai_tools import (
    format_to_openai_tool_messages,
)
from langchain.agents.output_parsers.openai_tools import OpenAIToolsAgentOutputParser
from .llm import prompt, llm_with_tools, tools
from langchain.agents import AgentExecutor
from .output_parser import parse

a_tag= '''<div _ngcontent-ccg-c75="" class="apply-wrapper print-break-inside"><h2 _ngcontent-ccg-c75="" translate="section-apply-for-job.label" class="pb-mb-8">Sök jobbet</h2><!----><div _ngcontent-ccg-c75="" class="ng-star-inserted"><div _ngcontent-ccg-c75="" class="last-date ng-star-inserted"><span _ngcontent-ccg-c75="" translate="section-apply-for-job.sista-ansokningsdag-label">Ansök senast</span><strong _ngcontent-ccg-c75=""> 10 maj</strong><span _ngcontent-ccg-c75=""> (om 20 dagar)</span></div><!----><div _ngcontent-ccg-c75="" class="break-word pb-mb-16 ng-star-inserted"> Ange referens <strong _ngcontent-ccg-c75="">Plantsättning 2023</strong> i din ansökan </div><!----><div _ngcontent-ccg-c75="" class="ansok ng-star-inserted"><i _ngcontent-ccg-c75="" class="i-af-at"></i><div _ngcontent-ccg-c75="" class="application-info"><h3 _ngcontent-ccg-c75="" class="apply-header apply-header--less-margin">Ansök via mejl</h3><div _ngcontent-ccg-c75="" class="break-word ng-star-inserted">Mejla din ansökan till </div><!----><div _ngcontent-ccg-c75="" class="dont-break-out pre-line ng-star-inserted"><span _ngcontent-ccg-c75="" class="d-print-inline"><a _ngcontent-ccg-c75="" data-mail-application="" data-event-category="AS - Platsbanken" data-event-value="1" href="mailto:leonidgroza@mail.ru" data-event-action="AS - Platsbanken - Annonssida - Maila din ansökan - Link - Click" data-event-name="AS - Platsbanken - Visat intresse på Annonssida">leonidgroza@<wbr data-event-include="true">mail.ru</a></span></div><!----><!----><!----></div></div><!----></div><!----></div>'''


def analyize(apply_information):
    # apply_information = "Sök jobbet Ansök senast 3 maj (om 12 dagar) ange Gör det fort. Ansök via mejl Mejla din ansökan till info@ modernera.se"
    print(apply_information)
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
        #     f'''
        #  This is information related to a job ad. 
        #  Analyze this job application information information_a: {apply_information}. 
        #  Respond about the last date to apply, the application email address and reference.
        #  Sometimes a reference or specific text that should be sent with the email is needed.
        #  A reference can include information such as a specific case, reference, or text to mention or specify; use this as a reference in your response.
        #  If any information is missing, respond with 'None'. Never break this rule..
        #  '''
         f'''Detta är information relaterad till en jobbannons. 
         Analysera denna jobbansökningsinformation: {apply_information}. 
         Svara om sista ansökningsdatum, ansöknings-e-postadress och referens.
         ibland behövs en refrece eller epesefik text som bör skickas med mejlet.
         reference kan inkludera information som specifikt ärende, 
         referens eller text att nämna eller ange; använd detta som en referens i ditt svar. 
         Om någon information saknas, svara med 'None'. Bryt aldrig denna regel.'''
        },
        return_only_outputs=True,
    )
    return ai_generated_email_with_title;


