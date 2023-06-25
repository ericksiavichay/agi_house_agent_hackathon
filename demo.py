from io import StringIO
import streamlit as st

import openai

st.set_page_config(layout="wide")

st.sidebar.title("Navigation")
uploaded_file = st.sidebar.file_uploader("Upload a file")

form = st.sidebar.form(key="my_form")
instructions = form.text_input(
    "instruction",
    value="edit the code to add a new AI snake 3 and the snake 3 should follow the same rules as snake 2",
    key="instruction",
)
left, right = st.columns(2)
submit_button = form.form_submit_button(label="Submit")

code_template = """Here is the code:
<code>
{code}
</code>
"""
instruction_template = """Here is the instruction:
<instruction>
{instruction}
</instruction>"""


with left:
    if uploaded_file is not None:
        stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
        file_contents = stringio.read()
        st.markdown("### Original Code")
        st.code(file_contents)
    if submit_button:
        code_message = code_template.format(code=file_contents)
        instruction_message = instruction_template.format(instruction=instructions)
        assistant_message = """Here is the modified code:
<code>"""
        messages = [
            {
                "role": "system",
                "content": """YYou are an experienced programmer. You will be provided a code, and then you task is to modify the code based on the user instruction.""",
            },
            {"role": "user", "content": code_message},
            {"role": "user", "content": instruction_message},
            {"role": "assistant", "content": assistant_message},
        ]
        model_response = openai.ChatCompletion.create(
            model="gpt-4-0613",
            messages=messages,
            temperature=0,
            max_tokens=4096,
            stop="</code>",
        )
        result = model_response.choices[0]["message"]["content"]
        st.markdown("### New Code")
        st.code(result)

with right:
    # URL of the website you want to display
    website_url = "https://trinket.io/features/pygame"
    # Use the iframe HTML tag to embed the website
    st.markdown(
        f'<iframe src="{website_url}" width="1000" height="600"></iframe>',
        unsafe_allow_html=True,
    )
