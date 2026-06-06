window.speechSynthesis.getVoices();

const recognition =
new (window.SpeechRecognition || window.webkitSpeechRecognition)();

recognition.continuous = true;
recognition.interimResults = false;
recognition.lang = "en-US";

let isProcessing = false;

const statusText =
document.getElementById("status");

const logs =
document.getElementById("logs");

const core =
document.getElementById("core");

const chatInput =
document.getElementById("chatInput");

const sendBtn =
document.getElementById("sendBtn");

function addLog(text){

const log =
document.createElement("div");

log.className =
"log";

log.innerHTML =
"[" +
new Date().toLocaleTimeString() +
"] " +
text;

logs.prepend(log);

}

function streamMessage(text){

return new Promise((resolve)=>{

let index = 0;

let output = "";

const interval =
setInterval(()=>{

if(index < text.length){

output +=
text.charAt(index);

statusText.innerText =
output;

index++;

}

else{

clearInterval(interval);

resolve();

}

},5);

});

}

function setState(state){

statusText.innerText =
state;

if(state.includes("LISTENING")){

core.style.transform =
"scale(1)";

core.style.filter =
"brightness(1)";

}

else if(state.includes("PROCESSING")){

core.style.transform =
"scale(1.08)";

core.style.filter =
"brightness(1.5)";

}

else if(state.includes("SPEAKING")){

core.style.transform =
"scale(1.04)";

core.style.filter =
"brightness(1.25)";

}

}

function setMoodVisual(mood){

const body =
document.body;

body.classList.remove(
"mood-calm",
"mood-happy",
"mood-sad",
"mood-focus",
"mood-system"
);

body.classList.add(
"mood-" +
(mood || "calm")
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

try{

recognition.start();

}

catch(e){

console.log(e);

}

addLog(
"SNOWY activated"
);

setState(
"LISTENING"
);

setMoodVisual(
"calm"
);

startIdleBreathing();

speak(
"Welcome back Kshitij. Neural systems are online."
);

}

recognition.onresult =
async function(event){

if(isProcessing)
return;

const command =
event.results[
event.results.length - 1
][0]
.transcript
.toLowerCase();

addLog(
"USER: " +
command
);

isProcessing =
true;

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

statusText.innerHTML =
'THINKING <span class="thinking"><span class="dot"></span><span class="dot"></span><span class="dot"></span></span>';

const response =
await fetch(

"https://capable-relying-obvious-wilderness.trycloudflare.com/command",

{

method:
"POST",

headers:{
"Content-Type":
"application/json"
},

body:
JSON.stringify({

command:
command

})

}

);

if(!response.ok){

throw new Error(
response.status
);

}

const data =
await response.json();

stopThinkingAnimation();

setMoodVisual(
data.mood
);

addLog(
"SNOWY: " +
data.response
);

await streamMessage(
data.response
);

speak(
data.response
);

}

catch(error){

console.error(
error
);

stopThinkingAnimation();

addLog(
"ERROR: Backend connection failed"
);

setMoodVisual(
"system"
);

speak(
"Sir, my neural channels are fluctuating slightly. Attempting recovery."
);

isProcessing =
false;

}

}

function speak(text){

try{

recognition.stop();

}

catch(e){}

window.speechSynthesis.cancel();

const speech =
new SpeechSynthesisUtterance(
text
);

speech.lang =
"en-US";

speech.rate =
0.92;

speech.pitch =
0.95;

speech.onstart =
()=>{

document.body.classList.add(
"speaking-active"
);

setState(
"SNOWY SPEAKING"
);

};

speech.onend =
()=>{

document.body.classList.remove(
"speaking-active"
);

setState(
"LISTENING"
);

isProcessing =
false;

setTimeout(()=>{

try{

recognition.start();

}

catch(e){}

},2500);

};

window.speechSynthesis.speak(
speech
);

}

sendBtn.addEventListener(
"click",
sendTextMessage
);

chatInput.addEventListener(
"keypress",
(event)=>{

if(
event.key==="Enter"
){

sendTextMessage();

}

}

);

async function sendTextMessage(){

const command =
chatInput.value
.trim();

if(!command)
return;

chatInput.value =
"";

addLog(
"USER: " +
command
);

isProcessing =
true;

await sendToBackend(
command
);

}

recognition.onerror =
function(){

isProcessing =
false;

setState(
"LISTENING"
);

};

window.onload =
()=>{

setMoodVisual(
"calm"
);

startIdleBreathing();

addLog(
"SNOWY neural interface synchronized."
);

};
