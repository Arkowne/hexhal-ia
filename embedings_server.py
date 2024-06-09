import gradio as gr
import json
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import Chroma
from langchain_community import embeddings
from langchain_community.chat_models import ChatOllama
from langchain_core. runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.embeddings import OllamaEmbeddings

# Chemin vers votre fichier JSON
json_file_path = "data.json"

# Fonction pour récupérer l'URL à partir du fichier JSON
def get_url_from_json(file_path):
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
            url = data.get('url')
            if url:
                return url
            else:
                print("Aucune URL trouvée dans le fichier JSON.")
                return None
    except FileNotFoundError:
        print(f"Fichier '{file_path}' non trouvé.")
        return None
    except json.JSONDecodeError:
        print(f"Erreur de décodage JSON pour le fichier '{file_path}'. Assurez-vous qu'il est au format JSON valide.")
        return None

# Appel de la fonction pour récupérer l'URL
url_from_json = get_url_from_json(json_file_path)

# Vérification si une URL a été récupérée avec succès
if url_from_json:
    print("URL récupérée avec succès :", url_from_json)
    urls = url_from_json
else:
    print("Impossible de récupérer l'URL.")


model_local = ChatOllama(model="mistral:latest")
# 1. Split data into chunks
urls_list = urls.split("\n")
docs = [WebBaseLoader(url).load() for url in urls_list]
docs_list = [item for sublist in docs for item in sublist]
text_splitter = CharacterTextSplitter.from_tiktoken_encoder(chunk_size=7500, chunk_overlap=100) 
doc_splits = text_splitter.split_documents(docs_list)

vectorstore = Chroma. from_documents(
    documents=doc_splits,
    collection_name="rag-chroma" ,
    embedding=embeddings.ollama.OllamaEmbeddings(model='nomic-embed-text')
)

retriever = vectorstore.as_retriever()

def process_input(question):  

    #print("Before Rag\n")
    #before_rag_template = "What is {topic}"
    #before_rag_prompt = ChatPromptTemplate.from_template(before_rag_template)
    #before_rag_chain = before_rag_prompt | model_local | StrOutputParser()
    #print(before_rag_chain.invoke({"topic": "Ollama"}))

    print("\n#######\nAfter Rag\n")
    after_rag_template = """Answer the question based only on the following context:
    {context}
    Question: {question}
    """

    after_rag_prompt = ChatPromptTemplate.from_template(after_rag_template)
    after_rag_chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | after_rag_prompt
        | model_local
        | StrOutputParser()
    )

    return after_rag_chain.invoke(question)

iface = gr.Interface(fn=process_input,
                     inputs=[gr.Textbox(label="Question")],
                     outputs="text",
                     title="Document Query",
                     description="Enter Urls")
iface.launch()
