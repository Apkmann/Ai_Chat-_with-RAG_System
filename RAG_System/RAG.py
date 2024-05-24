import google.generativeai as ai #For Ai Model
import chromadb #importing chromadb
from chromadb.config import Settings
from langchain_community.document_loaders import Docx2txtLoader ,PyPDFLoader #importing document loaders
from langchain_text_splitters import RecursiveCharacterTextSplitter #importing text splitters
import os
from dotenv import load_dotenv,find_dotenv


_ = load_dotenv(find_dotenv())
if _:
    ai.configure(

    api_key = os.environ["api_key"]

    )  
else:
    raise "API KEY Not Found!"

instruction = "You are a query solver.You are provided sentences; you need to answer the query by using the given sentences and your response must be in html tags and don't include like '''html''' to indicate this is html"
model = ai.GenerativeModel(model_name='gemini-1.5-pro-latest',
                               system_instruction=instruction)

messages = []
client = chromadb.Client(settings=Settings(allow_reset=True))
collection = client.create_collection(
    name="Temp_File",
    )

def FileLoader(file):
    try:
        #It is for laoding the pdf,docx and doc format files seperately
        if file.name.endswith('.docx') or file.name.endswith('.doc'):
            fileLoad = Docx2txtLoader(GetFilePath(file))
            loaded = fileLoad.load()
        else:
            fileLoad = PyPDFLoader(GetFilePath(file))
            loaded = fileLoad.load()

        text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=435, #size of chunks 
        chunk_overlap=3, #overlaping of chunks
        length_function=len, #passing the len function
        separators = ['/n','/n/n',' ',''] #seperators
        )

        splitted_document = text_splitter.split_documents(loaded)
        for i,_ in enumerate(splitted_document):

            #adding the chunks to vector database chromadb it will store in vector format
            collection.add(
                ids=[f"id{i}"],
                documents=[_.page_content],
                metadatas=[_.metadata]
            )

        return True
    except Exception as e:
        return False    

def GetFilePath(f):
    file_path = f"RAG_System//temp//{f.name}"
    with open(file_path, 'wb+') as target:
        for chunk in f.chunks():
            target.write(chunk)
    return file_path #It returns the path of the file fron temp folder

def History_File_Loader(path):
    #For retriving the file and again going to the same process above
    try:
        if path.endswith('.docx') or path.endswith('.doc'):
            fileLoad = Docx2txtLoader(path)
            loaded = fileLoad.load()
        else:
            fileLoad = PyPDFLoader(path)
            loaded = fileLoad.load()
        text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=435,
        chunk_overlap=3,
        length_function=len,
        separators = ['/n','/n/n',' ','']
        )

        splitted_document = text_splitter.split_documents(loaded)
        for i,_ in enumerate(splitted_document):
            collection.add(
                ids=[f"id{i}"],
                documents=[_.page_content],
                metadatas=[_.metadata]
            )

        return True
    except Exception as e:
        return False


result = ""
def Generate_answer(query):
    global result
    #It will give the matching chunks for the query
    paragarph = collection.query(
            query_texts = [query],
            n_results=3 
        )
    sentences = "".join(paragarph['documents'][0])
    complete_query = f"sentences:{sentences}; query:{query}; generate an answer for the query using the above sentences."
    try:
        if messages==[]:
            messages.append({'role':'user','parts':[complete_query]})
            result = model.generate_content(messages).text
            return {"complete_query":complete_query,"Airesponse":result}
        else:
            if result!=None:
                messages.append({'role':'model','parts':[result]})
                messages.append({'role':'user','parts':[complete_query]})
                result = model.generate_content(messages).text
                return {"complete_query":complete_query,"Airesponse":result} #It will return reponses from Ai and chunks with query
            else:
                return "An Error Occured: "
    except Exception as e:
        return "<h3 style='color:red;'>An Error Occured: "+str(e)+"</h3>"

    