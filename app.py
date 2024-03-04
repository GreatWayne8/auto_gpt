import os
from apikey import apikey

# streamlit is used for building interactive web apps
import streamlit as st
from langchain.llms import OpenAI 
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain 
from langchain.memory import ConversationBufferMemory 
from langchain.utilities import WikipediaAPIWrapper
os.environ['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'] = apikey


# app framework  
st.title('Waynes GPT')
prompt = st.text_input('Enter your prompt here') 

title_prompt = PromptTemplate(
    input_variables = ['topic'],
    template = 'write me a youtube video title about {topic}' 
)

script_prompt = PromptTemplate(
    input_variables = ['title' 'Wikipedia_research'],
    template = 'write me a youtube video script on this title TITLE: {Title} while also leveraging wikipedia research:{wikipedia_research}' 
)
title_memory = ConversationBufferMemory(input_key='topic', memory_key='chat_history')
script_memory = ConversationBufferMemory(input_key='title', memory_key='chat_history')



# llms
llm = OpenAI(temperature=0.9)
title_chain = LLMChain(llm=llm, prompt=title_prompt, verbose=True, output_key='title', memory=title_memory)
script_chain = LLMChain(llm=llm, prompt=script_prompt, verbose=True, output_key='script', memory=script_memory)
 
# sequential_chain = SequentialChain(chains = [title_chain, script_chain], input_variables=['topic'], 
# output_variables=['title' 'topic'], verbose=True ) 
wiki = WikipediaAPIWrapper()


# show  to the screen if theresa prompt
if prompt:
    title =  title_chain.run(prompt) 
    wiki_research = wiki.run(prompt)
    script = script_chain.run(Title=title, wikipedia_research=wiki_research, title=title ) 

    st.write(title)
    st.write(script)

    with st. expander('Title History'):
        st.info(title_memory.buffer)

    with st. expander('Script History'):
        st.info(script_memory.buffer)

    with st. expander('Wikipedia Research'):
        st.info(wiki_research)