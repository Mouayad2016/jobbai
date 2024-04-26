from langchain.agents.format_scratchpad.openai_tools import (
    format_to_openai_tool_messages,
)
from langchain.agents.output_parsers.openai_tools import OpenAIToolsAgentOutputParser
from .llm import prompt, llm_with_tools, tools
from langchain.agents import AgentExecutor
from .output_parser import parse


# * This is not working as expected. GPT-3 can't do the job, and 
# * parsing is not working correctly with GPT-4. Use Pydantic instead.


html_tagis = '''<body>
	<form id="applform">
		<h2 class="sub-heading h2">Personal information</h2>
		<label class="control-label input-label is-required"
			>E-mail address*
		</label>
		<input
			class="form-control input-field"
			id="prof_email"
			placeholder=""
			type="text"
			value=""
		/>

		<label class="control-label input-label is-required"
			>Confirm email address*
		</label>
		<input
			class="form-control input-field autosaveable"
			id="prof_emailrepeat"
			placeholder=""
			type="text"
			value=""
		/>

		<label class="control-label input-label is-required">First name* </label>
		<input
			class="form-control input-field autosaveable"
			id="prof_firstname"
			placeholder=""
			type="text"
			value=""
		/>

		<label class="control-label input-label is-required">Surname* </label>
		<input
			class="form-control input-field autosaveable"
			id="prof_surname"
			placeholder=""
			type="text"
			value=""
		/>

		<label class="input-label birthday-label is-required">Birth year * </label
		><select
			aria-label="Birth year "
			class="select-field select-field--auto-width autosaveable"
			id="prof_birthyear"
		></select>

		<label class="control-label input-label is-required">Phone* </label>
		<input
			class="form-control input-field autosaveable"
			id="prof_telephone"
			placeholder=""
			type="text"
			value=""
		/>

		<label class="control-label input-label is-required">Address* </label>
		<input
			class="form-control input-field autosaveable"
			id="prof_address"
			placeholder=""
			type="text"
			value=""
		/>

		<label class="control-label input-label is-required">Postal code* </label>
		<input
			class="form-control input-field autosaveable"
			id="prof_postalcode"
			placeholder=""
			type="text"
			value=""
		/>

		<label class="control-label input-label is-required">City* </label>
		<input
			class="form-control input-field autosaveable"
			id="prof_postalcity"
			placeholder=""
			type="text"
			value=""
		/>

		<label class="control-label input-label is-required">Country*</label>
		<select
			class="select-field form-control autosaveable"
			id="prof_countrycode"
			title="Country"
		></select>

		<h3
			class="control-label input-label is-required h3"
			id="heading-prof_cvdocument"
		>
			CV document*
		</h3>

		<p
			class="upload__acceptable-filetypes"
			id="acceptable-filetypes-prof_cvdocument"
		>
			You can attach files in following formats: .doc .docx .rtf .pdf .jpg .gif
		</p>

		<button
			aria-describedby="acceptable-filetypes-prof_cvdocument"
			aria-label="CV (opens new window)"
			aria-labelledby="heading-prof_cvdocument button-prof_cvdocument"
			class="button"
			id="button-prof_cvdocument"
			type="button"
		>
			Select file
		</button>
		<a class="nav-link" href="javascript:void(0)">Write in form instead</a>
		<input type="hidden" />
		<input type="hidden" />

		<textarea
			aria-hidden="true"
			class="editwithtinymce"
			id="prof_cvtext"
		></textarea
		>p
		<input id="prof_cvdocument0" type="hidden" value="" />
		<p class="text-color-muted">
			To get help with keyboard shortcuts, press ALT+0 while on the text area
		</p>
		<p><a class="nav-link" href="javascript:void(0)">Back to file upload</a></p>

		<input
			aria-hidden="true"
			class="hidden-input"
			id="prof_cvdocument-required"
		/>

		<h3
			class="control-label input-label is-required h3"
			id="heading-prof_pldocument"
		>
			Personal letter*
		</h3>

		<p
			class="upload__acceptable-filetypes"
			id="acceptable-filetypes-prof_pldocument"
		>
			You can attach files in following formats: .doc .docx .rtf .pdf .jpg .gif
		</p>

		<button
			aria-describedby="acceptable-filetypes-prof_pldocument"
			aria-label="Personal letter (opens in new window)"
			aria-labelledby="heading-prof_pldocument button-prof_pldocument"
			class="button"
			id="button-prof_pldocument"
			type="button"
		>
			Select file
		</button>
		<a class="nav-link" href="javascript:void(0)">Write in form instead</a>
		<input type="hidden" />
		<input type="hidden" />

		<textarea
			aria-hidden="true"
			class="editwithtinymce"
			id="prof_personalmotivation"
		></textarea
		>p
		<input id="prof_pldocument0" type="hidden" value="" />
		<p class="text-color-muted">
			To get help with keyboard shortcuts, press ALT+0 while on the text area
		</p>
		<p><a class="nav-link" href="javascript:void(0)">Back to file upload</a></p>

		<input
			aria-hidden="true"
			class="hidden-input"
			id="prof_pldocument-required"
		/>

		<h3 class="input-label h3" id="heading-file_othdocument">
			Other documents
		</h3>

		<p
			class="upload__acceptable-filetypes"
			id="acceptable-filetypes-file_othdocument"
		>
			You can attach files in following formats: .doc .docx .rtf .pdf .jpg .gif
		</p>
		<button
			aria-describedby="acceptable-filetypes-file_othdocument"
			aria-labelledby="heading-file_othdocument btn-file_othdocument"
			class="button"
			id="btn-file_othdocument"
			type="button"
		>
			Select file
		</button>

		<fieldset class="form-group">
			<legend class="input-label is-required">
				Do you have experience in project controlling?*
			</legend>
			<label class="radio-label"
				><input
					class="radio-input"
					id="radio_301_645"
					type="radio"
					value="645"
				/>
				 Yes</label
			><label class="radio-label"
				><input
					class="radio-input"
					id="radio_301_646"
					type="radio"
					value="646"
				/>
				 No</label
			>
		</fieldset>
		<fieldset class="form-group">
			<legend class="input-label is-required">
				Do you have experience in contract management?*
			</legend>
			<label class="radio-label"
				><input
					class="radio-input"
					id="radio_302_647"
					type="radio"
					value="647"
				/>
				 Yes</label
			><label class="radio-label"
				><input
					class="radio-input"
					id="radio_302_648"
					type="radio"
					value="648"
				/>
				 No</label
			>
		</fieldset>
		<fieldset class="form-group">
			<legend class="input-label is-required">
				Do you have experience from working in nonprofit environments?*
			</legend>
			<label class="radio-label"
				><input
					class="radio-input"
					id="radio_298_641"
					type="radio"
					value="641"
				/>
				 Yes</label
			><label class="radio-label"
				><input
					class="radio-input"
					id="radio_298_642"
					type="radio"
					value="642"
				/>
				 No</label
			>
		</fieldset>
		<fieldset class="form-group">
			<legend class="input-label is-required">
				Are you fluent in English?*
			</legend>
			<label class="radio-label"
				><input
					class="radio-input"
					id="radio_299_643"
					type="radio"
					value="643"
				/>
				 Yes</label
			><label class="radio-label"
				><input
					class="radio-input"
					id="radio_299_644"
					type="radio"
					value="644"
				/>
				 No</label
			>
		</fieldset>
		<label class="input-label is-required"
			>Do you hold a bachelor's degree in relevant fields or equivalent
			experience? Please explain:*</label
		>
		<textarea
			class="form-control textarea"
			id="text_300"
			placeholder=""
			value=""
		></textarea>

		<label class="chackbox is-required" id="labelterms">
			<input aria-labelledby="labelterms" id="acceptterms" type="checkbox" />
			I consent to my personal data being handled as described in the policy  <a
				href="javascript:showPolicy()"
				id="policy_link"
				>Show privacy policy</a
			>
		</label>

		<input id="policyid" type="hidden" value="8" />

		<h2 class="heading h2">Correct the following errors before submitting:</h2>

		<button class="button" type="submit">Register</button>
	</form>
	<form id="ie8form_upload"><input id="ie8_upload" type="file" /></form>
	<form id="fileform_ulitmate">
		<input id="fileform_ulitmateuploadfield" type="file" />
	</form>
</body>
'''


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
   {
  "input": 
    f'''
    
	This is an HTML tag {html_tagis} from a website. 
	In order to apply for this job, determine the answers for each question necessary to complete the application. 

	Answer as follows:

	- If the answer tag is "Text," create the text for the question.
	- If the answer tag is "File Upload," choose the correct file and put its path as the answer.
	- If the answer is to check or select, answer with the appropriate selection.
    - Add submit buttons ID with value of "Submit"

	Respond with a map of each tag's ID and its corresponding answer like this exemple
	{{"ID":"Answer"}}. 

	If you do not know the answer, respond randomly.
 
	'''
},
    return_only_outputs=True,
)
    # return ai_generated_email_with_title;
