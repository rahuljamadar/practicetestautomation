Resume JD Tailor — Local skill

Quick setup

1. From the `resume-jd-tailor` folder run:

```bash
npm install
```

2. Generate a resume from a spec:

```bash
node scripts/generate_resume.js spec.json output.docx
```

Example `spec.json` (minimal):

{
  "name": [ { "text": "Jane Doe" } ],
  "contact": [ [ { "text": "jane@example.com" } ] ],
  "sections": [
    {
      "title": "Experience",
      "items": [
        {
          "lines": [
            [ { "text": "Senior Engineer, Acme Corp — 2019–Present" } ],
            [ { "text": "Led the platform team focusing on reliability" }, { "text": "improving uptime", "hl": true } ]
          ]
        }
      ]
    }
  ]
}

Notes
- The script highlights runs where `hl` is true using a yellow highlight.
- The `docx` package must be installed (declared in `package.json`).
