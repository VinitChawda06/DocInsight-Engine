from typing import List, Dict
from langchain_community.llms import LlamaCpp
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from ..config import MODEL_PATH, TEMPERATURE, MAX_TOKENS

class LLMManager:
    def __init__(self):
        self._llm = None
        self._qa_chain = None
        
        self.qa_template = """
        Answer the following question based on the given context. Be concise and avoid repetition.
        If the context doesn't contain relevant information, say so.

        Context:
        {context}

        Question: {question}
        Answer:"""

        self.qa_prompt = PromptTemplate(
            input_variables=["context", "question"],
            template=self.qa_template
        )

    @property
    def llm(self):
        if self._llm is None:
            self._llm = LlamaCpp(
                model_path=MODEL_PATH,
                temperature=TEMPERATURE,
                max_tokens=MAX_TOKENS,
                n_ctx=2048,
                n_gpu_layers=1,
                verbose=False
            )
        return self._llm

    @property
    def qa_chain(self):
        if self._qa_chain is None:
            self._qa_chain = LLMChain(llm=self.llm, prompt=self.qa_prompt)
        return self._qa_chain

    def generate_response(self, question: str, context: str) -> str:
        """Generate a response based on the question and context string."""
        try:
            response = self.qa_chain.invoke({
                "context": context,
                "question": question
            })
            return response["text"].strip()
        except Exception as e:
            return f"Error generating response: {str(e)}"