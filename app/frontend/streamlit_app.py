import streamlit as st
from pathlib import Path
import tempfile
from app.core.query_engine import QueryEngine
from app.config import RAW_DATA_DIR

class DocumentInsightApp:
    def __init__(self):
        self.query_engine = QueryEngine()
        st.set_page_config(page_title="DocInsight Engine", layout="wide")

    def run(self):
        st.title("📚 DocInsight Engine")
        
        # Document upload section
        st.header("📄 Document Upload")
        uploaded_files = st.file_uploader(
            "Upload PDF documents", 
            type="pdf",
            accept_multiple_files=True
        )

        if uploaded_files:
            for uploaded_file in uploaded_files:
                with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
                    tmp_file.write(uploaded_file.read())
                    tmp_path = Path(tmp_file.name)
                
                with st.spinner(f'Processing {uploaded_file.name}...'):
                    self.query_engine.add_document(tmp_path)
                st.success(f"Successfully processed {uploaded_file.name}")

        # Query section
        st.header("❓ Ask Questions")
        question = st.text_input("Enter your question about the documents:")
        
        if question:
            with st.spinner('Generating response...'):
                response = self.query_engine.query(question)
                st.write(response)

if __name__ == "__main__":
    app = DocumentInsightApp()
    app.run()