import g4f
from flask import Flask, request, jsonify

app = Flask(__name__)

# --------- MAIN CHAT PAGE ---------
chat_html = """ 
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<title>Den-Alsa AI Assistant</title>
<style>
body { font-family: Arial; background:#0d0d0d; color:#fff; margin:0; padding:0;}
.container{display:flex;justify-content:center;align-items:center;height:100vh;flex-direction:column;}
.card{background:#111;border:2px solid #0ff;padding:30px;border-radius:15px;text-align:center;box-shadow:0 0 20px #0ff;width:90%;max-width:400px;}
h1{font-family:'Orbitron',sans-serif;color:#0ff;text-shadow:0 0 10px #0ff,0 0 20px #0ff;}
p{font-size:14px;line-height:1.5;}
input[type="text"]{padding:10px;width:80%;border-radius:10px;border:none;margin-top:15px;outline:none;}
button{margin-top:15px;padding:10px 20px;border:none;border-radius:10px;background:#0ff;color:#000;font-weight:bold;cursor:pointer;transition:0.3s;}
button:hover{background:#0aa;color:#fff;}
#chatbox{display:none;flex-direction:column;margin-top:20px;}
#chatlog{height:300px;overflow-y:auto;border:1px solid #0ff;padding:10px;margin-bottom:10px;border-radius:10px;background:#111;}
#userInput{width:60%;padding:10px;border-radius:10px;border:none;outline:none;}
</style>
</head>
<body>
<div class="container">

<!-- Welcome Card -->
<div id="welcomeCard" class="card">
  <h1>Welcome!</h1>
  <p>Hello!My name is Mohd Eisa, and I am a passionate Ethical Hacker and Python Expert. I have a deep interest in cybersecurity and programming, and I constantly seek out new challenges and innovative solutions.My focus is on designing secure and efficient systems, identifying vulnerabilities, and helping organizations protect their digital assets through ethical hacking. With Python, I specialize in automation, data analysis, and secure application development.I also enjoy sharing knowledge and teaching others about cybersecurity and programming. I firmly believe that learning and growth are continuous processes, and I am always eager to acquire new skills and techniques.<br>Founder of Darknet Gurukul.</p>
  <button onclick="nextStep()">Next</button>
</div>

<!-- Name Input Card -->
<div id="nameCard" class="card" style="display:none;">
  <h1>What's your name?</h1>
  <input type="text" id="userName" placeholder="Enter your name">
  <button onclick="startChat()">Start Chat</button>
</div>

<!-- Chat Box -->
<div id="chatbox" class="card">
  <h1 id="greeting"></h1>
  <div id="chatlog"></div>
  <input type="text" id="userInput" placeholder="Type your message">
  <button onclick="sendMessage()">Send</button>
  <button onclick="window.location='/speak'">🎤 Speak</button>
</div>

</div>

<script>
function nextStep(){
    document.getElementById("welcomeCard").style.display = "none";
    document.getElementById("nameCard").style.display = "block";
}

function startChat(){
    let name = document.getElementById("userName").value.trim();
    if(!name) return;
    document.getElementById("nameCard").style.display = "none";
    document.getElementById("chatbox").style.display = "flex";

    let hour = new Date().getHours();
    let greetText = "Hello";
    if(hour < 12) greetText = "Good Morning";
    else if(hour < 17) greetText = "Good Afternoon";
    else greetText = "Good Evening";

    document.getElementById("greeting").innerText = `${greetText}, ${name}! How can I help you?`;
}

async function sendMessage(){
    let inputBox = document.getElementById("userInput");
    let message = inputBox.value.trim();
    if(!message) return;

    let chatlog = document.getElementById("chatlog");
    chatlog.innerHTML += `<p><b>You:</b> ${message}</p>`;
    inputBox.value = "";

    let response = await fetch("/ask", {
        method:"POST",
        headers:{"Content-Type":"application/json"},
        body:JSON.stringify({message: message})
    });
    let data = await response.json();

    if(data.reply.startsWith("__open__:")){
        let url = data.reply.replace("__open__:", "").trim();
        window.open(url, "_blank");
        chatlog.innerHTML += `<p><b>AI:</b> Opening ${url}</p>`;
    } else {
        chatlog.innerHTML += `<p><b>AI:</b> ${data.reply}</p>`;
    }
    chatlog.scrollTop = chatlog.scrollHeight;
}

document.getElementById("userInput").addEventListener("keydown", function(e){
    if(e.key==="Enter"){
        sendMessage();
    }
});
</script>
</body>
</html>
"""

# --------- SPEAK PAGE ---------
speak_html = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<title>Speak to AI</title>
<style>
:root {
  --neon-1: #0ff;  /* Cyan */
  --neon-2: #0f0;  /* Green */
}

body {
  margin:0;
  padding:0;
  font-family:Arial;
  background:#0d0d0d;
  color:#fff;
  display:flex;
  justify-content:center;
  align-items:center;
  height:100vh;
  flex-direction:column;
}
#wheel {
  width:300px;
  height:300px;
  margin-bottom:20px;
}
input[type="text"] {
  width:70%;
  padding:10px;
  border-radius:10px;
  border:none;
  margin-right:10px;
  outline:none;
}
button {
  padding:10px 20px;
  border:none;
  border-radius:10px;
  background:var(--neon-1);
  color:#000;
  font-weight:bold;
  cursor:pointer;
  transition:0.3s;
}
button:hover {
  background:#0aa;
  color:#fff;
}
</style>
</head>
<body>

<h1>🎤 AI Voice Chat</h1>

<div id="wheel">
<svg viewBox="0 0 100 100">
  <defs>
    <linearGradient id="strokeGradient2" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="var(--neon-1)"/>
      <stop offset="100%" stop-color="var(--neon-2)"/>
    </linearGradient>
    <filter id="glow">
      <feGaussianBlur stdDeviation="2.5" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <radialGradient id="core" cx="50%" cy="50%">
      <stop offset="0%" stop-color="white" stop-opacity=".9"/>
      <stop offset="60%" stop-color="var(--neon-1)" stop-opacity=".9"/>
      <stop offset="100%" stop-color="transparent"/>
    </radialGradient>
  </defs>

  <!-- New Wheel Code -->
  <circle cx="50" cy="50" r="28" fill="none" 
          stroke="url(#strokeGradient2)" stroke-width="1.2" 
          opacity=".9" filter="url(#glow)"/>

  <line x1="50" y1="21" x2="50" y2="18"/>
  <line x1="50" y1="82" x2="50" y2="85"/>
  <line x1="21" y1="50" x2="18" y2="50"/>
  <line x1="82" y1="50" x2="85" y2="50"/>
  <line x1="72.7" y1="27.3" x2="74.8" y2="25.2"/>
  <line x1="27.3" y1="72.7" x2="25.2" y2="74.8"/>
  <line x1="72.7" y1="72.7" x2="74.8" y2="74.8"/>
  <line x1="27.3" y1="27.3" x2="25.2" y2="25.2"/>
  <line x1="63" y1="19" x2="64.5" y2="16.5"/>
  <line x1="37" y1="81" x2="35.5" y2="83.5"/>
  <line x1="81" y1="63" x2="83.5" y2="64.5"/>
  <line x1="19" y1="37" x2="16.5" y2="35.5"/>

  <circle cx="50" cy="50" r="14" fill="url(#core)" opacity=".18"/>
  <circle class="dot" cx="50" cy="50" r="8" fill="none" stroke="var(--neon-1)" stroke-width="0.8"/>
  <circle cx="50" cy="50" r="3.5" fill="var(--neon-2)" opacity=".95"/>
</svg>
</div>

<div>
  <input type="text" id="userInput" placeholder="Type your message...">
  <button onclick="sendMessage()">Send</button>
</div>

<script>
function say(text){
    if(!text) return;
    let u = new SpeechSynthesisUtterance(text);
    u.lang = 'hi-IN';
    speechSynthesis.speak(u);
}

async function sendMessage(){
    let input = document.getElementById("userInput");
    let message = input.value.trim();
    if(!message) return;
    input.value = "";

    let response = await fetch("/ask", {
        method:"POST",
        headers:{"Content-Type":"application/json"},
        body:JSON.stringify({message: message})
    });
    let data = await response.json();
    say(data.reply);
}
document.getElementById("userInput").addEventListener("keydown", function(e){
    if(e.key==="Enter") sendMessage();
});
</script>
</body>
</html>
"""

# --------- ROUTES ---------
@app.route("/")
def index():
    return chat_html

@app.route("/speak")
def speak():
    return speak_html

@app.route("/ask", methods=["POST"])
def ask():
    user_input = request.json.get("message", "").lower().strip()

    # Open commands
    if user_input.startswith("open "):
        site = user_input.replace("open ","").strip()
        url_map = {
    "google": "https://www.google.com",
    "facebook": "https://www.facebook.com",
    "instagram": "https://www.instagram.com",
    "twitter": "https://twitter.com",
    "x": "https://twitter.com",  # Twitter ka new name
    "linkedin": "https://www.linkedin.com",
    "youtube": "https://www.youtube.com",
    "tiktok": "https://www.tiktok.com",
    "snapchat": "https://www.snapchat.com",
    "whatsapp": "https://web.whatsapp.com",
    "telegram": "https://web.telegram.org",
    "messenger": "https://www.messenger.com",
    "reddit": "https://www.reddit.com",
    "pinterest": "https://www.pinterest.com",
    "tumblr": "https://www.tumblr.com",
    "discord": "https://discord.com",
    "slack": "https://slack.com",
    "quora": "https://www.quora.com",
    "twitch": "https://www.twitch.tv",
    "viber": "https://www.viber.com",
    "weibo": "https://www.weibo.com",
    "line": "https://line.me",
    "medium": "https://medium.com",
    "flickr": "https://www.flickr.com",
    "skype": "https://www.skype.com",
    "signal": "https://signal.org",
    "github": "https://github.com",
    "stack_overflow": "https://stackoverflow.com",
    "behance": "https://www.behance.net",
    "dribbble": "https://dribbble.com",
    "vk": "https://vk.com",
    "ok": "https://ok.ru",
    "xing": "https://www.xing.com",
    "meetup": "https://www.meetup.com",
    "yelp": "https://www.yelp.com",
    "dailymotion": "https://www.dailymotion.com",
    "spotify": "https://www.spotify.com",
    "soundcloud": "https://soundcloud.com",
    "patreon": "https://www.patreon.com",
    "bandcamp": "https://bandcamp.com",
    "taringa": "https://www.taringa.net",
    "mix": "https://mix.com",
    "deviantart": "https://www.deviantart.com",
    "vimeo": "https://vimeo.com",
    "foursquare": "https://foursquare.com",
    "badoo": "https://badoo.com",
    "myspace": "https://myspace.com",
    "periscope": "https://www.pscp.tv",
    "clubhouse": "https://www.clubhouse.com",
    "twitch_stream": "https://www.twitch.tv",
    "tgroup": "https://t.me/darknetgurukulbot"
}
        url = url_map.get(site, site if site.startswith("http") else f"https://{site}")
        return jsonify({"reply": f"__open__:{url}"})

    try:
        response = g4f.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role":"user","content":user_input}]
        )
    except:
        response = "Sorry, AI Server is busy. Try again later."
    return jsonify({"reply": response})

if __name__=="__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)