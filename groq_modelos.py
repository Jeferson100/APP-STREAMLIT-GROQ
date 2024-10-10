
import streamlit as st

from PIL import Image
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationEntityMemory
from langchain.chains.conversation.prompt import ENTITY_MEMORY_CONVERSATION_TEMPLATE
from langchain.llms import OpenAI
from langchain.callbacks import get_openai_callback
import re
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os
from groq import GroqError
from langchain_experimental.agents.agent_toolkits import create_python_agent
from langchain_experimental.tools.python.tool import PythonREPLTool
from langchain_experimental.utilities import PythonREPL
from langchain.agents.agent_types import AgentType



def is_four_digit_number(string):
    pattern = r'^\d{4}$'  # Matches exactly four digits
    return bool(re.match(pattern, string))

# Set Streamlit page configuration
st.set_page_config(page_title="GroqModelos", page_icon=":book:")

# Initialize session states
if "generated" not in st.session_state:
    st.session_state["generated"] = []
if "past" not in st.session_state:
    st.session_state["past"] = []
if "input" not in st.session_state:
    st.session_state["input"] = ""
if "stored_session" not in st.session_state:
    st.session_state["stored_session"] = []


def clear_text():
    st.session_state["temp"] = st.session_state["input"]
    st.session_state["input"] = ""


# Define function to get user input
def get_text():
    """
    Get the user input text.

    Returns:
        (str): The text entered by the user
    """
    input_text = st.text_input("You: ", st.session_state["input"], key="input", 
                            placeholder="Sou seu assistente. Como posso ajudá-lo?", 
                            on_change=clear_text,    
                            label_visibility='hidden')
    input_text = st.session_state["temp"]
    return input_text


    # Define function to start a new chat
def new_chat():
    """
    Clears session state and starts a new chat.
    """
    save = []
    for i in range(len(st.session_state['generated'])-1, -1, -1):
        save.append("User:" + st.session_state["past"][i])
        save.append("Bot:" + st.session_state["generated"][i])        
    st.session_state["stored_session"].append(save)
    st.session_state["generated"] = []
    st.session_state["past"] = []
    st.session_state["input"] = ""
    st.session_state.entity_memory.buffer.clear()
    
with st.sidebar:
    st.sidebar.markdown("""
                        <img src="https://cdn.prod.website-files.com/5da60b8bfc98fdf11111b791/66d62026cfb0f0c4d965cb68_667d84f156ec37bd39bba262_What%2520is%2520Groq%2520AI%2520and%2520How%2520to%2520Use%2520It.webp">
                        """, unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("# Sobre")
    st.markdown(
       "Esse chatbot é criado com os modelos da **GROQ**. Foram desenvolvido com 🦜 LangChain + 🤖 LLMs  + 💻 Streamlit." 
       
            )
    st.markdown("---")
    st.markdown("# Login GROQ:")
    st.write('Clique aqui na imagem para abrir uma conta na **GROQ** e obter um token. Se já tiver um token, insira-o abaixo.')
    st.sidebar.markdown(
    """
    [![Imagem](https://europe1.discourse-cdn.com/business20/uploads/make/original/3X/6/7/679e81c763407115a20f10cac79e1065b1092930.png)](https://console.groq.com/keys)
    """
    )
    
    
    if os.getenv('GROQ_API_KEY') is not None:
        replicate_api = os.getenv('GROQ_API_KEY')
        st.success('API key ja existe!', icon='✅')
    else:
        replicate_api = st.text_input('Enter Replicate API token:', type='password')
        
    
    st.markdown("---")
    st.markdown("# Modelos:")
        
    filtro_modelo = st.sidebar.selectbox("Selecione o modelo:", ["llama3-70b-8192",
                                                                 "llama-3.2-11b-vision-preview",
                                                                 "llama3-groq-70b-8192-tool-use-preview",
                                                                 #"llama-3.2-90b-vision-preview",
                                                                 "gemma2-9b-it",
                                                                 #"distil-whisper-large-v3-en",
                                                                 "llama-3.1-8b-instant",
                                                                 "llama-3.1-70b-versatile",
                                                                 "mixtral-8x7b-32768"])
    
    temperature = st.sidebar.slider('Temperatura', 
                                    min_value=0.01, 
                                    max_value=1.0, 
                                    value=0.1, 
                                    step=0.01)
    
    top_p = st.sidebar.slider('Top_p', 
                              min_value=0.01, 
                              max_value=1.0, 
                              value=0.9, 
                              step=0.01)
    
    max_length = st.sidebar.slider('Max_length', 
                                   min_value=20, 
                                   max_value=200, 
                                   value=100, 
                                   step=5)

    
# Set up the Streamlit app layout

st.markdown(
    '''
    <img src="https://cdn.asp.events/CLIENT_Informa__AADDE28D_5056_B739_5481D63BF875B0DF/sites/ai-summit-NY-2022/media/libraries/exhibitors/0b84f0a6-3bbd-11ee-bff906bd0f937899-cover-image.png" 
    style="width: 900px; height: auto;">
    ''',
    unsafe_allow_html=True
)

st.markdown('# Bem vindo ao Chat Bot GROQ!',)

hide_default_format = """
       <style>
       #MainMenu {visibility: hidden; }
       footer {visibility: hidden;}
       </style>
       """
st.markdown(hide_default_format, unsafe_allow_html=True)

load_dotenv()

try:
    llm = ChatGroq(
        model=filtro_modelo,
        temperature=temperature,
        top_p=top_p,
        max_tokens=max_length,
        streaming=True, 
        api_key=replicate_api 
    )
     
except GroqError:
    st.error("Por favor, insira um token de API válido. Clique no botão para abrir uma conta na [GROQ](https://console.groq.com/keys) e obter um token.")


    # Create a ConversationEntityMemory object if not already created
if 'entity_memory' not in st.session_state:
    st.session_state.entity_memory = ConversationEntityMemory(llm=llm, k=100)
        
        # Create the ConversationChain object with the specified configuration
        
Conversation = ConversationChain(
            llm=llm, 
            prompt=ENTITY_MEMORY_CONVERSATION_TEMPLATE,
            memory=st.session_state.entity_memory,
            verbose=True,
    
        ) 


# Get the user input
#user_input = get_text()

user_input = st.chat_input("Sou seu assistente. Como posso ajudá-lo?")


# Generate the output using the ConversationChain object and the user input, and add the input/output to the session
if user_input:
    with st.chat_message("assistant"):
        output = Conversation.run(input=user_input)  
        st.session_state.past.append(user_input)  
        st.session_state.generated.append(output) 
       
  

# Allow to download as well
download_str = []
# Display the conversation history using an expander, and allow the user to download it
with st.expander("Conversation", expanded=True):
    #for i in range(len(st.session_state['generated'])-1, -1, -1):
    for i in range(len(st.session_state['generated'])):
        st.info(st.session_state["past"][i],icon="🧐")
        st.success(st.session_state["generated"][i], icon="🤖")
        download_str.append(st.session_state["past"][i])
        download_str.append(st.session_state["generated"][i])
                            
    # Can throw error - requires fix
    download_str = '\n'.join(download_str)
    
    ##col1, col2, _ = st.columns(3)
       # col1.download_button('Download', download_str)  
        #col2.download_button('Download Markdown', download_str, file_name='documento.md', mime='text/markdown')
    
    if download_str:
        col1, col2 = st.columns([1, 4])  # ajusta o tamanho das colunas
        col1.download_button('Download Text', download_str)  
        col2.download_button('Download Markdown', download_str, file_name='documento.md', mime='text/markdown')
            


# Allow the user to clear all stored conversation sessions
# Add a button to start a new chat
st.sidebar.button("Limpar Chat", on_click = new_chat, type='primary')

st.sidebar.markdown("---")

st.sidebar.markdown("<h1 style='text-align: ; color: black;'>Contatos</h1>", unsafe_allow_html=True)
# Usando HTML para exibir os botões lado a lado
st.sidebar.markdown("""
    <div style="display: inline-block; margin-right: 10px;">
        <a href="https://github.com/jeferson100">
            <img src="https://img.shields.io/badge/github-100000?style=for-the-badge&logo=github">
        </a>
    </div>
    <div style="display: inline-block;">
        <a href="https://www.linkedin.com/in/jefersonsehnem/">
            <img src="https://img.shields.io/badge/linkedin-0077b5?style=for-the-badge&logo=linkedin&logocolor=white">
        </a>
    </div>
""", unsafe_allow_html=True) 

