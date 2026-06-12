# Ham Radio General Class Learning Center — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a Quarto website at `ham-study/learning-center/` that teaches all General Class exam content in logical pedagogical order, with all 422 exam questions embedded as collapsible callouts.

**Architecture:** Eleven `.qmd` files (one index + one per subelement). No code execution — pure Quarto markdown. Questions from `../data/general_class_questions.json` are embedded as `{.callout-note collapse="true"}` blocks with question text always visible and answers revealed on click (correct answer bolded). Built with `quarto render`, deployed to Posit Connect as a static site.

**Tech Stack:** Quarto 1.9.38, Markdown, Posit Connect

---

## Question callout format (universal — used in ALL content tasks)

Read from JSON: `id`, `question`, `answers` (dict A/B/C/D), `correct` (the letter). Bold the correct answer's line.

```markdown
::: {.callout-note collapse="true"}
## G1A01: On which HF and/or MF amateur bands are there portions where General class licensees cannot transmit?

- A) 60 meters, 30 meters, 17 meters, and 12 meters
- B) 160 meters, 60 meters, 15 meters, and 12 meters
- **C) 80 meters, 40 meters, 20 meters, and 15 meters**
- D) 80 meters, 20 meters, 15 meters, and 10 meters
:::
```

## Verification script (universal — used in ALL content tasks)

Replace `GN` and `gn-filename.qmd` with the subelement and file for each task:

```bash
uv run python -c "
import json
with open('../data/general_class_questions.json') as f:
    qs = json.load(f)
ids = [q['id'] for q in qs if q['subelement'] == 'GN']
with open('gn-filename.qmd') as f:
    content = f.read()
missing = [qid for qid in ids if qid not in content]
if missing:
    print('MISSING:', missing)
else:
    print('All', len(ids), 'questions present')
"
```

---

## Task 1: Scaffold the Quarto project

**Files:**
- Create: `learning-center/_quarto.yml`
- Create: `learning-center/.gitignore`

- [ ] **Step 1: Create the directory**

```bash
mkdir -p /Users/matt/Projects/Development/ham-study/learning-center
```

- [ ] **Step 2: Write `_quarto.yml`**

`learning-center/_quarto.yml`:
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
      - section: "Regulations"
        contents:
          - g1-rules.qmd
          - g2-operating.qmd
      - section: "Propagation & Practices"
        contents:
          - g3-propagation.qmd
          - g4-practices.qmd
      - section: "Electronics"
        contents:
          - g5-electrical.qmd
          - g6-components.qmd
          - g7-circuits.qmd
      - section: "Signals & Antennas"
        contents:
          - g8-signals.qmd
          - g9-antennas.qmd
      - section: "Safety"
        contents:
          - g0-safety.qmd

format:
  html:
    theme: cosmo
    toc: true
    toc-location: right
    toc-depth: 3
```

- [ ] **Step 3: Write `.gitignore`**

`learning-center/.gitignore`:
```
_site/
_freeze/
.quarto/
```

- [ ] **Step 4: Commit**

```bash
git -C /Users/matt/Projects/Development/ham-study add learning-center/_quarto.yml learning-center/.gitignore
git -C /Users/matt/Projects/Development/ham-study commit -m "feat: scaffold Quarto learning center project"
```

---

## Task 2: Create index.qmd

**Files:**
- Create: `learning-center/index.qmd`

- [ ] **Step 1: Write `index.qmd`**

`learning-center/index.qmd`:

```markdown
---
title: "General Class Ham Radio — Learning Center"
---

This site teaches the complete content of the FCC Amateur Radio General Class (Element 3) exam from first principles. It is a textbook with inline self-checks — concepts are introduced in logical order, and exam questions appear only after the knowledge needed to answer them has been presented.

## How to use this site

Navigate using the sidebar. Work through each page in order, or jump to a topic you want to study. When you encounter a question box, you have seen everything you need to answer it. Click the box to reveal the answer choices — the **bolded** choice is correct.

::: {.callout-note collapse="true"}
## Example: click to reveal the answer choices

- A) This is an incorrect answer
- **B) This is the correct answer**
- C) This is an incorrect answer
- D) This is an incorrect answer
:::

## Contents

| Section | Topic | Questions |
|---|---|---|
| [G1: Commission's Rules](g1-rules.qmd) | FCC regulations, privileges, licensing | 52 |
| [G2: Operating Procedures](g2-operating.qmd) | On-air conduct, modes, nets, digital | 59 |
| [G3: Radio Wave Propagation](g3-propagation.qmd) | Ionosphere, skip, MUF, solar effects | 37 |
| [G4: Amateur Radio Practices](g4-practices.qmd) | Station setup, test equipment, interference | 60 |
| [G5: Electrical Principles](g5-electrical.qmd) | Ohm's Law, AC, impedance, power, dB | 40 |
| [G6: Circuit Components](g6-components.qmd) | Resistors, capacitors, diodes, transistors | 23 |
| [G7: Practical Circuits](g7-circuits.qmd) | Power supplies, amplifiers, filters | 38 |
| [G8: Signals and Emissions](g8-signals.qmd) | AM, FM, SSB, digital modulation, bandwidth | 42 |
| [G9: Antennas and Feed Lines](g9-antennas.qmd) | Dipoles, verticals, Yagi, coax, SWR | 46 |
| [G0: Electrical and RF Safety](g0-safety.qmd) | RF exposure, electrical safety, grounding | 25 |
```

- [ ] **Step 2: Render**

```bash
cd /Users/matt/Projects/Development/ham-study/learning-center && quarto render index.qmd
```

Expected: no errors.

- [ ] **Step 3: Commit**

```bash
git -C /Users/matt/Projects/Development/ham-study add learning-center/index.qmd
git -C /Users/matt/Projects/Development/ham-study commit -m "feat: add learning center index page"
```

---

## Task 3: Write G1 — Commission's Rules (52 questions)

**Files:**
- Create: `learning-center/g1-rules.qmd`

G1 is a regulations section. Explain the *why* behind each rule before stating it. Use mnemonics where values must be memorized. Read all G1 questions first, then write the file.

- [ ] **Step 1: Read G1 questions**

```bash
uv run python -c "
import json
with open('../data/general_class_questions.json') as f:
    qs = json.load(f)
for q in [x for x in qs if x['subelement'] == 'G1']:
    print(q['id'], '|', q['question'])
    for k,v in q['answers'].items():
        prefix = '**' if k == q['correct'] else ''
        suffix = '**' if k == q['correct'] else ''
        print(f'  {prefix}{k}) {v}{suffix}')
    print()
"
```

- [ ] **Step 2: Write `g1-rules.qmd`**

Create `learning-center/g1-rules.qmd`. Frontmatter:
```yaml
---
title: "G1: Commission's Rules"
---
```

Write the following sections in order. After teaching the concepts in each section, embed the relevant questions as collapsible callouts (question text in header, all four answer choices in body with correct one bolded).

**Section 1 — The amateur radio license system**

Explain: The FCC issues three tiers of amateur license: Technician, General, and Amateur Extra. Each tier grants access to more spectrum and more operating modes. "Privileges" in this context means which frequencies and modes a licensee may use. Part 97 of the FCC Code of Federal Regulations (CFR Title 47, Part 97) governs amateur radio entirely. The FCC does not administer exams directly — exams are given by Volunteer Examiners (VEs).

Embed questions about license structure and the purpose of the Amateur Radio Service.

**Section 2 — Primary vs. secondary frequency allocations**

Explain: The radio spectrum is divided internationally by the ITU (International Telecommunication Union) into three regions. North America, Central America, and South America are ITU Region 2. Within each region, frequency bands are allocated to various radio services. A service may be designated as *primary* or *secondary* on a given band. Secondary users must not cause harmful interference to primary users and must accept any interference from primary users — they operate "at sufferance."

Embed: G1A06, G1E06.

**Section 3 — General class HF band privileges: where you can transmit**

Explain: The amateur HF spectrum (3–30 MHz) is divided into bands named by approximate wavelength. Within each band, different license classes are allocated to different sub-segments. Most HF bands give General class full access, but four bands have upper portions (typically the CW sub-bands) exclusive to Amateur Extra: 80m (3.5–4.0 MHz), 40m (7.0–7.3 MHz), 20m (14.0–14.35 MHz), and 15m (21.0–21.45 MHz).

Mnemonic: **"Eight, Four, Two, One-Five"** — 80m, 40m, 20m, 15m are the four restricted bands.

On the 60-meter band (5 channels near 5 MHz), General class operation is permitted but subject to special rules: only USB phone, one specific channel at a time, and a 100W PEP limit.

Embed: G1A01, G1A05, G1A07, G1A08, G1A09, G1A10, G1A11, G1C04.

**Section 4 — Mode restrictions: CW-only and no-phone segments**

Explain: "Mode" refers to the method of encoding information onto a radio signal. CW (Continuous Wave) is Morse code. Phone means voice. Image means video or fax (SSTV/facsimile). The 30-meter band (10.100–10.150 MHz) is special: it is narrow and shared with other services, so the FCC restricts it to CW and data only — no phone, no image. Some lower edges of HF bands are CW-only segments where General class phone operation is not permitted even though General class has access to those frequencies for CW.

Embed: G1A02, G1A03.

**Section 5 — Transmitter power limits**

Explain: The FCC measures amateur transmitter power in PEP — Peak Envelope Power — which is the average power during one complete cycle at the highest-amplitude point of a modulated signal. The standard HF limit is 1500 W PEP. Exceptions: the 30-meter band is limited to 200 W PEP; the 60-meter band is limited to 100 W PEP ERP (effective radiated power). Part 97 also requires using the minimum power necessary to carry out the communication ("good amateur practice").

Mnemonic: **"30m → 200W, 60m → 100W"** — both special bands have reduced power limits.

The FCC specifies PEP as the measurement standard (not average power, not peak power). G1C11 tests this directly.

Embed: G1C01, G1C02, G1C05, G1C06, G1C11.

**Section 6 — Bandwidth limits and new digital protocols**

Explain: FCC rules specify maximum bandwidth for emissions. For data/digital signals below 30 MHz, the limit is typically 2.8 kHz. Before using a new digital protocol on the air, the protocol specification must be publicly available (so others can identify the signal) — but no FCC approval is required.

Embed: G1C03, G1C07.

**Section 7 — Antenna structures and beacon stations**

Explain: Antenna structures over 200 feet above ground level (AGL) near airports require FAA notification. The threshold for notification near a public-use airport varies by distance from the runway. Beacon stations (automated, unattended transmitters that help assess propagation) have their own rules: 100 W maximum power, must transmit only on certain frequencies, must comply with ID rules.

Embed: G1B01, G1B02, G1B03, G1B09, G1B10.

**Section 8 — One-way transmissions and broadcasting**

Explain: Amateur radio is a two-way communication service. Broadcasting (transmissions intended for the general public) is prohibited. However, certain one-way transmissions are permitted: control signals to model aircraft/craft, telemetry, beacon signals, and transmissions to assist in emergency communications.

Also: state and local governments may only regulate amateur antennas under "reasonable accommodation" — they cannot simply ban antennas, but may impose restrictions that reasonably balance community interests with amateur radio needs (PRB-1 federal preemption).

Embed: G1B04, G1B05, G1B06, G1B07, G1B08, G1B11.

**Section 9 — Control operators and control types**

Explain: Every transmitting amateur station must have a designated *control operator* — a licensed amateur who is responsible for the station's proper operation. The station's privileges are limited to those of the control operator's license class. A *control point* is the location where the control operator function is performed. Three types of control exist: local control (operator physically present), remote control (operator elsewhere, direct real-time link), and automatic control (no operator present or needed, station operates by itself within defined rules).

Embed: G1E03, G1E04, G1E11, G1D05, G1D12.

**Section 10 — Remote control operations**

Explain: A remotely controlled station is one where the control point is not at the station location — the operator uses a real-time communications link (internet, phone, radio) to control it. The operator must hold a license appropriate for the frequencies used. When operating a US station remotely from outside the US, the control operator must hold a US license. When operating a foreign station from the US, the operator must hold both a US license and follow the rules of the foreign country.

Embed: G1D05, G1D12.

**Section 11 — Third-party communications**

Explain: A *third party* is someone who is not a licensed amateur radio operator, whose message is transmitted via amateur radio on their behalf. Third-party traffic (passing such messages) is only permitted with countries that have a third-party agreement with the United States. A person who is a former amateur licensee whose license was revoked, or who has been convicted of certain crimes, cannot participate as a third party.

During a declared communications emergency, third-party restrictions may be relaxed.

Embed: G1E01, G1E05, G1E12.

**Section 12 — Special frequencies and spread spectrum**

Explain: The 2.4 GHz amateur band overlaps with the unlicensed Wi-Fi spectrum. Amateurs may communicate with non-licensed Wi-Fi devices in limited sub-bands. Spread spectrum is a special mode where the signal is deliberately spread across a wide bandwidth; amateur SS operation requires 10 W maximum PEP.

Certain beacon and propagation-assessment frequencies (14.100, 18.110, 21.150, 24.930, 28.200 MHz) are used by the International Beacon Project — amateurs should avoid transmitting on them.

Embed: G1E07, G1E08, G1E10.

**Section 13 — Volunteer Examiner system**

Explain: The FCC Amateur Radio exam system is administered by Volunteer Examiners (VEs) accredited through Volunteer Examiner Coordinators (VECs). To be a VE you must hold a General or higher class license, be at least 18 years old, and not be related to the candidate. A minimum of 3 accredited VEs must be present at each exam session. A CSCE (Certificate of Successful Completion of Examination) is valid for 365 days — if you pass an element but don't get your license updated in time, you may need to retest. An expired license within 2 years of expiration can be reinstated without retesting (grace period renewal); after that, full retesting is required.

Embed: G1D01, G1D02, G1D03, G1D04, G1D06, G1D07, G1D08, G1D09, G1D10, G1D11.

**Section 14 — RACES and ARES emergency communications**

Explain: RACES (Radio Amateur Civil Emergency Service) is an FCC-defined service operating under civil defense authority. RACES drills may be conducted no more than 1 hour per week without special authorization (that is a G2B topic but logically fits with emergency rules). ARES (Amateur Radio Emergency Service) is an ARRL-organized group — not FCC-defined — with broader activation authority. A licensed amateur may belong to both. During an actual disaster, any station may transmit on any frequency to save lives.

The 10-meter band (28–29.7 MHz) has a portion (29.5–29.7 MHz) available for repeater use.

Embed: G1E02.

- [ ] **Step 3: Verify all 52 G1 questions present**

```bash
uv run python -c "
import json
with open('../data/general_class_questions.json') as f:
    qs = json.load(f)
ids = [q['id'] for q in qs if q['subelement'] == 'G1']
with open('g1-rules.qmd') as f:
    content = f.read()
missing = [qid for qid in ids if qid not in content]
if missing:
    print('MISSING:', missing)
else:
    print('All', len(ids), 'G1 questions present')
"
```

Expected: `All 52 G1 questions present`

- [ ] **Step 4: Render**

```bash
cd /Users/matt/Projects/Development/ham-study/learning-center && quarto render g1-rules.qmd
```

Expected: no errors.

- [ ] **Step 5: Commit**

```bash
git -C /Users/matt/Projects/Development/ham-study add learning-center/g1-rules.qmd
git -C /Users/matt/Projects/Development/ham-study commit -m "feat: add G1 Commission's Rules learning page"
```

---

## Task 4: Write G2 — Operating Procedures (59 questions)

**Files:**
- Create: `learning-center/g2-operating.qmd`

G2 covers on-air operating conventions. Mix of memorization (Q-codes, prosigns, phonetics) and procedure. Use mnemonics for Q-code meanings.

- [ ] **Step 1: Read G2 questions**

```bash
uv run python -c "
import json
with open('../data/general_class_questions.json') as f:
    qs = json.load(f)
for q in [x for x in qs if x['subelement'] == 'G2']:
    print(q['id'], '|', q['question'])
    for k,v in q['answers'].items():
        prefix = '**' if k == q['correct'] else ''
        suffix = '**' if k == q['correct'] else ''
        print(f'  {prefix}{k}) {v}{suffix}')
    print()
"
```

- [ ] **Step 2: Write `g2-operating.qmd`**

`learning-center/g2-operating.qmd`, frontmatter:
```yaml
---
title: "G2: Operating Procedures"
---
```

**Section 1 — Making contact: the basics**

Explain how HF contacts work: a station calls CQ (a general call to any station), another station responds, they exchange call signs and signal reports, then converse. "CQ DX" specifically invites contacts with distant stations — nearby stations should not respond. PTT (Push To Talk) means manually keying the transmitter; VOX (Voice Operated Transmission) means the transmitter keys automatically when you speak. VOX is convenient but can cause false triggering from background noise or received audio.

Embed: G2A11, G2A10, G2D05, G2D06, G2D08, G2D09, G2D10, G2D11.

**Section 2 — Voice modes on HF: AM vs. SSB**

Explain: AM (Amplitude Modulation) encodes audio by varying the power of the carrier wave. It produces a carrier plus two sidebands, occupying about 6 kHz of spectrum. SSB (Single Sideband) suppresses the carrier and one sideband, transmitting only the other sideband — about 3 kHz wide, and 4–6 dB more efficient. SSB dominates on HF because it's more spectrum-efficient and has better range per watt.

Convention: LSB (Lower Sideband) is used on 160m, 75m, and 40m. USB (Upper Sideband) is used on 20m, 17m, 15m, 12m, and 10m. This is a convention, not an FCC rule, but nearly universally followed.

Embed: G2A01, G2A02, G2A03, G2A04, G2A05, G2A06, G2A07, G2A09.

**Section 3 — Transceiver ALC and proper drive**

Explain: ALC (Automatic Level Control) is a feedback circuit that prevents the transmitter from being overdriven. On SSB, proper ALC means the ALC meter deflects only on voice peaks — consistently pegged ALC means the audio is too hot, causing splatter and distortion. The DRIVE control sets how much signal goes into the power amplifier stage; adjust for proper ALC behavior. When using AFSK (audio-frequency-shift-keying) for digital modes, ALC should be inactive or minimally active because the constant digital audio would cause ALC to compress the signal incorrectly.

Embed: G2A12, G4A11 (note: G4A11 lives in G4, embed it there instead — do not move it here).

**Section 4 — Operating courtesy and frequency access**

Explain: No one "owns" an amateur frequency. Before transmitting on a frequency, listen first to ensure it's clear. Announce "is this frequency in use?" before calling CQ. If a contact is already in progress on your desired frequency, move. Minimum frequency separation: 150–500 Hz for CW stations, at least 3 kHz for SSB stations (to avoid splatter). If propagation changes and your contact causes interference, you should QSY (move to another frequency).

Embed: G2B01, G2B02, G2B03, G2B04, G2B05, G2B06, G2B07, G2B08.

**Section 5 — Net operations and RACES**

Explain: A *net* is a scheduled on-air meeting of a group of stations. A *net control station (NCS)* manages the net — stations check in to the NCS, not directly to each other. Good net control keeps traffic flowing efficiently. RACES nets have special rules: only licensed amateurs may serve as control operators during RACES; RACES training drills are limited to 1 hour per week unless special authorization is obtained.

Embed: G2B09, G2B10, G2B11.

**Section 6 — CW operating procedures**

Explain: CW (Continuous Wave) is Morse code. On HF, CW occupies the lowest sub-band of most amateur allocations. Speed is measured in WPM (words per minute). When answering a CQ in CW, send at the same speed as the calling station — sending faster than the other operator can copy is rude and ineffective.

*Zero beat* means your transmit frequency matches the receive frequency of the other station. In CW, if two stations are not zero-beat, they hear different tones and may not find each other.

*Full break-in (QSK)*: in QSK, the transceiver switches between transmit and receive fast enough to hear signals between code elements — the operator can hear a station break in at any point. Without QSK (semi-break-in), the operator only receives audio between transmissions.

**Q-codes** (mnemonic: Q-codes are questions when sent with a "?", statements when sent alone):
- QRS — Send more slowly ("Q-Reduce Speed")
- QRL — Is this frequency in use? ("Q-Receive Listening")
- QSL — I acknowledge receipt ("Q-Sign Letter" — like a QSL card)
- QRN — I'm troubled by static noise ("Q-Radio Noise")
- QRV — I am ready ("Q-Ready Verified")
- QSK — Full break-in CW

**Prosigns** (procedure signals, sent as one character):
- AR — End of message (+ sign) ("All-Reception complete")
- SK — End of contact, signing off
- KN — Invitation for the named station only to reply ("K Named")
- BK — Break, brief interruption invited

Adding "C" to an RST report indicates a chirpy signal.

Embed: G2C01, G2C02, G2C03, G2C04, G2C05, G2C06, G2C07, G2C08, G2C09, G2C10, G2C11.

**Section 7 — NATO phonetic alphabet and station logs**

Explain: NATO phonetics are used to spell out letters unambiguously: Alpha, Bravo, Charlie, Delta, Echo, Foxtrot, Golf, Hotel, India, Juliet, Kilo, Lima, Mike, November, Oscar, Papa, Quebec, Romeo, Sierra, Tango, Uniform, Victor, Whiskey, X-ray, Yankee, Zulu. These are the standard — not improvised alternatives.

RST reports: Readability (1–5), Signal strength (1–9), Tone (1–9, CW only). Exchanged early in a contact to establish link quality.

Station logs: Not required by FCC rules for most amateur operation, but strongly encouraged. During contests, required by contest rules.

Embed: G2D07, G2D04.

**Section 8 — Volunteer Monitor Program**

Explain: The Volunteer Monitor (VM) Program is an ARRL program (not FCC-run) where experienced operators help identify and address on-air operating problems, such as stations with improper signals, unidentified transmissions, or interference issues. VMs can use direction-finding to locate a continuously broadcasting (stuck) station.

Embed: G2D01, G2D02, G2D03.

**Section 9 — Digital modes on HF**

Explain: Digital modes use audio tones generated by a computer's soundcard, fed into the microphone input of an SSB transceiver — called AFSK (Audio Frequency Shift Keying). The SSB radio carries those tones as if they were voice. The result is a digital signal on the air.

*RTTY (RadioTeletype)*: The oldest digital mode. Uses two tones (mark and space) — FSK. Standard shift in amateur RTTY is 170 Hz between the two tones. Encoded in Baudot code (5-bit characters). If tones are reversed (mark/space swapped), the received text is garbage — this is a common problem.

*PSK31*: Phase Shift Keying at 31 baud. Very narrow (~31 Hz bandwidth). Uses Varicode character encoding. Efficient but requires accurate frequency tuning. A PSK31 waterfall display shows characteristic "rail lines" if overdriven (key clicks on either side).

*FT8/FT4/JT65/JT9*: Weak-signal digital modes developed for extreme propagation conditions. Operate on USB. FT8 uses 8-GFSK modulation. FT8 requires accurate computer clock sync (within ~1 second). Signal reports in FT8 are in dB SNR (e.g., +3 means 3 dB above the noise floor). FT8 occupies the range 14.074 MHz (20m dial), always on USB. Requires a synchronized transmission protocol — you cannot simply "join" a contact in progress; PACTOR and VARA are ARQ protocols where joining mid-contact would disrupt the error correction.

*Winlink*: Email-over-radio system. Uses a Remote Message Server (RMS, also called a gateway) to relay messages between radio and the internet. Used for emergency communications.

*AREDN (Amateur Radio Emergency Data Network)*: Mesh networking using modified Wi-Fi equipment for broadband emergency data networks.

Embed: G2E01, G2E03, G2E04, G2E05, G2E06, G2E07, G2E08, G2E09, G2E10, G2E11, G2E12, G2E13, G2E14, G2E15.

- [ ] **Step 3: Verify all 59 G2 questions present**

```bash
uv run python -c "
import json
with open('../data/general_class_questions.json') as f:
    qs = json.load(f)
ids = [q['id'] for q in qs if q['subelement'] == 'G2']
with open('g2-operating.qmd') as f:
    content = f.read()
missing = [qid for qid in ids if qid not in content]
if missing:
    print('MISSING:', missing)
else:
    print('All', len(ids), 'G2 questions present')
"
```

Expected: `All 59 G2 questions present`

- [ ] **Step 4: Render**

```bash
cd /Users/matt/Projects/Development/ham-study/learning-center && quarto render g2-operating.qmd
```

- [ ] **Step 5: Commit**

```bash
git -C /Users/matt/Projects/Development/ham-study add learning-center/g2-operating.qmd
git -C /Users/matt/Projects/Development/ham-study commit -m "feat: add G2 Operating Procedures learning page"
```

---

## Task 5: Write G3 — Radio Wave Propagation (37 questions)

**Files:**
- Create: `learning-center/g3-propagation.qmd`

G3 is a technical section about physics. Define every term. Use analogies.

- [ ] **Step 1: Read G3 questions**

```bash
uv run python -c "
import json
with open('../data/general_class_questions.json') as f:
    qs = json.load(f)
for q in [x for x in qs if x['subelement'] == 'G3']:
    print(q['id'], '|', q['question'])
    for k,v in q['answers'].items():
        prefix = '**' if k == q['correct'] else ''
        suffix = '**' if k == q['correct'] else ''
        print(f'  {prefix}{k}) {v}{suffix}')
    print()
"
```

- [ ] **Step 2: Write `g3-propagation.qmd`**

`learning-center/g3-propagation.qmd`, frontmatter:
```yaml
---
title: "G3: Radio Wave Propagation"
---
```

**Section 1 — The ionosphere: what it is and why it matters**

Explain from first principles: The atmosphere extends from the ground to roughly 600 km altitude. Above ~60 km, solar ultraviolet (UV) and X-ray radiation ionizes gas molecules — stripping electrons free. This creates a region of free electrons and ions called the *ionosphere*. Free electrons can refract (bend) radio waves traveling through them, and under the right conditions, completely reflect them back to Earth — like a mirror in the sky. This makes very long-distance communication possible on HF.

**Section 2 — Ionospheric layers**

Explain the four layers:

*D layer* (60–90 km): Forms only during daylight. Absorbs radio waves rather than reflecting them — particularly harmful to signals below ~10 MHz. Signals that would otherwise skip via the F layer are attenuated by D layer absorption during the day. The D layer disappears at night, which is why 40m, 80m, and 160m open up dramatically after sunset.

*E layer* (90–120 km): Reflects signals in the 25–100 MHz range under normal conditions. Sporadic-E (Es) is a patchy, unpredictable ionization that can reflect signals as high as 100+ MHz, enabling brief long-distance VHF contacts.

*F layer* (150–500 km): The most important layer for HF DX (long-distance) communication. Splits into F1 and F2 sub-layers during daylight; merges into a single F layer at night. The F2 layer is the highest and most stable — because it's farther from Earth, it can produce much longer skip distances than E layer. F2 layer skip typically reaches 3,000–4,000 km in a single hop.

Mnemonic: **"D is Daytime Damper, E is Erratic Enabler, F is the Far-reaching one"**

Embed: G3C01, G3C03, G3C05, G3C11.

**Section 3 — Skip distance, skip zone, and the critical angle**

Explain: When a signal leaves the antenna at a low angle, it travels farther before hitting the ionosphere and is reflected farther away. At a high (near-vertical) angle, it hits the ionosphere overhead and comes back nearby — this is NVIS (Near Vertical Incidence Skywave), useful for regional coverage within a few hundred km.

*Skip distance*: The minimum distance at which a given frequency is reflected back from the ionosphere. Closer than the skip distance, only ground wave reaches you.

*Skip zone*: The silent zone between the ground-wave range (~50 km) and the skip-distance where neither ground wave nor sky wave arrives.

*Critical frequency*: The highest frequency that is reflected straight up (vertical incidence) at the ionosphere. At angles other than vertical, higher frequencies can be reflected (because the effective layer thickness is longer). The *critical angle* is the steepest angle at which a signal can still be reflected — signals above this angle pass through the ionosphere.

*Maximum Usable Frequency (MUF)*: The highest frequency that can be refracted back to Earth for a given path and ionospheric conditions. Signals above the MUF pass through the ionosphere into space. The MUF depends on solar activity, time of day, season, and the path geometry. E-layer MUF: ~150 km single-hop distance maximum. F2-layer MUF: ~4,000 km single-hop.

*Lowest Usable Frequency (LUF)*: The lowest frequency that has enough signal strength to be usable on a given path — determined by D-layer absorption (which increases for lower frequencies). When LUF > MUF, no skywave propagation is possible on that path.

Embed: G3B01, G3B02, G3B03, G3B04, G3B05, G3B06, G3B07, G3B08, G3B09, G3B10, G3B11, G3B12, G3C02, G3C04, G3C10.

**Section 4 — Solar activity and its effects on HF propagation**

Explain: The ionosphere is created and sustained by solar radiation. More solar activity → more ionization → higher MUF → better DX propagation (in general). Solar activity is measured in several ways:

*Sunspot number*: Sunspots are dark magnetic disturbances on the sun's surface. More sunspots → more UV/X-ray → higher F2 layer ionization → higher MUF. The sunspot cycle runs approximately 11 years.

*Solar Flux Index (SFI)*: A daily measurement of solar radio emission at 2.8 GHz (10.7 cm wavelength). Higher SFI correlates with more ionospheric ionization. SFI > 150 generally means excellent HF conditions; SFI < 70 means poor conditions.

*Sudden Ionospheric Disturbance (SID)*: A solar flare emits a burst of X-rays that reaches Earth in about 8 minutes (speed of light). This over-ionizes the D layer, causing a sudden blackout on HF — particularly on the sunlit side of Earth, and especially on lower HF bands. Recovery takes tens of minutes.

*Coronal Mass Ejection (CME)*: A massive eruption of solar plasma. Takes 1–3 days to reach Earth (particles travel slower than light). CMEs cause geomagnetic storms.

*Geomagnetic storm*: Disturbance of Earth's magnetic field by a CME or other solar wind event. Measured by the *K-index* (a 3-hour quasi-logarithmic index, 0–9; K ≥ 5 is a geomagnetic storm) and the *A-index* (a daily linear average, 0–400; A > 50 indicates major disturbance). High geomagnetic activity usually degrades HF propagation at high latitudes but can enable auroral propagation at VHF.

*Rotation cycle*: The sun rotates approximately every 27 days (as seen from Earth). Active solar regions return to face Earth every ~27 days, causing a recurring propagation pattern.

The 20-meter band (14 MHz) is often described as the most reliable DX band — it typically supports worldwide propagation at almost any point in the solar cycle.

Embed: G3A01, G3A02, G3A03, G3A04, G3A05, G3A06, G3A07, G3A08, G3A09, G3A10, G3A11, G3A12, G3A13, G3A14.

**Section 5 — Scatter propagation modes**

Explain: Even in the skip zone, weak signals can arrive via *scatter* — radio energy scattered by irregularities in the ionosphere or troposphere. Scattered signals are weak and often distorted because they arrive via multiple slightly different paths (multipath), causing phase differences that blur the signal.

*Ionospheric scatter*: Scattering from irregularities in the ionosphere. Useful at 20–60 MHz for paths of 800–2000 km.

*Tropospheric scatter*: Scattering from irregularities in the troposphere (lower atmosphere). Useful at VHF/UHF for paths of 300–1000 km.

*Meteor scatter*: Brief ionized trails left by meteors burning up in the atmosphere at ~100 km altitude can reflect VHF signals for fractions of a second to a few seconds. Useful for 6m and 2m operation during meteor showers.

*Short-path vs. long-path*: Every path between two points on Earth has two routes — the shorter great-circle path (short-path) and the longer route going the other way around the globe (long-path). When both paths are open simultaneously, signals arrive with slightly different delays and Doppler shifts — the received signal sounds "hollow" or distorted.

Embed: G3B01, G3C06, G3C07, G3C08, G3C09.

- [ ] **Step 3: Verify all 37 G3 questions present**

```bash
uv run python -c "
import json
with open('../data/general_class_questions.json') as f:
    qs = json.load(f)
ids = [q['id'] for q in qs if q['subelement'] == 'G3']
with open('g3-propagation.qmd') as f:
    content = f.read()
missing = [qid for qid in ids if qid not in content]
if missing:
    print('MISSING:', missing)
else:
    print('All', len(ids), 'G3 questions present')
"
```

- [ ] **Step 4: Render**

```bash
cd /Users/matt/Projects/Development/ham-study/learning-center && quarto render g3-propagation.qmd
```

- [ ] **Step 5: Commit**

```bash
git -C /Users/matt/Projects/Development/ham-study add learning-center/g3-propagation.qmd
git -C /Users/matt/Projects/Development/ham-study commit -m "feat: add G3 Radio Wave Propagation learning page"
```

---

## Task 6: Write G4 — Amateur Radio Practices (60 questions)

**Files:**
- Create: `learning-center/g4-practices.qmd`

G4 is a mix: station equipment controls, test equipment, RFI, and mobile/power. Explain concepts from first principles; define all terms.

- [ ] **Step 1: Read G4 questions**

```bash
uv run python -c "
import json
with open('../data/general_class_questions.json') as f:
    qs = json.load(f)
for q in [x for x in qs if x['subelement'] == 'G4']:
    print(q['id'], '|', q['question'])
    for k,v in q['answers'].items():
        prefix = '**' if k == q['correct'] else ''
        suffix = '**' if k == q['correct'] else ''
        print(f'  {prefix}{k}) {v}{suffix}')
    print()
"
```

- [ ] **Step 2: Write `g4-practices.qmd`**

`learning-center/g4-practices.qmd`, frontmatter:
```yaml
---
title: "G4: Amateur Radio Practices"
---
```

**Section 1 — Transceiver controls and receiver adjustments**

Explain: A modern HF transceiver is a combined transmitter and receiver (transceiver). The receiver section has several adjustable features:

*Notch filter*: A very narrow band-reject filter that removes a single interfering carrier (CW tone or heterodyne whistle) from the received audio without affecting the desired signal.

*Noise blanker*: A circuit that detects brief, strong noise pulses (such as from ignition systems) and blanks the receiver for the duration of the pulse, eliminating the click.

*IF shift*: Shifts the passband of the intermediate frequency (IF) filter up or down in frequency to move an interfering signal out of the passband.

*AGC (Automatic Gain Control)*: Adjusts receiver gain automatically to maintain constant audio output despite widely varying signal strength. Too much AGC on weak signals can cause "pumping" artifacts.

*Noise reduction (DSP)*: Digital Signal Processing-based noise reduction analyzes the received audio and attempts to remove broadband noise. Increasing the level removes more noise but can introduce artifacts — at high levels, weak signals become unintelligible or robotic-sounding.

*Attenuator*: Reduces the signal into the receiver's front end. Useful when a very strong nearby signal is overloading the receiver's front-end circuits. A properly functioning receiver should not need attenuation under normal conditions — using it reduces sensitivity.

*Dual-VFO*: Most modern transceivers have two Variable Frequency Oscillators (VFOs), allowing the operator to set two frequencies and switch between them — useful for monitoring a calling frequency while working split (transmitting on one frequency, receiving on another).

Embed: G4A01, G4A02, G4A03, G4A07, G4A12, G4A13.

**Section 2 — Transmitter controls: ALC, drive, and keying**

Explain:

*ALC (Automatic Level Control)*: A feedback loop from the power amplifier stage back to the earlier drive stages. Its function is to prevent overdrive — if the drive level is too high, the output stage becomes non-linear, generating distortion products (splatter) that interfere with adjacent frequencies. The ALC meter shows ALC activity; it should only deflect on voice peaks for SSB. If it's constantly pegged, the microphone gain or drive is too high.

*Drive/Power control*: Sets how much RF is fed into the final amplifier stage. Adjust to achieve proper ALC behavior and target output power.

*Vacuum tube amplifiers*: Older and high-power amplifiers often use vacuum tubes. The *grid* (input) of the tube is driven by the exciter. The *plate* (output) is tuned using TUNE and LOAD (or COUPLING) controls. Correct plate tuning is found by dipping the plate current to a minimum while peaking output power. The LOAD control adjusts how much power is coupled out — it should be set so the amplifier draws rated plate current at the tuned dip point. Incorrect loading causes the tube to run hot.

*ALC with digital modes*: When transmitting AFSK digital modes, the audio level is constant (unlike speech). ALC, which was designed for speech, will compress the constant digital audio — corrupting the signal. Disable or bypass ALC when using AFSK digital modes; instead set drive level by watching output power.

*Electronic keyer*: An automatic keyer for CW that produces correct dits and dahs at a set speed from a paddle input. Eliminates the need for perfect manual timing.

*QSK delay*: When switching from transmit to receive (especially with a linear amplifier), the amplifier may need a moment to recover before the antenna can safely be connected to the receiver. The delay circuit prevents the receiver from seeing transient switching noise.

Embed: G4A04, G4A05, G4A08, G4A09, G4A10, G4A11.

**Section 3 — Antenna tuner function**

Explain: An antenna tuner (ATU, or "antenna tuning unit," also called a "transceiver matching unit") does NOT tune the antenna itself — it matches the impedance presented by the feedline + antenna system to the 50-ohm output of the transceiver. This improves the SWR the transmitter sees, protecting it from high-SWR shutdowns. Important caveat: a tuner at the transmitter end does NOT reduce losses in the feedline — if the antenna is badly mismatched, there will still be significant loss in the coax. Losses in the feedline become heat.

Embed: G4A06.

**Section 4 — Test equipment**

Explain each instrument:

*Oscilloscope*: Displays voltage vs. time. Has horizontal (time) and vertical (amplitude) channel amplifiers. Allows you to observe signal waveforms, measure frequency, amplitude, and importantly — the keying waveform of a CW transmitter (to check for key clicks or chirp). For checking linearity of an SSB transmitter, use a *two-tone test*: apply two equal-amplitude audio tones simultaneously to the microphone input and observe the RF output envelope. A clean signal shows a trapezoidal envelope; clipping produces a distorted envelope.

*Voltmeter/Multimeter*: Measures voltage, current, and resistance. High input impedance is essential so the meter doesn't load the circuit being measured (changing the voltage). Digital multimeters are more precise; analog meters are better for tracking slowly changing signals or null-detecting (finding zero).

*Directional wattmeter*: Measures both forward power (from transmitter toward antenna) and reflected power (from antenna back toward transmitter), from which SWR is computed.

*Antenna analyzer*: Measures antenna impedance (resistance and reactance) at a given frequency. Must be connected to the antenna (disconnected from the transmitter) to work correctly. Strong nearby transmitters can affect readings.

*Signal generator / frequency counter*: Used to generate known test signals or measure frequency precisely.

Embed: G4B01, G4B02, G4B03, G4B04, G4B05, G4B06, G4B07, G4B08, G4B09, G4B10, G4B11, G4B12, G4B13.

**Section 5 — Grounding, bonding, and RFI**

Explain:

*Safety ground*: The green wire in AC mains wiring. Connects all equipment chassis to earth ground, providing a safe path for fault currents. FCC and NEC require all metal enclosures of station equipment to be grounded.

*RF ground*: A low-impedance connection to earth at RF frequencies, used to complete the antenna circuit for verticals and as a reference potential. A resonant ground connection (a ground wire that is a multiple of λ/4 long) can have high impedance at some frequencies rather than low — this is a problem. Single-point grounding avoids ground loops.

*Ground loops*: When multiple pieces of equipment are connected in a ring (or loop) via both audio cables and their power ground connections, any voltage difference in the ground potential drives current through the audio cable shield, creating hum or noise. Minimize by routing all ground connections to a single point (star grounding).

*RFI (Radio Frequency Interference)*: RF energy getting into audio circuits can cause distortion or interference. Common-mode RF current flows on the outside of a coaxial cable shield and can enter audio equipment. A ferrite bead (choke) on the audio cable can block this common-mode current without affecting the audio signal. An SSB signal entering an audio circuit sounds like garbled speech; a CW signal sounds like an audio tone. High RF voltages can cause RF burns at unintentional contact points in the station (such as a microphone connector).

*RF hot spots*: Can occur if station wiring creates resonances at certain frequencies. Bonding all metal equipment together and using a single-point ground system minimizes this.

Embed: G4C01, G4C02, G4C03, G4C04, G4C05, G4C06, G4C07, G4C08, G4C09, G4C10, G4C11, G4C12.

**Section 6 — Speech processing and S meters**

Explain:

*Speech processor*: A device (hardware or DSP) that compresses the dynamic range of the voice audio — making quiet parts louder and keeping loud parts from clipping. This increases average power output and intelligibility on weak signal paths. Incorrectly set (too much compression) causes splatter and distortion.

*S meter*: The received signal strength meter on a receiver. Calibrated in S units. One S unit = approximately 6 dB change in signal power. S9 corresponds to a received signal of 50 μV across 50 Ω in most receivers. "20 dB over S9" is 100 times more power than S9. To raise the received S meter reading by one S unit requires increasing transmit power by approximately 4× (since power doubles every 3 dB, and one S unit = ~6 dB = 4× power).

*SSB carrier frequency and band edges*: On LSB (Lower Sideband), the displayed carrier frequency is the *upper* edge of the transmitted signal. On USB (Upper Sideband), it's the *lower* edge. A 3 kHz LSB signal displayed at 7.253 MHz occupies 7.250–7.253 MHz. To stay within the phone band on LSB, keep the carrier frequency at least 3 kHz above the lower band edge; on USB, keep it at least 3 kHz below the upper band edge.

Embed: G4D01, G4D02, G4D03, G4D04, G4D05, G4D06, G4D07, G4D08, G4D09, G4D10, G4D11.

**Section 7 — Mobile and portable operation**

Explain:

*Mobile antennas*: A full-size quarter-wave vertical for HF is physically impractical on a vehicle (a λ/4 at 7 MHz is ~10 meters tall). Loading coils are used to electrically lengthen a physically short antenna — the coil adds inductance that resonates the antenna at a lower frequency than its physical length would suggest. A *capacitance hat* (a set of radial wires or a disk at the antenna top) increases the effective electrical length and lowers the required loading inductance, improving efficiency. A *screwdriver antenna* uses a motor-driven coil that can be adjusted in flight to tune to different frequencies. A *corona ball* is a smooth metal ball on the tip of the antenna that reduces the electric field gradient at the tip, preventing corona discharge (which causes noise and power loss) at high power levels.

*Power connections*: A 100W HF transceiver should be connected directly to the vehicle battery via dedicated fused cable — not the cigarette lighter or accessory outlet, which have limited current capacity and share a noisy electrical bus. The auxiliary power outlet/cigarette lighter should be avoided because it's often switched and has limited current rating.

*Vehicle RFI*: Vehicles generate RFI from the ignition system, alternator, fuel injectors, and increasingly from electronic control units. An HF mobile installation often requires careful routing of antenna cables and power leads to minimize pickup of vehicle electrical noise.

*Solar power*: Silicon photovoltaic (solar) cells produce approximately 0.5V open-circuit per cell. A typical solar panel for charging 12V batteries consists of cells in series. A series blocking diode prevents battery from discharging through the solar panel at night. A lithium iron phosphate (LiFePO4) battery requires a specific charge profile — do not connect a standard lead-acid charger or solar charge controller without verifying LiFePO4 compatibility, as overcharging can cause venting or fire.

Embed: G4E01, G4E02, G4E03, G4E04, G4E05, G4E06, G4E07, G4E08, G4E09, G4E10, G4E11.

- [ ] **Step 3: Verify all 60 G4 questions present**

```bash
uv run python -c "
import json
with open('../data/general_class_questions.json') as f:
    qs = json.load(f)
ids = [q['id'] for q in qs if q['subelement'] == 'G4']
with open('g4-practices.qmd') as f:
    content = f.read()
missing = [qid for qid in ids if qid not in content]
if missing:
    print('MISSING:', missing)
else:
    print('All', len(ids), 'G4 questions present')
"
```

- [ ] **Step 4: Render**

```bash
cd /Users/matt/Projects/Development/ham-study/learning-center && quarto render g4-practices.qmd
```

- [ ] **Step 5: Commit**

```bash
git -C /Users/matt/Projects/Development/ham-study add learning-center/g4-practices.qmd
git -C /Users/matt/Projects/Development/ham-study commit -m "feat: add G4 Amateur Radio Practices learning page"
```

---

## Task 7: Write G5 — Electrical Principles (40 questions)

**Files:**
- Create: `learning-center/g5-electrical.qmd`

G5 is the most mathematically demanding section. Define everything from first principles. Include worked numerical examples for every formula type tested.

- [ ] **Step 1: Read G5 questions**

```bash
uv run python -c "
import json
with open('../data/general_class_questions.json') as f:
    qs = json.load(f)
for q in [x for x in qs if x['subelement'] == 'G5']:
    print(q['id'], '|', q['question'])
    for k,v in q['answers'].items():
        prefix = '**' if k == q['correct'] else ''
        suffix = '**' if k == q['correct'] else ''
        print(f'  {prefix}{k}) {v}{suffix}')
    print()
"
```

- [ ] **Step 2: Write `g5-electrical.qmd`**

`learning-center/g5-electrical.qmd`, frontmatter:
```yaml
---
title: "G5: Electrical Principles"
---
```

**Section 1 — The four fundamental electrical quantities**

Define: Electric *charge* (measured in coulombs) is the property of matter that causes electromagnetic force. *Current* (I, measured in amperes = coulombs/second) is the flow of charge. *Voltage* (V or E, measured in volts) is the potential energy difference per unit charge — the "pressure" driving current. *Resistance* (R, measured in ohms, Ω) is opposition to current flow in a material. Higher resistance → less current for the same voltage.

**Section 2 — Ohm's Law and DC power**

Ohm's Law: V = I × R (voltage equals current times resistance). Rearranges to: I = V/R and R = V/I.

Power: P = V × I (watts = volts × amperes). Combined with Ohm's Law: P = I²R = V²/R.

Worked examples (matching the types tested in G5B):
- 400V across 800Ω: P = V²/R = 160,000/800 = 200W
- 12V, 0.2A: P = 12 × 0.2 = 2.4W
- 7mA through 1250Ω: P = I²R = (0.007)² × 1250 = 0.0614W

Embed: G5B02, G5B03, G5B04, G5B05.

**Section 3 — Resistors in series and parallel**

Series: R_total = R1 + R2 + R3... (resistances add).

Parallel: 1/R_total = 1/R1 + 1/R2 + 1/R3... Equivalently for two resistors: R_total = (R1 × R2)/(R1 + R2).

For parallel resistors, total current is the sum of branch currents.

Worked examples:
- 10Ω, 20Ω, 50Ω in parallel: 1/R = 1/10 + 1/20 + 1/50 = 10/100 + 5/100 + 2/100 = 17/100; R = 100/17 ≈ 5.9Ω
- 100Ω and 200Ω in parallel: R = (100×200)/(100+200) = 20000/300 ≈ 66.7Ω

Embed: G5B02, G5C03, G5C04.

**Section 4 — AC electricity: frequency, period, RMS, and peak**

Explain: AC (Alternating Current) reverses direction periodically. Household current in the US is 60 Hz — it completes 60 full cycles per second. A cycle consists of one positive half and one negative half.

*Peak voltage* (Vpeak): The maximum instantaneous voltage.
*Peak-to-peak voltage* (Vpp): The total swing from negative peak to positive peak = 2 × Vpeak.
*RMS voltage* (Vrms): Root Mean Square — the value that produces the same power dissipation as an equivalent DC voltage. For a sine wave: Vrms = Vpeak / √2 ≈ Vpeak × 0.707.

Worked examples:
- Vrms = 120V → Vpeak = 120 × √2 ≈ 170V; Vpp = 340V
- Vpeak = 17V → Vrms = 17 × 0.707 ≈ 12V
- Vpp = 200V → Vpeak = 100V → Vrms = 70.7V

PEP (Peak Envelope Power): For SSB and other signals, PEP = (Vpeak)² / (2 × R) = (Vpp/2)² / (2R) = Vpp² / (8R). For a 50Ω load:
- 200V peak-to-peak: PEP = 200² / (8 × 50) = 40000/400 = 100W
- 500V peak-to-peak: PEP = 500² / (8 × 50) = 250000/400 = 625W

For an unmodulated carrier (constant amplitude), PEP = average power. Ratio = 1:1. For SSB speech, average power is much less than PEP.

Embed: G5B06, G5B07, G5B08, G5B09, G5B11, G5B12, G5B13, G5B14.

**Section 5 — Decibels (dB)**

Explain: The decibel is a logarithmic ratio used to express power gain or loss. For power: dB = 10 × log₁₀(P2/P1). For voltage: dB = 20 × log₁₀(V2/V1).

Key relationships to memorize:
- +3 dB = 2× power
- -3 dB = ½ power (about 21% loss — actually 50% loss. 1 dB loss ≈ 20% power loss)
- +10 dB = 10× power
- -10 dB = 1/10 power
- +6 dB = 4× power (2× voltage)

Worked example: 1200W into a 50Ω dummy load → Vrms = √(P×R) = √(1200×50) = √60000 ≈ 245V.

One S unit = 6 dB = 4× power (relevant for G4D questions about S meters — embed those in G4, not here).

Embed: G5B01, G5B10.

**Section 6 — Capacitors and capacitive reactance**

Explain: A *capacitor* stores energy in an electric field between two conducting plates separated by a dielectric (insulator). Capacitance (C) is measured in farads (F); practical values are in microfarads (μF) or picofarads (pF). Capacitors in parallel add: C_total = C1 + C2. Capacitors in series: 1/C_total = 1/C1 + 1/C2.

For AC, a capacitor does not block the signal — it passes AC but blocks DC. The *capacitive reactance* Xc = 1/(2πfC) (ohms) decreases as frequency increases — a capacitor becomes a better conductor at higher frequencies. This is opposition to AC current flow, analogous to resistance.

Worked examples (from G5C questions):
- 20μF and 50μF in series: 1/C = 1/20 + 1/50 = 5/100 + 2/100 = 7/100; C = 100/7 ≈ 14.3μF
- Two 5nF in parallel + 750pF: C = 5000pF + 5000pF + 750pF = 10750pF = 10.75nF
- Three 100μF in series: 1/C = 3/100; C = 100/3 ≈ 33.3μF

Embed: G5A04, G5A06, G5C08, G5C09, G5C12, G5C13.

**Section 7 — Inductors and inductive reactance**

Explain: An *inductor* stores energy in a magnetic field created by current flowing through a coil of wire. Inductance (L) is measured in henries (H). Inductors in series add: L_total = L1 + L2. Inductors in parallel: 1/L_total = 1/L1 + 1/L2.

*Inductive reactance*: XL = 2πfL (ohms) increases as frequency increases — an inductor becomes a better blocker at higher frequencies. This is the opposite behavior from a capacitor.

Worked examples:
- Three 10mH in parallel: 1/L = 3/10; L = 10/3 ≈ 3.33mH
- 20mH in series with 60mH: L = 80mH

Embed: G5A03, G5A05, G5C10, G5C11, G5C14.

**Section 8 — Impedance and admittance**

Explain: *Impedance* (Z, measured in ohms) is the total opposition to AC current flow, combining resistance (R) and reactance (X): for a series circuit, Z = √(R² + X²). When X is inductive, it's positive; when capacitive, it's negative. At resonance, XL = XC and they cancel — total impedance is purely resistive (Z = R). The symbol for reactance is X.

*Admittance* (Y, measured in siemens) is the inverse of impedance: Y = 1/Z. It's the AC equivalent of conductance.

*Impedance matching devices* at RF include: L-networks, pi-networks, T-networks, transmission line transformers (baluns/ununs), and quarter-wave transmission line sections.

Embed: G5A01, G5A02, G5A07, G5A08, G5A09, G5A10, G5A11, G5A12.

**Section 9 — Transformers**

Explain: A transformer consists of two coupled inductors (primary and secondary windings) sharing a common magnetic core. When AC flows in the primary, the changing magnetic field induces a voltage in the secondary. The voltage ratio equals the turns ratio: V2/V1 = N2/N1. An ideal transformer conserves power: V1×I1 = V2×I2. Therefore current scales inversely with voltage — a step-up transformer in voltage is a step-down in current.

The primary winding of a step-up transformer carries more current than the secondary, so it needs thicker wire despite having fewer turns.

Impedance transformation: Z2/Z1 = (N2/N1)². To match 600Ω to 50Ω: turns ratio = √(600/50) = √12 ≈ 3.46:1.

Worked examples:
- 500-turn primary, 1500-turn secondary, 120V input: V2 = 120 × (1500/500) = 360V
- 4:1 transformer, 500V applied to secondary: V_primary = 500 × 4 = 2000V (secondary = input, primary = output here — read carefully which winding is being driven)

Embed: G5C01, G5C02, G5C05, G5C06, G5C07.

- [ ] **Step 3: Verify all 40 G5 questions present**

```bash
uv run python -c "
import json
with open('../data/general_class_questions.json') as f:
    qs = json.load(f)
ids = [q['id'] for q in qs if q['subelement'] == 'G5']
with open('g5-electrical.qmd') as f:
    content = f.read()
missing = [qid for qid in ids if qid not in content]
if missing:
    print('MISSING:', missing)
else:
    print('All', len(ids), 'G5 questions present')
"
```

- [ ] **Step 4: Render**

```bash
cd /Users/matt/Projects/Development/ham-study/learning-center && quarto render g5-electrical.qmd
```

- [ ] **Step 5: Commit**

```bash
git -C /Users/matt/Projects/Development/ham-study add learning-center/g5-electrical.qmd
git -C /Users/matt/Projects/Development/ham-study commit -m "feat: add G5 Electrical Principles learning page"
```

---

## Task 8: Write G6 — Circuit Components (23 questions)

**Files:**
- Create: `learning-center/g6-components.qmd`

G6 is a components reference section. Cover discrete components, semiconductors, connectors, and vacuum tubes.

- [ ] **Step 1: Read G6 questions**

```bash
uv run python -c "
import json
with open('../data/general_class_questions.json') as f:
    qs = json.load(f)
for q in [x for x in qs if x['subelement'] == 'G6']:
    print(q['id'], '|', q['question'])
    for k,v in q['answers'].items():
        prefix = '**' if k == q['correct'] else ''
        suffix = '**' if k == q['correct'] else ''
        print(f'  {prefix}{k}) {v}{suffix}')
    print()
"
```

- [ ] **Step 2: Write `g6-components.qmd`**

`learning-center/g6-components.qmd`, frontmatter:
```yaml
---
title: "G6: Circuit Components"
---
```

**Section 1 — Resistors**

Explain: A resistor is a passive two-terminal component that opposes current flow. Key specifications: resistance value (ohms) and power rating (watts). *Wire-wound resistors* are made by winding resistance wire on a form — this creates a small inductance, making them unsuitable for RF circuits where inductance would change their impedance. For RF circuits, use carbon composition or metal-film resistors.

Embed: G6A06.

**Section 2 — Capacitors**

Explain types by dielectric material: Electrolytic capacitors use an oxide layer as dielectric — they are polarized (must be connected with correct polarity), have high capacitance per volume, and are used for power supply filtering. Connecting them backwards destroys them. Ceramic capacitors are small, non-polarized, have good high-frequency characteristics, and are used throughout RF circuits. Low-voltage ceramic capacitors are temperature-stable and non-polarized.

Embed: G6A04, G6A08.

**Section 3 — Inductors and ferrite cores**

Explain: A ferrite core is a magnetic material (iron compound) used as the core of an inductor or transformer. The core's *permeability* (μ) multiplies the inductance compared to an air-core inductor. Different ferrite mixes (compositions) have different frequency characteristics — the permeability and loss characteristics of a core determine its optimal frequency range.

*Toroidal inductors*: A toroid (donut-shaped) core confines the magnetic field inside the core, reducing radiation and coupling to nearby components. This also means low susceptibility to external magnetic interference.

*Self-resonant frequency*: Every real inductor has parasitic capacitance between its windings. Above the self-resonant frequency, this capacitance dominates and the component behaves as a capacitor, not an inductor.

*Ferrite bead*: A ferrite bead placed over a wire forms a small inductor that blocks high-frequency common-mode currents while passing DC and low-frequency currents.

Embed: G6A11, G6B01, G6B05, G6B10.

**Section 4 — Diodes and the p-n junction**

Explain from first principles: Semiconductors (silicon, germanium) have an intermediate conductivity that can be controlled by *doping* — intentionally adding impurities. N-type material has extra electrons (negative carriers). P-type material has holes — missing electrons — that behave like positive carriers. A *p-n junction* is formed where the two meet.

At the junction, electrons and holes diffuse across and recombine, creating a *depletion region* with no free carriers — this acts like an insulator. Applying forward bias (positive to p-side, negative to n-side) narrows the depletion region and allows current to flow. The forward voltage threshold is ~0.6V for silicon and ~0.3V for germanium. Reverse bias widens the depletion region — essentially no current flows.

*Zener diode*: A diode designed to break down at a precise reverse voltage. Used for voltage regulation — in a circuit, it maintains a constant voltage drop equal to its Zener voltage when in reverse breakdown.

*LED (Light Emitting Diode)*: A forward-biased diode that emits light when electrons cross the junction.

*Varactor diode*: The capacitance of a reverse-biased diode varies with voltage (because the depletion region width changes). Varactors are used as voltage-controlled capacitors in tuning circuits and VCOs.

*PIN diode*: Has an intrinsic (undoped) layer between P and N layers. At DC or low frequencies, it acts as a normal diode. At RF, it acts as a variable resistor controlled by DC bias current — used as an RF switch or attenuator.

Embed: G6A03, G6A05, G6B08.

**Section 5 — Transistors: BJT and MOSFET**

Explain: A *Bipolar Junction Transistor (BJT)* has three terminals: base, collector, and emitter. NPN: current flows from collector to emitter when base is driven positive. PNP: current flows from emitter to collector when base is driven negative relative to emitter. Used as a switch: operating points are saturation (fully on) and cutoff (fully off). Used as an amplifier: operate in the linear (active) region.

A *MOSFET (Metal-Oxide-Semiconductor Field Effect Transistor)* has gate, drain, and source terminals. The gate is insulated from the channel by a thin oxide layer — it controls current by electric field, not by current. This gives very high input impedance. The gate oxide is extremely thin and can be destroyed by electrostatic discharge (ESD). MOSFET construction: a gate electrode separated from the channel by an insulating oxide layer.

Embed: G6A07, G6A09.

**Section 6 — Vacuum tubes**

Explain: A vacuum tube (valve) consists of electrodes inside an evacuated glass or metal envelope. Electrons are emitted from the heated *cathode* and attracted to the positive *plate* (anode). The *control grid* is placed between cathode and plate; varying the grid voltage controls the electron flow from cathode to plate, providing amplification. In a tetrode/pentode, a *screen grid* is added between the control grid and plate — it suppresses secondary emission and reduces plate-to-grid capacitance, improving high-frequency performance.

Embed: G6A10, G6A12.

**Section 7 — Integrated circuits and MMICs**

Explain: An *integrated circuit* (IC) is a miniaturized circuit fabricated on a single chip of semiconductor material. An *op-amp (operational amplifier)* is a high-gain, differential-input voltage amplifier — the fundamental analog building block for filters, comparators, and amplifiers. *CMOS (Complementary Metal-Oxide-Semiconductor)* logic uses pairs of N-channel and P-channel MOSFETs; it draws negligible static power compared to TTL (Transistor-Transistor Logic), which draws current continuously.

An *MMIC (Monolithic Microwave Integrated Circuit)* is an IC designed for microwave frequencies, integrating amplifiers, mixers, and other components on a single chip.

Embed: G6B02, G6B03, G6B06.

**Section 8 — Connectors and their frequency limits**

Explain: Connectors at RF must maintain controlled impedance and minimize signal leakage. Common types:
- *BNC*: Bayonet connector, common for lab equipment and lower-frequency RF. Typical upper limit for low SWR use: ~4 GHz.
- *N connector*: Larger threaded connector for higher power and frequency — rated to 11 GHz and beyond. Used for 2.4 GHz and 5.8 GHz (Wi-Fi/amateur) applications.
- *SMA*: Small threaded connector, rated to 18 GHz. Common in modern microwave equipment.
- *RCA (phono) jack*: Unbalanced, used for DC and audio frequencies only — not suitable for RF.

Mnemonic: **"BNC < N < SMA"** in frequency capability; **RCA is audio only**.

Embed: G6B04, G6B07, G6B11, G6B12.

**Section 9 — Batteries**

Explain: A *lead-acid battery* (standard 12V car battery) should not be discharged below about 10.5V (about 1.75V per cell) for maximum service life — deep discharge damages the plates. A battery with *low internal resistance* can deliver high current without significant voltage sag under load.

Embed: G6A01, G6A02.

- [ ] **Step 3: Verify all 23 G6 questions present**

```bash
uv run python -c "
import json
with open('../data/general_class_questions.json') as f:
    qs = json.load(f)
ids = [q['id'] for q in qs if q['subelement'] == 'G6']
with open('g6-components.qmd') as f:
    content = f.read()
missing = [qid for qid in ids if qid not in content]
if missing:
    print('MISSING:', missing)
else:
    print('All', len(ids), 'G6 questions present')
"
```

- [ ] **Step 4: Render**

```bash
cd /Users/matt/Projects/Development/ham-study/learning-center && quarto render g6-components.qmd
```

- [ ] **Step 5: Commit**

```bash
git -C /Users/matt/Projects/Development/ham-study add learning-center/g6-components.qmd
git -C /Users/matt/Projects/Development/ham-study commit -m "feat: add G6 Circuit Components learning page"
```

---

## Task 9: Write G7 — Practical Circuits (38 questions)

**Files:**
- Create: `learning-center/g7-circuits.qmd`

G7 covers complete circuits: power supplies, amplifiers, oscillators, filters, and receivers including software-defined radio.

- [ ] **Step 1: Read G7 questions**

```bash
uv run python -c "
import json
with open('../data/general_class_questions.json') as f:
    qs = json.load(f)
for q in [x for x in qs if x['subelement'] == 'G7']:
    print(q['id'], '|', q['question'])
    for k,v in q['answers'].items():
        prefix = '**' if k == q['correct'] else ''
        suffix = '**' if k == q['correct'] else ''
        print(f'  {prefix}{k}) {v}{suffix}')
    print()
"
```

- [ ] **Step 2: Write `g7-circuits.qmd`**

`learning-center/g7-circuits.qmd`, frontmatter:
```yaml
---
title: "G7: Practical Circuits"
---
```

**Section 1 — Power supplies: rectification and filtering**

Explain: A power supply converts AC mains voltage to regulated DC. The key stages are: transformer → rectifier → filter → regulator.

*Rectification*: Diodes allow current to flow in only one direction. A half-wave rectifier uses one diode, passes only one half of the AC cycle — the output is a bumpy DC with ripple at the mains frequency (60 Hz in the US). A full-wave rectifier uses two diodes and a center-tapped transformer, or four diodes in a bridge — it uses both halves of the AC cycle, so ripple frequency is 120 Hz (twice the mains frequency), and the output is smoother. The output of an unfiltered full-wave rectifier looks like a series of bumps (positive half-sine pulses).

*Filter capacitors*: A large capacitor across the output stores charge and smooths the ripple. The capacitor charges to the peak voltage and discharges slowly between peaks. Larger capacitance = smoother output = lower ripple.

*Bleeder resistor*: A resistor connected across the output that draws a small constant current. It discharges the filter capacitor when the supply is turned off (safety), and it improves voltage regulation by providing a minimum load.

*Switchmode (switching) power supply*: Converts DC to high-frequency AC, transforms at a small transformer (which can be physically small because efficiency increases with frequency), then rectifies and filters again. More efficient and lighter than linear supplies. Characteristic of switching supplies: they generate RF interference across a wide spectrum due to the high-frequency switching.

Schematic symbols: know how to identify a FET, Zener diode, NPN transistor, solid-core transformer, and tapped inductor from schematic symbols (reference G7-1 figure in the question pool).

Embed: G7A01, G7A02, G7A03, G7A04, G7A05, G7A06, G7A07, G7A08, G7A09, G7A10, G7A11, G7A12, G7A13.

**Section 2 — Amplifier classes and efficiency**

Explain: An amplifier's *class* describes what portion of the input signal cycle the active device conducts (is "on"):

*Class A*: The transistor/tube conducts 100% of the cycle (all 360°). Always "on," operating in the linear region. Excellent linearity — very low distortion. Efficiency: ~25–30%. Used where signal integrity matters more than efficiency.

*Class B*: The device conducts 50% of the cycle (180°). Two devices in push-pull share the signal — one handles the positive half, one the negative half. Efficiency ~78%. Some crossover distortion at the zero crossing.

*Class C*: The device conducts less than 50% of the cycle — typically 90–120°. The narrow conduction pulses are used to "kick" a resonant tank circuit (LC circuit) that produces a complete sine wave at its resonant frequency. Very efficient (~70–80%) but highly non-linear — only suitable for CW and FM, where amplitude linearity doesn't matter. Not suitable for SSB, AM, or any amplitude-modulated mode.

*Class D*: Switching mode — the device is either fully on or fully off (0% or 100%). Very high efficiency. Used in switching power supplies and some modern RF amplifiers.

Highest efficiency: Class C (or Class D). For modulated signals requiring amplitude linearity: only Class A or B.

*Neutralization*: In RF amplifiers, some of the output signal can couple back to the input through the internal capacitance of the active device (plate-to-grid in tubes, drain-to-gate in FETs). This feedback can cause oscillation. Neutralization introduces an equal and opposite signal to cancel this feedback.

*Efficiency calculation*: Efficiency = (RF output power / DC input power) × 100%.

Embed: G7B01, G7B02, G7B04, G7B08, G7B10, G7B11.

**Section 3 — Logic gates and digital circuits**

Explain briefly (limited to what's tested): An *AND gate* outputs a logic 1 only when both inputs are logic 1. A *shift register* is a chain of flip-flops that shifts a binary value one position per clock pulse — used for serial-to-parallel conversion and delay lines. A *3-bit binary counter* has 8 states (2³ = 8, counting 0 through 7).

Embed: G7B03, G7B05, G7B06.

**Section 4 — Oscillators**

Explain: An oscillator is an amplifier with positive feedback at one frequency. For sustained oscillation, the Barkhausen criterion requires: (1) gain ≥ 1 around the feedback loop, and (2) phase shift = 0° (or 360°) at the oscillation frequency. The oscillation frequency is set by the feedback network.

*LC oscillator*: Uses an inductor-capacitor resonant circuit to set frequency. The oscillation frequency is f = 1/(2π√(LC)). Common types: Hartley (tapped inductor), Colpitts (tapped capacitor).

*Sine wave oscillator components*: A frequency-determining network (LC tank, crystal), an amplifier, and a feedback path.

Embed: G7B07, G7B09.

**Section 5 — Filters**

Explain: A filter passes some frequencies and blocks others. Named by what it passes:
- *Low-pass filter*: Passes frequencies below the cutoff frequency (fc). Blocks higher frequencies. Used to remove harmonics from transmitter output.
- *High-pass filter*: Passes frequencies above fc. Blocks lower.
- *Band-pass filter*: Passes a range of frequencies around a center frequency. Bandwidth is measured between the -3 dB points (where power drops to half).
- *Band-stop (notch) filter*: Blocks a range, passes everything else.

Key specifications:
- *Insertion loss*: Power loss in the passband (should be near 0 dB for a good filter). Also called *passband loss*.
- *Rejection*: Attenuation outside the passband — how well it blocks unwanted signals.
- *Cutoff frequency (fc)*: The -3 dB point — where output power drops to half the passband level.

*Crystal filter*: Uses quartz crystals as resonators. Crystals have extremely high Q (quality factor), enabling very narrow, steep-sided filters — ideal for SSB IF filters.

*DSP filter*: Implemented in digital signal processing. Advantages: can implement very precise filter shapes, reconfigurable in software, no component drift.

Embed: G7C06, G7C07, G7C12, G7C13, G7C14.

**Section 6 — Modulators and demodulators**

Explain:

*Balanced modulator*: Combines the carrier with the audio (double-sideband suppressed-carrier output, DSB-SC). The carrier is balanced out — only the two sidebands appear at the output. To produce SSB, pass the DSB-SC through a sideband filter that passes only one sideband.

*Product detector*: Used in receivers to demodulate SSB and CW. It multiplies the incoming signal by a locally generated carrier (BFO — Beat Frequency Oscillator) to recover the audio.

*Impedance matching transformer at transmitter output*: The transmitter is designed for a 50Ω load. If the feedline presents a different impedance, using a matching transformer improves power transfer.

Embed: G7C01, G7C02, G7C03, G7C04.

**Section 7 — Superheterodyne receivers and frequency synthesis**

Explain: A *superheterodyne receiver* works by converting the received signal to a fixed intermediate frequency (IF) using a mixer. The mixer multiplies the RF input with a local oscillator (LO) signal; the output contains the sum and difference frequencies. The difference is selected as the IF (typically 455 kHz, 9 MHz, or others depending on design). The IF amplifier and filter then handle all selectivity and gain at a fixed frequency — this is much easier to design than a tunable filter.

*Image rejection*: A signal at twice the IF away from the desired signal can also produce the same IF — this is the *image*. The RF filter ahead of the mixer must reject the image frequency.

*Direct Digital Synthesis (DDS)*: A frequency synthesizer that generates precise frequencies by computing a digital sine wave and converting it to analog with a DAC. Advantages: fast frequency switching, fine resolution, phase-continuous frequency changes.

*Software Defined Radio (SDR)*: Most of the radio's processing is done in software rather than hardware. The key technique is *I/Q demodulation*: the incoming signal is split into two paths, one multiplied by the local oscillator (I, in-phase) and one multiplied by the LO shifted 90° (Q, quadrature). The 90° phase difference allows the software to determine the complete amplitude and phase of the signal at every instant. Advantages: one hardware platform can implement AM, FM, SSB, CW, PSK, and any other demodulation mode entirely in software.

*Receiver sensitivity*: Determined primarily by the noise figure of the front-end amplifier. A low-noise preamplifier improves sensitivity.

*Bandwidth matching*: The receiver bandwidth should match the signal's occupied bandwidth — a wider bandwidth admits more noise, degrading SNR; a narrower bandwidth might clip the signal.

Embed: G7C05, G7C08, G7C09, G7C10, G7C11, G8B01, G8B02, G8B03, G8B11. (Note: G8B questions about mixing are conceptually part of the superheterodyne discussion — embed them here to teach the concept, then reference that the G8 page continues the signal-level discussion. Actually: keep G8 questions in G8 only — do not embed them here. Instead, note the concept and embed only G7C questions in this file.)

Embed in G7: G7C05, G7C08, G7C09, G7C10, G7C11.

- [ ] **Step 3: Verify all 38 G7 questions present**

```bash
uv run python -c "
import json
with open('../data/general_class_questions.json') as f:
    qs = json.load(f)
ids = [q['id'] for q in qs if q['subelement'] == 'G7']
with open('g7-circuits.qmd') as f:
    content = f.read()
missing = [qid for qid in ids if qid not in content]
if missing:
    print('MISSING:', missing)
else:
    print('All', len(ids), 'G7 questions present')
"
```

- [ ] **Step 4: Render**

```bash
cd /Users/matt/Projects/Development/ham-study/learning-center && quarto render g7-circuits.qmd
```

- [ ] **Step 5: Commit**

```bash
git -C /Users/matt/Projects/Development/ham-study add learning-center/g7-circuits.qmd
git -C /Users/matt/Projects/Development/ham-study commit -m "feat: add G7 Practical Circuits learning page"
```

---

## Task 10: Write G8 — Signals and Emissions (42 questions)

**Files:**
- Create: `learning-center/g8-signals.qmd`

G8 covers modulation theory, bandwidth, and digital signal characteristics.

- [ ] **Step 1: Read G8 questions**

```bash
uv run python -c "
import json
with open('../data/general_class_questions.json') as f:
    qs = json.load(f)
for q in [x for x in qs if x['subelement'] == 'G8']:
    print(q['id'], '|', q['question'])
    for k,v in q['answers'].items():
        prefix = '**' if k == q['correct'] else ''
        suffix = '**' if k == q['correct'] else ''
        print(f'  {prefix}{k}) {v}{suffix}')
    print()
"
```

- [ ] **Step 2: Write `g8-signals.qmd`**

`learning-center/g8-signals.qmd`, frontmatter:
```yaml
---
title: "G8: Signals and Emissions"
---
```

**Section 1 — Why modulation is necessary**

Explain: An audio signal (20 Hz–20 kHz) cannot be efficiently transmitted as a radio wave — antennas would need to be kilometers long, and thousands of stations would all occupy the same spectrum. Modulation impresses the audio information onto a *carrier* wave at a specific radio frequency. The carrier is a continuous sine wave; the modulation changes one of its properties (amplitude, frequency, or phase) in proportion to the audio.

**Section 2 — Amplitude Modulation (AM)**

Explain: In AM, the instantaneous amplitude (envelope) of the carrier varies in proportion to the audio signal. The result in the frequency domain is the carrier plus two sidebands — an upper sideband (USB) and lower sideband (LSB), each carrying identical information. The bandwidth of an AM signal is twice the highest audio frequency: a signal modulated with 3 kHz audio occupies 6 kHz.

*The modulation envelope*: The outline of an AM signal's amplitude over time — it traces the shape of the audio waveform.

*Overmodulation*: If the audio amplitude exceeds 100% of the carrier amplitude, the carrier is driven to zero on negative peaks — this *clips* the envelope, producing flat-topped waveforms (flat-topping) and generating sidebands far beyond the normal bandwidth (splatter). This causes harmful interference to adjacent channels.

*Reactance modulator*: A device that varies a reactance (capacitance or inductance) in a transmitter's oscillator circuit, changing the frequency. When connected to an RF amplifier, it produces FM (frequency modulation). It does not directly produce AM.

The power in an AM signal: 2/3 of a fully modulated AM signal's total power is in the carrier (wasted), and only 1/3 is in the sidebands (information). This is why SSB is more efficient.

Embed: G8A05, G8A08, G8A10, G8A11, G8A04.

**Section 3 — Single Sideband (SSB)**

Explain: SSB suppresses the carrier completely and transmits only one sideband. The advantages: half the bandwidth of AM (3 kHz instead of 6 kHz), no power wasted on the carrier, all power goes to the information-bearing sideband. To demodulate SSB, the receiver must reinsert a carrier at the correct frequency — this is the BFO (Beat Frequency Oscillator) in the product detector.

SSB is the narrowest-bandwidth phone emission.

Which sideband? Upper Sideband (USB) is standard on 20m, 17m, 15m, 12m, 10m. Lower Sideband (LSB) is standard on 160m, 75/80m, 40m. On VHF/UHF, USB is the standard.

Embed: G8A07, G2A06, G2A07 (note: G2A questions belong in g2-operating.qmd — do not duplicate).

Embed here: G8A07.

**Section 4 — Frequency Modulation (FM)**

Explain: In FM, the carrier frequency varies in proportion to the audio signal while amplitude stays constant. Key terms:

*Deviation*: How far the carrier swings from its center frequency. Standard amateur FM: ±5 kHz deviation. *Modulation index* = deviation / audio frequency. For FM voice, modulation index varies with audio content.

*Bandwidth (Carson's rule)*: BW ≈ 2 × (deviation + maximum audio frequency). For ±5 kHz deviation and 3 kHz audio: BW = 2 × (5 + 3) = 16 kHz.

*Capture effect*: FM receivers naturally lock onto the strongest signal on a frequency and completely reject weaker signals — unlike AM, where multiple signals combine and create a mix.

Embed: G8A03, G8B06, G8B07.

**Section 5 — Phase modulation (PM) and QPSK**

Explain: In PSK (Phase Shift Keying), the carrier's phase angle is changed to carry information. *QPSK (Quadrature Phase Shift Keying)* uses four phase states (0°, 90°, 180°, 270°), each encoding 2 bits. QPSK31 is a variant of PSK31 using quadrature phase — it can carry twice the data of BPSK31 in the same bandwidth.

*FT8*: Uses 8-GFSK (Gaussian Frequency Shift Keying with 8 frequency states). Each symbol encodes 3 bits.

Embed: G8A02, G8A06, G8A09, G8A12.

**Section 6 — Frequency conversion and mixing (heterodyning)**

Explain: A *mixer* is a non-linear device that multiplies two signals together. When two frequencies f1 and f2 are mixed, the output contains the original frequencies plus their sum (f1+f2) and difference (f1-f2). In a superheterodyne receiver, the *local oscillator (LO)* is tuned to convert the desired RF signal to the fixed intermediate frequency (IF). The mixer output frequency = LO ± RF input.

*Intermodulation*: When two or more signals are present at a non-linear device (like a receiver front end or an overdriven amplifier), they mix to produce intermodulation products at frequencies nF1 ± mF2 where n and m are integers. The most troublesome are *odd-order products* (3rd order: 2F1-F2 and 2F2-F1) because they fall very close to the original signals and cannot be filtered. Third-order products at 2F1-F2 and 2F2-F1 are closest to the original signal frequencies.

*Image rejection*: A frequency at LO + IF (when the desired signal is at LO - IF, or vice versa) produces the same IF and arrives as an unwanted "image." The image must be rejected before the mixer. This is handled by the RF front-end selectivity or a dedicated image-rejection filter.

*Multiplier stage in FM transmitter*: To generate a 5 kHz deviation signal at VHF from a lower-frequency oscillator, a frequency multiplier (a circuit that generates harmonics) is used. Multiplication increases both frequency and deviation proportionally.

*Symbol rate and bandwidth*: Higher symbol rates require wider bandwidth — bandwidth is proportional to symbol rate (baud rate).

*Duty cycle and power*: Some modes (like FM or digital modes with continuous transmission) have a 100% duty cycle — the transmitter is always at full power. SSB voice has a low duty cycle (the carrier drops to near zero during pauses). Duty cycle matters for thermal management — a transmitter rated at 100W peak on SSB might overheat running the same power in a 100% duty cycle digital mode.

Embed: G8A13, G8A14, G8B01, G8B02, G8B03, G8B04, G8B05, G8B08, G8B09, G8B10, G8B11, G8B12, G8B13.

**Section 7 — Digital modes: encoding and error correction**

Explain:

*Baudot code*: A 5-bit character encoding, used in RTTY. Limited character set (letters, numbers, some punctuation).

*Packet radio*: Transmits data in *frames* — packets of data with header information. The *header* (address information field) contains routing and handling information: source address, destination address, protocol identifiers.

*ARQ (Automatic Repeat reQuest)*: A protocol where the receiver acknowledges each packet. A *NAK (Negative Acknowledgment)* means the packet was received with errors and should be retransmitted. Too many retransmissions with failed decoding → link failure.

*FEC (Forward Error Correction)*: Error correction built into the transmitted data stream. Extra *redundancy bits* are added so the receiver can reconstruct the original data even if some bits are corrupted — without requesting a retransmission. FEC is used in FT8 and many other weak-signal modes.

*FSK signal identification*: FSK uses two discrete frequencies (mark and space). They are identified by which audio frequency corresponds to mark and which to space — if inverted, received text is garbled.

*PSK31*: Uses Varicode — a variable-length binary code (shorter codes for common characters). Highly efficient for text. Sensitive to phase noise. A properly transmitted PSK31 signal shows a clean double-bar pattern on a waterfall display. Key clicks (vertical lines flanking the signal) indicate overdriving or improper filter settings.

*Waterfall display*: A spectrum display where frequency is on the horizontal axis, time flows downward (newer signals at top, older at bottom), and signal strength is shown by color. It lets you see signals over time.

*WSPR (Weak Signal Propagation Reporter)*: A beacon/propagation-assessment digital mode with very low power and very narrow bandwidth. Used to map propagation between stations.

*FT8 signal report*: Expressed in dB SNR relative to the noise floor in a 2500 Hz bandwidth. "+3" means the signal is 3 dB above the noise floor — a weak but copyable signal.

*Digital voice*: Modes like D-STAR, DMR, System Fusion (YSF), and P25 provide digital voice over amateur radio using various codecs.

*Mesh network nodes*: AREDN mesh network nodes are configured in a peer-to-peer mesh topology where each node can communicate with multiple others — no single point of failure.

Embed: G8C02, G8C03, G8C04, G8C05, G8C06, G8C07, G8C08, G8C09, G8C10, G8C11, G8C12, G8C13, G8C14, G8C15, G8C16.

Also embed: G8A01 (Binary FSK generation).

- [ ] **Step 3: Verify all 42 G8 questions present**

```bash
uv run python -c "
import json
with open('../data/general_class_questions.json') as f:
    qs = json.load(f)
ids = [q['id'] for q in qs if q['subelement'] == 'G8']
with open('g8-signals.qmd') as f:
    content = f.read()
missing = [qid for qid in ids if qid not in content]
if missing:
    print('MISSING:', missing)
else:
    print('All', len(ids), 'G8 questions present')
"
```

- [ ] **Step 4: Render**

```bash
cd /Users/matt/Projects/Development/ham-study/learning-center && quarto render g8-signals.qmd
```

- [ ] **Step 5: Commit**

```bash
git -C /Users/matt/Projects/Development/ham-study add learning-center/g8-signals.qmd
git -C /Users/matt/Projects/Development/ham-study commit -m "feat: add G8 Signals and Emissions learning page"
```

---

## Task 11: Write G9 — Antennas and Feed Lines (46 questions)

**Files:**
- Create: `learning-center/g9-antennas.qmd`

G9 is a technical section. Build from the physics of radiation through feed lines to specific antenna types.

- [ ] **Step 1: Read G9 questions**

```bash
uv run python -c "
import json
with open('../data/general_class_questions.json') as f:
    qs = json.load(f)
for q in [x for x in qs if x['subelement'] == 'G9']:
    print(q['id'], '|', q['question'])
    for k,v in q['answers'].items():
        prefix = '**' if k == q['correct'] else ''
        suffix = '**' if k == q['correct'] else ''
        print(f'  {prefix}{k}) {v}{suffix}')
    print()
"
```

- [ ] **Step 2: Write `g9-antennas.qmd`**

`learning-center/g9-antennas.qmd`, frontmatter:
```yaml
---
title: "G9: Antennas and Feed Lines"
---
```

**Section 1 — What an antenna does**

Explain from first principles: An antenna converts between electrical energy (voltage and current in a transmission line) and electromagnetic waves (electric and magnetic fields in free space). The same antenna works for both transmitting and receiving — this is the *principle of reciprocity*: an antenna's transmit and receive patterns are identical.

**Section 2 — The half-wave dipole**

Explain: The *dipole* is the fundamental HF antenna — two conductors extending in opposite directions from a feed point, each λ/4 long, for a total length of λ/2 (half wavelength). At the resonant frequency, the antenna presents a purely resistive impedance of approximately 73 Ω at the feed point.

*Resonant length*: A half-wave dipole is approximately 468/f(MHz) feet long (or 143/f(MHz) meters). This is slightly less than the actual free-space half wavelength because of the *velocity factor* of the wire in real antennas.

Worked examples:
- At 14.250 MHz: length ≈ 468/14.25 ≈ 32.8 feet
- At 3.550 MHz: length ≈ 468/3.55 ≈ 131.8 feet

*Radiation pattern*: A half-wave dipole in free space radiates maximum energy broadside to the wire (perpendicular to the wire), with nulls off the ends. In the plane containing the wire, the pattern is a figure-8 (two lobes). Height above ground affects the radiation angle and thus the pattern significantly.

*Polarization*: A horizontal dipole produces horizontally polarized radiation. A vertical antenna produces vertically polarized radiation. Horizontal polarization provides better rejection of man-made electrical noise (which tends to be vertically polarized). Vertical polarization provides a lower radiation angle at lower heights, which can be advantageous for DX.

*Feed point impedance vs. height*: As a dipole is lowered toward the ground, its feed impedance drops below 73 Ω. At very low heights, it can fall to 25–35 Ω.

*Feed point location*: Moving the feed point away from the center of a dipole changes the impedance — center feed gives ~73 Ω; off-center feed raises the impedance significantly.

Embed: G9B04, G9B05, G9B07, G9B08, G9B09, G9B10, G9B11.

**Section 3 — Quarter-wave verticals and ground planes**

Explain: A quarter-wave vertical monopole is the other fundamental antenna. It requires a ground plane (a set of radial wires, a metal surface, or actual earth) to complete the antenna system. The ground plane acts as a *counterpoise* — it provides the "other half" of the dipole that the earth would otherwise provide (imperfectly). An elevated quarter-wave antenna with radials has a feed impedance of approximately 50 Ω, which matches coaxial cable nicely.

*Radial placement*: Ground-mounted vertical radial wires should be buried just below the soil surface or laid on the ground. They reduce ground losses by providing a high-conductivity path for return currents.

*Quarter-wave monopole length*: λ/4 = 234/f(MHz) feet. At 28.5 MHz: 234/28.5 ≈ 8.2 feet.

*Radiation pattern*: A quarter-wave vertical over a perfect ground radiates with an omnidirectional azimuthal pattern and a maximum radiation angle near the horizon — ideal for long-distance (DX) communication.

Embed: G9B02, G9B03, G9B06, G9B12.

**Section 4 — Feed lines and coaxial cable**

Explain:

*Coaxial cable (coax)*: The standard HF feed line. An inner conductor is surrounded by a dielectric (insulator), then a braided or solid outer shield, then a protective jacket. The key properties:
- *Characteristic impedance* (Z₀): Determined by the geometry (inner conductor diameter, outer conductor diameter, dielectric constant) — not by the length. Common values: 50 Ω (most amateur equipment), 75 Ω (TV and some antenna applications). Cannot be changed by cutting the cable.
- *Velocity factor*: Signals travel slower in coax than in free space — typically 0.66–0.82× the speed of light, depending on the dielectric.
- *Attenuation*: Loss in dB per 100 feet, increases with frequency. Higher frequency → greater attenuation for the same cable length.

*Parallel line (window line, ladder line)*: Two parallel conductors separated by a dielectric. Typical characteristic impedance: 450 Ω (window line with periodic openings). Lower loss than coax at HF but requires an antenna tuner to match to the 50 Ω transceiver.

*Feed line loss units*: dB per 100 feet (or per 100 m).

A *random wire* antenna connected directly to the transmitter (without a tuner) presents a nearly random impedance — the transmitter's output amplifier may see highly reactive loads, causing stress and potential damage.

Embed: G9A01, G9A03, G9A05, G9A06, G9B01.

**Section 5 — Standing Wave Ratio (SWR)**

Explain: When a transmission line is connected to a load that doesn't match its characteristic impedance, some of the transmitted power is reflected back toward the source. The forward and reflected waves interfere, creating *standing waves* — a pattern of voltage and current maxima and minima along the line. SWR (Standing Wave Ratio) is the ratio of the maximum to minimum voltage on the line.

SWR = 1:1 means perfect match — no reflections, all power delivered to the load.
SWR = ∞ (open or short circuit) means total reflection.

*Calculating SWR*: SWR = Z_load / Z_line if Z_load > Z_line (or inverted if Z_line > Z_load).
- 200 Ω load on 50 Ω line: SWR = 200/50 = 4:1
- 10 Ω load on 50 Ω line: SWR = 50/10 = 5:1

*Effects of high SWR*:
- Increased feed line loss (the reflected power is absorbed by the line's resistance on the return trip)
- The transmitter's output stage may see a highly reactive load, causing it to reduce power or potentially be damaged
- A matching network at the transmitter makes the *transmitter* see a 50 Ω load, but does NOT reduce the losses in the feed line itself

*Reflected power cause*: Mismatch between the antenna's feed impedance and the transmission line's characteristic impedance.

*Line loss and SWR measurement*: Transmission line loss causes SWR measured at the transmitter end to appear lower than the actual SWR at the antenna — the line loss attenuates the reflected wave.

Preventing standing waves: match the antenna feed impedance to the transmission line — by antenna design or an impedance matching network at the feed point.

Embed: G9A02, G9A04, G9A07, G9A08, G9A09, G9A10, G9A11.

**Section 6 — Impedance matching**

Explain:

*Beta (hairpin) match*: A short-circuit stub of transmission line connected across the driven element feed point of a Yagi. Used to cancel out the capacitive reactance of the driven element when it is slightly shorter than resonance, transforming the impedance to match the feed line.

*Gamma match*: An asymmetric matching network connecting a coaxial feed line to the driven element of a Yagi. The inner conductor connects to a tap on the driven element; the outer shield connects to the boom/ground. Advantage: no insulator needed between driven element and boom — the driven element can be grounded to the boom. Allows adjustment of feed impedance.

*End-fed half-wave (EFHW) antenna*: Fed at one end rather than the center. The end of a half-wave dipole has very high impedance — several thousand ohms. An EFHW transformer (a high-impedance matching network, typically 49:1 or 64:1 impedance ratio) is needed to match to 50 Ω coax.

Embed: G9D02.

**Section 7 — Yagi-Uda directional antennas**

Explain: The *Yagi-Uda antenna* (usually just "Yagi") consists of a *driven element* (fed by the transmission line), one *reflector* (slightly longer than λ/2, behind the driven element), and one or more *directors* (slightly shorter than λ/2, in front of the driven element). The parasitic elements (reflector and directors) are not connected to the feed line — they are excited by the electromagnetic field from the driven element and re-radiate, shaping the pattern.

Key points:
- Driven element ≈ λ/2 in length.
- Reflector is slightly *longer* than the driven element.
- Directors are slightly *shorter* than the driven element.
- Adding more directors and lengthening the boom increases forward gain.
- *Main lobe*: The direction of maximum radiation.
- *Front-to-back ratio*: Ratio of gain in the main lobe direction to gain directly behind the antenna. A higher ratio means better rejection of signals from the rear.
- *Gain in dBi*: decibels relative to an isotropic radiator (theoretical antenna that radiates equally in all directions). *dBd*: decibels relative to a dipole. Since a dipole has 2.15 dBi gain, dBi = dBd + 2.15.
- *Stacking two Yagis*: Placing two identical Yagis vertically separated increases gain by approximately 3 dB (doubles the aperture).
- *Bandwidth*: Increased by using larger-diameter elements (or multiple rods), which lowers Q.

Embed: G9C01, G9C02, G9C03, G9C04, G9C05, G9C07, G9C08, G9C09, G9C10.

**Section 8 — Specialized antennas**

Explain:

*Log-periodic antenna*: A broadband directional antenna where multiple driven elements of decreasing length are arranged along a boom. All elements are driven (unlike a Yagi). The active region shifts with frequency, giving consistent performance across a wide frequency range. Gain is lower than a Yagi of similar boom length.

*NVIS antenna*: Near Vertical Incidence Skywave — used for regional coverage within ~0–500 km. Uses high radiation angles (nearly straight up) to bounce off the ionosphere and come back down nearby. Low dipoles (λ/10 above ground) naturally radiate at high angles. Requires lower HF frequencies (typically 40m or 80m) for daytime NVIS use.

*Halo antenna*: A horizontally polarized, omnidirectional VHF/UHF antenna. A bent half-wave dipole formed into a circle, with a gap at the top for impedance matching. Radiates horizontally — suitable for mobile VHF operation. Maximum radiation is broadside to the plane of the circle (omnidirectional in azimuth, but in the horizontal plane).

*Antenna traps*: LC resonant circuits inserted in antenna elements. A trap resonant at a given frequency acts as a high impedance at that frequency, electrically shortening the antenna for higher-frequency bands while allowing the full antenna length to be used on lower bands. Used in multiband trap dipoles and trap verticals. Disadvantage: traps add some loss, the antenna bandwidth is reduced, and interaction between traps can complicate tuning.

*Screwdriver antenna*: A mobile HF antenna with a motor-driven coil for remote adjustment of the loading inductance. Allows tuning different bands without manual adjustment.

*Beverage antenna*: A very long (multiple wavelengths), low-to-the-ground, end-fed wire antenna used exclusively for *receiving* on LF and HF. Excellent signal-to-noise ratio because it is directional and rejects noise from the back. Not used for transmitting.

*Small transmitting loop (magnetic loop)*: A compact (much less than λ in circumference) resonant loop antenna. Directional — nulls off the plane of the loop (an electrically small loop has null directions perpendicular to the plane of the loop in azimuth, with figure-8 pattern). High Q — narrow bandwidth, requires retuning between frequencies.

*Inverted V*: A dipole with a single central support at the apex and the two ends sloping down. Also called a "inverted V dipole." Common because only one tall support is needed.

*Stacked Yagis*: Two or more Yagis at the same azimuth, vertically separated. Vertically stacking increases gain by combining the broadside radiation from both antennas. Stacking distance typically λ/2 for maximum gain.

*Multiband antenna disadvantage*: Compromises across bands — may not be optimal on any single band.

Embed: G9C11, G9C12, G9D01, G9D03, G9D04, G9D05, G9D06, G9D07, G9D08, G9D09, G9D10, G9D11, G9D12.

- [ ] **Step 3: Verify all 46 G9 questions present**

```bash
uv run python -c "
import json
with open('../data/general_class_questions.json') as f:
    qs = json.load(f)
ids = [q['id'] for q in qs if q['subelement'] == 'G9']
with open('g9-antennas.qmd') as f:
    content = f.read()
missing = [qid for qid in ids if qid not in content]
if missing:
    print('MISSING:', missing)
else:
    print('All', len(ids), 'G9 questions present')
"
```

- [ ] **Step 4: Render**

```bash
cd /Users/matt/Projects/Development/ham-study/learning-center && quarto render g9-antennas.qmd
```

- [ ] **Step 5: Commit**

```bash
git -C /Users/matt/Projects/Development/ham-study add learning-center/g9-antennas.qmd
git -C /Users/matt/Projects/Development/ham-study commit -m "feat: add G9 Antennas and Feed Lines learning page"
```

---

## Task 12: Write G0 — Electrical and RF Safety (25 questions)

**Files:**
- Create: `learning-center/g0-safety.qmd`

G0 is a mix of regulation (RF exposure limits) and practical safety (electrical, grounding, tower).

- [ ] **Step 1: Read G0 questions**

```bash
uv run python -c "
import json
with open('../data/general_class_questions.json') as f:
    qs = json.load(f)
for q in [x for x in qs if x['subelement'] == 'G0']:
    print(q['id'], '|', q['question'])
    for k,v in q['answers'].items():
        prefix = '**' if k == q['correct'] else ''
        suffix = '**' if k == q['correct'] else ''
        print(f'  {prefix}{k}) {v}{suffix}')
    print()
"
```

- [ ] **Step 2: Write `g0-safety.qmd`**

`learning-center/g0-safety.qmd`, frontmatter:
```yaml
---
title: "G0: Electrical and RF Safety"
---
```

**Section 1 — RF radiation and biological effects**

Explain: RF (radio frequency) electromagnetic radiation at amateur power levels is *non-ionizing* — it does not have enough photon energy to remove electrons from atoms (unlike X-rays or gamma rays). The primary biological effect is *thermal* (heating): RF energy is absorbed by tissue and converted to heat, similar to a microwave oven. At sufficient power density, this heating can damage tissue. This is why RF safety matters, even though the risk is real only at high power levels and close proximity.

Embed: G0A01.

**Section 2 — FCC RF exposure limits and evaluation**

Explain: The FCC sets *Maximum Permissible Exposure (MPE)* limits — the maximum power density that humans may be exposed to from an amateur station. Two tiers:
- *Controlled environment*: Where the exposed person is aware of the RF and can take precautions (e.g., the operator at the transmitter). Higher limits allowed.
- *Uncontrolled environment*: General public, neighbors, passersby — lower limits apply.

*Time averaging*: MPE is evaluated as a time-averaged exposure. A station running 100W continuously has higher average exposure than one running 100W at 5% duty cycle (pulsed with lots of quiet time). The FCC allows averaging over 6 minutes for controlled and 30 minutes for uncontrolled environments. A mode's duty cycle directly affects the time-averaged power and therefore the effective RF exposure level.

*Who must evaluate*: Every amateur station. Stations below certain power thresholds on specific bands are exempt from the formal evaluation requirement. Above those thresholds, the operator must evaluate compliance (by calculation using the FCC's worksheets or online tools, or by direct measurement).

*What to do if non-compliant*: If an evaluation shows the station exceeds MPE limits, the operator must take steps to reduce exposure — increase distance to the antenna, reduce power, use a more directional antenna, reduce operating time, or restrict access to the near-field area.

*Neighbor exposure*: If evaluation shows a neighbor may receive more than the uncontrolled MPE limit, the operator must remedy this — reducing power, changing antenna direction, or coordinating with the neighbor.

*Indoor transmitting antennas*: Should be located far from areas where people spend significant time. Near-field RF exposure from an indoor antenna can be significant.

*Measurement instrument*: An *isotropic field strength meter* (or broadband RF field strength meter) can measure actual RF field intensity.

Embed: G0A02, G0A03, G0A04, G0A05, G0A06, G0A07, G0A08, G0A09, G0A10, G0A11, G0A12.

**Section 3 — Electrical safety fundamentals**

Explain: Electrical shock hazard depends on the *current* through the body, not voltage alone. However, since body resistance determines current (I = V/R), voltage matters in practice. Currents as low as 100 mA through the heart can cause ventricular fibrillation and death. Even 50 mA is dangerous. Household 120V AC can easily drive lethal current through a human body.

*Fusing and circuit protection*: Fuses and circuit breakers protect wiring from overheating due to excess current. NEC rules specify minimum wire gauge for 20A circuits (12 AWG). Fuse size should be selected to protect the wiring, not the equipment. Hot and neutral conductors (in US 120V) are fused; in 240V circuits, both hot legs must be fused. The neutral and ground conductors are not fused.

*GFCI (Ground Fault Circuit Interrupter)*: Detects tiny current imbalances between hot and neutral (as small as 5 mA), indicating current is flowing through an unintended path (like a person). Trips instantly. Required in wet areas.

*Capacitor hazard*: Filter capacitors in power supplies can retain dangerous charge after the supply is turned off. Always discharge capacitors before working on equipment.

*Power supply interlock*: A safety switch that disconnects power when a panel or cover is opened, preventing accidental contact with high-voltage components.

*Lead-tin solder hazard*: The lead in conventional solder (Pb-Sn) is a cumulative neurotoxin. Wash hands after handling; avoid inhaling solder fumes (flux, not lead vapor, but still harmful); use ventilation.

Embed: G0B01, G0B02, G0B03, G0B05, G0B06, G0B10, G0B12.

**Section 4 — Grounding and lightning protection**

Explain:

*Lightning ground location*: The lightning protection ground system should be located as close to the antenna entry point as possible — outside the building, at the point where antenna cables and tower ground wires enter. The purpose is to intercept lightning current and divert it to earth before it enters the building.

*Lightning arrestors*: Installed where antenna cables enter the building, connected to the station ground. They provide a low-impedance path to earth for lightning energy, protecting equipment inside. Correct location: at the building entry point.

*Ground rods*: Must meet NEC requirements for size and depth — typically 8 feet long, copper-clad steel, driven vertically. Rods can be bonded together for better earth contact.

*Soldering lightning protection grounds*: Do NOT use soldered joints in lightning protection grounding. Solder melts at low temperature; a lightning strike would melt the joint and open the ground path at the worst moment. Use mechanical (clamped or bolted) connections.

*Tower climbing*: Always use a properly fitted safety harness attached to the tower with a fall protection system. Always have a ground observer present — never climb alone. Before climbing, de-energize all antenna-connected equipment to prevent RF burns.

*Emergency generator installation*: Must be properly bonded to ground; must not back-feed into utility lines (requires transfer switch to disconnect utility before connecting generator).

Embed: G0B04, G0B07, G0B08, G0B09, G0B11, G0B13.

- [ ] **Step 3: Verify all 25 G0 questions present**

```bash
uv run python -c "
import json
with open('../data/general_class_questions.json') as f:
    qs = json.load(f)
ids = [q['id'] for q in qs if q['subelement'] == 'G0']
with open('g0-safety.qmd') as f:
    content = f.read()
missing = [qid for qid in ids if qid not in content]
if missing:
    print('MISSING:', missing)
else:
    print('All', len(ids), 'G0 questions present')
"
```

- [ ] **Step 4: Render**

```bash
cd /Users/matt/Projects/Development/ham-study/learning-center && quarto render g0-safety.qmd
```

- [ ] **Step 5: Commit**

```bash
git -C /Users/matt/Projects/Development/ham-study add learning-center/g0-safety.qmd
git -C /Users/matt/Projects/Development/ham-study commit -m "feat: add G0 Electrical and RF Safety learning page"
```

---

## Task 13: Full site render and final verification

- [ ] **Step 1: Render the complete site**

```bash
cd /Users/matt/Projects/Development/ham-study/learning-center && quarto render
```

Expected: all 11 pages render without errors.

- [ ] **Step 2: Verify all 422 questions are present across all files**

```bash
uv run python -c "
import json
with open('../data/general_class_questions.json') as f:
    qs = json.load(f)
import os
missing_all = []
for sub in ['G0','G1','G2','G3','G4','G5','G6','G7','G8','G9']:
    ids = [q['id'] for q in qs if q['subelement'] == sub]
    fname = {
        'G0': 'g0-safety.qmd',
        'G1': 'g1-rules.qmd',
        'G2': 'g2-operating.qmd',
        'G3': 'g3-propagation.qmd',
        'G4': 'g4-practices.qmd',
        'G5': 'g5-electrical.qmd',
        'G6': 'g6-components.qmd',
        'G7': 'g7-circuits.qmd',
        'G8': 'g8-signals.qmd',
        'G9': 'g9-antennas.qmd',
    }[sub]
    with open(fname) as f:
        content = f.read()
    missing = [qid for qid in ids if qid not in content]
    if missing:
        missing_all.extend(missing)
        print(sub, 'MISSING:', missing)
    else:
        print(sub, 'OK:', len(ids), 'questions')
print()
if missing_all:
    print('Total missing:', len(missing_all))
else:
    print('All 422 questions present across all files.')
"
```

Expected: All 10 subelements print OK, total 422 questions present.

- [ ] **Step 3: Preview the site locally**

```bash
cd /Users/matt/Projects/Development/ham-study/learning-center && quarto preview
```

Open the browser and verify: sidebar navigation works, TOC works, search works, question callouts collapse and expand correctly showing the correct answer bolded.

- [ ] **Step 4: Final commit**

```bash
git -C /Users/matt/Projects/Development/ham-study add learning-center/
git -C /Users/matt/Projects/Development/ham-study commit -m "feat: complete General Class learning center — all 422 questions"
```
