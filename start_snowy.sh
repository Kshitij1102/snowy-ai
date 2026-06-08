#!/bin/bash

echo "🚀 STARTING SNOWY..."

cd ~/jarvis


echo "🧠 Checking Backend..."

if lsof -i :5000 >/dev/null
then
echo "✅ Backend already running"
else
osascript -e 'tell application "Terminal" to do script "cd ~/jarvis && python3 app.py"'
fi


sleep 5


echo "🤖 Checking Ollama..."

if pgrep -x "ollama" >/dev/null
then
echo "✅ Ollama already running"
else
osascript -e 'tell application "Terminal" to do script "ollama serve"'
fi


sleep 5


echo "🌐 Starting Cloudflare..."

osascript -e 'tell application "Terminal" to do script "cloudflared tunnel --url http://localhost:5000"'


echo "❄️ SNOWY READY"