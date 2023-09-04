# A bare bones UI for chatbot using LLAMA-2 or other LLM
# Created by Gary Xiao

# import openai
import streamlit as st
import json
import requests
from streamlit_chat import message

# Set up Session State
if "messages" not in st.session_state:
    st.session_state["messages"] = []
if "primer" not in st.session_state:
    st.session_state["primer"] = "You are a friendly and helpful assistant."
if "context_length" not in st.session_state:
    st.session_state["context_length"] = 10


def main():
    # Initialization your state messages

    st.sidebar.header("Settings")

    with st.sidebar:
        # Allow the user to set their prompt
        st.session_state.primer = st.text_area(
            "Primer Message",
            "You are a friendly and helpful assistant.",
        )
        st.session_state.context_length = st.slider(
            "Context Message Length", min_value=10, max_value=1000, value=300, step=10
        )

        # Allow Users to reset the memory
        if st.button("New Chat"):
            st.session_state.messages = []
            st.info("Chat Memory Cleared. New chat session is initiated.")

    # A place to draw the chat history
    history = st.container()

    url = 'https://ef9b-34-126-178-0.ngrok.io/chatbot'


    with st.form("Chat"):
        input = st.text_input("You:", "")
        if st.form_submit_button():
            st.session_state.messages.append({"role": "user", "content": input})

            # Create an on the fly message stack
            messages = [{"role": "system", "content": st.session_state.primer}]
            messages.extend(
                st.session_state.messages[-st.session_state.context_length :]
            )

            # Call the OpenAI API
            # r = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
            r = {
            'llm' : "llama-7b-chat",
            'temperature' : 0.3,
            'top_k' : 3,
            'prompt' : input,
            "usage" : {"total_tokens": 300}
            # "content" : input
            }

            # input_data_for_model = {
            #  'prompt' : "Tell me something about Bluestem Brands."
            # }

            # json object
            # r = json.loads(json.dumps(r))

            r = json.dumps(r)

            r = requests.post(url, data=r)
            r = r.json()
            print("response_data: ", r)

            # print("r from llm: ", r)
            # print("tyep of r: ", type(r))
            # print(f'r["usage"]', r["usage"])
            
            # print(f'r["usage"]["total_tokens"]', r["usage"]["total_tokens"])

            # tokens = r["usage"]["total_tokens"]
            # cost = round((tokens / 1000) * 0.00, 3)
            # st.info(f"Message uses {tokens} tokens for a total cost of {cost} cents")

            # this will create additional container below the input area.
            # with st.expander("Result"):
            #     st.info("Your Output Response")
            #     st.write(r)

            st.session_state.messages.append(
                # {"role": "assistant", "content": r["choices"][0]["message"]["content"]}
                 {"role": "assistant", "content": r["content"]}
            )

    # with history:
    #     for i, message in enumerate(st.session_state.messages):
    #         # c1, c2 = st.columns([2, 10])
    #         print("st.columns: ", st.columns)

    #         # with c1:
           
    #         with st.chat_message("user"):
    #             st.write(message["role"])
    #         # with c2:
    #         with st.chat_message("assistant"):
    #             # Lets italisize the messages that are sent in the state
    #             if (
    #                 len(st.session_state.messages) - i
    #                 < st.session_state.context_length + 1
    #             ):
    #                 st.markdown(f'_{message["content"]}_')
    #             else:
    #                 st.markdown(f'{message["content"]}')

    # display message history
    with history:
        messages = st.session_state.get('messages', {"content": ""})
        for i, msg in enumerate(messages[:]):
            print("i, msg: ", i, msg)
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


st.title("GPT Demo for Bluestem Brands")

key = st.text_input("Your Password")
if key != "hackathon":
    st.error("Please input a valid password")

else:
    main()


st.info("Created by Gary Xiao, for hackathon at Bluestem Brands")