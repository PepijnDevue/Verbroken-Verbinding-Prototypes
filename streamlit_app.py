import threading

import streamlit as st
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    TextIteratorStreamer,
    GenerationConfig,
)

# ---- Utilities and caching ----

@st.cache_resource(show_spinner=False)
def load_tokenizer(model_id):
    tokenizer = AutoTokenizer.from_pretrained(model_id, use_fast=True)
    return tokenizer

@st.cache_resource(show_spinner=False)
def load_model(model_id, use_8bit=False):
    """Load model with sensible device placement and optional 8-bit.

    This uses transformers' device_map="auto" which with accelerate will
    place layers across all available devices. If no GPU is present this falls
    back to CPU.
    """
    # prefer safe defaults; allow quantized if bitsandbytes is available
    kwargs = {
        "device_map": "auto",
        "torch_dtype": None,
    }

    if use_8bit:
        kwargs["load_in_8bit"] = True

    model = AutoModelForCausalLM.from_pretrained(
        model_id,
        **kwargs,
    )
    model.eval()
    return model

# ---- Generation helpers ----

def build_prompt(system_prompt, user_prompt):
    """Combine system and user prompts with clear separation for models that
    expect a system message followed by the user's text.
    """
    if system_prompt:
        return f"<|SYSTEM|>\n{system_prompt}\n<|END_SYSTEM|>\n\n{user_prompt}"
    return user_prompt


def stream_generate(model, tokenizer, prompt, gen_kwargs, placeholder):
    """Run generation using TextIteratorStreamer to stream output into Streamlit.

    This function spawns a thread that runs model.generate and iterates over the
    streamer to update the given placeholder in the Streamlit app.
    """
    streamer = TextIteratorStreamer(tokenizer, skip_prompt=True, timeout=10.0)

    inputs = tokenizer(prompt, return_tensors="pt")

    # move inputs to model device(s)
    device = next(model.parameters()).device
    inputs = {k: v.to(device) for k, v in inputs.items()}

    gen_kwargs_local = dict(
        inputs, streamer=streamer, **gen_kwargs
    )

    def generate_thread():
        try:
            model.generate(**gen_kwargs_local)
        except Exception as e:
            # send an error token sequence through streamer by writing to placeholder
            placeholder.error(f"Generation failed: {e}")

    thread = threading.Thread(target=generate_thread)
    thread.start()

    # consume streamer
    collected = ""
    for new_text in streamer:
        collected += new_text
        placeholder.markdown(collected)
    thread.join()

# ---- Streamlit UI ----

def main():
    st.set_page_config(page_title="HF Streamlit Inference", layout="wide")

    st.title("Hugging Face — Streamlit Inference Prototype")

    with st.sidebar:
        st.header("Model & Settings")
        model_id = st.text_input("Model repo id", value="microsoft/Phi-4-mini-instruct")
        use_8bit = st.checkbox("Attempt 8-bit load (bitsandbytes)", value=False)
        max_new_tokens = st.number_input("Max new tokens", min_value=1, max_value=4096, value=256)
        temperature = st.slider("Temperature", min_value=0.0, max_value=2.0, value=0.7)
        top_k = st.number_input("Top-k", min_value=0, max_value=1000, value=50)
        top_p = st.slider("Top-p (nucleus)", min_value=0.0, max_value=1.0, value=0.95)
        do_stream = st.checkbox("Stream output", value=True)

    st.sidebar.markdown("---")
    st.sidebar.caption("Model loads are cached. Changing the model id forces a reload.")

    st.subheader("Prompts")
    system_prompt = st.text_area("System prompt (short)", height=120)
    user_prompt = st.text_area("User prompt", height=200)

    start_btn = st.button("Generate")

    placeholder = st.empty()

    if start_btn:
        with st.spinner("Loading tokenizer and model (cached when possible)..."):
            tokenizer = load_tokenizer(model_id)
            model = load_model(model_id, use_8bit=use_8bit)

        prompt = build_prompt(system_prompt, user_prompt)

        gen_cfg = GenerationConfig(
            max_new_tokens=int(max_new_tokens),
            temperature=float(temperature),
            top_k=int(top_k),
            top_p=float(top_p),
            do_sample=True,
        )

        gen_kwargs = dict(
            generation_config=gen_cfg,
        )

        # progress placeholder
        output_placeholder = placeholder.container()

        if do_stream:
            output_placeholder.markdown("")
            stream_generate(model, tokenizer, prompt, gen_kwargs, output_placeholder)
        else:
            # synchronous generate
            try:
                inputs = tokenizer(prompt, return_tensors="pt")
                device = next(model.parameters()).device
                inputs = {k: v.to(device) for k, v in inputs.items()}
                with st.spinner("Generating..."):
                    output_ids = model.generate(**inputs, **gen_kwargs)
                output = tokenizer.decode(output_ids[0], skip_special_tokens=True)
                output_placeholder.markdown(output)
            except Exception as e:
                st.error(f"Generation failed: {e}")


if __name__ == "__main__":
    main()