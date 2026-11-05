
import { useEffect, useState } from "react";
import {
  ArrowDown,
  ArrowRight,
  Check,
  CheckCircle2,
  Clipboard,
  FileText,
  LoaderCircle,
  RotateCcw,
  Sparkles,
  WandSparkles,
} from "lucide-react";

import "./App.css";

const API_URL = "http://127.0.0.1:8000";

const examples = [
  "She go to college every day.",
  "He don't likes coffee.",
  "I has completed my homework.",
];

function App() {
  const [text, setText] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [copied, setCopied] = useState(false);
  const [backendOnline, setBackendOnline] = useState(false);

  const characterCount = text.length;

  // Check backend connection

  useEffect(() => {
    let active = true;

    async function checkBackend() {
      try {
        const response = await fetch(`${API_URL}/api/health`);

        if (active) {
          setBackendOnline(response.ok);
        }
      } catch {
        if (active) {
          setBackendOnline(false);
        }
      }
    }

    checkBackend();

    return () => {
      active = false;
    };
  }, []);

  // Correct grammar

  async function handleCorrection() {
    if (!text.trim()) {
      setError("Add some text before requesting a correction.");
      return;
    }

    setLoading(true);
    setError("");
    setResult(null);
    setCopied(false);

    try {
      const response = await fetch(`${API_URL}/api/correct`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ text }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail || "Correction could not be completed."
        );
      }

      setResult(data);
    } catch (err) {
      setError(
        err.message ||
          "Unable to connect. Check whether the backend is running."
      );
    } finally {
      setLoading(false);
    }
  }

  // Copy corrected text

  async function handleCopy() {
    if (!result?.corrected) return;

    try {
      await navigator.clipboard.writeText(result.corrected);

      setCopied(true);

      window.setTimeout(() => setCopied(false), 1800);
    } catch {
      setError("Clipboard access failed. Please copy the text manually.");
    }
  }

  // Clear editor

  function handleReset() {
    setText("");
    setResult(null);
    setError("");
    setCopied(false);
  }

  // Load example text
  // Renamed from useExample to handleUseExample

  function handleUseExample(example) {
    setText(example);
    setResult(null);
    setError("");
    setCopied(false);
  }

  return (
    <div className="app-shell">

      {/* Navigation */}

      <header className="topbar">
        <a href="#" className="brand" aria-label="GrammarFix home">
          <span className="brand-mark">
            <WandSparkles size={19} />
          </span>

          <span>
            GrammarFix<span className="brand-period">.</span>
          </span>
        </a>

        <div className="topbar-right">
          <div className="model-label">
            <span className="model-dot" />
            <span>Local T5 model</span>
          </div>

          <div
            className={`connection ${
              backendOnline ? "online" : "offline"
            }`}
          >
            <span className="connection-dot" />

            {backendOnline ? "Connected" : "Backend offline"}
          </div>
        </div>
      </header>


      {/* Main */}

      <main className="main-content">

        {/* Introduction */}

        <section className="intro">
          <div className="eyebrow">
            <span className="eyebrow-line" />
            YOUR PERSONAL WRITING WORKSPACE
          </div>

          <h1>
            Make every
            <br />
            <span>word count.</span>
          </h1>

          <p className="intro-description">
            Good writing starts with clarity. Fix grammar, improve your
            sentences, and express your ideas with confidence.
          </p>
        </section>


        {/* Editor */}

        <section className="workspace">

          <div className="workspace-heading">
            <div>
              <p className="section-number">01 / THE EDITOR</p>
              <h2>Refine your writing</h2>
            </div>

            <span className="privacy-note">
              <CheckCircle2 size={15} />
              Processed on your device
            </span>
          </div>


          {/* Two-panel editor */}

          <div className="editor-grid">

            {/* Original text */}

            <section className="editor-panel input-panel">

              <div className="panel-heading">
                <div className="panel-title">
                  <FileText size={17} />
                  <span>Original text</span>
                </div>

                <span className="panel-index">INPUT</span>
              </div>

              <textarea
                value={text}
                onChange={(event) => {
                  setText(event.target.value);
                  setResult(null);
                  setError("");
                }}
                maxLength={5000}
                placeholder={`Start writing here...

For example:
She go to college every day.`}
                aria-label="Original text"
              />

              <div className="input-footer">
                <span>
                  {characterCount.toLocaleString()} / 5,000 characters
                </span>

                <button
                  type="button"
                  className="text-button"
                  onClick={handleReset}
                >
                  <RotateCcw size={14} />
                  Clear
                </button>
              </div>

              <button
                type="button"
                className="correct-button"
                onClick={handleCorrection}
                disabled={loading || !text.trim()}
              >
                {loading ? (
                  <>
                    <LoaderCircle size={17} className="spin" />
                    Working on your text...
                  </>
                ) : (
                  <>
                    <Sparkles size={17} />
                    Correct my writing
                    <ArrowRight size={16} />
                  </>
                )}
              </button>

            </section>


            {/* Corrected text */}

            <section className="editor-panel output-panel">

              <div className="panel-heading">
                <div className="panel-title">
                  <WandSparkles size={17} />
                  <span>Refined text</span>
                </div>

                <span className="panel-index">OUTPUT</span>
              </div>

              <div className="output-content">

                {result ? (
                  <p className="corrected-text">
                    {result.corrected}
                  </p>
                ) : (
                  <div className="empty-state">
                    <div className="empty-icon">
                      <Sparkles size={21} />
                    </div>

                    <p>Your improved text will appear here.</p>

                    <span>
                      Your original meaning is the starting point.
                    </span>
                  </div>
                )}

              </div>

              <div className="output-footer">
                {result ? (
                  <>
                    <span className="success-label">
                      <CheckCircle2 size={15} />
                      Correction complete
                    </span>

                    <button
                      type="button"
                      className="copy-button"
                      onClick={handleCopy}
                    >
                      {copied ? (
                        <Check size={15} />
                      ) : (
                        <Clipboard size={15} />
                      )}

                      {copied ? "Copied" : "Copy text"}
                    </button>
                  </>
                ) : (
                  <span className="waiting-label">
                    Waiting for your text
                  </span>
                )}
              </div>

            </section>

          </div>


          {/* Error message */}

          {error && (
            <div className="error-message" role="alert">
              {error}
            </div>
          )}


          {/* Example sentences */}

          <div className="examples">
            <span className="examples-label">
              NEED A STARTING POINT?
            </span>

            <div className="example-list">
              {examples.map((example) => (
                <button
                  key={example}
                  type="button"
                  onClick={() => handleUseExample(example)}
                  className="example-chip"
                >
                  {example}
                  <ArrowDown size={13} />
                </button>
              ))}
            </div>
          </div>

        </section>


        {/* Difference viewer */}

        {result && (
          <section className="changes-section">

            <div className="changes-heading">
              <div>
                <p className="section-number">02 / THE EDIT</p>
                <h2>What changed</h2>
              </div>

              <span className="changes-caption">
                A closer look at your corrections
              </span>
            </div>

            <div className="diff-box">
              <div
                className="diff-output"
                dangerouslySetInnerHTML={{
                  __html: result.highlighted_html,
                }}
              />
            </div>

            <div className="diff-legend">
              <span>
                <i className="legend-removed" />
                Removed
              </span>

              <span>
                <i className="legend-added" />
                Added
              </span>
            </div>

          </section>
        )}

      </main>


      {/* Footer */}

      <footer className="footer">
        <div className="footer-inner">

          <span className="footer-brand">
            GrammarFix<span>.</span>
          </span>

          <span>
            Built with React, FastAPI & fine-tuned T5-small
          </span>

          <span>Made for clearer writing.</span>

        </div>
      </footer>

    </div>
  );
}

export default App;
