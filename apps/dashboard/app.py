import streamlit as st
import requests
import time

API_URL = "http://127.0.0.1:8000/moderate"
RESULT_URL = "http://127.0.0.1:8000/result/"

st.title("🛡️ Real-Time Content Moderation")

text = st.text_area("Enter text")

if st.button("Moderate"):
    if text:
        res = requests.post(API_URL, json={"text": text})
        data = res.json()

        request_id = data.get("request_id")

        st.info(f"Request ID: {request_id}")

        # 🔁 Polling loop
        for _ in range(10):
            time.sleep(2)

            result = requests.get(f"{RESULT_URL}{request_id}").json()

            if result.get("label") != "processing":
                st.success("Result Ready!")
                st.write(result)
                break
            else:
                st.warning("Still processing...")
    else:
        st.warning("Enter text")
