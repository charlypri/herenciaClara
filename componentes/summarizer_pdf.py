# Streamlit library, used to create the user interface for the application.
import streamlit as st

# Module from the Langchain library that provides embeddings for text processing using OpenAI language models.
from langchain.embeddings.openai import OpenAIEmbeddings

# Python built-in module for handling temporary files.
import tempfile

# Python built-in module for time-related operations.
import time

# Below are the classes from the Langchain library
from langchain import OpenAI, PromptTemplate, LLMChain

# class from the Langchain library that splits text into smaller chunks based on specified parameters.
from langchain.text_splitter import CharacterTextSplitter

# This is a class from the Langchain library that loads PDF documents and splits them into pages.
from langchain.document_loaders import PyPDFLoader

# This is a function from the Langchain library that loads a summarization chain for generating summaries.
from langchain.chains.summarize import load_summarize_chain

# This is a class from the Langchain library that represents a document.
from langchain.docstore.document import Document

# This is a class from the Langchain library that provides vector indexing and similarity search using FAISS.
from langchain.vectorstores import FAISS

# This is a function from the Langchain library that loads a question-answering chain for generating answers to questions.
from langchain.chains.question_answering import load_qa_chain

import streamlit_analytics

from dotenv import load_dotenv
import os

load_dotenv()
OPEN_AI_API_KEY = os.environ["OPEN_AI_API_KEY"]

llm = OpenAI(openai_api_key=OPEN_AI_API_KEY, temperature=0)

# We need to split the text using Character Text Split such that it should not increase token size
text_splitter = CharacterTextSplitter(
    separator="\n",
    chunk_size=800,
    chunk_overlap=200,
    length_function=len,
)


def get_single_page_summary(page_number, pages):
    view = pages[page_number - 1]
    texts = text_splitter.split_text(view.page_content)
    docs = [Document(page_content=t) for t in texts]
    chain = load_summarize_chain(llm, chain_type="map_reduce", verbose=True)
    summaries = chain.run(docs)

    return summaries


def get_multiple_page_summary(start_page, end_page, pages):
    texts = []
    for page_number in range(start_page, end_page + 1):
        view = pages[page_number - 1]
        page_texts = text_splitter.split_text(view.page_content)
        texts.extend(page_texts)
    docs = [Document(page_content=t) for t in texts]
    chain = load_summarize_chain(llm, chain_type="map_reduce")
    summaries = chain.run(docs)

    return summaries


def get_multiple_page_summary(pages):
    combined_content = "".join(
        [p.page_content for p in pages]
    )  # we get entire page data
    texts = text_splitter.split_text(combined_content)
    docs = [Document(page_content=t) for t in texts]
    chain = load_summarize_chain(llm, chain_type="map_reduce")
    summaries = chain.run(docs)

    return summaries


def ask_the_document(pages, question):
    combined_content = "".join([p.page_content for p in pages])
    texts = text_splitter.split_text(combined_content)
    embedding = OpenAIEmbeddings(openai_api_key=OPEN_AI_API_KEY)
    document_search = FAISS.from_texts(texts, embedding)
    chain = load_qa_chain(llm, chain_type="stuff")
    docs = document_search.similarity_search(question)
    summaries = chain.run(input_documents=docs, question=question)


def pdf_smmarizer_component():
    streamlit_analytics.start_tracking()
    st.title("¿Dudas sobre tu PDF? Preguntale a nuestra IA")
    pdf_file = st.file_uploader("Elige un archivo PDF", type="pdf")

    if pdf_file is not None:
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            tmp_file.write(pdf_file.read())
            pdf_path = tmp_file.name
            loader = PyPDFLoader(pdf_path)
            pages = loader.load_and_split()

        # User input for page selection
        page_selection = st.radio(
            "Selecciona las páginas que quieras analizar",
            [
                "Una única pagina",
                "Un rango de páginas",
                "Resumen General",
                "Quiero hacer una pregunta concreta",
            ],
        )

        with st.form("myform", clear_on_submit=True):
            if page_selection == "Una única pagina":
                page_number = st.number_input(
                    "Elíge que página quieres analizar",
                    min_value=1,
                    max_value=len(pages),
                    value=1,
                    step=1,
                )
                submitted = st.form_submit_button(
                    "Enviar", disabled=not (page_selection)
                )
                if pdf_file and submitted:
                    summaries = get_single_page_summary(page_number, pages)

                    st.subheader("Summary")
                    st.write(summaries)

            elif page_selection == "Un rango de páginas":
                start_page = st.number_input(
                    "selecciona página inicial",
                    min_value=1,
                    max_value=len(pages),
                    value=1,
                    step=1,
                )
                end_page = st.number_input(
                    "selecciona página final",
                    min_value=start_page,
                    max_value=len(pages),
                    value=start_page,
                    step=1,
                )
                submitted = st.form_submit_button(
                    "Enviar", disabled=not (page_selection)
                )
                if pdf_file and submitted:
                    summaries = get_multiple_page_summary(start_page, end_page, pages)

                    st.subheader("Summary")
                    st.write(summaries)

            elif page_selection == "Resumen General":
                submitted = st.form_submit_button(
                    "Enviar", disabled=not (page_selection)
                )
                if pdf_file and submitted:
                    summaries = get_multiple_page_summary(pages)
                    st.subheader("Summary")
                    st.write(summaries)

            elif page_selection == "Quiero hacer una pregunta concreta":
                question = st.text_input(
                    "Introduce tu pregunta",
                    value="Quienes son los herederos directos segun este testamento?",
                )
                submitted = st.form_submit_button(
                    "Enviar", disabled=not (page_selection)
                )
                if pdf_file and submitted:
                    summaries = ask_the_document(pages, question)
                    st.write(summaries)

    streamlit_analytics.stop_tracking(
        unsafe_password="test123", save_to_json="analytics/data.json"
    )
