import os

import streamlit as st
from dotenv import load_dotenv
from groq import Groq
from loguru import logger

load_dotenv()

logger.info(os.getenv('GROQ_API_KEY'))

qclient = Groq()

st.title('Chat Electoral')

if 'messages' not in st.session_state:
    st.session_state.messages = []

for messages in st.session_state.messages:
    with st.chat_message(messages['role']):
        st.markdown(messages['content'])


def process_data(chat_completion) -> str:
    for chunk in chat_completion:
        if chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content

st.sidebar.header("Subir Archivo")
uploaded_file = st.sidebar.file_uploader("Elige un archivo (xlsx)", type=["xlsx"])

if prompt := st.chat_input('Insert questions'):
    with st.chat_message('user'):
        st.markdown(prompt)

    st.session_state.messages.append({'role': 'user', 'content': prompt})

    with st.chat_message('assistant'):
        
        stream_response = qclient.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "Eres un asistente electoral y te hare preuntas de las elecciones presidenciales de Ecuador"
,
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            model="mixtral-8x7b-32768",
            stream=True
        )

        response = process_data(stream_response)

        response = st.write_stream(response)

    st.session_state.messages.append({'role': 'asistant', 'content': response})
