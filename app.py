import torch
import streamlit as st
from transformers import T5Tokenizer, T5ForConditionalGeneration

hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

st.title('Abstractive Text Summarization using NLP')
st.markdown('Powered by Think In Bytes')


_num_beams = 4
_no_repeat_ngram_size = 3
_length_penalty = 2
_min_length = 30
_max_length = 200
_early_stopping = True

text = st.text_area('Text Input')


def run_model(input_text):
    with st.spinner('Take a sip of your coffee, AI is extracting the summary..'):
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        t5_model = T5ForConditionalGeneration.from_pretrained("t5-base")
        t5_tokenizer = T5Tokenizer.from_pretrained("t5-base")
        input_text = str(input_text).replace('\n', '')
        input_text = ' '.join(input_text.split())
        input_tokenized = t5_tokenizer.encode(input_text, return_tensors="pt").to(device)
        summary_task = torch.tensor([[21603, 10]]).to(device)
        input_tokenized = torch.cat([summary_task, input_tokenized], dim=-1).to(device)
        summary_ids = t5_model.generate(input_tokenized,
                                    num_beams=_num_beams,
                                    no_repeat_ngram_size=_no_repeat_ngram_size,
                                    length_penalty=_length_penalty,
                                    min_length=_min_length,
                                    max_length=_max_length,
                                    early_stopping=_early_stopping)
        output = [t5_tokenizer.decode(g, skip_special_tokens=True, clean_up_tokenization_spaces=False) for g in summary_ids]
        st.write('Summary')
    st.success(output[0])


if st.button('Submit'):
    run_model(text)

col1, col2, col3 = st.columns(3)


center_header = """
<h2 style='text-align: center; color: red;'>Industry Applications</h2>
"""

st.markdown(center_header, unsafe_allow_html=True)

with col1:
   st.header("User sentiment Analysis")
   st.markdown("Want to understand your customers ? Let our AI Engine detect the sentiment of your user's comments and feedback in seconds")
   #st.image("https://static.streamlit.io/examples/cat.jpg")

with col2:
   st.header("Document summarization")
   st.markdown("Get the gist of your extensive research papers or news articles in just a paragraph of few lines. Our AI engine can abstractively summarise long text matters in seconds")
   #st.image("https://static.streamlit.io/examples/dog.jpg")

with col3:
   st.header("Image to Text")
   st.markdown("Tired of finding creative content for your ad posts ? Let our AI Engine find the best caption for your image. ")
   #st.image("https://static.streamlit.io/examples/owl.jpg")
