import streamlit as st
from transformers import pipeline

# TODO
# - Dit voorbeeld uitwerken
# - Met vscode devcontainer werken (intellicode)

st.title("VV Prototype: Docker + Streamlit + Hugging Face Transformers")

st.info("Runs a local transformers pipeline. This can be heavy; small models are recommended.")

model = st.text_input("Local model (e.g. google/flan-t5-small, gpt2)", "google/flan-t5-small")

system_prompt = st.text_area("System prompt (instructions for the model)", "You are a helpful assistant.")
user_input = st.text_area("User input (the text to send to the model)")

max_tokens = st.number_input("Max new tokens", min_value=16, max_value=2048, value=128, step=16)

if st.button("Run"):
    if not user_input.strip():
        st.error("Provide user input.")
    else:
        prompt = system_prompt.strip() + "\n\n" + user_input.strip()
        
        try:
            gen = pipeline("text2text-generation", model=model)  # uses text2text for flan/t5; gpt2 will need text-generation
        except Exception:
            gen = pipeline("text-generation", model=model)

        out = gen(prompt, max_new_tokens=int(max_tokens), do_sample=False)

        # pipeline returns list of outputs
        text_out = ""
        if isinstance(out, list) and out:
            # common formats: [{"generated_text": "..."}] or [{"summary_text": "..."}]
            first : str | dict | list = out[0]
            text_out = first.get("generated_text") or first.get("summary_text") or str(first)
        else:
            text_out = str(out)
        st.subheader("Model output")
        st.code(text_out)
