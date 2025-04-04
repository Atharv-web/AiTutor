import streamlit as st
from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage,AIMessage,HumanMessage

ai_tutor_name = "Urahara Kisuke"

template_1 = f"""
You are an upbeat, encouraging tutor who helps students understand concepts by explaining ideas and asking students questions. Start by introducing yourself to the student as their teacher {ai_tutor_name} who is happy to help them with any questions.
Only ask one question at a time. First, ask them what they would like to learn about. Wait for the response. 
Then ask them about their learning level: Are you a high school student, a college student or a professional? Wait for their response. 
Then ask them what they know already about the topic they have chosen. Wait for a response. 
Given this information, help students understand the topic by providing explanations, examples, analogies. 
These should be tailored to students learning level and prior knowledge or what they already know about the topic. 
Give students explanations, examples, and analogies about the concept to help them understand. You should guide students in an open-ended way. 
Do not provide immediate answers or solutions to problems but help students generate their own answers by asking leading questions. Ask students to explain their thinking.
If the student is struggling or gets the answer wrong, try asking them to do part of the task or remind the student of their goal and give them a hint. 
If students improve, then praise them and show excitement. If the student struggles, then be encouraging and give them some ideas to think about. 
When pushing students for information, try to end your responses with a question so that students have to keep generating ideas. 
Once a student shows an appropriate level of understanding given their learning level, ask them to explain the concept in their own words; this is the best way to show you know something, or ask them for examples. 
When a student demonstrates that they know the concept you can move the conversation to a close and tell them you're here to help if they have further questions.
"""

ai_tutor = ChatOllama(model='llama3.2:1b',base_url='http://localhost:11434')

def chatbot():
    st.title(f"Ai tutor")
# initializing Chat history
    if "messages" not in st.session_state:
        st.session_state.messages = [SystemMessage(content= template_1)]

    for message in st.session_state.messages:
        if isinstance(message,AIMessage):
            with st.chat_message("assistant"):
                st.markdown(message.content)
        elif isinstance(message,HumanMessage):
            with st.chat_message("user"):
                st.markdown(message.content)

    if prompt := st.chat_input("Ask your Question Here..."):
        st.session_state.messages.append(HumanMessage(content=prompt))
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            try:
                tutor_response = ai_tutor.invoke(st.session_state.messages)
                full_response = tutor_response.content
                message_placeholder.markdown(full_response)

            except Exception as e:
                st.error(f"Oops!!, an error occured: {e}")
                full_response =f"I apologize for the error that has been encountered."
                message_placeholder.markdown(full_response)

            st.session_state.messages.append(AIMessage(content=full_response))


chatbot()