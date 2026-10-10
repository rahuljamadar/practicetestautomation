# RAG Basics Explorer

A local-first, single-PDF RAG demo. It extracts PDF text, splits it into overlapping chunks, embeds those chunks on the local machine, stores vectors in a file-backed Vectra index, and shows the top three cosine-similarity matches. Optional chat sends only the question and those retrieved passages to Groq's `openai/gpt-oss-120b` model.

## Run it

1. Make sure the workspace-root `.env` contains `GROQ_API_KEY=...` (the key is read only by the server; never put it in this folder's frontend code).
2. From this folder, run `npm install` once, `npm run build`, and then `npm start`.
3. Open `http://127.0.0.1:4174`.

The PDF already in this folder is ingested automatically on server startup. You can also select another PDF in the UI. For the first run, the server downloads the open-source MiniLM ONNX model to the Hugging Face cache; indexing thereafter runs locally.

The production API server serves the built UI on port 4174. The API accepts `RAG_PORT` (not the generic `PORT`) as an optional override. Development mode runs Vite separately at `http://127.0.0.1:5187`.

## What the explorer shows

- Extracted page count, text length, and every chunk with character offsets.
- Chunk overlap: 1,100-character windows with 180 characters of overlap.
- Local 384-dimensional `Xenova/all-MiniLM-L6-v2` embeddings (quantized ONNX).
- A Vectra local file-backed vector index in `.rag-index/`.
- Top-three similarity scores, matching query terms, and the first eight query/chunk embedding coordinates.
- Grounded Groq answer with chunk citations.

The shown coordinates are embedding values, not private LLM model weights. Cosine similarity scores are computed server-side.

## Confidentiality note

PDF extraction, chunking, embedding, indexing, and search run locally. Choosing **Ask with GPT-OSS 120B** sends the question and retrieved top-three passages to Groq for inference. Do not use that chat action for documents that your organization's policy forbids sending to Groq. The API key is never returned to the browser. The local `.rag-index/` contains extracted document text and embeddings, and is gitignored.

The default PDF is text-extracted without OCR; scanned/image-only PDFs need OCR before the text can be searched.
