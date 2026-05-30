window.speechSynthesis.getVoices();

const recognition =
new(window.SpeechRecognition || window.webkitSpeechRecognition)();

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



/* 📡 LOG SYSTEM */

function addLog(text){

    const log = document.createElement("div");

    log.className = "log";

    log.innerHTML =
    "[" + new Date().toLocaleTimeString() + "] " + text;

    logs.prepend(log);

}



/* ✨ STREAMING EFFECT */

function streamMessage(text){

    return new Promise((resolve)=>{

        let index = 0;

        let output = "";

        const interval = setInterval(()=>{

            if(index < text.length){

                output += text.charAt(index);

                statusText.innerText = output;

                index++;

            }

            else{

                clearInterval(interval);

                resolve();

            }

        },5);

    });

}



/* ⚡ CORE STATES */

function setState(state){

    statusText.innerText = state;

    if(state.includes("LISTENING")){

        core.style.transform = "scale(1)";
        core.style.filter = "brightness(1)";

    }

    else if(state.includes("PROCESSING")){

        core.style.transform = "scale(1.08)";
        core.style.filter = "brightness(1.5)";

    }

    else if(state.includes("SPEAKING")){

        core.style.transform = "scale(1.04)";
        core.style.filter = "brightness(1.25)";

    }

}



/* 🌈 MOOD VISUALS */

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

    if(mood === "happy"){

        body.classList.add("mood-happy");

    }

    else if(mood === "sad"){

        body.classList.add("mood-sad");

    }

    else if(mood === "focus"){

        body.classList.add("mood-focus");

    }

    else if(mood === "system"){

        body.classList.add("mood-system");

    }

    else{

        body.classList.add("mood-calm");

    }

}



/* 🌌 THINKING MODE */

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



/* 😴 IDLE BREATHING */

function startIdleBreathing(){

    document.body.classList.add(
        "idle-breathing"
    );

}



/* 🚀 START SNOWY */

function startSnowy(){

    try{

        recognition.start();

    }

    catch(error){

        console.log(error);

    }

    addLog("SNOWY activated");

    setState("LISTENING");

    setMoodVisual("calm");

    startIdleBreathing();

    speak(
        "Welcome back Kshitij. Neural systems are online."
    );

}



/* 🎙️ VOICE LISTENING */

recognition.onresult = async function(event){

    if(isProcessing) return;

    const command =
    event.results[event.results.length - 1][0]
    .transcript
    .toLowerCase();

    addLog("USER: " + command);

    isProcessing = true;

    await sendToBackend(command);

};



/* 🌐 SEND TO BACKEND */

async function sendToBackend(command){

    try{

        setState("PROCESSING");

        startThinkingAnimation();

        statusText.innerHTML =
        'THINKING <span class="thinking"><span class="dot"></span><span class="dot"></span><span class="dot"></span></span>';

        const response = await fetch(
            "https://ottawa-blank-induction-porcelain.trycloudflare.com/command",

            {

                method:"POST",

                headers:{
                    "Content-Type":"application/json"
                },

                body:JSON.stringify({
                    command:command
                })

            }
        );

        const data = await response.json();

        stopThinkingAnimation();

        setMoodVisual(data.mood);

        addLog("SNOWY: " + data.response);

        await streamMessage(data.response);
    console.log("🔊 Speaking:", data.response);
        speak(data.response);

    }

    catch(error){

        console.error(error);

        stopThinkingAnimation();

        addLog("ERROR: Backend connection failed");

        setMoodVisual("system");

        speak(
            "Sir, my neural channels are fluctuating slightly. Attempting recovery."
        );

        isProcessing = false;

    }

}



/* 🗣️ SPEECH ENGINE */

function speak(text){
    console.log("🎤 speak() called");

    try{

        recognition.stop();

    }

    catch(error){

        console.log(error);

    }

    if(window.speechSynthesis.speaking){

        window.speechSynthesis.cancel();

    }

    const speech =
    new SpeechSynthesisUtterance();

    speech.text = text;

    speech.lang = "en-US";

    const voices =
    window.speechSynthesis.getVoices();

    const selectedVoice =
    voices.find(
        voice =>
        voice.lang &&
        voice.lang.includes("en")
    );

    if(selectedVoice){

        speech.voice = selectedVoice;

    }

    speech.volume = 1;

    speech.rate = 0.92;

    speech.pitch = 0.95;



    speech.onstart = ()=>{

        document.body.classList.add(
            "speaking-active"
        );

        setState("SNOWY SPEAKING");

    };



    speech.onend = ()=>{

        document.body.classList.remove(
            "speaking-active"
        );

        setState("LISTENING");

        isProcessing = false;

        setTimeout(()=>{

            if(!isProcessing){

                try{

                    recognition.start();

                }

                catch(error){

                    console.log(error);

                }

            }

        },2500);

    };



    speech.onerror = ()=>{

        document.body.classList.remove(
            "speaking-active"
        );

        isProcessing = false;

        setState("LISTENING");

    };



    setTimeout(()=>{

        window.speechSynthesis.speak(speech);

    },250);

}



/* 💬 TEXT CHAT */

sendBtn.addEventListener(
    "click",
    sendTextMessage
);



chatInput.addEventListener(
    "keypress",
    function(event){

        if(event.key === "Enter"){

            sendTextMessage();

        }

    }
);



async function sendTextMessage(){

    const command =
    chatInput.value.trim();

    if(!command) return;

    addLog("USER: " + command);

    chatInput.value = "";

    isProcessing = true;

    await sendToBackend(command);

}



/* ❌ RECOGNITION ERRORS */

recognition.onerror = function(event){

    console.log(event.error);

    if(event.error === "no-speech"){

        try{

            recognition.start();

        }

        catch(error){

            console.log(error);

        }

        return;

    }

    if(event.error === "not-allowed"){

        addLog("Microphone permission denied");

        setState("MIC BLOCKED");

        return;

    }

    isProcessing = false;

    setState("LISTENING");

};



/* 🌌 STARTUP AMBIENCE */

window.onload = ()=>{

    setMoodVisual("calm");

    startIdleBreathing();

    addLog(
        "SNOWY neural interface synchronized."
    );

};