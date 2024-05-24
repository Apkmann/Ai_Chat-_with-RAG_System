from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from RAG_System.RAG import collection,FileLoader,Generate_answer,History_File_Loader,messages
from .models import RAGMessages
import os

unique_id = 0
Is_File_Loaded = False

#Entry point of RAG Application
@csrf_exempt
def RAG(request):
    global unique_id
    ids = collection.get()['ids']
    if ids!=[]:
        collection.delete(ids) #To reset the chromadb collection it deletes the all the data for new file
    messages.clear() #also deletes the current conversations for Ai
    last = RAGMessages.objects.last() #it will return the last appended object
    unique_id = last.chat_id+1 if last else unique_id+1 #For Generating new specific Chat id it uses the last appended chat's chat id to Generate the unique chat id 
    chatids = RAGMessages.objects.all()
    path = f"RAG_System//temp//"
    files = os.listdir(path)
    for i in files:
        os.remove(path+i) #It deletes the file from temp folder
    return render(request,'RAGSystem.html',{'chatids':chatids})

#Responsible for Loading the file
@csrf_exempt
def Upload_File(request):
    global unique_id,Is_File_Loaded
    if request.method=="POST":
        File = request.FILES['file']
        Is_File_Loaded = FileLoader(File) #Getting the indication if the file is loaded successfully

        if Is_File_Loaded:
            with open(f"RAG_System//media//{File.name}", 'wb+') as target:  #it saves the files for past conversation
                for chunk in File.chunks():
                    target.write(chunk)

        if Is_File_Loaded:
            RAGMessages.objects.create(chat_id=unique_id,File=f"RAG_System//media//{File.name}",title=File.name)
            return JsonResponse({"response":f"File:  {File.name}   Uploaded   Successfully!"}) #Returns to javascript after a successful file processing
        
        else:
            return JsonResponse({"response":"Failed to Upload"})
    else:
        return JsonResponse({"response":"false"})

#Responsible for answering query   
@csrf_exempt
def SolveQuery(request):
    global unique_id
    if request.method=="POST":
        query = request.POST.get('query',None)

        if query:
            Answer = Generate_answer(query)
            try:
                if "An Error Occurred" not in Answer and Is_File_Loaded: #This is to store the conversations in database for future retrival
                    RAGchat = RAGMessages.objects.get(chat_id=unique_id)
                
                    #This conversation is stored for the Ai it contains the chunks and queries as user message and ai responses
                    RAGchat.conversations_For_Ai.append({'role':'user','parts':[Answer['complete_query']]})
                    RAGchat.conversations_For_Ai.append({'role':'model','parts':[Answer['Airesponse']]})
                    
                    #This conversation is stored for the User it contains the queries of a user only and ai responses
                    RAGchat.conversations_For_User.append({'role':'user','parts':[query]})
                    RAGchat.conversations_For_User.append({'role':'model','parts':[Answer['Airesponse']]}) 
                    RAGchat.save()

                    return JsonResponse({"answer":Answer["Airesponse"]})
                else:
                    return JsonResponse({"answer":Answer})
            except Exception as e:
                return JsonResponse({"answer":"An Error Occurred: "+str(e)})
        else:
            return JsonResponse({"answer":"false"})
    else:
        return JsonResponse({"answer":"false"})


#Responsible for retriving Past Conversation
@csrf_exempt
def history(request,chatid):
    global unique_id,Is_File_Loaded
    ids = collection.get()['ids']

    if ids!=[]:
        collection.delete(ids)
    messages.clear()

    unique_id = chatid #It sets the recieved chat id of previous chat to global unique_id variable 
    RAGchat = RAGMessages.objects.get(chat_id=chatid) #It retrives the previous conversation by using the recived chat id
    Is_File_Loaded = History_File_Loader(RAGchat.File)
    
    if Is_File_Loaded:
        for i in RAGchat.conversations_For_Ai: #Appending the previous conversations to Ai after clicking the history chat
            messages.append(i)
        return JsonResponse({"history":RAGchat.conversations_For_User,"filename":RAGchat.title}) #Sending the previous conversations to user interface after clicking the history chat
    else:
        return JsonResponse({"history":"false"})