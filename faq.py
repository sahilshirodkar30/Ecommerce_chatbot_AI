import pandas as pd
from pathlib import Path
import chromadb
from chromadb.utils import embedding_functions
import os
from groq import Groq
from dotenv import load_dotenv
load_dotenv()


#Path(__file__).parent

faqs_path = Path(__file__).parent /"resources/faq_data.csv"
chroma_client = chromadb.Client()
collection_name_faq = "faq"
ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="sentence-transformers/all-MiniLM-L6-v2")
groq_client = Groq()


def ingest_faq_data(path):
    if collection_name_faq not in [c.name for c in chroma_client.list_collections()]:
        print("Ingesting faq data into chromadb ..")
        collection = chroma_client.get_or_create_collection(name=collection_name_faq, embedding_function=ef)
        df = pd.read_csv(path)
        docs = df['question'].tolist()
        metadatas = [{'answer': ans} for ans in df['answer'].tolist()]
        ids = [ f"id_{i}" for i in range(len(docs))]
        collection.add(
            documents=docs,
            metadatas=metadatas,
            ids=ids
        )
        print("Ingested faq data successfully into chromadb collection {collection_name_faq}")
    else:
        print("Collection {collection_name_faq} already exists")


def get_faq_answer(query):
    collection = chroma_client.get_collection(name=collection_name_faq ,embedding_function=ef)
    results = collection.query(
        query_texts=[query],
        n_results=2
    )
    return results


def generate_answer(query, context):
    prompt = f''' Given the following context and question, generate answer based on this context only.
    If the answer is not found in the context, kindly state "I don't know". Don't try to make up an answer.
    
    CONTEXT: {context}
    
    QUESTION: {query} '''
    completion = groq_client.chat.completions.create(
        model= os.environ['GROQ_MODEL'],
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return completion.choices[0].message.content


def faq_chain(query):
    results = get_faq_answer(query)
    context = "".join([r.get('answer') for r in results['metadatas'][0]])
    answers = generate_answer(query, context)
    return answers
    
if __name__ == '__main__':
    #print(faqs_path)
    ingest_faq_data(faqs_path)
    query = "what's your policy on defective products?"
    results = faq_chain(query)

    print("Answer:",results)
