from typing import List, Dict
from langchain.llms import LlamaCpp
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from ..config import MODEL_PATH, TEMPERATURE, MAX_TOKENS

class LLMManager:
    def __init__(self):
        self.llm = LlamaCpp(
            model_path=MODEL_PATH,
            temperature=TEMPERATURE,
            max_tokens=MAX_TOKENS,
            n_ctx=2048,
            verbose=False
        )

        self.qa_template = """
        Context information is below.
        ---------------------
        {context}
        ---------------------
        Given the context information and not prior knowledge, answer the question: {question}
        Answer:"""

        self.qa_prompt = PromptTemplate(
            input_variables=["context", "question"],
            template=self.qa_template
        )

        self.qa_chain = LLMChain(llm=self.llm, prompt=self.qa_prompt)

    def generate_response(self, question: str, context_docs: List[Dict]) -> str:
        """Generate a response based on the question and context documents."""
        context = "\n".join(doc['content'] for doc in context_docs)
        
        response = self.qa_chain.run(
            context=context,
            question=question
        )
        
        return response.strip()