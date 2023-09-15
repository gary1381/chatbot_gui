# encoding: utf-8
# A bare bones UI for chatbot using LLAMA-2 or other LLM
# Created by Gary Xiao

import streamlit as st
import json
import requests
# from streamlit_chat import message

# Set up Session State
if "messages" not in st.session_state:
    st.session_state["messages"] = []
if "primer" not in st.session_state:
    st.session_state["primer"] = "You are a friendly and helpful assistant."
if "context_length" not in st.session_state:
    st.session_state["context_length"] = 10


def main():
    # Initialization your state messages

    # st.sidebar.header("Settings")

    # with st.sidebar:
    #     # Allow the user to set their prompt
    #     st.session_state.primer = st.text_area(
    #         "Primer Message",
    #         "You are a friendly and helpful assistant.",
    #     )
    #     st.session_state.context_length = st.slider(
    #         "Context Message Length", min_value=10, max_value=1000, value=300, step=10
    #     )

    #     # Allow Users to reset the memory
    #     if st.button("New Chat"):
    #         st.session_state.messages = []
    #         st.info("Chat Memory Cleared. New chat session is initiated.")

    # A place to draw the chat history
    history = st.container()

    # Change this url if it is changed
    # url = 'https://ec3f-35-243-134-196.ngrok.io/chatbot'
    url = "https://3b7d-35-197-144-204.ngrok.io/chatbot_qa"


    with st.form("Chat"):
        input = st.text_input("You:", "")
        if st.form_submit_button():
            st.session_state.messages.append({"role": "user", "content": input})

            # Create an on the fly message stack
            messages = [{"role": "system", "content": st.session_state.primer}]
            messages.extend(
                st.session_state.messages[-st.session_state.context_length :]
            )

            data = {
            'llm' : "llama-7b-chat",
            'temperature' : 0.3,
            'top_k' : 3,
            'prompt' : input,
            # "usage" : {"total_tokens": 300}
            # "content" : input
            }

            # input_data_for_model = {
            #  'prompt' : "Tell me something about Bluestem Brands."
            # }

            # json object
            # r = json.loads(json.dumps(r))

            data_json = json.dumps(data)

             # r = requests.post(url, data=r)
            response = requests.request("post", url, data=data_json)

            print("response_data 1: ", response)
            try:
                r = response.json()
                # r = json.loads(response["text"].decode("utf-8"))
                print("response_data 2: ", r)
            except Exception as e:
                print(e)
                r = response.decode()
                # r = response.json()
                print("response_data 2: ", r)

            st.session_state.messages.append(
                # {"role": "assistant", "content": r["choices"][0]["message"]["content"]}
                 {"role": "assistant", "content": r["text"]}
            )

    # display message history
    with history:
        messages = st.session_state.get('messages', {"content": ""})
        for i, msg in enumerate(messages[:]):
            # print("i, msg: ", i, msg)
            if i % 2 != 0:
                with st.chat_message("user"):
                    st.markdown(f'{msg["content"]}')
                # message(msg["content"], is_user=True, key=str(i) + '_user')
            else:
                with st.chat_message("assistant"):
                    st.markdown(f'{msg["content"]}')
                # message(msg["content"], is_user=False, key=str(i) + '_ai')

# use streamlit_chat to set avatar styles:
# supported styles: https://www.dicebear.com/styles

# message(message, 
#             is_user=False, 
#             avatar_style="adventurer", # change this for different user icon
#             seed=123, # or the seed for different user icons
# )


st.title("Chatbot Demo for Bluestem Brands")

key = st.text_input("Your Password")
if (key == "hackathon") or (key=="Hackathon"):
    main()
    
else:
    st.error("Please input a valid password")
    
# main()

st.info("Created by Gary Xiao, Shawn Liu, Satyabrata Samal and Jixiong Han from CDS team of Bluestem Brands for Hackathon")