import os
from dotenv import load_dotenv
from openai import OpenAI
import streamlit as st

# MUST be the first Streamlit command
st.set_page_config(page_title="SAT Math Agent", layout="centered")

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))



SYSTEM_PROMPT = """
You are an expert SAT math tutor and content creator.
1. Read the user's SAT math question.
2. Identify the topic and key idea.
3. Solve it step by step, showing all important algebra and reasoning.
4. At the end, clearly state the final answer.
5. Then create a short TikTok-style explanation under 120 words, with a hook in the first sentence.
Format your response as:

[WRITTEN_SOLUTION]
...steps...

[TIKTOK_SCRIPT]
...short script...
"""

#st.set_page_config(page_title="SAT Math Agent", layout="centered")

st.title("📘 SAT Math Agent")
st.write("Paste any SAT math question and get a full solution + TikTok script.")

question = st.text_area("Enter SAT Math Question", height=150)

if st.button("Solve"):
    if not question.strip():
        st.warning("Please enter a question first.")
    else:
        with st.spinner("Thinking..."):
            completion = client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": question}
                ],
                temperature=0.2,
            )
            output = completion.choices[0].message.content

        # Split into sections
        written, tiktok = output.split("[TIKTOK_SCRIPT]")

        written = written.replace("[WRITTEN_SOLUTION]", "").strip()
        tiktok = tiktok.strip()

        st.subheader("📝 Written Solution")
        st.write(written)

        st.subheader("🎬 TikTok Script")
        st.write(tiktok)
