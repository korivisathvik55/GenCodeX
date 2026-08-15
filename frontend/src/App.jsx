import { useState } from "react";
import ReactMarkdown from "react-markdown";
import "./App.css";

function App() {
  const [repoUrl, setRepoUrl] = useState("");
  const [filePath, setFilePath] = useState("");
  const [question, setQuestion] = useState("");

  const [answer, setAnswer] = useState("");
  const [sources, setSources] = useState([]);

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const askGenCodeX = async () => {
    setError("");
    setAnswer("");
    setSources([]);

    if (!repoUrl.trim()) {
      setError("Please enter a GitHub repository URL.");
      return;
    }

    if (!filePath.trim()) {
      setError("Please enter a file path.");
      return;
    }

    if (!question.trim()) {
      setError("Please enter a question.");
      return;
    }

    setLoading(true);

    try {
      const response = await fetch(
        "http://127.0.0.1:8000/repositories/ask",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            repo_url: repoUrl,
            file_path: filePath,
            question: question,
          }),
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Something went wrong.");
      }

      setAnswer(data.answer);
      setSources(data.sources || []);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app">
      <header className="header">
        <div>
          <h1>GenCodeX</h1>
          <p>AI-powered GitHub Codebase Assistant</p>
        </div>
      </header>

      <main className="container">
        <section className="card">
          <h2>Ask your codebase</h2>

          <label>GitHub Repository URL</label>
          <input
            type="text"
            placeholder="https://github.com/fastapi/fastapi"
            value={repoUrl}
            onChange={(e) => setRepoUrl(e.target.value)}
          />

          <label>File Path</label>
          <input
            type="text"
            placeholder="fastapi/applications.py"
            value={filePath}
            onChange={(e) => setFilePath(e.target.value)}
          />

          <label>Your Question</label>
          <textarea
            placeholder="How is the FastAPI application initialized?"
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
          />

          <button
            onClick={askGenCodeX}
            disabled={loading}
          >
            {loading ? "Analyzing..." : "Ask GenCodeX"}
          </button>

          {error && (
            <div className="error">
              {error}
            </div>
          )}
        </section>

        {answer && (
          <section className="card answer-card">
            <h2>AI Answer</h2>

            <div className="answer">
  		<ReactMarkdown>
	            {answer}
  		</ReactMarkdown>
            </div>
          </section>
        )}

        {sources.length > 0 && (
          <section className="card">
            <h2>Retrieved Sources</h2>

            {sources.map((source, index) => (
              <div className="source" key={index}>
                <div className="source-header">
  		     <span className="source-file">
    		     {source.file}
  		     </span>

                     <span className="source-tag">
    		     Chunk {source.chunk_id}
 		     </span>

  		     <span className="source-distance">
                     Similarity distance: {source.distance.toFixed(3)}
                     </span>
                </div>
                <pre>
                  {source.content}
                </pre>
              </div>
            ))}
          </section>
        )}
      </main>
    </div>
  );
}

export default App;