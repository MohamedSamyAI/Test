import streamlit as st
from langchain_community.document_loaders import PDFPlumberLoader
import tempfile

def process_pdf(file_path):
    """
    Uses PDFPlumberLoader to load and extract text from the PDF.
    Accepts either a URL string or a local file path.
    """
    loader = PDFPlumberLoader(file_path)
    documents = loader.load()
    # Join all pages' content into one string
    pages = "\n".join([page.page_content for page in documents])
    return pages

# App title and description
st.title("PDF Text Extractor")
st.write("Extract text from a PDF by entering a URL or uploading a file.")

# Choose input type: URL or file upload
input_type = st.radio("Select input type", ("URL", "Upload File"))

if input_type == "URL":
    url = st.text_input("Enter the PDF URL")
    if st.button("Extract Text") and url:
         with st.spinner("Processing URL..."):
             text = process_pdf(url)
         st.subheader("Extracted Text")
         st.text_area("", text, height=400)
         
elif input_type == "Upload File":
    uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])
    if uploaded_file is not None:
         # Save the uploaded file temporarily and extract its text
         with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
             tmp_file.write(uploaded_file.read())
             tmp_file_path = tmp_file.name
         with st.spinner("Processing file..."):
             text = process_pdf(tmp_file_path)
         st.subheader("Extracted Text")
         st.text_area("", text, height=400)
