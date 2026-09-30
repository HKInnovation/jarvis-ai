const chatBox = document.getElementById("chatBox");
const userInput = document.getElementById("userInput");
const sendBtn = document.getElementById("sendBtn");
const micBtn = document.getElementById("micBtn");
const attachBtn = document.getElementById("attachBtn");
const fileInput = document.getElementById("fileInput");
const filePreview = document.getElementById("filePreview");
const clearBtn = document.getElementById("clearBtn");
const typingIndicator = document.getElementById("typingIndicator");
const dropZone = document.getElementById("dropZone");
const connStatus = document.getElementById("connStatus");
const languageSelect = document.getElementById("languageSelect");
const wakeToggleBtn = document.getElementById("wakeToggleBtn");
const wakeIndicator = document.getElementById("wakeIndicator");
const wakeIndicatorText = document.getElementById("wakeIndicatorText");
const wakeStatusDot = document.getElementById("wakeStatusDot");
const wakeStatusText = document.getElementById("wakeStatusText");

let selectedFile = null;
let currentLanguage = "en";
let wakeWordEnabled = false;
let wakeRecognition = null;

// ─── Language selector ───────────────────────────────────────────
languageSelect.addEventListener("change", () => {
  currentLanguage = languageSelect.value;
  appendMessage("JARVIS", `Language switched to ${languageSelect.options[languageSelect.selectedIndex].text}.`);
});

// ─── Append message ──────────────────────────────────────────────
function appendMessage(sender, text, imageUrl = null) {
  const isUser = sender === "You";
  const wrapper = document.createElement("div");
  wrapper.className = "message " + (isUser ? "user" : "jarvis");

  const avatar = document.createElement("div");
  avatar.className = "avatar " + (isUser ? "user-avatar" : "jarvis-avatar");
  avatar.textContent = isUser ? "U" : "J";

  const bubble = document.createElement("div");
  bubble.className = "bubble";

  // Format code blocks inside replies
  const formatted = formatText(text);
  const textDiv = document.createElement("div");
  textDiv.className = "bubble-text";
  textDiv.innerHTML = formatted;
  bubble.appendChild(textDiv);

  // Copy button for JARVIS messages
  if (!isUser) {
    const actions = document.createElement("div");
    actions.className = "bubble-actions";
    const copyBtn = document.createElement("button");
    copyBtn.className = "copy-btn";
    copyBtn.textContent = "📋";
    copyBtn.addEventListener("click", () => {
      navigator.clipboard.writeText(text);
      copyBtn.textContent = "✓ Copied!";
      setTimeout(() => copyBtn.textContent = "📋", 1500);
    });
    actions.appendChild(copyBtn);
    bubble.appendChild(actions);
  }

  // Image display
  if (imageUrl) {
    const loadingText = document.createElement("div");
    loadingText.textContent = "⏳ Generating image...";
    loadingText.style.cssText = "color:#00e5ff; font-size:0.85rem; margin-top:6px;";
    bubble.appendChild(loadingText);

    const img = document.createElement("img");
    img.src = imageUrl;
    img.alt = "Generated image";
    img.style.cssText = "max-width:100%; border-radius:10px; margin-top:10px; display:none; cursor:pointer;";
    img.title = "Click to open full size";
    img.addEventListener("click", () => window.open(imageUrl, "_blank"));
    img.onload = () => { loadingText.remove(); img.style.display = "block"; chatBox.scrollTop = chatBox.scrollHeight; };
    img.onerror = () => { loadingText.textContent = "❌ Image failed to load. Try again."; };
    bubble.appendChild(img);
  }

  wrapper.appendChild(avatar);
  wrapper.appendChild(bubble);
  chatBox.appendChild(wrapper);
  chatBox.scrollTop = chatBox.scrollHeight;
}

// ─── Format text — detect code blocks ───────────────────────────
function formatText(text) {
  // Convert ```code``` blocks
  text = text.replace(/```(\w+)?\n?([\s\S]*?)```/g, (_, lang, code) => {
    return `<pre><code>${escapeHtml(code.trim())}</code></pre>`;
  });
  // Convert `inline code`
  text = text.replace(/`([^`]+)`/g, '<code>$1</code>');
  // Convert newlines to <br> outside of pre tags
  text = text.replace(/\n/g, '<br>');
  return text;
}

function escapeHtml(text) {
  return text.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
}

// ─── Video card ──────────────────────────────────────────────────
function appendVideoCard(videoData) {
  const wrapper = document.createElement("div");
  wrapper.className = "message jarvis";

  const avatar = document.createElement("div");
  avatar.className = "avatar jarvis-avatar";
  avatar.textContent = "J";

  const bubble = document.createElement("div");
  bubble.className = "bubble";

  const promptBox = document.createElement("div");
  promptBox.style.cssText = "background:#0d1a2e; border:1px solid #00e5ff44; border-radius:8px; padding:10px; margin-bottom:12px; font-size:0.85rem;";
  promptBox.innerHTML = `<div style="color:#7d93ab; margin-bottom:4px;">✨ Enhanced prompt:</div>
    <div style="color:#00e5ff; font-weight:500;">${videoData.enhanced_prompt}</div>
    <button onclick="navigator.clipboard.writeText('${videoData.enhanced_prompt.replace(/'/g, "\\'")}'); this.textContent='✓ Copied!'; setTimeout(()=>this.textContent='📋 Copy Prompt',1500);"
      style="margin-top:8px; background:#00e5ff22; border:1px solid #00e5ff; color:#00e5ff; padding:5px 12px; border-radius:6px; cursor:pointer; font-size:0.8rem;">
      📋 Copy Prompt
    </button>`;
  bubble.appendChild(promptBox);

  const sitesLabel = document.createElement("div");
  sitesLabel.style.cssText = "color:#7d93ab; font-size:0.8rem; margin-bottom:8px;";
  sitesLabel.textContent = "🎬 Open a free video generator:";
  bubble.appendChild(sitesLabel);

  videoData.sites.forEach(site => {
    const btn = document.createElement("a");
    btn.href = site.url;
    btn.target = "_blank";
    btn.style.cssText = "display:block; background:#0d1a2e; border:1px solid #00e5ff44; border-radius:8px; padding:10px 14px; margin-bottom:8px; text-decoration:none; transition:0.2s;";
    btn.innerHTML = `<div style="color:#00e5ff; font-weight:600; font-size:0.88rem;">🎥 ${site.name}</div>
      <div style="color:#7d93ab; font-size:0.78rem; margin-top:2px;">${site.note}</div>`;
    btn.onmouseover = () => btn.style.background = "#00e5ff11";
    btn.onmouseout = () => btn.style.background = "#0d1a2e";
    bubble.appendChild(btn);
  });

  wrapper.appendChild(avatar);
  wrapper.appendChild(bubble);
  chatBox.appendChild(wrapper);
  chatBox.scrollTop = chatBox.scrollHeight;
}

// ─── Typing indicator ────────────────────────────────────────────
function showTyping(show) {
  typingIndicator.style.display = show ? "flex" : "none";
  if (show) chatBox.scrollTop = chatBox.scrollHeight;
}

// ─── Load history on page load ───────────────────────────────────
window.addEventListener("DOMContentLoaded", async () => {
  try {
    const res = await fetch("/health");
    if (res.ok) { connStatus.textContent = "● Connected"; connStatus.style.color = "#2ee6a8"; }
  } catch { connStatus.textContent = "● Offline"; connStatus.style.color = "#ff4d6d"; }

  try {
    const res = await fetch("/history");
    const data = await res.json();
    if (data.history && data.history.length > 0) {
      chatBox.innerHTML = "";
      data.history.forEach(msg => appendMessage(msg.role === "user" ? "You" : "JARVIS", msg.content));
    } else {
      appendMessage("JARVIS", "Online. How can I help you today?");
    }
  } catch (err) {
    appendMessage("JARVIS", "Online. How can I help you today?");
  }
});

// ─── Clear chat ──────────────────────────────────────────────────
clearBtn.addEventListener("click", async () => {
  if (!confirm("Clear all chat history? This cannot be undone.")) return;
  await fetch("/clear", { method: "POST" });
  chatBox.innerHTML = "";
  appendMessage("JARVIS", "Chat history cleared. Starting fresh.");
});

// ─── Quick chips ─────────────────────────────────────────────────
document.querySelectorAll(".chip").forEach(chip => {
  chip.addEventListener("click", () => {
    if (chip.id !== "wakeToggleBtn") sendMessage(chip.dataset.prompt);
  });
});

// ─── File attach ─────────────────────────────────────────────────
attachBtn.addEventListener("click", () => fileInput.click());
fileInput.addEventListener("change", () => {
  if (fileInput.files.length > 0) setSelectedFile(fileInput.files[0]);
});

function setSelectedFile(file) {
  selectedFile = file;
  filePreview.style.display = "flex";
  filePreview.innerHTML = `📎 ${file.name} <button id="removeFile">✕</button>`;
  document.getElementById("removeFile").addEventListener("click", () => {
    selectedFile = null; fileInput.value = ""; filePreview.style.display = "none";
  });
}

// ─── Ctrl+V paste ────────────────────────────────────────────────
window.addEventListener("paste", (e) => {
  const items = e.clipboardData && e.clipboardData.items;
  if (!items) return;
  for (let i = 0; i < items.length; i++) {
    const item = items[i];
    if (item.type.startsWith("image/")) {
      const file = item.getAsFile();
      const ext = item.type.split("/")[1] || "png";
      setSelectedFile(new File([file], `pasted_image.${ext}`, { type: item.type }));
      appendMessage("JARVIS", "Image pasted! Type a question or hit Send to analyze it.");
      break;
    }
    if (item.type === "text/plain") {
      item.getAsString((text) => { userInput.value += text; userInput.focus(); });
    }
  }
});

// ─── Drag and drop ───────────────────────────────────────────────
let dragCounter = 0;
window.addEventListener("dragenter", (e) => { e.preventDefault(); dragCounter++; dropZone.style.display = "flex"; });
window.addEventListener("dragleave", () => { dragCounter--; if (dragCounter <= 0) dropZone.style.display = "none"; });
window.addEventListener("dragover", (e) => e.preventDefault());
window.addEventListener("drop", (e) => {
  e.preventDefault(); dragCounter = 0; dropZone.style.display = "none";
  if (e.dataTransfer.files.length > 0) setSelectedFile(e.dataTransfer.files[0]);
});

// ─── Send message ────────────────────────────────────────────────
async function sendMessage(text) {
  if (selectedFile) { await sendFileMessage(text); return; }
  if (!text.trim()) return;
  appendMessage("You", text);
  userInput.value = "";
  showTyping(true);

  try {
    const res = await fetch("/ask", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text, speak: true, language: currentLanguage })
    });
    const data = await res.json();
    showTyping(false);
    if (data.video_data) {
      appendMessage("JARVIS", data.reply);
      appendVideoCard(data.video_data);
    } else {
      appendMessage("JARVIS", data.reply, data.image_url || null);
    }
  } catch (err) {
    showTyping(false);
    appendMessage("JARVIS", "Error reaching backend: " + err.message);
  }
}

async function sendFileMessage(question) {
  appendMessage("You", `📎 ${selectedFile.name}${question ? " — " + question : ""}`);
  userInput.value = "";
  showTyping(true);
  const formData = new FormData();
  formData.append("file", selectedFile);
  formData.append("question", question);
  try {
    const res = await fetch("/upload", { method: "POST", body: formData });
    const data = await res.json();
    showTyping(false);
    appendMessage("JARVIS", data.reply);
  } catch (err) {
    showTyping(false);
    appendMessage("JARVIS", "Error analyzing file: " + err.message);
  }
  selectedFile = null; fileInput.value = ""; filePreview.style.display = "none";
}

sendBtn.addEventListener("click", () => sendMessage(userInput.value));
userInput.addEventListener("keydown", (e) => { if (e.key === "Enter") sendMessage(userInput.value); });

// ─── Regular voice input ─────────────────────────────────────────
let recognition;
if ("webkitSpeechRecognition" in window) {
  recognition = new webkitSpeechRecognition();
  recognition.lang = "en-US";
  recognition.continuous = false;
  recognition.interimResults = false;

  micBtn.addEventListener("click", () => {
    if (wakeWordEnabled) {
      wakeRecognition && wakeRecognition.stop();
    }
    micBtn.classList.add("listening");
    recognition.start();
  });

  recognition.onresult = (event) => {
    const text = event.results[0][0].transcript;
    sendMessage(text);
  };
  recognition.onend = () => {
    micBtn.classList.remove("listening");
    if (wakeWordEnabled) startWakeWordListening();
  };
  recognition.onerror = () => {
    micBtn.classList.remove("listening");
    if (wakeWordEnabled) startWakeWordListening();
  };
} else {
  micBtn.addEventListener("click", () => {
    appendMessage("JARVIS", "Voice input isn't supported in this browser. Try Chrome.");
  });
}

// ─── Wake word detection ─────────────────────────────────────────
function startWakeWordListening() {
  if (!("webkitSpeechRecognition" in window)) {
    appendMessage("JARVIS", "Wake word detection requires Chrome browser.");
    return;
  }

  wakeRecognition = new webkitSpeechRecognition();
  wakeRecognition.continuous = true;
  wakeRecognition.interimResults = true;
  wakeRecognition.lang = "en-US";

  wakeRecognition.onresult = (event) => {
    for (let i = event.resultIndex; i < event.results.length; i++) {
      const transcript = event.results[i][0].transcript.toLowerCase().trim();

      // Check for wake word
      if (transcript.includes("hey jarvis") || transcript.includes("hi jarvis") || transcript.includes("okay jarvis")) {
        wakeIndicatorText.textContent = "Wake word detected! Listening...";

        // Stop wake listener, start command listener
        wakeRecognition.stop();

        setTimeout(() => {
          if (recognition) {
            recognition.lang = languageSelect.value === "en" ? "en-US" :
                               languageSelect.value === "ta" ? "ta-IN" :
                               languageSelect.value === "hi" ? "hi-IN" :
                               languageSelect.value === "te" ? "te-IN" : "en-US";
            recognition.start();
            appendMessage("JARVIS", "Yes? I'm listening...");
          }
        }, 300);
        break;
      }
    }
  };

  wakeRecognition.onend = () => {
    // Restart if wake word mode is still on
    if (wakeWordEnabled) {
      try { wakeRecognition.start(); } catch (e) {}
    }
  };

  wakeRecognition.onerror = (e) => {
    if (e.error !== "no-speech" && wakeWordEnabled) {
      try { wakeRecognition.start(); } catch (err) {}
    }
  };

  try {
    wakeRecognition.start();
  } catch (e) {
    console.error("Wake word start error:", e);
  }
}

wakeToggleBtn.addEventListener("click", () => {
  wakeWordEnabled = !wakeWordEnabled;

  if (wakeWordEnabled) {
    wakeToggleBtn.textContent = "🔴 Disable Wake Word";
    wakeToggleBtn.style.borderColor = "#ff4d6d";
    wakeToggleBtn.style.color = "#ff4d6d";
    wakeIndicator.classList.add("active");
    wakeStatusDot.style.background = "#2ee6a8";
    wakeStatusDot.style.boxShadow = "0 0 8px #2ee6a8";
    wakeStatusText.textContent = "Listening";
    startWakeWordListening();
    appendMessage("JARVIS", "Wake word enabled. Say \"Hey JARVIS\" anytime to activate me.");
  } else {
    wakeToggleBtn.textContent = "🎙 Enable \"Hey JARVIS\"";
    wakeToggleBtn.style.borderColor = "";
    wakeToggleBtn.style.color = "";
    wakeIndicator.classList.remove("active");
    wakeStatusDot.style.background = "";
    wakeStatusDot.style.boxShadow = "";
    wakeStatusText.textContent = "Off";
    if (wakeRecognition) { wakeRecognition.stop(); wakeRecognition = null; }
    appendMessage("JARVIS", "Wake word disabled.");
  }
});