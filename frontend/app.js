const BACKEND_URL = "http://127.0.0.1:8000";

const ingestForm = document.getElementById("ingest-form");
const youtubeUrlInput = document.getElementById("youtube-url");
const instagramUrlInput = document.getElementById("instagram-url");
const ingestResult = document.getElementById("ingest-result");
const ingestButton = document.getElementById("ingest-button");

const chatForm = document.getElementById("chat-form");
const questionInput = document.getElementById("question");
const chatLog = document.getElementById("chat-log");
const chatButton = document.getElementById("chat-button");

const historyButton = document.getElementById("history-button");
const historyList = document.getElementById("history-list");

function createMessage(text, role) {
  const item = document.createElement("div");
  item.className = `message ${role}`;
  item.innerHTML = `<strong>${role === "question" ? "You" : "Assistant"}</strong><span>${text}</span>`;
  return item;
}

function createHistoryItem(entry) {
  const item = document.createElement("div");
  item.className = "history-item";
  item.innerHTML = `<strong>Q:</strong> ${entry.question}<br /><strong>A:</strong> ${entry.answer}`;
  return item;
}

function setResult(text) {
  ingestResult.innerHTML = `<div class="status">${text}</div>`;
}

function setStatus(message) {
  setResult(message);
}

function toggleDisabled(state) {
  ingestButton.disabled = state;
  chatButton.disabled = state;
  historyButton.disabled = state;
}

async function ingestVideos(event) {
  event.preventDefault();
  const youtube_url = youtubeUrlInput.value.trim();
  const instagram_url = instagramUrlInput.value.trim();

  if (!youtube_url || !instagram_url) {
    setStatus("Please enter both URLs before ingesting.");
    return;
  }

  setStatus("Ingesting videos… this may take a minute.");
  toggleDisabled(true);

  try {
    const response = await fetch(`${BACKEND_URL}/ingest`, {
      method: "POST",
      mode: "cors",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ youtube_url, instagram_url }),
    });

    if (!response.ok) {
      throw new Error(`Ingest failed: ${response.statusText}`);
    }

    const data = await response.json();
    setStatus(`Ingest complete.\nVideo A title: ${data.video_a_title || "N/A"}\nVideo B title: ${data.video_b_title || "N/A"}\nChunks: ${data.video_a_chunks} / ${data.video_b_chunks}`);
  } catch (error) {
    console.error("Ingest error", error);
    setStatus(`Ingest error: ${error.message}`);
  } finally {
    toggleDisabled(false);
  }
}

async function streamChat(event) {
  event.preventDefault();
  const question = questionInput.value.trim();
  if (!question) {
    return;
  }

  const userMessage = createMessage(question, "question");
  chatLog.appendChild(userMessage);
  const answerMessage = createMessage("", "answer");
  chatLog.appendChild(answerMessage);
  chatLog.scrollTop = chatLog.scrollHeight;

  toggleDisabled(true);

  try {
    const response = await fetch(`${BACKEND_URL}/chat/stream`, {
      method: "POST",
      mode: "cors",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question }),
    });

    if (!response.ok) {
      throw new Error(`Chat request failed: ${response.statusText}`);
    }

    const reader = response.body.getReader();
    const decoder = new TextDecoder();
    let buffer = "";
    let accumulated = "";

    while (true) {
      const { done, value } = await reader.read();
      if (done) {
        break;
      }
      buffer += decoder.decode(value, { stream: true });
      const parts = buffer.split("\n\n");
      buffer = parts.pop();

      for (const part of parts) {
        if (!part.startsWith("data:")) {
          continue;
        }
        const payload = part.slice(5).trim();
        if (!payload || payload === "[DONE]") {
          continue;
        }

        const json = JSON.parse(payload);
        accumulated += json.text;
        answerMessage.querySelector("span").textContent = accumulated;
        chatLog.scrollTop = chatLog.scrollHeight;
      }
    }
  } catch (error) {
    console.error("Chat stream error", error);
    answerMessage.querySelector("span").textContent = `Error: ${error.message}`;
  } finally {
    toggleDisabled(false);
    questionInput.value = "";
  }
}

async function loadHistory() {
  historyList.innerHTML = "";
  setResult("Loading history…");
  toggleDisabled(true);

  try {
    const response = await fetch(`${BACKEND_URL}/history`, { mode: "cors" });
    if (!response.ok) {
      throw new Error(`History load failed: ${response.statusText}`);
    }

    const history = await response.json();
    if (!Array.isArray(history) || history.length === 0) {
      historyList.innerHTML = `<div class="status">No history available yet.</div>`;
    } else {
      history.forEach(item => {
        historyList.appendChild(createHistoryItem(item));
      });
      setResult(`Loaded ${history.length} history entries.`);
    }
  } catch (error) {
    console.error("History load error", error);
    setResult(`History error: ${error.message}`);
  } finally {
    toggleDisabled(false);
  }
}

ingestForm.addEventListener("submit", ingestVideos);
chatForm.addEventListener("submit", streamChat);
historyButton.addEventListener("click", loadHistory);
