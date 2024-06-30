# AIzaSyDWuTZF1d9dX_alGy0Gd_jkb9Mz-j508BY

import google.generativeai as genai
import os

def ask_gemini(question):
    genai.configure(api_key="AIzaSyBxJfF_KThZOUdzy_GBN1zOAABPd-n4rUc")

    model = genai.GenerativeModel('gemini-1.5-flash')
    chat = model.start_chat(history=[])

    response = chat.send_message(question)

    return(response.text)


