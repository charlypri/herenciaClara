import streamlit as st
import random
import time
import openai

from dotenv import load_dotenv
import os

load_dotenv()
OPEN_AI_API_KEY = os.environ["OPEN_AI_API_KEY"]


def calculate_cost(json_data):
    total_tokens = 0

    for message in json_data["messages"]:
        content = message["content"]
        tokens = len(content.split())  # Counting tokens by splitting on spaces
        total_tokens += tokens

    cost = total_tokens * 0.002 / 1000
    print(f"total tokens {total_tokens}")
    return cost


def chatbot_component():
    st.title("Habla con nuestra IA experta")

    openai.api_key = OPEN_AI_API_KEY
    # Add a reset button
    if st.button("Reiniciar el Chat"):
        st.session_state["messages"] = []

    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = "gpt-3.5-turbo"

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("¿En que te puedo ayudar?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            for response in openai.ChatCompletion.create(
                model=st.session_state["openai_model"],
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                stream=True,
            ):
                full_response += response.choices[0].delta.get("content", "")
                message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
        st.write(
            f"El coste de la conversación es de {calculate_cost(st.session_state):.07f} euros"
        )

        st.session_state.messages.append(
            {"role": "assistant", "content": full_response}
        )

        # st.write(st.session_state)
