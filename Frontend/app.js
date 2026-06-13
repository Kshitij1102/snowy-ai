try{
window.speechSynthesis.getVoices();
}
catch(e){
console.log(e);
}

const recognition =
new (
window.SpeechRecognition ||
window.webkitSpeechRecognition
)();

recognition.continuous=false;
recognition.interimResults=true;
recognition.maxAlternatives=1;
recognition.lang="en-US";

let isProcessing=false;

const statusText=document.getElementById("status");
const logs=document.getElementById("logs");
const core=document.getElementById("core");
const chatInput=document.getElementById("chatInput");
const sendBtn=document.getElementById("sendBtn");


function addLog(text){

const log=
document.createElement("div");

log.className="log";

log.innerHTML=
"["+
new Date().toLocaleTimeString()+
"] "+
text;

logs.prepend(log);

}


function streamMessage(text){

return new Promise(resolve=>{

let i=0;

statusText.innerHTML="";

const interval=
setInterval(()=>{

if(i<text.length){

statusText.innerHTML+=
text[i];

i++;

}

else{

clearInterval(interval);

resolve();

}

},2);

});

}


function setState(state){

statusText.innerHTML=
state;

}


function setMoodVisual(mood){

document.body.classList.remove(
"mood-calm",
"mood-happy",
"mood-sad",
"mood-focus",
"mood-system"
);

document.body.classList.add(
"mood-"+(mood||"calm")
);

}


function startThinkingAnimation(){

document.body.classList.add(
"thinking-active"
);

}


function stopThinkingAnimation(){

document.body.classList.remove(
"thinking-active"
);

}


function startIdleBreathing(){

document.body.classList.add(
"idle-breathing"
);

}


function startSnowy(){

if(isProcessing)
return;

addLog(
"SNOWY activated"
);

setMoodVisual(
"calm"
);

setState(
"LISTENING"
);

startIdleBreathing();

try{

recognition.start();

}

catch(e){

console.log(e);

}

speak(
"Welcome back Kshitij. Neural systems are online."
);

}


recognition.onresult=
async(event)=>{

if(isProcessing)
return;

const result=
event.results[
event.results.length-1
];

if(!result.isFinal)
return;

const command=
result[0]
.transcript;

addLog(
"USER: "+
command
);

isProcessing=true;

await sendToBackend(
command
);

};


async function sendToBackend(command){

try{

setState(
"PROCESSING"
);

startThinkingAnimation();

const controller=
new AbortController();

setTimeout(
()=>controller.abort(),
15000
);

const response=
await fetch(
CONFIG.BACKEND_URL+
"/command",
{
method:"POST",

signal:
controller.signal,

headers:{
"Content-Type":
"application/json"
},

body:
JSON.stringify({
command
})

}
);

const data=
await response.json();

stopThinkingAnimation();

setMoodVisual(
data.mood
);

addLog(
"SNOWY: "+
data.response
);

await streamMessage(
data.response
);

speak(
data.response
);

}

catch(e){

console.log(e);

stopThinkingAnimation();

addLog(
"ERROR: Backend connection failed"
);

setState(
"SYSTEM ERROR"
);

isProcessing=false;

}

}


function speak(text){

window.speechSynthesis.cancel();

const speech=
new SpeechSynthesisUtterance(
text.slice(
0,
250
)
);

speech.lang="en-US";

speech.rate=0.95;

speech.pitch=1;

speech.onstart=
()=>{

setState(
"SNOWY SPEAKING"
);

};

speech.onend=
()=>{

setState(
"LISTENING"
);

isProcessing=false;

};

window.speechSynthesis.speak(
speech
);

}


async function sendTextMessage(){

const command=
chatInput.value.trim();

if(!command)
return;

chatInput.value="";

addLog(
"USER: "+
command
);

isProcessing=true;

await sendToBackend(
command
);

}


sendBtn.addEventListener(
"click",
sendTextMessage
);

chatInput.addEventListener(
"keydown",
(e)=>{

if(
e.key==="Enter"
){

sendTextMessage();

}

}
);


recognition.onerror=
()=>{

isProcessing=false;

};


recognition.onend=
()=>{

if(
!isProcessing
){

setTimeout(()=>{

try{

recognition.start();

}

catch(e){}

},1000);

}

};


window.onload=
()=>{

window.startSnowy=
startSnowy;

setMoodVisual(
"calm"
);

startIdleBreathing();

addLog(
"SNOWY neural interface synchronized."
);

};