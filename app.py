import streamlit as st
import os
# import google.generativeai as genai
from langchain_core.messages import SystemMessage, AIMessage, HumanMessage
from langchain_ollama import ChatOllama
from templates import teaching_templates,tutor_profiles
from dotenv import load_dotenv
load_dotenv()

ai_tutor_name_1 = "Urahara Kisuke"
ai_tutor_name_2 = "Kuchiki Byakuya"
ai_tutor_name_3 = "Yamamoto Genryusai"

# api_key = os.getenv("GOOGLE_API_KEY")
# genai.configure(api_key=api_key)

@st.cache_resource(show_spinner=True)
def load_model():
    model = ChatOllama(model='llama3.2:1b',base_url='http://localhost:11434')
    return model

ai_tutor = load_model()

def chatbot():
    st.title("AI Tutor")

    # Sidebar for Teaching Templates
    st.sidebar.title("List of Sensei")
    selected_template = st.sidebar.selectbox(
        "Choose Your Sensei:",
        list(teaching_templates.keys())
    )

    # sensei's
    profile = tutor_profiles[selected_template]
    st.sidebar.image(profile["image"], use_container_width=True)
    st.sidebar.markdown(f"**{selected_template}**")
    st.sidebar.markdown(profile["description"])

    # initializing chat history for all versions of tutors.
    if "history" not in st.session_state:
        st.session_state.history = {}

    if selected_template not in st.session_state.history:
        st.session_state.history[selected_template] = [SystemMessage(content=teaching_templates[selected_template])]
    st.session_state.messages = st.session_state.history[selected_template]

    # Display chat history
    for message in st.session_state.messages:
        if isinstance(message, AIMessage):
            with st.chat_message("assistant"):
                st.markdown(message.content)
        elif isinstance(message, HumanMessage):
            with st.chat_message("user"):
                st.markdown(message.content)

    # Chat input and response generation
    if prompt := st.chat_input("Ask your Question Here..."):
        st.session_state.messages.append(HumanMessage(content=prompt))
        with st.chat_message("user"):
            st.markdown(prompt)
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            try:
                # contents = [msg.content for msg in st.session_state.messages]
                tutor_response = ai_tutor.invoke(inputs=st.session_state.messages)
                full_response = tutor_response.content
                message_placeholder.markdown(full_response)
            except Exception as e:
                st.error(f"Oops!! An error occurred: {e}")
                full_response = "I apologize for the error that has been encountered."
                message_placeholder.markdown(full_response)
            st.session_state.messages.append(AIMessage(content=full_response))

chatbot()
