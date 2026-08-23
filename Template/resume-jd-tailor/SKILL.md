---
name: resume-jd-tailor
description: Tailor an existing/older resume to a specific job description, producing a fresh Word resume with the changed or added text highlighted in yellow so the person can see exactly what was adjusted. Use this whenever the user provides (or references) an existing resume AND a job description and wants a matched, tailored, JD-aligned, or "ATS-friendly" version — trigger on phrases like "tailor my resume", "match this JD", "update my resume for this job", "job-matching resume", or when they paste a job description right after sharing a resume. Do NOT invent experience, tools, employers, or metrics the candidate doesn't actually have — every change must be traceable to something already true in the source resume.
---

# Resume ↔ Job Description Tailoring

Produces a fresh, JD-tailored resume from an existing resume + a job description, with every
added/reworded phrase highlighted in yellow in the output .docx. The core discipline of this
skill is **honesty over keyword-stuffing**: only emphasize, rephrase, or resurface content that
is already true of the candidate. Gaps get flagged in the chat reply, never papered over in the
resume itself.

## Step 0 — Read prerequisite skills

Before creating any file, view `/mnt/skills/public/docx/SKILL.md` (this skill still uses the
docx conventions for verification — render to PDF/images and visually check before delivering).
If the source resume is a file you haven't read yet (PDF/docx and not already in context), also
consult `/mnt/skills/public/file-reading/SKILL.md`.

## Step 1 — Gather inputs

You need both of these; if either is missing, ask for it rather than guessing:
1. **The existing/older resume** — an uploaded file, or content already in the conversation
   (e.g. from an earlier turn in this same chat).
2. **The job description** — pasted text or an uploaded/linked file.

If the user references "my resume" but none is in context or uploads, ask them to paste or
upload it. Don't fabricate a resume to fill the gap.

## Step 2 — Extract JD requirements

Read the JD and pull out a working list, split into:
- **Explicit/required skills, tools, certifications** (e.g. "JIRA", "Agile/Scrum", "5+ years")
- **Frequently repeated keywords/phrases** — terms that show up more than once, or that anchor
  a bullet point in the JD, are more ATS-significant than one-off mentions
- **Nice-to-have / plus items** — usually marked "a plus", "preferred", "nice to have"

## Step 3 — Cross-reference against the resume, honestly

For every item from Step 2, classify it against the source resume into exactly one bucket:

| Bucket | Meaning | Action |
|---|---|---|
| **Direct match** | Already stated in the resume, same or near-same wording | Leave as-is, or lightly reposition for visibility. No highlight needed unless reworded. |
| **Honest rephrase** | The resume shows real evidence of this, but in different words, or scattered/implicit | Rewrite that portion using the JD's language. Highlight the changed/added words. |
| **Reasonable inference** | Not stated outright, but a *direct logical consequence* of a fact already on the resume (e.g. a listed technology that is inherently desktop/Windows-based implies "standalone Windows application" experience) | OK to state explicitly, highlighted. Keep the inference tight and defensible — if you have to speculate, it's not this bucket, it's the next one. |
| **Gap** | No real evidence anywhere in the resume, and not a tight inference from stated facts | **Do not add to the resume.** List it in your final chat summary as a gap instead. |

This classification step is the heart of the skill. Do it explicitly (even just in your own
reasoning) before writing any resume text — don't rephrase-on-the-fly while drafting.

**Hard rules, no exceptions:**
- Never invent employers, job titles, dates, degrees, certifications, or tools.
- Never invent quantified achievements (%, counts, dollar amounts). If the JD context calls for
  a metric and the source resume doesn't have one, use a bracketed placeholder like `[XX]%` or
  `[X]` — never a fabricated-but-plausible-looking number presented as fact.
- Regulated/high-stakes requirements (medical device, aviation, finance compliance, security
  clearance, specific regulatory standards like FDA/ISO) deserve extra caution — these are exactly
  the kind of claims that cause real harm if fabricated. When in doubt, it's a gap, not an inference.

## Step 4 — Build the resume content as a JSON spec

Use `scripts/generate_resume.js`, a reusable docx builder driven by a JSON file. This keeps
formatting consistent across runs instead of hand-rolling docx code each time. Full schema and
field-by-field notes are in `references/resume_schema.md` — read it before writing the JSON.

Key points:
- Every piece of text is a `{ "text": "...", "hl": true|false }` run. Set `"hl": true` **only**
  on the words you added or reworded per Step 3 (Honest rephrase / Reasonable inference buckets).
  Everything untouched keeps `"hl": false` (or omit — defaults to false).
- Preserve the candidate's real structure: same employers, same dates, same job titles, same
  project names. You're re-emphasizing and rewording, not restructuring their history.
- Keep bracketed metric placeholders (`[XX]%`, `[X]+`) exactly as found in the source resume,
  or introduce them (unhighlighted-metric, highlighted-surrounding-phrase-if-new) only where the
  JD language calls for a metric that isn't in the source.
- Write the JSON to a scratch path (e.g. `/home/claude/resume_spec.json`), not directly to outputs.

## Step 5 — Generate, verify, and deliver

```bash
node /mnt/skills/user/resume-jd-tailor/scripts/generate_resume.js <spec.json> <output.docx>
```
(Adjust the script path to wherever this skill is actually installed — check with `view` on the
skill directory if unsure.)

Then, per standard docx-skill practice:
1. Convert to PDF and rasterize to images (`soffice.py --convert-to pdf`, then `pdftoppm`).
2. `view` the rendered page image(s) — check the highlights look right, nothing overflows a
   page awkwardly, and the layout still reads as a clean, professional resume, not a wall of
   yellow.
3. Copy the final file to `/mnt/user-data/outputs/`, then `present_files` it.

## Step 6 — Report honestly in chat (not in the resume)

After presenting the file, always include a short, plain-language summary with two parts:
1. **What was tailored** — the main keywords/phrases you incorporated and where (grouped
   naturally, not a giant list).
2. **Gaps** — JD requirements with no real basis in the resume, stated plainly, so the person can
   decide how to handle them (cover letter, interview talking points, or acknowledging the gap).
   Don't skip this section even if it feels like it undercuts the pitch — it's the difference
   between a tailored resume and a misleading one.

## Reusing this skill on the next resume + JD pair

Nothing in this skill is specific to any one candidate. Each time the user provides a new
resume + JD, repeat Steps 1–6 fresh: re-extract JD keywords, re-classify against *that* resume,
build a new JSON spec, generate a new docx. Don't carry over highlighted phrasing from a
previous run — every JD gets its own honest cross-reference.
