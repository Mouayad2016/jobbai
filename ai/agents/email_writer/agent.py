from langchain.agents.format_scratchpad.openai_tools import (
    format_to_openai_tool_messages,
)
from langchain.agents.output_parsers.openai_tools import OpenAIToolsAgentOutputParser
from .llm import prompt, llm_with_tools, tools
from langchain.agents import AgentExecutor
from .output_parser import parse


job_desc="Om jobbet About UnionAll UnionAll stands at the forefront of data innovation, crafting solutions that empower businesses to unlock the full potential of their data. With our cutting-edge AI tools, we streamline the process for businesses to derive actionable insights, while ensuring data providers maximize their earnings with minimal effort. Our commitment to automation and AI transforms data assets into profitable ventures, offering our clients and partners unparalleled service in today's data-driven market. Core Values Bring Passion: We pour our hearts into our work, pushing the boundaries of what's possible. Be Honest: Integrity guides every decision we make. Win Fast: We believe in quick, decisive action to stay ahead. Show Respect: Our team is our family. We thrive on mutual respect. Stay Endurant: Persistence is our key to overcoming challenges. Role Overview As a Full Stack Developer at UnionAll, you'll be instrumental in developing software solutions that align with our strategic vision. You will work closely with our team to design, build, and maintain our AI-powered platforms, directly contributing to our mission of transforming data into value. Key Responsibilities Develop and maintain scalable, robust applications from front to back end. Collaborate with cross-functional teams to define, design, and ship new features. Ensure code integrity, organization, and automation. Stay updated with new technologies and industry trends to incorporate into operations and activities. Skills and Qualifications Technical Skills Required: Proficiency in JavaScript, Python, frameworks (React, Next.js), databases (Postgres, Snowflake), Docker, Kubernetes, and GCP. Soft Skills: Exceptional problem-solving abilities, excellent communication skills, and a strong team player. Experience A minimum of 3 years of experience in full-stack development is required. Education A Bachelor's degree in IT or an equivalent field is required. Work Model This position is based in our Stockholm office located at S:t Eriksplan. Salary Range and Benefits Competitive salary package including health insurance, retirement plans, paid time off, professional development opportunities, and a health care allowance. How to Apply Ready to take your career to the next level with UnionAll? Please send your resume and cover letter to careers@unionall.ai by the 26th of April. We're looking forward to hearing how you can contribute to our journey of data innovation!"

def generate_email(job_desc, reference, email_receiver):
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
    user_input = f'For this job: {job_desc}. Create an email to {email_receiver} seeking this job with max 500 characters, you found this job at arbetsformedlingen Platsbanken. Be casual and polite keep you mail short. Never break this rule. {(f"Add this as email title: {reference}" if reference != "None" else "")}'
   
    ai_generated_email_with_title = agent_executor.invoke(
        {"input": user_input},
        return_only_outputs=True,
    )
    return ai_generated_email_with_title;
