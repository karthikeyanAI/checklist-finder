from langchain.chat_models import ChatOpenAI
from langchain import PromptTemplate, LLMChain
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    AIMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.schema import AIMessage, HumanMessage, SystemMessage
import os
from langchain_core.output_parsers import JsonOutputParser

os.environ["OPENAI_API_KEY"] ='your_api_key'
chat = ChatOpenAI(temperature=0)

template = "your are check list generator you have to get the error code from the user the answer should mutiple values"
system_message_prompt = SystemMessagePromptTemplate.from_template(template)

legal_text = "FRM-41082"
example_input_one = HumanMessagePromptTemplate.from_template(legal_text)

plain_text = '''Title: Verify the Field Width user preference for the affected user,
Description: Check the value of the 'Field Width' user preference for the user experiencing the issue.

Title: Check the current setting of SUMMARY_FIELD_WIDTH in MRP_WORKBENCH_DISPLAY_OPTIONS,
Description: Check the current value of the SUMMARY_FIELD_WIDTH setting in the MRP_WORKBENCH_DISPLAY_OPTIONS table for the affected user.

Title: Check the canvas position for items causing the error,
Description: Investigate the canvas position for items causing the FRM-41082 error.

Title: Validate other user preferences that might impact the form layout,
Description: Check other user preferences that might impact the layout of the form.

Title: Investigate any other customizations or personalizations that might affect the form,
Description: Look into any customizations or personalizations that might have been applied to the form and could be causing the error.
'''

example_output_one = AIMessagePromptTemplate.from_template(plain_text)

human_template = "{legal_text}"
human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
chat_prompt = ChatPromptTemplate.from_messages(
    [system_message_prompt, example_input_one, example_output_one, human_message_prompt]
)

def generate(input):

    request = chat_prompt.format_prompt(legal_text=input).to_messages()
    result = chat(request)



    parser=JsonOutputParser()

    parser.get_format_instructions()

    query = result.content

    parser = JsonOutputParser()

    prompt = PromptTemplate(
        template="convert the data into json output\n{format_instructions}\n{query}\n",
        input_variables=["query"],
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )

    chain = prompt | chat | parser

    data=chain.invoke({"query": query})


    return data




