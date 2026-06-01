import { useState, useRef } from "react";

const BACKEND_URL = "http://127.0.0.1:8000";

const createMessage = (text, role) => ({ text, role });

function App() {
  const [youtubeUrl, setYoutubeUrl] = useState("");
  const [instagramUrl, setInstagramUrl] = useState("");
  const [question, setQuestion] = useState("");
  const [status, setStatus] = useState("Ready.");
  const [chatHistory, setChatHistory] = useState([]);
  const [chatLog, setChatLog] = useState([]);
  const [isWorking, setIsWorking] = useState(false);
  const answerRef = useRef(null);

  const setResult = (text) => setStatus(text);

  const ingestVideos = async (event) => {
    event.preventDefault();
    if (!youtubeUrl || !instagramUrl) {
      setResult("Please enter both URLs before ingesting.");
      return;
    }

    setResult("Ingesting videos… this may take a minute.");
    setIsWorking(true);

    try {
      const response = await fetch(`${BACKEND_URL}/ingest`, {
        method: "POST",
        mode: "cors",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ youtube_url: youtubeUrl, instagram_url: instagramUrl }),
      });

      if (!response.ok) {
        throw new Error(`Ingest failed: ${response.statusText}`);
      }

      const data = await response.json();
      setResult(`Ingest complete.\nVideo A title: ${data.video_a_title || "N/A"}\nVideo B title: ${data.video_b_title || "N/A"}\nChunks: ${data.video_a_chunks} / ${data.video_b_chunks}`);
    } catch (error) {
      console.error("Ingest error", error);
      setResult(`Ingest error: ${error.message}`);
    } finally {
      setIsWorking(false);
    }
  };

  const streamChat = async (event) => {
    event.preventDefault();
    if (!question) return;

    const userMessage = createMessage(question, "question");
    setChatLog((prev) => [...prev, userMessage]);
    const answerMessage = createMessage("", "answer");
    setChatLog((prev) => [...prev, answerMessage]);
    setQuestion("");
    setIsWorking(true);
    setResult("Streaming answer…");

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
        if (done) break;

        buffer += decoder.decode(value, { stream: true });
        const parts = buffer.split("\n\n");
        buffer = parts.pop();

        for (const part of parts) {
          if (!part.startsWith("data:")) continue;
          const payload = part.slice(5).trim();
          if (!payload || payload === "[DONE]") continue;

          const json = JSON.parse(payload);
          accumulated += json.text;
          answerRef.current = accumulated;
          setChatLog((prev) => {
            const updated = [...prev];
            updated[updated.length - 1] = createMessage(accumulated, "answer");
            return updated;
          });
        }
      }

      setResult("Answer complete.");
    } catch (error) {
      console.error("Chat stream error", error);
      setChatLog((prev) => {
        const updated = [...prev];
        updated[updated.length - 1] = createMessage(`Error: ${error.message}`, "answer");
        return updated;
      });
      setResult(`Chat error: ${error.message}`);
    } finally {
      setIsWorking(false);
    }
  };

  const loadHistory = async () => {
    setIsWorking(true);
    setResult("Loading history…");

    try {
      const response = await fetch(`${BACKEND_URL}/history`, { mode: "cors" });
      if (!response.ok) {
        throw new Error(`History load failed: ${response.statusText}`);
      }

      const history = await response.json();
      setChatHistory(history || []);
      setResult(`Loaded ${history?.length || 0} history entries.`);
    } catch (error) {
      console.error("History load error", error);
      setResult(`History error: ${error.message}`);
    } finally {
      setIsWorking(false);
    }
  };

  return (
    <div className="container">
      <header>
        <h1>Video RAG Demo</h1>
        <p>A simple React demo for ingesting video URLs and asking questions.</p>
      </header>

      <section className="card">
        <h2>1. Ingest Videos</h2>
        <form onSubmit={ingestVideos}>
          <div className="field">
            <label htmlFor="youtube-url">YouTube URL</label>
            <input
              id="youtube-url"
              type="url"
              value={youtubeUrl}
              placeholder="https://www.youtube.com/watch?v=..."
              onChange={(event) => setYoutubeUrl(event.target.value)}
              required
            />
          </div>
          <div className="field">
            <label htmlFor="instagram-url">Instagram URL</label>
            <input
              id="instagram-url"
              type="url"
              value={instagramUrl}
              placeholder="https://www.instagram.com/..."
              onChange={(event) => setInstagramUrl(event.target.value)}
              required
            />
          </div>
          <button type="submit" disabled={isWorking}>
            Ingest videos
          </button>
        </form>
        <div className="result">{status}</div>
      </section>

      <section className="card">
        <h2>2. Ask a Question</h2>
        <form onSubmit={streamChat}>
          <div className="field">
            <label htmlFor="question">Question</label>
            <input
              id="question"
              type="text"
              value={question}
              placeholder="Ask something about the ingested videos"
              onChange={(event) => setQuestion(event.target.value)}
              required
            />
          </div>
          <button type="submit" disabled={isWorking}>
            Send question
          </button>
        </form>
        <div className="chat-log">
          {chatLog.map((message, index) => (
            <div key={index} className={`message ${message.role}`}>
              <strong>{message.role === "question" ? "You" : "Assistant"}</strong>
              <span>{message.text}</span>
            </div>
          ))}
        </div>
      </section>

      <section className="card">
        <h2>3. View History</h2>
        <button onClick={loadHistory} disabled={isWorking}>
          Load chat history
        </button>
        <div className="history-list">
          {chatHistory.length === 0 ? (
            <div className="status">No history available yet.</div>
          ) : (
            chatHistory.map((entry, index) => (
              <div className="history-item" key={index}>
                <strong>Q:</strong> {entry.question}
                <br />
                <strong>A:</strong> {entry.answer}
              </div>
            ))
          )}
        </div>
      </section>
    </div>
  );
}

export default App;
