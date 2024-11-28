import streamlit as st
from pathlib import Path
import tempfile
from app.core.query_engine import QueryEngine
from app.config import RAW_DATA_DIR

class DocumentInsightApp:
    def __init__(self):
        st.set_page_config(
            page_title="DocInsight Engine",
            layout="wide",
            initial_sidebar_state="collapsed"
        )
        
        # Initialize query engine only when needed
        self._query_engine = None

    @property
    def query_engine(self):
        if 'query_engine' not in st.session_state:
            with st.spinner("Initializing system..."):
                st.session_state.query_engine = QueryEngine()
        return st.session_state.query_engine

    def run(self):
        st.title("📚 DocInsight Engine")
        
        # Initialize session state
        if 'processed_files' not in st.session_state:
            st.session_state.processed_files = set()
        
        # Create tabs for better organization
        upload_tab, query_tab = st.tabs(["📄 Upload Documents", "❓ Ask Questions"])
        
        with upload_tab:
            self.render_upload_section()
            
        with query_tab:
            self.render_query_section()

    def render_upload_section(self):
        if st.session_state.processed_files:
            with st.expander("View Processed Documents", expanded=True):
                for doc in st.session_state.processed_files:
                    st.write(f"- {doc}")

        uploaded_files = st.file_uploader(
            "Upload PDF documents",
            type="pdf",
            accept_multiple_files=True
        )

        if uploaded_files:
            for uploaded_file in uploaded_files:
                if uploaded_file.name not in st.session_state.processed_files:
                    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
                        tmp_file.write(uploaded_file.read())
                        tmp_path = Path(tmp_file.name)
                    
                    with st.spinner(f'Processing {uploaded_file.name}...'):
                        self.query_engine.add_document(tmp_path)
                    st.session_state.processed_files.add(uploaded_file.name)
                    st.success(f"Successfully processed {uploaded_file.name}")
                else:
                    st.info(f"{uploaded_file.name} already processed")

    def render_query_section(self):
        question = st.text_input("Enter your question about the documents:")
        
        if question:
            if not st.session_state.processed_files:
                st.warning("Please upload some documents first!")
                return
                
            with st.spinner('Generating response...'):
                response = self.query_engine.query(question)
                st.write("Answer:", response)

if __name__ == "__main__":
    app = DocumentInsightApp()
    app.run()