from vector_store.query_vector_store import query_similar_documents, query_financial_data, query_from_multiple_sheets
from prompts.prompt_builder import build_prompt
from openai import OpenAI
from bot_config.config import openai_api_key

client = OpenAI(api_key=openai_api_key)

def ask(question):
    context_docs = query_similar_documents(question)
    context_data = query_from_multiple_sheets(question)
    # context_data = query_financial_data(question)
    all_context = context_docs + context_data

    prompt = build_prompt(question, all_context)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are Puppy – a Business Intelligence Assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content.strip()

    # content = response.choices[0].message.content
    # if content is None:
    #     return "Sorry, I couldn't generate a response."
    # return content.strip()
