# AIzaSyDWuTZF1d9dX_alGy0Gd_jkb9Mz-j508BY

import google.generativeai as genai
import os

def ask_gemini(question):
    genai.configure(api_key="AIzaSyBt4sUTtKp0wRl_K48Gz_EcpWCUpxDhF9c")

    model = genai.GenerativeModel('gemini-1.5-flash')
    chat = model.start_chat(history=[])

    response = chat.send_message(question)

    return(response.text)


