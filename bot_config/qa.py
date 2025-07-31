
# from openai import OpenAI
# from config import openai_api_key
# from bot_config.vector_store import query_similar_documents

# client = OpenAI(api_key=openai_api_key)

# def build_prompt(question):
#     relevant_chunks = query_similar_documents(question)
#     context = "\n\n".join(relevant_chunks)
#     return f"""
# Bạn là Meoz - trợ lý BI thân thiện.
# Hãy trả lời câu hỏi dựa trên thông tin sau:

# --- Kiến thức nội bộ ---
# {context}

# --- Câu hỏi ---
# {question}
# """

# def ask(question):
#     prompt = build_prompt(question)
#     print("\n===== PROMPT GỬI GPT =====\n")
#     print(prompt[:1500])
#     print("==========================\n")

#     response = client.chat.completions.create(
#         model="gpt-4o-mini",
#         messages=[
#             {"role": "system", "content": "You are Meoz - BI Assistant."},
#             {"role": "user", "content": prompt}
#         ]
#     )
#     return response.choices[0].message.content.strip()

from openai import OpenAI
from config import openai_api_key
from bot_config.vector_store import query_similar_documents

client = OpenAI(api_key=openai_api_key)

def build_prompt(question):
    relevant_chunks = query_similar_documents(question)

    if not relevant_chunks:
        return f"""
            You are Meoz – a friendly BI assistant at Yes4All.

            Unfortunately, there is no relevant internal context available for your question at the moment.
            Please provide more details or rephrase your question so I can assist you better. Alternatively, if this question requires support from another department, I can help you connect.
        --- Question ---
        {question}
        """
    
## You are Meoz - BI Assistant.
## Currently, you do not have any internal data related to the following question. Please respond politely or suggest the user provide more information:/

    context = "\n\n".join(relevant_chunks)
    return f"""
        You are Meoz – a helpful and professional Business Intelligence assistant at Yes4All.
        
        **1. Answer based on internal data:** 
        When the question relates to internal company information, please answer strictly based on the context below. 
        Do not assume or make up information. If the answer is unclear, kindly ask the user for more details or guide them to the appropriate department.

        **2. Answering other questions:** 
        For questions outside of internal company data, you can answer based on your general knowledge while maintaining a professional and neutral tone.

        **Tone and Style:** 
        Keep responses clear, concise, and polite. Avoid using overly technical language or sounding too rigid. 

        **Citing Sources:** 
        If possible, cite the source from the internal knowledge base (reference the text provided) to clarify the answer.

        --- Base Knowledge ---
        {context}

        --- Question ---
        {question}
    """
# You are Meoz - BI Assistant.
# Base on the internal information below, please answer the question concisely, accurately, and understandably, sticking closely to the provided content. Do not make excessive assumptions.
#
# 1. If the question is about Yes4All, your goal is to answer user questions strictly based on the provided internal company knowledge.
# Only use information found in the context below. Do not assume or make up information. 
# If the answer is unclear or not found in the context, respond politely asking the user for clarification or to contact the appropriate department. 
# Always answer in a clear, concise, and professional tone. You may cite the source if relevant.
# 2. Other questions, you can answer based on your knowledge, with professional tone.

# Base on the internal information below, please answer the question concisely, accurately, and understandably, sticking closely to the provided content. Do not make excessive assumptions.


def ask(question):
    prompt = build_prompt(question)
    print("\n===== PROMPT GỬI GPT =====\n")
    print(prompt[:1500])
    print("==========================\n")

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are Meoz - BI Assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content.strip()
