# Ham Radio General Class Learning Center — Design Spec

**Date:** 2026-06-11  
**Status:** Approved

---

## Overview

A Quarto website hosted at `ham-study/learning-center/` that teaches the content of the FCC Amateur Radio General Class (Element 3) exam. Unlike the existing Streamlit study app (which is a practice/quiz tool), this is a structured learning resource — a textbook with inline self-checks. It teaches concepts in a logical pedagogical order and embeds exam questions as collapsible callouts at the point where the prerequisite knowledge has just been taught.

Target reader: highly intelligent adult with no prior ham radio or electronics knowledge (PhD in an unrelated field). Everything is explained from first principles. No jargon without definition.

---

## Architecture

A Quarto website project living in a subdirectory of the existing repo:

```
ham-study/
└── learning-center/
    ├── _quarto.yml
    ├── index.qmd           # Overview + how to use the site
    ├── g1-rules.qmd        # Commission's Rules (52 questions)
    ├── g2-operating.qmd    # Operating Procedures (59 questions)
    ├── g3-propagation.qmd  # Radio Wave Propagation (37 questions)
    ├── g4-practices.qmd    # Amateur Radio Practices (60 questions)
    ├── g5-electrical.qmd   # Electrical Principles (40 questions)
    ├── g6-components.qmd   # Circuit Components (23 questions)
    ├── g7-circuits.qmd     # Practical Circuits (38 questions)
    ├── g8-signals.qmd      # Signals and Emissions (42 questions)
    ├── g9-antennas.qmd     # Antennas and Feed Lines (46 questions)
    └── g0-safety.qmd       # Electrical and RF Safety (25 questions)
```

`index.qmd` is the landing page: a brief description of the learning center's purpose, how to use the collapsible question callouts, and a linked table of contents to all 10 subelement pages.

No Python/R code execution. All `.qmd` files are pure markdown + Quarto directives. `quarto render` produces a static `_site/` directory deployed to Posit Connect.

---

## Configuration (`_quarto.yml`)

```yaml
project:
  type: website

website:
  title: "General Class Ham Radio — Learning Center"
  sidebar:
    style: "docked"
    search: true
    contents:
      - index.qmd
      - g1-rules.qmd
      - g2-operating.qmd
      - g3-propagation.qmd
      - g4-practices.qmd
      - g5-electrical.qmd
      - g6-components.qmd
      - g7-circuits.qmd
      - g8-signals.qmd
      - g9-antennas.qmd
      - g0-safety.qmd

format:
  html:
    theme: cosmo
    toc: true
    toc-location: right
```

Quarto's built-in search indexes all pages. The floating right-side TOC enables within-page navigation among conceptual sections.

---

## Question Callout Format

Every exam question is embedded as a Quarto collapsible callout block using the built-in `collapse="true"` option. The question text appears in the always-visible callout header. The four answer choices appear in the body, revealed when the user clicks. The correct answer is **bolded**.

```markdown
::: {.callout-note collapse="true"}
## G1A01: On which HF and/or MF amateur bands are there portions where General class licensees cannot transmit?

- A) 60 meters, 30 meters, 17 meters, and 12 meters
- B) 160 meters, 60 meters, 15 meters, and 12 meters
- **C) 80 meters, 40 meters, 20 meters, and 15 meters**
- D) 80 meters, 20 meters, 15 meters, and 10 meters
:::
```

No custom HTML, CSS, or JavaScript. This uses only built-in Quarto features.

---

## Content Approach

### Ordering

Content within each page is organized by **pedagogical logic**, not by the FCC's official sub-group lettering (G1A, G1B, etc.). Concepts are sequenced so that each section builds on the last. All 422 exam questions are placed inline at the first point where the reader has enough knowledge to engage with them.

### Two content modes

**Regulations and memorization sections** (e.g., band privileges, power limits, station identification rules):
1. Explain the regulatory framework and *why* the rule exists
2. Provide a mnemonic device where the rule requires memorization of specific values or lists
3. Embed the relevant question callout(s)

**Technical sections** (e.g., electrical principles, propagation, circuits, antennas):
1. Define every term from first principles before using it
2. Explain the underlying physics or engineering concept
3. Use analogies and worked examples where they aid understanding
4. Embed the relevant question callout(s)

### Coverage

All 422 questions from `data/general_class_questions.json` are covered. Every question appears exactly once, embedded at the appropriate point in the lesson. The source data is used for question IDs, question text, answer choices, and correct answer only — the existing AI-generated `explanation` field is not used. All pedagogical content is written fresh.

### Subelement summaries

| File | Subelement | Topic | Questions |
|---|---|---|---|
| g1-rules.qmd | G1 | Commission's Rules | 52 |
| g2-operating.qmd | G2 | Operating Procedures | 59 |
| g3-propagation.qmd | G3 | Radio Wave Propagation | 37 |
| g4-practices.qmd | G4 | Amateur Radio Practices | 60 |
| g5-electrical.qmd | G5 | Electrical Principles | 40 |
| g6-components.qmd | G6 | Circuit Components | 23 |
| g7-circuits.qmd | G7 | Practical Circuits | 38 |
| g8-signals.qmd | G8 | Signals and Emissions | 42 |
| g9-antennas.qmd | G9 | Antennas and Feed Lines | 46 |
| g0-safety.qmd | G0 | Electrical and RF Safety | 25 |

---

## Content Generation

All `.qmd` content is generated by Claude directly (no API calls at runtime, no external generation pipeline). Subagents may be used to parallelize content generation across subelements. Each subagent is responsible for one `.qmd` file: reading the relevant questions from the JSON, writing the pedagogical narrative in logical order, and embedding questions as collapsible callouts at appropriate points.

---

## Deployment

- **Platform:** Posit Connect (same as existing Streamlit app)
- **Build:** `quarto render` run from `learning-center/` produces `_site/`
- **No runtime dependencies:** fully static output, no server-side computation
- **No shared state with Streamlit app:** the two are independent deployments
