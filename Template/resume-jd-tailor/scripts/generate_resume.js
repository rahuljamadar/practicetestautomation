#!/usr/bin/env node
const fs = require('fs');
const path = require('path');
const { Document, Packer, Paragraph, TextRun, HeadingLevel } = require('docx');

function run() {
  const args = process.argv.slice(2);
  if (args.length < 2) {
    console.error('Usage: node generate_resume.js <spec.json> <output.docx>');
    process.exit(2);
  }

  const specPath = path.resolve(args[0]);
  const outPath = path.resolve(args[1]);

  if (!fs.existsSync(specPath)) {
    console.error('Spec file not found:', specPath);
    process.exit(2);
  }

  const spec = JSON.parse(fs.readFileSync(specPath, 'utf8'));

  const doc = new Document({});

  // Helper to convert a run {text, hl} to a TextRun
  function runToTextRun(run) {
    const opts = { text: run.text };
    if (run.hl) opts.highlight = 'yellow';
    return new TextRun(opts);
  }

  // Title / name
  if (spec.name) {
    const runs = Array.isArray(spec.name)
      ? spec.name.map(runToTextRun)
      : [new TextRun({ text: String(spec.name), bold: true })];
    doc.addSection({ children: [new Paragraph({ children: runs, heading: HeadingLevel.HEADING_1 })] });
  }

  // Contact lines
  if (spec.contact && Array.isArray(spec.contact)) {
    const contactParas = spec.contact.map(line => new Paragraph({ children: line.map(runToTextRun) }));
    doc.addSection({ children: contactParas });
  }

  // Sections
  if (spec.sections && Array.isArray(spec.sections)) {
    const children = [];
    spec.sections.forEach(section => {
      // Section title
      if (section.title) {
        children.push(new Paragraph({ text: section.title, heading: HeadingLevel.HEADING_2 }));
      }
      // Items (could be paragraphs or bullets)
      if (section.items && Array.isArray(section.items)) {
        section.items.forEach(item => {
          if (item.type === 'bullet' && Array.isArray(item.lines)) {
            // Join lines into one paragraph with line breaks
            const runs = [];
            item.lines.forEach((line, idx) => {
              runs.push(...line.map(runToTextRun));
              if (idx < item.lines.length - 1) runs.push(new TextRun({ text: '\n' }));
            });
            children.push(new Paragraph({ children: runs }));
          } else if (item.lines && Array.isArray(item.lines)) {
            const runs = [];
            item.lines.forEach((line, idx) => {
              runs.push(...line.map(runToTextRun));
              if (idx < item.lines.length - 1) runs.push(new TextRun({ text: '\n' }));
            });
            children.push(new Paragraph({ children: runs }));
          } else if (item.text) {
            children.push(new Paragraph({ children: [runToTextRun({ text: item.text, hl: !!item.hl })] }));
          }
        });
      }
    });
    if (children.length) doc.addSection({ children });
  }

  // Fallback: if no sections and no content, try spec.rawParagraphs
  if ((!spec.sections || spec.sections.length === 0) && spec.rawParagraphs) {
    const children = spec.rawParagraphs.map(p => new Paragraph({ children: p.map(runToTextRun) }));
    doc.addSection({ children });
  }

  Packer.toBuffer(doc).then(buffer => {
    fs.writeFileSync(outPath, buffer);
    console.log('Wrote', outPath);
  }).catch(err => {
    console.error('Error generating docx:', err);
    process.exit(3);
  });
}

run();
