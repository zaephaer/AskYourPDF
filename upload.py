import streamlit as st
import os
import pandas as pd

def save_uploaded_file(uploadedfile):
    with open(os.path.join("DataPath",uploadedfile.name),"wb") as f:
        f.write(uploadedfile.getbuffer())
    return st.success("File uploaded successfully in DataPath directory")

# Get a list of PDF files from the dedicated directory
pdf_dir = "DataPath"
pdf_files = [file for file in os.listdir(pdf_dir) if file.lower().endswith(".pdf")]

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
        selected_file = st.radio("Select file and click Remove File button to remove it:", pdf_files, index=0)
        st.success(selected_file)
        # Button remove file from folder
        if st.button("Remove File"):
            os.remove(os.path.join(pdf_dir, selected_file))
            st.rerun()