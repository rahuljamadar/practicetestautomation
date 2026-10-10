import { useCallback, useEffect, useRef, useState } from 'react';

const initialStatus = {
  phase: 'starting',
  error: '',
  sourceName: '',
  pages: 0,
  chunkCount: 0,
  embeddingModel: 'Xenova/all-MiniLM-L6-v2',
  embeddingDimensions: 384,
  embeddingPrecision: 'quantized ONNX',
  vectorStore: 'Vectra local file-backed vector index',
  llmModel: 'openai/gpt-oss-120b',
  llmConfigured: false,
};

async function api(path, options) {
  const response = await fetch(path, options);
  const payload = await response.json();
  if (!response.ok) throw new Error(payload.error || 'Request failed.');
  return payload;
}

function StatusPill({ phase }) {
  const label = phase === 'ready' ? 'Ready' : phase === 'ingesting' ? 'Ingesting PDF' : phase === 'error' ? 'Needs attention' : 'Starting';
  return <span className={`status-pill status-${phase}`}><span className="status-dot" />{label}</span>;
}

function Workflow({ phase }) {
  const steps = [
    ['01', 'Read PDF', 'Extract selectable text'],
    ['02', 'Make chunks', '1100 chars · 180 overlap'],
    ['03', 'Embed locally', 'MiniLM · 384 dimensions'],
    ['04', 'Rank matches', 'Cosine similarity · top 3'],
    ['05', 'Ground answer', 'Groq · GPT-OSS 120B'],
  ];
  return (
    <section className="workflow" aria-label="RAG pipeline">
      {steps.map(([number, title, detail], index) => (
        <div className="workflow-step" key={number}>
          <div className={`step-number ${phase === 'ready' && index < 4 ? 'step-done' : ''}`}>{number}</div>
          <div><strong>{title}</strong><small>{detail}</small></div>
          {index < steps.length - 1 && <span className="step-arrow" aria-hidden="true">→</span>}
        </div>
      ))}
    </section>
  );
}

function ResultCard({ result }) {
  return (
    <article className="result-card">
      <header className="result-head">
        <div className="result-title"><span className="rank-badge">{String(result.rank).padStart(2, '0')}</span><div><strong>Chunk {result.chunkIndex}</strong><small>Characters {result.start.toLocaleString()}–{result.end.toLocaleString()}</small></div></div>
        <div className="score-block"><strong>{result.score.toFixed(4)}</strong><small>cosine score</small></div>
      </header>
      <p className="result-text">{result.text}</p>
      <div className="result-foot">
        <div className="term-list"><span className="meta-label">Query terms found</span>{result.matchedTerms.length ? result.matchedTerms.map((term) => <span className="term-chip" key={term}>{term}</span>) : <span className="muted">semantic match</span>}</div>
        <details className="vector-details">
          <summary>Embedding values</summary>
          <code>[{result.vectorPreview.map((value) => value.toFixed(4)).join(', ')} …]</code>
        </details>
      </div>
    </article>
  );
}

function App() {
  const [status, setStatus] = useState(initialStatus);
  const [chunks, setChunks] = useState([]);
  const [activeTab, setActiveTab] = useState('search');
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);
  const [queryVector, setQueryVector] = useState([]);
  const [answer, setAnswer] = useState('');
  const [busy, setBusy] = useState(false);
  const [message, setMessage] = useState('');
  const chunksLoadedFor = useRef('');

  const refreshStatus = useCallback(async () => {
    try {
      const next = await api('/api/status');
      setStatus(next);
      const sourceVersion = `${next.sourceName}:${next.chunkCount}:${next.revision}`;
      if (next.phase === 'ready' && sourceVersion !== chunksLoadedFor.current) {
        chunksLoadedFor.current = sourceVersion;
        const data = await api('/api/chunks');
        setChunks(data.chunks);
      }
    } catch (error) {
      setMessage(error.message);
    }
  }, []);

  useEffect(() => {
    void refreshStatus();
    const timer = window.setInterval(() => void refreshStatus(), 2500);
    return () => window.clearInterval(timer);
  }, [refreshStatus]);

  async function runSearch(event) {
    event.preventDefault();
    if (!query.trim() || busy) return;
    setBusy(true);
    setMessage('');
    setAnswer('');
    try {
      const response = await api('/api/search', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query }),
      });
      setResults(response.results);
      setQueryVector(response.queryVectorPreview);
    } catch (error) {
      setMessage(error.message);
    } finally {
      setBusy(false);
    }
  }

  async function runChat() {
    if (!query.trim() || busy) return;
    setBusy(true);
    setMessage('');
    setAnswer('');
    try {
      const response = await api('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query }),
      });
      setAnswer(response.answer);
      setResults(response.results);
      setQueryVector(response.queryVectorPreview);
      setActiveTab('chat');
    } catch (error) {
      setMessage(error.message);
    } finally {
      setBusy(false);
    }
  }

  async function ingestFile(event) {
    const file = event.target.files?.[0];
    if (!file) return;
    setBusy(true);
    setMessage('Extracting, chunking and embedding the PDF locally…');
    chunksLoadedFor.current = '';
    setResults([]);
    setAnswer('');
    try {
      const form = new FormData();
      form.append('pdf', file);
      await api('/api/ingest', { method: 'POST', body: form });
      setMessage('PDF ingested successfully.');
      await refreshStatus();
    } catch (error) {
      setMessage(error.message);
      await refreshStatus();
    } finally {
      setBusy(false);
      event.target.value = '';
    }
  }

  const isReady = status.phase === 'ready';

  return (
    <main className="app-shell">
      <header className="topbar">
        <a className="brand" href="#top" aria-label="RAG Explorer home"><span className="brand-mark">R</span><span>RAG<span className="brand-light"> Explorer</span></span></a>
        <div className="topbar-right"><span className="local-tag"><span className="lock-icon">◆</span> Local-first indexing</span><StatusPill phase={status.phase} /></div>
      </header>

      <section className="hero" id="top">
        <div className="hero-copy">
          <div className="eyebrow"><span className="eyebrow-line" />A transparent, single-document RAG demo</div>
          <h1>From PDF to<br /><span>grounded answers.</span></h1>
          <p>Follow each step: extracted text becomes overlapping chunks, local embeddings find the best matches, and the LLM answers from those passages.</p>
          <div className="hero-actions">
            <label className={`upload-button ${busy ? 'disabled' : ''}`}>
              <span aria-hidden="true">＋</span> Ingest another PDF
              <input type="file" accept="application/pdf,.pdf" onChange={ingestFile} disabled={busy} />
            </label>
            <span className="file-hint">PDF · up to 20 MB</span>
          </div>
        </div>
        <div className="document-card">
          <div className="doc-illustration"><div className="doc-icon"><span>PDF</span><i /><i /><i /><b /></div><span className="spark spark-one">✦</span><span className="spark spark-two">✧</span></div>
          <div className="doc-info">
            <span className="meta-label">ACTIVE SOURCE</span>
            <strong title={status.sourceName || 'Waiting for PDF'}>{status.sourceName || 'Waiting for PDF…'}</strong>
            <div className="doc-stats"><span>{status.pages || '—'} pages</span><i /> <span>{status.chunkCount || 0} chunks</span><i /> <span>{status.textLength ? `${status.textLength.toLocaleString()} chars` : '—'}</span></div>
          </div>
          <div className="doc-ready">{isReady ? '✓' : '…'}</div>
        </div>
      </section>

      <Workflow phase={status.phase} />

      {status.phase === 'error' && <div className="notice notice-error" role="alert"><strong>Ingestion needs attention</strong><span>{status.error}</span></div>}
      {!status.llmConfigured && <div className="notice"><strong>Search is ready; chat needs a Groq key.</strong><span>Set GROQ_API_KEY in the workspace-root .env file. The key stays on the server and is never sent to the browser.</span></div>}

      <section className="workspace-grid">
        <div className="main-panel panel">
          <div className="panel-heading">
            <div><span className="section-kicker">ASK YOUR DOCUMENT</span><h2>Search & chat</h2><p>Search ranks the closest passages. Chat uses those same top three as context.</p></div>
            <div className="tab-switch" role="tablist" aria-label="Result mode">
              <button className={activeTab === 'search' ? 'active' : ''} onClick={() => setActiveTab('search')} role="tab" aria-selected={activeTab === 'search'}>Search</button>
              <button className={activeTab === 'chat' ? 'active' : ''} onClick={() => setActiveTab('chat')} role="tab" aria-selected={activeTab === 'chat'}>Chat</button>
            </div>
          </div>

          <form className="query-form" onSubmit={runSearch}>
            <span className="search-glyph" aria-hidden="true">⌕</span>
            <input value={query} onChange={(event) => setQuery(event.target.value)} placeholder="Ask about a requirement, workflow, or feature…" aria-label="Question for the PDF" disabled={!isReady} />
            <button className="search-button" type="submit" disabled={!isReady || busy || !query.trim()}>{busy ? 'Working…' : 'Find chunks'} <span aria-hidden="true">↗</span></button>
          </form>
          <div className="query-actions"><span>Uses local semantic embeddings</span><button type="button" className="text-button" disabled={!isReady || busy || !query.trim() || !status.llmConfigured} onClick={runChat}>✦ Ask with GPT-OSS 120B</button></div>
          {message && <div className={`inline-message ${message.includes('success') ? 'success' : ''}`} role="status">{message}</div>}

          {!isReady && status.phase !== 'error' && <div className="empty-state"><div className="loader" /><strong>Preparing the local embedding model</strong><span>On first launch, model files are downloaded and cached on this machine.</span></div>}
          {activeTab === 'chat' && answer && <div className="answer-card"><div className="answer-heading"><span className="answer-spark">✦</span><div><strong>Grounded answer</strong><small>{status.llmModel}</small></div></div><div className="answer-copy">{answer}</div><p className="privacy-note">Only the question and retrieved top-three passages were sent to Groq for this answer.</p></div>}
          {results.length > 0 && <div className="results-section">
            <div className="results-heading"><div><span className="section-kicker">RETRIEVAL TRACE</span><h3>Top 3 matching chunks</h3></div><span className="retrieval-method">Cosine similarity · descending</span></div>
            <div className="query-vector"><span className="meta-label">Query vector · first 8 dimensions</span><code>[{queryVector.map((value) => Number(value).toFixed(4)).join(', ')} …]</code></div>
            <div className="results-list">{results.map((result) => <ResultCard result={result} key={result.id} />)}</div>
          </div>}
          {isReady && results.length === 0 && !(activeTab === 'chat' && answer) && <div className="empty-state compact"><div className="empty-icon">⌕</div><strong>Your retrieval trace will appear here</strong><span>Try asking what the document says about login or dashboard behavior.</span></div>}
        </div>

        <aside className="side-column">
          <section className="panel chunks-panel">
            <div className="side-heading"><div><span className="section-kicker">INGESTION OUTPUT</span><h2>Document chunks</h2></div><span className="count-badge">{chunks.length}</span></div>
            <p className="side-description">Text is split into {status.chunkCount ? 'overlapping character windows' : 'overlapping chunks'}. Expand any item to inspect the exact passage sent to retrieval.</p>
            <div className="chunks-list">
              {chunks.length ? chunks.map((chunk) => <details className="chunk-item" key={chunk.id}>
                <summary><span className="chunk-number">{String(chunk.chunkIndex).padStart(2, '0')}</span><span className="chunk-summary"><strong>Chunk {chunk.chunkIndex}</strong><small>{chunk.text.length.toLocaleString()} characters · offset {chunk.start.toLocaleString()}</small></span><span className="chunk-chevron">⌄</span></summary>
                <p>{chunk.text}</p>
              </details>) : <div className="chunks-empty">Chunks will show here after PDF ingestion.</div>}
            </div>
          </section>

          <section className="panel settings-panel">
            <div className="side-heading"><div><span className="section-kicker">SERVER CONFIG</span><h2>Behind the scenes</h2></div><span className="settings-icon">⚙</span></div>
            <div className="config-row"><span>Embedding model</span><strong>{status.embeddingModel.split('/').at(-1)}</strong></div>
            <div className="config-row"><span>Vector dimensions</span><strong>{status.embeddingDimensions} · {status.embeddingPrecision.toUpperCase()}</strong></div>
            <div className="config-row"><span>Vector store</span><strong>{status.vectorStore.startsWith('Vectra') ? 'Vectra · local disk' : status.vectorStore}</strong></div>
            <div className="config-row"><span>Answer model</span><strong>{status.llmModel}</strong></div>
            <div className="weight-explainer"><span className="weight-icon">∑</span><p><strong>What are these “weights”?</strong> The displayed numbers are embedding coordinates and cosine similarity scores—not the LLM’s private neural-network parameters. Ranking is calculated on this server.</p></div>
          </section>
        </aside>
      </section>

      <footer className="footer"><span>RAG Explorer · retrieval and embeddings run locally</span><span>Groq is called only when you choose Chat</span></footer>
    </main>
  );
}

export default App;
