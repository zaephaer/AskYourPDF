# Using Gemini
# Using text file as knowledge base
# Without ServiceContext and works with current LlamaIndex version

import os
import streamlit as st
#import openai
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, ServiceContext
import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI
import traceback

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def save_uploaded_file(uploadedfile):
    with open(os.path.join("data",uploadedfile.name),"wb") as f:
        f.write(uploadedfile.getbuffer())
    return st.success("File uploaded successfully in data directory")

# Get a list of PDF files from the dedicated directory
pdf_dir = "data"
pdf_files = [file for file in os.listdir(pdf_dir) if file.lower().endswith(".pdf")]

st.set_page_config(page_title="Ask PDF", page_icon=":house:", layout="wide")

with st.sidebar:
        # About the app with Extender
        st.expander("About").write("This is a simple web app that enables you to upload a PDF file and ask questions from it.")
        # Upload PDF file
        datafile = st.file_uploader("Upload PDF File",type=['pdf'])
        if datafile is not None:
            file_details = {"FileName":datafile.name,"FileType":datafile.type}
            save_uploaded_file(datafile)   
            # Refresh button
            st.button("Refresh")     
        # Display a list of PDF files as radio buttons in the sidebar
        selected_file = st.radio("Select file and click Remove File button if you want to remove it:", pdf_files, index=0)
        st.success(selected_file)
        # Button remove file from folder
        if st.button("Remove File"):
            os.remove(os.path.join(pdf_dir, selected_file))
            st.rerun()

# Simple Streamlit app
st.title("Upload and Ask your PDF")
query = st.text_area("Enter your question")

# If submit button click
if st.button("Submit"):
    if not query.strip():
        st.error("Please enter a query")
    else:
        try:
            # Define custom LLM Model
            llm = ChatGoogleGenerativeAI(model="gemini-pro",temperature=0.7)
            # Load documents from directory name 'data'
            documents = SimpleDirectoryReader('data').load_data()
            # Build Index
            index = VectorStoreIndex.from_documents(documents)
            query_engine = index.as_query_engine()
            response = query_engine.query(query)
            st.success(response)
        except Exception as e:
            st.error(f"Error occurred: {e}")
            st.error(traceback.format_exc())
