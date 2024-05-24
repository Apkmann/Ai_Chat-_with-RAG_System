async function answer_to_query()
  {
    fetch('/SolveQuery/',{
      method:'POST',
      headers:{
        'Content-Type':'application/x-www-form-urlencoded'
      },
      body:"query="+encodeURIComponent(query.value)
    })
    .then(response=>response.json())
    .then(data=>{
      console.log(data.answer);
    })

  }

  if(messageinput.value!="")
  {
  let val = messageinput.value;
  starttext.style.display="none";
  chat.style.display="block";
  wholeexamples.style.display = "none";
  chat.innerHTML+=`<p>You: ${messageinput.value}</p>`;
  sendbutton.disabled = true;
  sendbuttonp.style.opacity = "0.3";
  messageinput.value="";
  chats.scrollTop = chats.scrollHeight;

  //Fetch method uses for api call
  fetch('/responseresult/', {
  method: 'POST',
  headers: {
  'Content-Type': 'application/x-www-form-urlencoded',
  },
  body: "query="+encodeURIComponent(val), //Sends the user message
})
.then(response => response.json())
.then(data => {
  sendbutton.disabled = false;
  sendbuttonp.style.opacity = "1";

  if((data.response.includes("An Error Occured"))===false) //For Handling Error If this false the retrived data will be shown in interface
  {
  chat.innerHTML+=`Ai: ${data.answer}`;
  chats.scrollTop = chats.scrollHeight;
  if('chatdata' in data)
  {
    if(nohistory)
    sidebar.innerHTML="";

    sidebar.innerHTML+=`<button id="historychat" onclick='sendid(${data.chatdata.chatid})'>${data.chatdata.title}...</button>`;

    sidebar.scrollTop=-sidebar.scrollHeight;

  }
}
else
{
  chat.innerHTML+=`<h3 style="color:red;">${data.response}</h3>`;
  sendbutton.disabled = true;
  sendbuttonp.style.opacity = "0.3";
}
  

})
.catch((error) => {

  console.error('Error:', error);
  
});
}


  async function history(id)
  {
    fetch(`/history/${id}`,{
      method:'POST'
    })
    .then(response=>response.json())
    .then(data=>{
      console.log(data.history);
    })

  }










function showsidebar()
{
    let sidebar = document.getElementById("sidebar");
    sidebar.style.transform = "none";
}

function hidesidebar()
{
    let sidebar = document.getElementById("sidebar");
    sidebar.style.transform = "translateX(-380px)";
}