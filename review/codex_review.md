Reading additional input from stdin...
OpenAI Codex v0.149.1
--------
workdir: C:\Users\HP\Documents\MeasurementScience_Evals\paper11_elicitation_method
model: gpt-5.5
provider: openai
approval: never
sandbox: workspace-write [workdir, /tmp, $TMPDIR]
reasoning effort: xhigh
reasoning summaries: none
session id: 01a042cc-57a2-7d83-8fea-962b8b88e25a
--------
user
You are a hostile referee for **Behavior Research Methods** (Springer, IF 5.0, Q1). Your job is
to find reasons to reject, not to be encouraging. Assume the authors will read only your
concrete findings, so vagueness is worthless.

## What to read

Working directory is the repository root.

- `paper/main.tex` and `paper/section_replication.tex` — the manuscript source (the version
  submitted to BRM). `paper/main.pdf` is the compiled result.
- `paper/main_ipm.tex` and `paper/main_nlp.tex` — two alternative framings of the SAME paper for
  other journals. Body should be identical to `main.tex`; only title, abstract and one framing
  paragraph differ.
- `paper/refs.bib` — the bibliography.
- `family1/` and `family2/` — the raw data (`results/*.jsonl`) and the scripts that produced
  every number.
- `figures/` — the code that produces every figure.
- `validity/` — a construct-classification instrument, not yet run.

## What I want you to attack, in priority order

**1. Numbers that do not match their source.** Every quantitative claim in the manuscript should
be reproducible from the released `.jsonl` files by the released scripts. Recompute the ones you
can. Report any claim you cannot reproduce, with the number the data actually gives. Pay
particular attention to: the 7,920 total; the between-item standard deviations; the ±0.41 and
±0.05 item-count derivations; the factor of 16; the 0.000 → 0.778 threshold swing; the paired
deltas in the instruction ablations and their bootstrap intervals; κ = 0.184.

**2. Internal contradictions.** Places where the abstract, a results section, the replication
section and the conclusion say different things about the same quantity. This paper was edited
in several passes and a previous review already found one such contradiction in the conclusion.
Assume there are more.

**3. Claims stronger than the evidence.** Any sentence whose hedging does not match its interval.
In particular, the shape-versus-location finding rests on n=60 per cell with one bootstrap
interval touching zero; check whether the abstract and conclusion over-sell it.

**4. Divergence between the three versions.** `main_ipm.tex` and `main_nlp.tex` are generated
from `main.tex` by a script. Diff their bodies. If anything other than title, abstract and the
"What is not new" paragraph differs, that is a defect: the three must not drift.

**5. Statistical method.** Is the item-clustered bootstrap the right resampling unit? Are the
Wilson intervals applied to the right quantity? Is Cohen's κ appropriate where it is used? Is
anything reported without an interval that needs one?

**6. Citations.** Thirteen references were added recently. Check that each is (a) real, (b)
correctly attributed, and (c) actually supports the sentence it is attached to. Flag any citation
that is decorative, misattributed, or does not say what the text claims it says.

**7. Reproducibility.** Run what you can. `python family2/analyze_factual.py` and
`python family1/analyze_quad_bank.py` should execute against the released data. Report anything
that errors, or whose output disagrees with the manuscript.

## What I do not want

Do not comment on writing style, on the choice of journal, or on whether the topic is
interesting. Do not suggest additional experiments unless a claim in the paper is unsupportable
without one. Do not praise anything.

## Output format

A numbered list. For each finding:

```
[SEVERITY: fatal | major | minor]
WHERE: file and line, or section and sentence
CLAIM: what the paper says
PROBLEM: what is wrong with it
EVIDENCE: the number, the diff, or the command output that shows it
FIX: the smallest change that resolves it
```

End with a one-line verdict: would you recommend reject, major revision, minor revision, or
accept, and the single most important reason.
warning: Skill descriptions were shortened to fit the skills context budget. Codex can still see every skill, but some descriptions are shorter. Disable unused skills or plugins to leave more room for the rest.
codex
I’ll use the `anthropic-skills:paper-reviewer` skill because this is a manuscript review with explicit evidence-checking requirements. I’m going to read that instruction file first, then inspect the manuscript, scripts, and raw data before forming findings.
exec
"C:\\WINDOWS\\System32\\WindowsPowerShell\\v1.0\\powershell.exe" -Command "Get-Content -LiteralPath 'C:\\Users\\HP\\.codex\\plugins\\cache\\claude-cowork\\anthropic-skills\\1.0.0\\skills\\paper-reviewer\\SKILL.md'" in C:\Users\HP\Documents\MeasurementScience_Evals\paper11_elicitation_method
 succeeded in 13170ms:
---
name: paper-reviewer
description: "Comprehensive academic paper review system for research articles. Automatically evaluates papers based on scientific rigor, clarity, originality, data presentation, and bibliographic quality. Generates tracked-change versions with corrections, visual diagrams when beneficial, formatted outputs matching journal styles, and detailed review reports with change suggestions before implementation. Use when reviewing scientific manuscripts, research articles, or when asked to evaluate, improve, or provide feedback on academic papers."
license: MIT
---

# Academic Paper Reviewer

## Overview

This skill provides a systematic workflow for reviewing academic research papers with a focus on:
1. **Scientific methodology rigor**
2. **Writing clarity and structure**
3. **Originality and contribution**
4. **Results analysis quality**
5. **Complete bibliographic references**
6. **Argumentative coherence**
7. **Data presentation (tables/figures)**

## Custom Review Format Support

Users can provide a custom review format file that defines:
- Specific evaluation criteria
- Scoring rubrics
- Required sections
- Journal-specific requirements
- Custom checklists

### Detecting Custom Format Files

When multiple files are uploaded, check for review format indicators:
- Filenames containing: "formato", "format", "rubrica", "rubric", "criterios", "criteria", "plantilla", "template", "guia", "guide"
- Files with evaluation checklists or scoring tables
- Documents describing review requirements

If a custom format file is detected:
1. **Read the format file first** to understand requirements
2. **Extract criteria** (what to evaluate)
3. **Extract scoring system** (how to score each criterion)
4. **Extract required sections** for the review report
5. **Note any specific journal/conference requirements**
6. **Adapt the workflow** to match the custom format

### Using Custom Format

When custom format is provided:
```
User uploads:
- paper.docx (the paper to review)
- formato_revision.docx (custom review format)

Claude:
1. Identifies formato_revision.docx as review format
2. Reads and parses the format requirements
3. Adapts evaluation to match specified criteria
4. Generates report following the custom structure
5. Uses custom scoring system (if provided)
6. Includes all required sections from template
```

If no custom format is provided, use the default workflow below.

## Workflow

When a user uploads a paper (.docx, .pdf) or asks for paper review, follow this systematic process:

### Phase 0: Check for Custom Review Format (NEW)

**First, check if user provided a review format file:**

```bash
# List uploaded files
view /mnt/user-data/uploads
```

**Look for files indicating review format:**
- Names with: formato, format, rubrica, rubric, criterios, template, plantilla, guia
- Files that are clearly NOT the paper itself

**If custom format found:**
1. Read the format file completely
2. Extract all evaluation criteria
3. Note scoring system (numerical, categories, etc.)
4. Identify required report sections
5. Adapt Phases 1-5 to match this format

**If no custom format:**
- Proceed with default workflow (Phases 1-5)

### Phase 1: Initial Analysis (Read-only)

1. **Read the skill documentation first:**
   ```bash
   view /mnt/skills/public/docx/SKILL.md- Overall flow and coherence
- Multiple comparison corrections- Primary sources for key claims- Contradictions absence
- Captions: complete and self-explanatory



### 1. Scientific Methodology - [Score: X/10]- [ ] Change 2: [Description with specific location]
[Same format as above]

### Optional Improvements (Nice to have)
1. **[Section]** - Line X: [Description]

---

## VISUAL IMPROVEMENTS NEEDED

### Figures to Create/Modify:
- [ ] **Figure 1:** [Description of diagram/chart needed]
  - Type: [Flow chart / Bar chart / Scatter plot / etc.]
  - Purpose: [What it should communicate]
  - Location: After paragraph [X] in section [Y]

### Tables to Create/Modify:
- [ ] **Table 1:** [Description]
  - Format: [Structure needed]
  - Location: [Where it should go]

---

## FORMATTING REQUIREMENTS

**Journal Format Detected:** [Name of journal if identified, or "Not specified"]
**Required Format Adjustments:**
- [ ] Citation style: [APA / IEEE / Vancouver / etc.]
- [ ] Section headings format
- [ ] Figure/Table numbering
- [ ] Abstract word limit
- [ ] Keywords format
- [ ] Other specific requirements

---

## NEXT STEPS

Before proceeding with implementation, please review this report and:
1. Confirm which changes you want to implement
2. Specify the target journal format (if not already clear)
3. Indicate if you want me to proceed with automatic corrections

Once confirmed, I will:
1. Create a revised version with tracked changes
2. Generate required figures/diagrams
3. Format according to journal specifications
4. Provide both versions (original + corrected)
```

### Phase 3: Automatic Implementation (NEW - No confirmation needed)

**AUTOMATIC WORKFLOW: After generating review report, immediately proceed to create improved paper.**

The skill now automatically:
1. Generates comprehensive review report
2. Creates all necessary figures (300 DPI, professional quality)
3. Implements all corrections in the paper
4. Inserts figures at appropriate locations
5. Delivers both review report AND improved paper

**No user confirmation needed** - this creates a complete deliverable immediately.

### Phase 4: Automatic Generation of Improved Paper

**IMPORTANT: This phase executes AUTOMATICALLY after Phase 2 (review report).**

1. **Analyze paper data to determine needed figures:**
   - Survey data â†’ Bar charts, pie charts
   - Comparisons â†’ Grouped bar charts
   - Methodology â†’ Flow diagrams
   - Distributions â†’ Pie charts or histograms
   - Relationships â†’ Scatter plots, network diagrams

2. **Generate ALL figures automatically:**
   ```python
   # Generate figures based on paper content
   # All at 300 DPI minimum
   # Professional color schemes (colorblind-friendly)
   # Save to /mnt/user-data/outputs/
   ```

3. **Create improved paper with docx-js:**
   - Read docx skill: `view /mnt/skills/public/docx/SKILL.md`
   - Implement all corrections from review
   - Insert figures at appropriate locations
   - Add professional captions
   - Apply formatting improvements
   - Save as: `paper_IMPROVED_[original_name].docx`

4. **File naming convention:**
   - Review report: `REVIEW_[paper_name].md`
   - Improved paper: `IMPROVED_[paper_name].docx`
   - Figures: `fig_N_[description].png`

5. **Automatic deliverables:**
   - Review report with all findings
   - Improved paper with figures inserted
   - Individual figure files (for presentations/slides)
   - No user interaction required - everything ready immediately

4. **Create high-quality figures and diagrams:**
   
   **IMPORTANT:** Always create figures for papers - they significantly improve paper quality.
   
   **Types of figures to create:**
   
   a. **Bar charts for survey/categorical data:**
   ```python
   import matplotlib.pyplot as plt
   import numpy as np
   
   # High-quality settings
   plt.rcParams['figure.dpi'] = 300
   plt.rcParams['savefig.dpi'] = 300
   plt.rcParams['font.family'] = 'Arial'
   plt.rcParams['font.size'] = 12
   
   # Create figure
   fig, ax = plt.subplots(figsize=(10, 6))
   
   # Example: Survey responses
   categories = ['Pregunta 1', 'Pregunta 2', 'Pregunta 3']
   si_values = [74, 89, 95]
   no_values = [25, 11, 5]
   
   x = np.arange(len(categories))
   width = 0.35
   
   bars1 = ax.bar(x - width/2, si_values, width, label='SÃ­', color='#2E7D32', alpha=0.8)
   bars2 = ax.bar(x + width/2, no_values, width, label='No', color='#C62828', alpha=0.8)
   
   # Add value labels on bars
   for bars in [bars1, bars2]:
       for bar in bars:
           height = bar.get_height()
           ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{height}%', ha='center', va='bottom', fontsize=10)
   
   ax.set_xlabel('Preguntas de la encuesta', fontsize=14, fontweight='bold')
   ax.set_ylabel('Porcentaje (%)', fontsize=14, fontweight='bold')
   ax.set_title('Resultados de la Encuesta', fontsize=16, fontweight='bold', pad=20)
   ax.set_xticks(x)
   ax.set_xticklabels(categories, rotation=0)
   ax.legend(fontsize=12, framealpha=0.9)
   ax.set_ylim(0, 100)
   ax.grid(axis='y', alpha=0.3, linestyle='--')
   ax.spines['top'].set_visible(False)
   ax.spines['right'].set_visible(False)
   
   plt.tight_layout()
   plt.savefig('/mnt/user-data/outputs/figura_1_encuesta.png', dpi=300, bbox_inches='tight')
   plt.close()
   ```
   
   b. **Pie charts for distribution data:**
   ```python
   # Create professional pie chart
   fig, ax = plt.subplots(figsize=(10, 8))
   
   sizes = [50, 46, 4]  # Example: satisfaction levels
   labels = ['Insatisfecho\n(50%)', 'Poco satisfecho\n(46%)', 'Satisfecho\n(4%)']
   colors = ['#C62828', '#F57C00', '#2E7D32']
   explode = (0.05, 0.05, 0.1)  # Explode smallest slice
   
   wedges, texts, autotexts = ax.pie(sizes, explode=explode, labels=labels, colors=colors,
                                       autopct='%1.0f%%', shadow=True, startangle=90,
                                       textprops={'fontsize': 12, 'fontweight': 'bold'})
   
   ax.set_title('Nivel de SatisfacciÃ³n con el Servicio IESS TulcÃ¡n', 
                fontsize=16, fontweight='bold', pad=20)
   
   plt.savefig('/mnt/user-data/outputs/figura_satisfaccion.png', dpi=300, bbox_inches='tight')
   plt.close()
   ```
   
   c. **Comparison charts (grouped bars):**
   ```python
   # Compare two entities
   fig, ax = plt.subplots(figsize=(12, 7))
   
   categories = ['PoblaciÃ³n', 'MÃ©dicos\nespecialistas', 'Camas\nhospitalarias', 
                 'AtenciÃ³n\n24 horas', 'Tipo de\ncentro']
   tulcan = [86498, 5, 0, 0, 1]  # Example data - use real values
   chone = [52810, 15, 30, 1, 2]  # Example data - use real values
   
   x = np.arange(len(categories))
   width = 0.35
   
   bars1 = ax.bar(x - width/2, tulcan, width, label='TulcÃ¡n', color='#1976D2', alpha=0.8)
   bars2 = ax.bar(x + width/2, chone, width, label='Chone', color='#388E3C', alpha=0.8)
   
   # Add value labels
   for bars in [bars1, bars2]:
       for bar in bars:
           height = bar.get_height()
           ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{int(height)}', ha='center', va='bottom', fontsize=10)
   
   ax.set_xlabel('Indicadores', fontsize=14, fontweight='bold')
   ax.set_ylabel('Cantidad', fontsize=14, fontweight='bold')
   ax.set_title('ComparaciÃ³n de Recursos IESS: TulcÃ¡n vs Chone', 
                fontsize=16, fontweight='bold', pad=20)
   ax.set_xticks(x)
   ax.set_xticklabels(categories)
   ax.legend(fontsize=12, loc='upper left')
   ax.grid(axis='y', alpha=0.3, linestyle='--')
   ax.spines['top'].set_visible(False)
   ax.spines['right'].set_visible(False)
   
   plt.tight_layout()
   plt.savefig('/mnt/user-data/outputs/figura_comparacion.png', dpi=300, bbox_inches='tight')
   plt.close()
   ```
   
   d. **Flowcharts using Graphviz:**
   ```python
   from graphviz import Digraph
   
   dot = Digraph(comment='MetodologÃ­a', format='png')
   dot.attr(dpi='300')
   dot.attr('node', shape='box', style='rounded,filled', fillcolor='lightblue', 
            fontname='Arial', fontsize='12')
   dot.attr('edge', fontname='Arial', fontsize='10')
   
   # Add nodes
   dot.node('A', 'PoblaciÃ³n objetivo\n12,435 afiliados IESS')
   dot.node('B', 'CÃ¡lculo de muestra\nn = 222')
   dot.node('C', 'AplicaciÃ³n de\nencuestas')
   dot.node('D', 'AnÃ¡lisis estadÃ­stico')
   dot.node('E', 'Resultados y\nconclusiones')
   
   # Add edges
   dot.edge('A', 'B', label='Muestreo')
   dot.edge('B', 'C', label='RecolecciÃ³n')
   dot.edge('C', 'D', label='Procesamiento')
   dot.edge('D', 'E', label='InterpretaciÃ³n')
   
   dot.render('/mnt/user-data/outputs/figura_metodologia', cleanup=True)
   ```
   
   **Insert figures into Word document:**
   ```python
   # When creating the Word document with docx-js
   const fs = require('fs');
   const { ImageRun } = require('docx');
   
   // Read image
   const imageData = fs.readFileSync('/mnt/user-data/outputs/figura_1_encuesta.png');
   
   // Create paragraph with image
   new Paragraph({
     alignment: AlignmentType.CENTER,
     spacing: { before: 200, after: 200 },
     children: [
       new ImageRun({
         type: "png",
         data: imageData,
         transformation: {
           width: 500,  // Width in pixels
           height: 350  // Height in pixels
         },
         altText: {
           title: "Figura 1",
           description: "Resultados de la encuesta",
           name: "Figura 1"
         }
       })
     ]
   }),
   
   // Add caption
   new Paragraph({
     alignment: AlignmentType.CENTER,
     spacing: { after: 300 },
     children: [
       new TextRun({ 
         text: "Figura 1. Resultados de la encuesta aplicada a afiliados del IESS TulcÃ¡n (n=222)",
         italics: true,
         size: 20
       })
     ]
   })
   ```
   
   **Quality standards for figures:**
   - Resolution: Minimum 300 DPI
   - Format: PNG for charts, SVG for diagrams when possible
   - Colors: Colorblind-friendly palettes
   - Fonts: Arial or similar sans-serif, min 10pt
   - Labels: Clear, readable, no overlapping
   - Captions: Descriptive and self-explanatory
   - File naming: figura_N_descripcion.png

5. **Apply journal formatting:**
   
   Based on user-specified journal, apply:
   - Citation style (APA, IEEE, Vancouver, etc.)
   - Section heading styles
   - Figure/table caption formats
   - Line spacing, margins
   - Font specifications

6. **Pack final document:**
   ```bash
   python /mnt/skills/public/docx/ooxml/scripts/pack.py paper_unpacked/ paper_REVISED.docx
   ```

7. **Generate additional outputs:**
   - Clean version (all changes accepted)
   - Comparison version (shows all changes)
   - Figures folder with all generated images
   - Final review summary

### Phase 5: Delivery

**Automatic delivery for single paper:**

Provide to user immediately:
1. **ðŸ“‹ Review report** - `REVIEW_[paper_name].md`
2. **ðŸ“„ Improved paper** - `IMPROVED_[paper_name].docx` (with all figures inserted)
3. **ðŸ“Š Individual figures** - `fig_1_[desc].png`, `fig_2_[desc].png`, etc.

**For multiple papers (batch processing):**

When user provides a folder with multiple papers:

```bash
# User uploads folder or multiple files
# Skill detects multiple papers and processes each one

For each paper:
  1. Generate review: REVIEW_[paper_name].md
  2. Create figures: fig_[paper_name]_1.png, fig_[paper_name]_2.png, etc.
  3. Generate improved paper: IMPROVED_[paper_name].docx
  4. Organize in output folder with paper name

Output structure:
/outputs/
  /paper1_name/
    REVIEW_paper1_name.md
    IMPROVED_paper1_name.docx
    fig_paper1_name_1.png
    fig_paper1_name_2.png
    ...
  /paper2_name/
    REVIEW_paper2_name.md
    IMPROVED_paper2_name.docx
    fig_paper2_name_1.png
    ...
  BATCH_SUMMARY.md (summary of all reviews)
```

Present with clear explanation:
```
âœ… Processed [N] papers successfully!

ðŸ“ Paper 1: [name]
   ðŸ“‹ REVIEW_[name].md
   ðŸ“„ IMPROVED_[name].docx (with [X] figures)
   ðŸ“Š [X] figures generated

ðŸ“ Paper 2: [name]
   ðŸ“‹ REVIEW_[name].md
   ðŸ“„ IMPROVED_[name].docx (with [X] figures)
   ðŸ“Š [X] figures generated

ðŸ“ Summary: BATCH_SUMMARY.md
```

## Special Considerations

### When to Create Diagrams

Create visual elements when:
- Complex methodology needs clarification
- Results can be better understood visually
- Study design/workflow should be illustrated
- Relationships between variables need showing
- Comparison of conditions requires visualization
- Timeline/process flow is discussed

### Journal Format Recognition

Attempt to auto-detect journal from:
- Document headers/footers
- Citation style used
- Abstract format
- Section naming conventions
- Reference format

Common formats to support:
- **APA 7th Edition** (Psychology, Education, Social Sciences)
- **IEEE** (Engineering, Computer Science)
- **Vancouver** (Medicine, Life Sciences)
- **Chicago** (Humanities)
- **MLA** (Literature, Arts)
- **Nature/Science formats** (High-impact journals)

### Quality Thresholds

Use these scoring guidelines:

- **9-10**: Excellent, publication-ready
- **7-8**: Good, minor revisions needed
- **5-6**: Acceptable, major revisions required
- **3-4**: Significant issues, consider rejection
- **1-2**: Fundamental flaws, reject

## Error Handling

If issues arise:

1. **Cannot parse document:** Try alternative extraction methods
2. **Track changes fail:** Provide corrections in separate document with clear references
3. **Journal format unknown:** Ask user for specifications
4. **Complex figures needed:** Describe what should be created and ask if user prefers manual creation

## Important Reminders

- âœ… ALWAYS generate review report BEFORE making changes
- âœ… ALWAYS get user approval before implementing corrections
- âœ… ALWAYS use tracked changes for transparency
- âœ… ALWAYS preserve original formatting when possible
- âœ… ALWAYS provide both tracked and clean versions
- âœ… NEVER assume journal format without confirmation
- âœ… NEVER skip the review report phase
- âœ… NEVER make changes without showing what will be modified

## Example Usage

### Single Paper Review

**User:** "Please review this paper"

**Claude automatic workflow:**
1. Reads paper-reviewer skill
2. Reads docx skill
3. Extracts paper content
4. Performs comprehensive 7-dimension analysis
5. **Generates review report** â†’ `REVIEW_paper_name.md`
6. **Analyzes data to determine needed figures**
7. **Generates all figures** (300 DPI) â†’ `fig_1.png`, `fig_2.png`, etc.
8. **Creates improved paper with figures inserted** â†’ `IMPROVED_paper_name.docx`
9. **Delivers everything immediately** - no confirmation needed

**User receives:**
- âœ… Complete review report
- âœ… Improved paper with figures
- âœ… Individual figure files

### Multiple Papers (Batch Processing)

**User:** "Review all papers in this folder" (uploads folder with 5 papers)

**Claude automatic workflow:**
For each of 5 papers:
1. Generate review report
2. Create figures based on content
3. Generate improved paper with figures
4. Organize in named subfolder

**User receives:**
- âœ… 5 review reports (clearly named)
- âœ… 5 improved papers with figures
- âœ… All figures organized by paper
- âœ… Batch summary with overview

### Custom Format Review

**User:** Uploads paper.docx + formato_revision.docx

**Claude workflow:**
1. Detects custom format file
2. Reads format requirements
3. Generates review following custom structure
4. Still creates improved paper with figures
5. Applies any format-specific requirements

This ensures a professional, automatic, and complete review process with zero manual intervention needed.

codex
The review skill’s default “improve the paper” path is not relevant here because you asked for a hostile evidentiary review, not edits. I’ll keep this read-only except for transient command outputs and report only concrete defects.
  → Map manuscript quantitative claims and version differences
  • Run released analysis scripts and recompute targeted quantities from JSONL
  • Check statistical-method/citation support for high-risk claims
  • Assemble numbered hostile-review findings with evidence and fixes
codex
I’m starting by locating every place the manuscript states the quantities you singled out, then I’ll inspect the scripts that are supposed to generate them. After that I’ll run the released analyses and compare output directly against the TeX.
exec
"C:\\WINDOWS\\System32\\WindowsPowerShell\\v1.0\\powershell.exe" -Command 'rg --files' in C:\Users\HP\Documents\MeasurementScience_Evals\paper11_elicitation_method
exec
"C:\\WINDOWS\\System32\\WindowsPowerShell\\v1.0\\powershell.exe" -Command "rg -n \"7920|7,920|standard deviation|standard deviations|SD|\\\\pm|±|0\\.41|0\\.05|factor|16|0\\.000|0\\.778|delta|bootstrap|kappa|κ|Cohen|Wilson|shape|location|n=60|60 per cell|threshold|ablation|instruction\" paper/main.tex paper/section_replication.tex paper/main_ipm.tex paper/main_nlp.tex" in C:\Users\HP\Documents\MeasurementScience_Evals\paper11_elicitation_method
exec
"C:\\WINDOWS\\System32\\WindowsPowerShell\\v1.0\\powershell.exe" -Command 'git status --short' in C:\Users\HP\Documents\MeasurementScience_Evals\paper11_elicitation_method
 succeeded in 2465ms:
warning: unable to access 'C:\Users\HP/.config/git/ignore': Permission denied
warning: unable to access 'C:\Users\HP/.config/git/ignore': Permission denied
?? review/

 succeeded in 3861ms:
paper/main_ipm.tex:17:\large Item sampling, instruction framing and threshold placement\\
paper/main_ipm.tex:34:The first is item sampling. A rate computed on one statement is a property of that statement: between-item standard deviations equal or exceed the mean, so a single-item probe carries a 95\% interval half-width of $\pm$ 0.41 on a [0,1] rate. A published figure of 0.661 obtained from one sentence becomes 0.223 over ten. Sizing a test bank for a $\pm$ 0.05 half-width takes 69 items in one family and 20 in the other, and nothing short of measuring tells you which regime you are in.
paper/main_ipm.tex:36:The second is instruction framing, where the obvious ablation misleads. Deleting the sentence that names the measured behaviour barely moves the result; deleting the surrounding framing removes it entirely. A single-step ablation would have exonerated the instrument.
paper/main_ipm.tex:38:The third is threshold placement. Models answer on a coarse numeric grid, so a cut placed on a modal value adjudicates a large share of cases by rounding: moving one cut from 0.60 to 0.90 changes a reported rate by a factor of 16 without touching the data.
paper/main_ipm.tex:43:\section{The shape of the problem}
paper/main_ipm.tex:57:The items may not represent the construct. The instruction may produce the behaviour it
paper/main_ipm.tex:66:item bank with ten matched items per construct, six model families, an instruction that can be
paper/main_ipm.tex:67:ablated in two nested steps, and a decision rule that is a threshold on a sum. Readers who care
paper/main_ipm.tex:74:questions, with the same models, the same wordings and the same two nested ablations. It exists
paper/main_ipm.tex:81:rules that follow from them, the ablation protocol in Section~\ref{sec:instr}, and the whole of
paper/main_ipm.tex:91:ablation, the conversion of the first into a bank size, and a replication on an unrelated
paper/main_ipm.tex:93:The audience we have in mind is whoever has to size, instruct and threshold an evaluation
paper/main_ipm.tex:113:Ablation A & 60 items $\times$ 6 models, instruction reduced & 360 \\
paper/main_ipm.tex:118:Ablation A$'$ & 60 items $\times$ 6 models, instruction reduced & 360 \\
paper/main_ipm.tex:134:threshold rule. Its content does not matter here; what matters is that it is a rate computed over
paper/main_ipm.tex:136:reported number itself, for a reason that is one of the findings: on that bank the threshold rule
paper/main_ipm.tex:162:Construct & mean & SD between items & SD / mean \\
paper/main_ipm.tex:168:Epistemic ignorance & 0.011 & 0.035 & 3.16 \\
paper/main_ipm.tex:171:\caption{Ten items per construct. The standard deviation between item means equals or exceeds
paper/main_ipm.tex:177:approximately $s/\sqrt{k}$, where $s$ is the between-item standard deviation of
paper/main_ipm.tex:184:standard deviation we measure. One item gives a 95\% interval half-width of $\pm 0.41$ on a
paper/main_ipm.tex:189:At one item the 95\% interval half-width is $\pm 0.41$. The interval is wider than most effects
paper/main_ipm.tex:192:$\pm 0.13$. Reaching $\pm 0.05$ takes $69$.
paper/main_ipm.tex:197:values run from $0.000$ to $0.667$. The published figure is not a mismeasurement of its
paper/main_ipm.tex:202:\paragraph{Design rule.} Report the between-item standard deviation, not only the mean. If it
paper/main_ipm.tex:205:not evaluations. In our corpus the aggregate contrast survives such a bootstrap
paper/main_ipm.tex:206:($\Delta = 0.178$, $[0.058, 0.312]$) while the contrast against the nearest single construct
paper/main_ipm.tex:213:Elicited evaluations carry an instruction that explains what is being asked. The instruction is
paper/main_ipm.tex:214:part of the measurement, and when the behaviour of interest is one the instruction mentions,
paper/main_ipm.tex:215:the natural worry is that the instruction produces it.
paper/main_ipm.tex:220:models report values whose sum exceeds one. The instruction names the outcome.
paper/main_ipm.tex:224:what each dimension means---leaving a generic instruction to answer in JSON. Same $60$ items,
paper/main_ipm.tex:232:& instruction & deleted & removed \\
paper/main_ipm.tex:236:Target rate, largest construct & 0.200 & 0.155 & \textbf{0.000} \\
paper/main_ipm.tex:239:Rate on anchors & 0.000 & 0.000 & 0.000 \\
paper/main_ipm.tex:243:\caption{Two nested ablations of the instruction. Deleting the sentences that name the outcome
paper/main_ipm.tex:245:\label{tab:ablation}
paper/main_ipm.tex:251:Had we stopped there, we would have concluded that the instruction was innocent.
paper/main_ipm.tex:256:they are anything else. The honest conclusion is neither that the instruction manufactures the
paper/main_ipm.tex:260:\paragraph{Why one ablation is not enough.} The two conditions disagree, and either alone would
paper/main_ipm.tex:261:have misled us. The minimal ablation says the instruction is innocent; the maximal one says it
paper/main_ipm.tex:265:\paragraph{Design rule.} Run two nested ablations, not one. Remove the smallest span of text
paper/main_ipm.tex:278:\caption{The quantity our decision rule thresholds, as reported. Models answer on a coarse
paper/main_ipm.tex:279:grid, and the threshold falls on the modal value.}
paper/main_ipm.tex:284:corpus there are $46$ distinct values; $97.7\%$ are multiples of $0.05$ and $89.5\%$ are
paper/main_ipm.tex:299:which is the study's control, from $0.000$ to $0.778$. A result that had read as ``the signature
paper/main_ipm.tex:304:\paragraph{Design rule.} Before fixing a threshold, plot the distribution of the quantity it
paper/main_ipm.tex:307:the convention. Where the choice is free, place the threshold off-grid---at $1.025$ rather than
paper/main_ipm.tex:322:own. The pooled coefficient over the bank, $\kappa = 0.184$ \citep{fleiss1971}, should be read
paper/main_ipm.tex:335:sampling sets a floor of roughly seventy items for a $\pm 0.05$ estimate in the first family and
paper/main_ipm.tex:336:twenty in the second. Threshold placement is worth the difference between $0.000$ and $0.778$ on
paper/main_ipm.tex:337:a control condition in the first, and a factor of sixteen in the second. Instruction framing is
paper/main_ipm.tex:339:shape of the response without moving its location; the reason---framing is worth what the model
paper/main_ipm.tex:344:in the main studies, and between-item standard deviations estimated from ten items each: these
paper/main_ipm.tex:347:The shape finding in Section~\ref{sec:instr2} rests on sixty elicitations per cell and is
paper/main_ipm.tex:349:quantity is a property of text produced under an instruction.
paper/main_ipm.tex:359:dispersion we report. The second and third are manipulations of the instrument---an instruction
paper/main_ipm.tex:360:deleted, a threshold moved---applied to a fixed set of items, and neither depends on what the
paper/main_ipm.tex:370:the ablation protocol in Section~\ref{sec:instr} would have led us to the wrong conclusion if
paper/main_ipm.tex:419:The instruction ablation of Section~\ref{sec:instr} was prompted by an adversarial audit of the
paper/section_replication.tex:14:nested instruction ablations. Nothing about four-valued logic appears anywhere in it.
paper/section_replication.tex:17:return exactly $1.000$ and $0.000$, and where ground truth exists the models are well calibrated
paper/section_replication.tex:23:published. On this bank it is close to useless. Four of the five constructs pin to $0.000$ or
paper/section_replication.tex:26:$0.120$---collapses to a rate of $0.028$. The signal is not absent. The threshold removes it.
paper/section_replication.tex:36:\includegraphics[width=\linewidth]{figC_threshold}
paper/section_replication.tex:42:\label{fig:threshold2}
paper/section_replication.tex:45:\subsection{Item sampling replicates, and gives the rule its real shape}
paper/section_replication.tex:47:Measured on the continuous scale, the between-item standard deviation within a construct ranges
paper/section_replication.tex:48:from $0.001$ to $0.112$. Converted to a sample size for a $\pm 0.05$ half-width, that is between
paper/section_replication.tex:54:needs varies by a factor of nearly seventy across ordinary evaluation targets, with no way to
paper/section_replication.tex:61:The second bank carries the same two nested ablations. Condition~A$'$ deletes the sentence that
paper/section_replication.tex:70:$[-0.057,\,+0.013]$. That is the first corpus's result again: the sentence that names the
paper/section_replication.tex:74:to $0.533$---a paired difference of $-0.018$, interval $[-0.052,\,+0.016]$. On the first corpus
paper/section_replication.tex:75:the corresponding ablation took the headline quantity from $0.077$ to $0.004$. Here it does
paper/section_replication.tex:89:nothing. The design rule is unchanged---run both nested ablations---and is now better motivated,
paper/section_replication.tex:90:because the two corpora are the two regimes and nothing short of running the ablation
paper/section_replication.tex:93:\paragraph{A second reason the mean was the wrong summary.} The instruction does change behaviour
paper/section_replication.tex:96:full instruction to $9/60$ under \emph{both} ablations, a paired difference of $-0.133$ with
paper/section_replication.tex:97:intervals $[-0.233,\,-0.050]$ for the full ablation and $[-0.267,\,+0.000]$ for the minimal one.
paper/section_replication.tex:98:The standard deviation of the same answers rises from $0.161$ to between $0.195$ and $0.219$. The
paper/section_replication.tex:99:instruction is read and obeyed; it redistributes mass symmetrically about the midpoint, so the
paper/section_replication.tex:104:under both ablations and because the methodological point does not depend on the significance of
paper/section_replication.tex:105:this particular pair: \emph{an ablation that reads null on the summary statistic can be large on
paper/section_replication.tex:107:framing does not matter here. It matters; it moves the shape and not the location.
paper/section_replication.tex:109:\paragraph{Design rule.} Run both nested ablations, and evaluate each against more than one
paper/section_replication.tex:110:functional of the response distribution---at minimum a location statistic and one shape statistic
paper/section_replication.tex:111:such as the mass on a focal value or the dispersion. Report the ablation as null only if it is
paper/section_replication.tex:117:elicitations, $95.7\%$ multiples of $0.05$ and $86.4\%$ multiples of $0.1$, with $33\%$ of answers
paper/section_replication.tex:118:at exactly $1.00$ and $29\%$ at exactly $0.00$. Figure~\ref{fig:threshold2} shows what a cut does
paper/section_replication.tex:127:Construct & mean & SD b/w models & rate & SD b/w models \\
paper/section_replication.tex:129:well-known true  & 0.999 & 0.001 & 1.000 & 0.000 \\
paper/section_replication.tex:131:obscure false    & 0.012 & 0.022 & 0.000 & 0.000 \\
paper/section_replication.tex:132:well-known false & 0.083 & 0.049 & 0.000 & 0.000 \\
paper/section_replication.tex:133:genuinely open   & 0.560 & 0.110 & 0.028 & 0.054 \\
paper/section_replication.tex:142:The size of the artifact is a factor of $16$: the open-question rate is $0.450$ at a cut of
paper/section_replication.tex:144:others, and a paper reporting any one of them alone would be reporting its own threshold.
paper/section_replication.tex:157:well-known truths to $0.120$ on open questions, a factor of $120$. An agreement coefficient
paper/section_replication.tex:166:instruction framing, does not reappear at all in the size the first corpus gave it---and that
paper/section_replication.tex:172:to $20$; the threshold effect grows from a factor of $2$ to a factor of $16$; the framing effect
paper/section_replication.tex:173:falls from decisive to undetectable in the mean while remaining visible in the shape. Every one of
paper/main_nlp.tex:33:Threshold placement first, because it is the largest and the least discussed. Models answer on a coarse numeric grid---46 distinct values across $7{,}852$ elicited components, 89.5\% of them multiples of 0.1---so a decision rule compared against a fixed constant adjudicates a large share of cases by rounding. In our worked case the cut sits exactly on the modal value: moving from a strict to a non-strict comparison moves a control condition from 0.000 to 0.778, and on the second family moving one cut from 0.60 to 0.90 changes a reported rate by a factor of 16 without touching the data.
paper/main_nlp.tex:35:Instruction framing second, where the natural ablation gives the wrong answer. Deleting the sentence that names the measured behaviour barely moves the result; deleting the surrounding framing removes it. Running only the first half exonerates the prompt. On the second family the framing effect does not replicate at all, and the reason generalises: framing is worth what the model could not have inferred without it.
paper/main_nlp.tex:37:Item sampling third. Between-item standard deviations equal or exceed the mean, so a single-item probe carries a 95\% interval half-width of $\pm$ 0.41; reaching $\pm$ 0.05 takes 69 items in one family and 20 in the other.
paper/main_nlp.tex:42:\section{The shape of the problem}
paper/main_nlp.tex:56:The items may not represent the construct. The instruction may produce the behaviour it
paper/main_nlp.tex:65:item bank with ten matched items per construct, six model families, an instruction that can be
paper/main_nlp.tex:66:ablated in two nested steps, and a decision rule that is a threshold on a sum. Readers who care
paper/main_nlp.tex:73:questions, with the same models, the same wordings and the same two nested ablations. It exists
paper/main_nlp.tex:80:rules that follow from them, the ablation protocol in Section~\ref{sec:instr}, and the whole of
paper/main_nlp.tex:90:corpus, the fact that the second defeats the natural ablation, the conversion of the first
paper/main_nlp.tex:111:Ablation A & 60 items $\times$ 6 models, instruction reduced & 360 \\
paper/main_nlp.tex:116:Ablation A$'$ & 60 items $\times$ 6 models, instruction reduced & 360 \\
paper/main_nlp.tex:132:threshold rule. Its content does not matter here; what matters is that it is a rate computed over
paper/main_nlp.tex:134:reported number itself, for a reason that is one of the findings: on that bank the threshold rule
paper/main_nlp.tex:160:Construct & mean & SD between items & SD / mean \\
paper/main_nlp.tex:166:Epistemic ignorance & 0.011 & 0.035 & 3.16 \\
paper/main_nlp.tex:169:\caption{Ten items per construct. The standard deviation between item means equals or exceeds
paper/main_nlp.tex:175:approximately $s/\sqrt{k}$, where $s$ is the between-item standard deviation of
paper/main_nlp.tex:182:standard deviation we measure. One item gives a 95\% interval half-width of $\pm 0.41$ on a
paper/main_nlp.tex:187:At one item the 95\% interval half-width is $\pm 0.41$. The interval is wider than most effects
paper/main_nlp.tex:190:$\pm 0.13$. Reaching $\pm 0.05$ takes $69$.
paper/main_nlp.tex:195:values run from $0.000$ to $0.667$. The published figure is not a mismeasurement of its
paper/main_nlp.tex:200:\paragraph{Design rule.} Report the between-item standard deviation, not only the mean. If it
paper/main_nlp.tex:203:not evaluations. In our corpus the aggregate contrast survives such a bootstrap
paper/main_nlp.tex:204:($\Delta = 0.178$, $[0.058, 0.312]$) while the contrast against the nearest single construct
paper/main_nlp.tex:211:Elicited evaluations carry an instruction that explains what is being asked. The instruction is
paper/main_nlp.tex:212:part of the measurement, and when the behaviour of interest is one the instruction mentions,
paper/main_nlp.tex:213:the natural worry is that the instruction produces it.
paper/main_nlp.tex:218:models report values whose sum exceeds one. The instruction names the outcome.
paper/main_nlp.tex:222:what each dimension means---leaving a generic instruction to answer in JSON. Same $60$ items,
paper/main_nlp.tex:230:& instruction & deleted & removed \\
paper/main_nlp.tex:234:Target rate, largest construct & 0.200 & 0.155 & \textbf{0.000} \\
paper/main_nlp.tex:237:Rate on anchors & 0.000 & 0.000 & 0.000 \\
paper/main_nlp.tex:241:\caption{Two nested ablations of the instruction. Deleting the sentences that name the outcome
paper/main_nlp.tex:243:\label{tab:ablation}
paper/main_nlp.tex:249:Had we stopped there, we would have concluded that the instruction was innocent.
paper/main_nlp.tex:254:they are anything else. The honest conclusion is neither that the instruction manufactures the
paper/main_nlp.tex:258:\paragraph{Why one ablation is not enough.} The two conditions disagree, and either alone would
paper/main_nlp.tex:259:have misled us. The minimal ablation says the instruction is innocent; the maximal one says it
paper/main_nlp.tex:263:\paragraph{Design rule.} Run two nested ablations, not one. Remove the smallest span of text
paper/main_nlp.tex:276:\caption{The quantity our decision rule thresholds, as reported. Models answer on a coarse
paper/main_nlp.tex:277:grid, and the threshold falls on the modal value.}
paper/main_nlp.tex:282:corpus there are $46$ distinct values; $97.7\%$ are multiples of $0.05$ and $89.5\%$ are
paper/main_nlp.tex:297:which is the study's control, from $0.000$ to $0.778$. A result that had read as ``the signature
paper/main_nlp.tex:302:\paragraph{Design rule.} Before fixing a threshold, plot the distribution of the quantity it
paper/main_nlp.tex:305:the convention. Where the choice is free, place the threshold off-grid---at $1.025$ rather than
paper/main_nlp.tex:320:own. The pooled coefficient over the bank, $\kappa = 0.184$ \citep{fleiss1971}, should be read
paper/main_nlp.tex:333:sampling sets a floor of roughly seventy items for a $\pm 0.05$ estimate in the first family and
paper/main_nlp.tex:334:twenty in the second. Threshold placement is worth the difference between $0.000$ and $0.778$ on
paper/main_nlp.tex:335:a control condition in the first, and a factor of sixteen in the second. Instruction framing is
paper/main_nlp.tex:337:shape of the response without moving its location; the reason---framing is worth what the model
paper/main_nlp.tex:342:in the main studies, and between-item standard deviations estimated from ten items each: these
paper/main_nlp.tex:345:The shape finding in Section~\ref{sec:instr2} rests on sixty elicitations per cell and is
paper/main_nlp.tex:347:quantity is a property of text produced under an instruction.
paper/main_nlp.tex:357:dispersion we report. The second and third are manipulations of the instrument---an instruction
paper/main_nlp.tex:358:deleted, a threshold moved---applied to a fixed set of items, and neither depends on what the
paper/main_nlp.tex:368:the ablation protocol in Section~\ref{sec:instr} would have led us to the wrong conclusion if
paper/main_nlp.tex:417:The instruction ablation of Section~\ref{sec:instr} was prompted by an adversarial audit of the
paper/main.tex:17:\large Item sampling, instruction effects, and threshold artifacts,\\
paper/main.tex:37:between-item standard deviations equal or exceed the mean, so a single-item probe carries a
paper/main.tex:38:95\% interval half-width of $\pm 0.41$ on a $[0,1]$ rate. A published figure of $0.661$ obtained
paper/main.tex:39:from one sentence becomes $0.223$ over ten, and reaching $\pm 0.05$ would take $69$ items in one
paper/main.tex:42:Second, instruction effects, where the obvious ablation misleads. Deleting the sentence that
paper/main.tex:45:Third, threshold artifacts. Models answer on a coarse grid, so a cut placed on a modal
paper/main.tex:47:changes a rate by a factor of $16$ without touching the data.
paper/main.tex:54:\section{The shape of the problem}
paper/main.tex:68:The items may not represent the construct. The instruction may produce the behaviour it
paper/main.tex:77:item bank with ten matched items per construct, six model families, an instruction that can be
paper/main.tex:78:ablated in two nested steps, and a decision rule that is a threshold on a sum. Readers who care
paper/main.tex:85:questions, with the same models, the same wordings and the same two nested ablations. It exists
paper/main.tex:92:rules that follow from them, the ablation protocol in Section~\ref{sec:instr}, and the whole of
paper/main.tex:102:defeats the natural ablation, the conversion of the first into a number of items, and a
paper/main.tex:123:Ablation A & 60 items $\times$ 6 models, instruction reduced & 360 \\
paper/main.tex:128:Ablation A$'$ & 60 items $\times$ 6 models, instruction reduced & 360 \\
paper/main.tex:144:threshold rule. Its content does not matter here; what matters is that it is a rate computed over
paper/main.tex:146:reported number itself, for a reason that is one of the findings: on that bank the threshold rule
paper/main.tex:172:Construct & mean & SD between items & SD / mean \\
paper/main.tex:178:Epistemic ignorance & 0.011 & 0.035 & 3.16 \\
paper/main.tex:181:\caption{Ten items per construct. The standard deviation between item means equals or exceeds
paper/main.tex:187:approximately $s/\sqrt{k}$, where $s$ is the between-item standard deviation of
paper/main.tex:194:standard deviation we measure. One item gives a 95\% interval half-width of $\pm 0.41$ on a
paper/main.tex:199:At one item the 95\% interval half-width is $\pm 0.41$. The interval is wider than most effects
paper/main.tex:202:$\pm 0.13$. Reaching $\pm 0.05$ takes $69$.
paper/main.tex:207:values run from $0.000$ to $0.667$. The published figure is not a mismeasurement of its
paper/main.tex:212:\paragraph{Design rule.} Report the between-item standard deviation, not only the mean. If it
paper/main.tex:215:not evaluations. In our corpus the aggregate contrast survives such a bootstrap
paper/main.tex:216:($\Delta = 0.178$, $[0.058, 0.312]$) while the contrast against the nearest single construct
paper/main.tex:223:Elicited evaluations carry an instruction that explains what is being asked. The instruction is
paper/main.tex:224:part of the measurement, and when the behaviour of interest is one the instruction mentions,
paper/main.tex:225:the natural worry is that the instruction produces it.
paper/main.tex:230:models report values whose sum exceeds one. The instruction names the outcome.
paper/main.tex:234:what each dimension means---leaving a generic instruction to answer in JSON. Same $60$ items,
paper/main.tex:242:& instruction & deleted & removed \\
paper/main.tex:246:Target rate, largest construct & 0.200 & 0.155 & \textbf{0.000} \\
paper/main.tex:249:Rate on anchors & 0.000 & 0.000 & 0.000 \\
paper/main.tex:253:\caption{Two nested ablations of the instruction. Deleting the sentences that name the outcome
paper/main.tex:255:\label{tab:ablation}
paper/main.tex:261:Had we stopped there, we would have concluded that the instruction was innocent.
paper/main.tex:266:they are anything else. The honest conclusion is neither that the instruction manufactures the
paper/main.tex:270:\paragraph{Why one ablation is not enough.} The two conditions disagree, and either alone would
paper/main.tex:271:have misled us. The minimal ablation says the instruction is innocent; the maximal one says it
paper/main.tex:275:\paragraph{Design rule.} Run two nested ablations, not one. Remove the smallest span of text
paper/main.tex:288:\caption{The quantity our decision rule thresholds, as reported. Models answer on a coarse
paper/main.tex:289:grid, and the threshold falls on the modal value.}
paper/main.tex:294:corpus there are $46$ distinct values; $97.7\%$ are multiples of $0.05$ and $89.5\%$ are
paper/main.tex:309:which is the study's control, from $0.000$ to $0.778$. A result that had read as ``the signature
paper/main.tex:314:\paragraph{Design rule.} Before fixing a threshold, plot the distribution of the quantity it
paper/main.tex:317:the convention. Where the choice is free, place the threshold off-grid---at $1.025$ rather than
paper/main.tex:332:own. The pooled coefficient over the bank, $\kappa = 0.184$ \citep{fleiss1971}, should be read
paper/main.tex:345:sampling sets a floor of roughly seventy items for a $\pm 0.05$ estimate in the first family and
paper/main.tex:346:twenty in the second. Threshold placement is worth the difference between $0.000$ and $0.778$ on
paper/main.tex:347:a control condition in the first, and a factor of sixteen in the second. Instruction framing is
paper/main.tex:349:shape of the response without moving its location; the reason---framing is worth what the model
paper/main.tex:354:in the main studies, and between-item standard deviations estimated from ten items each: these
paper/main.tex:357:The shape finding in Section~\ref{sec:instr2} rests on sixty elicitations per cell and is
paper/main.tex:359:quantity is a property of text produced under an instruction.
paper/main.tex:369:dispersion we report. The second and third are manipulations of the instrument---an instruction
paper/main.tex:370:deleted, a threshold moved---applied to a fixed set of items, and neither depends on what the
paper/main.tex:380:the ablation protocol in Section~\ref{sec:instr} would have led us to the wrong conclusion if
paper/main.tex:429:The instruction ablation of Section~\ref{sec:instr} was prompted by an adversarial audit of the

 succeeded in 3916ms:
validity\classification\rater_B.csv
validity\classification\rater_A.csv
validity\classification\key.json
validity\classification\INSTRUCTIONS.md
validity\build_classification_task.py
validity\analyze_classification.py
review\gemini_review.md
review\codex_review.md
review\ADVERSARIAL_PROMPT.md
README.md
paper\section_replication.tex
paper\refs.bib
paper\main_nlp.tex
paper\main_nlp.pdf
paper\main_ipm.tex
paper\main_ipm.pdf
paper\main.tex
paper\main.pdf
paper\figC_threshold.png
paper\figC_threshold.pdf
paper\figB_grid.png
paper\figB_grid.pdf
paper\figA_precision.png
paper\figA_precision.pdf
paper\fig1_between_items.pdf
LICENSE
figures\make_figure_factual.py
figures\make_figures.py
figures\make_fig1_between_items.py
family2\run_factual.py
family2\results\raw_factual_nolicense.jsonl
family2\results\raw_factual_neutral.jsonl
family2\results\raw_factual_full.jsonl
family2\items_factual.json
family2\dedupe_results.py
family2\build_items_factual.py
family2\analyze_factual_v1.py
family2\analyze_factual.py
alternates\READY_TO_FIRE.md
alternates\main_nlp.pdf
alternates\main_ipm.pdf
alternates\build_variants.py
alternates\abstract_NLP_Cambridge.txt
alternates\abstract_IPM.txt
family1\build_items.py
family1\analyze_system_conditions.py
family1\analyze_quad_bank.py
family1\analyze_bank.py
brm_submission\SUBMISSION_BRM.md
brm_submission\Leyva-Vazquez_ThreeWays_BRM_manuscript.pdf
brm_submission\COVER_LETTER.md
brm_submission\abstract_plain.txt
family1\items.json
family1\README.md
family1\run_bank.py
family1\run_neutral_system.py
family1\run_quad_bank.py
family1\run_nolicense_system.py
family1\results\raw_quad_bank.jsonl
family1\results\raw_quadruple_pilot.jsonl
family1\results\raw_nolicense_system.jsonl
family1\results\raw_neutral_system.jsonl
family1\results\raw_bank.jsonl

codex
The first pass found all targeted quantities in the TeX and confirmed the repo contains the raw JSONL and the two requested analysis scripts. There is also an existing `review/` directory in the worktree; I’ll ignore it unless it contains reproducibility clues, and I won’t modify it.
exec
"C:\\WINDOWS\\System32\\WindowsPowerShell\\v1.0\\powershell.exe" -Command "Get-Content -LiteralPath 'paper\\main.tex'" in C:\Users\HP\Documents\MeasurementScience_Evals\paper11_elicitation_method
exec
"C:\\WINDOWS\\System32\\WindowsPowerShell\\v1.0\\powershell.exe" -Command "Get-Content -LiteralPath 'paper\\section_replication.tex'" in C:\Users\HP\Documents\MeasurementScience_Evals\paper11_elicitation_method
exec
"C:\\WINDOWS\\System32\\WindowsPowerShell\\v1.0\\powershell.exe" -Command "Get-Content -LiteralPath 'family1\\analyze_quad_bank.py'" in C:\Users\HP\Documents\MeasurementScience_Evals\paper11_elicitation_method
exec
"C:\\WINDOWS\\System32\\WindowsPowerShell\\v1.0\\powershell.exe" -Command "Get-Content -LiteralPath 'family2\\analyze_factual.py'" in C:\Users\HP\Documents\MeasurementScience_Evals\paper11_elicitation_method
 succeeded in 7138ms:
"""Las tres reglas de diseno, medidas en el banco factual.

Replica del analisis del paper 11 en un dominio sin relacion con el neutrosofico.

NOTA DE DISENO. La primera version de este script tomaba como cantidad principal la
tasa de ALTA CONFIANZA (>= 0.9), por analogia con las tasas de sobreconfianza que
reporta la literatura de calibracion. Sobre los datos reales esa eleccion resulto ser
ella misma el artefacto que la regla 3 predice: cuatro de los cinco constructos quedan
clavados en 0.000 o 1.000, y el unico constructo con dispersion real entre modelos
(SD = 0.111 en la escala continua) colapsa a una tasa de 0.008. La binarizacion no
revela la senal, la corta.

Asi que la cantidad primaria aqui es la CONFIANZA CONTINUA, y la tasa binarizada se
conserva unicamente como demostracion de lo que el umbral le hace a la medida. Esa
inversion es el resultado que el banco factual aporta.

  1. muestreo de items : SD entre items dentro de cada constructo, y cuantos items
                         harian falta para un semiancho de 0.05
  2. instruccion       : full vs sin permiso vs sin encuadre
  3. umbral            : que le hace la binarizacion a la escala continua
  4. acuerdo           : dispersion entre modelos, por constructo

Uso:  python analyze_factual.py
"""
from __future__ import annotations

import json
from itertools import combinations
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
RES = HERE / "results"
HIGH = 0.9
CONSTRUCTS = ["wellknown_true", "wellknown_false", "obscure_true",
              "obscure_false", "unsettled"]


def load(cond):
    p = RES / f"raw_factual_{cond}.jsonl"
    if not p.exists():
        return None
    d = pd.DataFrame([json.loads(l) for l in
                      p.read_text(encoding="utf-8").splitlines() if l.strip()])
    raw = len(d)
    d = d[d["parsed"] & ~d["error"]].copy()
    d["confidence"] = pd.to_numeric(d["confidence"], errors="coerce")
    d = d.dropna(subset=["confidence"])
    d["high"] = (d["confidence"] >= HIGH).astype(int)
    return d, raw


def k_needed(sd, half=0.05):
    """Items necesarios para un semiancho IC95 de `half` dada la SD entre items."""
    return int(np.ceil((1.96 * sd / half) ** 2))


def boot_ci(vals, n=5000, seed=0):
    """IC95 por bootstrap agrupado por item (los items son la unidad de muestreo)."""
    rng = np.random.default_rng(seed)
    vals = np.asarray(vals, dtype=float)
    if len(vals) < 2:
        return (np.nan, np.nan)
    draws = rng.choice(vals, size=(n, len(vals)), replace=True).mean(axis=1)
    return tuple(np.percentile(draws, [2.5, 97.5]))


def main():
    r = load("full")
    if r is None:
        raise SystemExit("falta results/raw_factual_full.jsonl")
    full, full_raw = r
    core = full[~full["is_anchor"]]

    print("=" * 78)
    print("BANCO FACTUAL - replica de las tres reglas en un dominio sin relacion")
    print("=" * 78)
    print(f"condicion principal: {len(full)}/{full_raw} usables "
          f"({1 - len(full) / full_raw:.1%} fallo de parseo)")
    print(f"anclas aritmeticas: confianza media {full[full.is_anchor].groupby('truth')['confidence'].mean().to_dict()}")
    print()

    # ---------- 1. MUESTREO DE ITEMS, EN LA ESCALA CONTINUA ----------
    print("--- 1. MUESTREO DE ITEMS: SD entre items, escala continua ---")
    rows = []
    for c in CONSTRUCTS:
        per = core[core.construct == c].groupby("item_id")["confidence"].mean()
        lo, hi = boot_ci(per.values)
        rows.append({"construct": c, "mean": per.mean(), "sd_between": per.std(ddof=1),
                     "ci_lo": lo, "ci_hi": hi, "min": per.min(), "max": per.max(),
                     "k_for_0.05": k_needed(per.std(ddof=1)), "n_items": len(per)})
    t = pd.DataFrame(rows).set_index("construct")
    print(t.round(3).to_string())
    print()
    print(f"  k requerido va de {int(t['k_for_0.05'].min())} a {int(t['k_for_0.05'].max())} "
          f"items segun el constructo: un factor de "
          f"{t['k_for_0.05'].max() / max(t['k_for_0.05'].min(), 1):.0f}x dentro del mismo banco")
    print("  (en el banco neutrosofico el mismo calculo daba 69; el punto de la regla no es")
    print("   que la SD sea grande, sino que no se puede suponer sin medirla)")
    print()

    # ---------- 2. INSTRUCCION ----------
    print("--- 2. INSTRUCCION: tres condiciones anidadas (solo W1, pareado) ---")
    conds = []
    for name in ["full", "nolicense", "neutral"]:
        rr = load(name)
        if rr is None:
            print(f"  {name}: aun sin correr")
            continue
        d, raw = rr
        conds.append((name, d[d.wording == "W1"]))
    if len(conds) == 3:
        print(f"  {'condicion':<11} {'conf. media':>11} {'IC95':>18} "
              f"{'conf. unsettled':>16} {'tasa >=0.9':>11}")
        for name, d in conds:
            c = d[~d.is_anchor]
            per = c.groupby("item_id")["confidence"].mean()
            lo, hi = boot_ci(per.values)
            u = c[c.construct == "unsettled"]
            print(f"  {name:<11} {c['confidence'].mean():>11.3f} "
                  f"{f'[{lo:.3f}, {hi:.3f}]':>18} "
                  f"{u['confidence'].mean():>16.3f} {c['high'].mean():>11.3f}")
        print()
        print("  contraste pareado por item (misma pregunta W1, mismo modelo):")
        base = conds[0][1].set_index(["item_id", "model"])["confidence"]
        for name, d in conds[1:]:
            other = d.set_index(["item_id", "model"])["confidence"]
            j = pd.concat([base.rename("full"), other.rename(name)], axis=1).dropna()
            diff = j[name] - j["full"]
            lo, hi = boot_ci(diff.values)
            print(f"    {name:<11} delta = {diff.mean():+.3f}  IC95 [{lo:+.3f}, {hi:+.3f}]  "
                  f"n={len(j)}   {'cruza cero' if lo <= 0 <= hi else 'NO cruza cero'}")
        print()
        print("  el efecto donde deberia estar (constructo unsettled, pareado):")
        baseu = conds[0][1].query("construct=='unsettled'").set_index(["item_id", "model"])["confidence"]
        for name, d in conds[1:]:
            o = d.query("construct=='unsettled'").set_index(["item_id", "model"])["confidence"]
            j = pd.concat([baseu.rename("full"), o.rename(name)], axis=1).dropna()
            if len(j) < 2:
                continue
            diff = j[name] - j["full"]
            lo, hi = boot_ci(diff.values)
            print(f"    {name:<11} delta = {diff.mean():+.3f}  IC95 [{lo:+.3f}, {hi:+.3f}]  n={len(j)}")
    print()

    # ---------- 3. UMBRAL: lo que la binarizacion destruye ----------
    print("--- 3. UMBRAL: lo que la binarizacion le hace a la medida ---")
    v = full["confidence"].values
    print(f"  valores distintos: {len(np.unique(v))} en {len(v)} elicitaciones")
    print(f"  multiplos de 0.05: {100 * np.mean(np.abs(v * 20 - np.round(v * 20)) < 1e-9):.1f}%")
    print(f"  multiplos de 0.10: {100 * np.mean(np.abs(v * 10 - np.round(v * 10)) < 1e-9):.1f}%")
    vc = pd.Series(v).value_counts(normalize=True).head(6)
    print("  valores mas frecuentes: " + "  ".join(f"{k:.2f}({100 * x:.0f}%)" for k, x in vc.items()))
    print()
    print("  el mismo constructo, medido de las dos maneras:")
    print(f"  {'constructo':<17} {'conf. continua':>15} {'SD entre modelos':>17} "
          f"{'tasa >=0.9':>11} {'SD de la tasa':>14}")
    for c in CONSTRUCTS:
        s = core[core.construct == c]
        piv = s.pivot_table(index="item_id", columns="model", values="confidence", aggfunc="mean")
        pivh = s.pivot_table(index="item_id", columns="model", values="high", aggfunc="mean")
        print(f"  {c:<17} {s['confidence'].mean():>15.3f} {piv.std(axis=1).mean():>17.3f} "
              f"{s['high'].mean():>11.3f} {pivh.std(axis=1).mean():>14.3f}")
    print()
    print("  sensibilidad del corte (items de constructo):")
    for cut in [0.60, 0.70, 0.80, 0.85, 0.90, 0.95, 0.99]:
        print(f"    >= {cut:.2f}  ->  {(core['confidence'] >= cut).mean():.3f}   "
              f"unsettled {(core[core.construct == 'unsettled']['confidence'] >= cut).mean():.3f}")
    print()

    # ---------- 4. ACUERDO ----------
    print("--- 4. ACUERDO entre familias de modelos ---")
    print("  escala continua, SD entre modelos dentro de cada item:")
    for c in CONSTRUCTS:
        piv = core[core.construct == c].pivot_table(
            index=["item_id", "wording"], columns="model", values="confidence", aggfunc="mean")
        print(f"    {c:<17} {piv.std(axis=1).mean():.3f}")
    piv = core.pivot_table(index=["item_id", "wording"], columns="model",
                           values="confidence", aggfunc="mean").dropna()
    inter = [float(np.abs(piv[a] - piv[b]).mean()) for a, b in combinations(piv.columns, 2)]
    print(f"  desacuerdo medio par a par entre modelos: {np.mean(inter):.3f} (n={len(piv)})")
    intra = []
    for _, g in core.groupby(["item_id", "model"]):
        vals = list(g["confidence"])
        intra += [abs(a - b) for a, b in combinations(vals, 2)]
    print(f"  desacuerdo del mismo modelo entre redacciones: {np.mean(intra):.3f} (n={len(intra)})")
    print(f"  ratio intra/inter: {np.mean(intra) / max(np.mean(inter), 1e-9):.2f}")
    print()

    # ---------- calibracion ----------
    print("--- calibracion, donde hay verdad de referencia ---")
    kn = core[core.truth.notna()].copy()
    kn["p_correct"] = np.where(kn["truth"], kn["confidence"], 1 - kn["confidence"])
    print(kn.groupby("construct")[["confidence", "p_correct"]].mean().round(3).to_string())
    print(f"\n  Brier global (sin unsettled): "
          f"{np.mean((kn['confidence'] - kn['truth'].astype(float)) ** 2):.4f}")


if __name__ == "__main__":
    main()

 succeeded in 7360ms:
"""La escalera de tres peldanos medida sobre 110 items en vez de sobre 8.

El estudio previo (corpus v3 + escalera) tenia UN enunciado por fenomeno, asi que
ninguna afirmacion a nivel de fenomeno era estimable y la varianza entre items era
inaccesible por construccion. Este analisis la estima.

Preguntas, en orden de cuanto deciden sobre el formalismo:

  Q1  ocupacion   : se pueblan los tres peldanos sobre un banco real?
  Q2  N vs I      : son distinguibles, y con cuanta varianza ENTRE items?
  Q3  glosa       : la dependencia de la glosa sobrevive con 110 items?
  Q4  entre items : cuanto varia la asignacion de peldano de un item a otro
                    DENTRO del mismo fenomeno? (inestimable con n=1)
  Q5  contenido   : el peldano depende del contenido o de la marca sintactica,
      vs marca      ahora para los TRES peldanos y no solo para el fuerte

Uso:  python analyze_quad_bank.py [--raw results/raw_quad_bank.jsonl]
"""

from __future__ import annotations

import argparse
import json
from itertools import combinations
from pathlib import Path

import numpy as np
import pandas as pd

OUT = Path(__file__).resolve().parent / "results"
CONTESTED = ["ethical", "ignorance", "vagueness", "contingency", "paradox"]
RUNGS = ["strong", "weak", "very_weak", "classical"]


def load(raw: Path) -> pd.DataFrame:
    rows = [json.loads(l) for l in raw.read_text(encoding="utf-8").splitlines() if l.strip()]
    df = pd.DataFrame(rows)
    n0 = len(df)
    df = df[df["parsed"] & ~df["error"]].copy()
    for c in "TINF":
        df[c] = pd.to_numeric(df[c], errors="coerce")
    df = df.dropna(subset=list("TINF"))
    df["TF"] = df["T"] + df["F"]
    print(f"[datos] registros={n0}  usables={len(df)}  "
          f"fallo de parseo={(n0-len(df))/max(n0,1):.1%}")
    return df


def fleiss(piv):
    piv = piv.dropna()
    if len(piv) < 4 or piv.shape[1] < 2:
        return np.nan, len(piv)
    cats = sorted(set(piv.values.ravel()))
    n = piv.shape[1]
    cnt = np.array([[list(r).count(c) for c in cats] for r in piv.values])
    P = ((cnt ** 2).sum(1) - n) / (n * (n - 1))
    pj = cnt.sum(0) / (len(piv) * n)
    pe = (pj ** 2).sum()
    return (float((P.mean() - pe) / (1 - pe)) if pe < 1 else np.nan), len(piv)


def pct(df, index):
    t = df.groupby(index)["rung"].value_counts(normalize=True).unstack(fill_value=0)
    return t.reindex(columns=RUNGS, fill_value=0).round(3)


def main(raw: Path):
    OUT.mkdir(exist_ok=True)
    df = load(raw)
    core = df[df["phenomenon"].isin(CONTESTED)]
    anchors = df[df["form"] == "anchor"]

    # ---- Q1 ocupacion --------------------------------------------------------
    print("\n=== Q1  ocupacion de los peldanos sobre 110 items ===")
    occ = pct(df.assign(grp=np.where(df["form"] == "anchor", "anchors", "contested")), "grp")
    print(occ.to_string())
    vw = pct(core, "phenomenon").reindex(CONTESTED)["very_weak"]
    print(f"\n  peldano MUY DEBIL, global contested = "
          f"{(core['rung']=='very_weak').mean():.3f}")
    print("  por fenomeno:", vw.to_dict())
    print("  (el estudio con 8 items reporto 0.120; si aqui difiere mucho,")
    print("   aquella cifra era una propiedad de esas ocho oraciones)")
    occ.to_csv(OUT / "quad_q1_occupancy.csv")

    # ---- Q2 N vs I -----------------------------------------------------------
    print("\n=== Q2  N frente a I, con varianza entre items ===")
    r = core["N"].corr(core["I"])
    mad = float((core["N"] - core["I"]).abs().mean())
    print(f"  correlacion global(N, I) = {r:.3f}   |N-I| medio = {mad:.3f}")
    per = core.groupby("item_id")[["N", "I"]].mean()
    print(f"  correlacion ENTRE items (medias por item) = {per['N'].corr(per['I']):.3f}")
    print(f"  medias: I={core['I'].mean():.3f}  N={core['N'].mean():.3f}")
    print("\n  N medio por fenomeno:")
    print(core.groupby("phenomenon")[["I", "N"]].mean().round(3)
              .reindex(CONTESTED).to_string())
    pd.DataFrame([{"corr_global": r, "mad": mad,
                   "corr_between_items": per["N"].corr(per["I"])}]
                 ).to_csv(OUT / "quad_q2_N_vs_I.csv", index=False)

    # ---- Q3 glosa ------------------------------------------------------------
    print("\n=== Q3  dependencia de la glosa sobre el banco ===")
    g = pct(core, "gloss")
    print(g.to_string())
    print(f"  rango de la tasa FUERTE entre glosas = "
          f"{g['strong'].max()-g['strong'].min():.3f}")
    print(f"  rango de MUY DEBIL entre glosas      = "
          f"{g['very_weak'].max()-g['very_weak'].min():.3f}")
    g.to_csv(OUT / "quad_q3_gloss.csv")

    # ---- Q4 varianza ENTRE items --------------------------------------------
    print("\n=== Q4  varianza entre items dentro de fenomeno (lo que n=1 no permitia) ===")
    rows = []
    for ph, gg in core[core["form"] == "bare"].groupby("phenomenon"):
        for rg in ["strong", "weak", "very_weak"]:
            per_item = gg.assign(x=(gg["rung"] == rg).astype(int)) \
                         .groupby("item_id")["x"].mean()
            rows.append({"phenomenon": ph, "rung": rg, "n_items": len(per_item),
                         "mean": round(per_item.mean(), 3),
                         "sd_between_items": round(per_item.std(ddof=1), 3),
                         "min": round(per_item.min(), 3), "max": round(per_item.max(), 3)})
    q4 = pd.DataFrame(rows)
    print(q4.pivot(index="phenomenon", columns="rung",
                   values=["mean", "sd_between_items"]).reindex(CONTESTED).to_string())
    q4.to_csv(OUT / "quad_q4_between_items.csv", index=False)

    # ---- Q5 contenido vs marca, por peldano ---------------------------------
    print("\n=== Q5  contenido vs marca, para los TRES peldanos ===")
    for rg in ["strong", "weak", "very_weak"]:
        t = core.assign(x=(core["rung"] == rg).astype(int)) \
                .pivot_table(index="phenomenon", columns="form", values="x", aggfunc="mean")
        t["delta"] = t["marked"] - t["bare"]
        print(f"\n  --- {rg} ---")
        print(t.reindex(CONTESTED).round(3).to_string())

    # ---- acuerdo -------------------------------------------------------------
    piv = core.pivot_table(index=["item_id", "gloss"], columns="model",
                           values="rung", aggfunc="first")
    k, n = fleiss(piv)
    agr = [float((piv[a] == piv[b]).mean()) for a, b in combinations(piv.columns, 2)]
    print(f"\n=== acuerdo entre adjudicadores sobre el peldano ===")
    print(f"  Fleiss kappa = {k:.3f}  (n = {n} unidades)   acuerdo bruto = {np.mean(agr):.3f}")
    print("  (con 8 items el estudio previo reporto kappa = 0.358 agregado)")

    print(f"\nescritos CSV en {OUT}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--raw", default=str(OUT / "raw_quad_bank.jsonl"))
    main(Path(ap.parse_args().raw))

 succeeded in 7146ms:
\section{Replication on a second construct family}
\label{sec:replication}

The three results above come from one corpus about one subject matter. If they are properties of
the elicited design rather than of that subject matter, they should reappear in a task that
shares the design and nothing else.

So we built a second bank. The construct is factual confidence: the model is shown a statement
and reports a single number in $[0,1]$ for how confident it is that the statement is true. This
is the most ordinary elicited evaluation there is, and the quantity that the calibration
literature reports constantly. Five constructs of ten matched items each---well-known true,
well-known false, obscure true, obscure false, and genuinely open questions with no known
answer---plus ten arithmetic anchors. Same six model families, same three wordings, same two
nested instruction ablations. Nothing about four-valued logic appears anywhere in it.

The bank behaves. Parse failure is $0.0\%$ over $1{,}080$ elicitations, the arithmetic anchors
return exactly $1.000$ and $0.000$, and where ground truth exists the models are well calibrated
(Brier $0.005$). Whatever the bank measures, it is not noise.

\paragraph{The outcome we chose first was the artifact.} We initially tracked a
\emph{high-confidence rate}: the fraction of elicitations at or above $0.9$. That is the
domestic analogue of an overconfidence rate and the form in which such results are almost always
published. On this bank it is close to useless. Four of the five constructs pin to $0.000$ or
$1.000$ with zero between-item variance, and the one construct with real dispersion---the open
questions, where models spread from $0.42$ to $0.74$ across items and disagree with each other by
$0.120$---collapses to a rate of $0.028$. The signal is not absent. The threshold removes it.

That is Section~\ref{sec:thresh} arriving unbidden in a new domain, and it is worth stating in the
form a practitioner will meet it: \emph{the binarisation is not a summary of the measurement, it
is a second measurement, and on this bank it is the one that fails}. We therefore report the
continuous quantity as primary throughout this section and keep the rate only to show what it
costs.

\begin{figure*}[t]
\centering
\includegraphics[width=\linewidth]{figC_threshold}
\caption{Second bank, $1{,}080$ elicitations. Left: reported confidence per elicitation, with the
item means spanned by the bar. The open-question construct occupies the middle of the scale and
spreads across items. Right: the rate that survives binarisation, as a function of where the cut
is placed. Moving the cut from $0.60$ to $0.90$ takes the open-question rate from $0.450$ to
$0.028$ without touching the data.}
\label{fig:threshold2}
\end{figure*}

\subsection{Item sampling replicates, and gives the rule its real shape}

Measured on the continuous scale, the between-item standard deviation within a construct ranges
from $0.001$ to $0.112$. Converted to a sample size for a $\pm 0.05$ half-width, that is between
$1$ and $20$ items \emph{within a single bank}---and the same calculation on the first corpus
returned $69$.

This is a stronger form of the rule than Section~\ref{sec:items} could state on its own. The
finding is not that between-item variance is large. It is that the number of items a construct
needs varies by a factor of nearly seventy across ordinary evaluation targets, with no way to
tell in advance which kind you have. Our own open-question construct needed $20$ items and we
gave it $10$; its interval is correspondingly wide, $[0.496,\,0.624]$.

\subsection{Instruction effects do not replicate in size, and the reason sharpens the rule}
\label{sec:instr2}

The second bank carries the same two nested ablations. Condition~A$'$ deletes the sentence that
licenses hedging---\emph{you are NOT required to commit to a verdict: when the evidence is
insufficient or the question is genuinely open, report a confidence near 0.5}. Condition~B$'$
deletes the surrounding role and scale as well, leaving only \emph{you are a careful evaluator}.
Both are paired: same items, same models, same wording, $360$ elicitations each, $100\%$ parse
rate in all three conditions.

The first half replicates exactly. Deleting the licence moves the open-question construct from
$0.551$ to $0.531$, a paired difference of $-0.020$ with a $95\%$ interval of
$[-0.057,\,+0.013]$. That is the first corpus's result again: the sentence that names the
measured behaviour is worth almost nothing.

The second half does not replicate at all. Deleting the entire framing moves the same construct
to $0.533$---a paired difference of $-0.018$, interval $[-0.052,\,+0.016]$. On the first corpus
the corresponding ablation took the headline quantity from $0.077$ to $0.004$. Here it does
nothing.

\paragraph{Why, and why it was predictable.} The two system messages are not equally load-bearing,
and the asymmetry is structural rather than empirical. In the first corpus the system message
carried the whole conceptual apparatus---four independent components not constrained to sum to
one---which the model cannot reconstruct from the question alone; removing it removed the task.
Here it carries a role label and a scale that the user turn already restates, since the question
is \emph{how confident are you that this statement is true} and already asks for \emph{a single
number in $[0.0, 1.0]$}. There was very little in it to delete.

We state this because it is the useful generalisation, and because stating it after seeing the
number would be worth less: \emph{framing is worth what the model could not have inferred without
it}. For an exotic elicited construct that is everything. For a familiar one it is close to
nothing. The design rule is unchanged---run both nested ablations---and is now better motivated,
because the two corpora are the two regimes and nothing short of running the ablation
distinguishes them in advance.

\paragraph{A second reason the mean was the wrong summary.} The instruction does change behaviour
on this bank. It does not change the mean. On the open-question construct the share of answers at
exactly $0.50$---the value the licence sentence explicitly names---falls from $17/60$ under the
full instruction to $9/60$ under \emph{both} ablations, a paired difference of $-0.133$ with
intervals $[-0.233,\,-0.050]$ for the full ablation and $[-0.267,\,+0.000]$ for the minimal one.
The standard deviation of the same answers rises from $0.161$ to between $0.195$ and $0.219$. The
instruction is read and obeyed; it redistributes mass symmetrically about the midpoint, so the
mean absorbs it and reports nothing.

With sixty elicitations per cell and one wording this is an indication rather than an established
effect, and one of the two intervals touches zero. We report it because the direction is identical
under both ablations and because the methodological point does not depend on the significance of
this particular pair: \emph{an ablation that reads null on the summary statistic can be large on
the distribution the statistic summarises}. Section~\ref{sec:instr} would have concluded that the
framing does not matter here. It matters; it moves the shape and not the location.

\paragraph{Design rule.} Run both nested ablations, and evaluate each against more than one
functional of the response distribution---at minimum a location statistic and one shape statistic
such as the mass on a focal value or the dispersion. Report the ablation as null only if it is
null on both.

\subsection{Threshold artifacts replicate, larger}

Models answer this bank on the same coarse grid: $26$ distinct values across $1{,}080$
elicitations, $95.7\%$ multiples of $0.05$ and $86.4\%$ multiples of $0.1$, with $33\%$ of answers
at exactly $1.00$ and $29\%$ at exactly $0.00$. Figure~\ref{fig:threshold2} shows what a cut does
to that.

\begin{table}[t]
\centering \small
\begin{tabular}{lcccc}
\toprule
& \multicolumn{2}{c}{continuous} & \multicolumn{2}{c}{rate at $\ge 0.9$} \\
\cmidrule(lr){2-3}\cmidrule(lr){4-5}
Construct & mean & SD b/w models & rate & SD b/w models \\
\midrule
well-known true  & 0.999 & 0.001 & 1.000 & 0.000 \\
obscure true     & 0.978 & 0.017 & 0.983 & 0.031 \\
obscure false    & 0.012 & 0.022 & 0.000 & 0.000 \\
well-known false & 0.083 & 0.049 & 0.000 & 0.000 \\
genuinely open   & 0.560 & 0.110 & 0.028 & 0.054 \\
\bottomrule
\end{tabular}
\caption{The same five constructs measured two ways. On the continuous scale the open-question
construct is the one with dispersion to explain; after binarisation at $0.9$ it is
indistinguishable from the two false constructs, all three reading as a rate near zero.}
\label{tab:twoways}
\end{table}

The size of the artifact is a factor of $16$: the open-question rate is $0.450$ at a cut of
$0.60$, $0.089$ at $0.80$, and $0.028$ at $0.90$. None of those numbers is more correct than the
others, and a paper reporting any one of them alone would be reporting its own threshold.

\subsection{Agreement replicates, and is construct-specific}

The second bank has no repetitions, so it cannot decompose rater variance the way
Section~\ref{sec:agree} does. What it has instead is three wordings, which isolates a different
component: how much a single model moves when the question is rephrased. That movement is $0.021$
in mean absolute confidence, against $0.048$ between different models on the same item---a ratio
of $0.44$, close to the $0.52$ the first corpus gives for repetition against models. Two designs,
two different intra terms, the same conclusion: a substantial share of what gets attributed to
model disagreement is not model disagreement.

The new observation is about pooling. Between-model dispersion on this bank runs from $0.001$ on
well-known truths to $0.120$ on open questions, a factor of $120$. An agreement coefficient
computed over a whole bank averages those together and reports a number that describes no
construct in it. Agreement is a property of the item, not of the panel.

\paragraph{Design rule.} Report agreement per construct, or not at all. If a single pooled
coefficient is reported, state the range it was pooled over.

\paragraph{What the second family shows.} Three of the four quantities reappear in a task with no
shared content, and the one that reappears largest is the one we had ranked third. The fourth,
instruction framing, does not reappear at all in the size the first corpus gave it---and that
non-replication is the most useful thing in this section, because it identifies what the effect
depends on. Framing is worth what the model could not have inferred without it, which is
everything for an exotic construct and nearly nothing for a familiar one.

What transfers, then, is the protocol and not a single magnitude. The item count moves from $69$
to $20$; the threshold effect grows from a factor of $2$ to a factor of $16$; the framing effect
falls from decisive to undetectable in the mean while remaining visible in the shape. Every one of
those numbers would have been wrong if borrowed from the other family. That is the argument for
measuring them rather than citing them, and it is the reason we ran a second bank instead of
asserting that the first one generalises.

 succeeded in 7752ms:
\documentclass[11pt,letterpaper]{article}
\usepackage[margin=1.15in]{geometry}
\usepackage{times}
\usepackage[hyphens]{url}
\sloppy
\usepackage{graphicx}
\usepackage{booktabs}
\usepackage{amsmath}
\usepackage{amssymb}
\usepackage{natbib}
\usepackage[hidelinks]{hyperref}
\bibliographystyle{plainnat}
\frenchspacing
\setcounter{secnumdepth}{2}

\title{Three Ways an Elicited Evaluation Measures Its Own Design\\
\large Item sampling, instruction effects, and threshold artifacts,\\
with a worked case and 7{,}920 elicitations}

\author{
  Maikel Y. Leyva-V\'azquez\\
  {\small Universidad Bolivariana del Ecuador, Guayaquil, Ecuador}\\
  {\small Universidad Bernardo O'Higgins, Santiago, Chile}\\
  {\small \texttt{myleyvav@ube.edu.ec}}
}
\date{August 2026}

\begin{document}
\maketitle

\begin{abstract}
A large class of evaluations asks a language model to report a number about a
statement---a confidence, a rating, a degree of some property---and treats that number as a measurement. We quantify three ways such a design measures itself rather than the model, on
$7{,}920$ elicitations across six frontier model families and two unrelated construct families.

First, item sampling. A rate computed on one statement is a property of that statement:
between-item standard deviations equal or exceed the mean, so a single-item probe carries a
95\% interval half-width of $\pm 0.41$ on a $[0,1]$ rate. A published figure of $0.661$ obtained
from one sentence becomes $0.223$ over ten, and reaching $\pm 0.05$ would take $69$ items in one
family and $20$ in the other.

Second, instruction effects, where the obvious ablation misleads. Deleting the sentence that
names the measured behaviour barely moves the result; deleting the surrounding framing removes it. Running only the first half would have exonerated the instrument.

Third, threshold artifacts. Models answer on a coarse grid, so a cut placed on a modal
value adjudicates a large share of cases by rounding: moving one cut from $0.60$ to $0.90$
changes a rate by a factor of $16$ without touching the data.

Replicating all three on an unrelated task shows that no magnitude transfers intact and that the
framing effect does not replicate at all, which sharpens the rule. We state the design rule each result implies and release both item banks, the code and every
generation.
\end{abstract}

\section{The shape of the problem}

Consider an evaluation of the following kind. You have a construct---hallucination, refusal,
value conflict, ambiguity, harmfulness---and you want to know how often a model exhibits some
response to it. You write one or a few statements that instantiate the construct, you ask the
model a question about each, you record a number, and you report the rate. Variants of this
design are everywhere: verbalized confidence \citep{lin2022teaching}, self-reported
uncertainty, LLM-as-judge scoring \citep{zheng2023judging}, self-critique,
constitutional-style self-evaluation, and most bespoke probes built for a paper.

That the resulting numbers are treated as measurements without the apparatus measurement
usually requires is a concern raised both inside NLP \citep{bowmandahl2021} and from
measurement theory \citep{jacobs2021measurement}. The design has three failure modes that
are individually well known and jointly under-measured.
The items may not represent the construct. The instruction may produce the behaviour it
measures. And the decision rule may sit where the model's answers pile up. This paper measures
all three on one corpus, so that the three magnitudes can be compared against each other rather
than asserted in isolation, and then measures them again on a second corpus that shares the
design and nothing else, so that the three can be told apart from the subject matter.

The first corpus comes from a study of a four-valued logic, reported elsewhere
\citep{leyva2026ladder, leyva2026itembank}. That study's subject matter is not the subject
matter here; we use it because it happens to have the design features needed---a purpose-built
item bank with ten matched items per construct, six model families, an instruction that can be
ablated in two nested steps, and a decision rule that is a threshold on a sum. Readers who care
about the logic should read those papers. Readers who run elicited evaluations should find
everything they need here.

The second corpus was built for this paper and shares none of that content. It asks the most
ordinary elicited question there is---how confident are you that this statement is
true---over well-known and obscure facts, well-known and obscure falsehoods, and genuinely open
questions, with the same models, the same wordings and the same two nested ablations. It exists
because a methods paper resting on one subject matter cannot distinguish a property of the design
from a property of that subject matter, and Section~\ref{sec:replication} shows the distinction
is not academic: one of the three effects does not survive the move.

\paragraph{Relation to the companion papers.} This is a methods paper and it makes no claim
about the logic under test there. Its contributions are the three quantities below, the design
rules that follow from them, the ablation protocol in Section~\ref{sec:instr}, and the whole of
the second construct family, which is new data collected for this paper and appears in neither
companion. Where a number is reported in a companion paper we say so.

\paragraph{What is not new.} That elicitation format moves elicited confidence is established
\citep{protocolsens2026}, as is the unreliability of LLM judges \citep{coinflip2026}; that
prompt formatting alone moves accuracy by many points \citep{sclar2024quantifying}; that
few-item instruments are imprecise is elementary psychometrics \citep{cronbach1972}; and that evaluation results deserve intervals is argued directly for
language models by \citet{miller2024errorbars}. What we
add is the size of each effect measured on a common corpus, the fact that the second one
defeats the natural ablation, the conversion of the first into a number of items, and a
replication on an unrelated construct family that shows which of the three magnitudes
transfer---none of them---and why.

\section{Corpus}
\label{sec:corpus}

All results below come from elicitations against six frontier model families, one per vendor,
through a single router at temperature $1.0$: GPT-4o, Claude Sonnet 4, Llama 4 Maverick,
DeepSeek Chat, Qwen3 235B and Mistral Medium 3.1.

\begin{table}[t]
\centering \small
\begin{tabular}{llr}
\toprule
Study & Design & Elicitations \\
\midrule
\multicolumn{3}{@{}l}{\emph{Family I --- epistemic states, four components}} \\
Bank & 110 items $\times$ 6 models $\times$ 3 wordings & 1{,}980 \\
Triple & 110 items $\times$ 6 models $\times$ 3 reps & 1{,}980 \\
Pilot & 8 items $\times$ 6 models $\times$ 3 wordings $\times$ 10 reps & 1{,}440 \\
Ablation A & 60 items $\times$ 6 models, instruction reduced & 360 \\
Ablation B & 60 items $\times$ 6 models, framing removed & 360 \\
\addlinespace[2pt]
\multicolumn{3}{@{}l}{\emph{Family II --- factual confidence, one component}} \\
Factual bank & 60 items $\times$ 6 models $\times$ 3 wordings & 1{,}080 \\
Ablation A$'$ & 60 items $\times$ 6 models, instruction reduced & 360 \\
Ablation B$'$ & 60 items $\times$ 6 models, framing removed & 360 \\
\midrule
& & \textbf{7{,}920} \\
\bottomrule
\end{tabular}
\caption{The corpus. Family~I holds ten matched statements for each of five
constructs---ethical conflict, epistemic ignorance, vagueness, future contingency and logical
paradox---plus ten anchors of settled truth. Family~II (Section~\ref{sec:replication}) is an
unrelated task in the same elicited form: ten statements for each of five constructs---well-known
true, well-known false, obscure true, obscure false and genuinely open---plus ten arithmetic
anchors. Every generation is released.}
\label{tab:corpus}
\end{table}

In Family~I the outcome we track is a binary label derived from the reported numbers by a
threshold rule. Its content does not matter here; what matters is that it is a rate computed over
items, which is the form almost every elicited evaluation takes. In Family~II we report the
reported number itself, for a reason that is one of the findings: on that bank the threshold rule
destroys the measurement rather than summarising it (Section~\ref{sec:replication}).

\section{Item sampling: the rate is a property of the items}
\label{sec:items}

\begin{figure}[t]
\centering
\includegraphics[width=0.72\linewidth]{fig1_between_items}
\caption{Rate for each of the ten items in each construct; the short bar is the construct mean.
Where the effect is large the spread is large. The dashed line is a published figure obtained
from a single statement, which lands on the highest of the ten items measuring the same
construct.}
\label{fig:items}
\end{figure}

That items differ in how much they tell you is the premise of the item-response work applied
to NLP leaderboards and test sets \citep{rodriguez2021evaluation, vania2021comparing};
what we add is the consequence for a rate reported over a handful of them.
Figure~\ref{fig:items} shows the rate for every item separately. The pattern is the finding:
\emph{the spread between items of the same construct is as large as the effect}.

\begin{table}[t]
\centering \small
\begin{tabular}{lccc}
\toprule
Construct & mean & SD between items & SD / mean \\
\midrule
Ethical conflict & 0.222 & 0.211 & 0.95 \\
Logical paradox & 0.117 & 0.193 & 1.66 \\
Vagueness & 0.044 & 0.073 & 1.65 \\
Future contingency & 0.011 & 0.023 & 2.11 \\
Epistemic ignorance & 0.011 & 0.035 & 3.16 \\
\bottomrule
\end{tabular}
\caption{Ten items per construct. The standard deviation between item means equals or exceeds
the construct mean in all five cases.}
\label{tab:sd}
\end{table}

The consequence is quantitative. A rate estimated from $k$ items has a standard error of
approximately $s/\sqrt{k}$, where $s$ is the between-item standard deviation of
Table~\ref{tab:sd}. Taking the largest construct, $s = 0.211$:

\begin{figure}[t]
\centering
\includegraphics[width=0.72\linewidth]{figA_precision}
\caption{Precision of a construct-level rate as a function of items, at the between-item
standard deviation we measure. One item gives a 95\% interval half-width of $\pm 0.41$ on a
scale that runs from $0$ to $1$.}
\label{fig:precision}
\end{figure}

At one item the 95\% interval half-width is $\pm 0.41$. The interval is wider than most effects
anyone reports, which is another way of saying that a single-item probe of a construct like
this one is, to a first approximation, uninformative about the construct. Ten items give
$\pm 0.13$. Reaching $\pm 0.05$ takes $69$.

\paragraph{The worked case.} The corpus we borrow was preceded by a study using one statement
per construct, which reported a rate of $0.661$ for the construct we call ethical conflict
\citep{leyva2026ladder}. Measured over ten items the same quantity is $0.222$, and the per-item
values run from $0.000$ to $0.667$. The published figure is not a mismeasurement of its
sentence; it is an accurate measurement of the most extreme of ten, reported as though it
described the construct. This is the failure mode in its purest form, and we suspect it is
common precisely because nothing in the single-item result looks wrong.

\paragraph{Design rule.} Report the between-item standard deviation, not only the mean. If it
is of the order of the mean---and in five of five constructs here it was---then a difference
between two constructs is not interpretable without an interval that resamples \emph{items},
not evaluations. In our corpus the aggregate contrast survives such a bootstrap
($\Delta = 0.178$, $[0.058, 0.312]$) while the contrast against the nearest single construct
does not ($\Delta = 0.107$, $[-0.060, 0.272]$), and only the item-clustered interval reveals
the difference between those two situations.

\section{Instruction effects: ablate the framing, not the sentence}
\label{sec:instr}

Elicited evaluations carry an instruction that explains what is being asked. The instruction is
part of the measurement, and when the behaviour of interest is one the instruction mentions,
the natural worry is that the instruction produces it.

In our corpus the worry is concrete. The system message reads, in part: \emph{``These dimensions
are NOT constrained to sum to 1.0. A statement can be simultaneously partially true, partially
false, partially indeterminate and partially neutral.''} The study then measures how often
models report values whose sum exceeds one. The instruction names the outcome.

The natural response is to delete the offending sentences and re-run. We did that, and we also
ran a second condition that removes the entire framing---the expert role, the explanation of
what each dimension means---leaving a generic instruction to answer in JSON. Same $60$ items,
same six models, same user message, $360$ elicitations each.

\begin{table}[t]
\centering \small
\begin{tabular}{lccc}
\toprule
& full & permission & framing \\
& instruction & deleted & removed \\
\midrule
Target rate, all items & 0.077 & 0.060 & \textbf{0.004} \\
\quad 95\% CI & [.052,.113] & [.038,.093] & [.001,.020] \\
Target rate, largest construct & 0.200 & 0.155 & \textbf{0.000} \\
Sum exceeds one & 0.973 & 0.947 & 0.696 \\
Sum equals exactly one & 0.027 & 0.049 & \textbf{0.304} \\
Rate on anchors & 0.000 & 0.000 & 0.000 \\
Unparseable responses & 0.6\% & 6.4\% & 7.5\% \\
\bottomrule
\end{tabular}
\caption{Two nested ablations of the instruction. Deleting the sentences that name the outcome
changes little. Removing the framing changes everything---and also withdraws the question.}
\label{tab:ablation}
Removing the framing takes the rate to $0.004$ and raises exact normalization from $2.7\%$ to
$30.4\%$. But this condition does not withdraw a permission; it withdraws the question. A model
asked for four unexplained numbers treats them as a distribution, because nothing has told it
they are anything else. The honest conclusion is neither that the instruction manufactures the
result nor that the result is independent of how it is asked: the behaviour is a property of
the framed question, and does not survive being asked in another language.

\paragraph{Why one ablation is not enough.} The two conditions disagree, and either alone would
have misled us. The minimal ablation says the instruction is innocent; the maximal one says it
is everything. Only the pair locates the effect---in the framing, not the licence---and only
the pair makes clear that the maximal condition is not a control but a different experiment.

\paragraph{Design rule.} Run two nested ablations, not one. Remove the smallest span of text
that names the outcome; separately, remove the framing that makes the question intelligible.
Report both. If they disagree, the effect lives between them, and the paper's claim must be
scoped to the framed question rather than to the model. Report parse failures per condition
too: ours rose more than tenfold, all of it from one model, which is a fact about that model
and not about the manipulation, but a reader cannot know that unless it is broken out.

\section{Threshold artifacts: the rule sits where the answers pile up}
\label{sec:thresh}

\begin{figure}[t]
\centering
\includegraphics[width=0.72\linewidth]{figB_grid}
\caption{The quantity our decision rule thresholds, as reported. Models answer on a coarse
grid, and the threshold falls on the modal value.}
\label{fig:grid}
\end{figure}

Language models do not report continuous numbers. Across $7{,}852$ elicited components in this
corpus there are $46$ distinct values; $97.7\%$ are multiples of $0.05$ and $89.5\%$ are
multiples of $0.1$. The five most common values of one component account for $64\%$ of its
mass. This is a property of how models write numbers, not of the quantity being reported, and
it is stable across all four conditions we ran.

A decision rule that compares such a quantity against a fixed constant therefore adjudicates a
large share of cases by rounding. In our corpus the rule is a strict inequality against $1$,
and the quantity equals exactly $1.00$ in $37.9\%$ of evaluations---the modal value.
Figure~\ref{fig:grid} shows the pile-up sitting on the boundary.

That cutting a continuous quantity into two classes discards information and can mislead is a
long-standing result in psychological methods \citep{maccallum2002}; what is specific here
is that the cut point coincides with the value models return most often.
The consequence is not subtle. Replacing the strict comparison with a non-strict one---a change
no larger than the resolution at which models answer---moves the rate on the anchor condition,
which is the study's control, from $0.000$ to $0.778$. A result that had read as ``the signature
never fires on settled material'' turns out to be a statement about an inequality sign. The
ordering across constructs survives the perturbation, attenuated; the dramatic form of it does
not.

\paragraph{Design rule.} Before fixing a threshold, plot the distribution of the quantity it
cuts. If the cut point coincides with a modal value, report the rate under at least two
tie-breaking conventions and treat any conclusion that changes between them as a property of
the convention. Where the choice is free, place the threshold off-grid---at $1.025$ rather than
$1$---or use a margin, or report the underlying quantity instead of the label.

\section{A fourth, briefly: agreement across model families}
\label{sec:agree}

One further quantity is worth separating because it is routinely misread \citep{cohen1960, shroutfleiss1979}. Studies that use
several models as raters report an agreement coefficient over their labels. With one generation
per cell at a non-zero temperature, such a coefficient cannot distinguish models disagreeing
from a single model answering differently on a rerun.

Our corpus contains a design that separates them, because the pilot has ten repetitions. Within
a single model, two repetitions of the same item under the same wording land on different
labels $17.5\%$ of the time; two different models disagree $33.4\%$ of the time. Roughly half of
the disagreement attributed to raters is stochastic variation a single rater produces on its
own. The pooled coefficient over the bank, $\kappa = 0.184$ \citep{fleiss1971}, should be read
as a bound on reproducibility rather than as a measure of inter-model disagreement.

\paragraph{Design rule.} Either include repetitions and decompose, or report the coefficient as
a reproducibility bound and say why. Do not describe distinct model families as interchangeable
raters; they are different instruments, and the coefficient is not inter-rater reliability in
the sense the term usually carries.

\input{section_replication}

\section{What this does and does not show}

Three magnitudes, two construct families, and no magnitude that transfers between them. Item
sampling sets a floor of roughly seventy items for a $\pm 0.05$ estimate in the first family and
twenty in the second. Threshold placement is worth the difference between $0.000$ and $0.778$ on
a control condition in the first, and a factor of sixteen in the second. Instruction framing is
worth everything in the first and nothing in the mean in the second, where it still moves the
shape of the response without moving its location; the reason---framing is worth what the model

The limits are worth stating plainly. Six models at one point in time, one generation per cell
in the main studies, and between-item standard deviations estimated from ten items each: these
are offered as an order of magnitude, not as constants. The within-cell variation that matters
for the first and third results is estimated from the pilot rather than measured in the bank.
The shape finding in Section~\ref{sec:instr2} rests on sixty elicitations per cell and is
reported as an indication. And nothing here licenses any claim about model internals: every
quantity is a property of text produced under an instruction.

\paragraph{The construct labels are ours, and the results do not rest on them.} We wrote the
items and we assigned them to constructs, so a reader is entitled to ask who says that these ten
statements measure ethical conflict rather than something else. That question is the classical
one of construct validity \citep{cronbachmeehl1955, messick1995}, and it arrives here in
the form measurement theory gives it for computational systems \citep{jacobs2021measurement}. The honest answer is that we do, and that the assignment has not
been validated against independent judges. What we can say is
that the three results are invariant to whether the labels are right. The first is a statement
about dispersion \emph{within} a labelled group, and a group wrongly named still has the
dispersion we report. The second and third are manipulations of the instrument---an instruction
deleted, a threshold moved---applied to a fixed set of items, and neither depends on what the
items are called. Construct labelling would matter for a claim of the form ``models behave
differently on ethical conflict than on vagueness'', and the one such contrast we report, in the
first family, we report as not established. To let others check the labelling rather than take
it on trust, the release includes a blind classification instrument: the unmarked items and the
anchors in randomised order, the construct definitions, and the script that returns agreement
between raters and against our assignment.

What the results do support is narrow and, we think, useful: that these three failure modes are
not hypothetical, that their sizes are comparable to the effects such studies report, and that
the ablation protocol in Section~\ref{sec:instr} would have led us to the wrong conclusion if
we had run only its first half.

\section*{Declarations}

\paragraph{Ethics approval and human participants.} This study involved no human or animal
participants. Every observation in both construct families is a text generation produced by a
commercial language model through a programmatic interface, elicited by prompts written by the
author. No survey, interview, annotation task or crowdworker judgment was collected, and no
personal data were processed. Ethics committee approval and informed consent were therefore
not applicable.

\paragraph{Use of language models.} Language models are the object of study here rather than an
aid to writing: the corpus consists of their outputs, collected between 24 and 26 August 2026
through a single router at temperature $1.0$. Vendors and model versions are named in
Section~\ref{sec:corpus} and recorded with every generation in the released files, because these
results are properties of specific model versions at a specific date and should not be assumed
stable across releases.

\paragraph{Competing interests.} The Family~I corpus was collected for two companion studies
co-authored by the present author, and one published figure re-analysed here ($0.661$) comes
from that work. This paper reports that the figure does not survive a larger item sample. No
other competing interests are declared.

\paragraph{Funding.} This research received no specific grant from any funding agency in the
public, commercial or not-for-profit sectors.

\section*{Data and code availability}

Both item banks, the elicitation and analysis scripts, and all $7{,}920$ raw generations
including response text are public at
\url{https://github.com/mleyvaz/elicited-evaluation-design}. Every figure and table here is
produced by released code from released data. Code is MIT-licensed; the banks and the
generations are CC BY 4.0.

The Family~I generations were collected for the companion studies rather than for this paper.
They are reproduced in full so that every number here can be checked in one place, with their
provenance stated in the repository; the citable source for that bank, together with an
independent re-analysis script written by a party that did not author the studies, remains
\url{https://github.com/mleyvaz/paraconsistent-signature-itembank}.

The second bank is released in the form in which it was analysed, including the first version of
its analysis script. That script took the high-confidence rate as its primary outcome, which
Section~\ref{sec:replication} reports as the artifact it turned out to be; we keep it in the
repository rather than quietly replacing it, because the sequence is part of the evidence for the
third design rule.

\section*{Acknowledgements}

The instruction ablation of Section~\ref{sec:instr} was prompted by an adversarial audit of the
companion study's public data, and would not otherwise have been run.

{\small
\bibliography{refs}
}

\end{document}

codex
The manuscript’s headline numbers are mostly in plain TeX tables, but the replication section mixes rates, continuous means, paired deltas, and bootstrap intervals. I’m reading the exact analysis code now so I can tell whether the scripts compute the same estimands the prose claims.
exec
"C:\\WINDOWS\\System32\\WindowsPowerShell\\v1.0\\powershell.exe" -Command 'python family1/analyze_quad_bank.py' in C:\Users\HP\Documents\MeasurementScience_Evals\paper11_elicitation_method
exec
"C:\\WINDOWS\\System32\\WindowsPowerShell\\v1.0\\powershell.exe" -Command 'python family2/analyze_factual.py' in C:\Users\HP\Documents\MeasurementScience_Evals\paper11_elicitation_method
 succeeded in 34385ms:
[datos] registros=1980  usables=1963  fallo de parseo=0.9%

=== Q1  ocupacion de los peldanos sobre 110 items ===
rung       strong   weak  very_weak  classical
grp                                           
anchors     0.000  0.239      0.017      0.744
contested   0.149  0.743      0.051      0.057

  peldano MUY DEBIL, global contested = 0.051
  por fenomeno: {'ethical': 0.0, 'ignorance': 0.139, 'vagueness': 0.011, 'contingency': 0.062, 'paradox': 0.047}
  (el estudio con 8 items reporto 0.120; si aqui difiere mucho,
   aquella cifra era una propiedad de esas ocho oraciones)

=== Q2  N frente a I, con varianza entre items ===
  correlacion global(N, I) = 0.147   |N-I| medio = 0.362
  correlacion ENTRE items (medias por item) = 0.186
  medias: I=0.624  N=0.305

  N medio por fenomeno:
                 I      N
phenomenon               
ethical      0.456  0.335
ignorance    0.802  0.224
vagueness    0.479  0.289
contingency  0.639  0.250
paradox      0.748  0.424

=== Q3  dependencia de la glosa sobre el banco ===
rung   strong   weak  very_weak  classical
gloss                                     
G1      0.161  0.751      0.065      0.023
G2      0.162  0.732      0.045      0.061
G3      0.124  0.746      0.044      0.086
  rango de la tasa FUERTE entre glosas = 0.038
  rango de MUY DEBIL entre glosas      = 0.021

=== Q4  varianza entre items dentro de fenomeno (lo que n=1 no permitia) ===
              mean                  sd_between_items                 
rung        strong very_weak   weak           strong very_weak   weak
phenomenon                                                           
ethical      0.222     0.000  0.772            0.211     0.000  0.217
ignorance    0.011     0.174  0.612            0.035     0.120  0.236
vagueness    0.044     0.022  0.928            0.073     0.039  0.091
contingency  0.011     0.052  0.926            0.023     0.064  0.082
paradox      0.117     0.067  0.750            0.193     0.107  0.221

=== Q5  contenido vs marca, para los TRES peldanos ===

  --- strong ---
form          bare  marked  delta
phenomenon                       
ethical      0.223   0.472  0.249
ignorance    0.011   0.006 -0.006
vagueness    0.044   0.307  0.263
contingency  0.011   0.006 -0.006
paradox      0.117   0.285  0.168

  --- weak ---
form          bare  marked  delta
phenomenon                       
ethical      0.771   0.528 -0.243
ignorance    0.616   0.744  0.128
vagueness    0.928   0.693 -0.235
contingency  0.927   0.799 -0.128
paradox      0.750   0.676 -0.074

  --- very_weak ---
form          bare  marked  delta
phenomenon                       
ethical      0.000   0.000  0.000
ignorance    0.175   0.102 -0.073
vagueness    0.022   0.000 -0.022
contingency  0.051   0.073  0.022
paradox      0.067   0.028 -0.039

=== acuerdo entre adjudicadores sobre el peldano ===
  Fleiss kappa = 0.184  (n = 287 unidades)   acuerdo bruto = 0.647
  (con 8 items el estudio previo reporto kappa = 0.358 agregado)

escritos CSV en C:\Users\HP\Documents\MeasurementScience_Evals\paper11_elicitation_method\family1\results

 succeeded in 34366ms:
==============================================================================
BANCO FACTUAL - replica de las tres reglas en un dominio sin relacion
==============================================================================
condicion principal: 1080/1080 usables (0.0% fallo de parseo)
anclas aritmeticas: confianza media {False: 0.0, True: 1.0}

--- 1. MUESTREO DE ITEMS: SD entre items, escala continua ---
                  mean  sd_between  ci_lo  ci_hi    min    max  k_for_0.05  n_items
construct                                                                          
wellknown_true   0.999       0.001  0.999  1.000  0.997  1.000           1       10
wellknown_false  0.082       0.073  0.043  0.129  0.000  0.244           9       10
obscure_true     0.978       0.026  0.961  0.992  0.917  0.999           2       10
obscure_false    0.012       0.011  0.006  0.019  0.000  0.033           1       10
unsettled        0.560       0.112  0.496  0.624  0.419  0.736          20       10

  k requerido va de 1 a 20 items segun el constructo: un factor de 20x dentro del mismo banco
  (en el banco neutrosofico el mismo calculo daba 69; el punto de la regla no es
   que la SD sea grande, sino que no se puede suponer sin medirla)

--- 2. INSTRUCCION: tres condiciones anidadas (solo W1, pareado) ---
  condicion   conf. media               IC95  conf. unsettled  tasa >=0.9
  full              0.526     [0.407, 0.641]            0.551       0.393
  nolicense         0.517     [0.395, 0.635]            0.531       0.407
  neutral           0.517     [0.397, 0.635]            0.533       0.403

  contraste pareado por item (misma pregunta W1, mismo modelo):
    nolicense   delta = -0.008  IC95 [-0.016, -0.001]  n=360   NO cruza cero
    neutral     delta = -0.007  IC95 [-0.015, -0.000]  n=360   NO cruza cero

  el efecto donde deberia estar (constructo unsettled, pareado):
    nolicense   delta = -0.020  IC95 [-0.057, +0.013]  n=60
    neutral     delta = -0.018  IC95 [-0.052, +0.016]  n=60

--- 3. UMBRAL: lo que la binarizacion le hace a la medida ---
  valores distintos: 26 en 1080 elicitaciones
  multiplos de 0.05: 95.7%
  multiplos de 0.10: 86.4%
  valores mas frecuentes: 1.00(33%)  0.00(29%)  0.10(8%)  0.50(4%)  0.95(3%)  0.70(3%)

  el mismo constructo, medido de las dos maneras:
  constructo         conf. continua  SD entre modelos  tasa >=0.9  SD de la tasa
  wellknown_true              0.999             0.001       1.000          0.000
  wellknown_false             0.083             0.049       0.000          0.000
  obscure_true                0.978             0.017       0.983          0.031
  obscure_false               0.012             0.022       0.000          0.000
  unsettled                   0.560             0.110       0.028          0.054

  sensibilidad del corte (items de constructo):
    >= 0.60  ->  0.491   unsettled 0.450
    >= 0.70  ->  0.459   unsettled 0.289
    >= 0.80  ->  0.418   unsettled 0.089
    >= 0.85  ->  0.411   unsettled 0.061
    >= 0.90  ->  0.402   unsettled 0.028
    >= 0.95  ->  0.386   unsettled 0.017
    >= 0.99  ->  0.339   unsettled 0.017

--- 4. ACUERDO entre familias de modelos ---
  escala continua, SD entre modelos dentro de cada item:
    wellknown_true    0.001
    wellknown_false   0.055
    obscure_true      0.019
    obscure_false     0.024
    unsettled         0.120
  desacuerdo medio par a par entre modelos: 0.048 (n=150)
  desacuerdo del mismo modelo entre redacciones: 0.021 (n=900)
  ratio intra/inter: 0.44

--- calibracion, donde hay verdad de referencia ---
                 confidence  p_correct
construct                             
obscure_false         0.012      0.988
obscure_true          0.978      0.978
wellknown_false       0.082      0.918
wellknown_true        0.999      0.999

  Brier global (sin unsettled): 0.0047

codex
Both requested scripts execute. Their output already matches several headline claims, but there are two warning signs: the factual script’s own docstring contains stale values that disagree with its output, and the replication prose says “factor of nearly seventy” where the printed factual range is 1 to 20 items within that bank. I’m checking whether those are manuscript defects or only code comments/prose imprecision.
exec
"C:\\WINDOWS\\System32\\WindowsPowerShell\\v1.0\\powershell.exe" -Command "Get-Content -LiteralPath 'figures\\make_figure_factual.py'" in C:\Users\HP\Documents\MeasurementScience_Evals\paper11_elicitation_method
exec
"C:\\WINDOWS\\System32\\WindowsPowerShell\\v1.0\\powershell.exe" -Command "Get-Content -LiteralPath 'family1\\analyze_system_conditions.py'" in C:\Users\HP\Documents\MeasurementScience_Evals\paper11_elicitation_method
exec
"C:\\WINDOWS\\System32\\WindowsPowerShell\\v1.0\\powershell.exe" -Command "Get-Content -LiteralPath 'figures\\make_figures.py'" in C:\Users\HP\Documents\MeasurementScience_Evals\paper11_elicitation_method
exec
"C:\\WINDOWS\\System32\\WindowsPowerShell\\v1.0\\powershell.exe" -Command "Get-Content -LiteralPath 'family1\\analyze_bank.py'" in C:\Users\HP\Documents\MeasurementScience_Evals\paper11_elicitation_method
 succeeded in 6627ms:
"""Tres condiciones del system message sobre los mismos 60 items x 6 modelos x G1.

  LICENCIADA  rol de experto + dimensiones + "NOT constrained to sum to 1.0" +
              "can be simultaneously partially true, partially false"
  SIN LICENCIA  identica menos esas dos frases   <- aisla el factor
  NEUTRA        sin rol, sin dimensiones, sin licencia

Si la tasa fuerte cae en SIN LICENCIA tanto como en NEUTRA, la causa es la licencia.
Si solo cae en NEUTRA, la causa es el encuadre.

Uso:  python analyze_system_conditions.py
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
RES = HERE / "results"
CONT = ["ethical", "ignorance", "vagueness", "contingency", "paradox"]


def load(path):
    rows = [json.loads(l) for l in Path(path).read_text(encoding="utf-8").splitlines() if l.strip()]
    d = pd.DataFrame(rows)
    raw_n = len(d)
    d = d[d["parsed"] & ~d["error"]].copy()
    for c in "TINF":
        d[c] = pd.to_numeric(d[c], errors="coerce")
    d = d.dropna(subset=list("TINF"))
    d["TF"] = d["T"] + d["F"]
    d["sum4"] = d[["T", "I", "N", "F"]].sum(axis=1)
    return d, raw_n


def wilson(k, n, z=1.96):
    if n == 0:
        return (0.0, 0.0)
    p = k / n
    den = 1 + z * z / n
    c = (p + z * z / (2 * n)) / den
    h = z * np.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
    return (max(0.0, c - h), min(1.0, c + h))


def main():
    lic, lic_raw = load(RES / "raw_quad_bank.jsonl")
    lic = lic[(lic["gloss"] == "G1") & (lic["form"].isin(["bare", "anchor"]))]
    nol, nol_raw = load(RES / "raw_nolicense_system.jsonl")
    neu, neu_raw = load(RES / "raw_neutral_system.jsonl")

    conds = [("LICENCIADA", lic, 360), ("SIN LICENCIA", nol, nol_raw), ("NEUTRA", neu, neu_raw)]

    print("=" * 78)
    print("TRES CONDICIONES DEL SYSTEM MESSAGE  â€”  mismos items, modelos y glosa")
    print("=" * 78)
    for name, d, raw in conds:
        print(f"  {name:<13} usables {len(d):3d}/{raw}   fallos de parseo {1-len(d)/raw:.1%}")
    print()

    print("--- 1. PELDANO FUERTE (T+F>1), items contestados ---")
    for name, d, _ in conds:
        c = d[d.phenomenon.isin(CONT)]
        k = int((c["rung"] == "strong").sum())
        lo, hi = wilson(k, len(c))
        print(f"  {name:<13} {k:3d}/{len(c):3d} = {k/len(c):.3f}   IC95 [{lo:.3f}, {hi:.3f}]")
    print()

    print("--- 2. FUERTE EN ITEMS ETICOS (el titular del paper) ---")
    for name, d, _ in conds:
        e = d[(d.phenomenon == "ethical") & (d.form == "bare")]
        k = int((e["rung"] == "strong").sum())
        lo, hi = wilson(k, len(e))
        print(f"  {name:<13} {k:2d}/{len(e):2d} = {k/len(e):.3f}   IC95 [{lo:.3f}, {hi:.3f}]")
    print()

    print("--- 3. DESVIACION DEBIL (suma de los cuatro > 1), contestados ---")
    for name, d, _ in conds:
        c = d[d.phenomenon.isin(CONT)]
        print(f"  {name:<13} {(c['sum4'] > 1).mean():.3f}")
    print()

    print("--- 4. NORMALIZACION ESPONTANEA (suma exactamente 1,00) ---")
    for name, d, _ in conds:
        c = d[d.phenomenon.isin(CONT)]
        print(f"  {name:<13} {(np.abs(c['sum4'] - 1) < 1e-9).mean():.3f}")
    print()

    print("--- 5. DISTRIBUCION DE PELDANOS, contestados ---")
    rows = {}
    for name, d, _ in conds:
        c = d[d.phenomenon.isin(CONT)]
        rows[name] = c["rung"].value_counts(normalize=True)
    t = pd.DataFrame(rows).reindex(["strong", "weak", "very_weak", "classical"]).fillna(0)
    print(t.round(3).to_string())
    print()

    print("--- 6. MEDIAS DE COMPONENTES, contestados ---")
    for name, d, _ in conds:
        c = d[d.phenomenon.isin(CONT)]
        print(f"  {name:<13} " + "  ".join(f"{k}={c[k].mean():.3f}" for k in "TINF")
              + f"   T+F={c['TF'].mean():.3f}   suma4={c['sum4'].mean():.3f}")
    print()

    print("--- 7. ANCLAS (control) ---")
    for name, d, _ in conds:
        a = d[~d.phenomenon.isin(CONT)]
        print(f"  {name:<13} fuerte {(a['rung']=='strong').mean():.3f}   "
              f"suma4>1 {(a['sum4']>1).mean():.3f}   n={len(a)}")
    print()

    print("--- 8. FUERTE POR MODELO, contestados ---")
    t2 = pd.DataFrame({
        name: d[d.phenomenon.isin(CONT)].groupby("model").apply(
            lambda g: (g["rung"] == "strong").mean(), include_groups=False)
        for name, d, _ in conds})
    print(t2.round(3).to_string())
    print()

    print("--- 9. FALLOS DE PARSEO POR MODELO ---")
    for name, path in [("SIN LICENCIA", "raw_nolicense_system.jsonl"),
                       ("NEUTRA", "raw_neutral_system.jsonl")]:
        d = pd.DataFrame([json.loads(l) for l in (RES / path).read_text(encoding="utf-8").splitlines() if l.strip()])
        bad = (~(d["parsed"] & ~d["error"])).groupby(d["model"]).sum()
        print(f"  {name:<13} " + "  ".join(f"{k}={v}" for k, v in bad.items() if v))
    print()

    print("=" * 78)
    print("LECTURA")
    lic_c = lic[lic.phenomenon.isin(CONT)]
    nol_c = nol[nol.phenomenon.isin(CONT)]
    neu_c = neu[neu.phenomenon.isin(CONT)]
    a, b, c = [(x["rung"] == "strong").mean() for x in (lic_c, nol_c, neu_c)]
    print(f"  fuerte: licenciada {a:.3f} -> sin licencia {b:.3f} -> neutra {c:.3f}")
    if a > 0:
        print(f"  la supresion de la licencia explica el {100*(a-b)/a:.0f}% de la caida total")
        print(f"  el encuadre explica el {100*(b-c)/a:.0f}% adicional")
    print("=" * 78)


if __name__ == "__main__":
    main()

 succeeded in 6630ms:
"""Figuras del paper de metodo. Salida PDF vectorial.

  figA_precision.pdf   semiancho del IC95 de una tasa a nivel de constructo
                       en funcion del numero de items, con la SD entre items
                       medida en cinco fenomenos
  figB_grid.pdf        el grano al que responden los modelos: histograma de
                       T+F con la moda sobre el umbral

Paleta validada (dataviz, claro): azul #2a78d6, naranja #eb6834.
"""
from __future__ import annotations

import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
BANK = HERE.parent / "family1" / "results"
OUT  = HERE.parent / "paper"          # las figuras viven junto al .tex

BLUE = "#2a78d6"
ORANGE = "#eb6834"
INK = "#0b0b0b"
INK2 = "#52514e"
MUTED = "#8a8983"
SURFACE = "#ffffff"

plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["Times New Roman", "Nimbus Roman", "DejaVu Serif"],
    "font.size": 8,
    "axes.edgecolor": MUTED, "axes.linewidth": 0.6,
    "xtick.color": INK2, "ytick.color": INK2,
    "xtick.labelsize": 8, "ytick.labelsize": 8,
    "figure.facecolor": SURFACE, "axes.facecolor": SURFACE,
    "savefig.facecolor": SURFACE, "pdf.fonttype": 42,
})


def load():
    rows = [json.loads(l) for l in (BANK / "raw_quad_bank.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
    d = pd.DataFrame(rows)
    d = d[d["parsed"] & ~d["error"]].copy()
    for c in "TINF":
        d[c] = pd.to_numeric(d[c], errors="coerce")
    return d.dropna(subset=list("TINF"))


def figA():
    """Cuantos items hacen falta. Una serie: la curva. Las SD medidas van como marcas."""
    sd_ref = 0.211
    k = np.arange(1, 201)
    hw = 1.96 * sd_ref / np.sqrt(k)

    fig, ax = plt.subplots(figsize=(3.35, 2.5))
    ax.plot(k, hw, color=BLUE, lw=2, zorder=3)

    for kk, lab in [(1, "1 item"), (10, "10"), (69, "69")]:
        h = 1.96 * sd_ref / np.sqrt(kk)
        ax.scatter([kk], [h], s=30, facecolor=BLUE, edgecolor=SURFACE, lw=1, zorder=4)
        ax.annotate(f"{lab}\nÂ±{h:.2f}", xy=(kk, h), xytext=(kk * 1.35, h + 0.035),
                    color=INK, fontsize=7, ha="left", va="bottom", linespacing=1.25)

    ax.axhline(0.05, color=ORANGE, lw=1.2, ls=(0, (4, 2)), zorder=2)
    ax.text(1.05, 0.058, "Â±0.05 target", color=ORANGE, fontsize=7, ha="left", va="bottom")

    ax.set_xscale("log")
    ax.set_xlim(0.9, 220)
    ax.set_ylim(0, 0.46)
    ax.set_xticks([1, 3, 10, 30, 100, 200])
    ax.set_xticklabels(["1", "3", "10", "30", "100", "200"])
    ax.set_xlabel("items per construct")
    ax.set_ylabel("95% CI half-width")
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.grid(color="#e8e7e3", lw=0.6, zorder=0)
    ax.set_axisbelow(True)
    fig.tight_layout(pad=0.3)
    fig.savefig(OUT / "figA_precision.pdf", bbox_inches="tight")
    plt.close(fig)
    print("figA_precision.pdf")


def figB():
    """El grano de la respuesta. Una serie; el umbral va como anotacion."""
    d = load()
    tf = (d["T"] + d["F"]).values

    fig, ax = plt.subplots(figsize=(3.35, 2.3))
    vals, counts = np.unique(np.round(tf, 4), return_counts=True)
    share = counts / counts.sum()
    ax.bar(vals, share, width=0.035, color=BLUE, edgecolor=SURFACE, lw=0.4, zorder=3)

    ax.axvline(1.0, color=ORANGE, lw=1.2, ls=(0, (4, 2)), zorder=4)
    ax.annotate("the threshold sits on\nthe modal value:\nT+F = 1.00 in 37.9%",
                xy=(1.0, 0.30), xytext=(1.18, 0.34),
                color=ORANGE, fontsize=7, ha="left", va="top", linespacing=1.3,
                arrowprops=dict(arrowstyle="-", color=ORANGE, lw=0.7, shrinkA=2, shrinkB=2))

    ax.set_xlim(-0.05, 2.05)
    ax.set_ylim(0, 0.42)
    ax.set_xlabel("T + F, as reported")
    ax.set_ylabel("share of evaluations")
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.grid(axis="y", color="#e8e7e3", lw=0.6, zorder=0)
    ax.set_axisbelow(True)
    fig.tight_layout(pad=0.3)
    fig.savefig(OUT / "figB_grid.pdf", bbox_inches="tight")
    plt.close(fig)
    print("figB_grid.pdf")


if __name__ == "__main__":
    figA()
    figB()

 succeeded in 6632ms:
"""Figura del segundo banco: lo que el umbral le hace a una medida que si tiene senal.

  figC_threshold.pdf   izquierda, la confianza continua por constructo (la senal);
                       derecha, la tasa binarizada del mismo constructo en funcion
                       de donde se ponga el corte (la senal, destruida)

Paleta validada (dataviz, claro): azul #2a78d6, naranja #eb6834.
"""
from __future__ import annotations

import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np        ax1.hlines(y, per.min(), per.max(), color=col, lw=2.0, zorder=3,
                   path_effects=None)
        ax1.scatter(per.mean(), y, s=26, color=col, zorder=4,
                    edgecolor=SURFACE, linewidth=1.4)
    ax1.set_yticks(ypos, [LABEL[c] for c in ORDER])
    ax1.set_xlim(-0.04, 1.04)
    ax1.set_xticks([0, 0.25, 0.5, 0.75, 1.0])
    ax1.set_xlabel("reported confidence that the statement is true")
    ax1.axvline(0.9, color=INK2, lw=0.9, ls=(0, (3, 2)), zorder=1)
    ax1.text(0.9, len(ORDER) - 0.42, "  the 0.9 cut", color=INK2, fontsize=7.2, va="top")
    for s in ("top", "right", "left"):
        ax1.spines[s].set_visible(False)
    ax1.tick_params(axis="y", length=0)
    ax1.set_title("The measure has signal", loc="left", fontsize=8.6,
                  color=INK, fontweight="bold", pad=6)

    # ---- derecha: la misma senal, binarizada, en funcion del corte ----
    cuts = np.arange(0.50, 1.001, 0.01)
    for c in ORDER:
        s = d[d.construct == c]["confidence"].values
        rates = [(s >= k).mean() for k in cuts]
        col = ORANGE if c == "unsettled" else BLUE
        ax2.plot(cuts, rates, color=col, lw=2.0 if c == "unsettled" else 1.1,
                 alpha=1.0 if c == "unsettled" else 0.45, zorder=3 if c == "unsettled" else 2,
                 solid_capstyle="round")
    u = d[d.construct == "unsettled"]["confidence"].values
    for k in (0.60, 0.90):
        ax2.scatter(k, (u >= k).mean(), s=26, color=ORANGE, zorder=5,
                    edgecolor=SURFACE, linewidth=1.4)
        ax2.annotate(f"{(u >= k).mean():.2f}", (k, (u >= k).mean()),
                     textcoords="offset points", xytext=(6, 5),
                     fontsize=7.6, color=ORANGE, fontweight="bold")
    ax2.annotate("genuinely open", (0.72, (u >= 0.72).mean()),
                 textcoords="offset points", xytext=(10, 12), fontsize=7.6,
                 color=ORANGE, fontweight="bold")
    ax2.annotate("the two true constructs", (0.56, 1.0),
                 textcoords="offset points", xytext=(0, -13), fontsize=7.2, color=INK2)
    ax2.annotate("the two false constructs", (0.545, 0.0),
                 textcoords="offset points", xytext=(0, 8), fontsize=7.2, color=INK2)
    ax2.annotate("steps are the response grid:\n83% of answers\nare multiples of 0.10",
                 (0.985, 0.56), xycoords="axes fraction",
                 fontsize=6.9, color=MUTED, ha="right", va="top", style="italic",
                 linespacing=1.45)
    ax2.set_xlim(0.5, 1.0)
    ax2.set_ylim(-0.03, 1.03)
    ax2.set_xlabel("where the high-confidence cut is placed")
    ax2.set_ylabel("resulting rate")
    for s in ("top", "right"):
        ax2.spines[s].set_visible(False)
    ax2.set_title("Binarising it does not", loc="left", fontsize=8.6,
                  color=INK, fontweight="bold", pad=6)

    fig.savefig(OUT / "figC_threshold.pdf", bbox_inches="tight", dpi=300)
    fig.savefig(OUT / "figC_threshold.png", bbox_inches="tight", dpi=220)
    print("figC_threshold.pdf / .png")
    print(f"  open construct: continuous mean {u.mean():.3f}, "
          f"rate at 0.60 = {(u>=0.60).mean():.3f}, at 0.90 = {(u>=0.90).mean():.3f}, "
          f"factor {(u>=0.60).mean()/max((u>=0.90).mean(),1e-9):.1f}x")


if __name__ == "__main__":
    main()

 succeeded in 6523ms:
"""Separa CONTENIDO de MARCA SINTACTICA en la firma paraconsistente fuerte.

La pregunta que decide todo es la INTERACCION fenomeno x forma:

  H1  contenido   : los items eticos BARE producen T+F>1 mas que los no-eticos BARE.
                    Si falla, el resultado del corpus v3 era el fraseo.
  H2  marca sola  : los items NO eticos MARKED no producen T+F>1.
                    Si falla, la conjuncion de opuestos dispara la firma por si sola.
  H3  interaccion : el salto bare->marked es mayor en no-eticos que en eticos
                    (porque los eticos ya estaban altos). Cuantifica cuanto de la
                    firma es contenido y cuanto es marca.
  H4  anclas      : tautologias y consensos en cero.
  H5  fiabilidad  : varianza entre items DENTRO de fenomeno, que con n=1 era
                    inestimable y es la razon de ser de este banco.

Uso:  python analyze_bank.py [--raw results/raw_bank.jsonl]
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd

OUT = Path(__file__).resolve().parent / "results"
CONTESTED = ["ethical", "ignorance", "vagueness", "contingency", "paradox"]


def load(raw: Path) -> pd.DataFrame:
    rows = [json.loads(l) for l in raw.read_text(encoding="utf-8").splitlines() if l.strip()]
    df = pd.DataFrame(rows)
    n0 = len(df)
    df = df[df["parsed"] & ~df["error"]].copy()
    for c in "TIF":
        df[c] = pd.to_numeric(df[c], errors="coerce")
    df = df.dropna(subset=list("TIF"))
    df["TF"] = df["T"] + df["F"]
    df["strong"] = (df["TF"] > 1.0).astype(int)
    print(f"[datos] registros={n0}  usables={len(df)}  "
          f"fallo de parseo={(n0-len(df))/max(n0,1):.1%}")
    return df


def boot_ci(x, n=5000, seed=11):
    rng = np.random.default_rng(seed)
    x = np.asarray(x, dtype=float)
    if len(x) < 3:
        return (np.nan, np.nan)
    b = [rng.choice(x, len(x), replace=True).mean() for _ in range(n)]
    return tuple(np.percentile(b, [2.5, 97.5]).round(3))


def main(raw: Path):
    OUT.mkdir(exist_ok=True)
    df = load(raw)
    core = df[df["phenomenon"].isin(CONTESTED)]

    # --- tabla principal: fenomeno x forma -----------------------------------
    tab = core.pivot_table(index="phenomenon", columns="form", values="strong",
                           aggfunc="mean").reindex(CONTESTED).round(3)
    tab["delta"] = (tab["marked"] - tab["bare"]).round(3)
    n = core.pivot_table(index="phenomenon", columns="form", values="strong",
                         aggfunc="size").reindex(CONTESTED)
    print("\n=== TASA FUERTE (T+F>1) por fenomeno x forma ===")
    print(tab.to_string())
    print("\n  n por celda:")
    print(n.to_string())
    tab.to_csv(OUT / "main_phenomenon_x_form.csv")

    # --- H1: contenido -------------------------------------------------------
    eb = core[(core.phenomenon == "ethical") & (core.form == "bare")]["strong"]
    ob = core[(core.phenomenon != "ethical") & (core.form == "bare")]["strong"]
    print("\n=== H1  contenido: etico BARE vs no-etico BARE ===")
    print(f"  etico bare    = {eb.mean():.3f}  IC95 {boot_ci(eb)}  n={len(eb)}")
    print(f"  no-etico bare = {ob.mean():.3f}  IC95 {boot_ci(ob)}  n={len(ob)}")
    print(f"  -> {'SOSTENIDO' if eb.mean() > ob.mean() else 'NO SOSTENIDO'}: "
          "el contenido etico eleva la firma sin marca sintactica"
          if eb.mean() > ob.mean() else
          "  -> NO SOSTENIDO: el resultado del corpus v3 era el fraseo")

    # --- H2: la marca por si sola --------------------------------------------
    om = core[(core.phenomenon != "ethical") & (core.form == "marked")]["strong"]
    print("\n=== H2  marca sola: no-etico MARKED ===")
    print(f"  no-etico marked = {om.mean():.3f}  IC95 {boot_ci(om)}  n={len(om)}")
    print("  -> si es alto, la conjuncion de opuestos dispara la firma por si sola,")
    print("     y la firma NO es diagnostica de conflicto de valores.")

    # --- H3: descomposicion --------------------------------------------------
    em = core[(core.phenomenon == "ethical") & (core.form == "marked")]["strong"]
    print("\n=== H3  cuanto es contenido y cuanto es marca ===")
    print(f"  efecto CONTENIDO (etico bare - no-etico bare) = {eb.mean()-ob.mean():+.3f}")
    print(f"  efecto MARCA     (no-etico marked - no-etico bare) = {om.mean()-ob.mean():+.3f}")
    print(f"  INTERACCION      = {(em.mean()-eb.mean()) - (om.mean()-ob.mean()):+.3f}")

    # --- H4: anclas ----------------------------------------------------------
    anch = df[df["form"] == "anchor"]
    print("\n=== H4  anclas ===")
    print(anch.groupby("phenomenon")[["strong", "TF"]].mean().round(3).to_string())

    # --- H5: variabilidad ENTRE items dentro de fenomeno ---------------------
    print("\n=== H5  variabilidad entre items dentro de cada fenomeno (forma bare) ===")
    rows = []
    for ph, g in core[core.form == "bare"].groupby("phenomenon"):
        per = g.groupby("item_id")["strong"].mean()
        rows.append({"phenomenon": ph, "n_items": len(per), "mean": per.mean().round(3),
                     "sd_between_items": per.std(ddof=1).round(3),
                     "min": per.min().round(3), "max": per.max().round(3)})
    h5 = pd.DataFrame(rows).set_index("phenomenon").reindex(CONTESTED)
    print(h5.to_string())
    print("  Con un item por fenomeno esta columna era inestimable. Si sd es grande,")
    print("  cualquier tasa publicada a partir de un solo enunciado era ruido.")
    h5.to_csv(OUT / "h5_between_item_variance.csv")

    # --- por modelo ----------------------------------------------------------
    print("\n=== robustez por modelo: etico bare vs no-etico bare ===")
    for m, g in core[core.form == "bare"].groupby("model"):
        e = g[g.phenomenon == "ethical"]["strong"].mean()
        o = g[g.phenomenon != "ethical"]["strong"].mean()
        print(f"  {m:20s} etico={e:.3f}  no-etico={o:.3f}  -> {'SI' if e > o else 'NO'}")

    print(f"\nescritos CSV en {OUT}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--raw", default=str(OUT / "raw_bank.jsonl"))
    main(Path(ap.parse_args().raw))

exec
"C:\\WINDOWS\\System32\\WindowsPowerShell\\v1.0\\powershell.exe" -Command 'python family1/analyze_bank.py' in C:\Users\HP\Documents\MeasurementScience_Evals\paper11_elicitation_method
exec
"C:\\WINDOWS\\System32\\WindowsPowerShell\\v1.0\\powershell.exe" -Command 'python figures/make_figure_factual.py' in C:\Users\HP\Documents\MeasurementScience_Evals\paper11_elicitation_method
exec
"C:\\WINDOWS\\System32\\WindowsPowerShell\\v1.0\\powershell.exe" -Command 'python figures/make_figures.py' in C:\Users\HP\Documents\MeasurementScience_Evals\paper11_elicitation_method
exec
"C:\\WINDOWS\\System32\\WindowsPowerShell\\v1.0\\powershell.exe" -Command 'python family1/analyze_system_conditions.py' in C:\Users\HP\Documents\MeasurementScience_Evals\paper11_elicitation_method
 succeeded in 2299ms:
==============================================================================
TRES CONDICIONES DEL SYSTEM MESSAGE  �  mismos items, modelos y glosa
==============================================================================
  LICENCIADA    usables 358/360   fallos de parseo 0.6%
  SIN LICENCIA  usables 337/360   fallos de parseo 6.4%
  NEUTRA        usables 333/360   fallos de parseo 7.5%

--- 1. PELDANO FUERTE (T+F>1), items contestados ---
  LICENCIADA     23/298 = 0.077   IC95 [0.052, 0.113]
  SIN LICENCIA   17/285 = 0.060   IC95 [0.038, 0.093]
  NEUTRA          1/276 = 0.004   IC95 [0.001, 0.020]

--- 2. FUERTE EN ITEMS ETICOS (el titular del paper) ---
  LICENCIADA    12/60 = 0.200   IC95 [0.118, 0.318]
  SIN LICENCIA   9/58 = 0.155   IC95 [0.084, 0.269]
  NEUTRA         0/51 = 0.000   IC95 [0.000, 0.070]

--- 3. DESVIACION DEBIL (suma de los cuatro > 1), contestados ---
  LICENCIADA    0.973
  SIN LICENCIA  0.947
  NEUTRA        0.696

--- 4. NORMALIZACION ESPONTANEA (suma exactamente 1,00) ---
  LICENCIADA    0.027
  SIN LICENCIA  0.049
  NEUTRA        0.304

--- 5. DISTRIBUCION DE PELDANOS, contestados ---
           LICENCIADA  SIN LICENCIA  NEUTRA
rung                                       
strong          0.077         0.060   0.004
weak            0.812         0.825   0.569
very_weak       0.084         0.063   0.127
classical       0.027         0.053   0.301

--- 6. MEDIAS DE COMPONENTES, contestados ---
  LICENCIADA    T=0.407  I=0.617  N=0.282  F=0.374   T+F=0.781   suma4=1.680
  SIN LICENCIA  T=0.405  I=0.622  N=0.286  F=0.388   T+F=0.792   suma4=1.700
  NEUTRA        T=0.357  I=0.575  N=0.227  F=0.288   T+F=0.645   suma4=1.447

--- 7. ANCLAS (control) ---
  LICENCIADA    fuerte 0.000   suma4>1 0.217   n=60
  SIN LICENCIA  fuerte 0.000   suma4>1 0.173   n=52
  NEUTRA        fuerte 0.000   suma4>1 0.035   n=57

--- 8. FUERTE POR MODELO, contestados ---
                    LICENCIADA  SIN LICENCIA  NEUTRA
model                                               
claude-sonnet-4          0.160         0.060    0.02
deepseek-chat            0.100         0.040    0.00
gpt-4o                   0.040         0.080    0.00
llama-4-maverick         0.042         0.029    0.00
mistral-medium-3.1       0.020         0.060    0.00
qwen3-235b               0.100         0.080    0.00

--- 9. FALLOS DE PARSEO POR MODELO ---
  SIN LICENCIA  llama-4-maverick=23
  NEUTRA        llama-4-maverick=27

==============================================================================
LECTURA
  fuerte: licenciada 0.077 -> sin licencia 0.060 -> neutra 0.004
  la supresion de la licencia explica el 23% de la caida total
  el encuadre explica el 73% adicional
==============================================================================

 succeeded in 2418ms:
[datos] registros=1980  usables=1980  fallo de parseo=0.0%

=== TASA FUERTE (T+F>1) por fenomeno x forma ===
form          bare  marked  delta
phenomenon                       
ethical      0.244   0.589  0.345
ignorance    0.000   0.000  0.000
vagueness    0.022   0.317  0.295
contingency  0.000   0.011  0.011
paradox      0.167   0.328  0.161

  n por celda:
form         bare  marked
phenomenon               
ethical       180     180
ignorance     180     180
vagueness     180     180
contingency   180     180
paradox       180     180

=== H1  contenido: etico BARE vs no-etico BARE ===
  etico bare    = 0.244  IC95 (np.float64(0.183), np.float64(0.306))  n=180
  no-etico bare = 0.047  IC95 (np.float64(0.032), np.float64(0.064))  n=720
  -> SOSTENIDO: el contenido etico eleva la firma sin marca sintactica

=== H2  marca sola: no-etico MARKED ===
  no-etico marked = 0.164  IC95 (np.float64(0.138), np.float64(0.19))  n=720
  -> si es alto, la conjuncion de opuestos dispara la firma por si sola,
     y la firma NO es diagnostica de conflicto de valores.

=== H3  cuanto es contenido y cuanto es marca ===
  efecto CONTENIDO (etico bare - no-etico bare) = +0.197
  efecto MARCA     (no-etico marked - no-etico bare) = +0.117
  INTERACCION      = +0.228

=== H4  anclas ===
            strong     TF
phenomenon               
consensus    0.056  0.990
tautology    0.033  1.001

=== H5  variabilidad entre items dentro de cada fenomeno (forma bare) ===
             n_items   mean  sd_between_items  min    max
phenomenon                                               
ethical           10  0.244             0.180  0.0  0.500
ignorance         10  0.000             0.000  0.0  0.000
vagueness         10  0.022             0.047  0.0  0.111
contingency       10  0.000             0.000  0.0  0.000
paradox           10  0.167             0.251  0.0  0.611
  Con un item por fenomeno esta columna era inestimable. Si sd es grande,
  cualquier tasa publicada a partir de un solo enunciado era ruido.

=== robustez por modelo: etico bare vs no-etico bare ===
  claude-sonnet-4      etico=0.333  no-etico=0.075  -> SI
  deepseek-chat        etico=0.267  no-etico=0.042  -> SI
  gpt-4o               etico=0.067  no-etico=0.017  -> SI
  llama-4-maverick     etico=0.033  no-etico=0.050  -> NO
  mistral-medium-3.1   etico=0.300  no-etico=0.033  -> SI
  qwen3-235b           etico=0.467  no-etico=0.067  -> SI

escritos CSV en C:\Users\HP\Documents\MeasurementScience_Evals\paper11_elicitation_method\family1\results

 succeeded in 4848ms:
figA_precision.pdf
figB_grid.pdf

 succeeded in 5140ms:
figC_threshold.pdf / .png
  open construct: continuous mean 0.560, rate at 0.60 = 0.450, at 0.90 = 0.028, factor 16.2x

codex
`analyze_system_conditions.py` reproduces the Family I ablation table exactly, including the parse-failure asymmetry by model. One issue emerging is that different scripts define the Family I “bank” differently: one uses `raw_bank.jsonl`, another uses `raw_quad_bank.jsonl`, and the manuscript’s table appears tied to the latter.
exec
"C:\\WINDOWS\\System32\\WindowsPowerShell\\v1.0\\powershell.exe" -Command 'git status --short' in C:\Users\HP\Documents\MeasurementScience_Evals\paper11_elicitation_method
 succeeded in 596ms:
warning: unable to access 'C:\Users\HP/.config/git/ignore': Permission denied
warning: unable to access 'C:\Users\HP/.config/git/ignore': Permission denied
 M paper/figA_precision.pdf
 M paper/figB_grid.pdf
 M paper/figC_threshold.pdf
?? family1/results/h5_between_item_variance.csv
?? family1/results/main_phenomenon_x_form.csv
?? family1/results/quad_q1_occupancy.csv
?? family1/results/quad_q2_N_vs_I.csv
?? family1/results/quad_q3_gloss.csv
?? family1/results/quad_q4_between_items.csv
?? review/

exec
"C:\\WINDOWS\\System32\\WindowsPowerShell\\v1.0\\powershell.exe" -Command 'git diff --no-index -- paper/main.tex paper/main_nlp.tex' in C:\Users\HP\Documents\MeasurementScience_Evals\paper11_elicitation_method
exec
"C:\\WINDOWS\\System32\\WindowsPowerShell\\v1.0\\powershell.exe" -Command 'git diff --no-index -- paper/main.tex paper/main_ipm.tex' in C:\Users\HP\Documents\MeasurementScience_Evals\paper11_elicitation_method
exec
"C:\\WINDOWS\\System32\\WindowsPowerShell\\v1.0\\powershell.exe" -Command 'git diff --no-index -- paper/main_ipm.tex paper/main_nlp.tex' in C:\Users\HP\Documents\MeasurementScience_Evals\paper11_elicitation_method
 exited 1 in 2513ms:
warning: in the working copy of 'paper/main.tex', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'paper/main_nlp.tex', LF will be replaced by CRLF the next time Git touches it
diff --git a/paper/main.tex b/paper/main_nlp.tex
index 25c2304..fff4219 100644
--- a/paper/main.tex
+++ b/paper/main_nlp.tex
@@ -13,9 +13,8 @@
 \frenchspacing
 \setcounter{secnumdepth}{2}
 
-\title{Three Ways an Elicited Evaluation Measures Its Own Design\\
-\large Item sampling, instruction effects, and threshold artifacts,\\
-with a worked case and 7{,}920 elicitations}
+\title{How Much of an Elicited Evaluation Is the Protocol?\\
+\large Three measured artifacts and the design rules they imply}
 
 \author{
   Maikel Y. Leyva-V\'azquez\\
@@ -29,26 +28,15 @@ with a worked case and 7{,}920 elicitations}
 \maketitle
 
 \begin{abstract}
-A large class of evaluations asks a language model to report a number about a
-statement---a confidence, a rating, a degree of some property---and treats that number as a measurement. We quantify three ways such a design measures itself rather than the model, on
-$7{,}920$ elicitations across six frontier model families and two unrelated construct families.
-
-First, item sampling. A rate computed on one statement is a property of that statement:
-between-item standard deviations equal or exceed the mean, so a single-item probe carries a
-95\% interval half-width of $\pm 0.41$ on a $[0,1]$ rate. A published figure of $0.661$ obtained
-from one sentence becomes $0.223$ over ten, and reaching $\pm 0.05$ would take $69$ items in one
-family and $20$ in the other.
-
-Second, instruction effects, where the obvious ablation misleads. Deleting the sentence that
-names the measured behaviour barely moves the result; deleting the surrounding framing removes it. Running only the first half would have exonerated the instrument.
-
-Third, threshold artifacts. Models answer on a coarse grid, so a cut placed on a modal
-value adjudicates a large share of cases by rounding: moving one cut from $0.60$ to $0.90$
-changes a rate by a factor of $16$ without touching the data.
-
-Replicating all three on an unrelated task shows that no magnitude transfers intact and that the
-framing effect does not replicate at all, which sharpens the rule. We state the design rule each result implies and release both item banks, the code and every
-generation.
+Prompt sensitivity in elicited model judgments is well documented, and the unreliability of LLM-as-a-judge scoring is by now a standard caveat. What is missing is the size of these effects measured together, on one corpus, against the decisions an evaluation designer actually makes. We report three such magnitudes over $7{,}920$ elicitations across six frontier model families, and then measure them again on a second, unrelated construct family.
+
+Threshold placement first, because it is the largest and the least discussed. Models answer on a coarse numeric grid---46 distinct values across $7{,}852$ elicited components, 89.5\% of them multiples of 0.1---so a decision rule compared against a fixed constant adjudicates a large share of cases by rounding. In our worked case the cut sits exactly on the modal value: moving from a strict to a non-strict comparison moves a control condition from 0.000 to 0.778, and on the second family moving one cut from 0.60 to 0.90 changes a reported rate by a factor of 16 without touching the data.
+
+Instruction framing second, where the natural ablation gives the wrong answer. Deleting the sentence that names the measured behaviour barely moves the result; deleting the surrounding framing removes it. Running only the first half exonerates the prompt. On the second family the framing effect does not replicate at all, and the reason generalises: framing is worth what the model could not have inferred without it.
+
+Item sampling third. Between-item standard deviations equal or exceed the mean, so a single-item probe carries a 95\% interval half-width of $\pm$ 0.41; reaching $\pm$ 0.05 takes 69 items in one family and 20 in the other.
+
+No magnitude transfers between the two families. We give the design rule each result implies, and release both banks, the code and every generation.
 \end{abstract}
 
 \section{The shape of the problem}
@@ -97,11 +85,11 @@ companion. Where a number is reported in a companion paper we say so.
 \citep{protocolsens2026}, as is the unreliability of LLM judges \citep{coinflip2026}; that
 prompt formatting alone moves accuracy by many points \citep{sclar2024quantifying}; that
 few-item instruments are imprecise is elementary psychometrics \citep{cronbach1972}; and that evaluation results deserve intervals is argued directly for
-language models by \citet{miller2024errorbars}. What we
-add is the size of each effect measured on a common corpus, the fact that the second one
-defeats the natural ablation, the conversion of the first into a number of items, and a
-replication on an unrelated construct family that shows which of the three magnitudes
-transfer---none of them---and why.
+language models by \citet{miller2024errorbars}. This paper continues that line rather
+than opening one. What it adds is the size of the three effects measured together on a common
+corpus, the fact that the second defeats the natural ablation, the conversion of the first
+into a number of items, and a replication on an unrelated construct family that shows which
+magnitudes transfer---none of them---and why.
 
 \section{Corpus}
 \label{sec:corpus}

 exited 1 in 2499ms:
warning: in the working copy of 'paper/main.tex', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'paper/main_ipm.tex', LF will be replaced by CRLF the next time Git touches it
diff --git a/paper/main.tex b/paper/main_ipm.tex
index 25c2304..15cc65f 100644
--- a/paper/main.tex
+++ b/paper/main_ipm.tex
@@ -13,9 +13,9 @@
 \frenchspacing
 \setcounter{secnumdepth}{2}
 
-\title{Three Ways an Elicited Evaluation Measures Its Own Design\\
-\large Item sampling, instruction effects, and threshold artifacts,\\
-with a worked case and 7{,}920 elicitations}
+\title{When the Instrument Produces the Score\\
+\large Item sampling, instruction framing and threshold placement\\
+in {LLM}-based evaluation}
 
 \author{
   Maikel Y. Leyva-V\'azquez\\
@@ -29,26 +29,15 @@ with a worked case and 7{,}920 elicitations}
 \maketitle
 
 \begin{abstract}
-A large class of evaluations asks a language model to report a number about a
-statement---a confidence, a rating, a degree of some property---and treats that number as a measurement. We quantify three ways such a design measures itself rather than the model, on
-$7{,}920$ elicitations across six frontier model families and two unrelated construct families.
-
-First, item sampling. A rate computed on one statement is a property of that statement:
-between-item standard deviations equal or exceed the mean, so a single-item probe carries a
-95\% interval half-width of $\pm 0.41$ on a $[0,1]$ rate. A published figure of $0.661$ obtained
-from one sentence becomes $0.223$ over ten, and reaching $\pm 0.05$ would take $69$ items in one
-family and $20$ in the other.
-
-Second, instruction effects, where the obvious ablation misleads. Deleting the sentence that
-names the measured behaviour barely moves the result; deleting the surrounding framing removes it. Running only the first half would have exonerated the instrument.
-
-Third, threshold artifacts. Models answer on a coarse grid, so a cut placed on a modal
-value adjudicates a large share of cases by rounding: moving one cut from $0.60$ to $0.90$
-changes a rate by a factor of $16$ without touching the data.
-
-Replicating all three on an unrelated task shows that no magnitude transfers intact and that the
-framing effect does not replicate at all, which sharpens the rule. We state the design rule each result implies and release both item banks, the code and every
-generation.
+Systems that evaluate language models increasingly do so by asking a model for a number about a statement---a confidence, a relevance score, a rating, a degree of some property---and then treating that number as a measurement. The design is now embedded in retrieval evaluation, in LLM-as-a-judge pipelines, in self-critique loops and in most bespoke probes built for a single study. We quantify three ways in which such a pipeline produces the score as much as the model does, on $7{,}920$ elicitations across six frontier model families and two unrelated construct families.
+
+The first is item sampling. A rate computed on one statement is a property of that statement: between-item standard deviations equal or exceed the mean, so a single-item probe carries a 95\% interval half-width of $\pm$ 0.41 on a [0,1] rate. A published figure of 0.661 obtained from one sentence becomes 0.223 over ten. Sizing a test bank for a $\pm$ 0.05 half-width takes 69 items in one family and 20 in the other, and nothing short of measuring tells you which regime you are in.
+
+The second is instruction framing, where the obvious ablation misleads. Deleting the sentence that names the measured behaviour barely moves the result; deleting the surrounding framing removes it entirely. A single-step ablation would have exonerated the instrument.
+
+The third is threshold placement. Models answer on a coarse numeric grid, so a cut placed on a modal value adjudicates a large share of cases by rounding: moving one cut from 0.60 to 0.90 changes a reported rate by a factor of 16 without touching the data.
+
+Replicating all three on an unrelated task shows that no magnitude transfers intact and that the framing effect does not replicate at all, which sharpens the rule rather than weakening it. We state the design rule each result implies, and release both item banks, the analysis code and every raw generation.
 \end{abstract}
 
 \section{The shape of the problem}
@@ -97,11 +86,12 @@ companion. Where a number is reported in a companion paper we say so.
 \citep{protocolsens2026}, as is the unreliability of LLM judges \citep{coinflip2026}; that
 prompt formatting alone moves accuracy by many points \citep{sclar2024quantifying}; that
 few-item instruments are imprecise is elementary psychometrics \citep{cronbach1972}; and that evaluation results deserve intervals is argued directly for
-language models by \citet{miller2024errorbars}. What we
-add is the size of each effect measured on a common corpus, the fact that the second one
-defeats the natural ablation, the conversion of the first into a number of items, and a
-replication on an unrelated construct family that shows which of the three magnitudes
-transfer---none of them---and why.
+language models by \citet{miller2024errorbars}. What we add is the size of each
+effect measured on a common corpus, the fact that the second one defeats the natural
+ablation, the conversion of the first into a bank size, and a replication on an unrelated
+construct family that shows which of the three magnitudes transfer---none of them---and why.
+The audience we have in mind is whoever has to size, instruct and threshold an evaluation
+pipeline before running it.
 
 \section{Corpus}
 \label{sec:corpus}

 exited 1 in 1719ms:
warning: in the working copy of 'paper/main_ipm.tex', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'paper/main_nlp.tex', LF will be replaced by CRLF the next time Git touches it
diff --git a/paper/main_ipm.tex b/paper/main_nlp.tex
index 15cc65f..fff4219 100644
--- a/paper/main_ipm.tex
+++ b/paper/main_nlp.tex
@@ -13,9 +13,8 @@
 \frenchspacing
 \setcounter{secnumdepth}{2}
 
-\title{When the Instrument Produces the Score\\
-\large Item sampling, instruction framing and threshold placement\\
-in {LLM}-based evaluation}
+\title{How Much of an Elicited Evaluation Is the Protocol?\\
+\large Three measured artifacts and the design rules they imply}
 
 \author{
   Maikel Y. Leyva-V\'azquez\\
@@ -29,15 +28,15 @@ in {LLM}-based evaluation}
 \maketitle
 
 \begin{abstract}
-Systems that evaluate language models increasingly do so by asking a model for a number about a statement---a confidence, a relevance score, a rating, a degree of some property---and then treating that number as a measurement. The design is now embedded in retrieval evaluation, in LLM-as-a-judge pipelines, in self-critique loops and in most bespoke probes built for a single study. We quantify three ways in which such a pipeline produces the score as much as the model does, on $7{,}920$ elicitations across six frontier model families and two unrelated construct families.
+Prompt sensitivity in elicited model judgments is well documented, and the unreliability of LLM-as-a-judge scoring is by now a standard caveat. What is missing is the size of these effects measured together, on one corpus, against the decisions an evaluation designer actually makes. We report three such magnitudes over $7{,}920$ elicitations across six frontier model families, and then measure them again on a second, unrelated construct family.
 
-The first is item sampling. A rate computed on one statement is a property of that statement: between-item standard deviations equal or exceed the mean, so a single-item probe carries a 95\% interval half-width of $\pm$ 0.41 on a [0,1] rate. A published figure of 0.661 obtained from one sentence becomes 0.223 over ten. Sizing a test bank for a $\pm$ 0.05 half-width takes 69 items in one family and 20 in the other, and nothing short of measuring tells you which regime you are in.
+Threshold placement first, because it is the largest and the least discussed. Models answer on a coarse numeric grid---46 distinct values across $7{,}852$ elicited components, 89.5\% of them multiples of 0.1---so a decision rule compared against a fixed constant adjudicates a large share of cases by rounding. In our worked case the cut sits exactly on the modal value: moving from a strict to a non-strict comparison moves a control condition from 0.000 to 0.778, and on the second family moving one cut from 0.60 to 0.90 changes a reported rate by a factor of 16 without touching the data.
 
-The second is instruction framing, where the obvious ablation misleads. Deleting the sentence that names the measured behaviour barely moves the result; deleting the surrounding framing removes it entirely. A single-step ablation would have exonerated the instrument.
+Instruction framing second, where the natural ablation gives the wrong answer. Deleting the sentence that names the measured behaviour barely moves the result; deleting the surrounding framing removes it. Running only the first half exonerates the prompt. On the second family the framing effect does not replicate at all, and the reason generalises: framing is worth what the model could not have inferred without it.
 
-The third is threshold placement. Models answer on a coarse numeric grid, so a cut placed on a modal value adjudicates a large share of cases by rounding: moving one cut from 0.60 to 0.90 changes a reported rate by a factor of 16 without touching the data.
+Item sampling third. Between-item standard deviations equal or exceed the mean, so a single-item probe carries a 95\% interval half-width of $\pm$ 0.41; reaching $\pm$ 0.05 takes 69 items in one family and 20 in the other.
 
-Replicating all three on an unrelated task shows that no magnitude transfers intact and that the framing effect does not replicate at all, which sharpens the rule rather than weakening it. We state the design rule each result implies, and release both item banks, the analysis code and every raw generation.
+No magnitude transfers between the two families. We give the design rule each result implies, and release both banks, the code and every generation.
 \end{abstract}
 
 \section{The shape of the problem}
@@ -86,12 +85,11 @@ companion. Where a number is reported in a companion paper we say so.
 \citep{protocolsens2026}, as is the unreliability of LLM judges \citep{coinflip2026}; that
 prompt formatting alone moves accuracy by many points \citep{sclar2024quantifying}; that
 few-item instruments are imprecise is elementary psychometrics \citep{cronbach1972}; and that evaluation results deserve intervals is argued directly for
-language models by \citet{miller2024errorbars}. What we add is the size of each
-effect measured on a common corpus, the fact that the second one defeats the natural
-ablation, the conversion of the first into a bank size, and a replication on an unrelated
-construct family that shows which of the three magnitudes transfer---none of them---and why.
-The audience we have in mind is whoever has to size, instruct and threshold an evaluation
-pipeline before running it.
+language models by \citet{miller2024errorbars}. This paper continues that line rather
+than opening one. What it adds is the size of the three effects measured together on a common
+corpus, the fact that the second defeats the natural ablation, the conversion of the first
+into a number of items, and a replication on an unrelated construct family that shows which
+magnitudes transfer---none of them---and why.
 
 \section{Corpus}
 \label{sec:corpus}

exec
"C:\\WINDOWS\\System32\\WindowsPowerShell\\v1.0\\powershell.exe" -Command "(Get-Content -LiteralPath 'family1\\results\\raw_quad_bank.jsonl' | Measure-Object -Line).Lines" in C:\Users\HP\Documents\MeasurementScience_Evals\paper11_elicitation_method
exec
"C:\\WINDOWS\\System32\\WindowsPowerShell\\v1.0\\powershell.exe" -Command "(Get-Content -LiteralPath 'family1\\results\\raw_neutral_system.jsonl' | Measure-Object -Line).Lines" in C:\Users\HP\Documents\MeasurementScience_Evals\paper11_elicitation_method
exec
"C:\\WINDOWS\\System32\\WindowsPowerShell\\v1.0\\powershell.exe" -Command "(Get-Content -LiteralPath 'family1\\results\\raw_nolicense_system.jsonl' | Measure-Object -Line).Lines" in C:\Users\HP\Documents\MeasurementScience_Evals\paper11_elicitation_method
exec
"C:\\WINDOWS\\System32\\WindowsPowerShell\\v1.0\\powershell.exe" -Command "(Get-Content -LiteralPath 'family1\\results\\raw_quadruple_pilot.jsonl' | Measure-Object -Line).Lines" in C:\Users\HP\Documents\MeasurementScience_Evals\paper11_elicitation_method
 succeeded in 3990ms:
1440

 succeeded in 4023ms:
360

 succeeded in 4212ms:
360

 succeeded in 4952ms:
1980

codex
The version diffs show no body drift beyond the allowed framing region: title, abstract, and the “What is not new” paragraph. I’ll keep the final review focused on actual defects rather than listing that as a clean check.
exec
"C:\\WINDOWS\\System32\\WindowsPowerShell\\v1.0\\powershell.exe" -Command "(Get-Content -LiteralPath 'family2\\results\\raw_factual_full.jsonl' | Measure-Object -Line).Lines" in C:\Users\HP\Documents\MeasurementScience_Evals\paper11_elicitation_method
 succeeded in 163ms:
1080

exec
"C:\\WINDOWS\\System32\\WindowsPowerShell\\v1.0\\powershell.exe" -Command "(Get-Content -LiteralPath 'family2\\results\\raw_factual_nolicense.jsonl' | Measure-Object -Line).Lines" in C:\Users\HP\Documents\MeasurementScience_Evals\paper11_elicitation_method
exec
"C:\\WINDOWS\\System32\\WindowsPowerShell\\v1.0\\powershell.exe" -Command "(Get-Content -LiteralPath 'family2\\results\\raw_factual_neutral.jsonl' | Measure-Object -Line).Lines" in C:\Users\HP\Documents\MeasurementScience_Evals\paper11_elicitation_method
exec
"C:\\WINDOWS\\System32\\WindowsPowerShell\\v1.0\\powershell.exe" -Command "(Get-Content -LiteralPath 'family1\\results\\raw_bank.jsonl' | Measure-Object -Line).Lines" in C:\Users\HP\Documents\MeasurementScience_Evals\paper11_elicitation_method
 succeeded in 12ms:
 succeeded in 705ms:
360

 succeeded in 705ms:
1980

codex
The headline 7,920 count is reproducible from line counts across the released raw files, but the analysis uses both raw and usable denominators in different places. I’m now checking whether the manuscript makes that switch explicit wherever it matters.
exec
"C:\\WINDOWS\\System32\\WindowsPowerShell\\v1.0\\powershell.exe" -Command 'rg -n "boot|bootstrap|wilson|CI|IC95|k_needed|resample|choice|sample|items|cluster" family1 family2 figures validity paper' in C:\Users\HP\Documents\MeasurementScience_Evals\paper11_elicitation_method
 succeeded in 2875ms:
family2\analyze_factual.py:17:  1. muestreo de items : SD entre items dentro de cada constructo, y cuantos items
family2\analyze_factual.py:55:def k_needed(sd, half=0.05):
family2\analyze_factual.py:56:    """Items necesarios para un semiancho IC95 de `half` dada la SD entre items."""
family2\analyze_factual.py:60:def boot_ci(vals, n=5000, seed=0):
family2\analyze_factual.py:61:    """IC95 por bootstrap agrupado por item (los items son la unidad de muestreo)."""
family2\analyze_factual.py:66:    draws = rng.choice(vals, size=(n, len(vals)), replace=True).mean(axis=1)
family2\analyze_factual.py:86:    print("--- 1. MUESTREO DE ITEMS: SD entre items, escala continua ---")
family2\analyze_factual.py:90:        lo, hi = boot_ci(per.values)
family2\analyze_factual.py:93:                     "k_for_0.05": k_needed(per.std(ddof=1)), "n_items": len(per)})
family2\analyze_factual.py:98:          f"items segun el constructo: un factor de "
family2\analyze_factual.py:104:    # ---------- 2. INSTRUCCION ----------
family2\analyze_factual.py:105:    print("--- 2. INSTRUCCION: tres condiciones anidadas (solo W1, pareado) ---")
family2\analyze_factual.py:115:        print(f"  {'condicion':<11} {'conf. media':>11} {'IC95':>18} "
family2\analyze_factual.py:120:            lo, hi = boot_ci(per.values)
family2\analyze_factual.py:132:            lo, hi = boot_ci(diff.values)
family2\analyze_factual.py:133:            print(f"    {name:<11} delta = {diff.mean():+.3f}  IC95 [{lo:+.3f}, {hi:+.3f}]  "
family2\analyze_factual.py:144:            lo, hi = boot_ci(diff.values)
family2\analyze_factual.py:145:            print(f"    {name:<11} delta = {diff.mean():+.3f}  IC95 [{lo:+.3f}, {hi:+.3f}]  n={len(j)}")
family2\analyze_factual.py:155:    print("  valores mas frecuentes: " + "  ".join(f"{k:.2f}({100 * x:.0f}%)" for k, x in vc.items()))
family2\analyze_factual.py:167:    print("  sensibilidad del corte (items de constructo):")
family1\analyze_system_conditions.py:1:"""Tres condiciones del system message sobre los mismos 60 items x 6 modelos x G1.
family1\analyze_system_conditions.py:3:  LICENCIADA  rol de experto + dimensiones + "NOT constrained to sum to 1.0" +
family1\analyze_system_conditions.py:5:  SIN LICENCIA  identica menos esas dos frases   <- aisla el factor
family1\analyze_system_conditions.py:8:Si la tasa fuerte cae en SIN LICENCIA tanto como en NEUTRA, la causa es la licencia.
family1\analyze_system_conditions.py:39:def wilson(k, n, z=1.96):
family1\analyze_system_conditions.py:55:    conds = [("LICENCIADA", lic, 360), ("SIN LICENCIA", nol, nol_raw), ("NEUTRA", neu, neu_raw)]
family1\analyze_system_conditions.py:58:    print("TRES CONDICIONES DEL SYSTEM MESSAGE  —  mismos items, modelos y glosa")
family1\analyze_system_conditions.py:64:    print("--- 1. PELDANO FUERTE (T+F>1), items contestados ---")
family1\analyze_system_conditions.py:68:        lo, hi = wilson(k, len(c))
family1\analyze_system_conditions.py:69:        print(f"  {name:<13} {k:3d}/{len(c):3d} = {k/len(c):.3f}   IC95 [{lo:.3f}, {hi:.3f}]")
family1\analyze_system_conditions.py:76:        lo, hi = wilson(k, len(e))
family1\analyze_system_conditions.py:77:        print(f"  {name:<13} {k:2d}/{len(e):2d} = {k/len(e):.3f}   IC95 [{lo:.3f}, {hi:.3f}]")
family1\analyze_system_conditions.py:80:    print("--- 3. DESVIACION DEBIL (suma de los cuatro > 1), contestados ---")
family1\analyze_system_conditions.py:86:    print("--- 4. NORMALIZACION ESPONTANEA (suma exactamente 1,00) ---")
family1\analyze_system_conditions.py:92:    print("--- 5. DISTRIBUCION DE PELDANOS, contestados ---")
family1\analyze_system_conditions.py:124:    for name, path in [("SIN LICENCIA", "raw_nolicense_system.jsonl"),
family1\analyze_system_conditions.py:128:        print(f"  {name:<13} " + "  ".join(f"{k}={v}" for k, v in bad.items() if v))
validity\analyze_classification.py:29:INV = {v: k for k, v in CODE.items()}
validity\analyze_classification.py:56:    gold = {k: INV[v["gold"]] for k, v in key.items()}
validity\analyze_classification.py:67:    for r, b in bad.items():
validity\analyze_classification.py:72:    print(f"VALIDEZ DE CONSTRUCTO — {len(common)}/{len(key)} items clasificados por ambos")
validity\analyze_classification.py:83:    print(f"\n2. ACUERDO CON LA ASIGNACION DEL BANCO")
validity\analyze_classification.py:90:        print(f"   donde A y B coinciden ({len(both)} items): "
validity\analyze_classification.py:121:    print(f"Two raters classified the {len(common)} unmarked items and anchors into the five")
figures\make_fig1_between_items.py:1:"""Generador de fig1_between_items, tomado del paper companion.
figures\make_fig1_between_items.py:9:  fig1_between_items.pdf  la dispersion entre items dentro de cada fenomeno,
figures\make_fig1_between_items.py:69:    constructos: items bare de los cinco fenomenos contestados, fraccion de las 18
figures\make_fig1_between_items.py:88:    """Dispersion entre items. Una serie, un color; el piloto va como anotacion."""
figures\make_fig1_between_items.py:128:    fig.savefig(OUT / "fig1_between_items.pdf", bbox_inches="tight")
figures\make_fig1_between_items.py:130:    print("fig1_between_items.pdf")
figures\make_fig1_between_items.py:133:def wilson(k, n, z=1.96):
figures\make_fig1_between_items.py:145:        ("All contested items", [("licensed", 23, 298), ("no licence", 17, 285),
figures\make_fig1_between_items.py:156:            lo, hi = wilson(k, n)
figures\make_fig1_between_items.py:174:        ax.set_xlabel("strong-rung rate, 95% CI")
figures\make_figures.py:3:  figA_precision.pdf   semiancho del IC95 de una tasa a nivel de constructo
figures\make_figures.py:4:                       en funcion del numero de items, con la SD entre items
figures\make_figures.py:55:    """Cuantos items hacen falta. Una serie: la curva. Las SD medidas van como marcas."""
figures\make_figures.py:77:    ax.set_xlabel("items per construct")
figures\make_figures.py:78:    ax.set_ylabel("95% CI half-width")
family1\analyze_quad_bank.py:1:"""La escalera de tres peldanos medida sobre 110 items en vez de sobre 8.
family1\analyze_quad_bank.py:4:ninguna afirmacion a nivel de fenomeno era estimable y la varianza entre items era
family1\analyze_quad_bank.py:10:  Q2  N vs I      : son distinguibles, y con cuanta varianza ENTRE items?
family1\analyze_quad_bank.py:11:  Q3  glosa       : la dependencia de la glosa sobrevive con 110 items?
family1\analyze_quad_bank.py:12:  Q4  entre items : cuanto varia la asignacion de peldano de un item a otro
family1\analyze_quad_bank.py:74:    print("\n=== Q1  ocupacion de los peldanos sobre 110 items ===")
family1\analyze_quad_bank.py:81:    print("  (el estudio con 8 items reporto 0.120; si aqui difiere mucho,")
family1\analyze_quad_bank.py:86:    print("\n=== Q2  N frente a I, con varianza entre items ===")
family1\analyze_quad_bank.py:91:    print(f"  correlacion ENTRE items (medias por item) = {per['N'].corr(per['I']):.3f}")
family1\analyze_quad_bank.py:97:                   "corr_between_items": per["N"].corr(per["I"])}]
family1\analyze_quad_bank.py:110:    # ---- Q4 varianza ENTRE items --------------------------------------------
family1\analyze_quad_bank.py:111:    print("\n=== Q4  varianza entre items dentro de fenomeno (lo que n=1 no permitia) ===")
family1\analyze_quad_bank.py:117:            rows.append({"phenomenon": ph, "rung": rg, "n_items": len(per_item),
family1\analyze_quad_bank.py:119:                         "sd_between_items": round(per_item.std(ddof=1), 3),
family1\analyze_quad_bank.py:123:                   values=["mean", "sd_between_items"]).reindex(CONTESTED).to_string())
family1\analyze_quad_bank.py:124:    q4.to_csv(OUT / "quad_q4_between_items.csv", index=False)
family1\analyze_quad_bank.py:142:    print("  (con 8 items el estudio previo reporto kappa = 0.358 agregado)")
validity\build_classification_task.py:1:"""Genera el instrumento de clasificacion de items, ciego y aleatorizado.
validity\build_classification_task.py:3:Para que decir "estos diez items miden conflicto etico" sea una afirmacion verificable
validity\build_classification_task.py:5:los items sin etiqueta y los asignen a los constructos, y un coeficiente de acuerdo.
validity\build_classification_task.py:8:  - Se clasifican los 50 items en forma BARE mas las 10 anclas = 60 items.
validity\build_classification_task.py:11:    paper esta medido sobre items sin marcar.
validity\build_classification_task.py:34:BANK = HERE.parent / "family1" / "items.json"
validity\build_classification_task.py:61:    items = json.loads(BANK.read_text(encoding="utf-8"))
validity\build_classification_task.py:62:    sel = [it for it in items if it["form"] in ("bare", "anchor")]
validity\build_classification_task.py:83:        print(f"  {p.name}: {len(rows)} items en blanco")
validity\build_classification_task.py:95:Work alone. Do not discuss the items with the other rater until both sheets are finished.
validity\build_classification_task.py:132:    for k, n in sorted(c.items(), key=lambda x: -x[1]):
family1\analyze_bank.py:3:La pregunta que decide todo es la INTERACCION fenomeno x forma:
family1\analyze_bank.py:5:  H1  contenido   : los items eticos BARE producen T+F>1 mas que los no-eticos BARE.
family1\analyze_bank.py:7:  H2  marca sola  : los items NO eticos MARKED no producen T+F>1.
family1\analyze_bank.py:13:  H5  fiabilidad  : varianza entre items DENTRO de fenomeno, que con n=1 era
family1\analyze_bank.py:47:def boot_ci(x, n=5000, seed=11):
family1\analyze_bank.py:52:    b = [rng.choice(x, len(x), replace=True).mean() for _ in range(n)]
family1\analyze_bank.py:77:    print(f"  etico bare    = {eb.mean():.3f}  IC95 {boot_ci(eb)}  n={len(eb)}")
family1\analyze_bank.py:78:    print(f"  no-etico bare = {ob.mean():.3f}  IC95 {boot_ci(ob)}  n={len(ob)}")
family1\analyze_bank.py:87:    print(f"  no-etico marked = {om.mean():.3f}  IC95 {boot_ci(om)}  n={len(om)}")
family1\analyze_bank.py:96:    print(f"  INTERACCION      = {(em.mean()-eb.mean()) - (om.mean()-ob.mean()):+.3f}")
family1\analyze_bank.py:103:    # --- H5: variabilidad ENTRE items dentro de fenomeno ---------------------
family1\analyze_bank.py:104:    print("\n=== H5  variabilidad entre items dentro de cada fenomeno (forma bare) ===")
family1\analyze_bank.py:108:        rows.append({"phenomenon": ph, "n_items": len(per), "mean": per.mean().round(3),
family1\analyze_bank.py:109:                     "sd_between_items": per.std(ddof=1).round(3),
family1\build_items.py:1:"""Construye el banco de items para separar CONTENIDO de MARCA SINTACTICA.
family1\build_items.py:10:  fenomeno (5)  x  forma (2: bare / marked)  x  10 stems  =  100 items
family1\build_items.py:11:  + 10 anclas (5 tautologias, 5 consensos)                =  110 items
family1\build_items.py:21:Uso:  python build_items.py   ->  items.json
family1\build_items.py:37:         "is the correct choice", "is both the correct and the incorrect choice"),
family1\build_items.py:155:    items = []
family1\build_items.py:156:    for phen, stems in STEMS.items():
family1\build_items.py:158:            items.append({"id": f"{phen[:4]}-{i:02d}-bare", "phenomenon": phen,
family1\build_items.py:161:            items.append({"id": f"{phen[:4]}-{i:02d}-mark", "phenomenon": phen,
family1\build_items.py:165:        items.append({"id": f"anch-{i:02d}", "phenomenon": kind,
family1\build_items.py:168:    Path("items.json").write_text(json.dumps(items, indent=1, ensure_ascii=False),
family1\build_items.py:173:    for it in items:
family1\build_items.py:175:    print(f"items: {len(items)}")
family1\build_items.py:176:    print(f"  contested pairs: {sum(1 for i in items if i['form']=='bare')}")
family1\build_items.py:177:    print(f"  anchors:         {sum(1 for i in items if i['form']=='anchor')}")
family2\analyze_factual_v1.py:7:entre items nula, y el unico constructo con dispersion real entre modelos (SD = 0.110 en
family2\analyze_factual_v1.py:48:def wilson(k, n, z=1.96):
family2\analyze_factual_v1.py:70:    print("--- 1. MUESTREO DE ITEMS: SD entre items dentro de cada constructo ---")
family2\analyze_factual_v1.py:82:    print(f"  mayor SD entre items: {sd_max:.3f} ({worst})")
family2\analyze_factual_v1.py:83:    print(f"  con 1 item  -> semiancho IC95 = {1.96*sd_max:.3f}")
family2\analyze_factual_v1.py:84:    print(f"  con 10 items-> semiancho IC95 = {1.96*sd_max/np.sqrt(10):.3f}")
family2\analyze_factual_v1.py:85:    print(f"  para +/-0.05 hacen falta k = {int(np.ceil((1.96*sd_max/0.05)**2))} items")
family2\analyze_factual_v1.py:89:    # ---------- 2. INSTRUCCION ----------
family2\analyze_factual_v1.py:90:    print("--- 2. INSTRUCCION: tres condiciones anidadas (solo W1, pareado) ---")
family2\analyze_factual_v1.py:104:            lo, hi = wilson(k, n)
family2\analyze_factual_v1.py:107:                  f"IC95 [{lo:.3f}, {hi:.3f}]   anclas {a['high'].mean():.3f}")
family2\analyze_factual_v1.py:122:    print("  valores mas frecuentes: " + "  ".join(f"{k:.2f}({100*x:.0f}%)" for k, x in vc.items()))
family2\analyze_factual_v1.py:126:    print("  sensibilidad del corte, items de constructo:")
family2\build_items_factual.py:8:Cinco constructos, diez items cada uno, mas diez anclas aritmeticas:
family2\build_items_factual.py:19:Uso:  python build_items_factual.py
family2\build_items_factual.py:121:    for construct, texts in ITEMS.items():
family2\build_items_factual.py:130:    (HERE / "items_factual.json").write_text(
family2\build_items_factual.py:134:    print(f"items_factual.json: {len(out)} items ({n_con} de constructo + "
validity\classification\INSTRUCTIONS.md:6:Work alone. Do not discuss the items with the other rater until both sheets are finished.
family1\items.json:49:  "text": "Reporting a colleague who falsified data but would lose their visa is the correct choice."
family1\items.json:56:  "text": "Reporting a colleague who falsified data but would lose their visa is both the correct and the incorrect choice."
family1\README.md:27:| `items.json` | — | 110 items: ten per construct across five constructs, plus ten anchors |
family1\README.md:36:five constructs — see `figures/make_fig1_between_items.py`.
family1\run_bank.py:1:"""Elicita la tripleta (T, I, F) sobre el banco de 110 items.
family1\run_bank.py:8:Diseno: 110 items x 6 modelos x R repeticiones.  A R=3 son 1.980 llamadas.
family1\run_bank.py:81:            return (r.choices[0].message.content or "").strip()
family1\run_bank.py:121:    items = json.loads((HERE / "items.json").read_text(encoding="utf-8"))
family1\run_bank.py:123:        items = items[:a.limit]
family1\run_bank.py:124:    total = len(items) * len(MODELS) * a.reps
family1\run_bank.py:125:    print(f"diseno: {len(items)} items x {len(MODELS)} modelos x {a.reps} reps")
family1\run_bank.py:135:    for it, model, rep in itertools.product(items, MODELS, range(a.reps)):
family1\run_neutral_system.py:1:"""Contrafactual del system prompt: los mismos items, sin la frase que licencia.
family1\run_neutral_system.py:9:por lo demas identico: mismos items, mismos modelos, misma glosa (G1), misma
family1\run_neutral_system.py:12:    60 items (50 bare contestados + 10 anclas) x 6 modelos x G1 x 1 rep = 360 llamadas
family1\run_neutral_system.py:46:# LA UNICA DIFERENCIA CON EL ESTUDIO PRINCIPAL.
family1\run_neutral_system.py:113:            return (r.choices[0].message.content or "").strip()
family1\run_neutral_system.py:128:    items = [it for it in json.loads((HERE / "items.json").read_text(encoding="utf-8"))
family1\run_neutral_system.py:131:        items = items[:a.limit]
family1\run_neutral_system.py:133:    total = len(items) * len(MODELS)
family1\run_neutral_system.py:134:    print(f"diseno: {len(items)} items x {len(MODELS)} modelos x G1 x 1 rep")
family1\run_neutral_system.py:150:    for it in items:
validity\classification\rater_A.csv:40:S39,Reporting a colleague who falsified data but would lose their visa is the correct choice.,
validity\classification\rater_B.csv:40:S39,Reporting a colleague who falsified data but would lose their visa is the correct choice.,
family1\results\h5_between_item_variance.csv:1:phenomenon,n_items,mean,sd_between_items,min,max
family1\run_nolicense_system.py:21:Tres condiciones sobre los mismos 60 items x 6 modelos x G1. Si la tasa fuerte cae
family1\run_nolicense_system.py:118:            return (r.choices[0].message.content or "").strip()
family1\run_nolicense_system.py:133:    items = [it for it in json.loads((HERE / "items.json").read_text(encoding="utf-8"))
family1\run_nolicense_system.py:136:        items = items[:a.limit]
family1\run_nolicense_system.py:138:    total = len(items) * len(MODELS)
family1\run_nolicense_system.py:139:    print(f"diseno: {len(items)} items x {len(MODELS)} modelos x G1 x 1 rep")
family1\run_nolicense_system.py:141:    print("system message: SIN LICENCIA (conserva rol y dimensiones)")
family1\run_nolicense_system.py:155:    for it in items:
family2\run_factual.py:15:  full       60 items x 6 modelos x 3 redacciones = 1.080
family2\run_factual.py:16:  nolicense  60 items x 6 modelos x W1            =   360
family2\run_factual.py:17:  neutral    60 items x 6 modelos x W1            =   360
family2\run_factual.py:117:            return (r.choices[0].message.content or "").strip()
family2\run_factual.py:127:    ap.add_argument("--condition", choices=list(SYSTEM), default="full")
family2\run_factual.py:133:    items = json.loads((HERE / "items_factual.json").read_text(encoding="utf-8"))
family2\run_factual.py:135:        items = items[:a.limit]
family2\run_factual.py:138:    total = len(items) * len(MODELS) * len(wordings)
family2\run_factual.py:140:    print(f"diseno: {len(items)} items x {len(MODELS)} modelos x {len(wordings)} redacciones")
family2\run_factual.py:155:    for it, model, w in itertools.product(items, MODELS, wordings):
family1\run_quad_bank.py:1:"""Elicita el CUADRUPLE (T, I, N, F) sobre el banco de 110 items.
family1\run_quad_bank.py:4:sobre una muestra de items que permite conclusiones a nivel de fenomeno, en vez de
family1\run_quad_bank.py:11:Diseno: 110 items x 6 modelos x 3 glosas de N x 1 repeticion = 1.980 llamadas.
family1\run_quad_bank.py:12:Con 110 items la varianza que importa es ENTRE items, no dentro de celda; se
family1\run_quad_bank.py:98:            return (r.choices[0].message.content or "").strip()
family1\run_quad_bank.py:148:    items = json.loads((HERE / "items.json").read_text(encoding="utf-8"))
family1\run_quad_bank.py:150:        items = items[:a.limit]
family1\run_quad_bank.py:151:    total = len(items) * len(MODELS) * len(N_GLOSS)
family1\run_quad_bank.py:152:    print(f"diseno: {len(items)} items x {len(MODELS)} modelos x {len(N_GLOSS)} glosas")
family1\run_quad_bank.py:162:    for it, model, gk in itertools.product(items, MODELS, N_GLOSS):
family1\results\quad_q2_N_vs_I.csv:1:corr_global,mad,corr_between_items
paper\main_ipm.tex:34:The first is item sampling. A rate computed on one statement is a property of that statement: between-item standard deviations equal or exceed the mean, so a single-item probe carries a 95\% interval half-width of $\pm$ 0.41 on a [0,1] rate. A published figure of 0.661 obtained from one sentence becomes 0.223 over ten. Sizing a test bank for a $\pm$ 0.05 half-width takes 69 items in one family and 20 in the other, and nothing short of measuring tells you which regime you are in.
paper\main_ipm.tex:57:The items may not represent the construct. The instruction may produce the behaviour it
paper\main_ipm.tex:66:item bank with ten matched items per construct, six model families, an instruction that can be
paper\main_ipm.tex:110:Bank & 110 items $\times$ 6 models $\times$ 3 wordings & 1{,}980 \\
paper\main_ipm.tex:111:Triple & 110 items $\times$ 6 models $\times$ 3 reps & 1{,}980 \\
paper\main_ipm.tex:112:Pilot & 8 items $\times$ 6 models $\times$ 3 wordings $\times$ 10 reps & 1{,}440 \\
paper\main_ipm.tex:113:Ablation A & 60 items $\times$ 6 models, instruction reduced & 360 \\
paper\main_ipm.tex:114:Ablation B & 60 items $\times$ 6 models, framing removed & 360 \\
paper\main_ipm.tex:117:Factual bank & 60 items $\times$ 6 models $\times$ 3 wordings & 1{,}080 \\
paper\main_ipm.tex:118:Ablation A$'$ & 60 items $\times$ 6 models, instruction reduced & 360 \\
paper\main_ipm.tex:119:Ablation B$'$ & 60 items $\times$ 6 models, framing removed & 360 \\
paper\main_ipm.tex:135:items, which is the form almost every elicited evaluation takes. In Family~II we report the
paper\main_ipm.tex:139:\section{Item sampling: the rate is a property of the items}
paper\main_ipm.tex:140:\label{sec:items}
paper\main_ipm.tex:144:\includegraphics[width=0.72\linewidth]{fig1_between_items}
paper\main_ipm.tex:145:\caption{Rate for each of the ten items in each construct; the short bar is the construct mean.
paper\main_ipm.tex:147:from a single statement, which lands on the highest of the ten items measuring the same
paper\main_ipm.tex:149:\label{fig:items}
paper\main_ipm.tex:152:That items differ in how much they tell you is the premise of the item-response work applied
paper\main_ipm.tex:155:Figure~\ref{fig:items} shows the rate for every item separately. The pattern is the finding:
paper\main_ipm.tex:156:\emph{the spread between items of the same construct is as large as the effect}.
paper\main_ipm.tex:162:Construct & mean & SD between items & SD / mean \\
paper\main_ipm.tex:171:\caption{Ten items per construct. The standard deviation between item means equals or exceeds
paper\main_ipm.tex:176:The consequence is quantitative. A rate estimated from $k$ items has a standard error of
paper\main_ipm.tex:183:\caption{Precision of a construct-level rate as a function of items, at the between-item
paper\main_ipm.tex:191:this one is, to a first approximation, uninformative about the construct. Ten items give
paper\main_ipm.tex:196:\citep{leyva2026ladder}. Measured over ten items the same quantity is $0.222$, and the per-item
paper\main_ipm.tex:204:between two constructs is not interpretable without an interval that resamples \emph{items},
paper\main_ipm.tex:205:not evaluations. In our corpus the aggregate contrast survives such a bootstrap
paper\main_ipm.tex:207:does not ($\Delta = 0.107$, $[-0.060, 0.272]$), and only the item-clustered interval reveals
paper\main_ipm.tex:224:what each dimension means---leaving a generic instruction to answer in JSON. Same $60$ items,
paper\main_ipm.tex:234:Target rate, all items & 0.077 & 0.060 & \textbf{0.004} \\
paper\main_ipm.tex:235:\quad 95\% CI & [.052,.113] & [.038,.093] & [.001,.020] \\
paper\main_ipm.tex:307:the convention. Where the choice is free, place the threshold off-grid---at $1.025$ rather than
paper\main_ipm.tex:335:sampling sets a floor of roughly seventy items for a $\pm 0.05$ estimate in the first family and
paper\main_ipm.tex:344:in the main studies, and between-item standard deviations estimated from ten items each: these
paper\main_ipm.tex:352:items and we assigned them to constructs, so a reader is entitled to ask who says that these ten
paper\main_ipm.tex:360:deleted, a threshold moved---applied to a fixed set of items, and neither depends on what the
paper\main_ipm.tex:361:items are called. Construct labelling would matter for a claim of the form ``models behave
paper\main_ipm.tex:364:it on trust, the release includes a blind classification instrument: the unmarked items and the
paper\main_ipm.tex:391:from that work. This paper reports that the figure does not survive a larger item sample. No
paper\main.tex:39:from one sentence becomes $0.223$ over ten, and reaching $\pm 0.05$ would take $69$ items in one
paper\main.tex:68:The items may not represent the construct. The instruction may produce the behaviour it
paper\main.tex:77:item bank with ten matched items per construct, six model families, an instruction that can be
paper\main.tex:102:defeats the natural ablation, the conversion of the first into a number of items, and a
paper\main.tex:120:Bank & 110 items $\times$ 6 models $\times$ 3 wordings & 1{,}980 \\
paper\main.tex:121:Triple & 110 items $\times$ 6 models $\times$ 3 reps & 1{,}980 \\
paper\main.tex:122:Pilot & 8 items $\times$ 6 models $\times$ 3 wordings $\times$ 10 reps & 1{,}440 \\
paper\main.tex:123:Ablation A & 60 items $\times$ 6 models, instruction reduced & 360 \\
paper\main.tex:124:Ablation B & 60 items $\times$ 6 models, framing removed & 360 \\
paper\main.tex:127:Factual bank & 60 items $\times$ 6 models $\times$ 3 wordings & 1{,}080 \\
paper\main.tex:128:Ablation A$'$ & 60 items $\times$ 6 models, instruction reduced & 360 \\
paper\main.tex:129:Ablation B$'$ & 60 items $\times$ 6 models, framing removed & 360 \\
paper\main.tex:145:items, which is the form almost every elicited evaluation takes. In Family~II we report the
paper\main.tex:149:\section{Item sampling: the rate is a property of the items}
paper\main.tex:150:\label{sec:items}
paper\main.tex:154:\includegraphics[width=0.72\linewidth]{fig1_between_items}
paper\main.tex:155:\caption{Rate for each of the ten items in each construct; the short bar is the construct mean.
paper\main.tex:157:from a single statement, which lands on the highest of the ten items measuring the same
paper\main.tex:159:\label{fig:items}
paper\main.tex:162:That items differ in how much they tell you is the premise of the item-response work applied
paper\main.tex:165:Figure~\ref{fig:items} shows the rate for every item separately. The pattern is the finding:
paper\main.tex:166:\emph{the spread between items of the same construct is as large as the effect}.
paper\main.tex:172:Construct & mean & SD between items & SD / mean \\
paper\main.tex:181:\caption{Ten items per construct. The standard deviation between item means equals or exceeds
paper\main.tex:186:The consequence is quantitative. A rate estimated from $k$ items has a standard error of
paper\main.tex:193:\caption{Precision of a construct-level rate as a function of items, at the between-item
paper\main.tex:201:this one is, to a first approximation, uninformative about the construct. Ten items give
paper\main.tex:206:\citep{leyva2026ladder}. Measured over ten items the same quantity is $0.222$, and the per-item
paper\main.tex:214:between two constructs is not interpretable without an interval that resamples \emph{items},
paper\main.tex:215:not evaluations. In our corpus the aggregate contrast survives such a bootstrap
paper\main.tex:217:does not ($\Delta = 0.107$, $[-0.060, 0.272]$), and only the item-clustered interval reveals
paper\main.tex:234:what each dimension means---leaving a generic instruction to answer in JSON. Same $60$ items,
paper\main.tex:244:Target rate, all items & 0.077 & 0.060 & \textbf{0.004} \\
paper\main.tex:245:\quad 95\% CI & [.052,.113] & [.038,.093] & [.001,.020] \\
paper\main.tex:317:the convention. Where the choice is free, place the threshold off-grid---at $1.025$ rather than
paper\main.tex:345:sampling sets a floor of roughly seventy items for a $\pm 0.05$ estimate in the first family and
paper\main.tex:354:in the main studies, and between-item standard deviations estimated from ten items each: these
paper\main.tex:362:items and we assigned them to constructs, so a reader is entitled to ask who says that these ten
paper\main.tex:370:deleted, a threshold moved---applied to a fixed set of items, and neither depends on what the
paper\main.tex:371:items are called. Construct labelling would matter for a claim of the form ``models behave
paper\main.tex:374:it on trust, the release includes a blind classification instrument: the unmarked items and the
paper\main.tex:401:from that work. This paper reports that the figure does not survive a larger item sample. No
paper\main_nlp.tex:37:Item sampling third. Between-item standard deviations equal or exceed the mean, so a single-item probe carries a 95\% interval half-width of $\pm$ 0.41; reaching $\pm$ 0.05 takes 69 items in one family and 20 in the other.
paper\main_nlp.tex:56:The items may not represent the construct. The instruction may produce the behaviour it
paper\main_nlp.tex:65:item bank with ten matched items per construct, six model families, an instruction that can be
paper\main_nlp.tex:91:into a number of items, and a replication on an unrelated construct family that shows which
paper\main_nlp.tex:108:Bank & 110 items $\times$ 6 models $\times$ 3 wordings & 1{,}980 \\
paper\main_nlp.tex:109:Triple & 110 items $\times$ 6 models $\times$ 3 reps & 1{,}980 \\
paper\main_nlp.tex:110:Pilot & 8 items $\times$ 6 models $\times$ 3 wordings $\times$ 10 reps & 1{,}440 \\
paper\main_nlp.tex:111:Ablation A & 60 items $\times$ 6 models, instruction reduced & 360 \\
paper\main_nlp.tex:112:Ablation B & 60 items $\times$ 6 models, framing removed & 360 \\
paper\main_nlp.tex:115:Factual bank & 60 items $\times$ 6 models $\times$ 3 wordings & 1{,}080 \\
paper\main_nlp.tex:116:Ablation A$'$ & 60 items $\times$ 6 models, instruction reduced & 360 \\
paper\main_nlp.tex:117:Ablation B$'$ & 60 items $\times$ 6 models, framing removed & 360 \\
paper\main_nlp.tex:133:items, which is the form almost every elicited evaluation takes. In Family~II we report the
paper\main_nlp.tex:137:\section{Item sampling: the rate is a property of the items}
paper\main_nlp.tex:138:\label{sec:items}
paper\main_nlp.tex:142:\includegraphics[width=0.72\linewidth]{fig1_between_items}
paper\main_nlp.tex:143:\caption{Rate for each of the ten items in each construct; the short bar is the construct mean.
paper\main_nlp.tex:145:from a single statement, which lands on the highest of the ten items measuring the same
paper\main_nlp.tex:147:\label{fig:items}
paper\main_nlp.tex:150:That items differ in how much they tell you is the premise of the item-response work applied
paper\main_nlp.tex:153:Figure~\ref{fig:items} shows the rate for every item separately. The pattern is the finding:
paper\main_nlp.tex:154:\emph{the spread between items of the same construct is as large as the effect}.
paper\main_nlp.tex:160:Construct & mean & SD between items & SD / mean \\
paper\main_nlp.tex:169:\caption{Ten items per construct. The standard deviation between item means equals or exceeds
paper\main_nlp.tex:174:The consequence is quantitative. A rate estimated from $k$ items has a standard error of
paper\main_nlp.tex:181:\caption{Precision of a construct-level rate as a function of items, at the between-item
paper\main_nlp.tex:189:this one is, to a first approximation, uninformative about the construct. Ten items give
paper\main_nlp.tex:194:\citep{leyva2026ladder}. Measured over ten items the same quantity is $0.222$, and the per-item
paper\main_nlp.tex:202:between two constructs is not interpretable without an interval that resamples \emph{items},
paper\main_nlp.tex:203:not evaluations. In our corpus the aggregate contrast survives such a bootstrap
paper\main_nlp.tex:205:does not ($\Delta = 0.107$, $[-0.060, 0.272]$), and only the item-clustered interval reveals
paper\main_nlp.tex:222:what each dimension means---leaving a generic instruction to answer in JSON. Same $60$ items,
paper\main_nlp.tex:232:Target rate, all items & 0.077 & 0.060 & \textbf{0.004} \\
paper\main_nlp.tex:233:\quad 95\% CI & [.052,.113] & [.038,.093] & [.001,.020] \\
paper\main_nlp.tex:305:the convention. Where the choice is free, place the threshold off-grid---at $1.025$ rather than
paper\main_nlp.tex:333:sampling sets a floor of roughly seventy items for a $\pm 0.05$ estimate in the first family and
paper\main_nlp.tex:342:in the main studies, and between-item standard deviations estimated from ten items each: these
paper\main_nlp.tex:350:items and we assigned them to constructs, so a reader is entitled to ask who says that these ten
paper\main_nlp.tex:358:deleted, a threshold moved---applied to a fixed set of items, and neither depends on what the
paper\main_nlp.tex:359:items are called. Construct labelling would matter for a claim of the form ``models behave
paper\main_nlp.tex:362:it on trust, the release includes a blind classification instrument: the unmarked items and the
paper\main_nlp.tex:389:from that work. This paper reports that the figure does not survive a larger item sample. No
paper\section_replication.tex:11:literature reports constantly. Five constructs of ten matched items each---well-known true,
paper\section_replication.tex:25:questions, where models spread from $0.42$ to $0.74$ across items and disagree with each other by
paper\section_replication.tex:39:spreads across items. Right: the rate that survives binarisation, as a function of where the cut
paper\section_replication.tex:48:from $0.001$ to $0.112$. Converted to a sample size for a $\pm 0.05$ half-width, that is between
paper\section_replication.tex:49:$1$ and $20$ items \emph{within a single bank}---and the same calculation on the first corpus
paper\section_replication.tex:52:This is a stronger form of the rule than Section~\ref{sec:items} could state on its own. The
paper\section_replication.tex:53:finding is not that between-item variance is large. It is that the number of items a construct
paper\section_replication.tex:55:tell in advance which kind you have. Our own open-question construct needed $20$ items and we
paper\section_replication.tex:65:Both are paired: same items, same models, same wording, $360$ elicitations each, $100\%$ parse
family1\results\quad_q4_between_items.csv:1:phenomenon,rung,n_items,mean,sd_between_items,min,max
family1\results\raw_neutral_system.jsonl:19:{"model": "gpt-4o", "vendor": "openai", "item_id": "ethi-04-bare", "pair": "ethi-04", "phenomenon": "ethical", "form": "bare", "statement": "Reporting a colleague who falsified data but would lose their visa is the correct choice.", "gloss": "G1", "system": "neutral", "response": "```json\n{\"T\": 0.7, \"I\": 0.3, \"N\": 0.1, \"F\": 0.2}\n```", "T": 0.7, "I": 0.3, "N": 0.1, "F": 0.2, "rung": "weak", "parsed": true, "error": false}
family1\results\raw_neutral_system.jsonl:20:{"model": "claude-sonnet-4", "vendor": "anthropic", "item_id": "ethi-04-bare", "pair": "ethi-04", "phenomenon": "ethical", "form": "bare", "statement": "Reporting a colleague who falsified data but would lose their visa is the correct choice.", "gloss": "G1", "system": "neutral", "response": "{\"T\": 0.7, \"I\": 0.6, \"N\": 0.3, \"F\": 0.3}", "T": 0.7, "I": 0.6, "N": 0.3, "F": 0.3, "rung": "weak", "parsed": true, "error": false}
family1\results\raw_neutral_system.jsonl:21:{"model": "llama-4-maverick", "vendor": "meta", "item_id": "ethi-04-bare", "pair": "ethi-04", "phenomenon": "ethical", "form": "bare", "statement": "Reporting a colleague who falsified data but would lose their visa is the correct choice.", "gloss": "G1", "system": "neutral", "response": "{\"T\": 0.7, \"I\": 0.3, \"", "T": null, "I": null, "N": null, "F": null, "rung": null, "parsed": false, "error": false}
family1\results\raw_neutral_system.jsonl:22:{"model": "deepseek-chat", "vendor": "deepseek", "item_id": "ethi-04-bare", "pair": "ethi-04", "phenomenon": "ethical", "form": "bare", "statement": "Reporting a colleague who falsified data but would lose their visa is the correct choice.", "gloss": "G1", "system": "neutral", "response": "```json\n{\"T\": 0.7, \"I\": 0.3, \"N\": 0.2, \"F\": 0.1}\n```", "T": 0.7, "I": 0.3, "N": 0.2, "F": 0.1, "rung": "weak", "parsed": true, "error": false}
family1\results\raw_neutral_system.jsonl:23:{"model": "qwen3-235b", "vendor": "alibaba", "item_id": "ethi-04-bare", "pair": "ethi-04", "phenomenon": "ethical", "form": "bare", "statement": "Reporting a colleague who falsified data but would lose their visa is the correct choice.", "gloss": "G1", "system": "neutral", "response": "{\"T\": 0.8, \"I\": 0.15, \"N\": 0.05, \"F\": 0.2}", "T": 0.8, "I": 0.15, "N": 0.05, "F": 0.2, "rung": "weak", "parsed": true, "error": false}
family1\results\raw_neutral_system.jsonl:24:{"model": "mistral-medium-3.1", "vendor": "mistral", "item_id": "ethi-04-bare", "pair": "ethi-04", "phenomenon": "ethical", "form": "bare", "statement": "Reporting a colleague who falsified data but would lose their visa is the correct choice.", "gloss": "G1", "system": "neutral", "response": "```json\n{\n  \"T\": 0.75,\n  \"I\": 0.20,\n  \"N\": 0.05,\n  \"F\": 0.00\n}\n```", "T": 0.75, "I": 0.2, "N": 0.05, "F": 0.0, "rung": "classical", "parsed": true, "error": false}
family1\results\raw_nolicense_system.jsonl:19:{"model": "gpt-4o", "vendor": "openai", "item_id": "ethi-04-bare", "pair": "ethi-04", "phenomenon": "ethical", "form": "bare", "statement": "Reporting a colleague who falsified data but would lose their visa is the correct choice.", "gloss": "G1", "system": "nolicense", "response": "{\"T\": 0.7, \"I\": 0.4, \"N\": 0.3, \"F\": 0.5}", "T": 0.7, "I": 0.4, "N": 0.3, "F": 0.5, "rung": "strong", "parsed": true, "error": false}
family1\results\raw_nolicense_system.jsonl:20:{"model": "claude-sonnet-4", "vendor": "anthropic", "item_id": "ethi-04-bare", "pair": "ethi-04", "phenomenon": "ethical", "form": "bare", "statement": "Reporting a colleague who falsified data but would lose their visa is the correct choice.", "gloss": "G1", "system": "nolicense", "response": "{\"T\": 0.7, \"I\": 0.6, \"N\": 0.4, \"F\": 0.3}", "T": 0.7, "I": 0.6, "N": 0.4, "F": 0.3, "rung": "weak", "parsed": true, "error": false}
family1\results\raw_nolicense_system.jsonl:21:{"model": "llama-4-maverick", "vendor": "meta", "item_id": "ethi-04-bare", "pair": "ethi-04", "phenomenon": "ethical", "form": "bare", "statement": "Reporting a colleague who falsified data but would lose their visa is the correct choice.", "gloss": "G1", "system": "nolicense", "response": "{\"T\": 0.7, \"I\": 0.4, \"", "T": null, "I": null, "N": null, "F": null, "rung": null, "parsed": false, "error": false}
family1\results\raw_nolicense_system.jsonl:22:{"model": "deepseek-chat", "vendor": "deepseek", "item_id": "ethi-04-bare", "pair": "ethi-04", "phenomenon": "ethical", "form": "bare", "statement": "Reporting a colleague who falsified data but would lose their visa is the correct choice.", "gloss": "G1", "system": "nolicense", "response": "{\"T\": 0.7, \"I\": 0.4, \"N\": 0.3, \"F\": 0.2}", "T": 0.7, "I": 0.4, "N": 0.3, "F": 0.2, "rung": "weak", "parsed": true, "error": false}
family1\results\raw_nolicense_system.jsonl:23:{"model": "qwen3-235b", "vendor": "alibaba", "item_id": "ethi-04-bare", "pair": "ethi-04", "phenomenon": "ethical", "form": "bare", "statement": "Reporting a colleague who falsified data but would lose their visa is the correct choice.", "gloss": "G1", "system": "nolicense", "response": "{\"T\": 0.8, \"I\": 0.3, \"N\": 0.1, \"F\": 0.2}", "T": 0.8, "I": 0.3, "N": 0.1, "F": 0.2, "rung": "weak", "parsed": true, "error": false}
family1\results\raw_nolicense_system.jsonl:24:{"model": "mistral-medium-3.1", "vendor": "mistral", "item_id": "ethi-04-bare", "pair": "ethi-04", "phenomenon": "ethical", "form": "bare", "statement": "Reporting a colleague who falsified data but would lose their visa is the correct choice.", "gloss": "G1", "system": "nolicense", "response": "```json\n{\n  \"T\": 0.65,\n  \"I\": 0.55,\n  \"N\": 0.30,\n  \"F\": 0.40\n}\n```", "T": 0.65, "I": 0.55, "N": 0.3, "F": 0.4, "rung": "strong", "parsed": true, "error": false}
family1\results\raw_quad_bank.jsonl:109:{"model": "gpt-4o", "vendor": "openai", "item_id": "ethi-04-bare", "pair": "ethi-04", "phenomenon": "ethical", "form": "bare", "statement": "Reporting a colleague who falsified data but would lose their visa is the correct choice.", "gloss": "G1", "response": "{\"T\": 0.7, \"I\": 0.4, \"N\": 0.3, \"F\": 0.2}", "T": 0.7, "I": 0.4, "N": 0.3, "F": 0.2, "rung": "weak", "parsed": true, "error": false}
family1\results\raw_quad_bank.jsonl:110:{"model": "gpt-4o", "vendor": "openai", "item_id": "ethi-04-bare", "pair": "ethi-04", "phenomenon": "ethical", "form": "bare", "statement": "Reporting a colleague who falsified data but would lose their visa is the correct choice.", "gloss": "G2", "response": "```json\n{\"T\": 0.7, \"I\": 0.4, \"N\": 0.2, \"F\": 0.3}\n```", "T": 0.7, "I": 0.4, "N": 0.2, "F": 0.3, "rung": "weak", "parsed": true, "error": false}
family1\results\raw_quad_bank.jsonl:111:{"model": "gpt-4o", "vendor": "openai", "item_id": "ethi-04-bare", "pair": "ethi-04", "phenomenon": "ethical", "form": "bare", "statement": "Reporting a colleague who falsified data but would lose their visa is the correct choice.", "gloss": "G3", "response": "```json\n{\"T\": 0.7, \"I\": 0.5, \"N\": 0.6, \"F\": 0.3}\n```", "T": 0.7, "I": 0.5, "N": 0.6, "F": 0.3, "rung": "weak", "parsed": true, "error": false}
family1\results\raw_quad_bank.jsonl:112:{"model": "claude-sonnet-4", "vendor": "anthropic", "item_id": "ethi-04-bare", "pair": "ethi-04", "phenomenon": "ethical", "form": "bare", "statement": "Reporting a colleague who falsified data but would lose their visa is the correct choice.", "gloss": "G1", "response": "{\"T\": 0.7, \"I\": 0.8, \"N\": 0.2, \"F\": 0.4}", "T": 0.7, "I": 0.8, "N": 0.2, "F": 0.4, "rung": "strong", "parsed": true, "error": false}
family1\results\raw_quad_bank.jsonl:113:{"model": "claude-sonnet-4", "vendor": "anthropic", "item_id": "ethi-04-bare", "pair": "ethi-04", "phenomenon": "ethical", "form": "bare", "statement": "Reporting a colleague who falsified data but would lose their visa is the correct choice.", "gloss": "G2", "response": "{\"T\": 0.7, \"I\": 0.8, \"N\": 0.3, \"F\": 0.4}", "T": 0.7, "I": 0.8, "N": 0.3, "F": 0.4, "rung": "strong", "parsed": true, "error": false}
family1\results\raw_quad_bank.jsonl:114:{"model": "claude-sonnet-4", "vendor": "anthropic", "item_id": "ethi-04-bare", "pair": "ethi-04", "phenomenon": "ethical", "form": "bare", "statement": "Reporting a colleague who falsified data but would lose their visa is the correct choice.", "gloss": "G3", "response": "{\"T\": 0.7, \"I\": 0.6, \"N\": 0.8, \"F\": 0.4}", "T": 0.7, "I": 0.6, "N": 0.8, "F": 0.4, "rung": "strong", "parsed": true, "error": false}
family1\results\raw_quad_bank.jsonl:115:{"model": "llama-4-maverick", "vendor": "meta", "item_id": "ethi-04-bare", "pair": "ethi-04", "phenomenon": "ethical", "form": "bare", "statement": "Reporting a colleague who falsified data but would lose their visa is the correct choice.", "gloss": "G1", "response": "{\"T\": 0.7, \"I\": 0.4, \"N\": 0.2, \"F\": 0.3}", "T": 0.7, "I": 0.4, "N": 0.2, "F": 0.3, "rung": "weak", "parsed": true, "error": false}
family1\results\raw_quad_bank.jsonl:116:{"model": "llama-4-maverick", "vendor": "meta", "item_id": "ethi-04-bare", "pair": "ethi-04", "phenomenon": "ethical", "form": "bare", "statement": "Reporting a colleague who falsified data but would lose their visa is the correct choice.", "gloss": "G2", "response": "{\"T\": 0.7, \"I\": 0.4, \"N\": 0.1, \"F\": 0.3}", "T": 0.7, "I": 0.4, "N": 0.1, "F": 0.3, "rung": "weak", "parsed": true, "error": false}
family1\results\raw_quad_bank.jsonl:117:{"model": "llama-4-maverick", "vendor": "meta", "item_id": "ethi-04-bare", "pair": "ethi-04", "phenomenon": "ethical", "form": "bare", "statement": "Reporting a colleague who falsified data but would lose their visa is the correct choice.", "gloss": "G3", "response": "{\"T\": 0.7, \"I\": 0.4, \"N\": 0.2, \"F\": 0.3}", "T": 0.7, "I": 0.4, "N": 0.2, "F": 0.3, "rung": "weak", "parsed": true, "error": false}
family1\results\raw_quad_bank.jsonl:118:{"model": "deepseek-chat", "vendor": "deepseek", "item_id": "ethi-04-bare", "pair": "ethi-04", "phenomenon": "ethical", "form": "bare", "statement": "Reporting a colleague who falsified data but would lose their visa is the correct choice.", "gloss": "G1", "response": "```json\n{\"T\": 0.7, \"I\": 0.3, \"N\": 0.2, \"F\": 0.4}\n```", "T": 0.7, "I": 0.3, "N": 0.2, "F": 0.4, "rung": "strong", "parsed": true, "error": false}
family1\results\raw_quad_bank.jsonl:119:{"model": "deepseek-chat", "vendor": "deepseek", "item_id": "ethi-04-bare", "pair": "ethi-04", "phenomenon": "ethical", "form": "bare", "statement": "Reporting a colleague who falsified data but would lose their visa is the correct choice.", "gloss": "G2", "response": "```json\n{\"T\": 0.6, \"I\": 0.3, \"N\": 0.2, \"F\": 0.4}\n```", "T": 0.6, "I": 0.3, "N": 0.2, "F": 0.4, "rung": "weak", "parsed": true, "error": false}
family1\results\raw_quad_bank.jsonl:120:{"model": "deepseek-chat", "vendor": "deepseek", "item_id": "ethi-04-bare", "pair": "ethi-04", "phenomenon": "ethical", "form": "bare", "statement": "Reporting a colleague who falsified data but would lose their visa is the correct choice.", "gloss": "G3", "response": "```json\n{\"T\": 0.7, \"I\": 0.3, \"N\": 0.4, \"F\": 0.2}\n```", "T": 0.7, "I": 0.3, "N": 0.4, "F": 0.2, "rung": "weak", "parsed": true, "error": false}
family1\results\raw_quad_bank.jsonl:121:{"model": "qwen3-235b", "vendor": "alibaba", "item_id": "ethi-04-bare", "pair": "ethi-04", "phenomenon": "ethical", "form": "bare", "statement": "Reporting a colleague who falsified data but would lose their visa is the correct choice.", "gloss": "G1", "response": "{\"T\": 0.7, \"I\": 0.3, \"N\": 0.2, \"F\": 0.4}", "T": 0.7, "I": 0.3, "N": 0.2, "F": 0.4, "rung": "strong", "parsed": true, "error": false}
family1\results\raw_quad_bank.jsonl:122:{"model": "qwen3-235b", "vendor": "alibaba", "item_id": "ethi-04-bare", "pair": "ethi-04", "phenomenon": "ethical", "form": "bare", "statement": "Reporting a colleague who falsified data but would lose their visa is the correct choice.", "gloss": "G2", "response": "{\"T\": 0.7, \"I\": 0.2, \"N\": 0.1, \"F\": 0.3}", "T": 0.7, "I": 0.2, "N": 0.1, "F": 0.3, "rung": "weak", "parsed": true, "error": false}
family1\results\raw_quad_bank.jsonl:123:{"model": "qwen3-235b", "vendor": "alibaba", "item_id": "ethi-04-bare", "pair": "ethi-04", "phenomenon": "ethical", "form": "bare", "statement": "Reporting a colleague who falsified data but would lose their visa is the correct choice.", "gloss": "G3", "response": "{\"T\": 0.7, \"I\": 0.2, \"N\": 0.3, \"F\": 0.4}", "T": 0.7, "I": 0.2, "N": 0.3, "F": 0.4, "rung": "strong", "parsed": true, "error": false}
family1\results\raw_quad_bank.jsonl:124:{"model": "mistral-medium-3.1", "vendor": "mistral", "item_id": "ethi-04-bare", "pair": "ethi-04", "phenomenon": "ethical", "form": "bare", "statement": "Reporting a colleague who falsified data but would lose their visa is the correct choice.", "gloss": "G1", "response": "```json\n{\n  \"T\": 0.7,\n  \"I\": 0.35,\n  \"N\": 0.15,\n  \"F\": 0.2\n}\n```", "T": 0.7, "I": 0.35, "N": 0.15, "F": 0.2, "rung": "weak", "parsed": true, "error": false}
family1\results\raw_quad_bank.jsonl:125:{"model": "mistral-medium-3.1", "vendor": "mistral", "item_id": "ethi-04-bare", "pair": "ethi-04", "phenomenon": "ethical", "form": "bare", "statement": "Reporting a colleague who falsified data but would lose their visa is the correct choice.", "gloss": "G2", "response": "```json\n{\n  \"T\": 0.65,\n  \"I\": 0.55,\n  \"N\": 0.30,\n  \"F\": 0.40\n}\n```", "T": 0.65, "I": 0.55, "N": 0.3, "F": 0.4, "rung": "strong", "parsed": true, "error": false}
family1\results\raw_quad_bank.jsonl:126:{"model": "mistral-medium-3.1", "vendor": "mistral", "item_id": "ethi-04-bare", "pair": "ethi-04", "phenomenon": "ethical", "form": "bare", "statement": "Reporting a colleague who falsified data but would lose their visa is the correct choice.", "gloss": "G3", "response": "```json\n{\n  \"T\": 0.65,\n  \"I\": 0.40,\n  \"N\": 0.50,\n  \"F\": 0.30\n}\n```", "T": 0.65, "I": 0.4, "N": 0.5, "F": 0.3, "rung": "weak", "parsed": true, "error": false}
family1\results\raw_quad_bank.jsonl:127:{"model": "gpt-4o", "vendor": "openai", "item_id": "ethi-04-mark", "pair": "ethi-04", "phenomenon": "ethical", "form": "marked", "statement": "Reporting a colleague who falsified data but would lose their visa is both the correct and the incorrect choice.", "gloss": "G1", "response": "```json\n{\"T\": 0.6, \"I\": 0.4, \"N\": 0.3, \"F\": 0.5}\n```", "T": 0.6, "I": 0.4, "N": 0.3, "F": 0.5, "rung": "strong", "parsed": true, "error": false}
family1\results\raw_quad_bank.jsonl:128:{"model": "gpt-4o", "vendor": "openai", "item_id": "ethi-04-mark", "pair": "ethi-04", "phenomenon": "ethical", "form": "marked", "statement": "Reporting a colleague who falsified data but would lose their visa is both the correct and the incorrect choice.", "gloss": "G2", "response": "```json\n{\"T\": 0.6, \"I\": 0.7, \"N\": 0.5, \"F\": 0.4}\n```", "T": 0.6, "I": 0.7, "N": 0.5, "F": 0.4, "rung": "weak", "parsed": true, "error": false}
family1\results\raw_quad_bank.jsonl:129:{"model": "gpt-4o", "vendor": "openai", "item_id": "ethi-04-mark", "pair": "ethi-04", "phenomenon": "ethical", "form": "marked", "statement": "Reporting a colleague who falsified data but would lose their visa is both the correct and the incorrect choice.", "gloss": "G3", "response": "```json\n{\"T\": 0.7, \"I\": 0.4, \"N\": 0.8, \"F\": 0.6}\n```", "T": 0.7, "I": 0.4, "N": 0.8, "F": 0.6, "rung": "strong", "parsed": true, "error": false}
family1\results\raw_quad_bank.jsonl:130:{"model": "claude-sonnet-4", "vendor": "anthropic", "item_id": "ethi-04-mark", "pair": "ethi-04", "phenomenon": "ethical", "form": "marked", "statement": "Reporting a colleague who falsified data but would lose their visa is both the correct and the incorrect choice.", "gloss": "G1", "response": "{\"T\": 0.8, \"I\": 0.7, \"N\": 0.2, \"F\": 0.3}", "T": 0.8, "I": 0.7, "N": 0.2, "F": 0.3, "rung": "strong", "parsed": true, "error": false}
family1\results\raw_quad_bank.jsonl:131:{"model": "claude-sonnet-4", "vendor": "anthropic", "item_id": "ethi-04-mark", "pair": "ethi-04", "phenomenon": "ethical", "form": "marked", "statement": "Reporting a colleague who falsified data but would lose their visa is both the correct and the incorrect choice.", "gloss": "G2", "response": "{\"T\": 0.8, \"I\": 0.7, \"N\": 0.3, \"F\": 0.2}", "T": 0.8, "I": 0.7, "N": 0.3, "F": 0.2, "rung": "weak", "parsed": true, "error": false}
family1\results\raw_quad_bank.jsonl:132:{"model": "claude-sonnet-4", "vendor": "anthropic", "item_id": "ethi-04-mark", "pair": "ethi-04", "phenomenon": "ethical", "form": "marked", "statement": "Reporting a colleague who falsified data but would lose their visa is both the correct and the incorrect choice.", "gloss": "G3", "response": "{\"T\": 0.8, \"I\": 0.3, \"N\": 0.9, \"F\": 0.2}", "T": 0.8, "I": 0.3, "N": 0.9, "F": 0.2, "rung": "weak", "parsed": true, "error": false}
family1\results\raw_quad_bank.jsonl:133:{"model": "llama-4-maverick", "vendor": "meta", "item_id": "ethi-04-mark", "pair": "ethi-04", "phenomenon": "ethical", "form": "marked", "statement": "Reporting a colleague who falsified data but would lose their visa is both the correct and the incorrect choice.", "gloss": "G1", "response": "{\"T\": 0.7, \"I\": 0.4, \"N\": 0.3, \"F\": 0.2}", "T": 0.7, "I": 0.4, "N": 0.3, "F": 0.2, "rung": "weak", "parsed": true, "error": false}
family1\results\raw_quad_bank.jsonl:134:{"model": "llama-4-maverick", "vendor": "meta", "item_id": "ethi-04-mark", "pair": "ethi-04", "phenomenon": "ethical", "form": "marked", "statement": "Reporting a colleague who falsified data but would lose their visa is both the correct and the incorrect choice.", "gloss": "G2", "response": "{\"T\": 0.7, \"I\": 0.4, \"N\": 0.2, \"F\": 0.3}", "T": 0.7, "I": 0.4, "N": 0.2, "F": 0.3, "rung": "weak", "parsed": true, "error": false}
family1\results\raw_quad_bank.jsonl:135:{"model": "llama-4-maverick", "vendor": "meta", "item_id": "ethi-04-mark", "pair": "ethi-04", "phenomenon": "ethical", "form": "marked", "statement": "Reporting a colleague who falsified data but would lose their visa is both the correct and the incorrect choice.", "gloss": "G3", "response": "{\"T\": 0.7, \"I\": 0.4, \"N\": 0.8, \"F\": 0.3}", "T": 0.7, "I": 0.4, "N": 0.8, "F": 0.3, "rung": "weak", "parsed": true, "error": false}
family1\results\raw_quad_bank.jsonl:136:{"model": "deepseek-chat", "vendor": "deepseek", "item_id": "ethi-04-mark", "pair": "ethi-04", "phenomenon": "ethical", "form": "marked", "statement": "Reporting a colleague who falsified data but would lose their visa is both the correct and the incorrect choice.", "gloss": "G1", "response": "{\"T\": 0.7, \"I\": 0.3, \"N\": 0.2, \"F\": 0.4}", "T": 0.7, "I": 0.3, "N": 0.2, "F": 0.4, "rung": "strong", "parsed": true, "error": false}
family1\results\raw_quad_bank.jsonl:137:{"model": "deepseek-chat", "vendor": "deepseek", "item_id": "ethi-04-mark", "pair": "ethi-04", "phenomenon": "ethical", "form": "marked", "statement": "Reporting a colleague who falsified data but would lose their visa is both the correct and the incorrect choice.", "gloss": "G2", "response": "```json\n{\"T\": 0.7, \"I\": 0.5, \"N\": 0.3, \"F\": 0.4}\n```", "T": 0.7, "I": 0.5, "N": 0.3, "F": 0.4, "rung": "strong", "parsed": true, "error": false}
family1\results\raw_quad_bank.jsonl:138:{"model": "deepseek-chat", "vendor": "deepseek", "item_id": "ethi-04-mark", "pair": "ethi-04", "phenomenon": "ethical", "form": "marked", "statement": "Reporting a colleague who falsified data but would lose their visa is both the correct and the incorrect choice.", "gloss": "G3", "response": "```json\n{\"T\": 0.7, \"I\": 0.3, \"N\": 0.5, \"F\": 0.4}\n```", "T": 0.7, "I": 0.3, "N": 0.5, "F": 0.4, "rung": "strong", "parsed": true, "error": false}
family1\results\raw_quad_bank.jsonl:139:{"model": "qwen3-235b", "vendor": "alibaba", "item_id": "ethi-04-mark", "pair": "ethi-04", "phenomenon": "ethical", "form": "marked", "statement": "Reporting a colleague who falsified data but would lose their visa is both the correct and the incorrect choice.", "gloss": "G1", "response": "{\"T\": 0.7, \"I\": 0.6, \"N\": 0.5, \"F\": 0.3}", "T": 0.7, "I": 0.6, "N": 0.5, "F": 0.3, "rung": "weak", "parsed": true, "error": false}
family1\results\raw_quad_bank.jsonl:140:{"model": "qwen3-235b", "vendor": "alibaba", "item_id": "ethi-04-mark", "pair": "ethi-04", "phenomenon": "ethical", "form": "marked", "statement": "Reporting a colleague who falsified data but would lose their visa is both the correct and the incorrect choice.", "gloss": "G2", "response": "{\"T\": 0.7, \"I\": 0.6, \"N\": 0.2, \"F\": 0.5}", "T": 0.7, "I": 0.6, "N": 0.2, "F": 0.5, "rung": "strong", "parsed": true, "error": false}
family1\results\raw_quad_bank.jsonl:141:{"model": "qwen3-235b", "vendor": "alibaba", "item_id": "ethi-04-mark", "pair": "ethi-04", "phenomenon": "ethical", "form": "marked", "statement": "Reporting a colleague who falsified data but would lose their visa is both the correct and the incorrect choice.", "gloss": "G3", "response": "{\"T\": 0.7, \"I\": 0.5, \"N\": 0.6, \"F\": 0.3}", "T": 0.7, "I": 0.5, "N": 0.6, "F": 0.3, "rung": "weak", "parsed": true, "error": false}
family1\results\raw_quad_bank.jsonl:142:{"model": "mistral-medium-3.1", "vendor": "mistral", "item_id": "ethi-04-mark", "pair": "ethi-04", "phenomenon": "ethical", "form": "marked", "statement": "Reporting a colleague who falsified data but would lose their visa is both the correct and the incorrect choice.", "gloss": "G1", "response": "```json\n{\n  \"T\": 0.75,\n  \"I\": 0.65,\n  \"N\": 0.30,\n  \"F\": 0.60\n}\n```", "T": 0.75, "I": 0.65, "N": 0.3, "F": 0.6, "rung": "strong", "parsed": true, "error": false}
family1\results\raw_quad_bank.jsonl:143:{"model": "mistral-medium-3.1", "vendor": "mistral", "item_id": "ethi-04-mark", "pair": "ethi-04", "phenomenon": "ethical", "form": "marked", "statement": "Reporting a colleague who falsified data but would lose their visa is both the correct and the incorrect choice.", "gloss": "G2", "response": "```json\n{\n  \"T\": 0.75,\n  \"I\": 0.60,\n  \"N\": 0.30,\n  \"F\": 0.45\n}\n```", "T": 0.75, "I": 0.6, "N": 0.3, "F": 0.45, "rung": "strong", "parsed": true, "error": false}
family1\results\raw_quad_bank.jsonl:144:{"model": "mistral-medium-3.1", "vendor": "mistral", "item_id": "ethi-04-mark", "pair": "ethi-04", "phenomenon": "ethical", "form": "marked", "statement": "Reporting a colleague who falsified data but would lose their visa is both the correct and the incorrect choice.", "gloss": "G3", "response": "```json\n{\n  \"T\": 0.7,\n  \"I\": 0.5,\n  \"N\": 0.8,\n  \"F\": 0.3\n}\n```", "T": 0.7, "I": 0.5, "N": 0.8, "F": 0.3, "rung": "weak", "parsed": true, "error": false}
family1\results\raw_bank.jsonl:109:{"model": "gpt-4o", "vendor": "openai", "item_id": "ethi-04-bare", "pair": "ethi-04", "phenomenon": "ethical", "form": "bare", "statement": "Reporting a colleague who falsified data but would lose their visa is the correct choice.", "rep": 0, "response": "```json\n{\"T\": 0.7, \"I\": 0.5, \"F\": 0.3}\n```", "T": 0.7, "I": 0.5, "F": 0.3, "strong": 0, "parsed": true, "error": false}
family1\results\raw_bank.jsonl:110:{"model": "gpt-4o", "vendor": "openai", "item_id": "ethi-04-bare", "pair": "ethi-04", "phenomenon": "ethical", "form": "bare", "statement": "Reporting a colleague who falsified data but would lose their visa is the correct choice.", "rep": 1, "response": "{\"T\": 0.7, \"I\": 0.4, \"F\": 0.3}", "T": 0.7, "I": 0.4, "F": 0.3, "strong": 0, "parsed": true, "error": false}
family1\results\raw_bank.jsonl:111:{"model": "gpt-4o", "vendor": "openai", "item_id": "ethi-04-bare", "pair": "ethi-04", "phenomenon": "ethical", "form": "bare", "statement": "Reporting a colleague who falsified data but would lose their visa is the correct choice.", "rep": 2, "response": "```json\n{\"T\": 0.6, \"I\": 0.4, \"F\": 0.3}\n```", "T": 0.6, "I": 0.4, "F": 0.3, "strong": 0, "parsed": true, "error": false}
family1\results\raw_bank.jsonl:112:{"model": "claude-sonnet-4", "vendor": "anthropic", "item_id": "ethi-04-bare", "pair": "ethi-04", "phenomenon": "ethical", "form": "bare", "statement": "Reporting a colleague who falsified data but would lose their visa is the correct choice.", "rep": 0, "response": "{\"T\": 0.7, \"I\": 0.6, \"F\": 0.4}", "T": 0.7, "I": 0.6, "F": 0.4, "strong": 1, "parsed": true, "error": false}
family1\results\raw_bank.jsonl:113:{"model": "claude-sonnet-4", "vendor": "anthropic", "item_id": "ethi-04-bare", "pair": "ethi-04", "phenomenon": "ethical", "form": "bare", "statement": "Reporting a colleague who falsified data but would lose their visa is the correct choice.", "rep": 1, "response": "{\"T\": 0.7, \"I\": 0.6, \"F\": 0.4}", "T": 0.7, "I": 0.6, "F": 0.4, "strong": 1, "parsed": true, "error": false}
family1\results\raw_bank.jsonl:114:{"model": "claude-sonnet-4", "vendor": "anthropic", "item_id": "ethi-04-bare", "pair": "ethi-04", "phenomenon": "ethical", "form": "bare", "statement": "Reporting a colleague who falsified data but would lose their visa is the correct choice.", "rep": 2, "response": "{\"T\": 0.7, \"I\": 0.8, \"F\": 0.4}", "T": 0.7, "I": 0.8, "F": 0.4, "strong": 1, "parsed": true, "error": false}
family1\results\raw_bank.jsonl:115:{"model": "llama-4-maverick", "vendor": "meta", "item_id": "ethi-04-bare", "pair": "ethi-04", "phenomenon": "ethical", "form": "bare", "statement": "Reporting a colleague who falsified data but would lose their visa is the correct choice.", "rep": 0, "response": "{\"T\": 0.7, \"I\": 0.4, \"F\": 0.3}", "T": 0.7, "I": 0.4, "F": 0.3, "strong": 0, "parsed": true, "error": false}
family1\results\raw_bank.jsonl:116:{"model": "llama-4-maverick", "vendor": "meta", "item_id": "ethi-04-bare", "pair": "ethi-04", "phenomenon": "ethical", "form": "bare", "statement": "Reporting a colleague who falsified data but would lose their visa is the correct choice.", "rep": 1, "response": "{\"T\": 0.7, \"I\": 0.4, \"F\": 0.3}", "T": 0.7, "I": 0.4, "F": 0.3, "strong": 0, "parsed": true, "error": false}
family1\results\raw_bank.jsonl:117:{"model": "llama-4-maverick", "vendor": "meta", "item_id": "ethi-04-bare", "pair": "ethi-04", "phenomenon": "ethical", "form": "bare", "statement": "Reporting a colleague who falsified data but would lose their visa is the correct choice.", "rep": 2, "response": "{\"T\": 0.7, \"I\": 0.4, \"F\": 0.3}", "T": 0.7, "I": 0.4, "F": 0.3, "strong": 0, "parsed": true, "error": false}
family1\results\raw_bank.jsonl:118:{"model": "deepseek-chat", "vendor": "deepseek", "item_id": "ethi-04-bare", "pair": "ethi-04", "phenomenon": "ethical", "form": "bare", "statement": "Reporting a colleague who falsified data but would lose their visa is the correct choice.", "rep": 0, "response": "```json\n{\"T\": 0.7, \"I\": 0.3, \"F\": 0.2}\n```", "T": 0.7, "I": 0.3, "F": 0.2, "strong": 0, "parsed": true, "error": false}
family1\results\raw_bank.jsonl:119:{"model": "deepseek-chat", "vendor": "deepseek", "item_id": "ethi-04-bare", "pair": "ethi-04", "phenomenon": "ethical", "form": "bare", "statement": "Reporting a colleague who falsified data but would lose their visa is the correct choice.", "rep": 1, "response": "```json\n{\"T\": 0.7, \"I\": 0.5, \"F\": 0.3}\n```", "T": 0.7, "I": 0.5, "F": 0.3, "strong": 0, "parsed": true, "error": false}
family1\results\raw_bank.jsonl:120:{"model": "deepseek-chat", "vendor": "deepseek", "item_id": "ethi-04-bare", "pair": "ethi-04", "phenomenon": "ethical", "form": "bare", "statement": "Reporting a colleague who falsified data but would lose their visa is the correct choice.", "rep": 2, "response": "{\"T\": 0.7, \"I\": 0.4, \"F\": 0.3}", "T": 0.7, "I": 0.4, "F": 0.3, "strong": 0, "parsed": true, "error": false}
family1\results\raw_bank.jsonl:121:{"model": "qwen3-235b", "vendor": "alibaba", "item_id": "ethi-04-bare", "pair": "ethi-04", "phenomenon": "ethical", "form": "bare", "statement": "Reporting a colleague who falsified data but would lose their visa is the correct choice.", "rep": 0, "response": "{\"T\": 0.7, \"I\": 0.6, \"F\": 0.4}", "T": 0.7, "I": 0.6, "F": 0.4, "strong": 1, "parsed": true, "error": false}
family1\results\raw_bank.jsonl:122:{"model": "qwen3-235b", "vendor": "alibaba", "item_id": "ethi-04-bare", "pair": "ethi-04", "phenomenon": "ethical", "form": "bare", "statement": "Reporting a colleague who falsified data but would lose their visa is the correct choice.", "rep": 1, "response": "{\"T\": 0.7, \"I\": 0.5, \"F\": 0.3}", "T": 0.7, "I": 0.5, "F": 0.3, "strong": 0, "parsed": true, "error": false}
family1\results\raw_bank.jsonl:123:{"model": "qwen3-235b", "vendor": "alibaba", "item_id": "ethi-04-bare", "pair": "ethi-04", "phenomenon": "ethical", "form": "bare", "statement": "Reporting a colleague who falsified data but would lose their visa is the correct choice.", "rep": 2, "response": "{\"T\": 0.7, \"I\": 0.5, \"F\": 0.3}", "T": 0.7, "I": 0.5, "F": 0.3, "strong": 0, "parsed": true, "error": false}
family1\results\raw_bank.jsonl:124:{"model": "mistral-medium-3.1", "vendor": "mistral", "item_id": "ethi-04-bare", "pair": "ethi-04", "phenomenon": "ethical", "form": "bare", "statement": "Reporting a colleague who falsified data but would lose their visa is the correct choice.", "rep": 0, "response": "```json\n{\n  \"T\": 0.65,\n  \"I\": 0.70,\n  \"F\": 0.40\n}\n```", "T": 0.65, "I": 0.7, "F": 0.4, "strong": 1, "parsed": true, "error": false}
family1\results\raw_bank.jsonl:125:{"model": "mistral-medium-3.1", "vendor": "mistral", "item_id": "ethi-04-bare", "pair": "ethi-04", "phenomenon": "ethical", "form": "bare", "statement": "Reporting a colleague who falsified data but would lose their visa is the correct choice.", "rep": 1, "response": "```json\n{\n  \"T\": 0.65,\n  \"I\": 0.70,\n  \"F\": 0.40\n}\n```", "T": 0.65, "I": 0.7, "F": 0.4, "strong": 1, "parsed": true, "error": false}
family1\results\raw_bank.jsonl:126:{"model": "mistral-medium-3.1", "vendor": "mistral", "item_id": "ethi-04-bare", "pair": "ethi-04", "phenomenon": "ethical", "form": "bare", "statement": "Reporting a colleague who falsified data but would lose their visa is the correct choice.", "rep": 2, "response": "```json\n{\n  \"T\": 0.65,\n  \"I\": 0.70,\n  \"F\": 0.50\n}\n```", "T": 0.65, "I": 0.7, "F": 0.5, "strong": 1, "parsed": true, "error": false}
family1\results\raw_bank.jsonl:127:{"model": "gpt-4o", "vendor": "openai", "item_id": "ethi-04-mark", "pair": "ethi-04", "phenomenon": "ethical", "form": "marked", "statement": "Reporting a colleague who falsified data but would lose their visa is both the correct and the incorrect choice.", "rep": 0, "response": "```json\n{\"T\": 0.6, \"I\": 0.7, \"F\": 0.3}\n```", "T": 0.6, "I": 0.7, "F": 0.3, "strong": 0, "parsed": true, "error": false}
family1\results\raw_bank.jsonl:128:{"model": "gpt-4o", "vendor": "openai", "item_id": "ethi-04-mark", "pair": "ethi-04", "phenomenon": "ethical", "form": "marked", "statement": "Reporting a colleague who falsified data but would lose their visa is both the correct and the incorrect choice.", "rep": 1, "response": "{\"T\": 0.6, \"I\": 0.7, \"F\": 0.4}", "T": 0.6, "I": 0.7, "F": 0.4, "strong": 0, "parsed": true, "error": false}
family1\results\raw_bank.jsonl:129:{"model": "gpt-4o", "vendor": "openai", "item_id": "ethi-04-mark", "pair": "ethi-04", "phenomenon": "ethical", "form": "marked", "statement": "Reporting a colleague who falsified data but would lose their visa is both the correct and the incorrect choice.", "rep": 2, "response": "{\"T\": 0.7, \"I\": 0.6, \"F\": 0.4}", "T": 0.7, "I": 0.6, "F": 0.4, "strong": 1, "parsed": true, "error": false}
family1\results\raw_bank.jsonl:130:{"model": "claude-sonnet-4", "vendor": "anthropic", "item_id": "ethi-04-mark", "pair": "ethi-04", "phenomenon": "ethical", "form": "marked", "statement": "Reporting a colleague who falsified data but would lose their visa is both the correct and the incorrect choice.", "rep": 0, "response": "{\"T\": 0.8, \"I\": 0.7, \"F\": 0.8}", "T": 0.8, "I": 0.7, "F": 0.8, "strong": 1, "parsed": true, "error": false}
family1\results\raw_bank.jsonl:131:{"model": "claude-sonnet-4", "vendor": "anthropic", "item_id": "ethi-04-mark", "pair": "ethi-04", "phenomenon": "ethical", "form": "marked", "statement": "Reporting a colleague who falsified data but would lose their visa is both the correct and the incorrect choice.", "rep": 1, "response": "{\"T\": 0.8, \"I\": 0.7, \"F\": 0.8}", "T": 0.8, "I": 0.7, "F": 0.8, "strong": 1, "parsed": true, "error": false}
family1\results\raw_bank.jsonl:132:{"model": "claude-sonnet-4", "vendor": "anthropic", "item_id": "ethi-04-mark", "pair": "ethi-04", "phenomenon": "ethical", "form": "marked", "statement": "Reporting a colleague who falsified data but would lose their visa is both the correct and the incorrect choice.", "rep": 2, "response": "{\"T\": 0.8, \"I\": 0.7, \"F\": 0.8}", "T": 0.8, "I": 0.7, "F": 0.8, "strong": 1, "parsed": true, "error": false}
family1\results\raw_bank.jsonl:133:{"model": "llama-4-maverick", "vendor": "meta", "item_id": "ethi-04-mark", "pair": "ethi-04", "phenomenon": "ethical", "form": "marked", "statement": "Reporting a colleague who falsified data but would lose their visa is both the correct and the incorrect choice.", "rep": 0, "response": "{\"T\": 0.7, \"I\": 0.5, \"F\": 0.3}", "T": 0.7, "I": 0.5, "F": 0.3, "strong": 0, "parsed": true, "error": false}
family1\results\raw_bank.jsonl:134:{"model": "llama-4-maverick", "vendor": "meta", "item_id": "ethi-04-mark", "pair": "ethi-04", "phenomenon": "ethical", "form": "marked", "statement": "Reporting a colleague who falsified data but would lose their visa is both the correct and the incorrect choice.", "rep": 1, "response": "{\"T\": 0.7, \"I\": 0.5, \"F\": 0.3}", "T": 0.7, "I": 0.5, "F": 0.3, "strong": 0, "parsed": true, "error": false}
family1\results\raw_bank.jsonl:135:{"model": "llama-4-maverick", "vendor": "meta", "item_id": "ethi-04-mark", "pair": "ethi-04", "phenomenon": "ethical", "form": "marked", "statement": "Reporting a colleague who falsified data but would lose their visa is both the correct and the incorrect choice.", "rep": 2, "response": "{\"T\": 0.7, \"I\": 0.5, \"F\": 0.3}", "T": 0.7, "I": 0.5, "F": 0.3, "strong": 0, "parsed": true, "error": false}
family1\results\raw_bank.jsonl:136:{"model": "deepseek-chat", "vendor": "deepseek", "item_id": "ethi-04-mark", "pair": "ethi-04", "phenomenon": "ethical", "form": "marked", "statement": "Reporting a colleague who falsified data but would lose their visa is both the correct and the incorrect choice.", "rep": 0, "response": "```json\n{\"T\": 0.7, \"I\": 0.5, \"F\": 0.3}\n```", "T": 0.7, "I": 0.5, "F": 0.3, "strong": 0, "parsed": true, "error": false}
family1\results\raw_bank.jsonl:137:{"model": "deepseek-chat", "vendor": "deepseek", "item_id": "ethi-04-mark", "pair": "ethi-04", "phenomenon": "ethical", "form": "marked", "statement": "Reporting a colleague who falsified data but would lose their visa is both the correct and the incorrect choice.", "rep": 1, "response": "```json\n{\"T\": 0.7, \"I\": 0.3, \"F\": 0.2}\n```", "T": 0.7, "I": 0.3, "F": 0.2, "strong": 0, "parsed": true, "error": false}
family1\results\raw_bank.jsonl:138:{"model": "deepseek-chat", "vendor": "deepseek", "item_id": "ethi-04-mark", "pair": "ethi-04", "phenomenon": "ethical", "form": "marked", "statement": "Reporting a colleague who falsified data but would lose their visa is both the correct and the incorrect choice.", "rep": 2, "response": "```json\n{\"T\": 0.7, \"I\": 0.5, \"F\": 0.3}\n```", "T": 0.7, "I": 0.5, "F": 0.3, "strong": 0, "parsed": true, "error": false}
family1\results\raw_bank.jsonl:139:{"model": "qwen3-235b", "vendor": "alibaba", "item_id": "ethi-04-mark", "pair": "ethi-04", "phenomenon": "ethical", "form": "marked", "statement": "Reporting a colleague who falsified data but would lose their visa is both the correct and the incorrect choice.", "rep": 0, "response": "{\"T\": 0.7, \"I\": 0.8, \"F\": 0.6}", "T": 0.7, "I": 0.8, "F": 0.6, "strong": 1, "parsed": true, "error": false}
family1\results\raw_bank.jsonl:140:{"model": "qwen3-235b", "vendor": "alibaba", "item_id": "ethi-04-mark", "pair": "ethi-04", "phenomenon": "ethical", "form": "marked", "statement": "Reporting a colleague who falsified data but would lose their visa is both the correct and the incorrect choice.", "rep": 1, "response": "{\"T\": 0.7, \"I\": 0.8, \"F\": 0.6}", "T": 0.7, "I": 0.8, "F": 0.6, "strong": 1, "parsed": true, "error": false}
family1\results\raw_bank.jsonl:141:{"model": "qwen3-235b", "vendor": "alibaba", "item_id": "ethi-04-mark", "pair": "ethi-04", "phenomenon": "ethical", "form": "marked", "statement": "Reporting a colleague who falsified data but would lose their visa is both the correct and the incorrect choice.", "rep": 2, "response": "{\"T\": 0.7, \"I\": 0.8, \"F\": 0.6}", "T": 0.7, "I": 0.8, "F": 0.6, "strong": 1, "parsed": true, "error": false}
family1\results\raw_bank.jsonl:142:{"model": "mistral-medium-3.1", "vendor": "mistral", "item_id": "ethi-04-mark", "pair": "ethi-04", "phenomenon": "ethical", "form": "marked", "statement": "Reporting a colleague who falsified data but would lose their visa is both the correct and the incorrect choice.", "rep": 0, "response": "```json\n{\n  \"T\": 0.75,\n  \"I\": 0.80,\n  \"F\": 0.60\n}\n```", "T": 0.75, "I": 0.8, "F": 0.6, "strong": 1, "parsed": true, "error": false}
family1\results\raw_bank.jsonl:143:{"model": "mistral-medium-3.1", "vendor": "mistral", "item_id": "ethi-04-mark", "pair": "ethi-04", "phenomenon": "ethical", "form": "marked", "statement": "Reporting a colleague who falsified data but would lose their visa is both the correct and the incorrect choice.", "rep": 1, "response": "```json\n{\n  \"T\": 0.75,\n  \"I\": 0.80,\n  \"F\": 0.60\n}\n```", "T": 0.75, "I": 0.8, "F": 0.6, "strong": 1, "parsed": true, "error": false}
family1\results\raw_bank.jsonl:144:{"model": "mistral-medium-3.1", "vendor": "mistral", "item_id": "ethi-04-mark", "pair": "ethi-04", "phenomenon": "ethical", "form": "marked", "statement": "Reporting a colleague who falsified data but would lose their visa is both the correct and the incorrect choice.", "rep": 2, "response": "```json\n{\n  \"T\": 0.75,\n  \"I\": 0.60,\n  \"F\": 0.50\n}\n```", "T": 0.75, "I": 0.6, "F": 0.5, "strong": 1, "parsed": true, "error": false}

exec
"C:\\WINDOWS\\System32\\WindowsPowerShell\\v1.0\\powershell.exe" -Command "Get-Content -LiteralPath 'family1\\results\\raw_quadruple_pilot.jsonl' -TotalCount 5" in C:\Users\HP\Documents\MeasurementScience_Evals\paper11_elicitation_method
exec
"C:\\WINDOWS\\System32\\WindowsPowerShell\\v1.0\\powershell.exe" -Command "Get-Content -LiteralPath 'family1\\run_quad_bank.py'" in C:\Users\HP\Documents\MeasurementScience_Evals\paper11_elicitation_method
exec
"C:\\WINDOWS\\System32\\WindowsPowerShell\\v1.0\\powershell.exe" -Command "Get-Content -LiteralPath 'family1\\run_bank.py'" in C:\Users\HP\Documents\MeasurementScience_Evals\paper11_elicitation_method
exec
"C:\\WINDOWS\\System32\\WindowsPowerShell\\v1.0\\powershell.exe" -Command "Get-Content -LiteralPath 'family1\\README.md'" in C:\Users\HP\Documents\MeasurementScience_Evals\paper11_elicitation_method
 succeeded in 2992ms:
"""Elicita el CUADRUPLE (T, I, N, F) sobre el banco de 110 items.

Prueba la escalera de tres peldanos de Smarandache & Leyva-Vazquez (NSS 100, 2026)
sobre una muestra de items que permite conclusiones a nivel de fenomeno, en vez de
sobre las ocho oraciones del corpus v3.

    fuerte     : T + F > 1                                          (4)
    debil      : T + F <= 1  y  (T+F+I > 1  o  T+F+N > 1)           (5)
    muy debil  : T+F+I <= 1, T+F+N <= 1,  y  T+F+I+N > 1            (6)

Diseno: 110 items x 6 modelos x 3 glosas de N x 1 repeticion = 1.980 llamadas.
Con 110 items la varianza que importa es ENTRE items, no dentro de celda; se
cambian repeticiones por cobertura completa de las tres glosas al mismo costo.

Uso:
    set OPENROUTER_API_KEY=...
    python run_quad_bank.py --count-only
    python run_quad_bank.py --limit 4 --dry-run
    python run_quad_bank.py
"""

from __future__ import annotations

import argparse
import itertools
import json
import os
import re
import sys
import time
from pathlib import Path

from openai import OpenAI

HERE = Path(__file__).resolve().parent
OUT = HERE / "results"
OUT.mkdir(exist_ok=True)
RAW = OUT / "raw_quad_bank.jsonl"

MODELS = [
    {"id": "openai/gpt-4o", "label": "gpt-4o", "vendor": "openai"},
    {"id": "anthropic/claude-sonnet-4", "label": "claude-sonnet-4", "vendor": "anthropic"},
    {"id": "meta-llama/llama-4-maverick", "label": "llama-4-maverick", "vendor": "meta"},
    {"id": "deepseek/deepseek-chat", "label": "deepseek-chat", "vendor": "deepseek"},
    {"id": "qwen/qwen3-235b-a22b-2507", "label": "qwen3-235b", "vendor": "alibaba"},
    {"id": "mistralai/mistral-medium-3.1", "label": "mistral-medium-3.1", "vendor": "mistral"},
]

SYSTEM = (
    "You are an expert in Neutrosophic Logic. You evaluate statements using FOUR "
    "INDEPENDENT dimensions, each on [0.0, 1.0]. These dimensions are NOT constrained "
    "to sum to 1.0. A statement can be simultaneously partially true, partially false, "
    "partially indeterminate and partially neutral. Respond with ONLY a JSON object, "
    "no other text."
)

BASE = (
    'Evaluate this statement on four independent dimensions:\n\n'
    'Statement: "{stmt}"\n\n'
    '- Truth (T): To what degree is this statement true? [0.0 to 1.0]\n'
    '- Indeterminacy (I): To what degree is the truth value unknown, undetermined, '
    'or inherently uncertain? [0.0 to 1.0]\n'
    '- Neutrality (N): {n_gloss} [0.0 to 1.0]\n'
    '- Falsity (F): To what degree is this statement false? [0.0 to 1.0]\n\n'
    'Respond with ONLY this JSON: {{"T": <float>, "I": <float>, "N": <float>, "F": <float>}}'
)

# Las mismas tres glosas del estudio anterior, verbatim, para que los resultados
# sean comparables. La fuente no fija ninguna: por eso es un factor.
N_GLOSS = {
    "G1": "To what degree do you take no side on this statement, neither affirming nor "
          "denying it, independently of whether its truth value is knowable?",
    "G2": "To what degree does the predicate true-or-false simply not apply to this "
          "statement, so that assigning it a truth value would be a category error?",
    "G3": "To what degree do the grounds for and against this statement offset one "
          "another exactly, leaving a balanced position rather than a gap in knowledge?",
}

MAX_RETRIES = 4


def client() -> OpenAI:
    key = os.environ.get("OPENROUTER_API_KEY")
    if not key:
        sys.exit("OPENROUTER_API_KEY is not set.")
    return OpenAI(base_url="https://openrouter.ai/api/v1", api_key=key)


def call(cl, model_id, user):
    for attempt in range(MAX_RETRIES):
        try:
            r = cl.chat.completions.create(
                model=model_id,
                messages=[{"role": "system", "content": SYSTEM},
                          {"role": "user", "content": user}],
                temperature=1.0, max_tokens=200,
            )
            return (r.choices[0].message.content or "").strip()
        except Exception as exc:                       # noqa: BLE001
            if attempt == MAX_RETRIES - 1:
                return f"__ERROR__ {exc}"
            time.sleep(3.0 * (attempt + 1))
    return "__ERROR__ unreachable"


def parse(text: str):
    m = re.search(r"\{[^{}]*\}", text, re.S)
    if m:
        try:
            d = json.loads(m.group(0))
            v = [float(d[k]) for k in ("T", "I", "N", "F")]
            if all(0.0 <= x <= 1.0 for x in v):
                return tuple(v)
        except Exception:                              # noqa: BLE001
            pass
    got = {}
    for k in ("T", "I", "N", "F"):
        mm = re.search(rf'"?{k}"?\s*[:=]\s*([01](?:\.\d+)?|\.\d+)', text)
        if mm:
            got[k] = float(mm.group(1))
    return tuple(got[k] for k in ("T", "I", "N", "F")) if len(got) == 4 else None


def rung(T, I, N, F):
    if T + F > 1:
        return "strong"
    if T + F + I > 1 or T + F + N > 1:
        return "weak"
    if T + F + I + N > 1:
        return "very_weak"
    return "classical"


def done_keys():
    seen = set()
    if RAW.exists():
        with RAW.open(encoding="utf-8") as fh:
            for line in fh:
                try:
                    d = json.loads(line)
                    seen.add((d["model"], d["item_id"], d["gloss"]))
                except Exception:                      # noqa: BLE001
                    continue
    return seen


def main(a):
    items = json.loads((HERE / "items.json").read_text(encoding="utf-8"))
    if a.limit:
        items = items[:a.limit]
    total = len(items) * len(MODELS) * len(N_GLOSS)
    print(f"diseno: {len(items)} items x {len(MODELS)} modelos x {len(N_GLOSS)} glosas")
    print(f"TOTAL LLAMADAS = {total}")
    if a.count_only:
        return

    cl = client()
    seen = done_keys()
    print(f"reanudando: {len(seen)} llamadas ya registradas")

    n = 0
    for it, model, gk in itertools.product(items, MODELS, N_GLOSS):
        key = (model["label"], it["id"], gk)
        if key in seen:
            continue
        text = call(cl, model["id"], BASE.format(stmt=it["text"], n_gloss=N_GLOSS[gk]))
        v = parse(text)
        rec = {
            "model": model["label"], "vendor": model["vendor"],
            "item_id": it["id"], "pair": it["pair"],
            "phenomenon": it["phenomenon"], "form": it["form"],
            "statement": it["text"], "gloss": gk, "response": text,
            "T": v[0] if v else None, "I": v[1] if v else None,
            "N": v[2] if v else None, "F": v[3] if v else None,
            "rung": rung(*v) if v else None,
            "parsed": v is not None, "error": text.startswith("__ERROR__"),
        }
        if a.dry_run:
            print(json.dumps(rec, ensure_ascii=False)[:200])
        else:
            with RAW.open("a", encoding="utf-8") as fh:
                fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
        n += 1
        if n % 50 == 0:
            print(f"  {n}/{total} ...", flush=True)

    print(f"listo. llamadas en esta corrida: {n}. ANOTAR ESTE NUMERO EN EL PAPER.")


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--limit", type=int, default=None)
    p.add_argument("--count-only", action="store_true")
    p.add_argument("--dry-run", action="store_true")
    main(p.parse_args())

 succeeded in 3208ms:
{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Paradox (Logical)", "statement": "This sentence is false.", "gloss": "G1", "rep": 0, "response": "```json\n{\"T\": 0.0, \"I\": 1.0, \"N\": 0.5, \"F\": 0.0}\n```", "T": 0.0, "I": 1.0, "N": 0.5, "F": 0.0, "regime": "very_weak", "parsed": true, "error": false}
{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Paradox (Logical)", "statement": "This sentence is false.", "gloss": "G1", "rep": 1, "response": "```json\n{\"T\": 0.0, \"I\": 1.0, \"N\": 0.5, \"F\": 0.0}\n```", "T": 0.0, "I": 1.0, "N": 0.5, "F": 0.0, "regime": "very_weak", "parsed": true, "error": false}
{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Paradox (Logical)", "statement": "This sentence is false.", "gloss": "G1", "rep": 2, "response": "```json\n{\"T\": 0.0, \"I\": 1.0, \"N\": 0.5, \"F\": 0.0}\n```", "T": 0.0, "I": 1.0, "N": 0.5, "F": 0.0, "regime": "very_weak", "parsed": true, "error": false}
{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Paradox (Logical)", "statement": "This sentence is false.", "gloss": "G1", "rep": 3, "response": "```json\n{\"T\": 0.0, \"I\": 1.0, \"N\": 0.5, \"F\": 0.0}\n```", "T": 0.0, "I": 1.0, "N": 0.5, "F": 0.0, "regime": "very_weak", "parsed": true, "error": false}
{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Paradox (Logical)", "statement": "This sentence is false.", "gloss": "G1", "rep": 4, "response": "{\"T\": 0.0, \"I\": 1.0, \"N\": 0.5, \"F\": 0.0}", "T": 0.0, "I": 1.0, "N": 0.5, "F": 0.0, "regime": "very_weak", "parsed": true, "error": false}

 succeeded in 2962ms:
# Family I â€” epistemic states Â· provenance

**These generations were not collected for this paper.** They were collected for two companion
studies on a four-valued logic and are reproduced here so that this repository is self-contained
and every number in the paper can be checked without chasing a second repository.

Original repository, which is the citable source:
**[`mleyvaz/paraconsistent-signature-itembank`](https://github.com/mleyvaz/paraconsistent-signature-itembank)**

- Smarandache, F. & Leyva-VÃ¡zquez, M. Y. (2026). *Is the Ladder Measurable? Graded Paraconsistency
  Tested on Eight Statements and Then on a Bank.*
- Smarandache, F. & Leyva-VÃ¡zquez, M. Y. (2026). *One Item Is Not a Phenomenon: Separating Ethical
  Content from Syntactic Marking in Paraconsistent Signature Detection.*

If you are citing the epistemic-state bank itself, cite those. Cite this repository for the
methods paper and for Family II.

## What is here

| File | Elicitations | What it is |
|---|---|---|
| `results/raw_bank.jsonl` | 1,980 | the item bank, three wordings |
| `results/raw_quad_bank.jsonl` | 1,980 | the same bank, three repetitions |
| `results/raw_quadruple_pilot.jsonl` | 1,440 | the eight-statement pilot, ten repetitions |
| `results/raw_nolicense_system.jsonl` | 360 | ablation A â€” the permission sentence removed |
| `results/raw_neutral_system.jsonl` | 360 | ablation B â€” the framing removed |
| `items.json` | â€” | 110 items: ten per construct across five constructs, plus ten anchors |

Total 6,120. Each record carries the model, vendor, item, construct, elicitation form, the raw
response text, the parsed components and the derived label.

The elicitation and analysis scripts are copied alongside, unmodified, so the derived numbers can
be regenerated here. One file from the original repository is deliberately **not** reproduced:
`results/fig1_per_item.json`, a hand-made intermediate that no script produced. The figure that
consumed it now computes the same values from `raw_quad_bank.jsonl`, verified identical across all
five constructs â€” see `figures/make_fig1_between_items.py`.

## What is not here

The companion repository also carries the independent re-analysis script commissioned after an
adversarial audit, and the record of the claims that audit corrected. That material belongs to the
companion studies and is left where it is.

## Licence

CC BY 4.0, as released by the companion studies.

 succeeded in 2982ms:
"""Elicita la tripleta (T, I, F) sobre el banco de 110 items.

Usa el protocolo S1 del corpus v3 PALABRA POR PALABRA, para que los resultados
sean comparables con lo ya publicado. La condicion fuerte T+F>1 no contiene N,
asi que el cuadruple no aporta nada aqui y anadirlo introduciria la dependencia
de la glosa que ya documentamos.

Diseno: 110 items x 6 modelos x R repeticiones.  A R=3 son 1.980 llamadas.

Uso:
    set OPENROUTER_API_KEY=...
    python run_bank.py --count-only
    python run_bank.py --limit 4 --dry-run
    python run_bank.py
"""

from __future__ import annotations

import argparse
import itertools
import json
import os
import re
import sys
import time
from pathlib import Path

from openai import OpenAI

HERE = Path(__file__).resolve().parent
OUT = HERE / "results"
OUT.mkdir(exist_ok=True)
RAW = OUT / "raw_bank.jsonl"

MODELS = [
    {"id": "openai/gpt-4o", "label": "gpt-4o", "vendor": "openai"},
    {"id": "anthropic/claude-sonnet-4", "label": "claude-sonnet-4", "vendor": "anthropic"},
    {"id": "meta-llama/llama-4-maverick", "label": "llama-4-maverick", "vendor": "meta"},
    {"id": "deepseek/deepseek-chat", "label": "deepseek-chat", "vendor": "deepseek"},
    {"id": "qwen/qwen3-235b-a22b-2507", "label": "qwen3-235b", "vendor": "alibaba"},
    {"id": "mistralai/mistral-medium-3.1", "label": "mistral-medium-3.1", "vendor": "mistral"},
]

# Protocolo S1 del corpus v3, verbatim.
SYS = ("You are an expert in Neutrosophic Logic. You evaluate "
       "statements using three INDEPENDENT dimensions: Truth (T), "
       "Indeterminacy (I), and Falsity (F), each on [0.0, 1.0]. "
       "These dimensions are NOT constrained to sum to 1.0. A "
       "statement can be simultaneously partially true AND partially "
       "false AND partially indeterminate. Respond with ONLY a JSON "
       "object, no other text.")

USR = ('Evaluate this statement on three independent dimensions:\n\n'
       'Statement: "{stmt}"\n\n'
       '- Truth (T): To what degree is this statement true? [0.0 to 1.0]\n'
       '- Indeterminacy (I): To what degree is the truth value '
       'unknown, undetermined, or inherently uncertain? [0.0 to 1.0]\n'
       '- Falsity (F): To what degree is this statement false? '
       '[0.0 to 1.0]\n\n'
       'Respond with ONLY this JSON: {{"T": <float>, "I": <float>, "F": <float>}}')

MAX_RETRIES = 4


def client() -> OpenAI:
    key = os.environ.get("OPENROUTER_API_KEY")
    if not key:
        sys.exit("OPENROUTER_API_KEY is not set.")
    return OpenAI(base_url="https://openrouter.ai/api/v1", api_key=key)


def call(cl, model_id, stmt):
    for attempt in range(MAX_RETRIES):
        try:
            r = cl.chat.completions.create(
                model=model_id,
                messages=[{"role": "system", "content": SYS},
                          {"role": "user", "content": USR.format(stmt=stmt)}],
                temperature=1.0, max_tokens=150,
            )
            return (r.choices[0].message.content or "").strip()
        except Exception as exc:                       # noqa: BLE001
            if attempt == MAX_RETRIES - 1:
                return f"__ERROR__ {exc}"
            time.sleep(3.0 * (attempt + 1))
    return "__ERROR__ unreachable"


def parse(text: str):
    m = re.search(r"\{[^{}]*\}", text, re.S)
    if m:
        try:
            d = json.loads(m.group(0))
            v = [float(d[k]) for k in ("T", "I", "F")]
            if all(0.0 <= x <= 1.0 for x in v):
                return tuple(v)
        except Exception:                              # noqa: BLE001
            pass
    got = {}
    for k in ("T", "I", "F"):
        mm = re.search(rf'"?{k}"?\s*[:=]\s*([01](?:\.\d+)?|\.\d+)', text)
        if mm:
            got[k] = float(mm.group(1))
    return tuple(got[k] for k in ("T", "I", "F")) if len(got) == 3 else None


def done_keys():
    seen = set()
    if RAW.exists():
        with RAW.open(encoding="utf-8") as fh:
            for line in fh:
                try:
                    d = json.loads(line)
                    seen.add((d["model"], d["item_id"], d["rep"]))
                except Exception:                      # noqa: BLE001
                    continue
    return seen


def main(a):
    items = json.loads((HERE / "items.json").read_text(encoding="utf-8"))
    if a.limit:
        items = items[:a.limit]
    total = len(items) * len(MODELS) * a.reps
    print(f"diseno: {len(items)} items x {len(MODELS)} modelos x {a.reps} reps")
    print(f"TOTAL LLAMADAS = {total}")
    if a.count_only:
        return

    cl = client()
    seen = done_keys()
    print(f"reanudando: {len(seen)} llamadas ya registradas")

    n = 0
    for it, model, rep in itertools.product(items, MODELS, range(a.reps)):
        key = (model["label"], it["id"], rep)
        if key in seen:
            continue
        text = call(cl, model["id"], it["text"])
        v = parse(text)
        rec = {
            "model": model["label"], "vendor": model["vendor"],
            "item_id": it["id"], "pair": it["pair"],
            "phenomenon": it["phenomenon"], "form": it["form"],
            "statement": it["text"], "rep": rep, "response": text,
            "T": v[0] if v else None, "I": v[1] if v else None, "F": v[2] if v else None,
            "strong": (int(v[0] + v[2] > 1.0) if v else None),
            "parsed": v is not None, "error": text.startswith("__ERROR__"),
        }
        if a.dry_run:
            print(json.dumps(rec, ensure_ascii=False)[:200])
        else:
            with RAW.open("a", encoding="utf-8") as fh:
                fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
        n += 1
        if n % 50 == 0:
            print(f"  {n}/{total} ...", flush=True)

    print(f"listo. llamadas en esta corrida: {n}. ANOTAR ESTE NUMERO EN EL PAPER.")


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--reps", type=int, default=3)
    p.add_argument("--limit", type=int, default=None)
    p.add_argument("--count-only", action="store_true")
    p.add_argument("--dry-run", action="store_true")
    main(p.parse_args())

exec
"C:\\WINDOWS\\System32\\WindowsPowerShell\\v1.0\\powershell.exe" -Command "Get-Content -LiteralPath 'figures\\make_fig1_between_items.py'" in C:\Users\HP\Documents\MeasurementScience_Evals\paper11_elicitation_method
 succeeded in 3794ms:
"""Generador de fig1_between_items, tomado del paper companion.

El fichero original produce dos figuras; aqui solo se invoca la primera, que es la
unica que este paper usa. La segunda se deja en el fichero sin llamar para no
divergir del script publicado con el companion.

ORIGINAL: Las dos figuras del paper. Salida PDF vectorial para LaTeX.

  fig1_between_items.pdf  la dispersion entre items dentro de cada fenomeno,
                          con el valor del piloto de un solo enunciado marcado
  fig2_manipulation.pdf   las tres condiciones del system message, con IC del 95%

Paleta validada (dataviz, modo claro): serie 1 azul #2a78d6, serie 2 naranja #eb6834.
Ambos pasan banda de luminosidad, suelo de croma, separacion CVD y contraste.

Uso:  python make_figures.py
"""
from __future__ import annotations

import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

HERE = Path(__file__).resolve().parent
BANK = HERE.parent / "family1" / "results"
OUT  = HERE.parent / "paper"          # las figuras viven junto al .tex

BLUE = "#2a78d6"
ORANGE = "#eb6834"
INK = "#0b0b0b"
INK2 = "#52514e"
MUTED = "#8a8983"
SURFACE = "#ffffff"

plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["Times New Roman", "Nimbus Roman", "DejaVu Serif"],
    "font.size": 8,
    "axes.edgecolor": MUTED,
    "axes.linewidth": 0.6,
    "xtick.color": INK2,
    "ytick.color": INK2,
    "xtick.labelsize": 8,
    "ytick.labelsize": 8,
    "figure.facecolor": SURFACE,
    "axes.facecolor": SURFACE,
    "savefig.facecolor": SURFACE,
    "pdf.fonttype": 42,
})

LABEL = {
    "ethical": "Ethical conflict",
    "paradox": "Logical paradox",
    "vagueness": "Vagueness",
    "ignorance": "Epistemic ignorance",
    "contingency": "Future contingency",
}


def per_item_strong():
    """Tasa de la escala FUERTE por item, calculada del crudo.

    El script del companion leia aqui un intermedio, fig1_per_item.json, que ningun
    script producia. Se sustituye por el calculo, verificado identico en los cinco
    constructos: items bare de los cinco fenomenos contestados, fraccion de las 18
    elicitaciones por item (6 modelos x 3 glosas) clasificadas en la escala fuerte.
    """
    import pandas as pd
    rows = [json.loads(l) for l
            in (BANK / "raw_quad_bank.jsonl").read_text(encoding="utf-8").splitlines()
            if l.strip()]
    d = pd.DataFrame(rows)
    d = d[d["parsed"] & ~d["error"]].copy()
    for c in "TINF":
        d[c] = pd.to_numeric(d[c], errors="coerce")
    d = d.dropna(subset=list("TINF"))
    d = d[(d["form"] == "bare") & d["phenomenon"].isin(LABEL)]
    return {ph: sorted(g.assign(x=(g["rung"] == "strong").astype(int))
                       .groupby("item_id")["x"].mean().tolist())
            for ph, g in d.groupby("phenomenon")}


def fig1():
    """Dispersion entre items. Una serie, un color; el piloto va como anotacion."""
    per = per_item_strong()
    order = ["ethical", "paradox", "vagueness", "ignorance", "contingency"]

    fig, ax = plt.subplots(figsize=(3.35, 2.9))
    rng = np.random.default_rng(7)

    for i, ph in enumerate(order):
        v = np.array(per[ph])
        y = len(order) - 1 - i
        jit = rng.uniform(-0.13, 0.13, size=len(v))
        # media: barra vertical corta, recesiva
        ax.plot([v.mean(), v.mean()], [y - 0.28, y + 0.28],
                color=INK2, lw=1.4, solid_capstyle="butt", zorder=2)
        ax.scatter(v, y + jit, s=22, facecolor=BLUE, edgecolor=SURFACE,
                   linewidth=0.8, zorder=3, clip_on=False)

    # el enunciado unico del piloto: cae encima del item mas alto del banco
    ax.axvline(0.661, color=ORANGE, lw=1.4, ls=(0, (4, 2)), zorder=1)
    ax.annotate("the pilot's single sentence, 0.661,\n"
                "lands on the bank's highest item, 0.667",
                xy=(0.661, len(order) - 1 + 0.18), xytext=(0.16, len(order) - 0.16),
                color=ORANGE, fontsize=7, ha="left", va="top", linespacing=1.35,
                arrowprops=dict(arrowstyle="-", color=ORANGE, lw=0.7,
                                shrinkA=2, shrinkB=3,
                                connectionstyle="angle,angleA=0,angleB=90,rad=0"))

    ax.set_yticks(range(len(order)))
    ax.set_yticklabels([LABEL[p] for p in reversed(order)])
    ax.set_xlim(-0.02, 0.98)
    ax.set_ylim(-0.6, len(order) - 0.15)
    ax.set_xlabel("strong-rung rate, per item")
    ax.set_xticks([0, 0.2, 0.4, 0.6, 0.8])
    for side in ("top", "right", "left"):
        ax.spines[side].set_visible(False)
    ax.tick_params(axis="y", length=0)
    ax.grid(axis="x", color="#e8e7e3", lw=0.6, zorder=0)
    ax.set_axisbelow(True)

    fig.tight_layout(pad=0.3)
    fig.savefig(OUT / "fig1_between_items.pdf", bbox_inches="tight")
    plt.close(fig)
    print("fig1_between_items.pdf")


def wilson(k, n, z=1.96):
    p = k / n
    den = 1 + z * z / n
    c = (p + z * z / (2 * n)) / den
    h = z * np.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
    return max(0.0, c - h), min(1.0, c + h)


def fig2():
    """Tres condiciones del system message. Dos series por el tipo de pregunta."""
    # (etiqueta, k, n) por panel, en orden de presentacion
    panels = [
        ("All contested items", [("licensed", 23, 298), ("no licence", 17, 285),
                                 ("no framing", 1, 276)]),
        ("Ethical conflict only", [("licensed", 12, 60), ("no licence", 9, 58),
                                   ("no framing", 0, 51)]),
    ]

    fig, axes = plt.subplots(1, 2, figsize=(6.6, 2.0), sharex=True)
    for ax, (title, rows) in zip(axes, panels):
        for j, (lab, k, n) in enumerate(rows):
            y = len(rows) - 1 - j
            p = k / n
            lo, hi = wilson(k, n)
            same_question = lab != "no framing"
            col = BLUE if same_question else ORANGE
            ax.plot([lo, hi], [y, y], color=col, lw=2, solid_capstyle="butt", zorder=2)
            ax.scatter([p], [y], s=42, facecolor=col, edgecolor=SURFACE,
                       linewidth=1.0, zorder=3)
            ax.text(hi + 0.012, y, f"{p:.3f}", color=INK, fontsize=7.5,
                    va="center", ha="left")
        ax.set_yticks(range(len(rows)))
        ax.set_yticklabels([r[0] for r in reversed(rows)])
        ax.set_ylim(-0.55, len(rows) - 0.45)
        ax.set_xlim(-0.01, 0.40)
        ax.set_title(title, fontsize=8, color=INK, pad=6, loc="left")
        for side in ("top", "right", "left"):
            ax.spines[side].set_visible(False)
        ax.tick_params(axis="y", length=0)
        ax.grid(axis="x", color="#e8e7e3", lw=0.6, zorder=0)
        ax.set_axisbelow(True)
        ax.set_xlabel("strong-rung rate, 95% CI")

    # leyenda: la identidad no depende solo del color, y ademas va etiquetada en el eje
    h = [plt.Line2D([], [], color=BLUE, lw=2, marker="o", ms=5,
                    markeredgecolor=SURFACE, label="asks the neutrosophic question"),
         plt.Line2D([], [], color=ORANGE, lw=2, marker="o", ms=5,
                    markeredgecolor=SURFACE, label="does not")]
    axes[1].legend(handles=h, loc="lower right", frameon=False, fontsize=7,
                   handlelength=1.6, borderpad=0.2, labelspacing=0.3,
                   bbox_to_anchor=(1.0, -0.06))

    fig.tight_layout(pad=0.3)
    fig.savefig(OUT / "fig2_manipulation.pdf", bbox_inches="tight")
    plt.close(fig)
    print("fig2_manipulation.pdf")


if __name__ == "__main__":
    fig1()

codex
The figure scripts regenerate the plotted quantities from raw data rather than hidden intermediates. I did create generated outputs while running them; before I finish I’ll clean up the files this run changed so the review itself does not leave the repo altered.
exec
"C:\\WINDOWS\\System32\\WindowsPowerShell\\v1.0\\powershell.exe" -Command 'python family2/analyze_factual_v1.py' in C:\Users\HP\Documents\MeasurementScience_Evals\paper11_elicitation_method
 succeeded in 7463ms:
==========================================================================
BANCO FACTUAL - replica de las tres reglas en un dominio sin relacion
==========================================================================
condicion principal: 1080/1080 usables (0.0% fallo de parseo)

--- 1. MUESTREO DE ITEMS: SD entre items dentro de cada constructo ---
                  mean  sd_between  ratio    min    max   k
construct                                                  
wellknown_true   1.000       0.000  0.000  1.000  1.000  10
wellknown_false  0.000       0.000  0.000  0.000  0.000  10
obscure_true     0.983       0.037  0.038  0.889  1.000  10
obscure_false    0.000       0.000  0.000  0.000  0.000  10
unsettled        0.028       0.071  2.539  0.000  0.222  10

  mayor SD entre items: 0.071 (unsettled)
  con 1 item  -> semiancho IC95 = 0.138
  con 10 items-> semiancho IC95 = 0.044
  para +/-0.05 hacen falta k = 8 items
  constructos con SD >= media: 1 de 5

--- 2. INSTRUCCION: tres condiciones anidadas (solo W1, pareado) ---
  full       alta confianza 118/300 = 0.393 IC95 [0.340, 0.450]   anclas 0.500
  nolicense  alta confianza 122/300 = 0.407 IC95 [0.353, 0.463]   anclas 0.500
  neutral    alta confianza 121/300 = 0.403 IC95 [0.349, 0.460]   anclas 0.500

  alta confianza en 'unsettled' (donde deberia ser baja):
    full       0.017   confianza media 0.551
    nolicense  0.033   confianza media 0.531
    neutral    0.017   confianza media 0.533

--- 3. UMBRAL: grano de la rejilla ---
  valores distintos: 26 en 1080 elicitaciones
  multiplos de 0.05: 95.7%
  multiplos de 0.10: 86.4%
  valores mas frecuentes: 1.00(33%)  0.00(29%)  0.10(8%)  0.50(4%)  0.95(3%)  0.70(3%)
  confianza exactamente 0.90: 1.4%
  el corte 0.90 cae sobre la moda? moda = 1.00

  sensibilidad del corte, items de constructo:
    >= 0.85  ->  0.411
    >= 0.90  ->  0.402
    >= 0.95  ->  0.386
    >= 0.99  ->  0.339

--- 4. ACUERDO entre familias de modelos ---
  desacuerdo par a par entre modelos: 0.016 (n=150 unidades)
  desacuerdo del mismo modelo entre redacciones: 0.011 (n=900)
  ratio intra/inter: 0.69

--- BONUS: calibracion (solo donde hay verdad de referencia) ---
                 confidence  correct_dir
construct                               
obscure_false         0.012        0.988
obscure_true          0.978        0.978
wellknown_false       0.082        0.918
wellknown_true        0.999        0.999

exec
"C:\\WINDOWS\\System32\\WindowsPowerShell\\v1.0\\powershell.exe" -Command "python -c \"import json, pandas as pd, numpy as np, pathlib; p=pathlib.Path('family1/results/raw_quad_bank.jsonl'); d=pd.DataFrame([json.loads(l) for l in p.read_text(encoding='utf-8').splitlines() if l.strip()]); d=d[d['parsed'] & ~d['error']].copy();
for c in 'TINF': d[c]=pd.to_numeric(d[c], errors='coerce'); d=d.dropna(subset=list('TINF')); comps=d[list('TINF')].to_numpy().ravel(); tf=(d['T']+d['F']).to_numpy(); print('usable_rows', len(d), 'components', len(comps)); print('components_unique', len(np.unique(comps)), 'mult05', np.mean(np.abs(comps*20-np.round(comps*20))<1e-9), 'mult10', np.mean(np.abs(comps*10-np.round(comps*10))<1e-9)); print('tf_unique', len(np.unique(np.round(tf,10))), 'tf_eq_1', np.mean(np.abs(tf-1)<1e-9)); print('tf_modal', pd.Series(np.round(tf,10)).value_counts(normalize=True).head(6).to_dict()); anchors=d[d['form']=='anchor']; print('anchors n', len(anchors), 'strict_gt1', np.mean((anchors['T']+anchors['F'])>1), 'nonstrict_ge1', np.mean((anchors['T']+anchors['F'])>=1), 'eq1', np.mean(np.abs((anchors['T']+anchors['F'])-1)<1e-9)); print('contested strict', np.mean((d[d.form"'!='"'anchor']['T']+d[d.form"'!='"'anchor']['F'])>1), 'ge', np.mean((d[d.form"'!='"'anchor']['T']+d[d.form"'!='"'anchor']['F'])>=1))\"" in C:\Users\HP\Documents\MeasurementScience_Evals\paper11_elicitation_method
 succeeded in 7848ms:
usable_rows 1963 components 7852
components_unique 46 mult05 0.9769485481406012 mult10 0.8954406520631686
tf_unique 50 tf_eq_1 0.37850229240957717
tf_modal {1.0: 0.37850229240957717, 0.9: 0.12837493632195618, 0.8: 0.0728476821192053, 0.7: 0.06979113601630157, 1.1: 0.06775343861436577, 0.0: 0.06367804381049415}
anchors n 176 strict_gt1 0.0 nonstrict_ge1 0.7784090909090909 eq1 0.7784090909090909
contested strict 0.14885282596530497 ge 0.4879686625629547
usable_rows 1963 components 7852
components_unique 46 mult05 0.9769485481406012 mult10 0.8954406520631686
tf_unique 50 tf_eq_1 0.37850229240957717
tf_modal {1.0: 0.37850229240957717, 0.9: 0.12837493632195618, 0.8: 0.0728476821192053, 0.7: 0.06979113601630157, 1.1: 0.06775343861436577, 0.0: 0.06367804381049415}
anchors n 176 strict_gt1 0.0 nonstrict_ge1 0.7784090909090909 eq1 0.7784090909090909
contested strict 0.14885282596530497 ge 0.4879686625629547
usable_rows 1963 components 7852
components_unique 46 mult05 0.9769485481406012 mult10 0.8954406520631686
tf_unique 50 tf_eq_1 0.37850229240957717
tf_modal {1.0: 0.37850229240957717, 0.9: 0.12837493632195618, 0.8: 0.0728476821192053, 0.7: 0.06979113601630157, 1.1: 0.06775343861436577, 0.0: 0.06367804381049415}
anchors n 176 strict_gt1 0.0 nonstrict_ge1 0.7784090909090909 eq1 0.7784090909090909
contested strict 0.14885282596530497 ge 0.4879686625629547
usable_rows 1963 components 7852
components_unique 46 mult05 0.9769485481406012 mult10 0.8954406520631686
tf_unique 50 tf_eq_1 0.37850229240957717
tf_modal {1.0: 0.37850229240957717, 0.9: 0.12837493632195618, 0.8: 0.0728476821192053, 0.7: 0.06979113601630157, 1.1: 0.06775343861436577, 0.0: 0.06367804381049415}
anchors n 176 strict_gt1 0.0 nonstrict_ge1 0.7784090909090909 eq1 0.7784090909090909
contested strict 0.14885282596530497 ge 0.4879686625629547

exec
"C:\\WINDOWS\\System32\\WindowsPowerShell\\v1.0\\powershell.exe" -Command "python -c \"import json, pandas as pd, numpy as np, pathlib; d=pd.DataFrame([json.loads(l) for l in pathlib.Path('family1/results/raw_quad_bank.jsonl').read_text(encoding='utf-8').splitlines() if l.strip()]); d=d[d['parsed'] & ~d['error']].copy(); [d.__setitem__(c,pd.to_numeric(d[c],errors='coerce')) for c in 'TINF']; d=d.dropna(subset=list('TINF')); 
for c in 'TINF':
    top=pd.Series(d[c].to_numpy()).value_counts(normalize=True).head(5).sum(); print(c, round(float(top),3), pd.Series(d[c].to_numpy()).value_counts(normalize=True).head(5).to_dict())\"" in C:\Users\HP\Documents\MeasurementScience_Evals\paper11_elicitation_method
 succeeded in 7484ms:
<string>:1: ChainedAssignmentError: A value is being set on a copy of a DataFrame or Series through chained assignment.
Such chained assignment never works to update the original DataFrame or Series, because the intermediate object on which we are setting values always behaves as a copy (due to Copy-on-Write).

Try using '.loc[row_indexer, col_indexer] = value' instead, to perform the assignment in a single step.

See the documentation for a more detailed explanation: https://pandas.pydata.org/pandas-docs/stable/user_guide/copy_on_write.html#chained-assignment
T 0.644 {0.0: 0.1782985226693836, 0.7: 0.17116658176260827, 0.5: 0.11156393275598574, 0.4: 0.09169638308711156, 0.6: 0.0911869587366276}
I 0.576 {0.8: 0.1782985226693836, 0.3: 0.11971472236372899, 0.7: 0.11512990320937341, 0.6: 0.08863983698420784, 0.4: 0.0738665308201732}
N 0.75 {0.2: 0.19205298013245034, 0.3: 0.17727967396841568, 0.1: 0.14824248599083037, 0.0: 0.1360163015792155, 0.5: 0.09679062659195109}
F 0.658 {0.5: 0.1599592460519613, 0.4: 0.15180845644421803, 0.3: 0.13754457463066735, 0.0: 0.1293937850229241, 0.2: 0.07896077432501274}

exec
"C:\\WINDOWS\\System32\\WindowsPowerShell\\v1.0\\powershell.exe" -Command "python -c \"import json, pathlib, pandas as pd, numpy as np; d=pd.DataFrame([json.loads(l) for l in pathlib.Path('family1/results/raw_quad_bank.jsonl').read_text(encoding='utf-8').splitlines() if l.strip()]); d=d[d['parsed'] & ~d['error']].copy(); per=d[(d.form=='bare') & (d.phenomenon.isin(['ethical','ignorance','vagueness','contingency','paradox']))].assign(x=lambda x:(x.rung=='strong').astype(int)).groupby(['phenomenon','item_id'])['x'].mean().reset_index(); rng=np.random.default_rng(0);
def ci_diff(a,b,n=10000):
 a=np.array(a); b=np.array(b); draws=rng.choice(a,(n,len(a)),True).mean(1)-rng.choice(b,(n,len(b)),True).mean(1); return draws.mean(), np.percentile(draws,[2.5,97.5])
eth=per[per.phenomenon=='ethical'].x; non=per[per.phenomenon"'!='"'ethical'].x; par=per[per.phenomenon=='paradox'].x; print('means', eth.mean(), non.mean(), par.mean()); print('eth-vs-non', ci_diff(eth,non)); rng=np.random.default_rng(0); print('eth-vs-paradox', ci_diff(eth,par))\"" in C:\Users\HP\Documents\MeasurementScience_Evals\paper11_elicitation_method
 succeeded in 8649ms:
means 0.22222222222222224 0.04583333333333334 0.11666666666666667
eth-vs-non (np.float64(0.17702374999999998), array([0.05694444, 0.31388889]))
eth-vs-paradox (np.float64(0.10516777777777779), array([-0.06666667,  0.27222222]))

exec
"C:\\WINDOWS\\System32\\WindowsPowerShell\\v1.0\\powershell.exe" -Command "python -c \"import json, pathlib, pandas as pd, numpy as np
RES=pathlib.Path('family2/results')
def load(cond):
 d=pd.DataFrame([json.loads(l) for l in (RES/f'raw_factual_{cond}.jsonl').read_text(encoding='utf-8').splitlines() if l.strip()]); d=d[d.parsed & ~d.error].copy(); d['confidence']=pd.to_numeric(d.confidence, errors='coerce'); return d.dropna(subset=['confidence'])
D={c:load(c) for c in ['full','nolicense','neutral']}
rng=np.random.default_rng(0)
def boot_row(x,n=5000):
 x=np.asarray(x,float); draws=rng.choice(x,(n,len(x)),True).mean(1); return np.percentile(draws,[2.5,97.5])
def boot_item(df,col,n=5000):
 items=list(df.index.get_level_values('item_id').unique()); vals=[]; rr=np.random.default_rng(0)
 for _ in range(n):
  sample=rr.choice(items, len(items), True); vals.append(pd.concat([df.xs(i, level='item_id')[col] for i in sample]).mean())
 return np.percentile(vals,[2.5,97.5])
base=D['full'].query(\"wording=='W1' and construct=='unsettled'\").set_index(['item_id','model'])['confidence']
print('unsettled mean full', base.mean(), 'n', len(base), 'sd', base.std(ddof=1), 'eq50', (base==.5).sum())
for cond in ['nolicense','neutral']:
 o=D[cond].query(\"wording=='W1' and construct=='unsettled'\").set_index(['item_id','model'])['confidence']
 j=pd.concat([base.rename('full'),o.rename(cond)],axis=1).dropna(); j['diff']=j[cond]-j['full']; print(cond, 'mean', j[cond].mean(), 'delta', j['diff'].mean(), 'row_ci', boot_row(j['diff']), 'sd', j[cond].std(ddof=1), 'eq50', (j[cond]==.5).sum())
 df=j[['diff']]; print(cond, 'item_cluster_ci', boot_item(df,'diff'))
 # focal .5 paired binary diff
 jj=pd.DataFrame({'full':(j['full']==.5).astype(int), cond:(j[cond]==.5).astype(int)}); jj['diff']=jj[cond]-jj['full']; print(cond, 'eq50_delta', jj['diff'].mean(), 'eq50_row_ci', boot_row(jj['diff']), 'n', len(jj), 'fullcount', jj['full'].sum(), 'condcount', jj[cond].sum())
 print(cond, 'eq50_item_cluster_ci', boot_item(jj[['diff']], 'diff'))\"" in C:\Users\HP\Documents\MeasurementScience_Evals\paper11_elicitation_method
 exited 1 in 7794ms:
  File "<string>", line 14
    base=D['full'].query(
                        ^
SyntaxError: '(' was never closed

codex
The Family I item-clustered contrast does reproduce: ethical conflict minus the non-ethical constructs is about 0.177 with a bootstrap interval about `[0.057, 0.314]`, while ethical conflict minus logical paradox crosses zero. I’m now stress-testing the Family II ablation intervals under the clustering implied by the manuscript’s design rule.
exec
"C:\\WINDOWS\\System32\\WindowsPowerShell\\v1.0\\powershell.exe" -Command "python -c 'import json, pathlib, pandas as pd, numpy as np
RES=pathlib.Path(\"family2/results\")
def load(cond):
    d=pd.DataFrame([json.loads(l) for l in (RES/(\"raw_factual_\"+cond+\".jsonl\")).read_text(encoding=\"utf-8\").splitlines() if l.strip()])
    d=d[d.parsed & ~d.error].copy(); d[\"confidence\"]=pd.to_numeric(d.confidence, errors=\"coerce\")
    return d.dropna(subset=[\"confidence\"])
D={c:load(c) for c in [\"full\",\"nolicense\",\"neutral\"]}
def boot_row(x,n=5000,seed=0):
    rr=np.random.default_rng(seed); x=np.asarray(x,float); return np.percentile(rr.choice(x,(n,len(x)),True).mean(1),[2.5,97.5])
def boot_item(df,col,n=5000,seed=0):
    items=list(df.index.get_level_values(\"item_id\").unique()); vals=[]; rr=np.random.default_rng(seed)
    for _ in range(n):
        sample=rr.choice(items,len(items),True); vals.append(pd.concat([df.xs(i,level=\"item_id\")[col] for i in sample]).mean())
    return np.percentile(vals,[2.5,97.5])
base=D[\"full\"][(D[\"full\"].wording==\"W1\") & (D[\"full\"].construct==\"unsettled\")].set_index([\"item_id\",\"model\"])[\"confidence\"]
print(\"unsettled full\", \"mean\", round(base.mean(),3), \"n\", len(base), \"sd\", round(base.std(ddof=1),3), \"eq50\", int((base==.5).sum()))
for cond in [\"nolicense\",\"neutral\"]:
    o=D[cond][(D[cond].wording==\"W1\") & (D[cond].construct==\"unsettled\")].set_index([\"item_id\",\"model\"])[\"confidence\"]
    j=pd.concat([base.rename(\"full\"), o.rename(cond)], axis=1).dropna(); j[\"diff\"]=j[cond]-j[\"full\"]
    print(cond, \"mean\", round(j[cond].mean(),3), \"delta\", round(j[\"diff\"].mean(),3), \"row_ci\", np.round(boot_row(j[\"diff\"]),3).tolist(), \"item_ci\", np.round(boot_item(j[[\"diff\"]],\"diff\"),3).tolist(), \"sd\", round(j[cond].std(ddof=1),3), \"eq50\", int((j[cond]==.5).sum()))
    jj=pd.DataFrame({\"full\":(j[\"full\"]==.5).astype(int), cond:(j[cond]==.5).astype(int)}); jj[\"diff\"]=jj[cond]-jj[\"full\"]
    print(cond, \"eq50_delta\", round(jj[\"diff\"].mean(),3), \"eq50_row_ci\", np.round(boot_row(jj[\"diff\"]),3).tolist(), \"eq50_item_ci\", np.round(boot_item(jj[[\"diff\"]],\"diff\"),3).tolist(), \"fullcount\", int(jj[\"full\"].sum()), \"condcount\", int(jj[cond].sum()))'" in C:\Users\HP\Documents\MeasurementScience_Evals\paper11_elicitation_method
 exited 1 in 4362ms:
  File "<string>", line 4
    d=pd.DataFrame([json.loads(l) for l in (RES/(raw_factual_+cond+.jsonl)).read_text(encoding=utf-8).splitlines() if l.strip()])
                                                                   ^
SyntaxError: invalid syntax

codex
The quick `python -c` attempt hit PowerShell quoting, so I’m switching to a PowerShell here-string for the same read-only computation. The goal is just to compare row-level versus item-clustered intervals for the same paired differences.
exec
"C:\\WINDOWS\\System32\\WindowsPowerShell\\v1.0\\powershell.exe" -Command '$code = @'"'
import json, pathlib
import pandas as pd
import numpy as np

RES = pathlib.Path('family2/results')

def load(cond):
    p = RES / f'raw_factual_{cond}.jsonl'
    d = pd.DataFrame([json.loads(l) for l in p.read_text(encoding='utf-8').splitlines() if l.strip()])
    d = d[d.parsed & ~d.error].copy()
    d['confidence'] = pd.to_numeric(d.confidence, errors='coerce')
    return d.dropna(subset=['confidence'])

D = {c: load(c) for c in ['full', 'nolicense', 'neutral']}

def boot_row(x, n=5000, seed=0):
    rr = np.random.default_rng(seed)
    x = np.asarray(x, float)
    return np.percentile(rr.choice(x, (n, len(x)), True).mean(1), [2.5, 97.5])

def boot_item(df, col, n=5000, seed=0):
    items = list(df.index.get_level_values('item_id').unique())
    vals = []
    rr = np.random.default_rng(seed)
    for _ in range(n):
        sample = rr.choice(items, len(items), True)
        vals.append(pd.concat([df.xs(i, level='item_id')[col] for i in sample]).mean())
    return np.percentile(vals, [2.5, 97.5])

base = D['full'][(D['full'].wording == 'W1') & (D['full'].construct == 'unsettled')].set_index(['item_id', 'model'])['confidence']
print('unsettled full', 'mean', round(base.mean(), 3), 'n', len(base), 'sd', round(base.std(ddof=1), 3), 'eq50', int((base == .5).sum()))
for cond in ['nolicense', 'neutral']:
    o = D[cond][(D[cond].wording == 'W1') & (D[cond].construct == 'unsettled')].set_index(['item_id', 'model'])['confidence']
    j = pd.concat([base.rename('full'), o.rename(cond)], axis=1).dropna()
    j['diff'] = j[cond] - j['full']
    print(cond, 'mean', round(j[cond].mean(), 3), 'delta', round(j['diff'].mean(), 3), 'row_ci', np.round(boot_row(j['diff']), 3).tolist(), 'item_ci', np.round(boot_item(j[['diff']], 'diff'), 3).tolist(), 'sd', round(j[cond].std(ddof=1), 3), 'eq50', int((j[cond] == .5).sum()))
    jj = pd.DataFrame({'full': (j['full'] == .5).astype(int), cond: (j[cond] == .5).astype(int)})
    jj['diff'] = jj[cond] - jj['full']
    print(cond, 'eq50_delta', round(jj['diff'].mean(), 3), 'eq50_row_ci', np.round(boot_row(jj['diff']), 3).tolist(), 'eq50_item_ci', np.round(boot_item(jj[['diff']], 'diff'), 3).tolist(), 'fullcount', int(jj['full'].sum()), 'condcount', int(jj[cond].sum()))
'@
python -c "'$code' in C:\Users\HP\Documents\MeasurementScience_Evals\paper11_elicitation_method
codex
The item-clustered bootstrap is slower because it is resampling full item clusters rather than flat rows. I’m letting that finish rather than falling back to the manuscript’s faster row-level calculation, since the resampling unit is one of the requested review targets.
 succeeded in 70155ms:
unsettled full mean 0.551 n 60 sd 0.161 eq50 17
nolicense mean 0.531 delta -0.02 row_ci [-0.057, 0.013] item_ci [-0.051, 0.01] sd 0.219 eq50 9
nolicense eq50_delta -0.133 eq50_row_ci [-0.267, 0.0] eq50_item_ci [-0.233, -0.033] fullcount 17 condcount 9
neutral mean 0.533 delta -0.018 row_ci [-0.052, 0.016] item_ci [-0.045, 0.008] sd 0.195 eq50 9
neutral eq50_delta -0.133 eq50_row_ci [-0.217, -0.05] eq50_item_ci [-0.217, -0.067] fullcount 17 condcount 9

codex
One concrete mismatch is now clear: the Family I ablation table’s “all items” row is computed on contested items only. Including the anchor rows gives different rates and Wilson intervals, so the table label is not what the released script computes.
exec
"C:\\WINDOWS\\System32\\WindowsPowerShell\\v1.0\\powershell.exe" -Command '$code = @'"'
import json, pathlib
import pandas as pd
import numpy as np

RES = pathlib.Path('family1/results')
CONT = ['ethical', 'ignorance', 'vagueness', 'contingency', 'paradox']

def load(path):
    d = pd.DataFrame([json.loads(l) for l in path.read_text(encoding='utf-8').splitlines() if l.strip()])
    d = d[d.parsed & ~d.error].copy()
    for c in 'TINF':
        d[c] = pd.to_numeric(d[c], errors='coerce')
    d = d.dropna(subset=list('TINF'))
    return d

def wilson(k, n, z=1.96):
    p = k/n
    den = 1 + z*z/n
    c = (p + z*z/(2*n))/den
    h = z*np.sqrt(p*(1-p)/n + z*z/(4*n*n))/den
    return c-h, c+h

conds = {
    'full': load(RES/'raw_quad_bank.jsonl').query(\"gloss == 'G1' and form in ['bare','anchor']\"),
    'nolicense': load(RES/'raw_nolicense_system.jsonl'),
    'neutral': load(RES/'raw_neutral_system.jsonl'),
}
for name, d in conds.items():
    for label, subset in [('contested_only', d[d.phenomenon.isin(CONT)]), ('including_anchors', d)]:
        k = int((subset.rung == 'strong').sum())
        n = len(subset)
        lo, hi = wilson(k, n)
        print(name, label, f'{k}/{n}', f'{k/n:.3f}', f'[{lo:.3f},{hi:.3f}]')
'@
python -c "'$code' in C:\Users\HP\Documents\MeasurementScience_Evals\paper11_elicitation_method
 exited 1 in 3416ms:
  File "<string>", line 24
    'full': load(RES/'raw_quad_bank.jsonl').query(gloss
                                                 ^
SyntaxError: '(' was never closed

codex
That command hit the same nested-quote problem in the filter expression. I’m rerunning it without pandas query strings so the evidence is clean.
exec
"C:\\WINDOWS\\System32\\WindowsPowerShell\\v1.0\\powershell.exe" -Command '$code = @'"'
import json, pathlib
import pandas as pd
import numpy as np

RES = pathlib.Path('family1/results')
CONT = ['ethical', 'ignorance', 'vagueness', 'contingency', 'paradox']

def load(path):
    d = pd.DataFrame([json.loads(l) for l in path.read_text(encoding='utf-8').splitlines() if l.strip()])
    d = d[d.parsed & ~d.error].copy()
    for c in 'TINF':
        d[c] = pd.to_numeric(d[c], errors='coerce')
    d = d.dropna(subset=list('TINF'))
    return d

def wilson(k, n, z=1.96):
    p = k/n
    den = 1 + z*z/n
    c = (p + z*z/(2*n))/den
    h = z*np.sqrt(p*(1-p)/n + z*z/(4*n*n))/den
    return c-h, c+h

full0 = load(RES/'raw_quad_bank.jsonl')
full = full0[(full0.gloss == 'G1') & (full0.form.isin(['bare', 'anchor']))]
conds = {
    'full': full,
    'nolicense': load(RES/'raw_nolicense_system.jsonl'),
    'neutral': load(RES/'raw_neutral_system.jsonl'),
}
for name, d in conds.items():
    for label, subset in [('contested_only', d[d.phenomenon.isin(CONT)]), ('including_anchors', d)]:
        k = int((subset.rung == 'strong').sum())
        n = len(subset)
        lo, hi = wilson(k, n)
        print(name, label, str(k)+'/'+str(n), f'{k/n:.3f}', f'[{lo:.3f},{hi:.3f}]')
'@
python -c "'$code' in C:\Users\HP\Documents\MeasurementScience_Evals\paper11_elicitation_method
 succeeded in 6554ms:
full contested_only 23/298 0.077 [0.052,0.113]
full including_anchors 23/358 0.064 [0.043,0.095]
nolicense contested_only 17/285 0.060 [0.038,0.093]
nolicense including_anchors 17/337 0.050 [0.032,0.079]
neutral contested_only 1/276 0.004 [0.001,0.020]
neutral including_anchors 1/333 0.003 [0.001,0.017]

exec
"C:\\WINDOWS\\System32\\WindowsPowerShell\\v1.0\\powershell.exe" -Command "Get-Content -LiteralPath 'paper\\refs.bib'" in C:\Users\HP\Documents\MeasurementScience_Evals\paper11_elicitation_method
exec
"C:\\WINDOWS\\System32\\WindowsPowerShell\\v1.0\\powershell.exe" -Command 'python validity/analyze_classification.py' in C:\Users\HP\Documents\MeasurementScience_Evals\paper11_elicitation_method
exec
"C:\\WINDOWS\\System32\\WindowsPowerShell\\v1.0\\powershell.exe" -Command 'rg -n "citep|citet|cite" paper/main.tex paper/section_replication.tex paper/refs.bib' in C:\Users\HP\Documents\MeasurementScience_Evals\paper11_elicitation_method
 succeeded in 3612ms:
% Paper 11 -- metodo de elicitacion. Entradas verificadas 26-ago-2026.

@article{protocolsens2026,
  title   = {Same Answer, Different Confidence: Protocol Sensitivity in {LLM}
             Confidence Calibration},
  author  = {Kim, Hankyeol and Kang, Pilsung},
  journal = {arXiv preprint arXiv:2605.27752},
  year    = {2026},
  url     = {https://arxiv.org/abs/2605.27752}
}

@article{coinflip2026,
  title   = {The Coin Flip Judge? Reliability and Bias in {LLM}-as-a-Judge Evaluation},
  author  = {Yagubyan, Abel},
  journal = {arXiv preprint arXiv:2606.13685},
  year    = {2026},
  url     = {https://arxiv.org/abs/2606.13685}
}

@article{farquhar2024,
  title   = {Detecting hallucinations in large language models using semantic entropy},
  author  = {Farquhar, Sebastian and Kossen, Jannik and Kuhn, Lorenz and Gal, Yarin},
  journal = {Nature},
  volume  = {630}, pages = {625--630},
  year    = {2024},
  doi     = {10.1038/s41586-024-07421-0}
}

@inproceedings{manakul2023,
  title     = {{SelfCheckGPT}: Zero-Resource Black-Box Hallucination Detection for
               Generative Large Language Models},
  author    = {Manakul, Potsawee and Liusie, Adian and Gales, Mark J. F.},
  booktitle = {Proceedings of EMNLP 2023},
  pages     = {9004--9017},
  year      = {2023}
}

@article{fleiss1971,
  title   = {Measuring nominal scale agreement among many raters},
  author  = {Fleiss, Joseph L.},
  journal = {Psychological Bulletin},
  volume  = {76}, number = {5}, pages = {378--382},
  year    = {1971},
  doi     = {10.1037/h0031619}
}

@book{cronbach1972,
  title     = {The Dependability of Behavioral Measurements: Theory of Generalizability
               for Scores and Profiles},
  author    = {Cronbach, Lee J. and Gleser, Goldine C. and Nanda, Harinder and
               Rajaratnam, Nageswari},
  publisher = {Wiley},
  address   = {New York},
  year      = {1972}
}

% --- los dos estudios de los que salen los datos de este paper ---
@misc{leyva2026ladder,
  title  = {Is the Ladder Measurable? Graded Paraconsistency Tested on Eight Statements
            and Then on a Bank},
  author = {Smarandache, Florentin and Leyva-V{\'a}zquez, Maikel Y.},
  year   = {2026},
  note   = {Submitted to the AAAI 2026 Fall Symposium Series.}
}

@misc{leyva2026itembank,
  title  = {One Item Is Not a Phenomenon: Separating Ethical Content from Syntactic
            Marking in Paraconsistent Signature Detection},
  author = {Smarandache, Florentin and Leyva-V{\'a}zquez, Maikel Y.},
  year   = {2026},
  note   = {Submitted to the AAAI 2026 Fall Symposium Series. Item bank and generations
            released under CC BY 4.0.}
}

@misc{leyva2026protocol,
  title  = {The Protocol Is the Measurement: Elicitation Format Dominates Model Identity
            in Epistemic-State Probing},
  author = {Leyva-V{\'a}zquez, Maikel Y.},
  year   = {2026},
  note   = {Submitted to the AAAI 2026 Fall Symposium Series.}
}

@article{smarandache2026ladder,
  title   = {({T}, {I}, {N}, {F}) Neutrosophic Weak and Strong Paraconsistency and the
             Epistemics of Artificial Intelligence},  title   = {Intraclass correlations: Uses in assessing rater reliability},
  author  = {Shrout, Patrick E. and Fleiss, Joseph L.},
  journal = {Psychological Bulletin},
  volume  = {86}, number = {2}, pages = {420--428},
  year    = {1979},
  doi     = {10.1037/0033-2909.86.2.420}
}

% ---------------------------------------------------------------------------
% Confianza verbalizada y jueces LLM
% ---------------------------------------------------------------------------
@article{lin2022teaching,
  title   = {Teaching Models to Express Their Uncertainty in Words},
  author  = {Lin, Stephanie and Hilton, Jacob and Evans, Owain},
  journal = {Transactions on Machine Learning Research},
  year    = {2022},
  url     = {https://openreview.net/forum?id=8s8K2UZGTZ}
}

@inproceedings{zheng2023judging,
  title     = {Judging {LLM}-as-a-Judge with {MT}-Bench and Chatbot Arena},
  author    = {Zheng, Lianmin and Chiang, Wei-Lin and Sheng, Ying and Zhuang, Siyuan
               and Wu, Zhanghao and Zhuang, Yonghao and Lin, Zi and Li, Zhuohan
               and Li, Dacheng and Xing, Eric P. and Zhang, Hao and Gonzalez, Joseph E.
               and Stoica, Ion},
  booktitle = {Advances in Neural Information Processing Systems 36 (NeurIPS),
               Datasets and Benchmarks Track},
  year      = {2023}
}

% ---------------------------------------------------------------------------
% Sensibilidad al formato del prompt
% ---------------------------------------------------------------------------
@inproceedings{sclar2024quantifying,
  title     = {Quantifying Language Models' Sensitivity to Spurious Features in
               Prompt Design or: How I learned to start worrying about prompt
               formatting},
  author    = {Sclar, Melanie and Choi, Yejin and Tsvetkov, Yulia and Suhr, Alane},
  booktitle = {The Twelfth International Conference on Learning Representations (ICLR)},
  year      = {2024}
}

% ---------------------------------------------------------------------------
% Psicometria aplicada a benchmarks
% ---------------------------------------------------------------------------
@inproceedings{rodriguez2021evaluation,
  title     = {Evaluation Examples Are Not Equally Informative: How Should That
               Change {NLP} Leaderboards?},
  author    = {Rodriguez, Pedro and Barrow, Joe and Hoyle, Alexander Miserlis and
               Lalor, John P. and Jia, Robin and Boyd-Graber, Jordan},
  booktitle = {Proceedings of the 59th Annual Meeting of the Association for
               Computational Linguistics (ACL-IJCNLP)},
  pages     = {4486--4503},
  year      = {2021},
  url       = {https://aclanthology.org/2021.acl-long.346/}
}

@inproceedings{vania2021comparing,
  title     = {Comparing Test Sets with Item Response Theory},
  author    = {Vania, Clara and Htut, Phu Mon and Huang, William and Mungra, Dhara
               and Pang, Richard Yuanzhe and Phang, Jason and Liu, Haokun and
               Cho, Kyunghyun and Bowman, Samuel R.},
  booktitle = {Proceedings of the 59th Annual Meeting of the Association for
               Computational Linguistics (ACL-IJCNLP)},
  pages     = {1141--1158},
  year      = {2021},
  url       = {https://aclanthology.org/2021.acl-long.92/}
}

% ---------------------------------------------------------------------------
% Estadistica de las evaluaciones y estado del benchmarking
% ---------------------------------------------------------------------------
@article{miller2024errorbars,
  title   = {Adding Error Bars to Evals: A Statistical Approach to Language Model
             Evaluations},
  author  = {Miller, Evan},
  journal = {arXiv preprint arXiv:2411.00640},
  year    = {2024},
  url     = {https://arxiv.org/abs/2411.00640}
}

@inproceedings{bowmandahl2021,
  title     = {What Will it Take to Fix Benchmarking in Natural Language
               Understanding?},
  author    = {Bowman, Samuel R. and Dahl, George E.},
  booktitle = {Proceedings of the 2021 Conference of the North American Chapter of
               the Association for Computational Linguistics (NAACL-HLT)},
  pages     = {4843--4855},
  year      = {2021},
  url       = {https://aclanthology.org/2021.naacl-main.385/}
}


 succeeded in 3326ms:
faltan hojas rellenas: rater_A, rater_B
El instrumento esta listo; esto se corre cuando vuelvan.

 succeeded in 3781ms:
paper/section_replication.tex:5:the elicited design rather than of that subject matter, they should reappear in a task that
paper/section_replication.tex:10:is the most ordinary elicited evaluation there is, and the quantity that the calibration
paper/section_replication.tex:88:it}. For an exotic elicited construct that is everything. For a familiar one it is close to
paper/main.tex:16:\title{Three Ways an Elicited Evaluation Measures Its Own Design\\
paper/main.tex:60:design are everywhere: verbalized confidence \citep{lin2022teaching}, self-reported
paper/main.tex:61:uncertainty, LLM-as-judge scoring \citep{zheng2023judging}, self-critique,
paper/main.tex:65:usually requires is a concern raised both inside NLP \citep{bowmandahl2021} and from
paper/main.tex:66:measurement theory \citep{jacobs2021measurement}. The design has three failure modes that
paper/main.tex:75:\citep{leyva2026ladder, leyva2026itembank}. That study's subject matter is not the subject
paper/main.tex:79:about the logic should read those papers. Readers who run elicited evaluations should find
paper/main.tex:83:ordinary elicited question there is---how confident are you that this statement is
paper/main.tex:96:\paragraph{What is not new.} That elicitation format moves elicited confidence is established
paper/main.tex:97:\citep{protocolsens2026}, as is the unreliability of LLM judges \citep{coinflip2026}; that
paper/main.tex:98:prompt formatting alone moves accuracy by many points \citep{sclar2024quantifying}; that
paper/main.tex:99:few-item instruments are imprecise is elementary psychometrics \citep{cronbach1972}; and that evaluation results deserve intervals is argued directly for
paper/main.tex:100:language models by \citet{miller2024errorbars}. What we
paper/main.tex:137:unrelated task in the same elicited form: ten statements for each of five constructs---well-known
paper/main.tex:145:items, which is the form almost every elicited evaluation takes. In Family~II we report the
paper/main.tex:163:to NLP leaderboards and test sets \citep{rodriguez2021evaluation, vania2021comparing};
paper/main.tex:206:\citep{leyva2026ladder}. Measured over ten items the same quantity is $0.222$, and the per-item
paper/main.tex:223:Elicited evaluations carry an instruction that explains what is being asked. The instruction is
paper/main.tex:293:Language models do not report continuous numbers. Across $7{,}852$ elicited components in this
paper/main.tex:305:long-standing result in psychological methods \citep{maccallum2002}; what is specific here
paper/main.tex:323:One further quantity is worth separating because it is routinely misread \citep{cohen1960, shroutfleiss1979}. Studies that use
paper/main.tex:332:own. The pooled coefficient over the bank, $\kappa = 0.184$ \citep{fleiss1971}, should be read
paper/main.tex:364:one of construct validity \citep{cronbachmeehl1955, messick1995}, and it arrives here in
paper/main.tex:365:the form measurement theory gives it for computational systems \citep{jacobs2021measurement}. The honest answer is that we do, and that the assignment has not
paper/main.tex:387:commercial language model through a programmatic interface, elicited by prompts written by the
paper/main.tex:411:\url{https://github.com/mleyvaz/elicited-evaluation-design}. Every figure and table here is

exec
"C:\\WINDOWS\\System32\\WindowsPowerShell\\v1.0\\powershell.exe" -Command '$code = @'"'
import re, pathlib
bib = pathlib.Path('paper/refs.bib').read_text(encoding='utf-8')
keys = re.findall(r'@\\w+\\{(["'^,]+),'"', bib)
tex = pathlib.Path('paper/main.tex').read_text(encoding='utf-8') + '\\n' + pathlib.Path('paper/section_replication.tex').read_text(encoding='utf-8')
used = set()
for m in re.finditer(r'\\\\cite[tp]?\\{(["'^}]+)'"\\}', tex):
    for k in m.group(1).split(','):
        used.add(k.strip())
print('bib entries', len(keys), keys)
print('used', len(used), sorted(used))
print('unused', sorted(set(keys)-used))
print('missing', sorted(used-set(keys)))
'@
python -c "'$code' in C:\Users\HP\Documents\MeasurementScience_Evals\paper11_elicitation_method
 succeeded in 3605ms:
bib entries 23 ['protocolsens2026', 'coinflip2026', 'farquhar2024', 'manakul2023', 'fleiss1971', 'cronbach1972', 'leyva2026ladder', 'leyva2026itembank', 'leyva2026protocol', 'smarandache2026ladder', 'jacobs2021measurement', 'cronbachmeehl1955', 'messick1995', 'maccallum2002', 'cohen1960', 'shroutfleiss1979', 'lin2022teaching', 'zheng2023judging', 'sclar2024quantifying', 'rodriguez2021evaluation', 'vania2021comparing', 'miller2024errorbars', 'bowmandahl2021']
used 19 ['bowmandahl2021', 'cohen1960', 'coinflip2026', 'cronbach1972', 'cronbachmeehl1955', 'fleiss1971', 'jacobs2021measurement', 'leyva2026itembank', 'leyva2026ladder', 'lin2022teaching', 'maccallum2002', 'messick1995', 'miller2024errorbars', 'protocolsens2026', 'rodriguez2021evaluation', 'sclar2024quantifying', 'shroutfleiss1979', 'vania2021comparing', 'zheng2023judging']
unused ['farquhar2024', 'leyva2026protocol', 'manakul2023', 'smarandache2026ladder']
missing []

web search: 
web search: "Same Answer, Different Confidence" "Protocol Sensitivity" arXiv 2605.27752
web search: 
web search: https://arxiv.org/abs/2605.27752
web search: 
web search: "A coefficient of agreement for nominal scales" Cohen 1960 DOI
web search: 
web search: "Quantifying Language Models' Sensitivity to Spurious Features" Sclar Choi Tsvetkov Suhr ICLR 2024
web search: 
web search: https://aclanthology.org/2021.acl-long.92/
web search: 
web search: "Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena" Zheng Chiang Sheng Zhuang Wu 2023
web search: 
web search: https://aclanthology.org/2021.acl-long.346/
web search: 
web search: "On the practice of dichotomization of quantitative variables" "Psychological Methods" "19" "40"
web search: 
web search: 'Pages:' in https://aclanthology.org/2021.naacl-main.385/
codex
The agreement section reports κ and two disagreement percentages without uncertainty. I’m recomputing those from the pilot and bank and adding bootstrap intervals so I can distinguish “not reported” from “not estimable.”
exec
"C:\\WINDOWS\\System32\\WindowsPowerShell\\v1.0\\powershell.exe" -Command '$code = @'"'
import json, pathlib
from itertools import combinations
import pandas as pd
import numpy as np

# Pilot disagreement percentages
p = pathlib.Path('family1/results/raw_quadruple_pilot.jsonl')
pilot = pd.DataFrame([json.loads(l) for l in p.read_text(encoding='utf-8').splitlines() if l.strip()])
pilot = pilot[pilot.parsed & ~pilot.error].copy()
label_col = 'regime'
within = []
within_groups = []
for key, g in pilot.groupby(['phenomenon','statement','gloss','model']):
    labs = list(g.sort_values('rep')[label_col])
    vals = [a "'!= b for a, b in combinations(labs, 2)]
    within.extend(vals)
    within_groups.append((key, np.mean(vals)))
between = []
between_groups = []
for key, g in pilot.groupby(['"'phenomenon','statement','gloss','rep']):
    vals_by_model = g.set_index('model')[label_col]
    vals = [vals_by_model[a] "'!= vals_by_model[b] for a, b in combinations(vals_by_model.index, 2)]
    between.extend(vals)
    between_groups.append((key, np.mean(vals)))

def boot_means(group_vals, n=5000, seed=0):
    rr = np.random.default_rng(seed)
    v = np.asarray([x[1] for x in group_vals], float)
    return np.percentile(rr.choice(v, (n, len(v)), True).mean(1), [2.5, 97.5])
print('"'pilot raw', len(pilot), 'within', len(within), np.mean(within), np.round(boot_means(within_groups),3).tolist(), 'between', len(between), np.mean(between), np.round(boot_means(between_groups),3).tolist())

# Fleiss kappa and bootstrap CI over item_id/gloss units from raw_quad_bank.
def fleiss(piv):
    piv = piv.dropna()
    cats = sorted(set(piv.values.ravel()))
    n = piv.shape[1]
    cnt = np.array([[list(r).count(c) for c in cats] for r in piv.values])
    P = ((cnt**2).sum(1)-n)/(n*(n-1))
    pj = cnt.sum(0)/(len(piv)*n)
    pe = (pj**2).sum()
    return float((P.mean()-pe)/(1-pe)) if pe < 1 else np.nan
q = pd.DataFrame([json.loads(l) for l in pathlib.Path('family1/results/raw_quad_bank.jsonl').read_text(encoding='utf-8').splitlines() if l.strip()])
q = q[q.parsed & ~q.error].copy()
q = q[q.phenomenon.isin(['ethical','ignorance','vagueness','contingency','paradox'])]
piv = q.pivot_table(index=['item_id','gloss'], columns='model', values='rung', aggfunc='first').dropna()
print('kappa', fleiss(piv), 'n_units', len(piv))
rr = np.random.default_rng(1)
vals = []
for _ in range(2000):
    idx = rr.choice(np.arange(len(piv)), len(piv), True)
    vals.append(fleiss(piv.iloc[idx]))
print('kappa_unit_boot_ci', np.round(np.percentile(vals, [2.5, 97.5]), 3).tolist())
# item-cluster by item_id, preserving all available gloss rows per item
items = list(piv.reset_index().item_id.unique())
vals = []
reset = piv.reset_index()
for _ in range(2000):
    sample = rr.choice(items, len(items), True)
    sample_df = pd.concat([reset[reset.item_id == it] for it in sample], ignore_index=True)
    vals.append(fleiss(sample_df.set_index(['item_id','gloss']).drop(columns=[])))
print('kappa_item_boot_ci', np.round(np.percentile(vals, [2.5, 97.5]), 3).tolist())
'@
python -c "'$code' in C:\Users\HP\Documents\MeasurementScience_Evals\paper11_elicitation_method
codex
The agreement bootstrap is still running; it is resampling κ over the bank units and the repeat/model disagreement rates over pilot units. I’ll use it only if it finishes cleanly, otherwise I’ll report the missing-interval problem from the released script itself.
codex
The slow part is item-clustered κ, not the raw κ. Since the manuscript reports κ without any interval, even a unit bootstrap would be enough to show the omission is avoidable; I’m waiting one more cycle rather than starting a second competing process.
codex
This process is slower than expected but still doing bounded bootstrap work, so I’m not leaving it running in the background. After it exits I’ll move to line-specific evidence and cleanup.
codex
The κ bootstrap process is taking too long for what should be a supporting calculation. I’m interrupting it and will rerun a smaller, simpler interval computation that does not risk stalling the review.
 exited 1 in 148184ms:
codex
I interrupted the stalled process cleanly. I’m rerunning the same check with fewer bootstrap draws and a vectorized κ calculation so it stays bounded.
exec
"C:\\WINDOWS\\System32\\WindowsPowerShell\\v1.0\\powershell.exe" -Command '$code = @'"'
import json, pathlib
from itertools import combinations
import pandas as pd
import numpy as np

def ci(v, seed=0, B=1000):
    rr = np.random.default_rng(seed)
    v = np.asarray(v, float)
    return np.percentile(rr.choice(v, (B, len(v)), True).mean(1), [2.5, 97.5])

pilot = pd.DataFrame([json.loads(l) for l in pathlib.Path('family1/results/raw_quadruple_pilot.jsonl').read_text(encoding='utf-8').splitlines() if l.strip()])
pilot = pilot[pilot.parsed & ~pilot.error].copy()
within_group_means = []
for _, g in pilot.groupby(['phenomenon','statement','gloss','model']):
    labs = list(g.sort_values('rep').regime)
    within_group_means.append(np.mean([a "'!= b for a, b in combinations(labs, 2)]))
between_group_means = []
for _, g in pilot.groupby(['"'phenomenon','statement','gloss','rep']):
    labs = list(g.set_index('model').regime)
    between_group_means.append(np.mean([a "'!= b for a, b in combinations(labs, 2)]))
print('"'within_mean', round(float(np.mean(within_group_means)), 3), 'ci', np.round(ci(within_group_means), 3).tolist(), flush=True)
print('between_mean', round(float(np.mean(between_group_means)), 3), 'ci', np.round(ci(between_group_means), 3).tolist(), flush=True)

q = pd.DataFrame([json.loads(l) for l in pathlib.Path('family1/results/raw_quad_bank.jsonl').read_text(encoding='utf-8').splitlines() if l.strip()])
q = q[q.parsed & ~q.error].copy()
q = q[q.phenomenon.isin(['ethical','ignorance','vagueness','contingency','paradox'])]
piv = q.pivot_table(index=['item_id','gloss'], columns='model', values='rung', aggfunc='first').dropna()
labels, arr = np.unique(piv.to_numpy().ravel(), return_inverse=True)
arr = arr.reshape(piv.shape)

def fleiss_arr(a):
    m, n = a.shape
    cnt = np.zeros((m, len(labels)), dtype=float)
    for j in range(len(labels)):
        cnt[:, j] = (a == j).sum(axis=1)
    P = ((cnt ** 2).sum(axis=1) - n) / (n * (n - 1))
    pj = cnt.sum(axis=0) / (m * n)
    pe = (pj ** 2).sum()
    return (P.mean() - pe) / (1 - pe)
rr = np.random.default_rng(1)
unit_vals = [fleiss_arr(arr[rr.choice(arr.shape[0], arr.shape[0], True), :]) for _ in range(1000)]
print('kappa', round(float(fleiss_arr(arr)), 3), 'n_units', arr.shape[0], 'unit_ci', np.round(np.percentile(unit_vals, [2.5, 97.5]), 3).tolist(), flush=True)
'@
python -u -c "'$code' in C:\Users\HP\Documents\MeasurementScience_Evals\paper11_elicitation_method
 succeeded in 8625ms:
within_mean 0.123 ci [0.09, 0.158]
between_mean 0.227 ci [0.195, 0.263]
kappa 0.184 n_units 287 unit_ci [0.149, 0.216]

exec
"C:\\WINDOWS\\System32\\WindowsPowerShell\\v1.0\\powershell.exe" -Command "rg -n \"17\\.5|33\\.4|0\\.175|0\\.334|disagree|desacuerdo|kappa|Fleiss|raw_quadruple_pilot|pilot\" ." in C:\Users\HP\Documents\MeasurementScience_Evals\paper11_elicitation_method
 succeeded in 1981ms:
.\figures\make_fig1_between_items.py:10:                          con el valor del piloto de un solo enunciado marcado
.\figures\make_fig1_between_items.py:88:    """Dispersion entre items. Una serie, un color; el piloto va como anotacion."""
.\figures\make_fig1_between_items.py:105:    # el enunciado unico del piloto: cae encima del item mas alto del banco
.\figures\make_fig1_between_items.py:107:    ax.annotate("the pilot's single sentence, 0.661,\n"
.\family2\analyze_factual.py:183:    print(f"  desacuerdo medio par a par entre modelos: {np.mean(inter):.3f} (n={len(piv)})")
.\family2\analyze_factual.py:188:    print(f"  desacuerdo del mismo modelo entre redacciones: {np.mean(intra):.3f} (n={len(intra)})")
.\family2\analyze_factual_v1.py:137:    print(f"  desacuerdo par a par entre modelos: {np.mean(inter):.3f} (n={len(piv)} unidades)")
.\family2\analyze_factual_v1.py:142:    print(f"  desacuerdo del mismo modelo entre redacciones: {np.mean(intra):.3f} (n={len(intra)})")
.\README.md:43:merely cautionary. A fourth, shorter section separates inter-model disagreement from single-model
.\validity\analyze_classification.py:6:  1. Cohen kappa entre los dos clasificadores        -> es reproducible la asignacion?
.\validity\analyze_classification.py:45:def kappa(a, b, cats):
.\validity\analyze_classification.py:46:    """Cohen kappa sobre las etiquetas emparejadas."""
.\validity\analyze_classification.py:81:    print(f"   Cohen kappa         {kappa(la, lb, ORDER):.3f}")
.\validity\analyze_classification.py:86:              f"kappa {kappa(l, lg, ORDER):.3f}")
.\validity\analyze_classification.py:123:    print(f"other at kappa = {kappa(la, lb, ORDER):.3f} and reproduced the bank's assignment at")
.\validity\analyze_classification.py:124:    print(f"kappa = {kappa(la, lg, ORDER):.3f} and {kappa(lb, lg, ORDER):.3f}.")
.\review\ADVERSARIAL_PROMPT.md:52:that errors, or whose output disagrees with the manuscript.
.\review\codex_review.md:65:that errors, or whose output disagrees with the manuscript.
.\review\codex_review.md:685:"C:\\WINDOWS\\System32\\WindowsPowerShell\\v1.0\\powershell.exe" -Command "rg -n \"7920|7,920|standard deviation|standard deviations|SD|\\\\pm|±|0\\.41|0\\.05|factor|16|0\\.000|0\\.778|delta|bootstrap|kappa|κ|Cohen|Wilson|shape|location|n=60|60 per cell|threshold|ablation|instruction\" paper/main.tex paper/section_replication.tex paper/main_ipm.tex paper/main_nlp.tex" in C:\Users\HP\Documents\MeasurementScience_Evals\paper11_elicitation_method
.\review\codex_review.md:733:paper/main_ipm.tex:260:\paragraph{Why one ablation is not enough.} The two conditions disagree, and either alone would
.\review\codex_review.md:742:paper/main_ipm.tex:322:own. The pooled coefficient over the bank, $\kappa = 0.184$ \citep{fleiss1971}, should be read
.\review\codex_review.md:831:paper/main_nlp.tex:258:\paragraph{Why one ablation is not enough.} The two conditions disagree, and either alone would
.\review\codex_review.md:840:paper/main_nlp.tex:320:own. The pooled coefficient over the bank, $\kappa = 0.184$ \citep{fleiss1971}, should be read
.\review\codex_review.md:893:paper/main.tex:270:\paragraph{Why one ablation is not enough.} The two conditions disagree, and either alone would
.\review\codex_review.md:902:paper/main.tex:332:own. The pooled coefficient over the bank, $\kappa = 0.184$ \citep{fleiss1971}, should be read
.\review\codex_review.md:975:family1\results\raw_quadruple_pilot.jsonl
.\review\codex_review.md:1173:    print(f"  desacuerdo medio par a par entre modelos: {np.mean(inter):.3f} (n={len(piv)})")
.\review\codex_review.md:1178:    print(f"  desacuerdo del mismo modelo entre redacciones: {np.mean(intra):.3f} (n={len(intra)})")
.\review\codex_review.md:1335:    print(f"  Fleiss kappa = {k:.3f}  (n = {n} unidades)   acuerdo bruto = {np.mean(agr):.3f}")
.\review\codex_review.md:1336:    print("  (con 8 items el estudio previo reporto kappa = 0.358 agregado)")
.\review\codex_review.md:1371:questions, where models spread from $0.42$ to $0.74$ across items and disagree with each other by
.\review\codex_review.md:1500:model disagreement is not model disagreement.
.\review\codex_review.md:1787:\paragraph{Why one ablation is not enough.} The two conditions disagree, and either alone would
.\review\codex_review.md:1794:Report both. If they disagree, the effect lives between them, and the paper's claim must be
.\review\codex_review.md:1842:per cell at a non-zero temperature, such a coefficient cannot distinguish models disagreeing
.\review\codex_review.md:1845:Our corpus contains a design that separates them, because the pilot has ten repetitions. Within
.\review\codex_review.md:1847:labels $17.5\%$ of the time; two different models disagree $33.4\%$ of the time. Roughly half of
.\review\codex_review.md:1848:the disagreement attributed to raters is stochastic variation a single rater produces on its
.\review\codex_review.md:1849:own. The pooled coefficient over the bank, $\kappa = 0.184$ \citep{fleiss1971}, should be read
.\review\codex_review.md:1850:as a bound on reproducibility rather than as a measure of inter-model disagreement.
.\review\codex_review.md:1871:for the first and third results is estimated from the pilot rather than measured in the bank.
.\review\codex_review.md:2030:ignorance    0.175   0.102 -0.073
.\review\codex_review.md:2036:  Fleiss kappa = 0.184  (n = 287 unidades)   acuerdo bruto = 0.647
.\review\codex_review.md:2037:  (con 8 items el estudio previo reporto kappa = 0.358 agregado)
.\review\codex_review.md:2105:  desacuerdo medio par a par entre modelos: 0.048 (n=150)
.\review\codex_review.md:2106:  desacuerdo del mismo modelo entre redacciones: 0.021 (n=900)
.\review\codex_review.md:2120:Both requested scripts execute. Their output already matches several headline claims, but there are two warning signs: the factual script’s own docstring contains stale values that disagree with its output, and the replication prose says “factor of nearly seventy” where the printed factual range is 1 to 20 items within that bank. I’m checking whether those are manuscript defects or only code comments/prose imprecision.
.\review\codex_review.md:2995:"C:\\WINDOWS\\System32\\WindowsPowerShell\\v1.0\\powershell.exe" -Command "(Get-Content -LiteralPath 'family1\\results\\raw_quadruple_pilot.jsonl' | Measure-Object -Line).Lines" in C:\Users\HP\Documents\MeasurementScience_Evals\paper11_elicitation_method
.\review\codex_review.md:3080:figures\make_fig1_between_items.py:88:    """Dispersion entre items. Una serie, un color; el piloto va como anotacion."""
.\review\codex_review.md:3108:family1\analyze_quad_bank.py:142:    print("  (con 8 items el estudio previo reporto kappa = 0.358 agregado)")
.\review\codex_review.md:3348:paper\section_replication.tex:25:questions, where models spread from $0.42$ to $0.74$ across items and disagree with each other by
.\review\codex_review.md:3443:"C:\\WINDOWS\\System32\\WindowsPowerShell\\v1.0\\powershell.exe" -Command "Get-Content -LiteralPath 'family1\\results\\raw_quadruple_pilot.jsonl' -TotalCount 5" in C:\Users\HP\Documents\MeasurementScience_Evals\paper11_elicitation_method
.\review\codex_review.md:3678:| `results/raw_quadruple_pilot.jsonl` | 1,440 | the eight-statement pilot, ten repetitions |
.\review\codex_review.md:3884:                          con el valor del piloto de un solo enunciado marcado
.\review\codex_review.md:3962:    """Dispersion entre items. Una serie, un color; el piloto va como anotacion."""
.\review\codex_review.md:3979:    # el enunciado unico del piloto: cae encima del item mas alto del banco
.\review\codex_review.md:3981:    ax.annotate("the pilot's single sentence, 0.661,\n"
.\review\codex_review.md:4118:  desacuerdo par a par entre modelos: 0.016 (n=150 unidades)
.\review\codex_review.md:4119:  desacuerdo del mismo modelo entre redacciones: 0.011 (n=900)
.\review\codex_review.md:4439:  author  = {Fleiss, Joseph L.},
.\review\codex_review.md:4485:  author  = {Shrout, Patrick E. and Fleiss, Joseph L.},
.\review\codex_review.md:4606:paper/main.tex:332:own. The pooled coefficient over the bank, $\kappa = 0.184$ \citep{fleiss1971}, should be read
.\review\codex_review.md:4653:The agreement section reports κ and two disagreement percentages without uncertainty. I’m recomputing those from the pilot and bank and adding bootstrap intervals so I can distinguish “not reported” from “not estimable.”
.\review\codex_review.md:4661:# Pilot disagreement percentages
.\review\codex_review.md:4662:p = pathlib.Path('family1/results/raw_quadruple_pilot.jsonl')
.\review\codex_review.md:4663:pilot = pd.DataFrame([json.loads(l) for l in p.read_text(encoding='utf-8').splitlines() if l.strip()])
.\review\codex_review.md:4664:pilot = pilot[pilot.parsed & ~pilot.error].copy()
.\review\codex_review.md:4668:for key, g in pilot.groupby(['phenomenon','statement','gloss','model']):
.\review\codex_review.md:4675:for key, g in pilot.groupby(['"'phenomenon','statement','gloss','rep']):
.\review\codex_review.md:4685:print('"'pilot raw', len(pilot), 'within', len(within), np.mean(within), np.round(boot_means(within_groups),3).tolist(), 'between', len(between), np.mean(between), np.round(boot_means(between_groups),3).tolist())
.\review\codex_review.md:4687:# Fleiss kappa and bootstrap CI over item_id/gloss units from raw_quad_bank.
.\review\codex_review.md:4701:print('kappa', fleiss(piv), 'n_units', len(piv))
.\review\codex_review.md:4707:print('kappa_unit_boot_ci', np.round(np.percentile(vals, [2.5, 97.5]), 3).tolist())
.\review\codex_review.md:4716:print('kappa_item_boot_ci', np.round(np.percentile(vals, [2.5, 97.5]), 3).tolist())
.\review\codex_review.md:4720:The agreement bootstrap is still running; it is resampling κ over the bank units and the repeat/model disagreement rates over pilot units. I’ll use it only if it finishes cleanly, otherwise I’ll report the missing-interval problem from the released script itself.
.\review\codex_review.md:4742:pilot = pd.DataFrame([json.loads(l) for l in pathlib.Path('family1/results/raw_quadruple_pilot.jsonl').read_text(encoding='utf-8').splitlines() if l.strip()])
.\review\codex_review.md:4743:pilot = pilot[pilot.parsed & ~pilot.error].copy()
.\review\codex_review.md:4745:for _, g in pilot.groupby(['phenomenon','statement','gloss','model']):
.\review\codex_review.md:4749:for _, g in pilot.groupby(['"'phenomenon','statement','gloss','rep']):
.\review\codex_review.md:4773:print('kappa', round(float(fleiss_arr(arr)), 3), 'n_units', arr.shape[0], 'unit_ci', np.round(np.percentile(unit_vals, [2.5, 97.5]), 3).tolist(), flush=True)
.\review\codex_review.md:4779:kappa 0.184 n_units 287 unit_ci [0.149, 0.216]
.\review\codex_review.md:4782:"C:\\WINDOWS\\System32\\WindowsPowerShell\\v1.0\\powershell.exe" -Command "rg -n \"17\\.5|33\\.4|0\\.175|0\\.334|disagree|desacuerdo|kappa|Fleiss|raw_quadruple_pilot|pilot\" ." in C:\Users\HP\Documents\MeasurementScience_Evals\paper11_elicitation_method
.\validity\build_classification_task.py:51:| **EC** | Ethical conflict | competent people hold opposed moral views about it, and the disagreement is about values rather than about facts |
.\validity\build_classification_task.py:108:   whether competent people disagree, not whether you personally find it obvious.
.\family1\analyze_quad_bank.py:141:    print(f"  Fleiss kappa = {k:.3f}  (n = {n} unidades)   acuerdo bruto = {np.mean(agr):.3f}")
.\family1\analyze_quad_bank.py:142:    print("  (con 8 items el estudio previo reporto kappa = 0.358 agregado)")
.\paper\main.tex:270:\paragraph{Why one ablation is not enough.} The two conditions disagree, and either alone would
.\paper\main.tex:277:Report both. If they disagree, the effect lives between them, and the paper's claim must be
.\paper\main.tex:325:per cell at a non-zero temperature, such a coefficient cannot distinguish models disagreeing
.\paper\main.tex:328:Our corpus contains a design that separates them, because the pilot has ten repetitions. Within
.\paper\main.tex:330:labels $17.5\%$ of the time; two different models disagree $33.4\%$ of the time. Roughly half of
.\paper\main.tex:331:the disagreement attributed to raters is stochastic variation a single rater produces on its
.\paper\main.tex:332:own. The pooled coefficient over the bank, $\kappa = 0.184$ \citep{fleiss1971}, should be read
.\paper\main.tex:333:as a bound on reproducibility rather than as a measure of inter-model disagreement.
.\paper\main.tex:356:for the first and third results is estimated from the pilot rather than measured in the bank.
.\validity\classification\INSTRUCTIONS.md:15:| **EC** | Ethical conflict | competent people hold opposed moral views about it, and the disagreement is about values rather than about facts |
.\validity\classification\INSTRUCTIONS.md:27:   whether competent people disagree, not whether you personally find it obvious.
.\family1\README.md:24:| `results/raw_quadruple_pilot.jsonl` | 1,440 | the eight-statement pilot, ten repetitions |
.\paper\main_ipm.tex:260:\paragraph{Why one ablation is not enough.} The two conditions disagree, and either alone would
.\paper\main_ipm.tex:267:Report both. If they disagree, the effect lives between them, and the paper's claim must be
.\paper\main_ipm.tex:315:per cell at a non-zero temperature, such a coefficient cannot distinguish models disagreeing
.\paper\main_ipm.tex:318:Our corpus contains a design that separates them, because the pilot has ten repetitions. Within
.\paper\main_ipm.tex:320:labels $17.5\%$ of the time; two different models disagree $33.4\%$ of the time. Roughly half of
.\paper\main_ipm.tex:321:the disagreement attributed to raters is stochastic variation a single rater produces on its
.\paper\main_ipm.tex:322:own. The pooled coefficient over the bank, $\kappa = 0.184$ \citep{fleiss1971}, should be read
.\paper\main_ipm.tex:323:as a bound on reproducibility rather than as a measure of inter-model disagreement.
.\paper\main_ipm.tex:346:for the first and third results is estimated from the pilot rather than measured in the bank.
.\paper\main_nlp.tex:258:\paragraph{Why one ablation is not enough.} The two conditions disagree, and either alone would
.\paper\main_nlp.tex:265:Report both. If they disagree, the effect lives between them, and the paper's claim must be
.\paper\main_nlp.tex:313:per cell at a non-zero temperature, such a coefficient cannot distinguish models disagreeing
.\paper\main_nlp.tex:316:Our corpus contains a design that separates them, because the pilot has ten repetitions. Within
.\paper\main_nlp.tex:318:labels $17.5\%$ of the time; two different models disagree $33.4\%$ of the time. Roughly half of
.\paper\main_nlp.tex:319:the disagreement attributed to raters is stochastic variation a single rater produces on its
.\paper\main_nlp.tex:320:own. The pooled coefficient over the bank, $\kappa = 0.184$ \citep{fleiss1971}, should be read
.\paper\main_nlp.tex:321:as a bound on reproducibility rather than as a measure of inter-model disagreement.
.\paper\main_nlp.tex:344:for the first and third results is estimated from the pilot rather than measured in the bank.
.\paper\refs.bib:40:  author  = {Fleiss, Joseph L.},
.\paper\refs.bib:153:  author  = {Shrout, Patrick E. and Fleiss, Joseph L.},
.\paper\section_replication.tex:25:questions, where models spread from $0.42$ to $0.74$ across items and disagree with each other by
.\paper\section_replication.tex:154:model disagreement is not model disagreement.

exec
"C:\\WINDOWS\\System32\\WindowsPowerShell\\v1.0\\powershell.exe" -Command '$code = @'"'
import json, pathlib
from itertools import combinations
import pandas as pd
import numpy as np
pilot = pd.DataFrame([json.loads(l) for l in pathlib.Path('family1/results/raw_quadruple_pilot.jsonl').read_text(encoding='utf-8').splitlines() if l.strip()])
pilot = pilot[pilot.parsed & ~pilot.error].copy()
for label_name, series in [('regime', pilot.regime), ('strong_binary', (pilot.T + pilot.F > 1.0).map({True:'strong', False:'not'})), ('weak_or_more', ((pilot.T + pilot.F + pilot.I > 1.0) | (pilot.T + pilot.F + pilot.N > 1.0)).map({True:'nonclassical', False:'classical'}))]:
    pilot['_lab'] = series.values
    within = []
    for _, g in pilot.groupby(['phenomenon','statement','gloss','model']):
        labs = list(g.sort_values('rep')._lab)
        within.extend([a "'!= b for a, b in combinations(labs, 2)])
    between = []
    for _, g in pilot.groupby(['"'phenomenon','statement','gloss','rep']):
        labs = list(g.set_index('model')._lab)
        between.extend([a "'!= b for a, b in combinations(labs, 2)])
    print(label_name, '"'within_flat', round(float(np.mean(within)),3), 'between_flat', round(float(np.mean(between)),3), 'within_pairs', len(within), 'between_pairs', len(between))
'@
python -c "'$code' in C:\Users\HP\Documents\MeasurementScience_Evals\paper11_elicitation_method
 exited 1 in 9504ms:
Traceback (most recent call last):
  File "C:\Python314\Lib\site-packages\pandas\core\ops\array_ops.py", line 220, in _na_arithmetic_op
    result = func(left, right)
  File "C:\Python314\Lib\site-packages\pandas\core\computation\expressions.py", line 243, in evaluate
    return _evaluate(op, op_str, left_op, right_op)  # type: ignore[misc]
  File "C:\Python314\Lib\site-packages\pandas\core\computation\expressions.py", line 74, in _evaluate_standard
    return op(left_op, right_op)
TypeError: can only concatenate str (not "float") to str

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "<string>", line 7, in <module>
    for label_name, series in [('regime', pilot.regime), ('strong_binary', (pilot.T + pilot.F > 1.0).map({True:'strong', False:'not'})), ('weak_or_more', ((pilot.T + pilot.F + pilot.I > 1.0) | (pilot.T + pilot.F + pilot.N > 1.0)).map({True:'nonclassical', False:'classical'}))]:
                                                                            ~~~~~~~~^~~~~~~~~
  File "C:\Python314\Lib\site-packages\pandas\core\ops\common.py", line 85, in new_method
    return method(self, other)
  File "C:\Python314\Lib\site-packages\pandas\core\arraylike.py", line 190, in __add__
    return self._arith_method(other, operator.add)
           ~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^
  File "C:\Python314\Lib\site-packages\pandas\core\frame.py", line 9139, in _arith_method
    new_data = self._dispatch_frame_op(other, op, axis=axis)
  File "C:\Python314\Lib\site-packages\pandas\core\frame.py", line 9182, in _dispatch_frame_op
    bm = self._mgr.operate_blockwise(
        right._mgr,
        array_op,
    )
  File "C:\Python314\Lib\site-packages\pandas\core\internals\managers.py", line 1683, in operate_blockwise
    return operate_blockwise(self, other, array_op)
  File "C:\Python314\Lib\site-packages\pandas\core\internals\ops.py", line 65, in operate_blockwise
    res_values = array_op(lvals, rvals)
  File "C:\Python314\Lib\site-packages\pandas\core\ops\array_ops.py", line 289, in arithmetic_op
    res_values = _na_arithmetic_op(left, right, op)  # type: ignore[arg-type]
  File "C:\Python314\Lib\site-packages\pandas\core\ops\array_ops.py", line 229, in _na_arithmetic_op
    result = _masked_arith_op(left, right, op)
  File "C:\Python314\Lib\site-packages\pandas\core\ops\array_ops.py", line 165, in _masked_arith_op
    result[mask] = op(xrav[mask], yrav[mask])
                   ~~^^^^^^^^^^^^^^^^^^^^^^^^
TypeError: can only concatenate str (not "float") to str

codex
The pilot check found a real mismatch: using the released pilot labels, repeat and inter-model disagreement are 0.123 and 0.227, not the manuscript’s 0.175 and 0.334. I’m checking alternate binary definitions before treating that as final, because the prose just says “labels” and the pilot file names the column `regime`.
exec
"C:\\WINDOWS\\System32\\WindowsPowerShell\\v1.0\\powershell.exe" -Command '$code = @'"'
import json, pathlib
from itertools import combinations
import pandas as pd
import numpy as np
pilot = pd.DataFrame([json.loads(l) for l in pathlib.Path('family1/results/raw_quadruple_pilot.jsonl').read_text(encoding='utf-8').splitlines() if l.strip()])
pilot = pilot[pilot.parsed & ~pilot.error].copy()
for c in 'TINF':
    pilot[c] = pd.to_numeric(pilot[c], errors='coerce')
pilot = pilot.dropna(subset=list('TINF'))
labels = {
    'regime': pilot['regime'],
    'strong_binary': ((pilot['T'] + pilot['F']) > 1.0).map({True:'strong', False:'not'}),
    'classical_binary': (pilot['regime'] == 'classical').map({True:'classical', False:'nonclassical'}),
}
for label_name, series in labels.items():
    pilot['_lab'] = series.values
    within = []
    for _, g in pilot.groupby(['phenomenon','statement','gloss','model']):
        labs = list(g.sort_values('rep')['_lab'])
        within.extend([a "'!= b for a, b in combinations(labs, 2)])
    between = []
    for _, g in pilot.groupby(['"'phenomenon','statement','gloss','rep']):
        labs = list(g.set_index('model')['_lab'])
        between.extend([a "'!= b for a, b in combinations(labs, 2)])
    print(label_name, '"'within_flat', round(float(np.mean(within)),3), 'between_flat', round(float(np.mean(between)),3), 'within_pairs', len(within), 'between_pairs', len(between))
'@
python -c "'$code' in C:\Users\HP\Documents\MeasurementScience_Evals\paper11_elicitation_method
 succeeded in 11008ms:
regime within_flat 0.123 between_flat 0.234 within_pairs 6330 between_pairs 3455
strong_binary within_flat 0.034 between_flat 0.04 within_pairs 6330 between_pairs 3455
classical_binary within_flat 0.045 between_flat 0.085 within_pairs 6330 between_pairs 3455

exec
"C:\\WINDOWS\\System32\\WindowsPowerShell\\v1.0\\powershell.exe" -Command '$code = @'"'
import json, pathlib
from itertools import combinations
import pandas as pd
import numpy as np
for fname, label_col in [('raw_bank.jsonl','strong'), ('raw_quad_bank.jsonl','rung')]:
    d = pd.DataFrame([json.loads(l) for l in pathlib.Path('family1/results/'+fname).read_text(encoding='utf-8').splitlines() if l.strip()])
    d = d[d.parsed & ~d.error].copy()
    if fname == 'raw_bank.jsonl':
        # three reps; compare labels across reps and models
        d['_lab'] = d['strong'].astype(str)
        within=[]
        for _, g in d.groupby(['item_id','model']):
            labs=list(g.sort_values('rep')['_lab'])
            within.extend([a"'!=b for a,b in combinations(labs,2)])
        between=[]
        for _, g in d.groupby(['"'item_id','rep']):
            labs=list(g.set_index('model')['_lab'])
            between.extend([a"'!=b for a,b in combinations(labs,2)])
        print(fname, '"'within', round(float(np.mean(within)),3), len(within), 'between', round(float(np.mean(between)),3), len(between))
    else:
        # no reps; compare models on rung
        d['_lab'] = d['rung']
        between=[]
        for _, g in d.groupby(['item_id','gloss']):
            labs=list(g.set_index('model')['_lab'])
            between.extend([a"'!=b for a,b in combinations(labs,2)])
        print(fname, '"'between', round(float(np.mean(between)),3), len(between))
'@
python -c "'$code' in C:\Users\HP\Documents\MeasurementScience_Evals\paper11_elicitation_method
codex
The alternate label definitions still do not recover 17.5% or 33.4%. I’m checking whether those numbers came from the older three-component repeated bank rather than from the pilot the manuscript names.
 succeeded in 15825ms:
raw_bank.jsonl within 0.076 1980 between 0.188 4950
raw_quad_bank.jsonl between 0.34 4865

codex
The 33.4% appears to come from model disagreement in the full `raw_quad_bank.jsonl`, not the pilot. The manuscript says both quantities are from the pilot design, so I’m separating two defects: source misattribution and a non-reproducible 17.5% repeat-disagreement number.
exec
"C:\\WINDOWS\\System32\\WindowsPowerShell\\v1.0\\powershell.exe" -Command '$code = @'"'
import json, pathlib
from itertools import combinations
import pandas as pd
import numpy as np
raw = pd.DataFrame([json.loads(l) for l in pathlib.Path('family1/results/raw_quadruple_pilot.jsonl').read_text(encoding='utf-8').splitlines() if l.strip()])
for mode in ['parsed_only','include_fail_as_label']:
    d = raw.copy()
    if mode == 'parsed_only':
        d = d[d.parsed & ~d.error].copy()
        d['_lab'] = d['regime']
    else:
        d['_lab'] = np.where(d.parsed & ~d.error, d['regime'], 'parse_fail')
    within=[]
    sizes=[]
    for _, g in d.groupby(['phenomenon','statement','gloss','model']):
        labs=list(g.sort_values('rep')['_lab'])
        sizes.append(len(labs))
        within.extend([a"'!=b for a,b in combinations(labs,2)])
    between=[]
    for _, g in d.groupby(['"'phenomenon','statement','gloss','rep']):
        labs=list(g.set_index('model')['_lab'])
        between.extend([a"'!=b for a,b in combinations(labs,2)])
    print(mode, '"'rows', len(d), 'group_sizes', sorted(set(sizes)), 'within', round(float(np.mean(within)),3), len(within), 'between', round(float(np.mean(between)),3), len(between))
'@
python -c "'$code' in C:\Users\HP\Documents\MeasurementScience_Evals\paper11_elicitation_method
 succeeded in 6425ms:
parsed_only rows 1411 group_sizes [3, 9, 10] within 0.123 6330 between 0.234 3455
include_fail_as_label rows 1440 group_sizes [10] within 0.126 6480 between 0.265 3600

codex
Including parse failures as their own label still gives repeat disagreement around 12.6%, not 17.5%. I’m checking whether 17.5% could be “numeric vector changed” rather than “label changed”; if so the prose says the wrong outcome.
exec
"C:\\WINDOWS\\System32\\WindowsPowerShell\\v1.0\\powershell.exe" -Command '$code = @'"'
import json, pathlib
from itertools import combinations
import pandas as pd
import numpy as np
raw = pd.DataFrame([json.loads(l) for l in pathlib.Path('family1/results/raw_quadruple_pilot.jsonl').read_text(encoding='utf-8').splitlines() if l.strip()])
d = raw[raw.parsed & ~raw.error].copy()
for c in 'TINF':
    d[c] = pd.to_numeric(d[c], errors='coerce')
d = d.dropna(subset=list('TINF'))
for outcome in ['regime','vector','tf_sum','sum4']:
    diffs=[]
    for _, g in d.groupby(['phenomenon','statement','gloss','model']):
        g=g.sort_values('rep')
        if outcome == 'regime': vals=list(g['regime'])
        elif outcome == 'vector': vals=[tuple(row) for row in g[list('TINF')].round(12).to_numpy()]
        elif outcome == 'tf_sum': vals=list((g['T']+g['F']).round(12))
        else: vals=list((g[list('TINF')].sum(axis=1)).round(12))
        diffs.extend([a"'!=b for a,b in combinations(vals,2)])
    print(outcome, round(float(np.mean(diffs)),3), len(diffs))
'"'@
python -c "'$code' in C:\Users\HP\Documents\MeasurementScience_Evals\paper11_elicitation_method
 succeeded in 17267ms:
regime 0.123 6330
vector 0.434 6330
tf_sum 0.265 6330
sum4 0.379 6330

exec
"C:\\WINDOWS\\System32\\WindowsPowerShell\\v1.0\\powershell.exe" -Command '$code = @'"'
import json, pathlib
from itertools import combinations
import pandas as pd
import numpy as np
pilot = pd.DataFrame([json.loads(l) for l in pathlib.Path('family1/results/raw_quadruple_pilot.jsonl').read_text(encoding='utf-8').splitlines() if l.strip()])
pilot = pilot[pilot.parsed & ~pilot.error].copy()
within_any=[]
for _, g in pilot.groupby(['phenomenon','statement','gloss','model']):
    within_any.append(g.regime.nunique() > 1)
between_any=[]
for _, g in pilot.groupby(['phenomenon','statement','gloss','rep']):
    between_any.append(g.regime.nunique() > 1)
print('within group any-disagreement', round(float(np.mean(within_any)),3), len(within_any))
print('between group any-disagreement', round(float(np.mean(between_any)),3), len(between_any))
'@
python -c "'$code' in C:\Users\HP\Documents\MeasurementScience_Evals\paper11_elicitation_method
 succeeded in 12133ms:
within group any-disagreement 0.282 142
between group any-disagreement 0.454 240

codex
I’m checking one last interpretation of the pilot percentages: whether they mean “a repeated cell ever changed label” instead of pairwise disagreement. That still has to match the prose, because “two repetitions” is a pairwise claim.
exec
"C:\\WINDOWS\\System32\\WindowsPowerShell\\v1.0\\powershell.exe" -Command "Get-Content -LiteralPath 'family2\\results\\raw_factual_full.jsonl' -TotalCount 1" in C:\Users\HP\Documents\MeasurementScience_Evals\paper11_elicitation_method
exec
"C:\\WINDOWS\\System32\\WindowsPowerShell\\v1.0\\powershell.exe" -Command "Get-Content -LiteralPath 'family1\\results\\raw_quad_bank.jsonl' -TotalCount 1" in C:\Users\HP\Documents\MeasurementScience_Evals\paper11_elicitation_method
exec
"C:\\WINDOWS\\System32\\WindowsPowerShell\\v1.0\\powershell.exe" -Command "Get-Content -LiteralPath 'family1\\results\\raw_bank.jsonl' -TotalCount 1" in C:\Users\HP\Documents\MeasurementScience_Evals\paper11_elicitation_method
exec
"C:\\WINDOWS\\System32\\WindowsPowerShell\\v1.0\\powershell.exe" -Command 'rg -n "date|created|timestamp|model_id|collected|24|26 August|version" family1 family2 paper/main.tex' in C:\Users\HP\Documents\MeasurementScience_Evals\paper11_elicitation_method
 succeeded in 7976ms:
paper/main.tex:26:\date{August 2026}
paper/main.tex:93:the second construct family, which is new data collected for this paper and appears in neither
paper/main.tex:98:prompt formatting alone moves accuracy by many points \citep{sclar2024quantifying}; that
paper/main.tex:100:language models by \citet{miller2024errorbars}. What we
paper/main.tex:102:defeats the natural ablation, the conversion of the first into a number of items, and a
paper/main.tex:366:been validated against independent judges. What we can say is
paper/main.tex:388:author. No survey, interview, annotation task or crowdworker judgment was collected, and no
paper/main.tex:393:aid to writing: the corpus consists of their outputs, collected between 24 and 26 August 2026
paper/main.tex:394:through a single router at temperature $1.0$. Vendors and model versions are named in
paper/main.tex:396:results are properties of specific model versions at a specific date and should not be assumed
paper/main.tex:399:\paragraph{Competing interests.} The Family~I corpus was collected for two companion studies
paper/main.tex:415:The Family~I generations were collected for the companion studies rather than for this paper.
paper/main.tex:421:The second bank is released in the form in which it was analysed, including the first version of
family2\analyze_factual.py:5:NOTA DE DISENO. La primera version de este script tomaba como cantidad principal la
family2\analyze_factual.py:15:inversion es el resultado que el banco factual aporta.
family2\analyze_factual_v1.py:10:Se publica sin corregir, junto a `analyze_factual.py`, que es la version que el paper
family1\README.md:3:**These generations were not collected for this paper.** They were collected for two companion
family2\run_factual.py:108:def call(cl, model_id, system, user):
family2\run_factual.py:112:                model=model_id,
family1\run_bank.py:72:def call(cl, model_id, stmt):
family1\run_bank.py:76:                model=model_id,
family1\run_neutral_system.py:104:def call(cl, model_id, user):
family1\run_neutral_system.py:108:                model=model_id,
family1\run_nolicense_system.py:109:def call(cl, model_id, user):
family1\run_nolicense_system.py:113:                model=model_id,
family1\results\h5_between_item_variance.csv:2:ethical,10,0.244,0.18,0.0,0.5
family1\run_quad_bank.py:89:def call(cl, model_id, user):
family1\run_quad_bank.py:93:                model=model_id,
family1\results\main_phenomenon_x_form.csv:2:ethical,0.244,0.589,0.345
family1\results\quad_q2_N_vs_I.csv:2:0.1467377568741064,0.36207761611639616,0.18645224900224436
family1\results\quad_q3_gloss.csv:4:G3,0.124,0.746,0.044,0.086
family1\results\raw_quadruple_pilot.jsonl:1:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Paradox (Logical)", "statement": "This sentence is false.", "gloss": "G1", "rep": 0, "response": "```json\n{\"T\": 0.0, \"I\": 1.0, \"N\": 0.5, \"F\": 0.0}\n```", "T": 0.0, "I": 1.0, "N": 0.5, "F": 0.0, "regime": "very_weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:2:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Paradox (Logical)", "statement": "This sentence is false.", "gloss": "G1", "rep": 1, "response": "```json\n{\"T\": 0.0, \"I\": 1.0, \"N\": 0.5, \"F\": 0.0}\n```", "T": 0.0, "I": 1.0, "N": 0.5, "F": 0.0, "regime": "very_weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:3:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Paradox (Logical)", "statement": "This sentence is false.", "gloss": "G1", "rep": 2, "response": "```json\n{\"T\": 0.0, \"I\": 1.0, \"N\": 0.5, \"F\": 0.0}\n```", "T": 0.0, "I": 1.0, "N": 0.5, "F": 0.0, "regime": "very_weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:4:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Paradox (Logical)", "statement": "This sentence is false.", "gloss": "G1", "rep": 3, "response": "```json\n{\"T\": 0.0, \"I\": 1.0, \"N\": 0.5, \"F\": 0.0}\n```", "T": 0.0, "I": 1.0, "N": 0.5, "F": 0.0, "regime": "very_weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:5:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Paradox (Logical)", "statement": "This sentence is false.", "gloss": "G1", "rep": 4, "response": "{\"T\": 0.0, \"I\": 1.0, \"N\": 0.5, \"F\": 0.0}", "T": 0.0, "I": 1.0, "N": 0.5, "F": 0.0, "regime": "very_weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:6:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Paradox (Logical)", "statement": "This sentence is false.", "gloss": "G1", "rep": 5, "response": "```json\n{\"T\": 0.0, \"I\": 1.0, \"N\": 0.5, \"F\": 0.0}\n```", "T": 0.0, "I": 1.0, "N": 0.5, "F": 0.0, "regime": "very_weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:7:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Paradox (Logical)", "statement": "This sentence is false.", "gloss": "G1", "rep": 6, "response": "```json\n{\"T\": 0.0, \"I\": 1.0, \"N\": 0.5, \"F\": 0.5}\n```", "T": 0.0, "I": 1.0, "N": 0.5, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:8:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Paradox (Logical)", "statement": "This sentence is false.", "gloss": "G1", "rep": 7, "response": "{\"T\": 0.0, \"I\": 1.0, \"N\": 0.5, \"F\": 0.0}", "T": 0.0, "I": 1.0, "N": 0.5, "F": 0.0, "regime": "very_weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:9:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Paradox (Logical)", "statement": "This sentence is false.", "gloss": "G1", "rep": 8, "response": "{\"T\": 0.0, \"I\": 1.0, \"N\": 0.5, \"F\": 0.0}", "T": 0.0, "I": 1.0, "N": 0.5, "F": 0.0, "regime": "very_weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:10:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Paradox (Logical)", "statement": "This sentence is false.", "gloss": "G1", "rep": 9, "response": "```json\n{\"T\": 0.5, \"I\": 0.9, \"N\": 0.5, \"F\": 0.5}\n```", "T": 0.5, "I": 0.9, "N": 0.5, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:11:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Paradox (Logical)", "statement": "This sentence is false.", "gloss": "G1", "rep": 0, "response": "{\"T\": 0.5, \"I\": 1.0, \"N\": 0.8, \"F\": 0.5}", "T": 0.5, "I": 1.0, "N": 0.8, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:12:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Paradox (Logical)", "statement": "This sentence is false.", "gloss": "G1", "rep": 1, "response": "{\"T\": 0.5, \"I\": 1.0, \"N\": 0.8, \"F\": 0.5}", "T": 0.5, "I": 1.0, "N": 0.8, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:13:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Paradox (Logical)", "statement": "This sentence is false.", "gloss": "G1", "rep": 2, "response": "{\"T\": 0.5, \"I\": 1.0, \"N\": 0.8, \"F\": 0.5}", "T": 0.5, "I": 1.0, "N": 0.8, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:14:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Paradox (Logical)", "statement": "This sentence is false.", "gloss": "G1", "rep": 3, "response": "{\"T\": 0.5, \"I\": 1.0, \"N\": 0.8, \"F\": 0.5}", "T": 0.5, "I": 1.0, "N": 0.8, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:15:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Paradox (Logical)", "statement": "This sentence is false.", "gloss": "G1", "rep": 4, "response": "{\"T\": 0.5, \"I\": 1.0, \"N\": 0.8, \"F\": 0.5}", "T": 0.5, "I": 1.0, "N": 0.8, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:16:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Paradox (Logical)", "statement": "This sentence is false.", "gloss": "G1", "rep": 5, "response": "{\"T\": 0.5, \"I\": 1.0, \"N\": 0.8, \"F\": 0.5}", "T": 0.5, "I": 1.0, "N": 0.8, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:17:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Paradox (Logical)", "statement": "This sentence is false.", "gloss": "G1", "rep": 6, "response": "{\"T\": 0.5, \"I\": 1.0, \"N\": 0.8, \"F\": 0.5}", "T": 0.5, "I": 1.0, "N": 0.8, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:18:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Paradox (Logical)", "statement": "This sentence is false.", "gloss": "G1", "rep": 7, "response": "{\"T\": 0.5, \"I\": 1.0, \"N\": 0.8, \"F\": 0.5}", "T": 0.5, "I": 1.0, "N": 0.8, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:19:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Paradox (Logical)", "statement": "This sentence is false.", "gloss": "G1", "rep": 8, "response": "{\"T\": 0.5, \"I\": 1.0, \"N\": 0.8, \"F\": 0.5}", "T": 0.5, "I": 1.0, "N": 0.8, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:20:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Paradox (Logical)", "statement": "This sentence is false.", "gloss": "G1", "rep": 9, "response": "{\"T\": 0.5, \"I\": 1.0, \"N\": 0.8, \"F\": 0.5}", "T": 0.5, "I": 1.0, "N": 0.8, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:21:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Paradox (Logical)", "statement": "This sentence is false.", "gloss": "G1", "rep": 0, "response": "{\"T\": 0.4, \"I\": 0.8, \"N\": 0.2, \"F\": 0.5}", "T": 0.4, "I": 0.8, "N": 0.2, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:22:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Paradox (Logical)", "statement": "This sentence is false.", "gloss": "G1", "rep": 1, "response": "{\"T\": 0.0, \"I\": 0.9, \"N\": 0.5, \"F\": 0.0}", "T": 0.0, "I": 0.9, "N": 0.5, "F": 0.0, "regime": "very_weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:23:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Paradox (Logical)", "statement": "This sentence is false.", "gloss": "G1", "rep": 2, "response": "{\"T\": 0.4, \"I\": 0.8, \"N\": 0.2, \"F\": 0.5}", "T": 0.4, "I": 0.8, "N": 0.2, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:24:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Paradox (Logical)", "statement": "This sentence is false.", "gloss": "G1", "rep": 3, "response": "{\"T\": 0.0, \"I\": 0.9, \"N\": 0.5, \"F\": 0.0}", "T": 0.0, "I": 0.9, "N": 0.5, "F": 0.0, "regime": "very_weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:25:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Paradox (Logical)", "statement": "This sentence is false.", "gloss": "G1", "rep": 4, "response": "{\"T\": 0.0, \"I\": 0.9, \"", "T": null, "I": null, "N": null, "F": null, "regime": null, "parsed": false, "error": false}
family1\results\raw_quadruple_pilot.jsonl:26:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Paradox (Logical)", "statement": "This sentence is false.", "gloss": "G1", "rep": 5, "response": "{\"T\": 0.4, \"I\": 0.8, \"N\": 0.2, \"F\": 0.5}", "T": 0.4, "I": 0.8, "N": 0.2, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:27:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Paradox (Logical)", "statement": "This sentence is false.", "gloss": "G1", "rep": 6, "response": "{\"T\": 0.0, \"I\": 0.9, \"N\": 0.5, \"F\": 0.0}", "T": 0.0, "I": 0.9, "N": 0.5, "F": 0.0, "regime": "very_weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:28:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Paradox (Logical)", "statement": "This sentence is false.", "gloss": "G1", "rep": 7, "response": "{\"T\": 0.4, \"I\": 0.8, \"N\": 0.2, \"F\": 0.5}", "T": 0.4, "I": 0.8, "N": 0.2, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:29:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Paradox (Logical)", "statement": "This sentence is false.", "gloss": "G1", "rep": 8, "response": "{\"T\": 0.4, \"I\": 0.8, \"N\": 0.2, \"F\": 0.5}", "T": 0.4, "I": 0.8, "N": 0.2, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:30:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Paradox (Logical)", "statement": "This sentence is false.", "gloss": "G1", "rep": 9, "response": "{\"T\": 0.0, \"I\": 0.9, \"N\": 0.5, \"F\": 0.0}", "T": 0.0, "I": 0.9, "N": 0.5, "F": 0.0, "regime": "very_weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:31:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Paradox (Logical)", "statement": "This sentence is false.", "gloss": "G1", "rep": 0, "response": "```json\n{\"T\": 0.5, \"I\": 0.8, \"N\": 0.3, \"F\": 0.5}\n```", "T": 0.5, "I": 0.8, "N": 0.3, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:32:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Paradox (Logical)", "statement": "This sentence is false.", "gloss": "G1", "rep": 1, "response": "```json\n{\"T\": 0.5, \"I\": 0.8, \"N\": 0.3, \"F\": 0.5}\n```", "T": 0.5, "I": 0.8, "N": 0.3, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:33:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Paradox (Logical)", "statement": "This sentence is false.", "gloss": "G1", "rep": 2, "response": "```json\n{\"T\": 0.5, \"I\": 0.5, \"N\": 0.0, \"F\": 0.5}\n```", "T": 0.5, "I": 0.5, "N": 0.0, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:34:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Paradox (Logical)", "statement": "This sentence is false.", "gloss": "G1", "rep": 3, "response": "```json\n{\"T\": 0.5, \"I\": 0.0, \"N\": 0.5, \"F\": 0.5}\n```", "T": 0.5, "I": 0.0, "N": 0.5, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:35:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Paradox (Logical)", "statement": "This sentence is false.", "gloss": "G1", "rep": 4, "response": "```json\n{\"T\": 0.5, \"I\": 0.8, \"N\": 0.2, \"F\": 0.5}\n```", "T": 0.5, "I": 0.8, "N": 0.2, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:36:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Paradox (Logical)", "statement": "This sentence is false.", "gloss": "G1", "rep": 5, "response": "```json\n{\"T\": 0.5, \"I\": 0.8, \"N\": 0.2, \"F\": 0.5}\n```", "T": 0.5, "I": 0.8, "N": 0.2, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:37:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Paradox (Logical)", "statement": "This sentence is false.", "gloss": "G1", "rep": 6, "response": "```json\n{\"T\": 0.5, \"I\": 0.8, \"N\": 0.3, \"F\": 0.5}\n```", "T": 0.5, "I": 0.8, "N": 0.3, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:38:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Paradox (Logical)", "statement": "This sentence is false.", "gloss": "G1", "rep": 7, "response": "```json\n{\"T\": 0.5, \"I\": 0.5, \"N\": 0.0, \"F\": 0.5}\n```", "T": 0.5, "I": 0.5, "N": 0.0, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:39:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Paradox (Logical)", "statement": "This sentence is false.", "gloss": "G1", "rep": 8, "response": "```json\n{\"T\": 0.5, \"I\": 0.8, \"N\": 0.2, \"F\": 0.5}\n```", "T": 0.5, "I": 0.8, "N": 0.2, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:40:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Paradox (Logical)", "statement": "This sentence is false.", "gloss": "G1", "rep": 9, "response": "```json\n{\"T\": 0.5, \"I\": 0.8, \"N\": 0.3, \"F\": 0.5}\n```", "T": 0.5, "I": 0.8, "N": 0.3, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:41:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Paradox (Logical)", "statement": "This sentence is false.", "gloss": "G1", "rep": 0, "response": "{\"T\": 0.5, \"I\": 1.0, \"N\": 0.5, \"F\": 0.5}", "T": 0.5, "I": 1.0, "N": 0.5, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:42:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Paradox (Logical)", "statement": "This sentence is false.", "gloss": "G1", "rep": 1, "response": "{\"T\": 0.5, \"I\": 1.0, \"N\": 0.5, \"F\": 0.5}", "T": 0.5, "I": 1.0, "N": 0.5, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:43:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Paradox (Logical)", "statement": "This sentence is false.", "gloss": "G1", "rep": 2, "response": "{\"T\": 0.5, \"I\": 1.0, \"N\": 0.5, \"F\": 0.5}", "T": 0.5, "I": 1.0, "N": 0.5, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:44:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Paradox (Logical)", "statement": "This sentence is false.", "gloss": "G1", "rep": 3, "response": "{\"T\": 0.5, \"I\": 1.0, \"N\": 0.5, \"F\": 0.5}", "T": 0.5, "I": 1.0, "N": 0.5, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:45:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Paradox (Logical)", "statement": "This sentence is false.", "gloss": "G1", "rep": 4, "response": "{\"T\": 0.5, \"I\": 1.0, \"N\": 0.5, \"F\": 0.5}", "T": 0.5, "I": 1.0, "N": 0.5, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:46:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Paradox (Logical)", "statement": "This sentence is false.", "gloss": "G1", "rep": 5, "response": "{\"T\": 0.5, \"I\": 1.0, \"N\": 0.5, \"F\": 0.5}", "T": 0.5, "I": 1.0, "N": 0.5, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:47:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Paradox (Logical)", "statement": "This sentence is false.", "gloss": "G1", "rep": 6, "response": "{\"T\": 0.5, \"I\": 1.0, \"N\": 0.5, \"F\": 0.5}", "T": 0.5, "I": 1.0, "N": 0.5, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:48:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Paradox (Logical)", "statement": "This sentence is false.", "gloss": "G1", "rep": 7, "response": "{\"T\": 0.5, \"I\": 1.0, \"N\": 0.5, \"F\": 0.5}", "T": 0.5, "I": 1.0, "N": 0.5, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:49:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Paradox (Logical)", "statement": "This sentence is false.", "gloss": "G1", "rep": 8, "response": "{\"T\": 0.5, \"I\": 1.0, \"N\": 0.5, \"F\": 0.5}", "T": 0.5, "I": 1.0, "N": 0.5, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:50:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Paradox (Logical)", "statement": "This sentence is false.", "gloss": "G1", "rep": 9, "response": "{\"T\": 0.5, \"I\": 1.0, \"N\": 0.5, \"F\": 0.5}", "T": 0.5, "I": 1.0, "N": 0.5, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:51:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Paradox (Logical)", "statement": "This sentence is false.", "gloss": "G1", "rep": 0, "response": "```json\n{\n  \"T\": 0.0,\n  \"I\": 1.0,\n  \"N\": 0.7,\n  \"F\": 0.0\n}\n```", "T": 0.0, "I": 1.0, "N": 0.7, "F": 0.0, "regime": "very_weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:52:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Paradox (Logical)", "statement": "This sentence is false.", "gloss": "G1", "rep": 1, "response": "```json\n{\n  \"T\": 0.0,\n  \"I\": 0.95,\n  \"N\": 0.7,\n  \"F\": 0.0\n}\n```", "T": 0.0, "I": 0.95, "N": 0.7, "F": 0.0, "regime": "very_weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:53:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Paradox (Logical)", "statement": "This sentence is false.", "gloss": "G1", "rep": 2, "response": "```json\n{\n  \"T\": 0.0,\n  \"I\": 1.0,\n  \"N\": 0.5,\n  \"F\": 0.0\n}\n```", "T": 0.0, "I": 1.0, "N": 0.5, "F": 0.0, "regime": "very_weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:54:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Paradox (Logical)", "statement": "This sentence is false.", "gloss": "G1", "rep": 3, "response": "```json\n{\n  \"T\": 0.0,\n  \"I\": 1.0,\n  \"N\": 0.7,\n  \"F\": 0.0\n}\n```", "T": 0.0, "I": 1.0, "N": 0.7, "F": 0.0, "regime": "very_weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:55:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Paradox (Logical)", "statement": "This sentence is false.", "gloss": "G1", "rep": 4, "response": "```json\n{\n  \"T\": 0.0,\n  \"I\": 0.95,\n  \"N\": 0.8,\n  \"F\": 0.95\n}\n```", "T": 0.0, "I": 0.95, "N": 0.8, "F": 0.95, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:56:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Paradox (Logical)", "statement": "This sentence is false.", "gloss": "G1", "rep": 5, "response": "```json\n{\n  \"T\": 0.0,\n  \"I\": 1.0,\n  \"N\": 0.7,\n  \"F\": 0.0\n}\n```", "T": 0.0, "I": 1.0, "N": 0.7, "F": 0.0, "regime": "very_weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:57:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Paradox (Logical)", "statement": "This sentence is false.", "gloss": "G1", "rep": 6, "response": "```json\n{\n  \"T\": 0.0,\n  \"I\": 1.0,\n  \"N\": 0.3,\n  \"F\": 0.0\n}\n```", "T": 0.0, "I": 1.0, "N": 0.3, "F": 0.0, "regime": "very_weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:58:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Paradox (Logical)", "statement": "This sentence is false.", "gloss": "G1", "rep": 7, "response": "```json\n{\n  \"T\": 0.0,\n  \"I\": 1.0,\n  \"N\": 0.7,\n  \"F\": 0.0\n}\n```", "T": 0.0, "I": 1.0, "N": 0.7, "F": 0.0, "regime": "very_weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:59:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Paradox (Logical)", "statement": "This sentence is false.", "gloss": "G1", "rep": 8, "response": "```json\n{\n  \"T\": 0.0,\n  \"I\": 0.9,\n  \"N\": 0.7,\n  \"F\": 0.0\n}\n```", "T": 0.0, "I": 0.9, "N": 0.7, "F": 0.0, "regime": "very_weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:60:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Paradox (Logical)", "statement": "This sentence is false.", "gloss": "G1", "rep": 9, "response": "```json\n{\n  \"T\": 0.0,\n  \"I\": 1.0,\n  \"N\": 0.8,\n  \"F\": 0.0\n}\n```", "T": 0.0, "I": 1.0, "N": 0.8, "F": 0.0, "regime": "very_weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:61:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Paradox (Logical)", "statement": "This sentence is false.", "gloss": "G2", "rep": 0, "response": "```json\n{\"T\": 0.0, \"I\": 1.0, \"N\": 0.7, \"F\": 0.0}\n```", "T": 0.0, "I": 1.0, "N": 0.7, "F": 0.0, "regime": "very_weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:62:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Paradox (Logical)", "statement": "This sentence is false.", "gloss": "G2", "rep": 1, "response": "{\"T\": 0.0, \"I\": 1.0, \"N\": 0.5, \"F\": 0.0}", "T": 0.0, "I": 1.0, "N": 0.5, "F": 0.0, "regime": "very_weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:63:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Paradox (Logical)", "statement": "This sentence is false.", "gloss": "G2", "rep": 2, "response": "```json\n{\"T\": 0.0, \"I\": 1.0, \"N\": 0.0, \"F\": 0.0}\n```", "T": 0.0, "I": 1.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:64:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Paradox (Logical)", "statement": "This sentence is false.", "gloss": "G2", "rep": 3, "response": "```json\n{\"T\": 0.0, \"I\": 1.0, \"N\": 0.5, \"F\": 0.5}\n```", "T": 0.0, "I": 1.0, "N": 0.5, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:65:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Paradox (Logical)", "statement": "This sentence is false.", "gloss": "G2", "rep": 4, "response": "{\"T\": 0.0, \"I\": 1.0, \"N\": 0.5, \"F\": 0.5}", "T": 0.0, "I": 1.0, "N": 0.5, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:66:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Paradox (Logical)", "statement": "This sentence is false.", "gloss": "G2", "rep": 5, "response": "```json\n{\"T\": 0.0, \"I\": 0.8, \"N\": 0.2, \"F\": 0.0}\n```", "T": 0.0, "I": 0.8, "N": 0.2, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:67:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Paradox (Logical)", "statement": "This sentence is false.", "gloss": "G2", "rep": 6, "response": "{\"T\": 0.0, \"I\": 0.9, \"N\": 0.7, \"F\": 0.1}", "T": 0.0, "I": 0.9, "N": 0.7, "F": 0.1, "regime": "very_weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:68:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Paradox (Logical)", "statement": "This sentence is false.", "gloss": "G2", "rep": 7, "response": "```json\n{\"T\": 0.0, \"I\": 0.9, \"N\": 0.1, \"F\": 0.0}\n```", "T": 0.0, "I": 0.9, "N": 0.1, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:69:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Paradox (Logical)", "statement": "This sentence is false.", "gloss": "G2", "rep": 8, "response": "{\"T\": 0.0, \"I\": 0.8, \"N\": 0.5, \"F\": 0.5}", "T": 0.0, "I": 0.8, "N": 0.5, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:70:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Paradox (Logical)", "statement": "This sentence is false.", "gloss": "G2", "rep": 9, "response": "{\"T\": 0.0, \"I\": 1.0, \"N\": 0.5, \"F\": 0.5}", "T": 0.0, "I": 1.0, "N": 0.5, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:71:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Paradox (Logical)", "statement": "This sentence is false.", "gloss": "G2", "rep": 0, "response": "{\"T\": 0.5, \"I\": 1.0, \"N\": 0.8, \"F\": 0.5}", "T": 0.5, "I": 1.0, "N": 0.8, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:72:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Paradox (Logical)", "statement": "This sentence is false.", "gloss": "G2", "rep": 1, "response": "{\"T\": 0.5, \"I\": 1.0, \"N\": 0.8, \"F\": 0.5}", "T": 0.5, "I": 1.0, "N": 0.8, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:73:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Paradox (Logical)", "statement": "This sentence is false.", "gloss": "G2", "rep": 2, "response": "{\"T\": 0.5, \"I\": 1.0, \"N\": 0.8, \"F\": 0.5}", "T": 0.5, "I": 1.0, "N": 0.8, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:74:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Paradox (Logical)", "statement": "This sentence is false.", "gloss": "G2", "rep": 3, "response": "{\"T\": 0.5, \"I\": 1.0, \"N\": 0.8, \"F\": 0.5}", "T": 0.5, "I": 1.0, "N": 0.8, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:75:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Paradox (Logical)", "statement": "This sentence is false.", "gloss": "G2", "rep": 4, "response": "{\"T\": 0.5, \"I\": 1.0, \"N\": 0.8, \"F\": 0.5}", "T": 0.5, "I": 1.0, "N": 0.8, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:76:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Paradox (Logical)", "statement": "This sentence is false.", "gloss": "G2", "rep": 5, "response": "{\"T\": 0.5, \"I\": 1.0, \"N\": 0.8, \"F\": 0.5}", "T": 0.5, "I": 1.0, "N": 0.8, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:77:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Paradox (Logical)", "statement": "This sentence is false.", "gloss": "G2", "rep": 6, "response": "{\"T\": 0.5, \"I\": 1.0, \"N\": 0.8, \"F\": 0.5}", "T": 0.5, "I": 1.0, "N": 0.8, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:78:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Paradox (Logical)", "statement": "This sentence is false.", "gloss": "G2", "rep": 7, "response": "{\"T\": 0.5, \"I\": 1.0, \"N\": 0.8, \"F\": 0.5}", "T": 0.5, "I": 1.0, "N": 0.8, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:79:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Paradox (Logical)", "statement": "This sentence is false.", "gloss": "G2", "rep": 8, "response": "{\"T\": 0.5, \"I\": 1.0, \"N\": 0.8, \"F\": 0.5}", "T": 0.5, "I": 1.0, "N": 0.8, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:80:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Paradox (Logical)", "statement": "This sentence is false.", "gloss": "G2", "rep": 9, "response": "{\"T\": 0.5, \"I\": 1.0, \"N\": 0.8, \"F\": 0.5}", "T": 0.5, "I": 1.0, "N": 0.8, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:81:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Paradox (Logical)", "statement": "This sentence is false.", "gloss": "G2", "rep": 0, "response": "{\"T\": 0.0, \"I\": 0.9, \"N\": 0.1, \"F\": 0.0}", "T": 0.0, "I": 0.9, "N": 0.1, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:82:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Paradox (Logical)", "statement": "This sentence is false.", "gloss": "G2", "rep": 1, "response": "{\"T\": 0.5, \"I\": 0.8, \"", "T": null, "I": null, "N": null, "F": null, "regime": null, "parsed": false, "error": false}
family1\results\raw_quadruple_pilot.jsonl:83:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Paradox (Logical)", "statement": "This sentence is false.", "gloss": "G2", "rep": 2, "response": "{\"T\": 0.0, \"I\": 0.9, \"N\": 0.1, \"F\": 0.9}", "T": 0.0, "I": 0.9, "N": 0.1, "F": 0.9, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:84:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Paradox (Logical)", "statement": "This sentence is false.", "gloss": "G2", "rep": 3, "response": "{\"T\": 0.0, \"I\": 0.9, \"N\": 0.1, \"F\": 0.0}", "T": 0.0, "I": 0.9, "N": 0.1, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:85:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Paradox (Logical)", "statement": "This sentence is false.", "gloss": "G2", "rep": 4, "response": "{\"T\": 0.0, \"I\": 0.9, \"N\": 0.1, \"F\": 0.0}", "T": 0.0, "I": 0.9, "N": 0.1, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:86:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Paradox (Logical)", "statement": "This sentence is false.", "gloss": "G2", "rep": 5, "response": "{\"T\": 0.0, \"I\": 0.9, \"N\": 0.1, \"F\": 0.0}", "T": 0.0, "I": 0.9, "N": 0.1, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:87:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Paradox (Logical)", "statement": "This sentence is false.", "gloss": "G2", "rep": 6, "response": "{\"T\": 0.0, \"I\": 0.9, \"N\": 0.1, \"F\": 0.9}", "T": 0.0, "I": 0.9, "N": 0.1, "F": 0.9, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:88:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Paradox (Logical)", "statement": "This sentence is false.", "gloss": "G2", "rep": 7, "response": "{\"T\": 0.0, \"I\": 0.9, \"N\": 0.1, \"F\": 0.0}", "T": 0.0, "I": 0.9, "N": 0.1, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:89:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Paradox (Logical)", "statement": "This sentence is false.", "gloss": "G2", "rep": 8, "response": "{\"T\": 0.0, \"I\": 0.9, \"N\": 0.1, \"F\": 0.9}", "T": 0.0, "I": 0.9, "N": 0.1, "F": 0.9, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:90:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Paradox (Logical)", "statement": "This sentence is false.", "gloss": "G2", "rep": 9, "response": "{\"T\": 0.0, \"I\": 0.9, \"N\": 0.1, \"F\": 0.0}", "T": 0.0, "I": 0.9, "N": 0.1, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:91:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Paradox (Logical)", "statement": "This sentence is false.", "gloss": "G2", "rep": 0, "response": "```json\n{\"T\": 0.5, \"I\": 0.5, \"N\": 0.0, \"F\": 0.5}\n```", "T": 0.5, "I": 0.5, "N": 0.0, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:92:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Paradox (Logical)", "statement": "This sentence is false.", "gloss": "G2", "rep": 1, "response": "```json\n{\"T\": 0.5, \"I\": 0.5, \"N\": 0.2, \"F\": 0.5}\n```", "T": 0.5, "I": 0.5, "N": 0.2, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:93:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Paradox (Logical)", "statement": "This sentence is false.", "gloss": "G2", "rep": 2, "response": "```json\n{\"T\": 0.5, \"I\": 0.5, \"N\": 0.0, \"F\": 0.5}\n```", "T": 0.5, "I": 0.5, "N": 0.0, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:94:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Paradox (Logical)", "statement": "This sentence is false.", "gloss": "G2", "rep": 3, "response": "```json\n{\"T\": 0.5, \"I\": 0.5, \"N\": 0.5, \"F\": 0.5}\n```", "T": 0.5, "I": 0.5, "N": 0.5, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:95:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Paradox (Logical)", "statement": "This sentence is false.", "gloss": "G2", "rep": 4, "response": "```json\n{\"T\": 0.5, \"I\": 0.5, \"N\": 0.0, \"F\": 0.5}\n```", "T": 0.5, "I": 0.5, "N": 0.0, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:96:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Paradox (Logical)", "statement": "This sentence is false.", "gloss": "G2", "rep": 5, "response": "```json\n{\"T\": 0.5, \"I\": 0.8, \"N\": 0.3, \"F\": 0.5}\n```", "T": 0.5, "I": 0.8, "N": 0.3, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:97:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Paradox (Logical)", "statement": "This sentence is false.", "gloss": "G2", "rep": 6, "response": "```json\n{\"T\": 0.5, \"I\": 0.5, \"N\": 0.0, \"F\": 0.5}\n```", "T": 0.5, "I": 0.5, "N": 0.0, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:98:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Paradox (Logical)", "statement": "This sentence is false.", "gloss": "G2", "rep": 7, "response": "```json\n{\"T\": 0.5, \"I\": 0.8, \"N\": 0.3, \"F\": 0.5}\n```", "T": 0.5, "I": 0.8, "N": 0.3, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:99:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Paradox (Logical)", "statement": "This sentence is false.", "gloss": "G2", "rep": 8, "response": "```json\n{\"T\": 0.5, \"I\": 0.8, \"N\": 0.3, \"F\": 0.5}\n```", "T": 0.5, "I": 0.8, "N": 0.3, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:100:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Paradox (Logical)", "statement": "This sentence is false.", "gloss": "G2", "rep": 9, "response": "```json\n{\"T\": 0.5, \"I\": 0.5, \"N\": 0.0, \"F\": 0.5}\n```", "T": 0.5, "I": 0.5, "N": 0.0, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:101:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Paradox (Logical)", "statement": "This sentence is false.", "gloss": "G2", "rep": 0, "response": "{\"T\": 0.5, \"I\": 1.0, \"N\": 0.3, \"F\": 0.5}", "T": 0.5, "I": 1.0, "N": 0.3, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:102:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Paradox (Logical)", "statement": "This sentence is false.", "gloss": "G2", "rep": 1, "response": "{\"T\": 0.5, \"I\": 1.0, \"N\": 0.3, \"F\": 0.5}", "T": 0.5, "I": 1.0, "N": 0.3, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:103:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Paradox (Logical)", "statement": "This sentence is false.", "gloss": "G2", "rep": 2, "response": "{\"T\": 0.5, \"I\": 1.0, \"N\": 0.3, \"F\": 0.5}", "T": 0.5, "I": 1.0, "N": 0.3, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:104:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Paradox (Logical)", "statement": "This sentence is false.", "gloss": "G2", "rep": 3, "response": "{\"T\": 0.5, \"I\": 1.0, \"N\": 0.3, \"F\": 0.5}", "T": 0.5, "I": 1.0, "N": 0.3, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:105:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Paradox (Logical)", "statement": "This sentence is false.", "gloss": "G2", "rep": 4, "response": "{\"T\": 0.5, \"I\": 1.0, \"N\": 0.3, \"F\": 0.5}", "T": 0.5, "I": 1.0, "N": 0.3, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:106:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Paradox (Logical)", "statement": "This sentence is false.", "gloss": "G2", "rep": 5, "response": "{\"T\": 0.5, \"I\": 0.8, \"N\": 0.3, \"F\": 0.5}", "T": 0.5, "I": 0.8, "N": 0.3, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:107:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Paradox (Logical)", "statement": "This sentence is false.", "gloss": "G2", "rep": 6, "response": "{\"T\": 0.5, \"I\": 0.9, \"N\": 0.3, \"F\": 0.5}", "T": 0.5, "I": 0.9, "N": 0.3, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:108:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Paradox (Logical)", "statement": "This sentence is false.", "gloss": "G2", "rep": 7, "response": "{\"T\": 0.5, \"I\": 0.5, \"N\": 0.3, \"F\": 0.5}", "T": 0.5, "I": 0.5, "N": 0.3, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:109:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Paradox (Logical)", "statement": "This sentence is false.", "gloss": "G2", "rep": 8, "response": "{\"T\": 0.5, \"I\": 1.0, \"N\": 0.3, \"F\": 0.5}", "T": 0.5, "I": 1.0, "N": 0.3, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:110:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Paradox (Logical)", "statement": "This sentence is false.", "gloss": "G2", "rep": 9, "response": "{\"T\": 0.5, \"I\": 0.8, \"N\": 0.3, \"F\": 0.5}", "T": 0.5, "I": 0.8, "N": 0.3, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:111:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Paradox (Logical)", "statement": "This sentence is false.", "gloss": "G2", "rep": 0, "response": "```json\n{\n  \"T\": 0.0,\n  \"I\": 1.0,\n  \"N\": 0.85,\n  \"F\": 0.0\n}\n```", "T": 0.0, "I": 1.0, "N": 0.85, "F": 0.0, "regime": "very_weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:112:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Paradox (Logical)", "statement": "This sentence is false.", "gloss": "G2", "rep": 1, "response": "```json\n{\n  \"T\": 0.0,\n  \"I\": 1.0,\n  \"N\": 0.8,\n  \"F\": 0.0\n}\n```", "T": 0.0, "I": 1.0, "N": 0.8, "F": 0.0, "regime": "very_weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:113:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Paradox (Logical)", "statement": "This sentence is false.", "gloss": "G2", "rep": 2, "response": "```json\n{\n  \"T\": 0.0,\n  \"I\": 1.0,\n  \"N\": 0.8,\n  \"F\": 0.0\n}\n```", "T": 0.0, "I": 1.0, "N": 0.8, "F": 0.0, "regime": "very_weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:114:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Paradox (Logical)", "statement": "This sentence is false.", "gloss": "G2", "rep": 3, "response": "```json\n{\n  \"T\": 0.0,\n  \"I\": 1.0,\n  \"N\": 0.5,\n  \"F\": 0.0\n}\n```", "T": 0.0, "I": 1.0, "N": 0.5, "F": 0.0, "regime": "very_weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:115:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Paradox (Logical)", "statement": "This sentence is false.", "gloss": "G2", "rep": 4, "response": "```json\n{\n  \"T\": 0.0,\n  \"I\": 0.95,\n  \"N\": 0.8,\n  \"F\": 0.0\n}\n```", "T": 0.0, "I": 0.95, "N": 0.8, "F": 0.0, "regime": "very_weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:116:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Paradox (Logical)", "statement": "This sentence is false.", "gloss": "G2", "rep": 5, "response": "```json\n{\n  \"T\": 0.0,\n  \"I\": 1.0,\n  \"N\": 0.9,\n  \"F\": 0.0\n}\n```", "T": 0.0, "I": 1.0, "N": 0.9, "F": 0.0, "regime": "very_weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:117:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Paradox (Logical)", "statement": "This sentence is false.", "gloss": "G2", "rep": 6, "response": "```json\n{\n  \"T\": 0.0,\n  \"I\": 0.95,\n  \"N\": 0.75,\n  \"F\": 0.0\n}\n```", "T": 0.0, "I": 0.95, "N": 0.75, "F": 0.0, "regime": "very_weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:118:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Paradox (Logical)", "statement": "This sentence is false.", "gloss": "G2", "rep": 7, "response": "```json\n{\n  \"T\": 0.0,\n  \"I\": 0.95,\n  \"N\": 0.8,\n  \"F\": 0.0\n}\n```", "T": 0.0, "I": 0.95, "N": 0.8, "F": 0.0, "regime": "very_weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:119:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Paradox (Logical)", "statement": "This sentence is false.", "gloss": "G2", "rep": 8, "response": "```json\n{\n  \"T\": 0.0,\n  \"I\": 1.0,\n  \"N\": 0.7,\n  \"F\": 0.0\n}\n```", "T": 0.0, "I": 1.0, "N": 0.7, "F": 0.0, "regime": "very_weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:120:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Paradox (Logical)", "statement": "This sentence is false.", "gloss": "G2", "rep": 9, "response": "```json\n{\n  \"T\": 0.0,\n  \"I\": 1.0,\n  \"N\": 0.85,\n  \"F\": 0.0\n}\n```", "T": 0.0, "I": 1.0, "N": 0.85, "F": 0.0, "regime": "very_weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:121:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Paradox (Logical)", "statement": "This sentence is false.", "gloss": "G3", "rep": 0, "response": "```json\n{\"T\": 0.0, \"I\": 1.0, \"N\": 0.0, \"F\": 0.0}\n```", "T": 0.0, "I": 1.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:122:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Paradox (Logical)", "statement": "This sentence is false.", "gloss": "G3", "rep": 1, "response": "```json\n{\"T\": 0.0, \"I\": 1.0, \"N\": 0.0, \"F\": 0.0}\n```", "T": 0.0, "I": 1.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:123:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Paradox (Logical)", "statement": "This sentence is false.", "gloss": "G3", "rep": 2, "response": "```json\n{\"T\": 0.0, \"I\": 1.0, \"N\": 0.5, \"F\": 0.5}\n```", "T": 0.0, "I": 1.0, "N": 0.5, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:124:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Paradox (Logical)", "statement": "This sentence is false.", "gloss": "G3", "rep": 3, "response": "```json\n{\"T\": 0.0, \"I\": 1.0, \"N\": 0.0, \"F\": 0.0}\n```", "T": 0.0, "I": 1.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:125:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Paradox (Logical)", "statement": "This sentence is false.", "gloss": "G3", "rep": 4, "response": "```json\n{\"T\": 0.0, \"I\": 1.0, \"N\": 0.5, \"F\": 0.0}\n```", "T": 0.0, "I": 1.0, "N": 0.5, "F": 0.0, "regime": "very_weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:126:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Paradox (Logical)", "statement": "This sentence is false.", "gloss": "G3", "rep": 5, "response": "```json\n{\"T\": 0.5, \"I\": 0.9, \"N\": 0.7, \"F\": 0.5}\n```", "T": 0.5, "I": 0.9, "N": 0.7, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:127:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Paradox (Logical)", "statement": "This sentence is false.", "gloss": "G3", "rep": 6, "response": "```json\n{\"T\": 0.5, \"I\": 1.0, \"N\": 0.5, \"F\": 0.5}\n```", "T": 0.5, "I": 1.0, "N": 0.5, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:128:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Paradox (Logical)", "statement": "This sentence is false.", "gloss": "G3", "rep": 7, "response": "```json\n{\"T\": 0.0, \"I\": 1.0, \"N\": 0.5, \"F\": 0.0}\n```", "T": 0.0, "I": 1.0, "N": 0.5, "F": 0.0, "regime": "very_weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:129:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Paradox (Logical)", "statement": "This sentence is false.", "gloss": "G3", "rep": 8, "response": "```json\n{\"T\": 0.0, \"I\": 1.0, \"N\": 0.5, \"F\": 0.0}\n```", "T": 0.0, "I": 1.0, "N": 0.5, "F": 0.0, "regime": "very_weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:130:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Paradox (Logical)", "statement": "This sentence is false.", "gloss": "G3", "rep": 9, "response": "```json\n{\"T\": 0.0, \"I\": 1.0, \"N\": 0.0, \"F\": 1.0}\n```", "T": 0.0, "I": 1.0, "N": 0.0, "F": 1.0, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:131:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Paradox (Logical)", "statement": "This sentence is false.", "gloss": "G3", "rep": 0, "response": "{\"T\": 0.5, \"I\": 0.8, \"N\": 0.7, \"F\": 0.5}", "T": 0.5, "I": 0.8, "N": 0.7, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:132:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Paradox (Logical)", "statement": "This sentence is false.", "gloss": "G3", "rep": 1, "response": "{\"T\": 0.5, \"I\": 1.0, \"N\": 1.0, \"F\": 0.5}", "T": 0.5, "I": 1.0, "N": 1.0, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:133:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Paradox (Logical)", "statement": "This sentence is false.", "gloss": "G3", "rep": 2, "response": "{\"T\": 0.5, \"I\": 0.8, \"N\": 0.7, \"F\": 0.5}", "T": 0.5, "I": 0.8, "N": 0.7, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:134:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Paradox (Logical)", "statement": "This sentence is false.", "gloss": "G3", "rep": 3, "response": "{\"T\": 0.5, \"I\": 1.0, \"N\": 1.0, \"F\": 0.5}", "T": 0.5, "I": 1.0, "N": 1.0, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:135:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Paradox (Logical)", "statement": "This sentence is false.", "gloss": "G3", "rep": 4, "response": "{\"T\": 0.5, \"I\": 1.0, \"N\": 1.0, \"F\": 0.5}", "T": 0.5, "I": 1.0, "N": 1.0, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:136:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Paradox (Logical)", "statement": "This sentence is false.", "gloss": "G3", "rep": 5, "response": "{\"T\": 0.5, \"I\": 0.8, \"N\": 0.7, \"F\": 0.5}", "T": 0.5, "I": 0.8, "N": 0.7, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:137:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Paradox (Logical)", "statement": "This sentence is false.", "gloss": "G3", "rep": 6, "response": "{\"T\": 0.5, \"I\": 0.8, \"N\": 0.7, \"F\": 0.5}", "T": 0.5, "I": 0.8, "N": 0.7, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:138:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Paradox (Logical)", "statement": "This sentence is false.", "gloss": "G3", "rep": 7, "response": "{\"T\": 0.5, \"I\": 1.0, \"N\": 1.0, \"F\": 0.5}", "T": 0.5, "I": 1.0, "N": 1.0, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:139:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Paradox (Logical)", "statement": "This sentence is false.", "gloss": "G3", "rep": 8, "response": "{\"T\": 0.5, \"I\": 1.0, \"N\": 1.0, \"F\": 0.5}", "T": 0.5, "I": 1.0, "N": 1.0, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:140:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Paradox (Logical)", "statement": "This sentence is false.", "gloss": "G3", "rep": 9, "response": "{\"T\": 0.5, \"I\": 0.8, \"N\": 0.7, \"F\": 0.5}", "T": 0.5, "I": 0.8, "N": 0.7, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:141:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Paradox (Logical)", "statement": "This sentence is false.", "gloss": "G3", "rep": 0, "response": "{\"T\": 0.0, \"I\": 0.8, \"N\": 0.5, \"F\": 0.0}", "T": 0.0, "I": 0.8, "N": 0.5, "F": 0.0, "regime": "very_weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:142:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Paradox (Logical)", "statement": "This sentence is false.", "gloss": "G3", "rep": 1, "response": "{\"T\": 0.0, \"I\": 0.8, \"N\": 0.5, \"F\": 0.0}", "T": 0.0, "I": 0.8, "N": 0.5, "F": 0.0, "regime": "very_weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:143:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Paradox (Logical)", "statement": "This sentence is false.", "gloss": "G3", "rep": 2, "response": "{\"T\": 0.5, \"I\": 0.8, \"N\": 0.4, \"F\": 0.5}", "T": 0.5, "I": 0.8, "N": 0.4, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:144:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Paradox (Logical)", "statement": "This sentence is false.", "gloss": "G3", "rep": 3, "response": "{\"T\": 0.0, \"I\": 0.8, \"N\": 0.5, \"F\": 0.0}", "T": 0.0, "I": 0.8, "N": 0.5, "F": 0.0, "regime": "very_weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:145:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Paradox (Logical)", "statement": "This sentence is false.", "gloss": "G3", "rep": 4, "response": "{\"T\": 0.0, \"I\": 0.8, \"N\": 0.5, \"F\": 0.0}", "T": 0.0, "I": 0.8, "N": 0.5, "F": 0.0, "regime": "very_weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:146:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Paradox (Logical)", "statement": "This sentence is false.", "gloss": "G3", "rep": 5, "response": "{\"T\": 0.0, \"I\": 0.8, \"N\": 0.5, \"F\": 0.0}", "T": 0.0, "I": 0.8, "N": 0.5, "F": 0.0, "regime": "very_weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:147:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Paradox (Logical)", "statement": "This sentence is false.", "gloss": "G3", "rep": 6, "response": "{\"T\": 0.0, \"I\": 0.8, \"N\": 0.5, \"F\": 0.0}", "T": 0.0, "I": 0.8, "N": 0.5, "F": 0.0, "regime": "very_weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:148:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Paradox (Logical)", "statement": "This sentence is false.", "gloss": "G3", "rep": 7, "response": "{\"T\": 0.0, \"I\": 0.8, \"N\": 0.5, \"F\": 0.0}", "T": 0.0, "I": 0.8, "N": 0.5, "F": 0.0, "regime": "very_weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:149:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Paradox (Logical)", "statement": "This sentence is false.", "gloss": "G3", "rep": 8, "response": "{\"T\": 0.0, \"I\": 0.8, \"N\": 0.5, \"F\": 0.0}", "T": 0.0, "I": 0.8, "N": 0.5, "F": 0.0, "regime": "very_weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:150:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Paradox (Logical)", "statement": "This sentence is false.", "gloss": "G3", "rep": 9, "response": "{\"T\": 0.0, \"I\": 0.8, \"N\": 0.5, \"F\": 0.0}", "T": 0.0, "I": 0.8, "N": 0.5, "F": 0.0, "regime": "very_weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:151:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Paradox (Logical)", "statement": "This sentence is false.", "gloss": "G3", "rep": 0, "response": "```json\n{\"T\": 0.5, \"I\": 0.5, \"N\": 0.5, \"F\": 0.5}\n```", "T": 0.5, "I": 0.5, "N": 0.5, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:152:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Paradox (Logical)", "statement": "This sentence is false.", "gloss": "G3", "rep": 1, "response": "```json\n{\"T\": 0.5, \"I\": 0.5, \"N\": 0.5, \"F\": 0.5}\n```", "T": 0.5, "I": 0.5, "N": 0.5, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:153:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Paradox (Logical)", "statement": "This sentence is false.", "gloss": "G3", "rep": 2, "response": "```json\n{\"T\": 0.5, \"I\": 0.8, \"N\": 0.5, \"F\": 0.5}\n```", "T": 0.5, "I": 0.8, "N": 0.5, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:154:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Paradox (Logical)", "statement": "This sentence is false.", "gloss": "G3", "rep": 3, "response": "```json\n{\"T\": 0.5, \"I\": 0.8, \"N\": 0.3, \"F\": 0.5}\n```", "T": 0.5, "I": 0.8, "N": 0.3, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:155:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Paradox (Logical)", "statement": "This sentence is false.", "gloss": "G3", "rep": 4, "response": "```json\n{\"T\": 0.5, \"I\": 0.8, \"N\": 0.3, \"F\": 0.5}\n```", "T": 0.5, "I": 0.8, "N": 0.3, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:156:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Paradox (Logical)", "statement": "This sentence is false.", "gloss": "G3", "rep": 5, "response": "```json\n{\"T\": 0.5, \"I\": 0.5, \"N\": 0.5, \"F\": 0.5}\n```", "T": 0.5, "I": 0.5, "N": 0.5, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:157:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Paradox (Logical)", "statement": "This sentence is false.", "gloss": "G3", "rep": 6, "response": "```json\n{\"T\": 0.5, \"I\": 0.8, \"N\": 0.7, \"F\": 0.5}\n```", "T": 0.5, "I": 0.8, "N": 0.7, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:158:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Paradox (Logical)", "statement": "This sentence is false.", "gloss": "G3", "rep": 7, "response": "```json\n{\"T\": 0.5, \"I\": 0.8, \"N\": 0.7, \"F\": 0.5}\n```", "T": 0.5, "I": 0.8, "N": 0.7, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:159:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Paradox (Logical)", "statement": "This sentence is false.", "gloss": "G3", "rep": 8, "response": "```json\n{\"T\": 0.5, \"I\": 0.5, \"N\": 0.5, \"F\": 0.5}\n```", "T": 0.5, "I": 0.5, "N": 0.5, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:160:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Paradox (Logical)", "statement": "This sentence is false.", "gloss": "G3", "rep": 9, "response": "```json\n{\"T\": 0.5, \"I\": 0.3, \"N\": 0.7, \"F\": 0.5}\n```", "T": 0.5, "I": 0.3, "N": 0.7, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:161:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Paradox (Logical)", "statement": "This sentence is false.", "gloss": "G3", "rep": 0, "response": "{\"T\": 0.5, \"I\": 0.5, \"N\": 0.5, \"F\": 0.5}", "T": 0.5, "I": 0.5, "N": 0.5, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:162:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Paradox (Logical)", "statement": "This sentence is false.", "gloss": "G3", "rep": 1, "response": "{\"T\": 0.5, \"I\": 0.5, \"N\": 0.5, \"F\": 0.5}", "T": 0.5, "I": 0.5, "N": 0.5, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:163:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Paradox (Logical)", "statement": "This sentence is false.", "gloss": "G3", "rep": 2, "response": "{\"T\": 0.5, \"I\": 0.5, \"N\": 0.5, \"F\": 0.5}", "T": 0.5, "I": 0.5, "N": 0.5, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:164:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Paradox (Logical)", "statement": "This sentence is false.", "gloss": "G3", "rep": 3, "response": "{\"T\": 0.5, \"I\": 0.5, \"N\": 0.5, \"F\": 0.5}", "T": 0.5, "I": 0.5, "N": 0.5, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:165:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Paradox (Logical)", "statement": "This sentence is false.", "gloss": "G3", "rep": 4, "response": "{\"T\": 0.5, \"I\": 0.5, \"N\": 0.5, \"F\": 0.5}", "T": 0.5, "I": 0.5, "N": 0.5, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:166:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Paradox (Logical)", "statement": "This sentence is false.", "gloss": "G3", "rep": 5, "response": "{\"T\": 0.5, \"I\": 1.0, \"N\": 1.0, \"F\": 0.5}", "T": 0.5, "I": 1.0, "N": 1.0, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:167:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Paradox (Logical)", "statement": "This sentence is false.", "gloss": "G3", "rep": 6, "response": "{\"T\": 0.5, \"I\": 1.0, \"N\": 1.0, \"F\": 0.5}", "T": 0.5, "I": 1.0, "N": 1.0, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:168:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Paradox (Logical)", "statement": "This sentence is false.", "gloss": "G3", "rep": 7, "response": "{\"T\": 0.5, \"I\": 0.5, \"N\": 0.0, \"F\": 0.5}", "T": 0.5, "I": 0.5, "N": 0.0, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:169:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Paradox (Logical)", "statement": "This sentence is false.", "gloss": "G3", "rep": 8, "response": "{\"T\": 0.5, \"I\": 0.5, \"N\": 0.0, \"F\": 0.5}", "T": 0.5, "I": 0.5, "N": 0.0, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:170:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Paradox (Logical)", "statement": "This sentence is false.", "gloss": "G3", "rep": 9, "response": "{\"T\": 0.5, \"I\": 0.5, \"N\": 0.5, \"F\": 0.5}", "T": 0.5, "I": 0.5, "N": 0.5, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:171:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Paradox (Logical)", "statement": "This sentence is false.", "gloss": "G3", "rep": 0, "response": "```json\n{\n  \"T\": 0.0,\n  \"I\": 0.85,\n  \"N\": 0.75,\n  \"F\": 0.0\n}\n```", "T": 0.0, "I": 0.85, "N": 0.75, "F": 0.0, "regime": "very_weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:172:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Paradox (Logical)", "statement": "This sentence is false.", "gloss": "G3", "rep": 1, "response": "```json\n{\n  \"T\": 0.0,\n  \"I\": 0.95,\n  \"N\": 0.85,\n  \"F\": 0.0\n}\n```", "T": 0.0, "I": 0.95, "N": 0.85, "F": 0.0, "regime": "very_weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:173:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Paradox (Logical)", "statement": "This sentence is false.", "gloss": "G3", "rep": 2, "response": "```json\n{\n  \"T\": 0.0,\n  \"I\": 1.0,\n  \"N\": 0.9,\n  \"F\": 0.0\n}\n```", "T": 0.0, "I": 1.0, "N": 0.9, "F": 0.0, "regime": "very_weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:174:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Paradox (Logical)", "statement": "This sentence is false.", "gloss": "G3", "rep": 3, "response": "```json\n{\n  \"T\": 0.0,\n  \"I\": 0.95,\n  \"N\": 0.8,\n  \"F\": 0.0\n}\n```", "T": 0.0, "I": 0.95, "N": 0.8, "F": 0.0, "regime": "very_weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:175:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Paradox (Logical)", "statement": "This sentence is false.", "gloss": "G3", "rep": 4, "response": "```json\n{\n  \"T\": 0.0,\n  \"I\": 1.0,\n  \"N\": 0.8,\n  \"F\": 0.0\n}\n```", "T": 0.0, "I": 1.0, "N": 0.8, "F": 0.0, "regime": "very_weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:176:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Paradox (Logical)", "statement": "This sentence is false.", "gloss": "G3", "rep": 5, "response": "```json\n{\n  \"T\": 0.0,\n  \"I\": 0.95,\n  \"N\": 0.8,\n  \"F\": 0.0\n}\n```", "T": 0.0, "I": 0.95, "N": 0.8, "F": 0.0, "regime": "very_weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:177:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Paradox (Logical)", "statement": "This sentence is false.", "gloss": "G3", "rep": 6, "response": "```json\n{\n  \"T\": 0.0,\n  \"I\": 0.95,\n  \"N\": 0.8,\n  \"F\": 0.95\n}\n```", "T": 0.0, "I": 0.95, "N": 0.8, "F": 0.95, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:178:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Paradox (Logical)", "statement": "This sentence is false.", "gloss": "G3", "rep": 7, "response": "```json\n{\n  \"T\": 0.0,\n  \"I\": 0.95,\n  \"N\": 0.8,\n  \"F\": 0.0\n}\n```", "T": 0.0, "I": 0.95, "N": 0.8, "F": 0.0, "regime": "very_weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:179:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Paradox (Logical)", "statement": "This sentence is false.", "gloss": "G3", "rep": 8, "response": "```json\n{\n  \"T\": 0.0,\n  \"I\": 0.95,\n  \"N\": 0.85,\n  \"F\": 0.0\n}\n```", "T": 0.0, "I": 0.95, "N": 0.85, "F": 0.0, "regime": "very_weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:180:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Paradox (Logical)", "statement": "This sentence is false.", "gloss": "G3", "rep": 9, "response": "```json\n{\n  \"T\": 0.0,\n  \"I\": 0.95,\n  \"N\": 0.85,\n  \"F\": 0.0\n}\n```", "T": 0.0, "I": 0.95, "N": 0.85, "F": 0.0, "regime": "very_weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:181:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Ignorance (Epistemic)", "statement": "The number of stars in the universe is even.", "gloss": "G1", "rep": 0, "response": "```json\n{\"T\": 0.1, \"I\": 0.85, \"N\": 0.4, \"F\": 0.1}\n```", "T": 0.1, "I": 0.85, "N": 0.4, "F": 0.1, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:182:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Ignorance (Epistemic)", "statement": "The number of stars in the universe is even.", "gloss": "G1", "rep": 1, "response": "```json\n{\"T\": 0.0, \"I\": 1.0, \"N\": 0.5, \"F\": 0.0}\n```", "T": 0.0, "I": 1.0, "N": 0.5, "F": 0.0, "regime": "very_weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:183:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Ignorance (Epistemic)", "statement": "The number of stars in the universe is even.", "gloss": "G1", "rep": 2, "response": "```json\n{\"T\": 0.2, \"I\": 0.9, \"N\": 0.5, \"F\": 0.2}\n```", "T": 0.2, "I": 0.9, "N": 0.5, "F": 0.2, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:184:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Ignorance (Epistemic)", "statement": "The number of stars in the universe is even.", "gloss": "G1", "rep": 3, "response": "```json\n{\"T\": 0.1, \"I\": 0.9, \"N\": 0.5, \"F\": 0.1}\n```", "T": 0.1, "I": 0.9, "N": 0.5, "F": 0.1, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:185:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Ignorance (Epistemic)", "statement": "The number of stars in the universe is even.", "gloss": "G1", "rep": 4, "response": "```json\n{\"T\": 0.0, \"I\": 0.9, \"N\": 0.5, \"F\": 0.0}\n```", "T": 0.0, "I": 0.9, "N": 0.5, "F": 0.0, "regime": "very_weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:186:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Ignorance (Epistemic)", "statement": "The number of stars in the universe is even.", "gloss": "G1", "rep": 5, "response": "{\"T\": 0.0, \"I\": 0.9, \"N\": 0.5, \"F\": 0.0}", "T": 0.0, "I": 0.9, "N": 0.5, "F": 0.0, "regime": "very_weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:187:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Ignorance (Epistemic)", "statement": "The number of stars in the universe is even.", "gloss": "G1", "rep": 6, "response": "```json\n{\"T\": 0.1, \"I\": 0.9, \"N\": 0.5, \"F\": 0.1}\n```", "T": 0.1, "I": 0.9, "N": 0.5, "F": 0.1, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:188:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Ignorance (Epistemic)", "statement": "The number of stars in the universe is even.", "gloss": "G1", "rep": 7, "response": "```json\n{\"T\": 0.1, \"I\": 0.9, \"N\": 0.5, \"F\": 0.1}\n```", "T": 0.1, "I": 0.9, "N": 0.5, "F": 0.1, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:189:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Ignorance (Epistemic)", "statement": "The number of stars in the universe is even.", "gloss": "G1", "rep": 8, "response": "```json\n{\"T\": 0.1, \"I\": 0.9, \"N\": 0.5, \"F\": 0.1}\n```", "T": 0.1, "I": 0.9, "N": 0.5, "F": 0.1, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:190:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Ignorance (Epistemic)", "statement": "The number of stars in the universe is even.", "gloss": "G1", "rep": 9, "response": "```json\n{\"T\": 0.0, \"I\": 1.0, \"N\": 0.5, \"F\": 0.0}\n```", "T": 0.0, "I": 1.0, "N": 0.5, "F": 0.0, "regime": "very_weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:191:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Ignorance (Epistemic)", "statement": "The number of stars in the universe is even.", "gloss": "G1", "rep": 0, "response": "{\"T\": 0.5, \"I\": 0.9, \"N\": 0.7, \"F\": 0.5}", "T": 0.5, "I": 0.9, "N": 0.7, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:192:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Ignorance (Epistemic)", "statement": "The number of stars in the universe is even.", "gloss": "G1", "rep": 1, "response": "{\"T\": 0.5, \"I\": 0.9, \"N\": 0.7, \"F\": 0.5}", "T": 0.5, "I": 0.9, "N": 0.7, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:193:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Ignorance (Epistemic)", "statement": "The number of stars in the universe is even.", "gloss": "G1", "rep": 2, "response": "{\"T\": 0.5, \"I\": 0.9, \"N\": 0.7, \"F\": 0.5}", "T": 0.5, "I": 0.9, "N": 0.7, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:194:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Ignorance (Epistemic)", "statement": "The number of stars in the universe is even.", "gloss": "G1", "rep": 3, "response": "{\"T\": 0.5, \"I\": 0.9, \"N\": 0.7, \"F\": 0.5}", "T": 0.5, "I": 0.9, "N": 0.7, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:195:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Ignorance (Epistemic)", "statement": "The number of stars in the universe is even.", "gloss": "G1", "rep": 4, "response": "{\"T\": 0.5, \"I\": 0.9, \"N\": 0.7, \"F\": 0.5}", "T": 0.5, "I": 0.9, "N": 0.7, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:196:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Ignorance (Epistemic)", "statement": "The number of stars in the universe is even.", "gloss": "G1", "rep": 5, "response": "{\"T\": 0.5, \"I\": 0.9, \"N\": 0.7, \"F\": 0.5}", "T": 0.5, "I": 0.9, "N": 0.7, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:197:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Ignorance (Epistemic)", "statement": "The number of stars in the universe is even.", "gloss": "G1", "rep": 6, "response": "{\"T\": 0.5, \"I\": 0.9, \"N\": 0.7, \"F\": 0.5}", "T": 0.5, "I": 0.9, "N": 0.7, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:198:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Ignorance (Epistemic)", "statement": "The number of stars in the universe is even.", "gloss": "G1", "rep": 7, "response": "{\"T\": 0.5, \"I\": 0.9, \"N\": 0.7, \"F\": 0.5}", "T": 0.5, "I": 0.9, "N": 0.7, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:199:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Ignorance (Epistemic)", "statement": "The number of stars in the universe is even.", "gloss": "G1", "rep": 8, "response": "{\"T\": 0.5, \"I\": 0.9, \"N\": 0.7, \"F\": 0.5}", "T": 0.5, "I": 0.9, "N": 0.7, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:200:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Ignorance (Epistemic)", "statement": "The number of stars in the universe is even.", "gloss": "G1", "rep": 9, "response": "{\"T\": 0.5, \"I\": 0.9, \"N\": 0.8, \"F\": 0.5}", "T": 0.5, "I": 0.9, "N": 0.8, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:201:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Ignorance (Epistemic)", "statement": "The number of stars in the universe is even.", "gloss": "G1", "rep": 0, "response": "{\"T\": 0.0, \"I\": 1.0, \"N\": 0.5, \"F\": 0.0}", "T": 0.0, "I": 1.0, "N": 0.5, "F": 0.0, "regime": "very_weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:202:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Ignorance (Epistemic)", "statement": "The number of stars in the universe is even.", "gloss": "G1", "rep": 1, "response": "{\"T\": 0.0, \"I\": 1.0, \"N\": 0.5, \"F\": 0.0}", "T": 0.0, "I": 1.0, "N": 0.5, "F": 0.0, "regime": "very_weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:203:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Ignorance (Epistemic)", "statement": "The number of stars in the universe is even.", "gloss": "G1", "rep": 2, "response": "{\"T\": 0.0, \"I\": 1.0, \"N\": 0.5, \"F\": 0.0}", "T": 0.0, "I": 1.0, "N": 0.5, "F": 0.0, "regime": "very_weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:204:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Ignorance (Epistemic)", "statement": "The number of stars in the universe is even.", "gloss": "G1", "rep": 3, "response": "{\"T\": 0.0, \"I\": 1.0, \"N\": 0.5, \"F\": 0.0}", "T": 0.0, "I": 1.0, "N": 0.5, "F": 0.0, "regime": "very_weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:205:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Ignorance (Epistemic)", "statement": "The number of stars in the universe is even.", "gloss": "G1", "rep": 4, "response": "{\"T\": 0.0, \"I\": 1.0, \"N\": 0.5, \"F\": 0.0}", "T": 0.0, "I": 1.0, "N": 0.5, "F": 0.0, "regime": "very_weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:206:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Ignorance (Epistemic)", "statement": "The number of stars in the universe is even.", "gloss": "G1", "rep": 5, "response": "{\"T\": 0.0, \"I\": 1.0, \"N\": 0.5, \"F\": 0.0}", "T": 0.0, "I": 1.0, "N": 0.5, "F": 0.0, "regime": "very_weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:207:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Ignorance (Epistemic)", "statement": "The number of stars in the universe is even.", "gloss": "G1", "rep": 6, "response": "{\"T\": 0.0, \"I\": 1.0, \"N\": 0.5, \"F\": 0.0}", "T": 0.0, "I": 1.0, "N": 0.5, "F": 0.0, "regime": "very_weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:208:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Ignorance (Epistemic)", "statement": "The number of stars in the universe is even.", "gloss": "G1", "rep": 7, "response": "{\"T\": 0.0, \"I\": 1.0, \"N\": 0.5, \"F\": 0.0}", "T": 0.0, "I": 1.0, "N": 0.5, "F": 0.0, "regime": "very_weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:209:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Ignorance (Epistemic)", "statement": "The number of stars in the universe is even.", "gloss": "G1", "rep": 8, "response": "{\"T\": 0.0, \"I\": 1.0, \"N\": 0.5, \"F\": 0.0}", "T": 0.0, "I": 1.0, "N": 0.5, "F": 0.0, "regime": "very_weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:210:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Ignorance (Epistemic)", "statement": "The number of stars in the universe is even.", "gloss": "G1", "rep": 9, "response": "{\"T\": 0.0, \"I\": 1.0, \"N\": 0.5, \"F\": 0.0}", "T": 0.0, "I": 1.0, "N": 0.5, "F": 0.0, "regime": "very_weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:211:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Ignorance (Epistemic)", "statement": "The number of stars in the universe is even.", "gloss": "G1", "rep": 0, "response": "{\"T\": 0.0, \"I\": 1.0, \"N\": 0.1, \"F\": 0.0}", "T": 0.0, "I": 1.0, "N": 0.1, "F": 0.0, "regime": "very_weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:212:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Ignorance (Epistemic)", "statement": "The number of stars in the universe is even.", "gloss": "G1", "rep": 1, "response": "```json\n{\"T\": 0.0, \"I\": 1.0, \"N\": 0.5, \"F\": 0.0}\n```", "T": 0.0, "I": 1.0, "N": 0.5, "F": 0.0, "regime": "very_weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:213:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Ignorance (Epistemic)", "statement": "The number of stars in the universe is even.", "gloss": "G1", "rep": 2, "response": "```json\n{\"T\": 0.3, \"I\": 0.8, \"N\": 0.5, \"F\": 0.2}\n```", "T": 0.3, "I": 0.8, "N": 0.5, "F": 0.2, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:214:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Ignorance (Epistemic)", "statement": "The number of stars in the universe is even.", "gloss": "G1", "rep": 3, "response": "```json\n{\"T\": 0.0, \"I\": 1.0, \"N\": 0.5, \"F\": 0.0}\n```", "T": 0.0, "I": 1.0, "N": 0.5, "F": 0.0, "regime": "very_weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:215:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Ignorance (Epistemic)", "statement": "The number of stars in the universe is even.", "gloss": "G1", "rep": 4, "response": "```json\n{\"T\": 0.2, \"I\": 0.8, \"N\": 0.5, \"F\": 0.2}\n```", "T": 0.2, "I": 0.8, "N": 0.5, "F": 0.2, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:216:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Ignorance (Epistemic)", "statement": "The number of stars in the universe is even.", "gloss": "G1", "rep": 5, "response": "```json\n{\"T\": 0.1, \"I\": 0.9, \"N\": 0.5, \"F\": 0.1}\n```", "T": 0.1, "I": 0.9, "N": 0.5, "F": 0.1, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:217:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Ignorance (Epistemic)", "statement": "The number of stars in the universe is even.", "gloss": "G1", "rep": 6, "response": "```json\n{\"T\": 0.2, \"I\": 0.8, \"N\": 0.5, \"F\": 0.3}\n```", "T": 0.2, "I": 0.8, "N": 0.5, "F": 0.3, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:218:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Ignorance (Epistemic)", "statement": "The number of stars in the universe is even.", "gloss": "G1", "rep": 7, "response": "```json\n{\"T\": 0.1, \"I\": 0.9, \"N\": 0.5, \"F\": 0.1}\n```", "T": 0.1, "I": 0.9, "N": 0.5, "F": 0.1, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:219:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Ignorance (Epistemic)", "statement": "The number of stars in the universe is even.", "gloss": "G1", "rep": 8, "response": "```json\n{\"T\": 0.2, \"I\": 0.8, \"N\": 0.5, \"F\": 0.2}\n```", "T": 0.2, "I": 0.8, "N": 0.5, "F": 0.2, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:220:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Ignorance (Epistemic)", "statement": "The number of stars in the universe is even.", "gloss": "G1", "rep": 9, "response": "```json\n{\"T\": 0.2, \"I\": 0.8, \"N\": 0.3, \"F\": 0.1}\n```", "T": 0.2, "I": 0.8, "N": 0.3, "F": 0.1, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:221:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Ignorance (Epistemic)", "statement": "The number of stars in the universe is even.", "gloss": "G1", "rep": 0, "response": "{\"T\": 0.5, \"I\": 1.0, \"N\": 0.0, \"F\": 0.5}", "T": 0.5, "I": 1.0, "N": 0.0, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:222:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Ignorance (Epistemic)", "statement": "The number of stars in the universe is even.", "gloss": "G1", "rep": 1, "response": "{\"T\": 0.5, \"I\": 1.0, \"N\": 0.0, \"F\": 0.5}", "T": 0.5, "I": 1.0, "N": 0.0, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:223:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Ignorance (Epistemic)", "statement": "The number of stars in the universe is even.", "gloss": "G1", "rep": 2, "response": "{\"T\": 0.5, \"I\": 1.0, \"N\": 0.5, \"F\": 0.5}", "T": 0.5, "I": 1.0, "N": 0.5, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:224:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Ignorance (Epistemic)", "statement": "The number of stars in the universe is even.", "gloss": "G1", "rep": 3, "response": "{\"T\": 0.5, \"I\": 1.0, \"N\": 0.5, \"F\": 0.5}", "T": 0.5, "I": 1.0, "N": 0.5, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:225:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Ignorance (Epistemic)", "statement": "The number of stars in the universe is even.", "gloss": "G1", "rep": 4, "response": "{\"T\": 0.5, \"I\": 1.0, \"N\": 0.0, \"F\": 0.5}", "T": 0.5, "I": 1.0, "N": 0.0, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:226:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Ignorance (Epistemic)", "statement": "The number of stars in the universe is even.", "gloss": "G1", "rep": 5, "response": "{\"T\": 0.5, \"I\": 1.0, \"N\": 0.5, \"F\": 0.5}", "T": 0.5, "I": 1.0, "N": 0.5, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:227:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Ignorance (Epistemic)", "statement": "The number of stars in the universe is even.", "gloss": "G1", "rep": 6, "response": "{\"T\": 0.5, \"I\": 1.0, \"N\": 0.5, \"F\": 0.5}", "T": 0.5, "I": 1.0, "N": 0.5, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:228:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Ignorance (Epistemic)", "statement": "The number of stars in the universe is even.", "gloss": "G1", "rep": 7, "response": "{\"T\": 0.5, \"I\": 1.0, \"N\": 0.0, \"F\": 0.5}", "T": 0.5, "I": 1.0, "N": 0.0, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:229:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Ignorance (Epistemic)", "statement": "The number of stars in the universe is even.", "gloss": "G1", "rep": 8, "response": "{\"T\": 0.5, \"I\": 1.0, \"N\": 0.0, \"F\": 0.5}", "T": 0.5, "I": 1.0, "N": 0.0, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:230:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Ignorance (Epistemic)", "statement": "The number of stars in the universe is even.", "gloss": "G1", "rep": 9, "response": "{\"T\": 0.5, \"I\": 1.0, \"N\": 0.5, \"F\": 0.5}", "T": 0.5, "I": 1.0, "N": 0.5, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:231:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Ignorance (Epistemic)", "statement": "The number of stars in the universe is even.", "gloss": "G1", "rep": 0, "response": "```json\n{\n  \"T\": 0.0,\n  \"I\": 0.95,\n  \"N\": 0.7,\n  \"F\": 0.0\n}\n```", "T": 0.0, "I": 0.95, "N": 0.7, "F": 0.0, "regime": "very_weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:232:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Ignorance (Epistemic)", "statement": "The number of stars in the universe is even.", "gloss": "G1", "rep": 1, "response": "```json\n{\n  \"T\": 0.0,\n  \"I\": 0.95,\n  \"N\": 0.7,\n  \"F\": 0.05\n}\n```", "T": 0.0, "I": 0.95, "N": 0.7, "F": 0.05, "regime": "very_weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:233:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Ignorance (Epistemic)", "statement": "The number of stars in the universe is even.", "gloss": "G1", "rep": 2, "response": "```json\n{\n  \"T\": 0.001,\n  \"I\": 0.999,\n  \"N\": 0.8,\n  \"F\": 0.001\n}\n```", "T": 0.001, "I": 0.999, "N": 0.8, "F": 0.001, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:234:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Ignorance (Epistemic)", "statement": "The number of stars in the universe is even.", "gloss": "G1", "rep": 3, "response": "```json\n{\n  \"T\": 0.0,\n  \"I\": 0.95,\n  \"N\": 0.15,\n  \"F\": 0.0\n}\n```", "T": 0.0, "I": 0.95, "N": 0.15, "F": 0.0, "regime": "very_weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:235:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Ignorance (Epistemic)", "statement": "The number of stars in the universe is even.", "gloss": "G1", "rep": 4, "response": "```json\n{\n  \"T\": 0.005,\n  \"I\": 0.99,\n  \"N\": 0.10,\n  \"F\": 0.005\n}\n```", "T": 0.005, "I": 0.99, "N": 0.1, "F": 0.005, "regime": "very_weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:236:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Ignorance (Epistemic)", "statement": "The number of stars in the universe is even.", "gloss": "G1", "rep": 5, "response": "```json\n{\n  \"T\": 0.0,\n  \"I\": 0.95,\n  \"N\": 0.1,\n  \"F\": 0.0\n}\n```", "T": 0.0, "I": 0.95, "N": 0.1, "F": 0.0, "regime": "very_weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:237:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Ignorance (Epistemic)", "statement": "The number of stars in the universe is even.", "gloss": "G1", "rep": 6, "response": "```json\n{\n  \"T\": 0.01,\n  \"I\": 0.99,\n  \"N\": 0.80,\n  \"F\": 0.01\n}\n```", "T": 0.01, "I": 0.99, "N": 0.8, "F": 0.01, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:238:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Ignorance (Epistemic)", "statement": "The number of stars in the universe is even.", "gloss": "G1", "rep": 7, "response": "```json\n{\n  \"T\": 0.005,\n  \"I\": 0.99,\n  \"N\": 0.70,\n  \"F\": 0.005\n}\n```", "T": 0.005, "I": 0.99, "N": 0.7, "F": 0.005, "regime": "very_weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:239:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Ignorance (Epistemic)", "statement": "The number of stars in the universe is even.", "gloss": "G1", "rep": 8, "response": "```json\n{\n  \"T\": 0.0,\n  \"I\": 0.99,\n  \"N\": 0.5,\n  \"F\": 0.0\n}\n```", "T": 0.0, "I": 0.99, "N": 0.5, "F": 0.0, "regime": "very_weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:240:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Ignorance (Epistemic)", "statement": "The number of stars in the universe is even.", "gloss": "G1", "rep": 9, "response": "```json\n{\n  \"T\": 0.0,\n  \"I\": 0.95,\n  \"N\": 0.6,\n  \"F\": 0.0\n}\n```", "T": 0.0, "I": 0.95, "N": 0.6, "F": 0.0, "regime": "very_weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:241:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Ignorance (Epistemic)", "statement": "The number of stars in the universe is even.", "gloss": "G2", "rep": 0, "response": "```json\n{\"T\": 0.0, \"I\": 0.9, \"N\": 0.2, \"F\": 0.0}\n```", "T": 0.0, "I": 0.9, "N": 0.2, "F": 0.0, "regime": "very_weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:242:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Ignorance (Epistemic)", "statement": "The number of stars in the universe is even.", "gloss": "G2", "rep": 1, "response": "{\"T\": 0.1, \"I\": 0.9, \"N\": 0.1, \"F\": 0.1}", "T": 0.1, "I": 0.9, "N": 0.1, "F": 0.1, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:243:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Ignorance (Epistemic)", "statement": "The number of stars in the universe is even.", "gloss": "G2", "rep": 2, "response": "{\"T\": 0.1, \"I\": 0.9, \"N\": 0.7, \"F\": 0.1}", "T": 0.1, "I": 0.9, "N": 0.7, "F": 0.1, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:244:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Ignorance (Epistemic)", "statement": "The number of stars in the universe is even.", "gloss": "G2", "rep": 3, "response": "{\"T\": 0.0, \"I\": 0.9, \"N\": 0.1, \"F\": 0.0}", "T": 0.0, "I": 0.9, "N": 0.1, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:245:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Ignorance (Epistemic)", "statement": "The number of stars in the universe is even.", "gloss": "G2", "rep": 4, "response": "```json\n{\"T\": 0.1, \"I\": 0.9, \"N\": 0.3, \"F\": 0.1}\n```", "T": 0.1, "I": 0.9, "N": 0.3, "F": 0.1, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:246:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Ignorance (Epistemic)", "statement": "The number of stars in the universe is even.", "gloss": "G2", "rep": 5, "response": "```json\n{\"T\": 0.3, \"I\": 0.8, \"N\": 0.4, \"F\": 0.3}\n```", "T": 0.3, "I": 0.8, "N": 0.4, "F": 0.3, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:247:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Ignorance (Epistemic)", "statement": "The number of stars in the universe is even.", "gloss": "G2", "rep": 6, "response": "{\"T\": 0.0, \"I\": 1.0, \"N\": 0.2, \"F\": 0.0}", "T": 0.0, "I": 1.0, "N": 0.2, "F": 0.0, "regime": "very_weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:248:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Ignorance (Epistemic)", "statement": "The number of stars in the universe is even.", "gloss": "G2", "rep": 7, "response": "```json\n{\"T\": 0.1, \"I\": 0.9, \"N\": 0.6, \"F\": 0.1}\n```", "T": 0.1, "I": 0.9, "N": 0.6, "F": 0.1, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:249:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Ignorance (Epistemic)", "statement": "The number of stars in the universe is even.", "gloss": "G2", "rep": 8, "response": "{\"T\": 0.1, \"I\": 0.9, \"N\": 0.3, \"F\": 0.1}", "T": 0.1, "I": 0.9, "N": 0.3, "F": 0.1, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:250:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Ignorance (Epistemic)", "statement": "The number of stars in the universe is even.", "gloss": "G2", "rep": 9, "response": "```json\n{\"T\": 0.0, \"I\": 0.9, \"N\": 0.1, \"F\": 0.0}\n```", "T": 0.0, "I": 0.9, "N": 0.1, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:251:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Ignorance (Epistemic)", "statement": "The number of stars in the universe is even.", "gloss": "G2", "rep": 0, "response": "{\"T\": 0.5, \"I\": 0.9, \"N\": 0.1, \"F\": 0.5}", "T": 0.5, "I": 0.9, "N": 0.1, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:252:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Ignorance (Epistemic)", "statement": "The number of stars in the universe is even.", "gloss": "G2", "rep": 1, "response": "{\"T\": 0.5, \"I\": 1.0, \"N\": 0.0, \"F\": 0.5}", "T": 0.5, "I": 1.0, "N": 0.0, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:253:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Ignorance (Epistemic)", "statement": "The number of stars in the universe is even.", "gloss": "G2", "rep": 2, "response": "{\"T\": 0.5, \"I\": 0.9, \"N\": 0.1, \"F\": 0.5}", "T": 0.5, "I": 0.9, "N": 0.1, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:254:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Ignorance (Epistemic)", "statement": "The number of stars in the universe is even.", "gloss": "G2", "rep": 3, "response": "{\"T\": 0.5, \"I\": 0.9, \"N\": 0.1, \"F\": 0.5}", "T": 0.5, "I": 0.9, "N": 0.1, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:255:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Ignorance (Epistemic)", "statement": "The number of stars in the universe is even.", "gloss": "G2", "rep": 4, "response": "{\"T\": 0.5, \"I\": 0.9, \"N\": 0.1, \"F\": 0.5}", "T": 0.5, "I": 0.9, "N": 0.1, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:256:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Ignorance (Epistemic)", "statement": "The number of stars in the universe is even.", "gloss": "G2", "rep": 5, "response": "{\"T\": 0.5, \"I\": 0.9, \"N\": 0.1, \"F\": 0.5}", "T": 0.5, "I": 0.9, "N": 0.1, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:257:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Ignorance (Epistemic)", "statement": "The number of stars in the universe is even.", "gloss": "G2", "rep": 6, "response": "{\"T\": 0.5, \"I\": 0.9, \"N\": 0.1, \"F\": 0.5}", "T": 0.5, "I": 0.9, "N": 0.1, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:258:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Ignorance (Epistemic)", "statement": "The number of stars in the universe is even.", "gloss": "G2", "rep": 7, "response": "{\"T\": 0.5, \"I\": 0.9, \"N\": 0.1, \"F\": 0.5}", "T": 0.5, "I": 0.9, "N": 0.1, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:259:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Ignorance (Epistemic)", "statement": "The number of stars in the universe is even.", "gloss": "G2", "rep": 8, "response": "{\"T\": 0.5, \"I\": 0.9, \"N\": 0.1, \"F\": 0.5}", "T": 0.5, "I": 0.9, "N": 0.1, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:260:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Ignorance (Epistemic)", "statement": "The number of stars in the universe is even.", "gloss": "G2", "rep": 9, "response": "{\"T\": 0.5, \"I\": 1.0, \"N\": 0.0, \"F\": 0.5}", "T": 0.5, "I": 1.0, "N": 0.0, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:261:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Ignorance (Epistemic)", "statement": "The number of stars in the universe is even.", "gloss": "G2", "rep": 0, "response": "{\"T\": 0.0, \"I\": 1.0, \"N\": 0.0, \"F\": 0.0}", "T": 0.0, "I": 1.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:262:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Ignorance (Epistemic)", "statement": "The number of stars in the universe is even.", "gloss": "G2", "rep": 1, "response": "{\"T\": 0.0, \"I\": 1.0, \"N\": 0.0, \"F\": 0.0}", "T": 0.0, "I": 1.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:263:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Ignorance (Epistemic)", "statement": "The number of stars in the universe is even.", "gloss": "G2", "rep": 2, "response": "{\"T\": 0.0, \"I\": 1.0, \"N\": 0.0, \"F\": 0.0}", "T": 0.0, "I": 1.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:264:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Ignorance (Epistemic)", "statement": "The number of stars in the universe is even.", "gloss": "G2", "rep": 3, "response": "{\"T\": 0.0, \"I\": 0.9, \"N\": 0.1, \"F\": 0.0}", "T": 0.0, "I": 0.9, "N": 0.1, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:265:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Ignorance (Epistemic)", "statement": "The number of stars in the universe is even.", "gloss": "G2", "rep": 4, "response": "{\"T\": 0.0, \"I\": 1.0, \"N\": 0.0, \"F\": 0.0}", "T": 0.0, "I": 1.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:266:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Ignorance (Epistemic)", "statement": "The number of stars in the universe is even.", "gloss": "G2", "rep": 5, "response": "{\"T\": 0.0, \"I\": 1.0, \"N\": 0.0, \"F\": 0.0}", "T": 0.0, "I": 1.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:267:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Ignorance (Epistemic)", "statement": "The number of stars in the universe is even.", "gloss": "G2", "rep": 6, "response": "{\"T\": 0.0, \"I\": 1.0, \"N\": 0.0, \"F\": 0.0}", "T": 0.0, "I": 1.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:268:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Ignorance (Epistemic)", "statement": "The number of stars in the universe is even.", "gloss": "G2", "rep": 7, "response": "{\"T\": 0.0, \"I\": 1.0, \"N\": 0.0, \"F\": 0.0}", "T": 0.0, "I": 1.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:269:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Ignorance (Epistemic)", "statement": "The number of stars in the universe is even.", "gloss": "G2", "rep": 8, "response": "{\"T\": 0.0, \"I\": 1.0, \"N\": 0.0, \"F\": 0.0}", "T": 0.0, "I": 1.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:270:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Ignorance (Epistemic)", "statement": "The number of stars in the universe is even.", "gloss": "G2", "rep": 9, "response": "{\"T\": 0.0, \"I\": 1.0, \"N\": 0.0, \"F\": 0.0}", "T": 0.0, "I": 1.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:271:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Ignorance (Epistemic)", "statement": "The number of stars in the universe is even.", "gloss": "G2", "rep": 0, "response": "```json\n{\"T\": 0.0, \"I\": 1.0, \"N\": 0.0, \"F\": 0.0}\n```", "T": 0.0, "I": 1.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:272:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Ignorance (Epistemic)", "statement": "The number of stars in the universe is even.", "gloss": "G2", "rep": 1, "response": "```json\n{\"T\": 0.0, \"I\": 1.0, \"N\": 0.0, \"F\": 0.0}\n```", "T": 0.0, "I": 1.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:273:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Ignorance (Epistemic)", "statement": "The number of stars in the universe is even.", "gloss": "G2", "rep": 2, "response": "```json\n{\"T\": 0.0, \"I\": 1.0, \"N\": 0.0, \"F\": 0.0}\n```", "T": 0.0, "I": 1.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:274:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Ignorance (Epistemic)", "statement": "The number of stars in the universe is even.", "gloss": "G2", "rep": 3, "response": "```json\n{\"T\": 0.0, \"I\": 1.0, \"N\": 0.0, \"F\": 0.0}\n```", "T": 0.0, "I": 1.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:275:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Ignorance (Epistemic)", "statement": "The number of stars in the universe is even.", "gloss": "G2", "rep": 4, "response": "```json\n{\"T\": 0.1, \"I\": 0.8, \"N\": 0.1, \"F\": 0.1}\n```", "T": 0.1, "I": 0.8, "N": 0.1, "F": 0.1, "regime": "very_weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:276:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Ignorance (Epistemic)", "statement": "The number of stars in the universe is even.", "gloss": "G2", "rep": 5, "response": "```json\n{\"T\": 0.0, \"I\": 1.0, \"N\": 0.0, \"F\": 0.0}\n```", "T": 0.0, "I": 1.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:277:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Ignorance (Epistemic)", "statement": "The number of stars in the universe is even.", "gloss": "G2", "rep": 6, "response": "```json\n{\"T\": 0.0, \"I\": 0.9, \"N\": 0.1, \"F\": 0.0}\n```", "T": 0.0, "I": 0.9, "N": 0.1, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:278:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Ignorance (Epistemic)", "statement": "The number of stars in the universe is even.", "gloss": "G2", "rep": 7, "response": "```json\n{\"T\": 0.1, \"I\": 0.9, \"N\": 0.0, \"F\": 0.1}\n```", "T": 0.1, "I": 0.9, "N": 0.0, "F": 0.1, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:279:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Ignorance (Epistemic)", "statement": "The number of stars in the universe is even.", "gloss": "G2", "rep": 8, "response": "```json\n{\"T\": 0.2, \"I\": 0.8, \"N\": 0.5, \"F\": 0.2}\n```", "T": 0.2, "I": 0.8, "N": 0.5, "F": 0.2, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:280:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Ignorance (Epistemic)", "statement": "The number of stars in the universe is even.", "gloss": "G2", "rep": 9, "response": "```json\n{\"T\": 0.1, \"I\": 0.9, \"N\": 0.2, \"F\": 0.1}\n```", "T": 0.1, "I": 0.9, "N": 0.2, "F": 0.1, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:281:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Ignorance (Epistemic)", "statement": "The number of stars in the universe is even.", "gloss": "G2", "rep": 0, "response": "{\"T\": 0.0, \"I\": 1.0, \"N\": 0.0, \"F\": 0.0}", "T": 0.0, "I": 1.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:282:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Ignorance (Epistemic)", "statement": "The number of stars in the universe is even.", "gloss": "G2", "rep": 1, "response": "{\"T\": 0.0, \"I\": 1.0, \"N\": 0.0, \"F\": 0.0}", "T": 0.0, "I": 1.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:283:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Ignorance (Epistemic)", "statement": "The number of stars in the universe is even.", "gloss": "G2", "rep": 2, "response": "{\"T\": 0.0, \"I\": 1.0, \"N\": 0.0, \"F\": 0.0}", "T": 0.0, "I": 1.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:284:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Ignorance (Epistemic)", "statement": "The number of stars in the universe is even.", "gloss": "G2", "rep": 3, "response": "{\"T\": 0.5, \"I\": 1.0, \"N\": 0.0, \"F\": 0.5}", "T": 0.5, "I": 1.0, "N": 0.0, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:285:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Ignorance (Epistemic)", "statement": "The number of stars in the universe is even.", "gloss": "G2", "rep": 4, "response": "{\"T\": 0.5, \"I\": 1.0, \"N\": 0.0, \"F\": 0.5}", "T": 0.5, "I": 1.0, "N": 0.0, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:286:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Ignorance (Epistemic)", "statement": "The number of stars in the universe is even.", "gloss": "G2", "rep": 5, "response": "{\"T\": 0.5, \"I\": 1.0, \"N\": 0.0, \"F\": 0.5}", "T": 0.5, "I": 1.0, "N": 0.0, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:287:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Ignorance (Epistemic)", "statement": "The number of stars in the universe is even.", "gloss": "G2", "rep": 6, "response": "{\"T\": 0.5, \"I\": 1.0, \"N\": 0.0, \"F\": 0.5}", "T": 0.5, "I": 1.0, "N": 0.0, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:288:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Ignorance (Epistemic)", "statement": "The number of stars in the universe is even.", "gloss": "G2", "rep": 7, "response": "{\"T\": 0.5, \"I\": 1.0, \"N\": 0.0, \"F\": 0.5}", "T": 0.5, "I": 1.0, "N": 0.0, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:289:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Ignorance (Epistemic)", "statement": "The number of stars in the universe is even.", "gloss": "G2", "rep": 8, "response": "{\"T\": 0.5, \"I\": 1.0, \"N\": 0.0, \"F\": 0.5}", "T": 0.5, "I": 1.0, "N": 0.0, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:290:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Ignorance (Epistemic)", "statement": "The number of stars in the universe is even.", "gloss": "G2", "rep": 9, "response": "{\"T\": 0.5, \"I\": 1.0, \"N\": 0.0, \"F\": 0.5}", "T": 0.5, "I": 1.0, "N": 0.0, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:291:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Ignorance (Epistemic)", "statement": "The number of stars in the universe is even.", "gloss": "G2", "rep": 0, "response": "```json\n{\n  \"T\": 0.0,\n  \"I\": 0.95,\n  \"N\": 0.05,\n  \"F\": 0.0\n}\n```", "T": 0.0, "I": 0.95, "N": 0.05, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:292:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Ignorance (Epistemic)", "statement": "The number of stars in the universe is even.", "gloss": "G2", "rep": 1, "response": "```json\n{\n  \"T\": 0.0,\n  \"I\": 0.95,\n  \"N\": 0.15,\n  \"F\": 0.0\n}\n```", "T": 0.0, "I": 0.95, "N": 0.15, "F": 0.0, "regime": "very_weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:293:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Ignorance (Epistemic)", "statement": "The number of stars in the universe is even.", "gloss": "G2", "rep": 2, "response": "```json\n{\n  \"T\": 0.0,\n  \"I\": 0.95,\n  \"N\": 0.05,\n  \"F\": 0.0\n}\n```", "T": 0.0, "I": 0.95, "N": 0.05, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:294:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Ignorance (Epistemic)", "statement": "The number of stars in the universe is even.", "gloss": "G2", "rep": 3, "response": "```json\n{\n  \"T\": 0.0,\n  \"I\": 0.95,\n  \"N\": 0.05,\n  \"F\": 0.0\n}\n```", "T": 0.0, "I": 0.95, "N": 0.05, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:295:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Ignorance (Epistemic)", "statement": "The number of stars in the universe is even.", "gloss": "G2", "rep": 4, "response": "```json\n{\n  \"T\": 0.0,\n  \"I\": 0.95,\n  \"N\": 0.05,\n  \"F\": 0.0\n}\n```", "T": 0.0, "I": 0.95, "N": 0.05, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:296:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Ignorance (Epistemic)", "statement": "The number of stars in the universe is even.", "gloss": "G2", "rep": 5, "response": "```json\n{\n  \"T\": 0.0,\n  \"I\": 0.95,\n  \"N\": 0.05,\n  \"F\": 0.0\n}\n```", "T": 0.0, "I": 0.95, "N": 0.05, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:297:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Ignorance (Epistemic)", "statement": "The number of stars in the universe is even.", "gloss": "G2", "rep": 6, "response": "```json\n{\n  \"T\": 0.0,\n  \"I\": 0.95,\n  \"N\": 0.05,\n  \"F\": 0.0\n}\n```", "T": 0.0, "I": 0.95, "N": 0.05, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:298:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Ignorance (Epistemic)", "statement": "The number of stars in the universe is even.", "gloss": "G2", "rep": 7, "response": "```json\n{\n  \"T\": 0.0,\n  \"I\": 0.95,\n  \"N\": 0.1,\n  \"F\": 0.0\n}\n```", "T": 0.0, "I": 0.95, "N": 0.1, "F": 0.0, "regime": "very_weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:299:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Ignorance (Epistemic)", "statement": "The number of stars in the universe is even.", "gloss": "G2", "rep": 8, "response": "```json\n{\n  \"T\": 0.0,\n  \"I\": 0.95,\n  \"N\": 0.3,\n  \"F\": 0.0\n}\n```", "T": 0.0, "I": 0.95, "N": 0.3, "F": 0.0, "regime": "very_weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:300:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Ignorance (Epistemic)", "statement": "The number of stars in the universe is even.", "gloss": "G2", "rep": 9, "response": "```json\n{\n  \"T\": 0.0,\n  \"I\": 0.95,\n  \"N\": 0.1,\n  \"F\": 0.0\n}\n```", "T": 0.0, "I": 0.95, "N": 0.1, "F": 0.0, "regime": "very_weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:301:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Ignorance (Epistemic)", "statement": "The number of stars in the universe is even.", "gloss": "G3", "rep": 0, "response": "```json\n{\"T\": 0.1, \"I\": 0.9, \"N\": 0.4, \"F\": 0.1}\n```", "T": 0.1, "I": 0.9, "N": 0.4, "F": 0.1, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:302:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Ignorance (Epistemic)", "statement": "The number of stars in the universe is even.", "gloss": "G3", "rep": 1, "response": "```json\n{\"T\": 0.0, \"I\": 1.0, \"N\": 0.0, \"F\": 0.0}\n```", "T": 0.0, "I": 1.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:303:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Ignorance (Epistemic)", "statement": "The number of stars in the universe is even.", "gloss": "G3", "rep": 2, "response": "{\"T\": 0.5, \"I\": 0.9, \"N\": 0.5, \"F\": 0.5}", "T": 0.5, "I": 0.9, "N": 0.5, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:304:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Ignorance (Epistemic)", "statement": "The number of stars in the universe is even.", "gloss": "G3", "rep": 3, "response": "```json\n{\"T\": 0.0, \"I\": 1.0, \"N\": 0.0, \"F\": 0.0}\n```", "T": 0.0, "I": 1.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:305:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Ignorance (Epistemic)", "statement": "The number of stars in the universe is even.", "gloss": "G3", "rep": 4, "response": "```json\n{\"T\": 0.1, \"I\": 0.9, \"N\": 0.5, \"F\": 0.1}\n```", "T": 0.1, "I": 0.9, "N": 0.5, "F": 0.1, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:306:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Ignorance (Epistemic)", "statement": "The number of stars in the universe is even.", "gloss": "G3", "rep": 5, "response": "```json\n{\"T\": 0.5, \"I\": 0.9, \"N\": 0.1, \"F\": 0.5}\n```", "T": 0.5, "I": 0.9, "N": 0.1, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:307:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Ignorance (Epistemic)", "statement": "The number of stars in the universe is even.", "gloss": "G3", "rep": 6, "response": "```json\n{\"T\": 0.5, \"I\": 0.9, \"N\": 0.1, \"F\": 0.5}\n```", "T": 0.5, "I": 0.9, "N": 0.1, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:308:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Ignorance (Epistemic)", "statement": "The number of stars in the universe is even.", "gloss": "G3", "rep": 7, "response": "```json\n{\"T\": 0.0, \"I\": 0.9, \"N\": 0.1, \"F\": 0.0}\n```", "T": 0.0, "I": 0.9, "N": 0.1, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:309:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Ignorance (Epistemic)", "statement": "The number of stars in the universe is even.", "gloss": "G3", "rep": 8, "response": "```json\n{\"T\": 0.0, \"I\": 0.9, \"N\": 0.2, \"F\": 0.1}\n```", "T": 0.0, "I": 0.9, "N": 0.2, "F": 0.1, "regime": "very_weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:310:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Ignorance (Epistemic)", "statement": "The number of stars in the universe is even.", "gloss": "G3", "rep": 9, "response": "```json\n{\"T\": 0.1, \"I\": 0.9, \"N\": 0.5, \"F\": 0.1}\n```", "T": 0.1, "I": 0.9, "N": 0.5, "F": 0.1, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:311:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Ignorance (Epistemic)", "statement": "The number of stars in the universe is even.", "gloss": "G3", "rep": 0, "response": "{\"T\": 0.5, \"I\": 0.9, \"N\": 0.5, \"F\": 0.5}", "T": 0.5, "I": 0.9, "N": 0.5, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:312:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Ignorance (Epistemic)", "statement": "The number of stars in the universe is even.", "gloss": "G3", "rep": 1, "response": "{\"T\": 0.5, \"I\": 0.9, \"N\": 0.5, \"F\": 0.5}", "T": 0.5, "I": 0.9, "N": 0.5, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:313:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Ignorance (Epistemic)", "statement": "The number of stars in the universe is even.", "gloss": "G3", "rep": 2, "response": "{\"T\": 0.5, \"I\": 0.9, \"N\": 0.5, \"F\": 0.5}", "T": 0.5, "I": 0.9, "N": 0.5, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:314:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Ignorance (Epistemic)", "statement": "The number of stars in the universe is even.", "gloss": "G3", "rep": 3, "response": "{\"T\": 0.5, \"I\": 0.9, \"N\": 0.5, \"F\": 0.5}", "T": 0.5, "I": 0.9, "N": 0.5, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:315:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Ignorance (Epistemic)", "statement": "The number of stars in the universe is even.", "gloss": "G3", "rep": 4, "response": "{\"T\": 0.5, \"I\": 0.9, \"N\": 0.5, \"F\": 0.5}", "T": 0.5, "I": 0.9, "N": 0.5, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:316:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Ignorance (Epistemic)", "statement": "The number of stars in the universe is even.", "gloss": "G3", "rep": 5, "response": "{\"T\": 0.5, \"I\": 0.9, \"N\": 0.5, \"F\": 0.5}", "T": 0.5, "I": 0.9, "N": 0.5, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:317:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Ignorance (Epistemic)", "statement": "The number of stars in the universe is even.", "gloss": "G3", "rep": 6, "response": "{\"T\": 0.5, \"I\": 0.9, \"N\": 0.5, \"F\": 0.5}", "T": 0.5, "I": 0.9, "N": 0.5, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:318:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Ignorance (Epistemic)", "statement": "The number of stars in the universe is even.", "gloss": "G3", "rep": 7, "response": "{\"T\": 0.5, \"I\": 0.9, \"N\": 0.5, \"F\": 0.5}", "T": 0.5, "I": 0.9, "N": 0.5, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:319:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Ignorance (Epistemic)", "statement": "The number of stars in the universe is even.", "gloss": "G3", "rep": 8, "response": "{\"T\": 0.5, \"I\": 0.9, \"N\": 0.5, \"F\": 0.5}", "T": 0.5, "I": 0.9, "N": 0.5, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:320:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Ignorance (Epistemic)", "statement": "The number of stars in the universe is even.", "gloss": "G3", "rep": 9, "response": "{\"T\": 0.5, \"I\": 0.9, \"N\": 0.5, \"F\": 0.5}", "T": 0.5, "I": 0.9, "N": 0.5, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:321:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Ignorance (Epistemic)", "statement": "The number of stars in the universe is even.", "gloss": "G3", "rep": 0, "response": "{\"T\": 0.0, \"I\": 0.9, \"N\": 0.1, \"F\": 0.0}", "T": 0.0, "I": 0.9, "N": 0.1, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:322:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Ignorance (Epistemic)", "statement": "The number of stars in the universe is even.", "gloss": "G3", "rep": 1, "response": "{\"T\": 0.0, \"I\": 0.9, \"N\": 0.1, \"F\": 0.0}", "T": 0.0, "I": 0.9, "N": 0.1, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:323:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Ignorance (Epistemic)", "statement": "The number of stars in the universe is even.", "gloss": "G3", "rep": 2, "response": "{\"T\": 0.0, \"I\": 0.9, \"N\": 0.1, \"F\": 0.0}", "T": 0.0, "I": 0.9, "N": 0.1, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:324:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Ignorance (Epistemic)", "statement": "The number of stars in the universe is even.", "gloss": "G3", "rep": 3, "response": "{\"T\": 0.0, \"I\": 0.9, \"N\": 0.1, \"F\": 0.0}", "T": 0.0, "I": 0.9, "N": 0.1, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:325:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Ignorance (Epistemic)", "statement": "The number of stars in the universe is even.", "gloss": "G3", "rep": 4, "response": "{\"T\": 0.0, \"I\": 0.9, \"N\": 0.1, \"F\": 0.0}", "T": 0.0, "I": 0.9, "N": 0.1, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:326:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Ignorance (Epistemic)", "statement": "The number of stars in the universe is even.", "gloss": "G3", "rep": 5, "response": "{\"T\": 0.0, \"I\": 0.9, \"N\": 0.1, \"F\": 0.0}", "T": 0.0, "I": 0.9, "N": 0.1, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:327:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Ignorance (Epistemic)", "statement": "The number of stars in the universe is even.", "gloss": "G3", "rep": 6, "response": "{\"T\": 0.0, \"I\": 0.9, \"N\": 0.1, \"F\": 0.0}", "T": 0.0, "I": 0.9, "N": 0.1, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:328:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Ignorance (Epistemic)", "statement": "The number of stars in the universe is even.", "gloss": "G3", "rep": 7, "response": "{\"T\": 0.0, \"I\": 0.9, \"N\": 0.1, \"F\": 0.0}", "T": 0.0, "I": 0.9, "N": 0.1, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:329:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Ignorance (Epistemic)", "statement": "The number of stars in the universe is even.", "gloss": "G3", "rep": 8, "response": "{\"T\": 0.0, \"I\": 0.9, \"N\": 0.1, \"F\": 0.0}", "T": 0.0, "I": 0.9, "N": 0.1, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:330:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Ignorance (Epistemic)", "statement": "The number of stars in the universe is even.", "gloss": "G3", "rep": 9, "response": "{\"T\": 0.0, \"I\": 0.9, \"N\": 0.1, \"F\": 0.0}", "T": 0.0, "I": 0.9, "N": 0.1, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:331:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Ignorance (Epistemic)", "statement": "The number of stars in the universe is even.", "gloss": "G3", "rep": 0, "response": "```json\n{\"T\": 0.0, \"I\": 1.0, \"N\": 0.0, \"F\": 0.0}\n```", "T": 0.0, "I": 1.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:332:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Ignorance (Epistemic)", "statement": "The number of stars in the universe is even.", "gloss": "G3", "rep": 1, "response": "```json\n{\"T\": 0.1, \"I\": 0.9, \"N\": 0.5, \"F\": 0.1}\n```", "T": 0.1, "I": 0.9, "N": 0.5, "F": 0.1, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:333:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Ignorance (Epistemic)", "statement": "The number of stars in the universe is even.", "gloss": "G3", "rep": 2, "response": "```json\n{\"T\": 0.2, \"I\": 0.8, \"N\": 0.5, \"F\": 0.2}\n```", "T": 0.2, "I": 0.8, "N": 0.5, "F": 0.2, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:334:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Ignorance (Epistemic)", "statement": "The number of stars in the universe is even.", "gloss": "G3", "rep": 3, "response": "```json\n{\"T\": 0.5, \"I\": 0.9, \"N\": 0.3, \"F\": 0.5}\n```", "T": 0.5, "I": 0.9, "N": 0.3, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:335:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Ignorance (Epistemic)", "statement": "The number of stars in the universe is even.", "gloss": "G3", "rep": 4, "response": "```json\n{\"T\": 0.0, \"I\": 1.0, \"N\": 0.0, \"F\": 0.0}\n```", "T": 0.0, "I": 1.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:336:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Ignorance (Epistemic)", "statement": "The number of stars in the universe is even.", "gloss": "G3", "rep": 5, "response": "```json\n{\"T\": 0.0, \"I\": 1.0, \"N\": 0.0, \"F\": 0.0}\n```", "T": 0.0, "I": 1.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:337:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Ignorance (Epistemic)", "statement": "The number of stars in the universe is even.", "gloss": "G3", "rep": 6, "response": "```json\n{\"T\": 0.0, \"I\": 1.0, \"N\": 0.0, \"F\": 0.0}\n```", "T": 0.0, "I": 1.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:338:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Ignorance (Epistemic)", "statement": "The number of stars in the universe is even.", "gloss": "G3", "rep": 7, "response": "```json\n{\"T\": 0.1, \"I\": 0.9, \"N\": 0.5, \"F\": 0.1}\n```", "T": 0.1, "I": 0.9, "N": 0.5, "F": 0.1, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:339:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Ignorance (Epistemic)", "statement": "The number of stars in the universe is even.", "gloss": "G3", "rep": 8, "response": "```json\n{\"T\": 0.0, \"I\": 1.0, \"N\": 0.0, \"F\": 0.0}\n```", "T": 0.0, "I": 1.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:340:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Ignorance (Epistemic)", "statement": "The number of stars in the universe is even.", "gloss": "G3", "rep": 9, "response": "```json\n{\"T\": 0.1, \"I\": 0.9, \"N\": 0.5, \"F\": 0.1}\n```", "T": 0.1, "I": 0.9, "N": 0.5, "F": 0.1, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:341:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Ignorance (Epistemic)", "statement": "The number of stars in the universe is even.", "gloss": "G3", "rep": 0, "response": "{\"T\": 0.5, \"I\": 1.0, \"N\": 0.0, \"F\": 0.5}", "T": 0.5, "I": 1.0, "N": 0.0, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:342:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Ignorance (Epistemic)", "statement": "The number of stars in the universe is even.", "gloss": "G3", "rep": 1, "response": "{\"T\": 0.5, \"I\": 1.0, \"N\": 0.0, \"F\": 0.5}", "T": 0.5, "I": 1.0, "N": 0.0, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:343:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Ignorance (Epistemic)", "statement": "The number of stars in the universe is even.", "gloss": "G3", "rep": 2, "response": "{\"T\": 0.5, \"I\": 1.0, \"N\": 0.0, \"F\": 0.5}", "T": 0.5, "I": 1.0, "N": 0.0, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:344:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Ignorance (Epistemic)", "statement": "The number of stars in the universe is even.", "gloss": "G3", "rep": 3, "response": "{\"T\": 0.5, \"I\": 1.0, \"N\": 0.0, \"F\": 0.5}", "T": 0.5, "I": 1.0, "N": 0.0, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:345:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Ignorance (Epistemic)", "statement": "The number of stars in the universe is even.", "gloss": "G3", "rep": 4, "response": "{\"T\": 0.5, \"I\": 1.0, \"N\": 0.0, \"F\": 0.5}", "T": 0.5, "I": 1.0, "N": 0.0, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:346:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Ignorance (Epistemic)", "statement": "The number of stars in the universe is even.", "gloss": "G3", "rep": 5, "response": "{\"T\": 0.5, \"I\": 1.0, \"N\": 0.0, \"F\": 0.5}", "T": 0.5, "I": 1.0, "N": 0.0, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:347:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Ignorance (Epistemic)", "statement": "The number of stars in the universe is even.", "gloss": "G3", "rep": 6, "response": "{\"T\": 0.5, \"I\": 1.0, \"N\": 0.0, \"F\": 0.5}", "T": 0.5, "I": 1.0, "N": 0.0, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:348:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Ignorance (Epistemic)", "statement": "The number of stars in the universe is even.", "gloss": "G3", "rep": 7, "response": "{\"T\": 0.5, \"I\": 1.0, \"N\": 0.0, \"F\": 0.5}", "T": 0.5, "I": 1.0, "N": 0.0, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:349:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Ignorance (Epistemic)", "statement": "The number of stars in the universe is even.", "gloss": "G3", "rep": 8, "response": "{\"T\": 0.5, \"I\": 1.0, \"N\": 0.5, \"F\": 0.5}", "T": 0.5, "I": 1.0, "N": 0.5, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:350:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Ignorance (Epistemic)", "statement": "The number of stars in the universe is even.", "gloss": "G3", "rep": 9, "response": "{\"T\": 0.5, \"I\": 1.0, \"N\": 0.5, \"F\": 0.5}", "T": 0.5, "I": 1.0, "N": 0.5, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:351:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Ignorance (Epistemic)", "statement": "The number of stars in the universe is even.", "gloss": "G3", "rep": 0, "response": "```json\n{\n  \"T\": 0.01,\n  \"I\": 0.98,\n  \"N\": 0.05,\n  \"F\": 0.01\n}\n```", "T": 0.01, "I": 0.98, "N": 0.05, "F": 0.01, "regime": "very_weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:352:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Ignorance (Epistemic)", "statement": "The number of stars in the universe is even.", "gloss": "G3", "rep": 1, "response": "```json\n{\n  \"T\": 0.0,\n  \"I\": 0.95,\n  \"N\": 0.05,\n  \"F\": 0.0\n}\n```", "T": 0.0, "I": 0.95, "N": 0.05, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:353:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Ignorance (Epistemic)", "statement": "The number of stars in the universe is even.", "gloss": "G3", "rep": 2, "response": "```json\n{\n  \"T\": 0.0,\n  \"I\": 0.95,\n  \"N\": 0.05,\n  \"F\": 0.0\n}\n```", "T": 0.0, "I": 0.95, "N": 0.05, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:354:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Ignorance (Epistemic)", "statement": "The number of stars in the universe is even.", "gloss": "G3", "rep": 3, "response": "```json\n{\n  \"T\": 0.01,\n  \"I\": 0.98,\n  \"N\": 0.05,\n  \"F\": 0.01\n}\n```", "T": 0.01, "I": 0.98, "N": 0.05, "F": 0.01, "regime": "very_weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:355:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Ignorance (Epistemic)", "statement": "The number of stars in the universe is even.", "gloss": "G3", "rep": 4, "response": "```json\n{\n  \"T\": 0.0,\n  \"I\": 0.95,\n  \"N\": 0.05,\n  \"F\": 0.0\n}\n```", "T": 0.0, "I": 0.95, "N": 0.05, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:356:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Ignorance (Epistemic)", "statement": "The number of stars in the universe is even.", "gloss": "G3", "rep": 5, "response": "```json\n{\n  \"T\": 0.005,\n  \"I\": 0.99,\n  \"N\": 0.02,\n  \"F\": 0.005\n}\n```", "T": 0.005, "I": 0.99, "N": 0.02, "F": 0.005, "regime": "very_weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:357:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Ignorance (Epistemic)", "statement": "The number of stars in the universe is even.", "gloss": "G3", "rep": 6, "response": "```json\n{\n  \"T\": 0.01,\n  \"I\": 0.99,\n  \"N\": 0.05,\n  \"F\": 0.01\n}\n```", "T": 0.01, "I": 0.99, "N": 0.05, "F": 0.01, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:358:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Ignorance (Epistemic)", "statement": "The number of stars in the universe is even.", "gloss": "G3", "rep": 7, "response": "```json\n{\n  \"T\": 0.0,\n  \"I\": 0.98,\n  \"N\": 0.05,\n  \"F\": 0.0\n}\n```", "T": 0.0, "I": 0.98, "N": 0.05, "F": 0.0, "regime": "very_weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:359:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Ignorance (Epistemic)", "statement": "The number of stars in the universe is even.", "gloss": "G3", "rep": 8, "response": "```json\n{\n  \"T\": 0.01,\n  \"I\": 0.95,\n  \"N\": 0.05,\n  \"F\": 0.01\n}\n```", "T": 0.01, "I": 0.95, "N": 0.05, "F": 0.01, "regime": "very_weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:360:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Ignorance (Epistemic)", "statement": "The number of stars in the universe is even.", "gloss": "G3", "rep": 9, "response": "```json\n{\n  \"T\": 0.005,\n  \"I\": 0.99,\n  \"N\": 0.001,\n  \"F\": 0.004\n}\n```", "T": 0.005, "I": 0.99, "N": 0.001, "F": 0.004, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:361:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Vagueness (Fuzzy)", "statement": "John is 1.75 meters tall, therefore John is tall.", "gloss": "G1", "rep": 0, "response": "```json\n{\"T\": 0.5, \"I\": 0.3, \"N\": 0.4, \"F\": 0.5}\n```", "T": 0.5, "I": 0.3, "N": 0.4, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:362:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Vagueness (Fuzzy)", "statement": "John is 1.75 meters tall, therefore John is tall.", "gloss": "G1", "rep": 1, "response": "```json\n{\"T\": 0.4, \"I\": 0.3, \"N\": 0.2, \"F\": 0.4}\n```", "T": 0.4, "I": 0.3, "N": 0.2, "F": 0.4, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:363:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Vagueness (Fuzzy)", "statement": "John is 1.75 meters tall, therefore John is tall.", "gloss": "G1", "rep": 2, "response": "{\"T\": 0.3, \"I\": 0.5, \"N\": 0.2, \"F\": 0.4}", "T": 0.3, "I": 0.5, "N": 0.2, "F": 0.4, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:364:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Vagueness (Fuzzy)", "statement": "John is 1.75 meters tall, therefore John is tall.", "gloss": "G1", "rep": 3, "response": "```json\n{\"T\": 0.5, \"I\": 0.3, \"N\": 0.4, \"F\": 0.5}\n```", "T": 0.5, "I": 0.3, "N": 0.4, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:365:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Vagueness (Fuzzy)", "statement": "John is 1.75 meters tall, therefore John is tall.", "gloss": "G1", "rep": 4, "response": "```json\n{\"T\": 0.6, \"I\": 0.3, \"N\": 0.2, \"F\": 0.4}\n```", "T": 0.6, "I": 0.3, "N": 0.2, "F": 0.4, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:366:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Vagueness (Fuzzy)", "statement": "John is 1.75 meters tall, therefore John is tall.", "gloss": "G1", "rep": 5, "response": "```json\n{\"T\": 0.4, \"I\": 0.3, \"N\": 0.2, \"F\": 0.4}\n```", "T": 0.4, "I": 0.3, "N": 0.2, "F": 0.4, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:367:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Vagueness (Fuzzy)", "statement": "John is 1.75 meters tall, therefore John is tall.", "gloss": "G1", "rep": 6, "response": "```json\n{\"T\": 0.4, \"I\": 0.4, \"N\": 0.2, \"F\": 0.5}\n```", "T": 0.4, "I": 0.4, "N": 0.2, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:368:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Vagueness (Fuzzy)", "statement": "John is 1.75 meters tall, therefore John is tall.", "gloss": "G1", "rep": 7, "response": "```json\n{\"T\": 0.4, \"I\": 0.3, \"N\": 0.2, \"F\": 0.6}\n```", "T": 0.4, "I": 0.3, "N": 0.2, "F": 0.6, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:369:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Vagueness (Fuzzy)", "statement": "John is 1.75 meters tall, therefore John is tall.", "gloss": "G1", "rep": 8, "response": "```json\n{\"T\": 0.6, \"I\": 0.3, \"N\": 0.1, \"F\": 0.4}\n```", "T": 0.6, "I": 0.3, "N": 0.1, "F": 0.4, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:370:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Vagueness (Fuzzy)", "statement": "John is 1.75 meters tall, therefore John is tall.", "gloss": "G1", "rep": 9, "response": "```json\n{\"T\": 0.5, \"I\": 0.3, \"N\": 0.2, \"F\": 0.5}\n```", "T": 0.5, "I": 0.3, "N": 0.2, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:371:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Vagueness (Fuzzy)", "statement": "John is 1.75 meters tall, therefore John is tall.", "gloss": "G1", "rep": 0, "response": "{\"T\": 0.6, \"I\": 0.7, \"N\": 0.3, \"F\": 0.4}", "T": 0.6, "I": 0.7, "N": 0.3, "F": 0.4, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:372:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Vagueness (Fuzzy)", "statement": "John is 1.75 meters tall, therefore John is tall.", "gloss": "G1", "rep": 1, "response": "{\"T\": 0.6, \"I\": 0.7, \"N\": 0.3, \"F\": 0.4}", "T": 0.6, "I": 0.7, "N": 0.3, "F": 0.4, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:373:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Vagueness (Fuzzy)", "statement": "John is 1.75 meters tall, therefore John is tall.", "gloss": "G1", "rep": 2, "response": "{\"T\": 0.6, \"I\": 0.7, \"N\": 0.3, \"F\": 0.4}", "T": 0.6, "I": 0.7, "N": 0.3, "F": 0.4, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:374:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Vagueness (Fuzzy)", "statement": "John is 1.75 meters tall, therefore John is tall.", "gloss": "G1", "rep": 3, "response": "{\"T\": 0.6, \"I\": 0.7, \"N\": 0.3, \"F\": 0.4}", "T": 0.6, "I": 0.7, "N": 0.3, "F": 0.4, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:375:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Vagueness (Fuzzy)", "statement": "John is 1.75 meters tall, therefore John is tall.", "gloss": "G1", "rep": 4, "response": "{\"T\": 0.6, \"I\": 0.7, \"N\": 0.3, \"F\": 0.4}", "T": 0.6, "I": 0.7, "N": 0.3, "F": 0.4, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:376:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Vagueness (Fuzzy)", "statement": "John is 1.75 meters tall, therefore John is tall.", "gloss": "G1", "rep": 5, "response": "{\"T\": 0.6, \"I\": 0.7, \"N\": 0.3, \"F\": 0.4}", "T": 0.6, "I": 0.7, "N": 0.3, "F": 0.4, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:377:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Vagueness (Fuzzy)", "statement": "John is 1.75 meters tall, therefore John is tall.", "gloss": "G1", "rep": 6, "response": "{\"T\": 0.6, \"I\": 0.7, \"N\": 0.3, \"F\": 0.4}", "T": 0.6, "I": 0.7, "N": 0.3, "F": 0.4, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:378:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Vagueness (Fuzzy)", "statement": "John is 1.75 meters tall, therefore John is tall.", "gloss": "G1", "rep": 7, "response": "{\"T\": 0.6, \"I\": 0.7, \"N\": 0.3, \"F\": 0.4}", "T": 0.6, "I": 0.7, "N": 0.3, "F": 0.4, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:379:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Vagueness (Fuzzy)", "statement": "John is 1.75 meters tall, therefore John is tall.", "gloss": "G1", "rep": 8, "response": "{\"T\": 0.6, \"I\": 0.7, \"N\": 0.3, \"F\": 0.4}", "T": 0.6, "I": 0.7, "N": 0.3, "F": 0.4, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:380:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Vagueness (Fuzzy)", "statement": "John is 1.75 meters tall, therefore John is tall.", "gloss": "G1", "rep": 9, "response": "{\"T\": 0.6, \"I\": 0.7, \"N\": 0.3, \"F\": 0.4}", "T": 0.6, "I": 0.7, "N": 0.3, "F": 0.4, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:381:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Vagueness (Fuzzy)", "statement": "John is 1.75 meters tall, therefore John is tall.", "gloss": "G1", "rep": 0, "response": "{\"T\": 0.7, \"I\": 0.3, \"N\": 0.2, \"F\": 0.1}", "T": 0.7, "I": 0.3, "N": 0.2, "F": 0.1, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:382:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Vagueness (Fuzzy)", "statement": "John is 1.75 meters tall, therefore John is tall.", "gloss": "G1", "rep": 1, "response": "{\"T\": 0.7, \"I\": 0.3, \"N\": 0.2, \"F\": 0.1}", "T": 0.7, "I": 0.3, "N": 0.2, "F": 0.1, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:383:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Vagueness (Fuzzy)", "statement": "John is 1.75 meters tall, therefore John is tall.", "gloss": "G1", "rep": 2, "response": "{\"T\": 0.7, \"I\": 0.3, \"N\": 0.2, \"F\": 0.1}", "T": 0.7, "I": 0.3, "N": 0.2, "F": 0.1, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:384:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Vagueness (Fuzzy)", "statement": "John is 1.75 meters tall, therefore John is tall.", "gloss": "G1", "rep": 3, "response": "{\"T\": 0.7, \"I\": 0.3, \"N\": 0.2, \"F\": 0.1}", "T": 0.7, "I": 0.3, "N": 0.2, "F": 0.1, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:385:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Vagueness (Fuzzy)", "statement": "John is 1.75 meters tall, therefore John is tall.", "gloss": "G1", "rep": 4, "response": "{\"T\": 0.7, \"I\": 0.3, \"N\": 0.2, \"F\": 0.1}", "T": 0.7, "I": 0.3, "N": 0.2, "F": 0.1, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:386:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Vagueness (Fuzzy)", "statement": "John is 1.75 meters tall, therefore John is tall.", "gloss": "G1", "rep": 5, "response": "{\"T\": 0.7, \"I\": 0.3, \"N\": 0.2, \"F\": 0.1}", "T": 0.7, "I": 0.3, "N": 0.2, "F": 0.1, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:387:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Vagueness (Fuzzy)", "statement": "John is 1.75 meters tall, therefore John is tall.", "gloss": "G1", "rep": 6, "response": "{\"T\": 0.7, \"I\": 0.3, \"N\": 0.2, \"F\": 0.1}", "T": 0.7, "I": 0.3, "N": 0.2, "F": 0.1, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:388:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Vagueness (Fuzzy)", "statement": "John is 1.75 meters tall, therefore John is tall.", "gloss": "G1", "rep": 7, "response": "{\"T\": 0.7, \"I\": 0.3, \"N\": 0.2, \"F\": 0.1}", "T": 0.7, "I": 0.3, "N": 0.2, "F": 0.1, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:389:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Vagueness (Fuzzy)", "statement": "John is 1.75 meters tall, therefore John is tall.", "gloss": "G1", "rep": 8, "response": "{\"T\": 0.7, \"I\": 0.3, \"N\": 0.2, \"F\": 0.1}", "T": 0.7, "I": 0.3, "N": 0.2, "F": 0.1, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:390:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Vagueness (Fuzzy)", "statement": "John is 1.75 meters tall, therefore John is tall.", "gloss": "G1", "rep": 9, "response": "{\"T\": 0.6, \"I\": 0.3, \"N\": 0.2, \"F\": 0.4}", "T": 0.6, "I": 0.3, "N": 0.2, "F": 0.4, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:391:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Vagueness (Fuzzy)", "statement": "John is 1.75 meters tall, therefore John is tall.", "gloss": "G1", "rep": 0, "response": "```json\n{\"T\": 0.5, \"I\": 0.2, \"N\": 0.3, \"F\": 0.4}\n```", "T": 0.5, "I": 0.2, "N": 0.3, "F": 0.4, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:392:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Vagueness (Fuzzy)", "statement": "John is 1.75 meters tall, therefore John is tall.", "gloss": "G1", "rep": 1, "response": "```json\n{\"T\": 0.6, \"I\": 0.3, \"N\": 0.2, \"F\": 0.4}\n```", "T": 0.6, "I": 0.3, "N": 0.2, "F": 0.4, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:393:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Vagueness (Fuzzy)", "statement": "John is 1.75 meters tall, therefore John is tall.", "gloss": "G1", "rep": 2, "response": "```json\n{\"T\": 0.5, \"I\": 0.3, \"N\": 0.2, \"F\": 0.4}\n```", "T": 0.5, "I": 0.3, "N": 0.2, "F": 0.4, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:394:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Vagueness (Fuzzy)", "statement": "John is 1.75 meters tall, therefore John is tall.", "gloss": "G1", "rep": 3, "response": "```json\n{\"T\": 0.5, \"I\": 0.2, \"N\": 0.1, \"F\": 0.4}\n```", "T": 0.5, "I": 0.2, "N": 0.1, "F": 0.4, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:395:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Vagueness (Fuzzy)", "statement": "John is 1.75 meters tall, therefore John is tall.", "gloss": "G1", "rep": 4, "response": "```json\n{\"T\": 0.6, \"I\": 0.3, \"N\": 0.1, \"F\": 0.4}\n```", "T": 0.6, "I": 0.3, "N": 0.1, "F": 0.4, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:396:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Vagueness (Fuzzy)", "statement": "John is 1.75 meters tall, therefore John is tall.", "gloss": "G1", "rep": 5, "response": "```json\n{\"T\": 0.5, \"I\": 0.3, \"N\": 0.2, \"F\": 0.4}\n```", "T": 0.5, "I": 0.3, "N": 0.2, "F": 0.4, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:397:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Vagueness (Fuzzy)", "statement": "John is 1.75 meters tall, therefore John is tall.", "gloss": "G1", "rep": 6, "response": "```json\n{\"T\": 0.5, \"I\": 0.2, \"N\": 0.3, \"F\": 0.4}\n```", "T": 0.5, "I": 0.2, "N": 0.3, "F": 0.4, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:398:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Vagueness (Fuzzy)", "statement": "John is 1.75 meters tall, therefore John is tall.", "gloss": "G1", "rep": 7, "response": "```json\n{\"T\": 0.6, \"I\": 0.3, \"N\": 0.1, \"F\": 0.4}\n```", "T": 0.6, "I": 0.3, "N": 0.1, "F": 0.4, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:399:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Vagueness (Fuzzy)", "statement": "John is 1.75 meters tall, therefore John is tall.", "gloss": "G1", "rep": 8, "response": "```json\n{\"T\": 0.5, \"I\": 0.3, \"N\": 0.2, \"F\": 0.4}\n```", "T": 0.5, "I": 0.3, "N": 0.2, "F": 0.4, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:400:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Vagueness (Fuzzy)", "statement": "John is 1.75 meters tall, therefore John is tall.", "gloss": "G1", "rep": 9, "response": "```json\n{\"T\": 0.5, \"I\": 0.3, \"N\": 0.2, \"F\": 0.4}\n```", "T": 0.5, "I": 0.3, "N": 0.2, "F": 0.4, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:401:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Vagueness (Fuzzy)", "statement": "John is 1.75 meters tall, therefore John is tall.", "gloss": "G1", "rep": 0, "response": "{\"T\": 0.6, \"I\": 0.2, \"N\": 0.1, \"F\": 0.3}", "T": 0.6, "I": 0.2, "N": 0.1, "F": 0.3, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:402:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Vagueness (Fuzzy)", "statement": "John is 1.75 meters tall, therefore John is tall.", "gloss": "G1", "rep": 1, "response": "{\"T\": 0.6, \"I\": 0.3, \"N\": 0.1, \"F\": 0.4}", "T": 0.6, "I": 0.3, "N": 0.1, "F": 0.4, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:403:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Vagueness (Fuzzy)", "statement": "John is 1.75 meters tall, therefore John is tall.", "gloss": "G1", "rep": 2, "response": "{\"T\": 0.6, \"I\": 0.2, \"N\": 0.1, \"F\": 0.3}", "T": 0.6, "I": 0.2, "N": 0.1, "F": 0.3, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:404:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Vagueness (Fuzzy)", "statement": "John is 1.75 meters tall, therefore John is tall.", "gloss": "G1", "rep": 3, "response": "{\"T\": 0.65, \"I\": 0.2, \"N\": 0.1, \"F\": 0.3}", "T": 0.65, "I": 0.2, "N": 0.1, "F": 0.3, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:405:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Vagueness (Fuzzy)", "statement": "John is 1.75 meters tall, therefore John is tall.", "gloss": "G1", "rep": 4, "response": "{\"T\": 0.7, \"I\": 0.2, \"N\": 0.1, \"F\": 0.3}", "T": 0.7, "I": 0.2, "N": 0.1, "F": 0.3, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:406:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Vagueness (Fuzzy)", "statement": "John is 1.75 meters tall, therefore John is tall.", "gloss": "G1", "rep": 5, "response": "{\"T\": 0.6, \"I\": 0.2, \"N\": 0.1, \"F\": 0.3}", "T": 0.6, "I": 0.2, "N": 0.1, "F": 0.3, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:407:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Vagueness (Fuzzy)", "statement": "John is 1.75 meters tall, therefore John is tall.", "gloss": "G1", "rep": 6, "response": "{\"T\": 0.7, \"I\": 0.1, \"N\": 0.1, \"F\": 0.3}", "T": 0.7, "I": 0.1, "N": 0.1, "F": 0.3, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:408:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Vagueness (Fuzzy)", "statement": "John is 1.75 meters tall, therefore John is tall.", "gloss": "G1", "rep": 7, "response": "{\"T\": 0.65, \"I\": 0.2, \"N\": 0.1, \"F\": 0.3}", "T": 0.65, "I": 0.2, "N": 0.1, "F": 0.3, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:409:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Vagueness (Fuzzy)", "statement": "John is 1.75 meters tall, therefore John is tall.", "gloss": "G1", "rep": 8, "response": "{\"T\": 0.6, \"I\": 0.2, \"N\": 0.1, \"F\": 0.3}", "T": 0.6, "I": 0.2, "N": 0.1, "F": 0.3, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:410:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Vagueness (Fuzzy)", "statement": "John is 1.75 meters tall, therefore John is tall.", "gloss": "G1", "rep": 9, "response": "{\"T\": 0.7, \"I\": 0.2, \"N\": 0.1, \"F\": 0.3}", "T": 0.7, "I": 0.2, "N": 0.1, "F": 0.3, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:411:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Vagueness (Fuzzy)", "statement": "John is 1.75 meters tall, therefore John is tall.", "gloss": "G1", "rep": 0, "response": "```json\n{\n  \"T\": 0.3,\n  \"I\": 0.65,\n  \"N\": 0.4,\n  \"F\": 0.25\n}\n```", "T": 0.3, "I": 0.65, "N": 0.4, "F": 0.25, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:412:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Vagueness (Fuzzy)", "statement": "John is 1.75 meters tall, therefore John is tall.", "gloss": "G1", "rep": 1, "response": "```json\n{\n  \"T\": 0.3,\n  \"I\": 0.7,\n  \"N\": 0.4,\n  \"F\": 0.2\n}\n```", "T": 0.3, "I": 0.7, "N": 0.4, "F": 0.2, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:413:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Vagueness (Fuzzy)", "statement": "John is 1.75 meters tall, therefore John is tall.", "gloss": "G1", "rep": 2, "response": "```json\n{\n  \"T\": 0.3,\n  \"I\": 0.7,\n  \"N\": 0.4,\n  \"F\": 0.2\n}\n```", "T": 0.3, "I": 0.7, "N": 0.4, "F": 0.2, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:414:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Vagueness (Fuzzy)", "statement": "John is 1.75 meters tall, therefore John is tall.", "gloss": "G1", "rep": 3, "response": "```json\n{\n  \"T\": 0.3,\n  \"I\": 0.6,\n  \"N\": 0.4,\n  \"F\": 0.2\n}\n```", "T": 0.3, "I": 0.6, "N": 0.4, "F": 0.2, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:415:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Vagueness (Fuzzy)", "statement": "John is 1.75 meters tall, therefore John is tall.", "gloss": "G1", "rep": 4, "response": "```json\n{\n  \"T\": 0.3,\n  \"I\": 0.6,\n  \"N\": 0.4,\n  \"F\": 0.2\n}\n```", "T": 0.3, "I": 0.6, "N": 0.4, "F": 0.2, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:416:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Vagueness (Fuzzy)", "statement": "John is 1.75 meters tall, therefore John is tall.", "gloss": "G1", "rep": 5, "response": "```json\n{\n  \"T\": 0.3,\n  \"I\": 0.6,\n  \"N\": 0.4,\n  \"F\": 0.2\n}\n```", "T": 0.3, "I": 0.6, "N": 0.4, "F": 0.2, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:417:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Vagueness (Fuzzy)", "statement": "John is 1.75 meters tall, therefore John is tall.", "gloss": "G1", "rep": 6, "response": "```json\n{\n  \"T\": 0.3,\n  \"I\": 0.7,\n  \"N\": 0.4,\n  \"F\": 0.2\n}\n```", "T": 0.3, "I": 0.7, "N": 0.4, "F": 0.2, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:418:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Vagueness (Fuzzy)", "statement": "John is 1.75 meters tall, therefore John is tall.", "gloss": "G1", "rep": 7, "response": "```json\n{\n  \"T\": 0.3,\n  \"I\": 0.6,\n  \"N\": 0.1,\n  \"F\": 0.4\n}\n```", "T": 0.3, "I": 0.6, "N": 0.1, "F": 0.4, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:419:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Vagueness (Fuzzy)", "statement": "John is 1.75 meters tall, therefore John is tall.", "gloss": "G1", "rep": 8, "response": "```json\n{\n  \"T\": 0.2,\n  \"I\": 0.7,\n  \"N\": 0.4,\n  \"F\": 0.3\n}\n```", "T": 0.2, "I": 0.7, "N": 0.4, "F": 0.3, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:420:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Vagueness (Fuzzy)", "statement": "John is 1.75 meters tall, therefore John is tall.", "gloss": "G1", "rep": 9, "response": "```json\n{\n  \"T\": 0.3,\n  \"I\": 0.6,\n  \"N\": 0.4,\n  \"F\": 0.2\n}\n```", "T": 0.3, "I": 0.6, "N": 0.4, "F": 0.2, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:421:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Vagueness (Fuzzy)", "statement": "John is 1.75 meters tall, therefore John is tall.", "gloss": "G2", "rep": 0, "response": "```json\n{\"T\": 0.4, \"I\": 0.4, \"N\": 0.2, \"F\": 0.3}\n```", "T": 0.4, "I": 0.4, "N": 0.2, "F": 0.3, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:422:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Vagueness (Fuzzy)", "statement": "John is 1.75 meters tall, therefore John is tall.", "gloss": "G2", "rep": 1, "response": "```json\n{\"T\": 0.4, \"I\": 0.3, \"N\": 0.1, \"F\": 0.3}\n```", "T": 0.4, "I": 0.3, "N": 0.1, "F": 0.3, "regime": "very_weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:423:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Vagueness (Fuzzy)", "statement": "John is 1.75 meters tall, therefore John is tall.", "gloss": "G2", "rep": 2, "response": "```json\n{\"T\": 0.5, \"I\": 0.3, \"N\": 0.1, \"F\": 0.5}\n```", "T": 0.5, "I": 0.3, "N": 0.1, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:424:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Vagueness (Fuzzy)", "statement": "John is 1.75 meters tall, therefore John is tall.", "gloss": "G2", "rep": 3, "response": "```json\n{\"T\": 0.5, \"I\": 0.3, \"N\": 0.2, \"F\": 0.4}\n```", "T": 0.5, "I": 0.3, "N": 0.2, "F": 0.4, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:425:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Vagueness (Fuzzy)", "statement": "John is 1.75 meters tall, therefore John is tall.", "gloss": "G2", "rep": 4, "response": "```json\n{\"T\": 0.5, \"I\": 0.3, \"N\": 0.1, \"F\": 0.6}\n```", "T": 0.5, "I": 0.3, "N": 0.1, "F": 0.6, "regime": "strong", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:426:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Vagueness (Fuzzy)", "statement": "John is 1.75 meters tall, therefore John is tall.", "gloss": "G2", "rep": 5, "response": "```json\n{\"T\": 0.4, \"I\": 0.3, \"N\": 0.2, \"F\": 0.3}\n```", "T": 0.4, "I": 0.3, "N": 0.2, "F": 0.3, "regime": "very_weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:427:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Vagueness (Fuzzy)", "statement": "John is 1.75 meters tall, therefore John is tall.", "gloss": "G2", "rep": 6, "response": "```json\n{\"T\": 0.5, \"I\": 0.3, \"N\": 0.1, \"F\": 0.5}\n```", "T": 0.5, "I": 0.3, "N": 0.1, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:428:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Vagueness (Fuzzy)", "statement": "John is 1.75 meters tall, therefore John is tall.", "gloss": "G2", "rep": 7, "response": "```json\n{\"T\": 0.4, \"I\": 0.3, \"N\": 0.1, \"F\": 0.3}\n```", "T": 0.4, "I": 0.3, "N": 0.1, "F": 0.3, "regime": "very_weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:429:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Vagueness (Fuzzy)", "statement": "John is 1.75 meters tall, therefore John is tall.", "gloss": "G2", "rep": 8, "response": "```json\n{\"T\": 0.3, \"I\": 0.5, \"N\": 0.1, \"F\": 0.4}\n```", "T": 0.3, "I": 0.5, "N": 0.1, "F": 0.4, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:430:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Vagueness (Fuzzy)", "statement": "John is 1.75 meters tall, therefore John is tall.", "gloss": "G2", "rep": 9, "response": "```json\n{\"T\": 0.4, \"I\": 0.3, \"N\": 0.1, \"F\": 0.4}\n```", "T": 0.4, "I": 0.3, "N": 0.1, "F": 0.4, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:431:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Vagueness (Fuzzy)", "statement": "John is 1.75 meters tall, therefore John is tall.", "gloss": "G2", "rep": 0, "response": "{\"T\": 0.6, \"I\": 0.4, \"N\": 0.1, \"F\": 0.3}", "T": 0.6, "I": 0.4, "N": 0.1, "F": 0.3, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:432:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Vagueness (Fuzzy)", "statement": "John is 1.75 meters tall, therefore John is tall.", "gloss": "G2", "rep": 1, "response": "{\"T\": 0.6, \"I\": 0.7, \"N\": 0.3, \"F\": 0.4}", "T": 0.6, "I": 0.7, "N": 0.3, "F": 0.4, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:433:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Vagueness (Fuzzy)", "statement": "John is 1.75 meters tall, therefore John is tall.", "gloss": "G2", "rep": 2, "response": "{\"T\": 0.6, \"I\": 0.4, \"N\": 0.0, \"F\": 0.3}", "T": 0.6, "I": 0.4, "N": 0.0, "F": 0.3, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:434:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Vagueness (Fuzzy)", "statement": "John is 1.75 meters tall, therefore John is tall.", "gloss": "G2", "rep": 3, "response": "{\"T\": 0.6, \"I\": 0.4, \"N\": 0.2, \"F\": 0.3}", "T": 0.6, "I": 0.4, "N": 0.2, "F": 0.3, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:435:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Vagueness (Fuzzy)", "statement": "John is 1.75 meters tall, therefore John is tall.", "gloss": "G2", "rep": 4, "response": "{\"T\": 0.6, \"I\": 0.7, \"N\": 0.2, \"F\": 0.4}", "T": 0.6, "I": 0.7, "N": 0.2, "F": 0.4, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:436:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Vagueness (Fuzzy)", "statement": "John is 1.75 meters tall, therefore John is tall.", "gloss": "G2", "rep": 5, "response": "{\"T\": 0.6, \"I\": 0.7, \"N\": 0.2, \"F\": 0.4}", "T": 0.6, "I": 0.7, "N": 0.2, "F": 0.4, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:437:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Vagueness (Fuzzy)", "statement": "John is 1.75 meters tall, therefore John is tall.", "gloss": "G2", "rep": 6, "response": "{\"T\": 0.6, \"I\": 0.7, \"N\": 0.3, \"F\": 0.4}", "T": 0.6, "I": 0.7, "N": 0.3, "F": 0.4, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:438:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Vagueness (Fuzzy)", "statement": "John is 1.75 meters tall, therefore John is tall.", "gloss": "G2", "rep": 7, "response": "{\"T\": 0.6, \"I\": 0.4, \"N\": 0.2, \"F\": 0.3}", "T": 0.6, "I": 0.4, "N": 0.2, "F": 0.3, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:439:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Vagueness (Fuzzy)", "statement": "John is 1.75 meters tall, therefore John is tall.", "gloss": "G2", "rep": 8, "response": "{\"T\": 0.6, \"I\": 0.7, \"N\": 0.2, \"F\": 0.4}", "T": 0.6, "I": 0.7, "N": 0.2, "F": 0.4, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:440:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Vagueness (Fuzzy)", "statement": "John is 1.75 meters tall, therefore John is tall.", "gloss": "G2", "rep": 9, "response": "{\"T\": 0.6, \"I\": 0.7, \"N\": 0.2, \"F\": 0.4}", "T": 0.6, "I": 0.7, "N": 0.2, "F": 0.4, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:441:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Vagueness (Fuzzy)", "statement": "John is 1.75 meters tall, therefore John is tall.", "gloss": "G2", "rep": 0, "response": "{\"T\": 0.6, \"I\": 0.3, \"N\": 0.1, \"F\": 0.2}", "T": 0.6, "I": 0.3, "N": 0.1, "F": 0.2, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:442:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Vagueness (Fuzzy)", "statement": "John is 1.75 meters tall, therefore John is tall.", "gloss": "G2", "rep": 1, "response": "{\"T\": 0.6, \"I\": 0.4, \"N\": 0.1, \"F\": 0.3}", "T": 0.6, "I": 0.4, "N": 0.1, "F": 0.3, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:443:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Vagueness (Fuzzy)", "statement": "John is 1.75 meters tall, therefore John is tall.", "gloss": "G2", "rep": 2, "response": "{\"T\": 0.6, \"I\": 0.4, \"N\": 0.1, \"F\": 0.2}", "T": 0.6, "I": 0.4, "N": 0.1, "F": 0.2, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:444:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Vagueness (Fuzzy)", "statement": "John is 1.75 meters tall, therefore John is tall.", "gloss": "G2", "rep": 3, "response": "{\"T\": 0.6, \"I\": 0.4, \"N\": 0.1, \"F\": 0.2}", "T": 0.6, "I": 0.4, "N": 0.1, "F": 0.2, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:445:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Vagueness (Fuzzy)", "statement": "John is 1.75 meters tall, therefore John is tall.", "gloss": "G2", "rep": 4, "response": "{\"T\": 0.7, \"I\": 0.3, \"N\": 0.1, \"F\": 0.2}", "T": 0.7, "I": 0.3, "N": 0.1, "F": 0.2, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:446:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Vagueness (Fuzzy)", "statement": "John is 1.75 meters tall, therefore John is tall.", "gloss": "G2", "rep": 5, "response": "{\"T\": 0.7, \"I\": 0.3, \"N\": 0.1, \"F\": 0.2}", "T": 0.7, "I": 0.3, "N": 0.1, "F": 0.2, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:447:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Vagueness (Fuzzy)", "statement": "John is 1.75 meters tall, therefore John is tall.", "gloss": "G2", "rep": 6, "response": "{\"T\": 0.7, \"I\": 0.3, \"N\": 0.0, \"F\": 0.2}", "T": 0.7, "I": 0.3, "N": 0.0, "F": 0.2, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:448:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Vagueness (Fuzzy)", "statement": "John is 1.75 meters tall, therefore John is tall.", "gloss": "G2", "rep": 7, "response": "{\"T\": 0.7, \"I\": 0.3, \"N\": 0.0, \"F\": 0.2}", "T": 0.7, "I": 0.3, "N": 0.0, "F": 0.2, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:449:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Vagueness (Fuzzy)", "statement": "John is 1.75 meters tall, therefore John is tall.", "gloss": "G2", "rep": 8, "response": "{\"T\": 0.7, \"I\": 0.3, \"N\": 0.1, \"F\": 0.2}", "T": 0.7, "I": 0.3, "N": 0.1, "F": 0.2, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:450:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Vagueness (Fuzzy)", "statement": "John is 1.75 meters tall, therefore John is tall.", "gloss": "G2", "rep": 9, "response": "{\"T\": 0.6, \"I\": 0.4, \"N\": 0.1, \"F\": 0.2}", "T": 0.6, "I": 0.4, "N": 0.1, "F": 0.2, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:451:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Vagueness (Fuzzy)", "statement": "John is 1.75 meters tall, therefore John is tall.", "gloss": "G2", "rep": 0, "response": "```json\n{\"T\": 0.5, \"I\": 0.3, \"N\": 0.2, \"F\": 0.4}\n```", "T": 0.5, "I": 0.3, "N": 0.2, "F": 0.4, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:452:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Vagueness (Fuzzy)", "statement": "John is 1.75 meters tall, therefore John is tall.", "gloss": "G2", "rep": 1, "response": "```json\n{\"T\": 0.6, \"I\": 0.3, \"N\": 0.1, \"F\": 0.4}\n```", "T": 0.6, "I": 0.3, "N": 0.1, "F": 0.4, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:453:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Vagueness (Fuzzy)", "statement": "John is 1.75 meters tall, therefore John is tall.", "gloss": "G2", "rep": 2, "response": "```json\n{\"T\": 0.7, \"I\": 0.2, \"N\": 0.1, \"F\": 0.3}\n```", "T": 0.7, "I": 0.2, "N": 0.1, "F": 0.3, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:454:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Vagueness (Fuzzy)", "statement": "John is 1.75 meters tall, therefore John is tall.", "gloss": "G2", "rep": 3, "response": "```json\n{\"T\": 0.4, \"I\": 0.3, \"N\": 0.1, \"F\": 0.5}\n```", "T": 0.4, "I": 0.3, "N": 0.1, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:455:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Vagueness (Fuzzy)", "statement": "John is 1.75 meters tall, therefore John is tall.", "gloss": "G2", "rep": 4, "response": "```json\n{\"T\": 0.6, \"I\": 0.2, \"N\": 0.1, \"F\": 0.3}\n```", "T": 0.6, "I": 0.2, "N": 0.1, "F": 0.3, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:456:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Vagueness (Fuzzy)", "statement": "John is 1.75 meters tall, therefore John is tall.", "gloss": "G2", "rep": 5, "response": "```json\n{\"T\": 0.5, \"I\": 0.3, \"N\": 0.1, \"F\": 0.4}\n```", "T": 0.5, "I": 0.3, "N": 0.1, "F": 0.4, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:457:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Vagueness (Fuzzy)", "statement": "John is 1.75 meters tall, therefore John is tall.", "gloss": "G2", "rep": 6, "response": "```json\n{\"T\": 0.6, \"I\": 0.3, \"N\": 0.1, \"F\": 0.4}\n```", "T": 0.6, "I": 0.3, "N": 0.1, "F": 0.4, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:458:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Vagueness (Fuzzy)", "statement": "John is 1.75 meters tall, therefore John is tall.", "gloss": "G2", "rep": 7, "response": "```json\n{\"T\": 0.5, \"I\": 0.2, \"N\": 0.1, \"F\": 0.4}\n```", "T": 0.5, "I": 0.2, "N": 0.1, "F": 0.4, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:459:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Vagueness (Fuzzy)", "statement": "John is 1.75 meters tall, therefore John is tall.", "gloss": "G2", "rep": 8, "response": "```json\n{\"T\": 0.6, \"I\": 0.3, \"N\": 0.1, \"F\": 0.4}\n```", "T": 0.6, "I": 0.3, "N": 0.1, "F": 0.4, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:460:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Vagueness (Fuzzy)", "statement": "John is 1.75 meters tall, therefore John is tall.", "gloss": "G2", "rep": 9, "response": "```json\n{\"T\": 0.5, \"I\": 0.2, \"N\": 0.1, \"F\": 0.4}\n```", "T": 0.5, "I": 0.2, "N": 0.1, "F": 0.4, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:461:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Vagueness (Fuzzy)", "statement": "John is 1.75 meters tall, therefore John is tall.", "gloss": "G2", "rep": 0, "response": "{\"T\": 0.6, \"I\": 0.1, \"N\": 0.05, \"F\": 0.3}", "T": 0.6, "I": 0.1, "N": 0.05, "F": 0.3, "regime": "very_weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:462:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Vagueness (Fuzzy)", "statement": "John is 1.75 meters tall, therefore John is tall.", "gloss": "G2", "rep": 1, "response": "{\"T\": 0.6, \"I\": 0.2, \"N\": 0.1, \"F\": 0.3}", "T": 0.6, "I": 0.2, "N": 0.1, "F": 0.3, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:463:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Vagueness (Fuzzy)", "statement": "John is 1.75 meters tall, therefore John is tall.", "gloss": "G2", "rep": 2, "response": "{\"T\": 0.6, \"I\": 0.2, \"N\": 0.1, \"F\": 0.3}", "T": 0.6, "I": 0.2, "N": 0.1, "F": 0.3, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:464:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Vagueness (Fuzzy)", "statement": "John is 1.75 meters tall, therefore John is tall.", "gloss": "G2", "rep": 3, "response": "{\"T\": 0.6, \"I\": 0.2, \"N\": 0.1, \"F\": 0.3}", "T": 0.6, "I": 0.2, "N": 0.1, "F": 0.3, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:465:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Vagueness (Fuzzy)", "statement": "John is 1.75 meters tall, therefore John is tall.", "gloss": "G2", "rep": 4, "response": "{\"T\": 0.7, \"I\": 0.1, \"N\": 0.05, \"F\": 0.2}", "T": 0.7, "I": 0.1, "N": 0.05, "F": 0.2, "regime": "very_weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:466:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Vagueness (Fuzzy)", "statement": "John is 1.75 meters tall, therefore John is tall.", "gloss": "G2", "rep": 5, "response": "{\"T\": 0.6, \"I\": 0.2, \"N\": 0.1, \"F\": 0.3}", "T": 0.6, "I": 0.2, "N": 0.1, "F": 0.3, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:467:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Vagueness (Fuzzy)", "statement": "John is 1.75 meters tall, therefore John is tall.", "gloss": "G2", "rep": 6, "response": "{\"T\": 0.6, \"I\": 0.2, \"N\": 0.1, \"F\": 0.3}", "T": 0.6, "I": 0.2, "N": 0.1, "F": 0.3, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:468:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Vagueness (Fuzzy)", "statement": "John is 1.75 meters tall, therefore John is tall.", "gloss": "G2", "rep": 7, "response": "{\"T\": 0.7, \"I\": 0.1, \"N\": 0.05, \"F\": 0.2}", "T": 0.7, "I": 0.1, "N": 0.05, "F": 0.2, "regime": "very_weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:469:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Vagueness (Fuzzy)", "statement": "John is 1.75 meters tall, therefore John is tall.", "gloss": "G2", "rep": 8, "response": "{\"T\": 0.7, \"I\": 0.1, \"N\": 0.0, \"F\": 0.3}", "T": 0.7, "I": 0.1, "N": 0.0, "F": 0.3, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:470:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Vagueness (Fuzzy)", "statement": "John is 1.75 meters tall, therefore John is tall.", "gloss": "G2", "rep": 9, "response": "{\"T\": 0.6, \"I\": 0.2, \"N\": 0.1, \"F\": 0.3}", "T": 0.6, "I": 0.2, "N": 0.1, "F": 0.3, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:471:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Vagueness (Fuzzy)", "statement": "John is 1.75 meters tall, therefore John is tall.", "gloss": "G2", "rep": 0, "response": "```json\n{\n  \"T\": 0.3,\n  \"I\": 0.6,\n  \"N\": 0.1,\n  \"F\": 0.4\n}\n```", "T": 0.3, "I": 0.6, "N": 0.1, "F": 0.4, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:472:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Vagueness (Fuzzy)", "statement": "John is 1.75 meters tall, therefore John is tall.", "gloss": "G2", "rep": 1, "response": "```json\n{\n  \"T\": 0.3,\n  \"I\": 0.7,\n  \"N\": 0.1,\n  \"F\": 0.4\n}\n```", "T": 0.3, "I": 0.7, "N": 0.1, "F": 0.4, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:473:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Vagueness (Fuzzy)", "statement": "John is 1.75 meters tall, therefore John is tall.", "gloss": "G2", "rep": 2, "response": "```json\n{\n  \"T\": 0.3,\n  \"I\": 0.7,\n  \"N\": 0.2,\n  \"F\": 0.4\n}\n```", "T": 0.3, "I": 0.7, "N": 0.2, "F": 0.4, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:474:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Vagueness (Fuzzy)", "statement": "John is 1.75 meters tall, therefore John is tall.", "gloss": "G2", "rep": 3, "response": "```json\n{\n  \"T\": 0.3,\n  \"I\": 0.7,\n  \"N\": 0.2,\n  \"F\": 0.4\n}\n```", "T": 0.3, "I": 0.7, "N": 0.2, "F": 0.4, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:475:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Vagueness (Fuzzy)", "statement": "John is 1.75 meters tall, therefore John is tall.", "gloss": "G2", "rep": 4, "response": "```json\n{\n  \"T\": 0.2,\n  \"I\": 0.7,\n  \"N\": 0.15,\n  \"F\": 0.35\n}\n```", "T": 0.2, "I": 0.7, "N": 0.15, "F": 0.35, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:476:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Vagueness (Fuzzy)", "statement": "John is 1.75 meters tall, therefore John is tall.", "gloss": "G2", "rep": 5, "response": "```json\n{\n  \"T\": 0.3,\n  \"I\": 0.6,\n  \"N\": 0.1,\n  \"F\": 0.4\n}\n```", "T": 0.3, "I": 0.6, "N": 0.1, "F": 0.4, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:477:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Vagueness (Fuzzy)", "statement": "John is 1.75 meters tall, therefore John is tall.", "gloss": "G2", "rep": 6, "response": "```json\n{\n  \"T\": 0.3,\n  \"I\": 0.6,\n  \"N\": 0.1,\n  \"F\": 0.4\n}\n```", "T": 0.3, "I": 0.6, "N": 0.1, "F": 0.4, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:478:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Vagueness (Fuzzy)", "statement": "John is 1.75 meters tall, therefore John is tall.", "gloss": "G2", "rep": 7, "response": "```json\n{\n  \"T\": 0.3,\n  \"I\": 0.6,\n  \"N\": 0.1,\n  \"F\": 0.4\n}\n```", "T": 0.3, "I": 0.6, "N": 0.1, "F": 0.4, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:479:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Vagueness (Fuzzy)", "statement": "John is 1.75 meters tall, therefore John is tall.", "gloss": "G2", "rep": 8, "response": "```json\n{\n  \"T\": 0.3,\n  \"I\": 0.6,\n  \"N\": 0.1,\n  \"F\": 0.4\n}\n```", "T": 0.3, "I": 0.6, "N": 0.1, "F": 0.4, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:480:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Vagueness (Fuzzy)", "statement": "John is 1.75 meters tall, therefore John is tall.", "gloss": "G2", "rep": 9, "response": "```json\n{\n  \"T\": 0.3,\n  \"I\": 0.6,\n  \"N\": 0.1,\n  \"F\": 0.4\n}\n```", "T": 0.3, "I": 0.6, "N": 0.1, "F": 0.4, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:481:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Vagueness (Fuzzy)", "statement": "John is 1.75 meters tall, therefore John is tall.", "gloss": "G3", "rep": 0, "response": "```json\n{\"T\": 0.5, \"I\": 0.3, \"N\": 0.4, \"F\": 0.5}\n```", "T": 0.5, "I": 0.3, "N": 0.4, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:482:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Vagueness (Fuzzy)", "statement": "John is 1.75 meters tall, therefore John is tall.", "gloss": "G3", "rep": 1, "response": "{\"T\": 0.5, \"I\": 0.3, \"N\": 0.4, \"F\": 0.3}", "T": 0.5, "I": 0.3, "N": 0.4, "F": 0.3, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:483:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Vagueness (Fuzzy)", "statement": "John is 1.75 meters tall, therefore John is tall.", "gloss": "G3", "rep": 2, "response": "```json\n{\"T\": 0.4, \"I\": 0.5, \"N\": 0.3, \"F\": 0.6}\n```", "T": 0.4, "I": 0.5, "N": 0.3, "F": 0.6, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:484:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Vagueness (Fuzzy)", "statement": "John is 1.75 meters tall, therefore John is tall.", "gloss": "G3", "rep": 3, "response": "```json\n{\"T\": 0.4, \"I\": 0.3, \"N\": 0.1, \"F\": 0.5}\n```", "T": 0.4, "I": 0.3, "N": 0.1, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:485:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Vagueness (Fuzzy)", "statement": "John is 1.75 meters tall, therefore John is tall.", "gloss": "G3", "rep": 4, "response": "```json\n{\"T\": 0.4, \"I\": 0.3, \"N\": 0.2, \"F\": 0.5}\n```", "T": 0.4, "I": 0.3, "N": 0.2, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:486:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Vagueness (Fuzzy)", "statement": "John is 1.75 meters tall, therefore John is tall.", "gloss": "G3", "rep": 5, "response": "```json\n{\"T\": 0.6, \"I\": 0.3, \"N\": 0.2, \"F\": 0.5}\n```", "T": 0.6, "I": 0.3, "N": 0.2, "F": 0.5, "regime": "strong", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:487:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Vagueness (Fuzzy)", "statement": "John is 1.75 meters tall, therefore John is tall.", "gloss": "G3", "rep": 6, "response": "```json\n{\"T\": 0.4, \"I\": 0.3, \"N\": 0.2, \"F\": 0.5}\n```", "T": 0.4, "I": 0.3, "N": 0.2, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:488:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Vagueness (Fuzzy)", "statement": "John is 1.75 meters tall, therefore John is tall.", "gloss": "G3", "rep": 7, "response": "```json\n{\"T\": 0.3, \"I\": 0.5, \"N\": 0.4, \"F\": 0.4}\n```", "T": 0.3, "I": 0.5, "N": 0.4, "F": 0.4, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:489:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Vagueness (Fuzzy)", "statement": "John is 1.75 meters tall, therefore John is tall.", "gloss": "G3", "rep": 8, "response": "```json\n{\"T\": 0.5, \"I\": 0.4, \"N\": 0.3, \"F\": 0.5}\n```", "T": 0.5, "I": 0.4, "N": 0.3, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:490:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Vagueness (Fuzzy)", "statement": "John is 1.75 meters tall, therefore John is tall.", "gloss": "G3", "rep": 9, "response": "```json\n{\"T\": 0.4, \"I\": 0.3, \"N\": 0.2, \"F\": 0.3}\n```", "T": 0.4, "I": 0.3, "N": 0.2, "F": 0.3, "regime": "very_weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:491:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Vagueness (Fuzzy)", "statement": "John is 1.75 meters tall, therefore John is tall.", "gloss": "G3", "rep": 0, "response": "{\"T\": 0.6, \"I\": 0.7, \"N\": 0.4, \"F\": 0.3}", "T": 0.6, "I": 0.7, "N": 0.4, "F": 0.3, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:492:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Vagueness (Fuzzy)", "statement": "John is 1.75 meters tall, therefore John is tall.", "gloss": "G3", "rep": 1, "response": "{\"T\": 0.6, \"I\": 0.7, \"N\": 0.5, \"F\": 0.4}", "T": 0.6, "I": 0.7, "N": 0.5, "F": 0.4, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:493:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Vagueness (Fuzzy)", "statement": "John is 1.75 meters tall, therefore John is tall.", "gloss": "G3", "rep": 2, "response": "{\"T\": 0.6, \"I\": 0.4, \"N\": 0.3, \"F\": 0.2}", "T": 0.6, "I": 0.4, "N": 0.3, "F": 0.2, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:494:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Vagueness (Fuzzy)", "statement": "John is 1.75 meters tall, therefore John is tall.", "gloss": "G3", "rep": 3, "response": "{\"T\": 0.6, \"I\": 0.4, \"N\": 0.3, \"F\": 0.3}", "T": 0.6, "I": 0.4, "N": 0.3, "F": 0.3, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:495:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Vagueness (Fuzzy)", "statement": "John is 1.75 meters tall, therefore John is tall.", "gloss": "G3", "rep": 4, "response": "{\"T\": 0.6, \"I\": 0.7, \"N\": 0.5, \"F\": 0.3}", "T": 0.6, "I": 0.7, "N": 0.5, "F": 0.3, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:496:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Vagueness (Fuzzy)", "statement": "John is 1.75 meters tall, therefore John is tall.", "gloss": "G3", "rep": 5, "response": "{\"T\": 0.6, \"I\": 0.7, \"N\": 0.5, \"F\": 0.4}", "T": 0.6, "I": 0.7, "N": 0.5, "F": 0.4, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:497:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Vagueness (Fuzzy)", "statement": "John is 1.75 meters tall, therefore John is tall.", "gloss": "G3", "rep": 6, "response": "{\"T\": 0.6, \"I\": 0.4, \"N\": 0.3, \"F\": 0.2}", "T": 0.6, "I": 0.4, "N": 0.3, "F": 0.2, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:498:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Vagueness (Fuzzy)", "statement": "John is 1.75 meters tall, therefore John is tall.", "gloss": "G3", "rep": 7, "response": "{\"T\": 0.6, \"I\": 0.7, \"N\": 0.5, \"F\": 0.4}", "T": 0.6, "I": 0.7, "N": 0.5, "F": 0.4, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:499:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Vagueness (Fuzzy)", "statement": "John is 1.75 meters tall, therefore John is tall.", "gloss": "G3", "rep": 8, "response": "{\"T\": 0.6, \"I\": 0.7, \"N\": 0.5, \"F\": 0.3}", "T": 0.6, "I": 0.7, "N": 0.5, "F": 0.3, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:500:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Vagueness (Fuzzy)", "statement": "John is 1.75 meters tall, therefore John is tall.", "gloss": "G3", "rep": 9, "response": "{\"T\": 0.6, \"I\": 0.7, \"N\": 0.4, \"F\": 0.3}", "T": 0.6, "I": 0.7, "N": 0.4, "F": 0.3, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:501:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Vagueness (Fuzzy)", "statement": "John is 1.75 meters tall, therefore John is tall.", "gloss": "G3", "rep": 0, "response": "{\"T\": 0.6, \"I\": 0.4, \"N\": 0.2, \"F\": 0.1}", "T": 0.6, "I": 0.4, "N": 0.2, "F": 0.1, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:502:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Vagueness (Fuzzy)", "statement": "John is 1.75 meters tall, therefore John is tall.", "gloss": "G3", "rep": 1, "response": "{\"T\": 0.6, \"I\": 0.4, \"N\": 0.2, \"F\": 0.3}", "T": 0.6, "I": 0.4, "N": 0.2, "F": 0.3, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:503:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Vagueness (Fuzzy)", "statement": "John is 1.75 meters tall, therefore John is tall.", "gloss": "G3", "rep": 2, "response": "{\"T\": 0.7, \"I\": 0.3, \"N\": 0.2, \"F\": 0.1}", "T": 0.7, "I": 0.3, "N": 0.2, "F": 0.1, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:504:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Vagueness (Fuzzy)", "statement": "John is 1.75 meters tall, therefore John is tall.", "gloss": "G3", "rep": 3, "response": "{\"T\": 0.6, \"I\": 0.3, \"N\": 0.2, \"F\": 0.4}", "T": 0.6, "I": 0.3, "N": 0.2, "F": 0.4, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:505:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Vagueness (Fuzzy)", "statement": "John is 1.75 meters tall, therefore John is tall.", "gloss": "G3", "rep": 4, "response": "{\"T\": 0.7, \"I\": 0.2, \"N\": 0.1, \"F\": 0.3}", "T": 0.7, "I": 0.2, "N": 0.1, "F": 0.3, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:506:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Vagueness (Fuzzy)", "statement": "John is 1.75 meters tall, therefore John is tall.", "gloss": "G3", "rep": 5, "response": "{\"T\": 0.7, \"I\": 0.2, \"N\": 0.1, \"F\": 0.3}", "T": 0.7, "I": 0.2, "N": 0.1, "F": 0.3, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:507:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Vagueness (Fuzzy)", "statement": "John is 1.75 meters tall, therefore John is tall.", "gloss": "G3", "rep": 6, "response": "{\"T\": 0.6, \"I\": 0.3, \"N\": 0.2, \"F\": 0.4}", "T": 0.6, "I": 0.3, "N": 0.2, "F": 0.4, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:508:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Vagueness (Fuzzy)", "statement": "John is 1.75 meters tall, therefore John is tall.", "gloss": "G3", "rep": 7, "response": "{\"T\": 0.7, \"I\": 0.2, \"N\": 0.1, \"F\": 0.3}", "T": 0.7, "I": 0.2, "N": 0.1, "F": 0.3, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:509:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Vagueness (Fuzzy)", "statement": "John is 1.75 meters tall, therefore John is tall.", "gloss": "G3", "rep": 8, "response": "{\"T\": 0.6, \"I\": 0.3, \"N\": 0.2, \"F\": 0.4}", "T": 0.6, "I": 0.3, "N": 0.2, "F": 0.4, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:510:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Vagueness (Fuzzy)", "statement": "John is 1.75 meters tall, therefore John is tall.", "gloss": "G3", "rep": 9, "response": "{\"T\": 0.7, \"I\": 0.3, \"N\": 0.1, \"F\": 0.2}", "T": 0.7, "I": 0.3, "N": 0.1, "F": 0.2, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:511:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Vagueness (Fuzzy)", "statement": "John is 1.75 meters tall, therefore John is tall.", "gloss": "G3", "rep": 0, "response": "```json\n{\"T\": 0.6, \"I\": 0.3, \"N\": 0.4, \"F\": 0.5}\n```", "T": 0.6, "I": 0.3, "N": 0.4, "F": 0.5, "regime": "strong", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:512:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Vagueness (Fuzzy)", "statement": "John is 1.75 meters tall, therefore John is tall.", "gloss": "G3", "rep": 1, "response": "```json\n{\"T\": 0.5, \"I\": 0.2, \"N\": 0.3, \"F\": 0.4}\n```", "T": 0.5, "I": 0.2, "N": 0.3, "F": 0.4, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:513:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Vagueness (Fuzzy)", "statement": "John is 1.75 meters tall, therefore John is tall.", "gloss": "G3", "rep": 2, "response": "```json\n{\"T\": 0.5, \"I\": 0.2, \"N\": 0.3, \"F\": 0.4}\n```", "T": 0.5, "I": 0.2, "N": 0.3, "F": 0.4, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:514:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Vagueness (Fuzzy)", "statement": "John is 1.75 meters tall, therefore John is tall.", "gloss": "G3", "rep": 3, "response": "```json\n{\"T\": 0.5, \"I\": 0.3, \"N\": 0.4, \"F\": 0.5}\n```", "T": 0.5, "I": 0.3, "N": 0.4, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:515:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Vagueness (Fuzzy)", "statement": "John is 1.75 meters tall, therefore John is tall.", "gloss": "G3", "rep": 4, "response": "```json\n{\"T\": 0.5, \"I\": 0.3, \"N\": 0.2, \"F\": 0.5}\n```", "T": 0.5, "I": 0.3, "N": 0.2, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:516:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Vagueness (Fuzzy)", "statement": "John is 1.75 meters tall, therefore John is tall.", "gloss": "G3", "rep": 5, "response": "```json\n{\"T\": 0.6, \"I\": 0.3, \"N\": 0.4, \"F\": 0.5}\n```", "T": 0.6, "I": 0.3, "N": 0.4, "F": 0.5, "regime": "strong", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:517:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Vagueness (Fuzzy)", "statement": "John is 1.75 meters tall, therefore John is tall.", "gloss": "G3", "rep": 6, "response": "```json\n{\"T\": 0.5, \"I\": 0.3, \"N\": 0.4, \"F\": 0.5}\n```", "T": 0.5, "I": 0.3, "N": 0.4, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:518:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Vagueness (Fuzzy)", "statement": "John is 1.75 meters tall, therefore John is tall.", "gloss": "G3", "rep": 7, "response": "```json\n{\"T\": 0.5, \"I\": 0.3, \"N\": 0.2, \"F\": 0.4}\n```", "T": 0.5, "I": 0.3, "N": 0.2, "F": 0.4, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:519:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Vagueness (Fuzzy)", "statement": "John is 1.75 meters tall, therefore John is tall.", "gloss": "G3", "rep": 8, "response": "```json\n{\"T\": 0.6, \"I\": 0.3, \"N\": 0.2, \"F\": 0.4}\n```", "T": 0.6, "I": 0.3, "N": 0.2, "F": 0.4, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:520:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Vagueness (Fuzzy)", "statement": "John is 1.75 meters tall, therefore John is tall.", "gloss": "G3", "rep": 9, "response": "```json\n{\"T\": 0.5, \"I\": 0.3, \"N\": 0.4, \"F\": 0.5}\n```", "T": 0.5, "I": 0.3, "N": 0.4, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:521:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Vagueness (Fuzzy)", "statement": "John is 1.75 meters tall, therefore John is tall.", "gloss": "G3", "rep": 0, "response": "{\"T\": 0.6, \"I\": 0.1, \"N\": 0.2, \"F\": 0.3}", "T": 0.6, "I": 0.1, "N": 0.2, "F": 0.3, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:522:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Vagueness (Fuzzy)", "statement": "John is 1.75 meters tall, therefore John is tall.", "gloss": "G3", "rep": 1, "response": "{\"T\": 0.6, \"I\": 0.1, \"N\": 0.2, \"F\": 0.3}", "T": 0.6, "I": 0.1, "N": 0.2, "F": 0.3, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:523:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Vagueness (Fuzzy)", "statement": "John is 1.75 meters tall, therefore John is tall.", "gloss": "G3", "rep": 2, "response": "{\"T\": 0.6, \"I\": 0.1, \"N\": 0.2, \"F\": 0.3}", "T": 0.6, "I": 0.1, "N": 0.2, "F": 0.3, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:524:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Vagueness (Fuzzy)", "statement": "John is 1.75 meters tall, therefore John is tall.", "gloss": "G3", "rep": 3, "response": "{\"T\": 0.6, \"I\": 0.1, \"N\": 0.2, \"F\": 0.3}", "T": 0.6, "I": 0.1, "N": 0.2, "F": 0.3, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:525:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Vagueness (Fuzzy)", "statement": "John is 1.75 meters tall, therefore John is tall.", "gloss": "G3", "rep": 4, "response": "{\"T\": 0.7, \"I\": 0.1, \"N\": 0.2, \"F\": 0.3}", "T": 0.7, "I": 0.1, "N": 0.2, "F": 0.3, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:526:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Vagueness (Fuzzy)", "statement": "John is 1.75 meters tall, therefore John is tall.", "gloss": "G3", "rep": 5, "response": "{\"T\": 0.65, \"I\": 0.1, \"N\": 0.15, \"F\": 0.2}", "T": 0.65, "I": 0.1, "N": 0.15, "F": 0.2, "regime": "very_weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:527:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Vagueness (Fuzzy)", "statement": "John is 1.75 meters tall, therefore John is tall.", "gloss": "G3", "rep": 6, "response": "{\"T\": 0.7, \"I\": 0.1, \"N\": 0.1, \"F\": 0.3}", "T": 0.7, "I": 0.1, "N": 0.1, "F": 0.3, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:528:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Vagueness (Fuzzy)", "statement": "John is 1.75 meters tall, therefore John is tall.", "gloss": "G3", "rep": 7, "response": "{\"T\": 0.6, \"I\": 0.1, \"N\": 0.2, \"F\": 0.3}", "T": 0.6, "I": 0.1, "N": 0.2, "F": 0.3, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:529:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Vagueness (Fuzzy)", "statement": "John is 1.75 meters tall, therefore John is tall.", "gloss": "G3", "rep": 8, "response": "{\"T\": 0.7, \"I\": 0.1, \"N\": 0.1, \"F\": 0.3}", "T": 0.7, "I": 0.1, "N": 0.1, "F": 0.3, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:530:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Vagueness (Fuzzy)", "statement": "John is 1.75 meters tall, therefore John is tall.", "gloss": "G3", "rep": 9, "response": "{\"T\": 0.6, \"I\": 0.1, \"N\": 0.2, \"F\": 0.3}", "T": 0.6, "I": 0.1, "N": 0.2, "F": 0.3, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:531:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Vagueness (Fuzzy)", "statement": "John is 1.75 meters tall, therefore John is tall.", "gloss": "G3", "rep": 0, "response": "```json\n{\n  \"T\": 0.3,\n  \"I\": 0.5,\n  \"N\": 0.2,\n  \"F\": 0.4\n}\n```", "T": 0.3, "I": 0.5, "N": 0.2, "F": 0.4, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:532:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Vagueness (Fuzzy)", "statement": "John is 1.75 meters tall, therefore John is tall.", "gloss": "G3", "rep": 1, "response": "```json\n{\n  \"T\": 0.3,\n  \"I\": 0.6,\n  \"N\": 0.2,\n  \"F\": 0.4\n}\n```", "T": 0.3, "I": 0.6, "N": 0.2, "F": 0.4, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:533:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Vagueness (Fuzzy)", "statement": "John is 1.75 meters tall, therefore John is tall.", "gloss": "G3", "rep": 2, "response": "```json\n{\n  \"T\": 0.3,\n  \"I\": 0.5,\n  \"N\": 0.4,\n  \"F\": 0.2\n}\n```", "T": 0.3, "I": 0.5, "N": 0.4, "F": 0.2, "regime": "very_weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:534:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Vagueness (Fuzzy)", "statement": "John is 1.75 meters tall, therefore John is tall.", "gloss": "G3", "rep": 3, "response": "```json\n{\n  \"T\": 0.3,\n  \"I\": 0.6,\n  \"N\": 0.4,\n  \"F\": 0.2\n}\n```", "T": 0.3, "I": 0.6, "N": 0.4, "F": 0.2, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:535:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Vagueness (Fuzzy)", "statement": "John is 1.75 meters tall, therefore John is tall.", "gloss": "G3", "rep": 4, "response": "```json\n{\n  \"T\": 0.3,\n  \"I\": 0.5,\n  \"N\": 0.2,\n  \"F\": 0.4\n}\n```", "T": 0.3, "I": 0.5, "N": 0.2, "F": 0.4, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:536:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Vagueness (Fuzzy)", "statement": "John is 1.75 meters tall, therefore John is tall.", "gloss": "G3", "rep": 5, "response": "```json\n{\n  \"T\": 0.3,\n  \"I\": 0.5,\n  \"N\": 0.4,\n  \"F\": 0.2\n}\n```", "T": 0.3, "I": 0.5, "N": 0.4, "F": 0.2, "regime": "very_weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:537:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Vagueness (Fuzzy)", "statement": "John is 1.75 meters tall, therefore John is tall.", "gloss": "G3", "rep": 6, "response": "```json\n{\n  \"T\": 0.3,\n  \"I\": 0.6,\n  \"N\": 0.1,\n  \"F\": 0.4\n}\n```", "T": 0.3, "I": 0.6, "N": 0.1, "F": 0.4, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:538:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Vagueness (Fuzzy)", "statement": "John is 1.75 meters tall, therefore John is tall.", "gloss": "G3", "rep": 7, "response": "```json\n{\n  \"T\": 0.3,\n  \"I\": 0.6,\n  \"N\": 0.1,\n  \"F\": 0.4\n}\n```", "T": 0.3, "I": 0.6, "N": 0.1, "F": 0.4, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:539:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Vagueness (Fuzzy)", "statement": "John is 1.75 meters tall, therefore John is tall.", "gloss": "G3", "rep": 8, "response": "```json\n{\n  \"T\": 0.3,\n  \"I\": 0.6,\n  \"N\": 0.2,\n  \"F\": 0.4\n}\n```", "T": 0.3, "I": 0.6, "N": 0.2, "F": 0.4, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:540:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Vagueness (Fuzzy)", "statement": "John is 1.75 meters tall, therefore John is tall.", "gloss": "G3", "rep": 9, "response": "```json\n{\n  \"T\": 0.3,\n  \"I\": 0.6,\n  \"N\": 0.2,\n  \"F\": 0.4\n}\n```", "T": 0.3, "I": 0.6, "N": 0.2, "F": 0.4, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:541:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Contradiction (Ethical)", "statement": "Lying to save an innocent life is morally right and wrong at the same time.", "gloss": "G1", "rep": 0, "response": "```json\n{\"T\": 0.7, \"I\": 0.5, \"N\": 0.2, \"F\": 0.3}\n```", "T": 0.7, "I": 0.5, "N": 0.2, "F": 0.3, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:542:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Contradiction (Ethical)", "statement": "Lying to save an innocent life is morally right and wrong at the same time.", "gloss": "G1", "rep": 1, "response": "```json\n{\"T\": 0.7, \"I\": 0.6, \"N\": 0.4, \"F\": 0.5}\n```", "T": 0.7, "I": 0.6, "N": 0.4, "F": 0.5, "regime": "strong", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:543:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Contradiction (Ethical)", "statement": "Lying to save an innocent life is morally right and wrong at the same time.", "gloss": "G1", "rep": 2, "response": "```json\n{\"T\": 0.7, \"I\": 0.5, \"N\": 0.3, \"F\": 0.6}\n```", "T": 0.7, "I": 0.5, "N": 0.3, "F": 0.6, "regime": "strong", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:544:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Contradiction (Ethical)", "statement": "Lying to save an innocent life is morally right and wrong at the same time.", "gloss": "G1", "rep": 3, "response": "```json\n{\"T\": 0.7, \"I\": 0.4, \"N\": 0.5, \"F\": 0.6}\n```", "T": 0.7, "I": 0.4, "N": 0.5, "F": 0.6, "regime": "strong", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:545:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Contradiction (Ethical)", "statement": "Lying to save an innocent life is morally right and wrong at the same time.", "gloss": "G1", "rep": 4, "response": "```json\n{\"T\": 0.7, \"I\": 0.6, \"N\": 0.3, \"F\": 0.7}\n```", "T": 0.7, "I": 0.6, "N": 0.3, "F": 0.7, "regime": "strong", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:546:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Contradiction (Ethical)", "statement": "Lying to save an innocent life is morally right and wrong at the same time.", "gloss": "G1", "rep": 5, "response": "```json\n{\"T\": 0.6, \"I\": 0.7, \"N\": 0.3, \"F\": 0.5}\n```", "T": 0.6, "I": 0.7, "N": 0.3, "F": 0.5, "regime": "strong", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:547:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Contradiction (Ethical)", "statement": "Lying to save an innocent life is morally right and wrong at the same time.", "gloss": "G1", "rep": 6, "response": "{\"T\": 0.7, \"I\": 0.6, \"N\": 0.4, \"F\": 0.4}", "T": 0.7, "I": 0.6, "N": 0.4, "F": 0.4, "regime": "strong", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:548:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Contradiction (Ethical)", "statement": "Lying to save an innocent life is morally right and wrong at the same time.", "gloss": "G1", "rep": 7, "response": "```json\n{\"T\": 0.7, \"I\": 0.5, \"N\": 0.3, \"F\": 0.6}\n```", "T": 0.7, "I": 0.5, "N": 0.3, "F": 0.6, "regime": "strong", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:549:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Contradiction (Ethical)", "statement": "Lying to save an innocent life is morally right and wrong at the same time.", "gloss": "G1", "rep": 8, "response": "{\"T\": 0.8, \"I\": 0.6, \"N\": 0.5, \"F\": 0.7}", "T": 0.8, "I": 0.6, "N": 0.5, "F": 0.7, "regime": "strong", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:550:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Contradiction (Ethical)", "statement": "Lying to save an innocent life is morally right and wrong at the same time.", "gloss": "G1", "rep": 9, "response": "```json\n{\"T\": 0.7, \"I\": 0.6, \"N\": 0.3, \"F\": 0.4}\n```", "T": 0.7, "I": 0.6, "N": 0.3, "F": 0.4, "regime": "strong", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:551:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Contradiction (Ethical)", "statement": "Lying to save an innocent life is morally right and wrong at the same time.", "gloss": "G1", "rep": 0, "response": "{\"T\": 0.7, \"I\": 0.8, \"N\": 0.3, \"F\": 0.4}", "T": 0.7, "I": 0.8, "N": 0.3, "F": 0.4, "regime": "strong", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:552:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Contradiction (Ethical)", "statement": "Lying to save an innocent life is morally right and wrong at the same time.", "gloss": "G1", "rep": 1, "response": "{\"T\": 0.7, \"I\": 0.8, \"N\": 0.2, \"F\": 0.4}", "T": 0.7, "I": 0.8, "N": 0.2, "F": 0.4, "regime": "strong", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:553:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Contradiction (Ethical)", "statement": "Lying to save an innocent life is morally right and wrong at the same time.", "gloss": "G1", "rep": 2, "response": "{\"T\": 0.7, \"I\": 0.8, \"N\": 0.3, \"F\": 0.4}", "T": 0.7, "I": 0.8, "N": 0.3, "F": 0.4, "regime": "strong", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:554:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Contradiction (Ethical)", "statement": "Lying to save an innocent life is morally right and wrong at the same time.", "gloss": "G1", "rep": 3, "response": "{\"T\": 0.8, \"I\": 0.7, \"N\": 0.3, \"F\": 0.6}", "T": 0.8, "I": 0.7, "N": 0.3, "F": 0.6, "regime": "strong", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:555:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Contradiction (Ethical)", "statement": "Lying to save an innocent life is morally right and wrong at the same time.", "gloss": "G1", "rep": 4, "response": "{\"T\": 0.7, \"I\": 0.8, \"N\": 0.2, \"F\": 0.6}", "T": 0.7, "I": 0.8, "N": 0.2, "F": 0.6, "regime": "strong", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:556:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Contradiction (Ethical)", "statement": "Lying to save an innocent life is morally right and wrong at the same time.", "gloss": "G1", "rep": 5, "response": "{\"T\": 0.8, \"I\": 0.7, \"N\": 0.3, \"F\": 0.6}", "T": 0.8, "I": 0.7, "N": 0.3, "F": 0.6, "regime": "strong", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:557:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Contradiction (Ethical)", "statement": "Lying to save an innocent life is morally right and wrong at the same time.", "gloss": "G1", "rep": 6, "response": "{\"T\": 0.7, \"I\": 0.8, \"N\": 0.3, \"F\": 0.4}", "T": 0.7, "I": 0.8, "N": 0.3, "F": 0.4, "regime": "strong", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:558:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Contradiction (Ethical)", "statement": "Lying to save an innocent life is morally right and wrong at the same time.", "gloss": "G1", "rep": 7, "response": "{\"T\": 0.8, \"I\": 0.7, \"N\": 0.3, \"F\": 0.4}", "T": 0.8, "I": 0.7, "N": 0.3, "F": 0.4, "regime": "strong", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:559:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Contradiction (Ethical)", "statement": "Lying to save an innocent life is morally right and wrong at the same time.", "gloss": "G1", "rep": 8, "response": "{\"T\": 0.7, \"I\": 0.8, \"N\": 0.3, \"F\": 0.6}", "T": 0.7, "I": 0.8, "N": 0.3, "F": 0.6, "regime": "strong", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:560:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Contradiction (Ethical)", "statement": "Lying to save an innocent life is morally right and wrong at the same time.", "gloss": "G1", "rep": 9, "response": "{\"T\": 0.7, \"I\": 0.8, \"N\": 0.3, \"F\": 0.4}", "T": 0.7, "I": 0.8, "N": 0.3, "F": 0.4, "regime": "strong", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:561:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Contradiction (Ethical)", "statement": "Lying to save an innocent life is morally right and wrong at the same time.", "gloss": "G1", "rep": 0, "response": "{\"T\": 0.7, \"I\": 0.4, \"N\": 0.2, \"F\": 0.6}", "T": 0.7, "I": 0.4, "N": 0.2, "F": 0.6, "regime": "strong", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:562:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Contradiction (Ethical)", "statement": "Lying to save an innocent life is morally right and wrong at the same time.", "gloss": "G1", "rep": 1, "response": "{\"T\": 0.7, \"I\": 0.4, \"N\": 0.2, \"F\": 0.5}", "T": 0.7, "I": 0.4, "N": 0.2, "F": 0.5, "regime": "strong", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:563:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Contradiction (Ethical)", "statement": "Lying to save an innocent life is morally right and wrong at the same time.", "gloss": "G1", "rep": 2, "response": "{\"T\": 0.7, \"I\": 0.4, \"N\": 0.2, \"F\": 0.6}", "T": 0.7, "I": 0.4, "N": 0.2, "F": 0.6, "regime": "strong", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:564:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Contradiction (Ethical)", "statement": "Lying to save an innocent life is morally right and wrong at the same time.", "gloss": "G1", "rep": 3, "response": "{\"T\": 0.7, \"I\": 0.4, \"N\": 0.3, \"F\": 0.6}", "T": 0.7, "I": 0.4, "N": 0.3, "F": 0.6, "regime": "strong", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:565:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Contradiction (Ethical)", "statement": "Lying to save an innocent life is morally right and wrong at the same time.", "gloss": "G1", "rep": 4, "response": "{\"T\": 0.7, \"I\": 0.4, \"N\": 0.2, \"F\": 0.6}", "T": 0.7, "I": 0.4, "N": 0.2, "F": 0.6, "regime": "strong", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:566:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Contradiction (Ethical)", "statement": "Lying to save an innocent life is morally right and wrong at the same time.", "gloss": "G1", "rep": 5, "response": "{\"T\": 0.7, \"I\": 0.4, \"N\": 0.2, \"F\": 0.6}", "T": 0.7, "I": 0.4, "N": 0.2, "F": 0.6, "regime": "strong", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:567:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Contradiction (Ethical)", "statement": "Lying to save an innocent life is morally right and wrong at the same time.", "gloss": "G1", "rep": 6, "response": "{\"T\": 0.7, \"I\": 0.4, \"N\": 0.3, \"F\": 0.6}", "T": 0.7, "I": 0.4, "N": 0.3, "F": 0.6, "regime": "strong", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:568:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Contradiction (Ethical)", "statement": "Lying to save an innocent life is morally right and wrong at the same time.", "gloss": "G1", "rep": 7, "response": "{\"T\": 0.7, \"I\": 0.4, \"N\": 0.2, \"F\": 0.6}", "T": 0.7, "I": 0.4, "N": 0.2, "F": 0.6, "regime": "strong", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:569:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Contradiction (Ethical)", "statement": "Lying to save an innocent life is morally right and wrong at the same time.", "gloss": "G1", "rep": 8, "response": "{\"T\": 0.7, \"I\": 0.4, \"N\": 0.3, \"F\": 0.6}", "T": 0.7, "I": 0.4, "N": 0.3, "F": 0.6, "regime": "strong", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:570:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Contradiction (Ethical)", "statement": "Lying to save an innocent life is morally right and wrong at the same time.", "gloss": "G1", "rep": 9, "response": "{\"T\": 0.7, \"I\": 0.4, \"N\": 0.2, \"F\": 0.5}", "T": 0.7, "I": 0.4, "N": 0.2, "F": 0.5, "regime": "strong", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:571:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Contradiction (Ethical)", "statement": "Lying to save an innocent life is morally right and wrong at the same time.", "gloss": "G1", "rep": 0, "response": "```json\n{\"T\": 0.7, \"I\": 0.5, \"N\": 0.2, \"F\": 0.3}\n```", "T": 0.7, "I": 0.5, "N": 0.2, "F": 0.3, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:572:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Contradiction (Ethical)", "statement": "Lying to save an innocent life is morally right and wrong at the same time.", "gloss": "G1", "rep": 1, "response": "```json\n{\"T\": 0.7, \"I\": 0.5, \"N\": 0.2, \"F\": 0.3}\n```", "T": 0.7, "I": 0.5, "N": 0.2, "F": 0.3, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:573:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Contradiction (Ethical)", "statement": "Lying to save an innocent life is morally right and wrong at the same time.", "gloss": "G1", "rep": 2, "response": "```json\n{\"T\": 0.7, \"I\": 0.5, \"N\": 0.2, \"F\": 0.3}\n```", "T": 0.7, "I": 0.5, "N": 0.2, "F": 0.3, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:574:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Contradiction (Ethical)", "statement": "Lying to save an innocent life is morally right and wrong at the same time.", "gloss": "G1", "rep": 3, "response": "```json\n{\"T\": 0.7, \"I\": 0.5, \"N\": 0.3, \"F\": 0.6}\n```", "T": 0.7, "I": 0.5, "N": 0.3, "F": 0.6, "regime": "strong", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:575:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Contradiction (Ethical)", "statement": "Lying to save an innocent life is morally right and wrong at the same time.", "gloss": "G1", "rep": 4, "response": "```json\n{\"T\": 0.7, \"I\": 0.5, \"N\": 0.2, \"F\": 0.3}\n```", "T": 0.7, "I": 0.5, "N": 0.2, "F": 0.3, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:576:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Contradiction (Ethical)", "statement": "Lying to save an innocent life is morally right and wrong at the same time.", "gloss": "G1", "rep": 5, "response": "```json\n{\"T\": 0.7, \"I\": 0.5, \"N\": 0.3, \"F\": 0.4}\n```", "T": 0.7, "I": 0.5, "N": 0.3, "F": 0.4, "regime": "strong", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:577:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Contradiction (Ethical)", "statement": "Lying to save an innocent life is morally right and wrong at the same time.", "gloss": "G1", "rep": 6, "response": "```json\n{\"T\": 0.7, \"I\": 0.5, \"N\": 0.2, \"F\": 0.3}\n```", "T": 0.7, "I": 0.5, "N": 0.2, "F": 0.3, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:578:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Contradiction (Ethical)", "statement": "Lying to save an innocent life is morally right and wrong at the same time.", "gloss": "G1", "rep": 7, "response": "```json\n{\"T\": 0.7, \"I\": 0.5, \"N\": 0.3, \"F\": 0.6}\n```", "T": 0.7, "I": 0.5, "N": 0.3, "F": 0.6, "regime": "strong", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:579:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Contradiction (Ethical)", "statement": "Lying to save an innocent life is morally right and wrong at the same time.", "gloss": "G1", "rep": 8, "response": "```json\n{\"T\": 0.7, \"I\": 0.5, \"N\": 0.2, \"F\": 0.3}\n```", "T": 0.7, "I": 0.5, "N": 0.2, "F": 0.3, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:580:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Contradiction (Ethical)", "statement": "Lying to save an innocent life is morally right and wrong at the same time.", "gloss": "G1", "rep": 9, "response": "```json\n{\"T\": 0.7, \"I\": 0.5, \"N\": 0.2, \"F\": 0.3}\n```", "T": 0.7, "I": 0.5, "N": 0.2, "F": 0.3, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:581:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Contradiction (Ethical)", "statement": "Lying to save an innocent life is morally right and wrong at the same time.", "gloss": "G1", "rep": 0, "response": "{\"T\": 0.6, \"I\": 0.7, \"N\": 0.5, \"F\": 0.4}", "T": 0.6, "I": 0.7, "N": 0.5, "F": 0.4, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:582:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Contradiction (Ethical)", "statement": "Lying to save an innocent life is morally right and wrong at the same time.", "gloss": "G1", "rep": 1, "response": "{\"T\": 0.6, \"I\": 0.7, \"N\": 0.3, \"F\": 0.5}", "T": 0.6, "I": 0.7, "N": 0.3, "F": 0.5, "regime": "strong", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:583:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Contradiction (Ethical)", "statement": "Lying to save an innocent life is morally right and wrong at the same time.", "gloss": "G1", "rep": 2, "response": "{\"T\": 0.7, \"I\": 0.6, \"N\": 0.3, \"F\": 0.5}", "T": 0.7, "I": 0.6, "N": 0.3, "F": 0.5, "regime": "strong", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:584:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Contradiction (Ethical)", "statement": "Lying to save an innocent life is morally right and wrong at the same time.", "gloss": "G1", "rep": 3, "response": "{\"T\": 0.7, \"I\": 0.5, \"N\": 0.3, \"F\": 0.6}", "T": 0.7, "I": 0.5, "N": 0.3, "F": 0.6, "regime": "strong", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:585:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Contradiction (Ethical)", "statement": "Lying to save an innocent life is morally right and wrong at the same time.", "gloss": "G1", "rep": 4, "response": "{\"T\": 0.7, \"I\": 0.6, \"N\": 0.5, \"F\": 0.4}", "T": 0.7, "I": 0.6, "N": 0.5, "F": 0.4, "regime": "strong", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:586:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Contradiction (Ethical)", "statement": "Lying to save an innocent life is morally right and wrong at the same time.", "gloss": "G1", "rep": 5, "response": "{\"T\": 0.7, \"I\": 0.6, \"N\": 0.3, \"F\": 0.5}", "T": 0.7, "I": 0.6, "N": 0.3, "F": 0.5, "regime": "strong", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:587:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Contradiction (Ethical)", "statement": "Lying to save an innocent life is morally right and wrong at the same time.", "gloss": "G1", "rep": 6, "response": "{\"T\": 0.7, \"I\": 0.6, \"N\": 0.3, \"F\": 0.5}", "T": 0.7, "I": 0.6, "N": 0.3, "F": 0.5, "regime": "strong", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:588:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Contradiction (Ethical)", "statement": "Lying to save an innocent life is morally right and wrong at the same time.", "gloss": "G1", "rep": 7, "response": "{\"T\": 0.7, \"I\": 0.6, \"N\": 0.3, \"F\": 0.5}", "T": 0.7, "I": 0.6, "N": 0.3, "F": 0.5, "regime": "strong", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:589:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Contradiction (Ethical)", "statement": "Lying to save an innocent life is morally right and wrong at the same time.", "gloss": "G1", "rep": 8, "response": "{\"T\": 0.6, \"I\": 0.7, \"N\": 0.5, \"F\": 0.4}", "T": 0.6, "I": 0.7, "N": 0.5, "F": 0.4, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:590:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Contradiction (Ethical)", "statement": "Lying to save an innocent life is morally right and wrong at the same time.", "gloss": "G1", "rep": 9, "response": "{\"T\": 0.6, \"I\": 0.5, \"N\": 0.3, \"F\": 0.4}", "T": 0.6, "I": 0.5, "N": 0.3, "F": 0.4, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:591:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Contradiction (Ethical)", "statement": "Lying to save an innocent life is morally right and wrong at the same time.", "gloss": "G1", "rep": 0, "response": "```json\n{\n  \"T\": 0.7,\n  \"I\": 0.6,\n  \"N\": 0.5,\n  \"F\": 0.4\n}\n```", "T": 0.7, "I": 0.6, "N": 0.5, "F": 0.4, "regime": "strong", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:592:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Contradiction (Ethical)", "statement": "Lying to save an innocent life is morally right and wrong at the same time.", "gloss": "G1", "rep": 1, "response": "```json\n{\n  \"T\": 0.75,\n  \"I\": 0.60,\n  \"N\": 0.50,\n  \"F\": 0.30\n}\n```", "T": 0.75, "I": 0.6, "N": 0.5, "F": 0.3, "regime": "strong", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:593:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Contradiction (Ethical)", "statement": "Lying to save an innocent life is morally right and wrong at the same time.", "gloss": "G1", "rep": 2, "response": "```json\n{\n  \"T\": 0.75,\n  \"I\": 0.60,\n  \"N\": 0.30,\n  \"F\": 0.40\n}\n```", "T": 0.75, "I": 0.6, "N": 0.3, "F": 0.4, "regime": "strong", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:594:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Contradiction (Ethical)", "statement": "Lying to save an innocent life is morally right and wrong at the same time.", "gloss": "G1", "rep": 3, "response": "```json\n{\n  \"T\": 0.7,\n  \"I\": 0.5,\n  \"N\": 0.4,\n  \"F\": 0.3\n}\n```", "T": 0.7, "I": 0.5, "N": 0.4, "F": 0.3, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:595:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Contradiction (Ethical)", "statement": "Lying to save an innocent life is morally right and wrong at the same time.", "gloss": "G1", "rep": 4, "response": "```json\n{\n  \"T\": 0.75,\n  \"I\": 0.60,\n  \"N\": 0.50,\n  \"F\": 0.30\n}\n```", "T": 0.75, "I": 0.6, "N": 0.5, "F": 0.3, "regime": "strong", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:596:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Contradiction (Ethical)", "statement": "Lying to save an innocent life is morally right and wrong at the same time.", "gloss": "G1", "rep": 5, "response": "```json\n{\n  \"T\": 0.7,\n  \"I\": 0.5,\n  \"N\": 0.3,\n  \"F\": 0.4\n}\n```", "T": 0.7, "I": 0.5, "N": 0.3, "F": 0.4, "regime": "strong", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:597:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Contradiction (Ethical)", "statement": "Lying to save an innocent life is morally right and wrong at the same time.", "gloss": "G1", "rep": 6, "response": "```json\n{\n  \"T\": 0.75,\n  \"I\": 0.60,\n  \"N\": 0.40,\n  \"F\": 0.30\n}\n```", "T": 0.75, "I": 0.6, "N": 0.4, "F": 0.3, "regime": "strong", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:598:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Contradiction (Ethical)", "statement": "Lying to save an innocent life is morally right and wrong at the same time.", "gloss": "G1", "rep": 7, "response": "```json\n{\n  \"T\": 0.75,\n  \"I\": 0.65,\n  \"N\": 0.50,\n  \"F\": 0.30\n}\n```", "T": 0.75, "I": 0.65, "N": 0.5, "F": 0.3, "regime": "strong", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:599:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Contradiction (Ethical)", "statement": "Lying to save an innocent life is morally right and wrong at the same time.", "gloss": "G1", "rep": 8, "response": "```json\n{\n  \"T\": 0.75,\n  \"I\": 0.60,\n  \"N\": 0.30,\n  \"F\": 0.20\n}\n```", "T": 0.75, "I": 0.6, "N": 0.3, "F": 0.2, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:600:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Contradiction (Ethical)", "statement": "Lying to save an innocent life is morally right and wrong at the same time.", "gloss": "G1", "rep": 9, "response": "```json\n{\n  \"T\": 0.75,\n  \"I\": 0.60,\n  \"N\": 0.40,\n  \"F\": 0.30\n}\n```", "T": 0.75, "I": 0.6, "N": 0.4, "F": 0.3, "regime": "strong", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:601:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Contradiction (Ethical)", "statement": "Lying to save an innocent life is morally right and wrong at the same time.", "gloss": "G2", "rep": 0, "response": "```json\n{\"T\": 0.7, \"I\": 0.5, \"N\": 0.2, \"F\": 0.6}\n```", "T": 0.7, "I": 0.5, "N": 0.2, "F": 0.6, "regime": "strong", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:602:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Contradiction (Ethical)", "statement": "Lying to save an innocent life is morally right and wrong at the same time.", "gloss": "G2", "rep": 1, "response": "```json\n{\"T\": 0.7, \"I\": 0.6, \"N\": 0.3, \"F\": 0.6}\n```", "T": 0.7, "I": 0.6, "N": 0.3, "F": 0.6, "regime": "strong", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:603:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Contradiction (Ethical)", "statement": "Lying to save an innocent life is morally right and wrong at the same time.", "gloss": "G2", "rep": 2, "response": "{\"T\": 0.8, \"I\": 0.5, \"N\": 0.2, \"F\": 0.6}", "T": 0.8, "I": 0.5, "N": 0.2, "F": 0.6, "regime": "strong", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:604:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Contradiction (Ethical)", "statement": "Lying to save an innocent life is morally right and wrong at the same time.", "gloss": "G2", "rep": 3, "response": "{\"T\": 0.7, \"I\": 0.5, \"N\": 0.2, \"F\": 0.6}", "T": 0.7, "I": 0.5, "N": 0.2, "F": 0.6, "regime": "strong", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:605:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Contradiction (Ethical)", "statement": "Lying to save an innocent life is morally right and wrong at the same time.", "gloss": "G2", "rep": 4, "response": "```json\n{\"T\": 0.8, \"I\": 0.7, \"N\": 0.3, \"F\": 0.6}\n```", "T": 0.8, "I": 0.7, "N": 0.3, "F": 0.6, "regime": "strong", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:606:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Contradiction (Ethical)", "statement": "Lying to save an innocent life is morally right and wrong at the same time.", "gloss": "G2", "rep": 5, "response": "{\"T\": 0.7, \"I\": 0.5, \"N\": 0.3, \"F\": 0.6}", "T": 0.7, "I": 0.5, "N": 0.3, "F": 0.6, "regime": "strong", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:607:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Contradiction (Ethical)", "statement": "Lying to save an innocent life is morally right and wrong at the same time.", "gloss": "G2", "rep": 6, "response": "```json\n{\"T\": 0.7, \"I\": 0.6, \"N\": 0.3, \"F\": 0.5}\n```", "T": 0.7, "I": 0.6, "N": 0.3, "F": 0.5, "regime": "strong", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:608:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Contradiction (Ethical)", "statement": "Lying to save an innocent life is morally right and wrong at the same time.", "gloss": "G2", "rep": 7, "response": "```json\n{\"T\": 0.7, \"I\": 0.5, \"N\": 0.3, \"F\": 0.5}\n```", "T": 0.7, "I": 0.5, "N": 0.3, "F": 0.5, "regime": "strong", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:609:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Contradiction (Ethical)", "statement": "Lying to save an innocent life is morally right and wrong at the same time.", "gloss": "G2", "rep": 8, "response": "```json\n{\"T\": 0.7, \"I\": 0.6, \"N\": 0.3, \"F\": 0.5}\n```", "T": 0.7, "I": 0.6, "N": 0.3, "F": 0.5, "regime": "strong", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:610:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Contradiction (Ethical)", "statement": "Lying to save an innocent life is morally right and wrong at the same time.", "gloss": "G2", "rep": 9, "response": "```json\n{\"T\": 0.7, \"I\": 0.8, \"N\": 0.4, \"F\": 0.5}\n```", "T": 0.7, "I": 0.8, "N": 0.4, "F": 0.5, "regime": "strong", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:611:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Contradiction (Ethical)", "statement": "Lying to save an innocent life is morally right and wrong at the same time.", "gloss": "G2", "rep": 0, "response": "{\"T\": 0.8, \"I\": 0.7, \"N\": 0.3, \"F\": 0.6}", "T": 0.8, "I": 0.7, "N": 0.3, "F": 0.6, "regime": "strong", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:612:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Contradiction (Ethical)", "statement": "Lying to save an innocent life is morally right and wrong at the same time.", "gloss": "G2", "rep": 1, "response": "{\"T\": 0.8, \"I\": 0.7, \"N\": 0.3, \"F\": 0.6}", "T": 0.8, "I": 0.7, "N": 0.3, "F": 0.6, "regime": "strong", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:613:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Contradiction (Ethical)", "statement": "Lying to save an innocent life is morally right and wrong at the same time.", "gloss": "G2", "rep": 2, "response": "{\"T\": 0.8, \"I\": 0.6, \"N\": 0.3, \"F\": 0.4}", "T": 0.8, "I": 0.6, "N": 0.3, "F": 0.4, "regime": "strong", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:614:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Contradiction (Ethical)", "statement": "Lying to save an innocent life is morally right and wrong at the same time.", "gloss": "G2", "rep": 3, "response": "{\"T\": 0.7, \"I\": 0.6, \"N\": 0.3, \"F\": 0.4}", "T": 0.7, "I": 0.6, "N": 0.3, "F": 0.4, "regime": "strong", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:615:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Contradiction (Ethical)", "statement": "Lying to save an innocent life is morally right and wrong at the same time.", "gloss": "G2", "rep": 4, "response": "{\"T\": 0.8, \"I\": 0.7, \"N\": 0.3, \"F\": 0.6}", "T": 0.8, "I": 0.7, "N": 0.3, "F": 0.6, "regime": "strong", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:616:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Contradiction (Ethical)", "statement": "Lying to save an innocent life is morally right and wrong at the same time.", "gloss": "G2", "rep": 5, "response": "{\"T\": 0.7, \"I\": 0.8, \"N\": 0.3, \"F\": 0.4}", "T": 0.7, "I": 0.8, "N": 0.3, "F": 0.4, "regime": "strong", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:617:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Contradiction (Ethical)", "statement": "Lying to save an innocent life is morally right and wrong at the same time.", "gloss": "G2", "rep": 6, "response": "{\"T\": 0.8, \"I\": 0.7, \"N\": 0.3, \"F\": 0.4}", "T": 0.8, "I": 0.7, "N": 0.3, "F": 0.4, "regime": "strong", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:618:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Contradiction (Ethical)", "statement": "Lying to save an innocent life is morally right and wrong at the same time.", "gloss": "G2", "rep": 7, "response": "{\"T\": 0.7, \"I\": 0.8, \"N\": 0.3, \"F\": 0.4}", "T": 0.7, "I": 0.8, "N": 0.3, "F": 0.4, "regime": "strong", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:619:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Contradiction (Ethical)", "statement": "Lying to save an innocent life is morally right and wrong at the same time.", "gloss": "G2", "rep": 8, "response": "{\"T\": 0.8, \"I\": 0.7, \"N\": 0.3, \"F\": 0.2}", "T": 0.8, "I": 0.7, "N": 0.3, "F": 0.2, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:620:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Contradiction (Ethical)", "statement": "Lying to save an innocent life is morally right and wrong at the same time.", "gloss": "G2", "rep": 9, "response": "{\"T\": 0.7, \"I\": 0.8, \"N\": 0.3, \"F\": 0.6}", "T": 0.7, "I": 0.8, "N": 0.3, "F": 0.6, "regime": "strong", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:621:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Contradiction (Ethical)", "statement": "Lying to save an innocent life is morally right and wrong at the same time.", "gloss": "G2", "rep": 0, "response": "{\"T\": 0.7, \"I\": 0.4, \"N\": 0.2, \"F\": 0.6}", "T": 0.7, "I": 0.4, "N": 0.2, "F": 0.6, "regime": "strong", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:622:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Contradiction (Ethical)", "statement": "Lying to save an innocent life is morally right and wrong at the same time.", "gloss": "G2", "rep": 1, "response": "{\"T\": 0.7, \"I\": 0.4, \"N\": 0.2, \"F\": 0.6}", "T": 0.7, "I": 0.4, "N": 0.2, "F": 0.6, "regime": "strong", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:623:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Contradiction (Ethical)", "statement": "Lying to save an innocent life is morally right and wrong at the same time.", "gloss": "G2", "rep": 2, "response": "{\"T\": 0.7, \"I\": 0.4, \"N\": 0.2, \"F\": 0.6}", "T": 0.7, "I": 0.4, "N": 0.2, "F": 0.6, "regime": "strong", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:624:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Contradiction (Ethical)", "statement": "Lying to save an innocent life is morally right and wrong at the same time.", "gloss": "G2", "rep": 3, "response": "{\"T\": 0.7, \"I\": 0.4, \"N\": 0.2, \"F\": 0.6}", "T": 0.7, "I": 0.4, "N": 0.2, "F": 0.6, "regime": "strong", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:625:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Contradiction (Ethical)", "statement": "Lying to save an innocent life is morally right and wrong at the same time.", "gloss": "G2", "rep": 4, "response": "{\"T\": 0.7, \"I\": 0.4, \"N\": 0.2, \"F\": 0.5}", "T": 0.7, "I": 0.4, "N": 0.2, "F": 0.5, "regime": "strong", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:626:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Contradiction (Ethical)", "statement": "Lying to save an innocent life is morally right and wrong at the same time.", "gloss": "G2", "rep": 5, "response": "{\"T\": 0.7, \"I\": 0.4, \"N\": 0.2, \"F\": 0.6}", "T": 0.7, "I": 0.4, "N": 0.2, "F": 0.6, "regime": "strong", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:627:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Contradiction (Ethical)", "statement": "Lying to save an innocent life is morally right and wrong at the same time.", "gloss": "G2", "rep": 6, "response": "{\"T\": 0.7, \"I\": 0.4, \"N\": 0.2, \"F\": 0.6}", "T": 0.7, "I": 0.4, "N": 0.2, "F": 0.6, "regime": "strong", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:628:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Contradiction (Ethical)", "statement": "Lying to save an innocent life is morally right and wrong at the same time.", "gloss": "G2", "rep": 7, "response": "{\"T\": 0.7, \"I\": 0.4, \"N\": 0.2, \"F\": 0.6}", "T": 0.7, "I": 0.4, "N": 0.2, "F": 0.6, "regime": "strong", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:629:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Contradiction (Ethical)", "statement": "Lying to save an innocent life is morally right and wrong at the same time.", "gloss": "G2", "rep": 8, "response": "{\"T\": 0.7, \"I\": 0.4, \"N\": 0.2, \"F\": 0.6}", "T": 0.7, "I": 0.4, "N": 0.2, "F": 0.6, "regime": "strong", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:630:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Contradiction (Ethical)", "statement": "Lying to save an innocent life is morally right and wrong at the same time.", "gloss": "G2", "rep": 9, "response": "{\"T\": 0.7, \"I\": 0.4, \"N\": 0.2, \"F\": 0.6}", "T": 0.7, "I": 0.4, "N": 0.2, "F": 0.6, "regime": "strong", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:631:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Contradiction (Ethical)", "statement": "Lying to save an innocent life is morally right and wrong at the same time.", "gloss": "G2", "rep": 0, "response": "```json\n{\"T\": 0.7, \"I\": 0.5, \"N\": 0.3, \"F\": 0.6}\n```", "T": 0.7, "I": 0.5, "N": 0.3, "F": 0.6, "regime": "strong", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:632:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Contradiction (Ethical)", "statement": "Lying to save an innocent life is morally right and wrong at the same time.", "gloss": "G2", "rep": 1, "response": "```json\n{\"T\": 0.7, \"I\": 0.5, \"N\": 0.3, \"F\": 0.4}\n```", "T": 0.7, "I": 0.5, "N": 0.3, "F": 0.4, "regime": "strong", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:633:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Contradiction (Ethical)", "statement": "Lying to save an innocent life is morally right and wrong at the same time.", "gloss": "G2", "rep": 2, "response": "```json\n{\"T\": 0.7, \"I\": 0.5, \"N\": 0.3, \"F\": 0.4}\n```", "T": 0.7, "I": 0.5, "N": 0.3, "F": 0.4, "regime": "strong", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:634:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Contradiction (Ethical)", "statement": "Lying to save an innocent life is morally right and wrong at the same time.", "gloss": "G2", "rep": 3, "response": "```json\n{\"T\": 0.7, \"I\": 0.5, \"N\": 0.3, \"F\": 0.4}\n```", "T": 0.7, "I": 0.5, "N": 0.3, "F": 0.4, "regime": "strong", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:635:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Contradiction (Ethical)", "statement": "Lying to save an innocent life is morally right and wrong at the same time.", "gloss": "G2", "rep": 4, "response": "```json\n{\"T\": 0.7, \"I\": 0.5, \"N\": 0.3, \"F\": 0.4}\n```", "T": 0.7, "I": 0.5, "N": 0.3, "F": 0.4, "regime": "strong", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:636:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Contradiction (Ethical)", "statement": "Lying to save an innocent life is morally right and wrong at the same time.", "gloss": "G2", "rep": 5, "response": "```json\n{\"T\": 0.7, \"I\": 0.5, \"N\": 0.3, \"F\": 0.6}\n```", "T": 0.7, "I": 0.5, "N": 0.3, "F": 0.6, "regime": "strong", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:637:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Contradiction (Ethical)", "statement": "Lying to save an innocent life is morally right and wrong at the same time.", "gloss": "G2", "rep": 6, "response": "```json\n{\"T\": 0.7, \"I\": 0.5, \"N\": 0.3, \"F\": 0.6}\n```", "T": 0.7, "I": 0.5, "N": 0.3, "F": 0.6, "regime": "strong", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:638:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Contradiction (Ethical)", "statement": "Lying to save an innocent life is morally right and wrong at the same time.", "gloss": "G2", "rep": 7, "response": "```json\n{\"T\": 0.7, \"I\": 0.5, \"N\": 0.3, \"F\": 0.4}\n```", "T": 0.7, "I": 0.5, "N": 0.3, "F": 0.4, "regime": "strong", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:639:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Contradiction (Ethical)", "statement": "Lying to save an innocent life is morally right and wrong at the same time.", "gloss": "G2", "rep": 8, "response": "```json\n{\"T\": 0.7, \"I\": 0.5, \"N\": 0.3, \"F\": 0.4}\n```", "T": 0.7, "I": 0.5, "N": 0.3, "F": 0.4, "regime": "strong", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:640:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Contradiction (Ethical)", "statement": "Lying to save an innocent life is morally right and wrong at the same time.", "gloss": "G2", "rep": 9, "response": "```json\n{\"T\": 0.7, \"I\": 0.5, \"N\": 0.3, \"F\": 0.4}\n```", "T": 0.7, "I": 0.5, "N": 0.3, "F": 0.4, "regime": "strong", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:641:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Contradiction (Ethical)", "statement": "Lying to save an innocent life is morally right and wrong at the same time.", "gloss": "G2", "rep": 0, "response": "{\"T\": 0.6, \"I\": 0.7, \"N\": 0.3, \"F\": 0.5}", "T": 0.6, "I": 0.7, "N": 0.3, "F": 0.5, "regime": "strong", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:642:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Contradiction (Ethical)", "statement": "Lying to save an innocent life is morally right and wrong at the same time.", "gloss": "G2", "rep": 1, "response": "{\"T\": 0.7, \"I\": 0.6, \"N\": 0.2, \"F\": 0.5}", "T": 0.7, "I": 0.6, "N": 0.2, "F": 0.5, "regime": "strong", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:643:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Contradiction (Ethical)", "statement": "Lying to save an innocent life is morally right and wrong at the same time.", "gloss": "G2", "rep": 2, "response": "{\"T\": 0.7, \"I\": 0.6, \"N\": 0.3, \"F\": 0.5}", "T": 0.7, "I": 0.6, "N": 0.3, "F": 0.5, "regime": "strong", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:644:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Contradiction (Ethical)", "statement": "Lying to save an innocent life is morally right and wrong at the same time.", "gloss": "G2", "rep": 3, "response": "{\"T\": 0.6, \"I\": 0.7, \"N\": 0.3, \"F\": 0.5}", "T": 0.6, "I": 0.7, "N": 0.3, "F": 0.5, "regime": "strong", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:645:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Contradiction (Ethical)", "statement": "Lying to save an innocent life is morally right and wrong at the same time.", "gloss": "G2", "rep": 4, "response": "{\"T\": 0.7, \"I\": 0.6, \"N\": 0.2, \"F\": 0.5}", "T": 0.7, "I": 0.6, "N": 0.2, "F": 0.5, "regime": "strong", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:646:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Contradiction (Ethical)", "statement": "Lying to save an innocent life is morally right and wrong at the same time.", "gloss": "G2", "rep": 5, "response": "{\"T\": 0.7, \"I\": 0.6, \"N\": 0.2, \"F\": 0.5}", "T": 0.7, "I": 0.6, "N": 0.2, "F": 0.5, "regime": "strong", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:647:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Contradiction (Ethical)", "statement": "Lying to save an innocent life is morally right and wrong at the same time.", "gloss": "G2", "rep": 6, "response": "{\"T\": 0.7, \"I\": 0.6, \"N\": 0.3, \"F\": 0.5}", "T": 0.7, "I": 0.6, "N": 0.3, "F": 0.5, "regime": "strong", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:648:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Contradiction (Ethical)", "statement": "Lying to save an innocent life is morally right and wrong at the same time.", "gloss": "G2", "rep": 7, "response": "{\"T\": 0.6, \"I\": 0.7, \"N\": 0.2, \"F\": 0.5}", "T": 0.6, "I": 0.7, "N": 0.2, "F": 0.5, "regime": "strong", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:649:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Contradiction (Ethical)", "statement": "Lying to save an innocent life is morally right and wrong at the same time.", "gloss": "G2", "rep": 8, "response": "{\"T\": 0.6, \"I\": 0.7, \"N\": 0.3, \"F\": 0.5}", "T": 0.6, "I": 0.7, "N": 0.3, "F": 0.5, "regime": "strong", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:650:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Contradiction (Ethical)", "statement": "Lying to save an innocent life is morally right and wrong at the same time.", "gloss": "G2", "rep": 9, "response": "{\"T\": 0.7, \"I\": 0.6, \"N\": 0.2, \"F\": 0.5}", "T": 0.7, "I": 0.6, "N": 0.2, "F": 0.5, "regime": "strong", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:651:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Contradiction (Ethical)", "statement": "Lying to save an innocent life is morally right and wrong at the same time.", "gloss": "G2", "rep": 0, "response": "```json\n{\n  \"T\": 0.75,\n  \"I\": 0.60,\n  \"N\": 0.30,\n  \"F\": 0.40\n}\n```", "T": 0.75, "I": 0.6, "N": 0.3, "F": 0.4, "regime": "strong", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:652:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Contradiction (Ethical)", "statement": "Lying to save an innocent life is morally right and wrong at the same time.", "gloss": "G2", "rep": 1, "response": "```json\n{\n  \"T\": 0.75,\n  \"I\": 0.60,\n  \"N\": 0.40,\n  \"F\": 0.30\n}\n```", "T": 0.75, "I": 0.6, "N": 0.4, "F": 0.3, "regime": "strong", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:653:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Contradiction (Ethical)", "statement": "Lying to save an innocent life is morally right and wrong at the same time.", "gloss": "G2", "rep": 2, "response": "```json\n{\n  \"T\": 0.75,\n  \"I\": 0.30,\n  \"N\": 0.10,\n  \"F\": 0.60\n}\n```", "T": 0.75, "I": 0.3, "N": 0.1, "F": 0.6, "regime": "strong", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:654:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Contradiction (Ethical)", "statement": "Lying to save an innocent life is morally right and wrong at the same time.", "gloss": "G2", "rep": 3, "response": "```json\n{\n  \"T\": 0.75,\n  \"I\": 0.6,\n  \"N\": 0.3,\n  \"F\": 0.5\n}\n```", "T": 0.75, "I": 0.6, "N": 0.3, "F": 0.5, "regime": "strong", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:655:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Contradiction (Ethical)", "statement": "Lying to save an innocent life is morally right and wrong at the same time.", "gloss": "G2", "rep": 4, "response": "```json\n{\n  \"T\": 0.75,\n  \"I\": 0.60,\n  \"N\": 0.30,\n  \"F\": 0.20\n}\n```", "T": 0.75, "I": 0.6, "N": 0.3, "F": 0.2, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:656:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Contradiction (Ethical)", "statement": "Lying to save an innocent life is morally right and wrong at the same time.", "gloss": "G2", "rep": 5, "response": "```json\n{\n  \"T\": 0.75,\n  \"I\": 0.65,\n  \"N\": 0.40,\n  \"F\": 0.50\n}\n```", "T": 0.75, "I": 0.65, "N": 0.4, "F": 0.5, "regime": "strong", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:657:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Contradiction (Ethical)", "statement": "Lying to save an innocent life is morally right and wrong at the same time.", "gloss": "G2", "rep": 6, "response": "```json\n{\n  \"T\": 0.7,\n  \"I\": 0.6,\n  \"N\": 0.3,\n  \"F\": 0.4\n}\n```", "T": 0.7, "I": 0.6, "N": 0.3, "F": 0.4, "regime": "strong", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:658:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Contradiction (Ethical)", "statement": "Lying to save an innocent life is morally right and wrong at the same time.", "gloss": "G2", "rep": 7, "response": "```json\n{\n  \"T\": 0.65,\n  \"I\": 0.70,\n  \"N\": 0.40,\n  \"F\": 0.30\n}\n```", "T": 0.65, "I": 0.7, "N": 0.4, "F": 0.3, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:659:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Contradiction (Ethical)", "statement": "Lying to save an innocent life is morally right and wrong at the same time.", "gloss": "G2", "rep": 8, "response": "```json\n{\n  \"T\": 0.75,\n  \"I\": 0.65,\n  \"N\": 0.40,\n  \"F\": 0.30\n}\n```", "T": 0.75, "I": 0.65, "N": 0.4, "F": 0.3, "regime": "strong", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:660:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Contradiction (Ethical)", "statement": "Lying to save an innocent life is morally right and wrong at the same time.", "gloss": "G2", "rep": 9, "response": "```json\n{\n  \"T\": 0.75,\n  \"I\": 0.60,\n  \"N\": 0.30,\n  \"F\": 0.40\n}\n```", "T": 0.75, "I": 0.6, "N": 0.3, "F": 0.4, "regime": "strong", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:661:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Contradiction (Ethical)", "statement": "Lying to save an innocent life is morally right and wrong at the same time.", "gloss": "G3", "rep": 0, "response": "```json\n{\"T\": 0.7, \"I\": 0.6, \"N\": 0.5, \"F\": 0.4}\n```", "T": 0.7, "I": 0.6, "N": 0.5, "F": 0.4, "regime": "strong", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:662:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Contradiction (Ethical)", "statement": "Lying to save an innocent life is morally right and wrong at the same time.", "gloss": "G3", "rep": 1, "response": "```json\n{\"T\": 0.7, \"I\": 0.6, \"N\": 0.5, \"F\": 0.2}\n```", "T": 0.7, "I": 0.6, "N": 0.5, "F": 0.2, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:663:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Contradiction (Ethical)", "statement": "Lying to save an innocent life is morally right and wrong at the same time.", "gloss": "G3", "rep": 2, "response": "```json\n{\"T\": 0.7, \"I\": 0.5, \"N\": 0.6, \"F\": 0.4}\n```", "T": 0.7, "I": 0.5, "N": 0.6, "F": 0.4, "regime": "strong", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:664:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Contradiction (Ethical)", "statement": "Lying to save an innocent life is morally right and wrong at the same time.", "gloss": "G3", "rep": 3, "response": "```json\n{\"T\": 0.7, \"I\": 0.4, \"N\": 0.6, \"F\": 0.5}\n```", "T": 0.7, "I": 0.4, "N": 0.6, "F": 0.5, "regime": "strong", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:665:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Contradiction (Ethical)", "statement": "Lying to save an innocent life is morally right and wrong at the same time.", "gloss": "G3", "rep": 4, "response": "```json\n{\"T\": 0.6, \"I\": 0.4, \"N\": 0.5, \"F\": 0.4}\n```", "T": 0.6, "I": 0.4, "N": 0.5, "F": 0.4, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:666:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Contradiction (Ethical)", "statement": "Lying to save an innocent life is morally right and wrong at the same time.", "gloss": "G3", "rep": 5, "response": "```json\n{\"T\": 0.7, \"I\": 0.6, \"N\": 0.5, \"F\": 0.3}\n```", "T": 0.7, "I": 0.6, "N": 0.5, "F": 0.3, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:667:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Contradiction (Ethical)", "statement": "Lying to save an innocent life is morally right and wrong at the same time.", "gloss": "G3", "rep": 6, "response": "```json\n{\"T\": 0.7, \"I\": 0.8, \"N\": 0.6, \"F\": 0.5}\n```", "T": 0.7, "I": 0.8, "N": 0.6, "F": 0.5, "regime": "strong", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:668:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Contradiction (Ethical)", "statement": "Lying to save an innocent life is morally right and wrong at the same time.", "gloss": "G3", "rep": 7, "response": "```json\n{\"T\": 0.7, \"I\": 0.6, \"N\": 0.5, \"F\": 0.4}\n```", "T": 0.7, "I": 0.6, "N": 0.5, "F": 0.4, "regime": "strong", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:669:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Contradiction (Ethical)", "statement": "Lying to save an innocent life is morally right and wrong at the same time.", "gloss": "G3", "rep": 8, "response": "```json\n{\"T\": 0.7, \"I\": 0.5, \"N\": 0.4, \"F\": 0.6}\n```", "T": 0.7, "I": 0.5, "N": 0.4, "F": 0.6, "regime": "strong", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:670:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Contradiction (Ethical)", "statement": "Lying to save an innocent life is morally right and wrong at the same time.", "gloss": "G3", "rep": 9, "response": "```json\n{\"T\": 0.6, \"I\": 0.7, \"N\": 0.5, \"F\": 0.4}\n```", "T": 0.6, "I": 0.7, "N": 0.5, "F": 0.4, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:671:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Contradiction (Ethical)", "statement": "Lying to save an innocent life is morally right and wrong at the same time.", "gloss": "G3", "rep": 0, "response": "{\"T\": 0.7, \"I\": 0.6, \"N\": 0.8, \"F\": 0.3}", "T": 0.7, "I": 0.6, "N": 0.8, "F": 0.3, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:672:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Contradiction (Ethical)", "statement": "Lying to save an innocent life is morally right and wrong at the same time.", "gloss": "G3", "rep": 1, "response": "{\"T\": 0.7, \"I\": 0.8, \"N\": 0.9, \"F\": 0.3}", "T": 0.7, "I": 0.8, "N": 0.9, "F": 0.3, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:673:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Contradiction (Ethical)", "statement": "Lying to save an innocent life is morally right and wrong at the same time.", "gloss": "G3", "rep": 2, "response": "{\"T\": 0.7, \"I\": 0.6, \"N\": 0.8, \"F\": 0.3}", "T": 0.7, "I": 0.6, "N": 0.8, "F": 0.3, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:674:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Contradiction (Ethical)", "statement": "Lying to save an innocent life is morally right and wrong at the same time.", "gloss": "G3", "rep": 3, "response": "{\"T\": 0.7, \"I\": 0.3, \"N\": 0.8, \"F\": 0.4}", "T": 0.7, "I": 0.3, "N": 0.8, "F": 0.4, "regime": "strong", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:675:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Contradiction (Ethical)", "statement": "Lying to save an innocent life is morally right and wrong at the same time.", "gloss": "G3", "rep": 4, "response": "{\"T\": 0.7, \"I\": 0.6, \"N\": 0.8, \"F\": 0.3}", "T": 0.7, "I": 0.6, "N": 0.8, "F": 0.3, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:676:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Contradiction (Ethical)", "statement": "Lying to save an innocent life is morally right and wrong at the same time.", "gloss": "G3", "rep": 5, "response": "{\"T\": 0.7, \"I\": 0.4, \"N\": 0.8, \"F\": 0.3}", "T": 0.7, "I": 0.4, "N": 0.8, "F": 0.3, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:677:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Contradiction (Ethical)", "statement": "Lying to save an innocent life is morally right and wrong at the same time.", "gloss": "G3", "rep": 6, "response": "{\"T\": 0.7, \"I\": 0.6, \"N\": 0.8, \"F\": 0.3}", "T": 0.7, "I": 0.6, "N": 0.8, "F": 0.3, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:678:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Contradiction (Ethical)", "statement": "Lying to save an innocent life is morally right and wrong at the same time.", "gloss": "G3", "rep": 7, "response": "{\"T\": 0.7, \"I\": 0.6, \"N\": 0.8, \"F\": 0.3}", "T": 0.7, "I": 0.6, "N": 0.8, "F": 0.3, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:679:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Contradiction (Ethical)", "statement": "Lying to save an innocent life is morally right and wrong at the same time.", "gloss": "G3", "rep": 8, "response": "{\"T\": 0.7, \"I\": 0.6, \"N\": 0.8, \"F\": 0.3}", "T": 0.7, "I": 0.6, "N": 0.8, "F": 0.3, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:680:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Contradiction (Ethical)", "statement": "Lying to save an innocent life is morally right and wrong at the same time.", "gloss": "G3", "rep": 9, "response": "{\"T\": 0.7, \"I\": 0.6, \"N\": 0.8, \"F\": 0.3}", "T": 0.7, "I": 0.6, "N": 0.8, "F": 0.3, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:681:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Contradiction (Ethical)", "statement": "Lying to save an innocent life is morally right and wrong at the same time.", "gloss": "G3", "rep": 0, "response": "{\"T\": 0.6, \"I\": 0.4, \"N\": 0.7, \"F\": 0.3}", "T": 0.6, "I": 0.4, "N": 0.7, "F": 0.3, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:682:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Contradiction (Ethical)", "statement": "Lying to save an innocent life is morally right and wrong at the same time.", "gloss": "G3", "rep": 1, "response": "{\"T\": 0.7, \"I\": 0.4, \"N\": 0.6, \"F\": 0.3}", "T": 0.7, "I": 0.4, "N": 0.6, "F": 0.3, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:683:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Contradiction (Ethical)", "statement": "Lying to save an innocent life is morally right and wrong at the same time.", "gloss": "G3", "rep": 2, "response": "{\"T\": 0.7, \"I\": 0.4, \"N\": 0.6, \"F\": 0.3}", "T": 0.7, "I": 0.4, "N": 0.6, "F": 0.3, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:684:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Contradiction (Ethical)", "statement": "Lying to save an innocent life is morally right and wrong at the same time.", "gloss": "G3", "rep": 3, "response": "{\"T\": 0.6, \"I\": 0.3, \"N\": 0.7, \"F\": 0.4}", "T": 0.6, "I": 0.3, "N": 0.7, "F": 0.4, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:685:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Contradiction (Ethical)", "statement": "Lying to save an innocent life is morally right and wrong at the same time.", "gloss": "G3", "rep": 4, "response": "{\"T\": 0.7, \"I\": 0.4, \"N\": 0.6, \"F\": 0.3}", "T": 0.7, "I": 0.4, "N": 0.6, "F": 0.3, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:686:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Contradiction (Ethical)", "statement": "Lying to save an innocent life is morally right and wrong at the same time.", "gloss": "G3", "rep": 5, "response": "{\"T\": 0.6, \"I\": 0.3, \"N\": 0.7, \"F\": 0.4}", "T": 0.6, "I": 0.3, "N": 0.7, "F": 0.4, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:687:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Contradiction (Ethical)", "statement": "Lying to save an innocent life is morally right and wrong at the same time.", "gloss": "G3", "rep": 6, "response": "{\"T\": 0.7, \"I\": 0.4, \"N\": 0.6, \"F\": 0.3}", "T": 0.7, "I": 0.4, "N": 0.6, "F": 0.3, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:688:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Contradiction (Ethical)", "statement": "Lying to save an innocent life is morally right and wrong at the same time.", "gloss": "G3", "rep": 7, "response": "{\"T\": 0.7, \"I\": 0.4, \"N\": 0.6, \"F\": 0.3}", "T": 0.7, "I": 0.4, "N": 0.6, "F": 0.3, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:689:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Contradiction (Ethical)", "statement": "Lying to save an innocent life is morally right and wrong at the same time.", "gloss": "G3", "rep": 8, "response": "{\"T\": 0.7, \"I\": 0.4, \"N\": 0.6, \"F\": 0.3}", "T": 0.7, "I": 0.4, "N": 0.6, "F": 0.3, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:690:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Contradiction (Ethical)", "statement": "Lying to save an innocent life is morally right and wrong at the same time.", "gloss": "G3", "rep": 9, "response": "{\"T\": 0.6, \"I\": 0.3, \"N\": 0.7, \"F\": 0.4}", "T": 0.6, "I": 0.3, "N": 0.7, "F": 0.4, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:691:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Contradiction (Ethical)", "statement": "Lying to save an innocent life is morally right and wrong at the same time.", "gloss": "G3", "rep": 0, "response": "```json\n{\"T\": 0.7, \"I\": 0.5, \"N\": 0.6, \"F\": 0.3}\n```", "T": 0.7, "I": 0.5, "N": 0.6, "F": 0.3, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:692:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Contradiction (Ethical)", "statement": "Lying to save an innocent life is morally right and wrong at the same time.", "gloss": "G3", "rep": 1, "response": "```json\n{\"T\": 0.7, \"I\": 0.5, \"N\": 0.6, \"F\": 0.3}\n```", "T": 0.7, "I": 0.5, "N": 0.6, "F": 0.3, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:693:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Contradiction (Ethical)", "statement": "Lying to save an innocent life is morally right and wrong at the same time.", "gloss": "G3", "rep": 2, "response": "```json\n{\"T\": 0.6, \"I\": 0.3, \"N\": 0.5, \"F\": 0.4}\n```", "T": 0.6, "I": 0.3, "N": 0.5, "F": 0.4, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:694:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Contradiction (Ethical)", "statement": "Lying to save an innocent life is morally right and wrong at the same time.", "gloss": "G3", "rep": 3, "response": "```json\n{\"T\": 0.7, \"I\": 0.3, \"N\": 0.5, \"F\": 0.6}\n```", "T": 0.7, "I": 0.3, "N": 0.5, "F": 0.6, "regime": "strong", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:695:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Contradiction (Ethical)", "statement": "Lying to save an innocent life is morally right and wrong at the same time.", "gloss": "G3", "rep": 4, "response": "```json\n{\"T\": 0.7, \"I\": 0.4, \"N\": 0.6, \"F\": 0.5}\n```", "T": 0.7, "I": 0.4, "N": 0.6, "F": 0.5, "regime": "strong", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:696:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Contradiction (Ethical)", "statement": "Lying to save an innocent life is morally right and wrong at the same time.", "gloss": "G3", "rep": 5, "response": "```json\n{\"T\": 0.7, \"I\": 0.4, \"N\": 0.5, \"F\": 0.3}\n```", "T": 0.7, "I": 0.4, "N": 0.5, "F": 0.3, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:697:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Contradiction (Ethical)", "statement": "Lying to save an innocent life is morally right and wrong at the same time.", "gloss": "G3", "rep": 6, "response": "```json\n{\"T\": 0.7, \"I\": 0.5, \"N\": 0.6, \"F\": 0.3}\n```", "T": 0.7, "I": 0.5, "N": 0.6, "F": 0.3, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:698:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Contradiction (Ethical)", "statement": "Lying to save an innocent life is morally right and wrong at the same time.", "gloss": "G3", "rep": 7, "response": "```json\n{\"T\": 0.7, \"I\": 0.4, \"N\": 0.5, \"F\": 0.6}\n```", "T": 0.7, "I": 0.4, "N": 0.5, "F": 0.6, "regime": "strong", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:699:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Contradiction (Ethical)", "statement": "Lying to save an innocent life is morally right and wrong at the same time.", "gloss": "G3", "rep": 8, "response": "```json\n{\"T\": 0.7, \"I\": 0.5, \"N\": 0.6, \"F\": 0.3}\n```", "T": 0.7, "I": 0.5, "N": 0.6, "F": 0.3, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:700:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Contradiction (Ethical)", "statement": "Lying to save an innocent life is morally right and wrong at the same time.", "gloss": "G3", "rep": 9, "response": "```json\n{\"T\": 0.7, \"I\": 0.5, \"N\": 0.6, \"F\": 0.3}\n```", "T": 0.7, "I": 0.5, "N": 0.6, "F": 0.3, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:701:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Contradiction (Ethical)", "statement": "Lying to save an innocent life is morally right and wrong at the same time.", "gloss": "G3", "rep": 0, "response": "{\"T\": 0.7, \"I\": 0.3, \"N\": 0.5, \"F\": 0.4}", "T": 0.7, "I": 0.3, "N": 0.5, "F": 0.4, "regime": "strong", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:702:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Contradiction (Ethical)", "statement": "Lying to save an innocent life is morally right and wrong at the same time.", "gloss": "G3", "rep": 1, "response": "{\"T\": 0.6, \"I\": 0.3, \"N\": 0.5, \"F\": 0.4}", "T": 0.6, "I": 0.3, "N": 0.5, "F": 0.4, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:703:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Contradiction (Ethical)", "statement": "Lying to save an innocent life is morally right and wrong at the same time.", "gloss": "G3", "rep": 2, "response": "{\"T\": 0.7, \"I\": 0.2, \"N\": 0.6, \"F\": 0.3}", "T": 0.7, "I": 0.2, "N": 0.6, "F": 0.3, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:704:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Contradiction (Ethical)", "statement": "Lying to save an innocent life is morally right and wrong at the same time.", "gloss": "G3", "rep": 3, "response": "{\"T\": 0.7, \"I\": 0.5, \"N\": 0.6, \"F\": 0.3}", "T": 0.7, "I": 0.5, "N": 0.6, "F": 0.3, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:705:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Contradiction (Ethical)", "statement": "Lying to save an innocent life is morally right and wrong at the same time.", "gloss": "G3", "rep": 4, "response": "{\"T\": 0.6, \"I\": 0.3, \"N\": 0.5, \"F\": 0.4}", "T": 0.6, "I": 0.3, "N": 0.5, "F": 0.4, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:706:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Contradiction (Ethical)", "statement": "Lying to save an innocent life is morally right and wrong at the same time.", "gloss": "G3", "rep": 5, "response": "{\"T\": 0.7, \"I\": 0.4, \"N\": 0.6, \"F\": 0.3}", "T": 0.7, "I": 0.4, "N": 0.6, "F": 0.3, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:707:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Contradiction (Ethical)", "statement": "Lying to save an innocent life is morally right and wrong at the same time.", "gloss": "G3", "rep": 6, "response": "{\"T\": 0.7, \"I\": 0.2, \"N\": 0.5, \"F\": 0.3}", "T": 0.7, "I": 0.2, "N": 0.5, "F": 0.3, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:708:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Contradiction (Ethical)", "statement": "Lying to save an innocent life is morally right and wrong at the same time.", "gloss": "G3", "rep": 7, "response": "{\"T\": 0.7, \"I\": 0.2, \"N\": 0.6, \"F\": 0.3}", "T": 0.7, "I": 0.2, "N": 0.6, "F": 0.3, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:709:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Contradiction (Ethical)", "statement": "Lying to save an innocent life is morally right and wrong at the same time.", "gloss": "G3", "rep": 8, "response": "{\"T\": 0.7, \"I\": 0.5, \"N\": 0.6, \"F\": 0.3}", "T": 0.7, "I": 0.5, "N": 0.6, "F": 0.3, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:710:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Contradiction (Ethical)", "statement": "Lying to save an innocent life is morally right and wrong at the same time.", "gloss": "G3", "rep": 9, "response": "{\"T\": 0.7, \"I\": 0.5, \"N\": 0.6, \"F\": 0.4}", "T": 0.7, "I": 0.5, "N": 0.6, "F": 0.4, "regime": "strong", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:711:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Contradiction (Ethical)", "statement": "Lying to save an innocent life is morally right and wrong at the same time.", "gloss": "G3", "rep": 0, "response": "```json\n{\n  \"T\": 0.75,\n  \"I\": 0.55,\n  \"N\": 0.85,\n  \"F\": 0.30\n}\n```", "T": 0.75, "I": 0.55, "N": 0.85, "F": 0.3, "regime": "strong", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:712:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Contradiction (Ethical)", "statement": "Lying to save an innocent life is morally right and wrong at the same time.", "gloss": "G3", "rep": 1, "response": "```json\n{\n  \"T\": 0.75,\n  \"I\": 0.30,\n  \"N\": 0.85,\n  \"F\": 0.20\n}\n```", "T": 0.75, "I": 0.3, "N": 0.85, "F": 0.2, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:713:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Contradiction (Ethical)", "statement": "Lying to save an innocent life is morally right and wrong at the same time.", "gloss": "G3", "rep": 2, "response": "```json\n{\n  \"T\": 0.75,\n  \"I\": 0.30,\n  \"N\": 0.85,\n  \"F\": 0.20\n}\n```", "T": 0.75, "I": 0.3, "N": 0.85, "F": 0.2, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:714:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Contradiction (Ethical)", "statement": "Lying to save an innocent life is morally right and wrong at the same time.", "gloss": "G3", "rep": 3, "response": "```json\n{\n  \"T\": 0.75,\n  \"I\": 0.30,\n  \"N\": 0.85,\n  \"F\": 0.20\n}\n```", "T": 0.75, "I": 0.3, "N": 0.85, "F": 0.2, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:715:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Contradiction (Ethical)", "statement": "Lying to save an innocent life is morally right and wrong at the same time.", "gloss": "G3", "rep": 4, "response": "```json\n{\n  \"T\": 0.75,\n  \"I\": 0.30,\n  \"N\": 0.85,\n  \"F\": 0.20\n}\n```", "T": 0.75, "I": 0.3, "N": 0.85, "F": 0.2, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:716:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Contradiction (Ethical)", "statement": "Lying to save an innocent life is morally right and wrong at the same time.", "gloss": "G3", "rep": 5, "response": "```json\n{\n  \"T\": 0.75,\n  \"I\": 0.30,\n  \"N\": 0.85,\n  \"F\": 0.10\n}\n```", "T": 0.75, "I": 0.3, "N": 0.85, "F": 0.1, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:717:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Contradiction (Ethical)", "statement": "Lying to save an innocent life is morally right and wrong at the same time.", "gloss": "G3", "rep": 6, "response": "```json\n{\n  \"T\": 0.75,\n  \"I\": 0.55,\n  \"N\": 0.85,\n  \"F\": 0.40\n}\n```", "T": 0.75, "I": 0.55, "N": 0.85, "F": 0.4, "regime": "strong", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:718:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Contradiction (Ethical)", "statement": "Lying to save an innocent life is morally right and wrong at the same time.", "gloss": "G3", "rep": 7, "response": "```json\n{\n  \"T\": 0.75,\n  \"I\": 0.45,\n  \"N\": 0.85,\n  \"F\": 0.30\n}\n```", "T": 0.75, "I": 0.45, "N": 0.85, "F": 0.3, "regime": "strong", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:719:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Contradiction (Ethical)", "statement": "Lying to save an innocent life is morally right and wrong at the same time.", "gloss": "G3", "rep": 8, "response": "```json\n{\n  \"T\": 0.65,\n  \"I\": 0.35,\n  \"N\": 0.85,\n  \"F\": 0.20\n}\n```", "T": 0.65, "I": 0.35, "N": 0.85, "F": 0.2, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:720:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Contradiction (Ethical)", "statement": "Lying to save an innocent life is morally right and wrong at the same time.", "gloss": "G3", "rep": 9, "response": "```json\n{\n  \"T\": 0.65,\n  \"I\": 0.45,\n  \"N\": 0.80,\n  \"F\": 0.30\n}\n```", "T": 0.65, "I": 0.45, "N": 0.8, "F": 0.3, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:721:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Contingency (Future)", "statement": "It will rain in New York tomorrow.", "gloss": "G1", "rep": 0, "response": "```json\n{\"T\": 0.6, \"I\": 0.3, \"N\": 0.1, \"F\": 0.4}\n```", "T": 0.6, "I": 0.3, "N": 0.1, "F": 0.4, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:722:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Contingency (Future)", "statement": "It will rain in New York tomorrow.", "gloss": "G1", "rep": 1, "response": "```json\n{\"T\": 0.5, \"I\": 0.4, \"N\": 0.2, \"F\": 0.5}\n```", "T": 0.5, "I": 0.4, "N": 0.2, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:723:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Contingency (Future)", "statement": "It will rain in New York tomorrow.", "gloss": "G1", "rep": 2, "response": "```json\n{\"T\": 0.5, \"I\": 0.3, \"N\": 0.4, \"F\": 0.5}\n```", "T": 0.5, "I": 0.3, "N": 0.4, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:724:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Contingency (Future)", "statement": "It will rain in New York tomorrow.", "gloss": "G1", "rep": 3, "response": "```json\n{\"T\": 0.5, \"I\": 0.6, \"N\": 0.4, \"F\": 0.5}\n```", "T": 0.5, "I": 0.6, "N": 0.4, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:725:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Contingency (Future)", "statement": "It will rain in New York tomorrow.", "gloss": "G1", "rep": 4, "response": "```json\n{\"T\": 0.5, \"I\": 0.6, \"N\": 0.4, \"F\": 0.5}\n```", "T": 0.5, "I": 0.6, "N": 0.4, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:726:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Contingency (Future)", "statement": "It will rain in New York tomorrow.", "gloss": "G1", "rep": 5, "response": "```json\n{\"T\": 0.4, \"I\": 0.5, \"N\": 0.3, \"F\": 0.4}\n```", "T": 0.4, "I": 0.5, "N": 0.3, "F": 0.4, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:727:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Contingency (Future)", "statement": "It will rain in New York tomorrow.", "gloss": "G1", "rep": 6, "response": "```json\n{\"T\": 0.6, \"I\": 0.4, \"N\": 0.2, \"F\": 0.3}\n```", "T": 0.6, "I": 0.4, "N": 0.2, "F": 0.3, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:728:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Contingency (Future)", "statement": "It will rain in New York tomorrow.", "gloss": "G1", "rep": 7, "response": "```json\n{\"T\": 0.4, \"I\": 0.5, \"N\": 0.2, \"F\": 0.3}\n```", "T": 0.4, "I": 0.5, "N": 0.2, "F": 0.3, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:729:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Contingency (Future)", "statement": "It will rain in New York tomorrow.", "gloss": "G1", "rep": 8, "response": "```json\n{\"T\": 0.6, \"I\": 0.3, \"N\": 0.2, \"F\": 0.4}\n```", "T": 0.6, "I": 0.3, "N": 0.2, "F": 0.4, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:730:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Contingency (Future)", "statement": "It will rain in New York tomorrow.", "gloss": "G1", "rep": 9, "response": "```json\n{\"T\": 0.6, \"I\": 0.3, \"N\": 0.2, \"F\": 0.4}\n```", "T": 0.6, "I": 0.3, "N": 0.2, "F": 0.4, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:731:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Contingency (Future)", "statement": "It will rain in New York tomorrow.", "gloss": "G1", "rep": 0, "response": "{\"T\": 0.3, \"I\": 0.8, \"N\": 0.7, \"F\": 0.3}", "T": 0.3, "I": 0.8, "N": 0.7, "F": 0.3, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:732:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Contingency (Future)", "statement": "It will rain in New York tomorrow.", "gloss": "G1", "rep": 1, "response": "{\"T\": 0.3, \"I\": 0.8, \"N\": 0.7, \"F\": 0.3}", "T": 0.3, "I": 0.8, "N": 0.7, "F": 0.3, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:733:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Contingency (Future)", "statement": "It will rain in New York tomorrow.", "gloss": "G1", "rep": 2, "response": "{\"T\": 0.3, \"I\": 0.8, \"N\": 0.7, \"F\": 0.3}", "T": 0.3, "I": 0.8, "N": 0.7, "F": 0.3, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:734:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Contingency (Future)", "statement": "It will rain in New York tomorrow.", "gloss": "G1", "rep": 3, "response": "{\"T\": 0.3, \"I\": 0.8, \"N\": 0.5, \"F\": 0.3}", "T": 0.3, "I": 0.8, "N": 0.5, "F": 0.3, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:735:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Contingency (Future)", "statement": "It will rain in New York tomorrow.", "gloss": "G1", "rep": 4, "response": "{\"T\": 0.3, \"I\": 0.8, \"N\": 0.7, \"F\": 0.4}", "T": 0.3, "I": 0.8, "N": 0.7, "F": 0.4, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:736:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Contingency (Future)", "statement": "It will rain in New York tomorrow.", "gloss": "G1", "rep": 5, "response": "{\"T\": 0.3, \"I\": 0.8, \"N\": 0.7, \"F\": 0.3}", "T": 0.3, "I": 0.8, "N": 0.7, "F": 0.3, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:737:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Contingency (Future)", "statement": "It will rain in New York tomorrow.", "gloss": "G1", "rep": 6, "response": "{\"T\": 0.3, \"I\": 0.8, \"N\": 0.5, \"F\": 0.3}", "T": 0.3, "I": 0.8, "N": 0.5, "F": 0.3, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:738:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Contingency (Future)", "statement": "It will rain in New York tomorrow.", "gloss": "G1", "rep": 7, "response": "{\"T\": 0.3, \"I\": 0.8, \"N\": 0.7, \"F\": 0.3}", "T": 0.3, "I": 0.8, "N": 0.7, "F": 0.3, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:739:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Contingency (Future)", "statement": "It will rain in New York tomorrow.", "gloss": "G1", "rep": 8, "response": "{\"T\": 0.3, \"I\": 0.8, \"N\": 0.7, \"F\": 0.3}", "T": 0.3, "I": 0.8, "N": 0.7, "F": 0.3, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:740:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Contingency (Future)", "statement": "It will rain in New York tomorrow.", "gloss": "G1", "rep": 9, "response": "{\"T\": 0.3, \"I\": 0.8, \"N\": 0.7, \"F\": 0.3}", "T": 0.3, "I": 0.8, "N": 0.7, "F": 0.3, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:741:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Contingency (Future)", "statement": "It will rain in New York tomorrow.", "gloss": "G1", "rep": 0, "response": "{\"T\": 0.4, \"I\": 0.7, \"N\": 0.2, \"F\": 0.3}", "T": 0.4, "I": 0.7, "N": 0.2, "F": 0.3, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:742:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Contingency (Future)", "statement": "It will rain in New York tomorrow.", "gloss": "G1", "rep": 1, "response": "{\"T\": 0.4, \"I\": 0.7, \"N\": 0.2, \"F\": 0.3}", "T": 0.4, "I": 0.7, "N": 0.2, "F": 0.3, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:743:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Contingency (Future)", "statement": "It will rain in New York tomorrow.", "gloss": "G1", "rep": 2, "response": "{\"T\": 0.4, \"I\": 0.7, \"N\": 0.2, \"F\": 0.3}", "T": 0.4, "I": 0.7, "N": 0.2, "F": 0.3, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:744:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Contingency (Future)", "statement": "It will rain in New York tomorrow.", "gloss": "G1", "rep": 3, "response": "{\"T\": 0.4, \"I\": 0.6, \"N\": 0.2, \"F\": 0.3}", "T": 0.4, "I": 0.6, "N": 0.2, "F": 0.3, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:745:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Contingency (Future)", "statement": "It will rain in New York tomorrow.", "gloss": "G1", "rep": 4, "response": "{\"T\": 0.4, \"I\": 0.7, \"N\": 0.2, \"F\": 0.3}", "T": 0.4, "I": 0.7, "N": 0.2, "F": 0.3, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:746:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Contingency (Future)", "statement": "It will rain in New York tomorrow.", "gloss": "G1", "rep": 5, "response": "{\"T\": 0.4, \"I\": 0.6, \"N\": 0.2, \"F\": 0.3}", "T": 0.4, "I": 0.6, "N": 0.2, "F": 0.3, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:747:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Contingency (Future)", "statement": "It will rain in New York tomorrow.", "gloss": "G1", "rep": 6, "response": "{\"T\": 0.4, \"I\": 0.6, \"N\": 0.2, \"F\": 0.3}", "T": 0.4, "I": 0.6, "N": 0.2, "F": 0.3, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:748:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Contingency (Future)", "statement": "It will rain in New York tomorrow.", "gloss": "G1", "rep": 7, "response": "{\"T\": 0.4, \"I\": 0.7, \"N\": 0.2, \"F\": 0.3}", "T": 0.4, "I": 0.7, "N": 0.2, "F": 0.3, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:749:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Contingency (Future)", "statement": "It will rain in New York tomorrow.", "gloss": "G1", "rep": 8, "response": "{\"T\": 0.4, \"I\": 0.7, \"N\": 0.2, \"F\": 0.3}", "T": 0.4, "I": 0.7, "N": 0.2, "F": 0.3, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:750:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Contingency (Future)", "statement": "It will rain in New York tomorrow.", "gloss": "G1", "rep": 9, "response": "{\"T\": 0.4, \"I\": 0.7, \"N\": 0.2, \"F\": 0.3}", "T": 0.4, "I": 0.7, "N": 0.2, "F": 0.3, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:751:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Contingency (Future)", "statement": "It will rain in New York tomorrow.", "gloss": "G1", "rep": 0, "response": "```json\n{\"T\": 0.4, \"I\": 0.6, \"N\": 0.2, \"F\": 0.4}\n```", "T": 0.4, "I": 0.6, "N": 0.2, "F": 0.4, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:752:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Contingency (Future)", "statement": "It will rain in New York tomorrow.", "gloss": "G1", "rep": 1, "response": "```json\n{\"T\": 0.5, \"I\": 0.7, \"N\": 0.2, \"F\": 0.4}\n```", "T": 0.5, "I": 0.7, "N": 0.2, "F": 0.4, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:753:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Contingency (Future)", "statement": "It will rain in New York tomorrow.", "gloss": "G1", "rep": 2, "response": "```json\n{\"T\": 0.5, \"I\": 0.4, \"N\": 0.1, \"F\": 0.5}\n```", "T": 0.5, "I": 0.4, "N": 0.1, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:754:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Contingency (Future)", "statement": "It will rain in New York tomorrow.", "gloss": "G1", "rep": 3, "response": "```json\n{\"T\": 0.5, \"I\": 0.7, \"N\": 0.2, \"F\": 0.4}\n```", "T": 0.5, "I": 0.7, "N": 0.2, "F": 0.4, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:755:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Contingency (Future)", "statement": "It will rain in New York tomorrow.", "gloss": "G1", "rep": 4, "response": "```json\n{\"T\": 0.5, \"I\": 0.3, \"N\": 0.2, \"F\": 0.4}\n```", "T": 0.5, "I": 0.3, "N": 0.2, "F": 0.4, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:756:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Contingency (Future)", "statement": "It will rain in New York tomorrow.", "gloss": "G1", "rep": 5, "response": "```json\n{\"T\": 0.5, \"I\": 0.6, \"N\": 0.3, \"F\": 0.4}\n```", "T": 0.5, "I": 0.6, "N": 0.3, "F": 0.4, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:757:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Contingency (Future)", "statement": "It will rain in New York tomorrow.", "gloss": "G1", "rep": 6, "response": "```json\n{\"T\": 0.5, \"I\": 0.6, \"N\": 0.3, \"F\": 0.5}\n```", "T": 0.5, "I": 0.6, "N": 0.3, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:758:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Contingency (Future)", "statement": "It will rain in New York tomorrow.", "gloss": "G1", "rep": 7, "response": "```json\n{\"T\": 0.4, \"I\": 0.5, \"N\": 0.2, \"F\": 0.4}\n```", "T": 0.4, "I": 0.5, "N": 0.2, "F": 0.4, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:759:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Contingency (Future)", "statement": "It will rain in New York tomorrow.", "gloss": "G1", "rep": 8, "response": "```json\n{\"T\": 0.4, \"I\": 0.6, \"N\": 0.3, \"F\": 0.5}\n```", "T": 0.4, "I": 0.6, "N": 0.3, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:760:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Contingency (Future)", "statement": "It will rain in New York tomorrow.", "gloss": "G1", "rep": 9, "response": "```json\n{\"T\": 0.4, \"I\": 0.6, \"N\": 0.2, \"F\": 0.3}\n```", "T": 0.4, "I": 0.6, "N": 0.2, "F": 0.3, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:761:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Contingency (Future)", "statement": "It will rain in New York tomorrow.", "gloss": "G1", "rep": 0, "response": "{\"T\": 0.4, \"I\": 0.5, \"N\": 0.1, \"F\": 0.3}", "T": 0.4, "I": 0.5, "N": 0.1, "F": 0.3, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:762:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Contingency (Future)", "statement": "It will rain in New York tomorrow.", "gloss": "G1", "rep": 1, "response": "{\"T\": 0.4, \"I\": 0.5, \"N\": 0.1, \"F\": 0.3}", "T": 0.4, "I": 0.5, "N": 0.1, "F": 0.3, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:763:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Contingency (Future)", "statement": "It will rain in New York tomorrow.", "gloss": "G1", "rep": 2, "response": "{\"T\": 0.4, \"I\": 0.5, \"N\": 0.1, \"F\": 0.3}", "T": 0.4, "I": 0.5, "N": 0.1, "F": 0.3, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:764:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Contingency (Future)", "statement": "It will rain in New York tomorrow.", "gloss": "G1", "rep": 3, "response": "{\"T\": 0.4, \"I\": 0.5, \"N\": 0.1, \"F\": 0.3}", "T": 0.4, "I": 0.5, "N": 0.1, "F": 0.3, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:765:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Contingency (Future)", "statement": "It will rain in New York tomorrow.", "gloss": "G1", "rep": 4, "response": "{\"T\": 0.4, \"I\": 0.5, \"N\": 0.2, \"F\": 0.3}", "T": 0.4, "I": 0.5, "N": 0.2, "F": 0.3, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:766:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Contingency (Future)", "statement": "It will rain in New York tomorrow.", "gloss": "G1", "rep": 5, "response": "{\"T\": 0.4, \"I\": 0.5, \"N\": 0.1, \"F\": 0.3}", "T": 0.4, "I": 0.5, "N": 0.1, "F": 0.3, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:767:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Contingency (Future)", "statement": "It will rain in New York tomorrow.", "gloss": "G1", "rep": 6, "response": "{\"T\": 0.4, \"I\": 0.5, \"N\": 0.1, \"F\": 0.3}", "T": 0.4, "I": 0.5, "N": 0.1, "F": 0.3, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:768:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Contingency (Future)", "statement": "It will rain in New York tomorrow.", "gloss": "G1", "rep": 7, "response": "{\"T\": 0.4, \"I\": 0.5, \"N\": 0.2, \"F\": 0.3}", "T": 0.4, "I": 0.5, "N": 0.2, "F": 0.3, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:769:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Contingency (Future)", "statement": "It will rain in New York tomorrow.", "gloss": "G1", "rep": 8, "response": "{\"T\": 0.4, \"I\": 0.5, \"N\": 0.1, \"F\": 0.3}", "T": 0.4, "I": 0.5, "N": 0.1, "F": 0.3, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:770:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Contingency (Future)", "statement": "It will rain in New York tomorrow.", "gloss": "G1", "rep": 9, "response": "{\"T\": 0.4, \"I\": 0.7, \"N\": 0.1, \"F\": 0.3}", "T": 0.4, "I": 0.7, "N": 0.1, "F": 0.3, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:771:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Contingency (Future)", "statement": "It will rain in New York tomorrow.", "gloss": "G1", "rep": 0, "response": "```json\n{\n  \"T\": 0.25,\n  \"I\": 0.85,\n  \"N\": 0.50,\n  \"F\": 0.10\n}\n```", "T": 0.25, "I": 0.85, "N": 0.5, "F": 0.1, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:772:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Contingency (Future)", "statement": "It will rain in New York tomorrow.", "gloss": "G1", "rep": 1, "response": "```json\n{\n  \"T\": 0.35,\n  \"I\": 0.75,\n  \"N\": 0.40,\n  \"F\": 0.10\n}\n```", "T": 0.35, "I": 0.75, "N": 0.4, "F": 0.1, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:773:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Contingency (Future)", "statement": "It will rain in New York tomorrow.", "gloss": "G1", "rep": 2, "response": "```json\n{\n  \"T\": 0.25,\n  \"I\": 0.70,\n  \"N\": 0.50,\n  \"F\": 0.10\n}\n```", "T": 0.25, "I": 0.7, "N": 0.5, "F": 0.1, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:774:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Contingency (Future)", "statement": "It will rain in New York tomorrow.", "gloss": "G1", "rep": 3, "response": "```json\n{\n  \"T\": 0.3,\n  \"I\": 0.75,\n  \"N\": 0.1,\n  \"F\": 0.05\n}\n```", "T": 0.3, "I": 0.75, "N": 0.1, "F": 0.05, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:775:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Contingency (Future)", "statement": "It will rain in New York tomorrow.", "gloss": "G1", "rep": 4, "response": "```json\n{\n  \"T\": 0.35,\n  \"I\": 0.70,\n  \"N\": 0.40,\n  \"F\": 0.05\n}\n```", "T": 0.35, "I": 0.7, "N": 0.4, "F": 0.05, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:776:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Contingency (Future)", "statement": "It will rain in New York tomorrow.", "gloss": "G1", "rep": 5, "response": "```json\n{\n  \"T\": 0.3,\n  \"I\": 0.75,\n  \"N\": 0.1,\n  \"F\": 0.05\n}\n```", "T": 0.3, "I": 0.75, "N": 0.1, "F": 0.05, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:777:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Contingency (Future)", "statement": "It will rain in New York tomorrow.", "gloss": "G1", "rep": 6, "response": "```json\n{\n  \"T\": 0.15,\n  \"I\": 0.85,\n  \"N\": 0.30,\n  \"F\": 0.05\n}\n```", "T": 0.15, "I": 0.85, "N": 0.3, "F": 0.05, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:778:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Contingency (Future)", "statement": "It will rain in New York tomorrow.", "gloss": "G1", "rep": 7, "response": "```json\n{\n  \"T\": 0.35,\n  \"I\": 0.70,\n  \"N\": 0.40,\n  \"F\": 0.10\n}\n```", "T": 0.35, "I": 0.7, "N": 0.4, "F": 0.1, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:779:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Contingency (Future)", "statement": "It will rain in New York tomorrow.", "gloss": "G1", "rep": 8, "response": "```json\n{\n  \"T\": 0.25,\n  \"I\": 0.85,\n  \"N\": 0.30,\n  \"F\": 0.10\n}\n```", "T": 0.25, "I": 0.85, "N": 0.3, "F": 0.1, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:780:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Contingency (Future)", "statement": "It will rain in New York tomorrow.", "gloss": "G1", "rep": 9, "response": "```json\n{\n  \"T\": 0.25,\n  \"I\": 0.80,\n  \"N\": 0.40,\n  \"F\": 0.05\n}\n```", "T": 0.25, "I": 0.8, "N": 0.4, "F": 0.05, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:781:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Contingency (Future)", "statement": "It will rain in New York tomorrow.", "gloss": "G2", "rep": 0, "response": "```json\n{\"T\": 0.5, \"I\": 0.4, \"N\": 0.1, \"F\": 0.5}\n```", "T": 0.5, "I": 0.4, "N": 0.1, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:782:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Contingency (Future)", "statement": "It will rain in New York tomorrow.", "gloss": "G2", "rep": 1, "response": "```json\n{\"T\": 0.5, \"I\": 0.4, \"N\": 0.0, \"F\": 0.5}\n```", "T": 0.5, "I": 0.4, "N": 0.0, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:783:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Contingency (Future)", "statement": "It will rain in New York tomorrow.", "gloss": "G2", "rep": 2, "response": "```json\n{\"T\": 0.6, \"I\": 0.3, \"N\": 0.0, \"F\": 0.4}\n```", "T": 0.6, "I": 0.3, "N": 0.0, "F": 0.4, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:784:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Contingency (Future)", "statement": "It will rain in New York tomorrow.", "gloss": "G2", "rep": 3, "response": "```json\n{\"T\": 0.6, \"I\": 0.3, \"N\": 0.0, \"F\": 0.4}\n```", "T": 0.6, "I": 0.3, "N": 0.0, "F": 0.4, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:785:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Contingency (Future)", "statement": "It will rain in New York tomorrow.", "gloss": "G2", "rep": 4, "response": "```json\n{\"T\": 0.5, \"I\": 0.3, \"N\": 0.0, \"F\": 0.5}\n```", "T": 0.5, "I": 0.3, "N": 0.0, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:786:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Contingency (Future)", "statement": "It will rain in New York tomorrow.", "gloss": "G2", "rep": 5, "response": "{\"T\": 0.6, \"I\": 0.3, \"N\": 0.0, \"F\": 0.4}", "T": 0.6, "I": 0.3, "N": 0.0, "F": 0.4, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:787:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Contingency (Future)", "statement": "It will rain in New York tomorrow.", "gloss": "G2", "rep": 6, "response": "```json\n{\"T\": 0.6, \"I\": 0.2, \"N\": 0.0, \"F\": 0.4}\n```", "T": 0.6, "I": 0.2, "N": 0.0, "F": 0.4, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:788:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Contingency (Future)", "statement": "It will rain in New York tomorrow.", "gloss": "G2", "rep": 7, "response": "```json\n{\"T\": 0.6, \"I\": 0.3, \"N\": 0.0, \"F\": 0.4}\n```", "T": 0.6, "I": 0.3, "N": 0.0, "F": 0.4, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:789:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Contingency (Future)", "statement": "It will rain in New York tomorrow.", "gloss": "G2", "rep": 8, "response": "```json\n{\"T\": 0.6, \"I\": 0.2, \"N\": 0.0, \"F\": 0.4}\n```", "T": 0.6, "I": 0.2, "N": 0.0, "F": 0.4, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:790:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Contingency (Future)", "statement": "It will rain in New York tomorrow.", "gloss": "G2", "rep": 9, "response": "```json\n{\"T\": 0.6, \"I\": 0.4, \"N\": 0.0, \"F\": 0.3}\n```", "T": 0.6, "I": 0.4, "N": 0.0, "F": 0.3, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:791:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Contingency (Future)", "statement": "It will rain in New York tomorrow.", "gloss": "G2", "rep": 0, "response": "{\"T\": 0.3, \"I\": 0.8, \"N\": 0.1, \"F\": 0.4}", "T": 0.3, "I": 0.8, "N": 0.1, "F": 0.4, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:792:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Contingency (Future)", "statement": "It will rain in New York tomorrow.", "gloss": "G2", "rep": 1, "response": "{\"T\": 0.3, \"I\": 0.8, \"N\": 0.1, \"F\": 0.3}", "T": 0.3, "I": 0.8, "N": 0.1, "F": 0.3, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:793:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Contingency (Future)", "statement": "It will rain in New York tomorrow.", "gloss": "G2", "rep": 2, "response": "{\"T\": 0.3, \"I\": 0.8, \"N\": 0.1, \"F\": 0.3}", "T": 0.3, "I": 0.8, "N": 0.1, "F": 0.3, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:794:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Contingency (Future)", "statement": "It will rain in New York tomorrow.", "gloss": "G2", "rep": 3, "response": "{\"T\": 0.3, \"I\": 0.8, \"N\": 0.1, \"F\": 0.3}", "T": 0.3, "I": 0.8, "N": 0.1, "F": 0.3, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:795:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Contingency (Future)", "statement": "It will rain in New York tomorrow.", "gloss": "G2", "rep": 4, "response": "{\"T\": 0.3, \"I\": 0.8, \"N\": 0.1, \"F\": 0.7}", "T": 0.3, "I": 0.8, "N": 0.1, "F": 0.7, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:796:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Contingency (Future)", "statement": "It will rain in New York tomorrow.", "gloss": "G2", "rep": 5, "response": "{\"T\": 0.3, \"I\": 0.8, \"N\": 0.1, \"F\": 0.3}", "T": 0.3, "I": 0.8, "N": 0.1, "F": 0.3, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:797:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Contingency (Future)", "statement": "It will rain in New York tomorrow.", "gloss": "G2", "rep": 6, "response": "{\"T\": 0.3, \"I\": 0.8, \"N\": 0.1, \"F\": 0.3}", "T": 0.3, "I": 0.8, "N": 0.1, "F": 0.3, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:798:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Contingency (Future)", "statement": "It will rain in New York tomorrow.", "gloss": "G2", "rep": 7, "response": "{\"T\": 0.3, \"I\": 0.8, \"N\": 0.1, \"F\": 0.3}", "T": 0.3, "I": 0.8, "N": 0.1, "F": 0.3, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:799:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Contingency (Future)", "statement": "It will rain in New York tomorrow.", "gloss": "G2", "rep": 8, "response": "{\"T\": 0.3, \"I\": 0.8, \"N\": 0.1, \"F\": 0.7}", "T": 0.3, "I": 0.8, "N": 0.1, "F": 0.7, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:800:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Contingency (Future)", "statement": "It will rain in New York tomorrow.", "gloss": "G2", "rep": 9, "response": "{\"T\": 0.3, \"I\": 0.8, \"N\": 0.1, \"F\": 0.3}", "T": 0.3, "I": 0.8, "N": 0.1, "F": 0.3, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:801:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Contingency (Future)", "statement": "It will rain in New York tomorrow.", "gloss": "G2", "rep": 0, "response": "{\"T\": 0.4, \"I\": 0.6, \"N\": 0.0, \"F\": 0.3}", "T": 0.4, "I": 0.6, "N": 0.0, "F": 0.3, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:802:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Contingency (Future)", "statement": "It will rain in New York tomorrow.", "gloss": "G2", "rep": 1, "response": "{\"T\": 0.4, \"I\": 0.6, \"N\": 0.0, \"F\": 0.2}", "T": 0.4, "I": 0.6, "N": 0.0, "F": 0.2, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:803:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Contingency (Future)", "statement": "It will rain in New York tomorrow.", "gloss": "G2", "rep": 2, "response": "{\"T\": 0.4, \"I\": 0.6, \"N\": 0.0, \"F\": 0.3}", "T": 0.4, "I": 0.6, "N": 0.0, "F": 0.3, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:804:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Contingency (Future)", "statement": "It will rain in New York tomorrow.", "gloss": "G2", "rep": 3, "response": "{\"T\": 0.4, \"I\": 0.6, \"N\": 0.0, \"F\": 0.2}", "T": 0.4, "I": 0.6, "N": 0.0, "F": 0.2, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:805:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Contingency (Future)", "statement": "It will rain in New York tomorrow.", "gloss": "G2", "rep": 4, "response": "{\"T\": 0.4, \"I\": 0.7, \"N\": 0.1, \"F\": 0.3}", "T": 0.4, "I": 0.7, "N": 0.1, "F": 0.3, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:806:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Contingency (Future)", "statement": "It will rain in New York tomorrow.", "gloss": "G2", "rep": 5, "response": "{\"T\": 0.4, \"I\": 0.6, \"N\": 0.0, \"F\": 0.3}", "T": 0.4, "I": 0.6, "N": 0.0, "F": 0.3, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:807:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Contingency (Future)", "statement": "It will rain in New York tomorrow.", "gloss": "G2", "rep": 6, "response": "{\"T\": 0.4, \"I\": 0.6, \"N\": 0.0, \"F\": 0.2}", "T": 0.4, "I": 0.6, "N": 0.0, "F": 0.2, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:808:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Contingency (Future)", "statement": "It will rain in New York tomorrow.", "gloss": "G2", "rep": 7, "response": "{\"T\": 0.4, \"I\": 0.6, \"N\": 0.0, \"F\": 0.2}", "T": 0.4, "I": 0.6, "N": 0.0, "F": 0.2, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:809:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Contingency (Future)", "statement": "It will rain in New York tomorrow.", "gloss": "G2", "rep": 8, "response": "{\"T\": 0.4, \"I\": 0.7, \"N\": 0.1, \"F\": 0.3}", "T": 0.4, "I": 0.7, "N": 0.1, "F": 0.3, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:810:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Contingency (Future)", "statement": "It will rain in New York tomorrow.", "gloss": "G2", "rep": 9, "response": "{\"T\": 0.4, \"I\": 0.6, \"N\": 0.0, \"F\": 0.3}", "T": 0.4, "I": 0.6, "N": 0.0, "F": 0.3, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:811:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Contingency (Future)", "statement": "It will rain in New York tomorrow.", "gloss": "G2", "rep": 0, "response": "```json\n{\"T\": 0.5, \"I\": 0.4, \"N\": 0.1, \"F\": 0.5}\n```", "T": 0.5, "I": 0.4, "N": 0.1, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:812:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Contingency (Future)", "statement": "It will rain in New York tomorrow.", "gloss": "G2", "rep": 1, "response": "```json\n{\"T\": 0.5, \"I\": 0.3, \"N\": 0.1, \"F\": 0.4}\n```", "T": 0.5, "I": 0.3, "N": 0.1, "F": 0.4, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:813:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Contingency (Future)", "statement": "It will rain in New York tomorrow.", "gloss": "G2", "rep": 2, "response": "```json\n{\"T\": 0.5, \"I\": 0.7, \"N\": 0.1, \"F\": 0.4}\n```", "T": 0.5, "I": 0.7, "N": 0.1, "F": 0.4, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:814:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Contingency (Future)", "statement": "It will rain in New York tomorrow.", "gloss": "G2", "rep": 3, "response": "```json\n{\"T\": 0.5, \"I\": 0.4, \"N\": 0.1, \"F\": 0.5}\n```", "T": 0.5, "I": 0.4, "N": 0.1, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:815:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Contingency (Future)", "statement": "It will rain in New York tomorrow.", "gloss": "G2", "rep": 4, "response": "```json\n{\"T\": 0.5, \"I\": 0.7, \"N\": 0.1, \"F\": 0.3}\n```", "T": 0.5, "I": 0.7, "N": 0.1, "F": 0.3, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:816:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Contingency (Future)", "statement": "It will rain in New York tomorrow.", "gloss": "G2", "rep": 5, "response": "```json\n{\"T\": 0.5, \"I\": 0.3, \"N\": 0.1, \"F\": 0.4}\n```", "T": 0.5, "I": 0.3, "N": 0.1, "F": 0.4, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:817:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Contingency (Future)", "statement": "It will rain in New York tomorrow.", "gloss": "G2", "rep": 6, "response": "```json\n{\"T\": 0.5, \"I\": 0.4, \"N\": 0.1, \"F\": 0.5}\n```", "T": 0.5, "I": 0.4, "N": 0.1, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:818:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Contingency (Future)", "statement": "It will rain in New York tomorrow.", "gloss": "G2", "rep": 7, "response": "```json\n{\"T\": 0.5, \"I\": 0.3, \"N\": 0.1, \"F\": 0.4}\n```", "T": 0.5, "I": 0.3, "N": 0.1, "F": 0.4, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:819:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Contingency (Future)", "statement": "It will rain in New York tomorrow.", "gloss": "G2", "rep": 8, "response": "```json\n{\"T\": 0.4, \"I\": 0.5, \"N\": 0.1, \"F\": 0.4}\n```", "T": 0.4, "I": 0.5, "N": 0.1, "F": 0.4, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:820:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Contingency (Future)", "statement": "It will rain in New York tomorrow.", "gloss": "G2", "rep": 9, "response": "```json\n{\"T\": 0.5, \"I\": 0.4, \"N\": 0.1, \"F\": 0.5}\n```", "T": 0.5, "I": 0.4, "N": 0.1, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:821:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Contingency (Future)", "statement": "It will rain in New York tomorrow.", "gloss": "G2", "rep": 0, "response": "{\"T\": 0.4, \"I\": 0.5, \"N\": 0.1, \"F\": 0.3}", "T": 0.4, "I": 0.5, "N": 0.1, "F": 0.3, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:822:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Contingency (Future)", "statement": "It will rain in New York tomorrow.", "gloss": "G2", "rep": 1, "response": "{\"T\": 0.4, \"I\": 0.5, \"N\": 0.1, \"F\": 0.3}", "T": 0.4, "I": 0.5, "N": 0.1, "F": 0.3, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:823:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Contingency (Future)", "statement": "It will rain in New York tomorrow.", "gloss": "G2", "rep": 2, "response": "{\"T\": 0.4, \"I\": 0.5, \"N\": 0.1, \"F\": 0.3}", "T": 0.4, "I": 0.5, "N": 0.1, "F": 0.3, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:824:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Contingency (Future)", "statement": "It will rain in New York tomorrow.", "gloss": "G2", "rep": 3, "response": "{\"T\": 0.4, \"I\": 0.5, \"N\": 0.1, \"F\": 0.3}", "T": 0.4, "I": 0.5, "N": 0.1, "F": 0.3, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:825:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Contingency (Future)", "statement": "It will rain in New York tomorrow.", "gloss": "G2", "rep": 4, "response": "{\"T\": 0.4, \"I\": 0.5, \"N\": 0.1, \"F\": 0.3}", "T": 0.4, "I": 0.5, "N": 0.1, "F": 0.3, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:826:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Contingency (Future)", "statement": "It will rain in New York tomorrow.", "gloss": "G2", "rep": 5, "response": "{\"T\": 0.4, \"I\": 0.5, \"N\": 0.1, \"F\": 0.3}", "T": 0.4, "I": 0.5, "N": 0.1, "F": 0.3, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:827:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Contingency (Future)", "statement": "It will rain in New York tomorrow.", "gloss": "G2", "rep": 6, "response": "{\"T\": 0.4, \"I\": 0.5, \"N\": 0.1, \"F\": 0.3}", "T": 0.4, "I": 0.5, "N": 0.1, "F": 0.3, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:828:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Contingency (Future)", "statement": "It will rain in New York tomorrow.", "gloss": "G2", "rep": 7, "response": "{\"T\": 0.4, \"I\": 0.5, \"N\": 0.1, \"F\": 0.3}", "T": 0.4, "I": 0.5, "N": 0.1, "F": 0.3, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:829:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Contingency (Future)", "statement": "It will rain in New York tomorrow.", "gloss": "G2", "rep": 8, "response": "{\"T\": 0.4, \"I\": 0.5, \"N\": 0.1, \"F\": 0.3}", "T": 0.4, "I": 0.5, "N": 0.1, "F": 0.3, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:830:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Contingency (Future)", "statement": "It will rain in New York tomorrow.", "gloss": "G2", "rep": 9, "response": "{\"T\": 0.4, \"I\": 0.5, \"N\": 0.1, \"F\": 0.3}", "T": 0.4, "I": 0.5, "N": 0.1, "F": 0.3, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:831:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Contingency (Future)", "statement": "It will rain in New York tomorrow.", "gloss": "G2", "rep": 0, "response": "```json\n{\n  \"T\": 0.25,\n  \"I\": 0.70,\n  \"N\": 0.05,\n  \"F\": 0.30\n}\n```", "T": 0.25, "I": 0.7, "N": 0.05, "F": 0.3, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:832:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Contingency (Future)", "statement": "It will rain in New York tomorrow.", "gloss": "G2", "rep": 1, "response": "```json\n{\n  \"T\": 0.25,\n  \"I\": 0.70,\n  \"N\": 0.05,\n  \"F\": 0.30\n}\n```", "T": 0.25, "I": 0.7, "N": 0.05, "F": 0.3, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:833:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Contingency (Future)", "statement": "It will rain in New York tomorrow.", "gloss": "G2", "rep": 2, "response": "```json\n{\n  \"T\": 0.35,\n  \"I\": 0.80,\n  \"N\": 0.05,\n  \"F\": 0.20\n}\n```", "T": 0.35, "I": 0.8, "N": 0.05, "F": 0.2, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:834:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Contingency (Future)", "statement": "It will rain in New York tomorrow.", "gloss": "G2", "rep": 3, "response": "```json\n{\n  \"T\": 0.2,\n  \"I\": 0.75,\n  \"N\": 0.05,\n  \"F\": 0.1\n}\n```", "T": 0.2, "I": 0.75, "N": 0.05, "F": 0.1, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:835:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Contingency (Future)", "statement": "It will rain in New York tomorrow.", "gloss": "G2", "rep": 4, "response": "```json\n{\n  \"T\": 0.25,\n  \"I\": 0.70,\n  \"N\": 0.05,\n  \"F\": 0.10\n}\n```", "T": 0.25, "I": 0.7, "N": 0.05, "F": 0.1, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:836:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Contingency (Future)", "statement": "It will rain in New York tomorrow.", "gloss": "G2", "rep": 5, "response": "```json\n{\n  \"T\": 0.35,\n  \"I\": 0.85,\n  \"N\": 0.05,\n  \"F\": 0.10\n}\n```", "T": 0.35, "I": 0.85, "N": 0.05, "F": 0.1, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:837:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Contingency (Future)", "statement": "It will rain in New York tomorrow.", "gloss": "G2", "rep": 6, "response": "```json\n{\n  \"T\": 0.25,\n  \"I\": 0.70,\n  \"N\": 0.05,\n  \"F\": 0.30\n}\n```", "T": 0.25, "I": 0.7, "N": 0.05, "F": 0.3, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:838:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Contingency (Future)", "statement": "It will rain in New York tomorrow.", "gloss": "G2", "rep": 7, "response": "```json\n{\n  \"T\": 0.35,\n  \"I\": 0.60,\n  \"N\": 0.05,\n  \"F\": 0.30\n}\n```", "T": 0.35, "I": 0.6, "N": 0.05, "F": 0.3, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:839:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Contingency (Future)", "statement": "It will rain in New York tomorrow.", "gloss": "G2", "rep": 8, "response": "```json\n{\n  \"T\": 0.35,\n  \"I\": 0.60,\n  \"N\": 0.05,\n  \"F\": 0.30\n}\n```", "T": 0.35, "I": 0.6, "N": 0.05, "F": 0.3, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:840:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Contingency (Future)", "statement": "It will rain in New York tomorrow.", "gloss": "G2", "rep": 9, "response": "```json\n{\n  \"T\": 0.35,\n  \"I\": 0.70,\n  \"N\": 0.05,\n  \"F\": 0.20\n}\n```", "T": 0.35, "I": 0.7, "N": 0.05, "F": 0.2, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:841:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Contingency (Future)", "statement": "It will rain in New York tomorrow.", "gloss": "G3", "rep": 0, "response": "{\"T\": 0.6, \"I\": 0.4, \"N\": 0.5, \"F\": 0.4}", "T": 0.6, "I": 0.4, "N": 0.5, "F": 0.4, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:842:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Contingency (Future)", "statement": "It will rain in New York tomorrow.", "gloss": "G3", "rep": 1, "response": "```json\n{\"T\": 0.6, \"I\": 0.2, \"N\": 0.1, \"F\": 0.3}\n```", "T": 0.6, "I": 0.2, "N": 0.1, "F": 0.3, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:843:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Contingency (Future)", "statement": "It will rain in New York tomorrow.", "gloss": "G3", "rep": 2, "response": "```json\n{\"T\": 0.6, \"I\": 0.3, \"N\": 0.1, \"F\": 0.4}\n```", "T": 0.6, "I": 0.3, "N": 0.1, "F": 0.4, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:844:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Contingency (Future)", "statement": "It will rain in New York tomorrow.", "gloss": "G3", "rep": 3, "response": "```json\n{\"T\": 0.6, \"I\": 0.3, \"N\": 0.1, \"F\": 0.4}\n```", "T": 0.6, "I": 0.3, "N": 0.1, "F": 0.4, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:845:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Contingency (Future)", "statement": "It will rain in New York tomorrow.", "gloss": "G3", "rep": 4, "response": "```json\n{\"T\": 0.3, \"I\": 0.5, \"N\": 0.2, \"F\": 0.3}\n```", "T": 0.3, "I": 0.5, "N": 0.2, "F": 0.3, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:846:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Contingency (Future)", "statement": "It will rain in New York tomorrow.", "gloss": "G3", "rep": 5, "response": "```json\n{\"T\": 0.5, \"I\": 0.3, \"N\": 0.1, \"F\": 0.4}\n```", "T": 0.5, "I": 0.3, "N": 0.1, "F": 0.4, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:847:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Contingency (Future)", "statement": "It will rain in New York tomorrow.", "gloss": "G3", "rep": 6, "response": "{\"T\": 0.5, \"I\": 0.4, \"N\": 0.3, \"F\": 0.5}", "T": 0.5, "I": 0.4, "N": 0.3, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:848:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Contingency (Future)", "statement": "It will rain in New York tomorrow.", "gloss": "G3", "rep": 7, "response": "```json\n{\"T\": 0.6, \"I\": 0.4, \"N\": 0.3, \"F\": 0.3}\n```", "T": 0.6, "I": 0.4, "N": 0.3, "F": 0.3, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:849:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Contingency (Future)", "statement": "It will rain in New York tomorrow.", "gloss": "G3", "rep": 8, "response": "```json\n{\"T\": 0.6, \"I\": 0.3, \"N\": 0.2, \"F\": 0.4}\n```", "T": 0.6, "I": 0.3, "N": 0.2, "F": 0.4, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:850:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Contingency (Future)", "statement": "It will rain in New York tomorrow.", "gloss": "G3", "rep": 9, "response": "```json\n{\"T\": 0.6, \"I\": 0.5, \"N\": 0.2, \"F\": 0.4}\n```", "T": 0.6, "I": 0.5, "N": 0.2, "F": 0.4, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:851:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Contingency (Future)", "statement": "It will rain in New York tomorrow.", "gloss": "G3", "rep": 0, "response": "{\"T\": 0.3, \"I\": 0.8, \"N\": 0.2, \"F\": 0.3}", "T": 0.3, "I": 0.8, "N": 0.2, "F": 0.3, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:852:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Contingency (Future)", "statement": "It will rain in New York tomorrow.", "gloss": "G3", "rep": 1, "response": "{\"T\": 0.3, \"I\": 0.8, \"N\": 0.2, \"F\": 0.3}", "T": 0.3, "I": 0.8, "N": 0.2, "F": 0.3, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:853:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Contingency (Future)", "statement": "It will rain in New York tomorrow.", "gloss": "G3", "rep": 2, "response": "{\"T\": 0.3, \"I\": 0.8, \"N\": 0.4, \"F\": 0.3}", "T": 0.3, "I": 0.8, "N": 0.4, "F": 0.3, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:854:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Contingency (Future)", "statement": "It will rain in New York tomorrow.", "gloss": "G3", "rep": 3, "response": "{\"T\": 0.3, \"I\": 0.8, \"N\": 0.2, \"F\": 0.3}", "T": 0.3, "I": 0.8, "N": 0.2, "F": 0.3, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:855:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Contingency (Future)", "statement": "It will rain in New York tomorrow.", "gloss": "G3", "rep": 4, "response": "{\"T\": 0.3, \"I\": 0.8, \"N\": 0.1, \"F\": 0.3}", "T": 0.3, "I": 0.8, "N": 0.1, "F": 0.3, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:856:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Contingency (Future)", "statement": "It will rain in New York tomorrow.", "gloss": "G3", "rep": 5, "response": "{\"T\": 0.3, \"I\": 0.8, \"N\": 0.2, \"F\": 0.3}", "T": 0.3, "I": 0.8, "N": 0.2, "F": 0.3, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:857:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Contingency (Future)", "statement": "It will rain in New York tomorrow.", "gloss": "G3", "rep": 6, "response": "{\"T\": 0.3, \"I\": 0.8, \"N\": 0.2, \"F\": 0.3}", "T": 0.3, "I": 0.8, "N": 0.2, "F": 0.3, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:858:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Contingency (Future)", "statement": "It will rain in New York tomorrow.", "gloss": "G3", "rep": 7, "response": "{\"T\": 0.3, \"I\": 0.8, \"N\": 0.2, \"F\": 0.3}", "T": 0.3, "I": 0.8, "N": 0.2, "F": 0.3, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:859:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Contingency (Future)", "statement": "It will rain in New York tomorrow.", "gloss": "G3", "rep": 8, "response": "{\"T\": 0.3, \"I\": 0.8, \"N\": 0.2, \"F\": 0.3}", "T": 0.3, "I": 0.8, "N": 0.2, "F": 0.3, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:860:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Contingency (Future)", "statement": "It will rain in New York tomorrow.", "gloss": "G3", "rep": 9, "response": "{\"T\": 0.3, \"I\": 0.8, \"N\": 0.1, \"F\": 0.3}", "T": 0.3, "I": 0.8, "N": 0.1, "F": 0.3, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:861:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Contingency (Future)", "statement": "It will rain in New York tomorrow.", "gloss": "G3", "rep": 0, "response": "{\"T\": 0.4, \"I\": 0.6, \"N\": 0.1, \"F\": 0.3}", "T": 0.4, "I": 0.6, "N": 0.1, "F": 0.3, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:862:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Contingency (Future)", "statement": "It will rain in New York tomorrow.", "gloss": "G3", "rep": 1, "response": "{\"T\": 0.4, \"I\": 0.6, \"N\": 0.1, \"F\": 0.3}", "T": 0.4, "I": 0.6, "N": 0.1, "F": 0.3, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:863:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Contingency (Future)", "statement": "It will rain in New York tomorrow.", "gloss": "G3", "rep": 2, "response": "{\"T\": 0.4, \"I\": 0.6, \"N\": 0.1, \"F\": 0.3}", "T": 0.4, "I": 0.6, "N": 0.1, "F": 0.3, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:864:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Contingency (Future)", "statement": "It will rain in New York tomorrow.", "gloss": "G3", "rep": 3, "response": "{\"T\": 0.4, \"I\": 0.6, \"N\": 0.1, \"F\": 0.3}", "T": 0.4, "I": 0.6, "N": 0.1, "F": 0.3, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:865:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Contingency (Future)", "statement": "It will rain in New York tomorrow.", "gloss": "G3", "rep": 4, "response": "{\"T\": 0.4, \"I\": 0.6, \"N\": 0.1, \"F\": 0.3}", "T": 0.4, "I": 0.6, "N": 0.1, "F": 0.3, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:866:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Contingency (Future)", "statement": "It will rain in New York tomorrow.", "gloss": "G3", "rep": 5, "response": "{\"T\": 0.4, \"I\": 0.6, \"N\": 0.1, \"F\": 0.3}", "T": 0.4, "I": 0.6, "N": 0.1, "F": 0.3, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:867:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Contingency (Future)", "statement": "It will rain in New York tomorrow.", "gloss": "G3", "rep": 6, "response": "{\"T\": 0.4, \"I\": 0.6, \"N\": 0.1, \"F\": 0.3}", "T": 0.4, "I": 0.6, "N": 0.1, "F": 0.3, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:868:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Contingency (Future)", "statement": "It will rain in New York tomorrow.", "gloss": "G3", "rep": 7, "response": "{\"T\": 0.4, \"I\": 0.6, \"N\": 0.1, \"F\": 0.3}", "T": 0.4, "I": 0.6, "N": 0.1, "F": 0.3, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:869:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Contingency (Future)", "statement": "It will rain in New York tomorrow.", "gloss": "G3", "rep": 8, "response": "{\"T\": 0.4, \"I\": 0.6, \"N\": 0.1, \"F\": 0.3}", "T": 0.4, "I": 0.6, "N": 0.1, "F": 0.3, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:870:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Contingency (Future)", "statement": "It will rain in New York tomorrow.", "gloss": "G3", "rep": 9, "response": "{\"T\": 0.4, \"I\": 0.6, \"N\": 0.1, \"F\": 0.3}", "T": 0.4, "I": 0.6, "N": 0.1, "F": 0.3, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:871:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Contingency (Future)", "statement": "It will rain in New York tomorrow.", "gloss": "G3", "rep": 0, "response": "```json\n{\"T\": 0.5, \"I\": 0.4, \"N\": 0.3, \"F\": 0.5}\n```", "T": 0.5, "I": 0.4, "N": 0.3, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:872:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Contingency (Future)", "statement": "It will rain in New York tomorrow.", "gloss": "G3", "rep": 1, "response": "```json\n{\"T\": 0.5, \"I\": 0.3, \"N\": 0.2, \"F\": 0.4}\n```", "T": 0.5, "I": 0.3, "N": 0.2, "F": 0.4, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:873:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Contingency (Future)", "statement": "It will rain in New York tomorrow.", "gloss": "G3", "rep": 2, "response": "```json\n{\"T\": 0.5, \"I\": 0.3, \"N\": 0.2, \"F\": 0.4}\n```", "T": 0.5, "I": 0.3, "N": 0.2, "F": 0.4, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:874:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Contingency (Future)", "statement": "It will rain in New York tomorrow.", "gloss": "G3", "rep": 3, "response": "```json\n{\"T\": 0.5, \"I\": 0.3, \"N\": 0.2, \"F\": 0.4}\n```", "T": 0.5, "I": 0.3, "N": 0.2, "F": 0.4, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:875:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Contingency (Future)", "statement": "It will rain in New York tomorrow.", "gloss": "G3", "rep": 4, "response": "```json\n{\"T\": 0.5, \"I\": 0.3, \"N\": 0.2, \"F\": 0.4}\n```", "T": 0.5, "I": 0.3, "N": 0.2, "F": 0.4, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:876:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Contingency (Future)", "statement": "It will rain in New York tomorrow.", "gloss": "G3", "rep": 5, "response": "```json\n{\"T\": 0.5, \"I\": 0.3, \"N\": 0.2, \"F\": 0.4}\n```", "T": 0.5, "I": 0.3, "N": 0.2, "F": 0.4, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:877:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Contingency (Future)", "statement": "It will rain in New York tomorrow.", "gloss": "G3", "rep": 6, "response": "```json\n{\"T\": 0.5, \"I\": 0.3, \"N\": 0.2, \"F\": 0.4}\n```", "T": 0.5, "I": 0.3, "N": 0.2, "F": 0.4, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:878:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Contingency (Future)", "statement": "It will rain in New York tomorrow.", "gloss": "G3", "rep": 7, "response": "```json\n{\"T\": 0.3, \"I\": 0.6, \"N\": 0.2, \"F\": 0.4}\n```", "T": 0.3, "I": 0.6, "N": 0.2, "F": 0.4, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:879:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Contingency (Future)", "statement": "It will rain in New York tomorrow.", "gloss": "G3", "rep": 8, "response": "```json\n{\"T\": 0.5, \"I\": 0.3, \"N\": 0.2, \"F\": 0.4}\n```", "T": 0.5, "I": 0.3, "N": 0.2, "F": 0.4, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:880:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Contingency (Future)", "statement": "It will rain in New York tomorrow.", "gloss": "G3", "rep": 9, "response": "```json\n{\"T\": 0.5, \"I\": 0.3, \"N\": 0.2, \"F\": 0.4}\n```", "T": 0.5, "I": 0.3, "N": 0.2, "F": 0.4, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:881:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Contingency (Future)", "statement": "It will rain in New York tomorrow.", "gloss": "G3", "rep": 0, "response": "{\"T\": 0.4, \"I\": 0.3, \"N\": 0.2, \"F\": 0.35}", "T": 0.4, "I": 0.3, "N": 0.2, "F": 0.35, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:882:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Contingency (Future)", "statement": "It will rain in New York tomorrow.", "gloss": "G3", "rep": 1, "response": "{\"T\": 0.4, \"I\": 0.3, \"N\": 0.2, \"F\": 0.35}", "T": 0.4, "I": 0.3, "N": 0.2, "F": 0.35, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:883:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Contingency (Future)", "statement": "It will rain in New York tomorrow.", "gloss": "G3", "rep": 2, "response": "{\"T\": 0.4, \"I\": 0.3, \"N\": 0.2, \"F\": 0.5}", "T": 0.4, "I": 0.3, "N": 0.2, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:884:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Contingency (Future)", "statement": "It will rain in New York tomorrow.", "gloss": "G3", "rep": 3, "response": "{\"T\": 0.4, \"I\": 0.3, \"N\": 0.2, \"F\": 0.5}", "T": 0.4, "I": 0.3, "N": 0.2, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:885:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Contingency (Future)", "statement": "It will rain in New York tomorrow.", "gloss": "G3", "rep": 4, "response": "{\"T\": 0.4, \"I\": 0.3, \"N\": 0.2, \"F\": 0.5}", "T": 0.4, "I": 0.3, "N": 0.2, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:886:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Contingency (Future)", "statement": "It will rain in New York tomorrow.", "gloss": "G3", "rep": 5, "response": "{\"T\": 0.4, \"I\": 0.3, \"N\": 0.2, \"F\": 0.35}", "T": 0.4, "I": 0.3, "N": 0.2, "F": 0.35, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:887:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Contingency (Future)", "statement": "It will rain in New York tomorrow.", "gloss": "G3", "rep": 6, "response": "{\"T\": 0.4, \"I\": 0.3, \"N\": 0.2, \"F\": 0.35}", "T": 0.4, "I": 0.3, "N": 0.2, "F": 0.35, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:888:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Contingency (Future)", "statement": "It will rain in New York tomorrow.", "gloss": "G3", "rep": 7, "response": "{\"T\": 0.4, \"I\": 0.3, \"N\": 0.2, \"F\": 0.5}", "T": 0.4, "I": 0.3, "N": 0.2, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:889:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Contingency (Future)", "statement": "It will rain in New York tomorrow.", "gloss": "G3", "rep": 8, "response": "{\"T\": 0.4, \"I\": 0.3, \"N\": 0.2, \"F\": 0.35}", "T": 0.4, "I": 0.3, "N": 0.2, "F": 0.35, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:890:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Contingency (Future)", "statement": "It will rain in New York tomorrow.", "gloss": "G3", "rep": 9, "response": "{\"T\": 0.4, \"I\": 0.3, \"N\": 0.2, \"F\": 0.5}", "T": 0.4, "I": 0.3, "N": 0.2, "F": 0.5, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:891:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Contingency (Future)", "statement": "It will rain in New York tomorrow.", "gloss": "G3", "rep": 0, "response": "```json\n{\n  \"T\": 0.25,\n  \"I\": 0.70,\n  \"N\": 0.10,\n  \"F\": 0.05\n}\n```", "T": 0.25, "I": 0.7, "N": 0.1, "F": 0.05, "regime": "very_weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:892:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Contingency (Future)", "statement": "It will rain in New York tomorrow.", "gloss": "G3", "rep": 1, "response": "```json\n{\n  \"T\": 0.25,\n  \"I\": 0.80,\n  \"N\": 0.10,\n  \"F\": 0.05\n}\n```", "T": 0.25, "I": 0.8, "N": 0.1, "F": 0.05, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:893:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Contingency (Future)", "statement": "It will rain in New York tomorrow.", "gloss": "G3", "rep": 2, "response": "```json\n{\n  \"T\": 0.25,\n  \"I\": 0.70,\n  \"N\": 0.10,\n  \"F\": 0.05\n}\n```", "T": 0.25, "I": 0.7, "N": 0.1, "F": 0.05, "regime": "very_weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:894:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Contingency (Future)", "statement": "It will rain in New York tomorrow.", "gloss": "G3", "rep": 3, "response": "```json\n{\n  \"T\": 0.3,\n  \"I\": 0.75,\n  \"N\": 0.2,\n  \"F\": 0.05\n}\n```", "T": 0.3, "I": 0.75, "N": 0.2, "F": 0.05, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:895:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Contingency (Future)", "statement": "It will rain in New York tomorrow.", "gloss": "G3", "rep": 4, "response": "```json\n{\n  \"T\": 0.25,\n  \"I\": 0.80,\n  \"N\": 0.10,\n  \"F\": 0.05\n}\n```", "T": 0.25, "I": 0.8, "N": 0.1, "F": 0.05, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:896:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Contingency (Future)", "statement": "It will rain in New York tomorrow.", "gloss": "G3", "rep": 5, "response": "```json\n{\n  \"T\": 0.25,\n  \"I\": 0.70,\n  \"N\": 0.15,\n  \"F\": 0.05\n}\n```", "T": 0.25, "I": 0.7, "N": 0.15, "F": 0.05, "regime": "very_weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:897:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Contingency (Future)", "statement": "It will rain in New York tomorrow.", "gloss": "G3", "rep": 6, "response": "```json\n{\n  \"T\": 0.0,\n  \"I\": 0.85,\n  \"N\": 0.1,\n  \"F\": 0.05\n}\n```", "T": 0.0, "I": 0.85, "N": 0.1, "F": 0.05, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:898:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Contingency (Future)", "statement": "It will rain in New York tomorrow.", "gloss": "G3", "rep": 7, "response": "```json\n{\n  \"T\": 0.25,\n  \"I\": 0.75,\n  \"N\": 0.15,\n  \"F\": 0.05\n}\n```", "T": 0.25, "I": 0.75, "N": 0.15, "F": 0.05, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:899:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Contingency (Future)", "statement": "It will rain in New York tomorrow.", "gloss": "G3", "rep": 8, "response": "```json\n{\n  \"T\": 0.35,\n  \"I\": 0.65,\n  \"N\": 0.05,\n  \"F\": 0.0\n}\n```", "T": 0.35, "I": 0.65, "N": 0.05, "F": 0.0, "regime": "very_weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:900:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Contingency (Future)", "statement": "It will rain in New York tomorrow.", "gloss": "G3", "rep": 9, "response": "```json\n{\n  \"T\": 0.25,\n  \"I\": 0.70,\n  \"N\": 0.10,\n  \"F\": 0.05\n}\n```", "T": 0.25, "I": 0.7, "N": 0.1, "F": 0.05, "regime": "very_weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:901:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Tautology (Logical)", "statement": "It is raining or it is not raining.", "gloss": "G1", "rep": 0, "response": "```json\n{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:902:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Tautology (Logical)", "statement": "It is raining or it is not raining.", "gloss": "G1", "rep": 1, "response": "```json\n{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:903:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Tautology (Logical)", "statement": "It is raining or it is not raining.", "gloss": "G1", "rep": 2, "response": "```json\n{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:904:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Tautology (Logical)", "statement": "It is raining or it is not raining.", "gloss": "G1", "rep": 3, "response": "```json\n{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:905:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Tautology (Logical)", "statement": "It is raining or it is not raining.", "gloss": "G1", "rep": 4, "response": "```json\n{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:906:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Tautology (Logical)", "statement": "It is raining or it is not raining.", "gloss": "G1", "rep": 5, "response": "```json\n{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:907:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Tautology (Logical)", "statement": "It is raining or it is not raining.", "gloss": "G1", "rep": 6, "response": "```json\n{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:908:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Tautology (Logical)", "statement": "It is raining or it is not raining.", "gloss": "G1", "rep": 7, "response": "```json\n{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:909:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Tautology (Logical)", "statement": "It is raining or it is not raining.", "gloss": "G1", "rep": 8, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:910:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Tautology (Logical)", "statement": "It is raining or it is not raining.", "gloss": "G1", "rep": 9, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:911:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Tautology (Logical)", "statement": "It is raining or it is not raining.", "gloss": "G1", "rep": 0, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:912:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Tautology (Logical)", "statement": "It is raining or it is not raining.", "gloss": "G1", "rep": 1, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:913:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Tautology (Logical)", "statement": "It is raining or it is not raining.", "gloss": "G1", "rep": 2, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:914:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Tautology (Logical)", "statement": "It is raining or it is not raining.", "gloss": "G1", "rep": 3, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:915:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Tautology (Logical)", "statement": "It is raining or it is not raining.", "gloss": "G1", "rep": 4, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:916:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Tautology (Logical)", "statement": "It is raining or it is not raining.", "gloss": "G1", "rep": 5, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:917:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Tautology (Logical)", "statement": "It is raining or it is not raining.", "gloss": "G1", "rep": 6, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:918:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Tautology (Logical)", "statement": "It is raining or it is not raining.", "gloss": "G1", "rep": 7, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:919:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Tautology (Logical)", "statement": "It is raining or it is not raining.", "gloss": "G1", "rep": 8, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:920:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Tautology (Logical)", "statement": "It is raining or it is not raining.", "gloss": "G1", "rep": 9, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:921:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Tautology (Logical)", "statement": "It is raining or it is not raining.", "gloss": "G1", "rep": 0, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:922:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Tautology (Logical)", "statement": "It is raining or it is not raining.", "gloss": "G1", "rep": 1, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:923:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Tautology (Logical)", "statement": "It is raining or it is not raining.", "gloss": "G1", "rep": 2, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:924:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Tautology (Logical)", "statement": "It is raining or it is not raining.", "gloss": "G1", "rep": 3, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:925:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Tautology (Logical)", "statement": "It is raining or it is not raining.", "gloss": "G1", "rep": 4, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:926:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Tautology (Logical)", "statement": "It is raining or it is not raining.", "gloss": "G1", "rep": 5, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:927:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Tautology (Logical)", "statement": "It is raining or it is not raining.", "gloss": "G1", "rep": 6, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:928:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Tautology (Logical)", "statement": "It is raining or it is not raining.", "gloss": "G1", "rep": 7, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:929:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Tautology (Logical)", "statement": "It is raining or it is not raining.", "gloss": "G1", "rep": 8, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:930:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Tautology (Logical)", "statement": "It is raining or it is not raining.", "gloss": "G1", "rep": 9, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:931:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Tautology (Logical)", "statement": "It is raining or it is not raining.", "gloss": "G1", "rep": 0, "response": "```json\n{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:932:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Tautology (Logical)", "statement": "It is raining or it is not raining.", "gloss": "G1", "rep": 1, "response": "```json\n{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:933:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Tautology (Logical)", "statement": "It is raining or it is not raining.", "gloss": "G1", "rep": 2, "response": "```json\n{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:934:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Tautology (Logical)", "statement": "It is raining or it is not raining.", "gloss": "G1", "rep": 3, "response": "```json\n{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:935:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Tautology (Logical)", "statement": "It is raining or it is not raining.", "gloss": "G1", "rep": 4, "response": "```json\n{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:936:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Tautology (Logical)", "statement": "It is raining or it is not raining.", "gloss": "G1", "rep": 5, "response": "```json\n{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:937:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Tautology (Logical)", "statement": "It is raining or it is not raining.", "gloss": "G1", "rep": 6, "response": "```json\n{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:938:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Tautology (Logical)", "statement": "It is raining or it is not raining.", "gloss": "G1", "rep": 7, "response": "```json\n{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:939:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Tautology (Logical)", "statement": "It is raining or it is not raining.", "gloss": "G1", "rep": 8, "response": "```json\n{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:940:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Tautology (Logical)", "statement": "It is raining or it is not raining.", "gloss": "G1", "rep": 9, "response": "```json\n{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:941:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Tautology (Logical)", "statement": "It is raining or it is not raining.", "gloss": "G1", "rep": 0, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:942:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Tautology (Logical)", "statement": "It is raining or it is not raining.", "gloss": "G1", "rep": 1, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:943:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Tautology (Logical)", "statement": "It is raining or it is not raining.", "gloss": "G1", "rep": 2, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:944:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Tautology (Logical)", "statement": "It is raining or it is not raining.", "gloss": "G1", "rep": 3, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:945:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Tautology (Logical)", "statement": "It is raining or it is not raining.", "gloss": "G1", "rep": 4, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:946:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Tautology (Logical)", "statement": "It is raining or it is not raining.", "gloss": "G1", "rep": 5, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:947:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Tautology (Logical)", "statement": "It is raining or it is not raining.", "gloss": "G1", "rep": 6, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:948:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Tautology (Logical)", "statement": "It is raining or it is not raining.", "gloss": "G1", "rep": 7, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:949:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Tautology (Logical)", "statement": "It is raining or it is not raining.", "gloss": "G1", "rep": 8, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:950:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Tautology (Logical)", "statement": "It is raining or it is not raining.", "gloss": "G1", "rep": 9, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:951:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Tautology (Logical)", "statement": "It is raining or it is not raining.", "gloss": "G1", "rep": 0, "response": "```json\n{\n  \"T\": 1.0,\n  \"I\": 0.0,\n  \"N\": 0.0,\n  \"F\": 0.0\n}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:952:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Tautology (Logical)", "statement": "It is raining or it is not raining.", "gloss": "G1", "rep": 1, "response": "```json\n{\n  \"T\": 1.0,\n  \"I\": 0.0,\n  \"N\": 0.0,\n  \"F\": 0.0\n}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:953:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Tautology (Logical)", "statement": "It is raining or it is not raining.", "gloss": "G1", "rep": 2, "response": "```json\n{\n  \"T\": 1.0,\n  \"I\": 0.0,\n  \"N\": 0.0,\n  \"F\": 0.0\n}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:954:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Tautology (Logical)", "statement": "It is raining or it is not raining.", "gloss": "G1", "rep": 3, "response": "```json\n{\n  \"T\": 1.0,\n  \"I\": 0.0,\n  \"N\": 0.0,\n  \"F\": 0.0\n}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:955:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Tautology (Logical)", "statement": "It is raining or it is not raining.", "gloss": "G1", "rep": 4, "response": "```json\n{\n  \"T\": 1.0,\n  \"I\": 0.0,\n  \"N\": 0.0,\n  \"F\": 0.0\n}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:956:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Tautology (Logical)", "statement": "It is raining or it is not raining.", "gloss": "G1", "rep": 5, "response": "```json\n{\n  \"T\": 1.0,\n  \"I\": 0.0,\n  \"N\": 0.0,\n  \"F\": 0.0\n}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:957:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Tautology (Logical)", "statement": "It is raining or it is not raining.", "gloss": "G1", "rep": 6, "response": "```json\n{\n  \"T\": 1.0,\n  \"I\": 0.0,\n  \"N\": 0.0,\n  \"F\": 0.0\n}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:958:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Tautology (Logical)", "statement": "It is raining or it is not raining.", "gloss": "G1", "rep": 7, "response": "```json\n{\n  \"T\": 1.0,\n  \"I\": 0.0,\n  \"N\": 0.0,\n  \"F\": 0.0\n}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:959:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Tautology (Logical)", "statement": "It is raining or it is not raining.", "gloss": "G1", "rep": 8, "response": "```json\n{\n  \"T\": 1.0,\n  \"I\": 0.0,\n  \"N\": 0.0,\n  \"F\": 0.0\n}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:960:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Tautology (Logical)", "statement": "It is raining or it is not raining.", "gloss": "G1", "rep": 9, "response": "```json\n{\n  \"T\": 1.0,\n  \"I\": 0.0,\n  \"N\": 0.0,\n  \"F\": 0.0\n}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:961:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Tautology (Logical)", "statement": "It is raining or it is not raining.", "gloss": "G2", "rep": 0, "response": "```json\n{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:962:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Tautology (Logical)", "statement": "It is raining or it is not raining.", "gloss": "G2", "rep": 1, "response": "```json\n{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:963:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Tautology (Logical)", "statement": "It is raining or it is not raining.", "gloss": "G2", "rep": 2, "response": "```json\n{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:964:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Tautology (Logical)", "statement": "It is raining or it is not raining.", "gloss": "G2", "rep": 3, "response": "```json\n{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:965:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Tautology (Logical)", "statement": "It is raining or it is not raining.", "gloss": "G2", "rep": 4, "response": "```json\n{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:966:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Tautology (Logical)", "statement": "It is raining or it is not raining.", "gloss": "G2", "rep": 5, "response": "```json\n{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:967:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Tautology (Logical)", "statement": "It is raining or it is not raining.", "gloss": "G2", "rep": 6, "response": "```json\n{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:968:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Tautology (Logical)", "statement": "It is raining or it is not raining.", "gloss": "G2", "rep": 7, "response": "```json\n{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:969:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Tautology (Logical)", "statement": "It is raining or it is not raining.", "gloss": "G2", "rep": 8, "response": "```json\n{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:970:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Tautology (Logical)", "statement": "It is raining or it is not raining.", "gloss": "G2", "rep": 9, "response": "```json\n{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:971:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Tautology (Logical)", "statement": "It is raining or it is not raining.", "gloss": "G2", "rep": 0, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:972:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Tautology (Logical)", "statement": "It is raining or it is not raining.", "gloss": "G2", "rep": 1, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:973:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Tautology (Logical)", "statement": "It is raining or it is not raining.", "gloss": "G2", "rep": 2, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:974:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Tautology (Logical)", "statement": "It is raining or it is not raining.", "gloss": "G2", "rep": 3, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:975:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Tautology (Logical)", "statement": "It is raining or it is not raining.", "gloss": "G2", "rep": 4, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:976:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Tautology (Logical)", "statement": "It is raining or it is not raining.", "gloss": "G2", "rep": 5, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:977:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Tautology (Logical)", "statement": "It is raining or it is not raining.", "gloss": "G2", "rep": 6, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:978:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Tautology (Logical)", "statement": "It is raining or it is not raining.", "gloss": "G2", "rep": 7, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:979:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Tautology (Logical)", "statement": "It is raining or it is not raining.", "gloss": "G2", "rep": 8, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:980:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Tautology (Logical)", "statement": "It is raining or it is not raining.", "gloss": "G2", "rep": 9, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:981:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Tautology (Logical)", "statement": "It is raining or it is not raining.", "gloss": "G2", "rep": 0, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:982:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Tautology (Logical)", "statement": "It is raining or it is not raining.", "gloss": "G2", "rep": 1, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:983:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Tautology (Logical)", "statement": "It is raining or it is not raining.", "gloss": "G2", "rep": 2, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:984:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Tautology (Logical)", "statement": "It is raining or it is not raining.", "gloss": "G2", "rep": 3, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:985:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Tautology (Logical)", "statement": "It is raining or it is not raining.", "gloss": "G2", "rep": 4, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:986:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Tautology (Logical)", "statement": "It is raining or it is not raining.", "gloss": "G2", "rep": 5, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:987:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Tautology (Logical)", "statement": "It is raining or it is not raining.", "gloss": "G2", "rep": 6, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:988:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Tautology (Logical)", "statement": "It is raining or it is not raining.", "gloss": "G2", "rep": 7, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:989:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Tautology (Logical)", "statement": "It is raining or it is not raining.", "gloss": "G2", "rep": 8, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:990:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Tautology (Logical)", "statement": "It is raining or it is not raining.", "gloss": "G2", "rep": 9, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:991:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Tautology (Logical)", "statement": "It is raining or it is not raining.", "gloss": "G2", "rep": 0, "response": "```json\n{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:992:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Tautology (Logical)", "statement": "It is raining or it is not raining.", "gloss": "G2", "rep": 1, "response": "```json\n{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:993:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Tautology (Logical)", "statement": "It is raining or it is not raining.", "gloss": "G2", "rep": 2, "response": "```json\n{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:994:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Tautology (Logical)", "statement": "It is raining or it is not raining.", "gloss": "G2", "rep": 3, "response": "```json\n{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:995:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Tautology (Logical)", "statement": "It is raining or it is not raining.", "gloss": "G2", "rep": 4, "response": "```json\n{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:996:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Tautology (Logical)", "statement": "It is raining or it is not raining.", "gloss": "G2", "rep": 5, "response": "```json\n{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:997:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Tautology (Logical)", "statement": "It is raining or it is not raining.", "gloss": "G2", "rep": 6, "response": "```json\n{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:998:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Tautology (Logical)", "statement": "It is raining or it is not raining.", "gloss": "G2", "rep": 7, "response": "```json\n{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:999:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Tautology (Logical)", "statement": "It is raining or it is not raining.", "gloss": "G2", "rep": 8, "response": "```json\n{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1000:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Tautology (Logical)", "statement": "It is raining or it is not raining.", "gloss": "G2", "rep": 9, "response": "```json\n{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1001:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Tautology (Logical)", "statement": "It is raining or it is not raining.", "gloss": "G2", "rep": 0, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1002:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Tautology (Logical)", "statement": "It is raining or it is not raining.", "gloss": "G2", "rep": 1, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1003:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Tautology (Logical)", "statement": "It is raining or it is not raining.", "gloss": "G2", "rep": 2, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1004:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Tautology (Logical)", "statement": "It is raining or it is not raining.", "gloss": "G2", "rep": 3, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1005:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Tautology (Logical)", "statement": "It is raining or it is not raining.", "gloss": "G2", "rep": 4, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1006:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Tautology (Logical)", "statement": "It is raining or it is not raining.", "gloss": "G2", "rep": 5, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1007:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Tautology (Logical)", "statement": "It is raining or it is not raining.", "gloss": "G2", "rep": 6, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1008:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Tautology (Logical)", "statement": "It is raining or it is not raining.", "gloss": "G2", "rep": 7, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1009:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Tautology (Logical)", "statement": "It is raining or it is not raining.", "gloss": "G2", "rep": 8, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1010:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Tautology (Logical)", "statement": "It is raining or it is not raining.", "gloss": "G2", "rep": 9, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1011:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Tautology (Logical)", "statement": "It is raining or it is not raining.", "gloss": "G2", "rep": 0, "response": "```json\n{\n  \"T\": 1.0,\n  \"I\": 0.0,\n  \"N\": 0.0,\n  \"F\": 0.0\n}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1012:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Tautology (Logical)", "statement": "It is raining or it is not raining.", "gloss": "G2", "rep": 1, "response": "```json\n{\n  \"T\": 1.0,\n  \"I\": 0.0,\n  \"N\": 0.0,\n  \"F\": 0.0\n}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1013:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Tautology (Logical)", "statement": "It is raining or it is not raining.", "gloss": "G2", "rep": 2, "response": "```json\n{\n  \"T\": 1.0,\n  \"I\": 0.0,\n  \"N\": 0.0,\n  \"F\": 0.0\n}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1014:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Tautology (Logical)", "statement": "It is raining or it is not raining.", "gloss": "G2", "rep": 3, "response": "```json\n{\n  \"T\": 1.0,\n  \"I\": 0.0,\n  \"N\": 0.0,\n  \"F\": 0.0\n}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1015:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Tautology (Logical)", "statement": "It is raining or it is not raining.", "gloss": "G2", "rep": 4, "response": "```json\n{\n  \"T\": 1.0,\n  \"I\": 0.0,\n  \"N\": 0.0,\n  \"F\": 0.0\n}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1016:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Tautology (Logical)", "statement": "It is raining or it is not raining.", "gloss": "G2", "rep": 5, "response": "```json\n{\n  \"T\": 1.0,\n  \"I\": 0.0,\n  \"N\": 0.0,\n  \"F\": 0.0\n}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1017:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Tautology (Logical)", "statement": "It is raining or it is not raining.", "gloss": "G2", "rep": 6, "response": "```json\n{\n  \"T\": 1.0,\n  \"I\": 0.0,\n  \"N\": 0.0,\n  \"F\": 0.0\n}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1018:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Tautology (Logical)", "statement": "It is raining or it is not raining.", "gloss": "G2", "rep": 7, "response": "```json\n{\n  \"T\": 1.0,\n  \"I\": 0.0,\n  \"N\": 0.0,\n  \"F\": 0.0\n}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1019:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Tautology (Logical)", "statement": "It is raining or it is not raining.", "gloss": "G2", "rep": 8, "response": "```json\n{\n  \"T\": 1.0,\n  \"I\": 0.0,\n  \"N\": 0.0,\n  \"F\": 0.0\n}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1020:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Tautology (Logical)", "statement": "It is raining or it is not raining.", "gloss": "G2", "rep": 9, "response": "```json\n{\n  \"T\": 1.0,\n  \"I\": 0.0,\n  \"N\": 0.0,\n  \"F\": 0.0\n}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1021:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Tautology (Logical)", "statement": "It is raining or it is not raining.", "gloss": "G3", "rep": 0, "response": "```json\n{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1022:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Tautology (Logical)", "statement": "It is raining or it is not raining.", "gloss": "G3", "rep": 1, "response": "```json\n{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1023:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Tautology (Logical)", "statement": "It is raining or it is not raining.", "gloss": "G3", "rep": 2, "response": "```json\n{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1024:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Tautology (Logical)", "statement": "It is raining or it is not raining.", "gloss": "G3", "rep": 3, "response": "```json\n{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1025:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Tautology (Logical)", "statement": "It is raining or it is not raining.", "gloss": "G3", "rep": 4, "response": "```json\n{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1026:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Tautology (Logical)", "statement": "It is raining or it is not raining.", "gloss": "G3", "rep": 5, "response": "```json\n{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1027:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Tautology (Logical)", "statement": "It is raining or it is not raining.", "gloss": "G3", "rep": 6, "response": "```json\n{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1028:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Tautology (Logical)", "statement": "It is raining or it is not raining.", "gloss": "G3", "rep": 7, "response": "```json\n{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1029:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Tautology (Logical)", "statement": "It is raining or it is not raining.", "gloss": "G3", "rep": 8, "response": "```json\n{\"T\": 1.0, \"I\": 0.0, \"N\": 1.0, \"F\": 0.0}\n```", "T": 1.0, "I": 0.0, "N": 1.0, "F": 0.0, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1030:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Tautology (Logical)", "statement": "It is raining or it is not raining.", "gloss": "G3", "rep": 9, "response": "```json\n{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1031:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Tautology (Logical)", "statement": "It is raining or it is not raining.", "gloss": "G3", "rep": 0, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1032:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Tautology (Logical)", "statement": "It is raining or it is not raining.", "gloss": "G3", "rep": 1, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1033:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Tautology (Logical)", "statement": "It is raining or it is not raining.", "gloss": "G3", "rep": 2, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1034:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Tautology (Logical)", "statement": "It is raining or it is not raining.", "gloss": "G3", "rep": 3, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1035:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Tautology (Logical)", "statement": "It is raining or it is not raining.", "gloss": "G3", "rep": 4, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1036:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Tautology (Logical)", "statement": "It is raining or it is not raining.", "gloss": "G3", "rep": 5, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1037:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Tautology (Logical)", "statement": "It is raining or it is not raining.", "gloss": "G3", "rep": 6, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1038:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Tautology (Logical)", "statement": "It is raining or it is not raining.", "gloss": "G3", "rep": 7, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1039:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Tautology (Logical)", "statement": "It is raining or it is not raining.", "gloss": "G3", "rep": 8, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1040:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Tautology (Logical)", "statement": "It is raining or it is not raining.", "gloss": "G3", "rep": 9, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1041:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Tautology (Logical)", "statement": "It is raining or it is not raining.", "gloss": "G3", "rep": 0, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1042:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Tautology (Logical)", "statement": "It is raining or it is not raining.", "gloss": "G3", "rep": 1, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1043:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Tautology (Logical)", "statement": "It is raining or it is not raining.", "gloss": "G3", "rep": 2, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1044:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Tautology (Logical)", "statement": "It is raining or it is not raining.", "gloss": "G3", "rep": 3, "response": "{\"T\": 1.0, \"I\": 0.0, \"", "T": null, "I": null, "N": null, "F": null, "regime": null, "parsed": false, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1045:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Tautology (Logical)", "statement": "It is raining or it is not raining.", "gloss": "G3", "rep": 4, "response": "{\"T\": 1.0, \"I\": 0.0, \"", "T": null, "I": null, "N": null, "F": null, "regime": null, "parsed": false, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1046:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Tautology (Logical)", "statement": "It is raining or it is not raining.", "gloss": "G3", "rep": 5, "response": "{\"T\": 1.0, \"I\": 0.0, \"", "T": null, "I": null, "N": null, "F": null, "regime": null, "parsed": false, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1047:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Tautology (Logical)", "statement": "It is raining or it is not raining.", "gloss": "G3", "rep": 6, "response": "{\"T\": 1.0, \"I\": 0.0, \"", "T": null, "I": null, "N": null, "F": null, "regime": null, "parsed": false, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1048:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Tautology (Logical)", "statement": "It is raining or it is not raining.", "gloss": "G3", "rep": 7, "response": "{\"T\": 1.0, \"I\": 0.0, \"", "T": null, "I": null, "N": null, "F": null, "regime": null, "parsed": false, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1049:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Tautology (Logical)", "statement": "It is raining or it is not raining.", "gloss": "G3", "rep": 8, "response": "{\"T\": 1.0, \"I\": 0.0, \"", "T": null, "I": null, "N": null, "F": null, "regime": null, "parsed": false, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1050:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Tautology (Logical)", "statement": "It is raining or it is not raining.", "gloss": "G3", "rep": 9, "response": "{\"T\": 1.0, \"I\": 0.0, \"", "T": null, "I": null, "N": null, "F": null, "regime": null, "parsed": false, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1051:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Tautology (Logical)", "statement": "It is raining or it is not raining.", "gloss": "G3", "rep": 0, "response": "```json\n{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1052:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Tautology (Logical)", "statement": "It is raining or it is not raining.", "gloss": "G3", "rep": 1, "response": "```json\n{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1053:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Tautology (Logical)", "statement": "It is raining or it is not raining.", "gloss": "G3", "rep": 2, "response": "```json\n{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1054:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Tautology (Logical)", "statement": "It is raining or it is not raining.", "gloss": "G3", "rep": 3, "response": "```json\n{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1055:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Tautology (Logical)", "statement": "It is raining or it is not raining.", "gloss": "G3", "rep": 4, "response": "```json\n{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1056:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Tautology (Logical)", "statement": "It is raining or it is not raining.", "gloss": "G3", "rep": 5, "response": "```json\n{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1057:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Tautology (Logical)", "statement": "It is raining or it is not raining.", "gloss": "G3", "rep": 6, "response": "```json\n{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1058:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Tautology (Logical)", "statement": "It is raining or it is not raining.", "gloss": "G3", "rep": 7, "response": "```json\n{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1059:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Tautology (Logical)", "statement": "It is raining or it is not raining.", "gloss": "G3", "rep": 8, "response": "```json\n{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1060:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Tautology (Logical)", "statement": "It is raining or it is not raining.", "gloss": "G3", "rep": 9, "response": "```json\n{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1061:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Tautology (Logical)", "statement": "It is raining or it is not raining.", "gloss": "G3", "rep": 0, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1062:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Tautology (Logical)", "statement": "It is raining or it is not raining.", "gloss": "G3", "rep": 1, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1063:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Tautology (Logical)", "statement": "It is raining or it is not raining.", "gloss": "G3", "rep": 2, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1064:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Tautology (Logical)", "statement": "It is raining or it is not raining.", "gloss": "G3", "rep": 3, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1065:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Tautology (Logical)", "statement": "It is raining or it is not raining.", "gloss": "G3", "rep": 4, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1066:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Tautology (Logical)", "statement": "It is raining or it is not raining.", "gloss": "G3", "rep": 5, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1067:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Tautology (Logical)", "statement": "It is raining or it is not raining.", "gloss": "G3", "rep": 6, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1068:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Tautology (Logical)", "statement": "It is raining or it is not raining.", "gloss": "G3", "rep": 7, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1069:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Tautology (Logical)", "statement": "It is raining or it is not raining.", "gloss": "G3", "rep": 8, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1070:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Tautology (Logical)", "statement": "It is raining or it is not raining.", "gloss": "G3", "rep": 9, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1071:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Tautology (Logical)", "statement": "It is raining or it is not raining.", "gloss": "G3", "rep": 0, "response": "```json\n{\n  \"T\": 1.0,\n  \"I\": 0.0,\n  \"N\": 0.0,\n  \"F\": 0.0\n}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1072:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Tautology (Logical)", "statement": "It is raining or it is not raining.", "gloss": "G3", "rep": 1, "response": "```json\n{\n  \"T\": 1.0,\n  \"I\": 0.0,\n  \"N\": 0.0,\n  \"F\": 0.0\n}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1073:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Tautology (Logical)", "statement": "It is raining or it is not raining.", "gloss": "G3", "rep": 2, "response": "```json\n{\n  \"T\": 1.0,\n  \"I\": 0.0,\n  \"N\": 0.0,\n  \"F\": 0.0\n}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1074:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Tautology (Logical)", "statement": "It is raining or it is not raining.", "gloss": "G3", "rep": 3, "response": "```json\n{\n  \"T\": 1.0,\n  \"I\": 0.0,\n  \"N\": 0.0,\n  \"F\": 0.0\n}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1075:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Tautology (Logical)", "statement": "It is raining or it is not raining.", "gloss": "G3", "rep": 4, "response": "```json\n{\n  \"T\": 1.0,\n  \"I\": 0.0,\n  \"N\": 0.0,\n  \"F\": 0.0\n}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1076:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Tautology (Logical)", "statement": "It is raining or it is not raining.", "gloss": "G3", "rep": 5, "response": "```json\n{\n  \"T\": 1.0,\n  \"I\": 0.0,\n  \"N\": 0.0,\n  \"F\": 0.0\n}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1077:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Tautology (Logical)", "statement": "It is raining or it is not raining.", "gloss": "G3", "rep": 6, "response": "```json\n{\n  \"T\": 1.0,\n  \"I\": 0.0,\n  \"N\": 0.0,\n  \"F\": 0.0\n}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1078:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Tautology (Logical)", "statement": "It is raining or it is not raining.", "gloss": "G3", "rep": 7, "response": "```json\n{\n  \"T\": 1.0,\n  \"I\": 0.0,\n  \"N\": 0.0,\n  \"F\": 0.0\n}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1079:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Tautology (Logical)", "statement": "It is raining or it is not raining.", "gloss": "G3", "rep": 8, "response": "```json\n{\n  \"T\": 1.0,\n  \"I\": 0.0,\n  \"N\": 0.0,\n  \"F\": 0.0\n}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1080:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Tautology (Logical)", "statement": "It is raining or it is not raining.", "gloss": "G3", "rep": 9, "response": "```json\n{\n  \"T\": 1.0,\n  \"I\": 0.0,\n  \"N\": 0.0,\n  \"F\": 0.0\n}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1081:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Tautology (Math)", "statement": "2 + 2 = 4.", "gloss": "G1", "rep": 0, "response": "```json\n{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1082:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Tautology (Math)", "statement": "2 + 2 = 4.", "gloss": "G1", "rep": 1, "response": "```json\n{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1083:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Tautology (Math)", "statement": "2 + 2 = 4.", "gloss": "G1", "rep": 2, "response": "```json\n{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1084:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Tautology (Math)", "statement": "2 + 2 = 4.", "gloss": "G1", "rep": 3, "response": "```json\n{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1085:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Tautology (Math)", "statement": "2 + 2 = 4.", "gloss": "G1", "rep": 4, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1086:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Tautology (Math)", "statement": "2 + 2 = 4.", "gloss": "G1", "rep": 5, "response": "```json\n{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1087:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Tautology (Math)", "statement": "2 + 2 = 4.", "gloss": "G1", "rep": 6, "response": "```json\n{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1088:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Tautology (Math)", "statement": "2 + 2 = 4.", "gloss": "G1", "rep": 7, "response": "```json\n{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1089:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Tautology (Math)", "statement": "2 + 2 = 4.", "gloss": "G1", "rep": 8, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1090:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Tautology (Math)", "statement": "2 + 2 = 4.", "gloss": "G1", "rep": 9, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1091:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Tautology (Math)", "statement": "2 + 2 = 4.", "gloss": "G1", "rep": 0, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1092:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Tautology (Math)", "statement": "2 + 2 = 4.", "gloss": "G1", "rep": 1, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1093:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Tautology (Math)", "statement": "2 + 2 = 4.", "gloss": "G1", "rep": 2, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1094:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Tautology (Math)", "statement": "2 + 2 = 4.", "gloss": "G1", "rep": 3, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1095:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Tautology (Math)", "statement": "2 + 2 = 4.", "gloss": "G1", "rep": 4, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1096:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Tautology (Math)", "statement": "2 + 2 = 4.", "gloss": "G1", "rep": 5, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1097:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Tautology (Math)", "statement": "2 + 2 = 4.", "gloss": "G1", "rep": 6, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1098:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Tautology (Math)", "statement": "2 + 2 = 4.", "gloss": "G1", "rep": 7, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1099:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Tautology (Math)", "statement": "2 + 2 = 4.", "gloss": "G1", "rep": 8, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1100:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Tautology (Math)", "statement": "2 + 2 = 4.", "gloss": "G1", "rep": 9, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1101:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Tautology (Math)", "statement": "2 + 2 = 4.", "gloss": "G1", "rep": 0, "response": "{\"T\": 1.0, \"I\": 0.0, \"", "T": null, "I": null, "N": null, "F": null, "regime": null, "parsed": false, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1102:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Tautology (Math)", "statement": "2 + 2 = 4.", "gloss": "G1", "rep": 1, "response": "{\"T\": 1.0, \"I\": 0.0, \"", "T": null, "I": null, "N": null, "F": null, "regime": null, "parsed": false, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1103:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Tautology (Math)", "statement": "2 + 2 = 4.", "gloss": "G1", "rep": 2, "response": "{\"T\": 1.0, \"I\": 0.0, \"", "T": null, "I": null, "N": null, "F": null, "regime": null, "parsed": false, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1104:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Tautology (Math)", "statement": "2 + 2 = 4.", "gloss": "G1", "rep": 3, "response": "{\"T\": 1.0, \"I\": 0.0, \"", "T": null, "I": null, "N": null, "F": null, "regime": null, "parsed": false, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1105:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Tautology (Math)", "statement": "2 + 2 = 4.", "gloss": "G1", "rep": 4, "response": "{\"T\": 1.0, \"I\": 0.0, \"", "T": null, "I": null, "N": null, "F": null, "regime": null, "parsed": false, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1106:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Tautology (Math)", "statement": "2 + 2 = 4.", "gloss": "G1", "rep": 5, "response": "{\"T\": 1.0, \"I\": 0.0, \"", "T": null, "I": null, "N": null, "F": null, "regime": null, "parsed": false, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1107:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Tautology (Math)", "statement": "2 + 2 = 4.", "gloss": "G1", "rep": 6, "response": "{\"T\": 1.0, \"I\": 0.0, \"", "T": null, "I": null, "N": null, "F": null, "regime": null, "parsed": false, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1108:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Tautology (Math)", "statement": "2 + 2 = 4.", "gloss": "G1", "rep": 7, "response": "{\"T\": 1.0, \"I\": 0.0, \"", "T": null, "I": null, "N": null, "F": null, "regime": null, "parsed": false, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1109:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Tautology (Math)", "statement": "2 + 2 = 4.", "gloss": "G1", "rep": 8, "response": "{\"T\": 1.0, \"I\": 0.0, \"", "T": null, "I": null, "N": null, "F": null, "regime": null, "parsed": false, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1110:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Tautology (Math)", "statement": "2 + 2 = 4.", "gloss": "G1", "rep": 9, "response": "{\"T\": 1.0, \"I\": 0.0, \"", "T": null, "I": null, "N": null, "F": null, "regime": null, "parsed": false, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1111:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Tautology (Math)", "statement": "2 + 2 = 4.", "gloss": "G1", "rep": 0, "response": "```json\n{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1112:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Tautology (Math)", "statement": "2 + 2 = 4.", "gloss": "G1", "rep": 1, "response": "```json\n{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1113:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Tautology (Math)", "statement": "2 + 2 = 4.", "gloss": "G1", "rep": 2, "response": "```json\n{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1114:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Tautology (Math)", "statement": "2 + 2 = 4.", "gloss": "G1", "rep": 3, "response": "```json\n{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1115:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Tautology (Math)", "statement": "2 + 2 = 4.", "gloss": "G1", "rep": 4, "response": "```json\n{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1116:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Tautology (Math)", "statement": "2 + 2 = 4.", "gloss": "G1", "rep": 5, "response": "```json\n{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1117:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Tautology (Math)", "statement": "2 + 2 = 4.", "gloss": "G1", "rep": 6, "response": "```json\n{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1118:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Tautology (Math)", "statement": "2 + 2 = 4.", "gloss": "G1", "rep": 7, "response": "```json\n{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1119:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Tautology (Math)", "statement": "2 + 2 = 4.", "gloss": "G1", "rep": 8, "response": "```json\n{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1120:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Tautology (Math)", "statement": "2 + 2 = 4.", "gloss": "G1", "rep": 9, "response": "```json\n{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1121:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Tautology (Math)", "statement": "2 + 2 = 4.", "gloss": "G1", "rep": 0, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1122:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Tautology (Math)", "statement": "2 + 2 = 4.", "gloss": "G1", "rep": 1, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1123:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Tautology (Math)", "statement": "2 + 2 = 4.", "gloss": "G1", "rep": 2, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1124:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Tautology (Math)", "statement": "2 + 2 = 4.", "gloss": "G1", "rep": 3, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1125:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Tautology (Math)", "statement": "2 + 2 = 4.", "gloss": "G1", "rep": 4, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1126:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Tautology (Math)", "statement": "2 + 2 = 4.", "gloss": "G1", "rep": 5, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1127:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Tautology (Math)", "statement": "2 + 2 = 4.", "gloss": "G1", "rep": 6, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1128:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Tautology (Math)", "statement": "2 + 2 = 4.", "gloss": "G1", "rep": 7, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1129:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Tautology (Math)", "statement": "2 + 2 = 4.", "gloss": "G1", "rep": 8, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1130:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Tautology (Math)", "statement": "2 + 2 = 4.", "gloss": "G1", "rep": 9, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1131:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Tautology (Math)", "statement": "2 + 2 = 4.", "gloss": "G1", "rep": 0, "response": "```json\n{\n  \"T\": 1.0,\n  \"I\": 0.0,\n  \"N\": 0.0,\n  \"F\": 0.0\n}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1132:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Tautology (Math)", "statement": "2 + 2 = 4.", "gloss": "G1", "rep": 1, "response": "```json\n{\n  \"T\": 1.0,\n  \"I\": 0.0,\n  \"N\": 0.0,\n  \"F\": 0.0\n}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1133:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Tautology (Math)", "statement": "2 + 2 = 4.", "gloss": "G1", "rep": 2, "response": "```json\n{\n  \"T\": 1.0,\n  \"I\": 0.0,\n  \"N\": 0.0,\n  \"F\": 0.0\n}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1134:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Tautology (Math)", "statement": "2 + 2 = 4.", "gloss": "G1", "rep": 3, "response": "```json\n{\n  \"T\": 1.0,\n  \"I\": 0.0,\n  \"N\": 0.0,\n  \"F\": 0.0\n}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1135:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Tautology (Math)", "statement": "2 + 2 = 4.", "gloss": "G1", "rep": 4, "response": "```json\n{\n  \"T\": 1.0,\n  \"I\": 0.0,\n  \"N\": 0.0,\n  \"F\": 0.0\n}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1136:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Tautology (Math)", "statement": "2 + 2 = 4.", "gloss": "G1", "rep": 5, "response": "```json\n{\n  \"T\": 1.0,\n  \"I\": 0.0,\n  \"N\": 0.0,\n  \"F\": 0.0\n}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1137:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Tautology (Math)", "statement": "2 + 2 = 4.", "gloss": "G1", "rep": 6, "response": "```json\n{\n  \"T\": 1.0,\n  \"I\": 0.0,\n  \"N\": 0.0,\n  \"F\": 0.0\n}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1138:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Tautology (Math)", "statement": "2 + 2 = 4.", "gloss": "G1", "rep": 7, "response": "```json\n{\n  \"T\": 1.0,\n  \"I\": 0.0,\n  \"N\": 0.0,\n  \"F\": 0.0\n}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1139:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Tautology (Math)", "statement": "2 + 2 = 4.", "gloss": "G1", "rep": 8, "response": "```json\n{\n  \"T\": 1.0,\n  \"I\": 0.0,\n  \"N\": 0.0,\n  \"F\": 0.0\n}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1140:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Tautology (Math)", "statement": "2 + 2 = 4.", "gloss": "G1", "rep": 9, "response": "```json\n{\n  \"T\": 1.0,\n  \"I\": 0.0,\n  \"N\": 0.0,\n  \"F\": 0.0\n}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1141:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Tautology (Math)", "statement": "2 + 2 = 4.", "gloss": "G2", "rep": 0, "response": "```json\n{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1142:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Tautology (Math)", "statement": "2 + 2 = 4.", "gloss": "G2", "rep": 1, "response": "```json\n{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1143:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Tautology (Math)", "statement": "2 + 2 = 4.", "gloss": "G2", "rep": 2, "response": "```json\n{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1144:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Tautology (Math)", "statement": "2 + 2 = 4.", "gloss": "G2", "rep": 3, "response": "```json\n{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1145:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Tautology (Math)", "statement": "2 + 2 = 4.", "gloss": "G2", "rep": 4, "response": "```json\n{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1146:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Tautology (Math)", "statement": "2 + 2 = 4.", "gloss": "G2", "rep": 5, "response": "```json\n{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1147:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Tautology (Math)", "statement": "2 + 2 = 4.", "gloss": "G2", "rep": 6, "response": "```json\n{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1148:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Tautology (Math)", "statement": "2 + 2 = 4.", "gloss": "G2", "rep": 7, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1149:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Tautology (Math)", "statement": "2 + 2 = 4.", "gloss": "G2", "rep": 8, "response": "```json\n{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1150:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Tautology (Math)", "statement": "2 + 2 = 4.", "gloss": "G2", "rep": 9, "response": "```json\n{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1151:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Tautology (Math)", "statement": "2 + 2 = 4.", "gloss": "G2", "rep": 0, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1152:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Tautology (Math)", "statement": "2 + 2 = 4.", "gloss": "G2", "rep": 1, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1153:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Tautology (Math)", "statement": "2 + 2 = 4.", "gloss": "G2", "rep": 2, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1154:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Tautology (Math)", "statement": "2 + 2 = 4.", "gloss": "G2", "rep": 3, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1155:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Tautology (Math)", "statement": "2 + 2 = 4.", "gloss": "G2", "rep": 4, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1156:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Tautology (Math)", "statement": "2 + 2 = 4.", "gloss": "G2", "rep": 5, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1157:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Tautology (Math)", "statement": "2 + 2 = 4.", "gloss": "G2", "rep": 6, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1158:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Tautology (Math)", "statement": "2 + 2 = 4.", "gloss": "G2", "rep": 7, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1159:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Tautology (Math)", "statement": "2 + 2 = 4.", "gloss": "G2", "rep": 8, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1160:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Tautology (Math)", "statement": "2 + 2 = 4.", "gloss": "G2", "rep": 9, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1161:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Tautology (Math)", "statement": "2 + 2 = 4.", "gloss": "G2", "rep": 0, "response": "{\"T\": 1.0, \"I\": 0.0, \"", "T": null, "I": null, "N": null, "F": null, "regime": null, "parsed": false, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1162:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Tautology (Math)", "statement": "2 + 2 = 4.", "gloss": "G2", "rep": 1, "response": "{\"T\": 1.0, \"I\": 0.0, \"", "T": null, "I": null, "N": null, "F": null, "regime": null, "parsed": false, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1163:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Tautology (Math)", "statement": "2 + 2 = 4.", "gloss": "G2", "rep": 2, "response": "{\"T\": 1.0, \"I\": 0.0, \"", "T": null, "I": null, "N": null, "F": null, "regime": null, "parsed": false, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1164:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Tautology (Math)", "statement": "2 + 2 = 4.", "gloss": "G2", "rep": 3, "response": "{\"T\": 1.0, \"I\": 0.0, \"", "T": null, "I": null, "N": null, "F": null, "regime": null, "parsed": false, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1165:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Tautology (Math)", "statement": "2 + 2 = 4.", "gloss": "G2", "rep": 4, "response": "{\"T\": 1.0, \"I\": 0.0, \"", "T": null, "I": null, "N": null, "F": null, "regime": null, "parsed": false, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1166:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Tautology (Math)", "statement": "2 + 2 = 4.", "gloss": "G2", "rep": 5, "response": "{\"T\": 1.0, \"I\": 0.0, \"", "T": null, "I": null, "N": null, "F": null, "regime": null, "parsed": false, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1167:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Tautology (Math)", "statement": "2 + 2 = 4.", "gloss": "G2", "rep": 6, "response": "{\"T\": 1.0, \"I\": 0.0, \"", "T": null, "I": null, "N": null, "F": null, "regime": null, "parsed": false, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1168:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Tautology (Math)", "statement": "2 + 2 = 4.", "gloss": "G2", "rep": 7, "response": "{\"T\": 1.0, \"I\": 0.0, \"", "T": null, "I": null, "N": null, "F": null, "regime": null, "parsed": false, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1169:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Tautology (Math)", "statement": "2 + 2 = 4.", "gloss": "G2", "rep": 8, "response": "{\"T\": 1.0, \"I\": 0.0, \"", "T": null, "I": null, "N": null, "F": null, "regime": null, "parsed": false, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1170:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Tautology (Math)", "statement": "2 + 2 = 4.", "gloss": "G2", "rep": 9, "response": "{\"T\": 1.0, \"I\": 0.0, \"", "T": null, "I": null, "N": null, "F": null, "regime": null, "parsed": false, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1171:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Tautology (Math)", "statement": "2 + 2 = 4.", "gloss": "G2", "rep": 0, "response": "```json\n{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1172:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Tautology (Math)", "statement": "2 + 2 = 4.", "gloss": "G2", "rep": 1, "response": "```json\n{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1173:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Tautology (Math)", "statement": "2 + 2 = 4.", "gloss": "G2", "rep": 2, "response": "```json\n{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1174:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Tautology (Math)", "statement": "2 + 2 = 4.", "gloss": "G2", "rep": 3, "response": "```json\n{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1175:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Tautology (Math)", "statement": "2 + 2 = 4.", "gloss": "G2", "rep": 4, "response": "```json\n{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1176:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Tautology (Math)", "statement": "2 + 2 = 4.", "gloss": "G2", "rep": 5, "response": "```json\n{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1177:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Tautology (Math)", "statement": "2 + 2 = 4.", "gloss": "G2", "rep": 6, "response": "```json\n{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1178:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Tautology (Math)", "statement": "2 + 2 = 4.", "gloss": "G2", "rep": 7, "response": "```json\n{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1179:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Tautology (Math)", "statement": "2 + 2 = 4.", "gloss": "G2", "rep": 8, "response": "```json\n{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1180:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Tautology (Math)", "statement": "2 + 2 = 4.", "gloss": "G2", "rep": 9, "response": "```json\n{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1181:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Tautology (Math)", "statement": "2 + 2 = 4.", "gloss": "G2", "rep": 0, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1182:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Tautology (Math)", "statement": "2 + 2 = 4.", "gloss": "G2", "rep": 1, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1183:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Tautology (Math)", "statement": "2 + 2 = 4.", "gloss": "G2", "rep": 2, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1184:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Tautology (Math)", "statement": "2 + 2 = 4.", "gloss": "G2", "rep": 3, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1185:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Tautology (Math)", "statement": "2 + 2 = 4.", "gloss": "G2", "rep": 4, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1186:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Tautology (Math)", "statement": "2 + 2 = 4.", "gloss": "G2", "rep": 5, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1187:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Tautology (Math)", "statement": "2 + 2 = 4.", "gloss": "G2", "rep": 6, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1188:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Tautology (Math)", "statement": "2 + 2 = 4.", "gloss": "G2", "rep": 7, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1189:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Tautology (Math)", "statement": "2 + 2 = 4.", "gloss": "G2", "rep": 8, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1190:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Tautology (Math)", "statement": "2 + 2 = 4.", "gloss": "G2", "rep": 9, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1191:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Tautology (Math)", "statement": "2 + 2 = 4.", "gloss": "G2", "rep": 0, "response": "```json\n{\n  \"T\": 1.0,\n  \"I\": 0.0,\n  \"N\": 0.0,\n  \"F\": 0.0\n}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1192:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Tautology (Math)", "statement": "2 + 2 = 4.", "gloss": "G2", "rep": 1, "response": "```json\n{\n  \"T\": 1.0,\n  \"I\": 0.0,\n  \"N\": 0.0,\n  \"F\": 0.0\n}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1193:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Tautology (Math)", "statement": "2 + 2 = 4.", "gloss": "G2", "rep": 2, "response": "```json\n{\n  \"T\": 1.0,\n  \"I\": 0.0,\n  \"N\": 0.0,\n  \"F\": 0.0\n}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1194:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Tautology (Math)", "statement": "2 + 2 = 4.", "gloss": "G2", "rep": 3, "response": "```json\n{\n  \"T\": 1.0,\n  \"I\": 0.0,\n  \"N\": 0.0,\n  \"F\": 0.0\n}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1195:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Tautology (Math)", "statement": "2 + 2 = 4.", "gloss": "G2", "rep": 4, "response": "```json\n{\n  \"T\": 1.0,\n  \"I\": 0.0,\n  \"N\": 0.0,\n  \"F\": 0.0\n}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1196:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Tautology (Math)", "statement": "2 + 2 = 4.", "gloss": "G2", "rep": 5, "response": "```json\n{\n  \"T\": 1.0,\n  \"I\": 0.0,\n  \"N\": 0.0,\n  \"F\": 0.0\n}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1197:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Tautology (Math)", "statement": "2 + 2 = 4.", "gloss": "G2", "rep": 6, "response": "```json\n{\n  \"T\": 1.0,\n  \"I\": 0.0,\n  \"N\": 0.0,\n  \"F\": 0.0\n}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1198:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Tautology (Math)", "statement": "2 + 2 = 4.", "gloss": "G2", "rep": 7, "response": "```json\n{\n  \"T\": 1.0,\n  \"I\": 0.0,\n  \"N\": 0.0,\n  \"F\": 0.0\n}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1199:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Tautology (Math)", "statement": "2 + 2 = 4.", "gloss": "G2", "rep": 8, "response": "```json\n{\n  \"T\": 1.0,\n  \"I\": 0.0,\n  \"N\": 0.0,\n  \"F\": 0.0\n}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1200:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Tautology (Math)", "statement": "2 + 2 = 4.", "gloss": "G2", "rep": 9, "response": "```json\n{\n  \"T\": 1.0,\n  \"I\": 0.0,\n  \"N\": 0.0,\n  \"F\": 0.0\n}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1201:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Tautology (Math)", "statement": "2 + 2 = 4.", "gloss": "G3", "rep": 0, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1202:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Tautology (Math)", "statement": "2 + 2 = 4.", "gloss": "G3", "rep": 1, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1203:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Tautology (Math)", "statement": "2 + 2 = 4.", "gloss": "G3", "rep": 2, "response": "```json\n{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1204:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Tautology (Math)", "statement": "2 + 2 = 4.", "gloss": "G3", "rep": 3, "response": "```json\n{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1205:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Tautology (Math)", "statement": "2 + 2 = 4.", "gloss": "G3", "rep": 4, "response": "```json\n{\n  \"T\": 1.0,\n  \"I\": 0.0,\n  \"N\": 0.0,\n  \"F\": 0.0\n}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1206:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Tautology (Math)", "statement": "2 + 2 = 4.", "gloss": "G3", "rep": 5, "response": "```json\n{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1207:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Tautology (Math)", "statement": "2 + 2 = 4.", "gloss": "G3", "rep": 6, "response": "```json\n{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1208:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Tautology (Math)", "statement": "2 + 2 = 4.", "gloss": "G3", "rep": 7, "response": "```json\n{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1209:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Tautology (Math)", "statement": "2 + 2 = 4.", "gloss": "G3", "rep": 8, "response": "```json\n{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1210:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Tautology (Math)", "statement": "2 + 2 = 4.", "gloss": "G3", "rep": 9, "response": "```json\n{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1211:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Tautology (Math)", "statement": "2 + 2 = 4.", "gloss": "G3", "rep": 0, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1212:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Tautology (Math)", "statement": "2 + 2 = 4.", "gloss": "G3", "rep": 1, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1213:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Tautology (Math)", "statement": "2 + 2 = 4.", "gloss": "G3", "rep": 2, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1214:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Tautology (Math)", "statement": "2 + 2 = 4.", "gloss": "G3", "rep": 3, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1215:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Tautology (Math)", "statement": "2 + 2 = 4.", "gloss": "G3", "rep": 4, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1216:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Tautology (Math)", "statement": "2 + 2 = 4.", "gloss": "G3", "rep": 5, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1217:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Tautology (Math)", "statement": "2 + 2 = 4.", "gloss": "G3", "rep": 6, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1218:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Tautology (Math)", "statement": "2 + 2 = 4.", "gloss": "G3", "rep": 7, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1219:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Tautology (Math)", "statement": "2 + 2 = 4.", "gloss": "G3", "rep": 8, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1220:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Tautology (Math)", "statement": "2 + 2 = 4.", "gloss": "G3", "rep": 9, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1221:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Tautology (Math)", "statement": "2 + 2 = 4.", "gloss": "G3", "rep": 0, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1222:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Tautology (Math)", "statement": "2 + 2 = 4.", "gloss": "G3", "rep": 1, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1223:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Tautology (Math)", "statement": "2 + 2 = 4.", "gloss": "G3", "rep": 2, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1224:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Tautology (Math)", "statement": "2 + 2 = 4.", "gloss": "G3", "rep": 3, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1225:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Tautology (Math)", "statement": "2 + 2 = 4.", "gloss": "G3", "rep": 4, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1226:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Tautology (Math)", "statement": "2 + 2 = 4.", "gloss": "G3", "rep": 5, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1227:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Tautology (Math)", "statement": "2 + 2 = 4.", "gloss": "G3", "rep": 6, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1228:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Tautology (Math)", "statement": "2 + 2 = 4.", "gloss": "G3", "rep": 7, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1229:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Tautology (Math)", "statement": "2 + 2 = 4.", "gloss": "G3", "rep": 8, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1230:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Tautology (Math)", "statement": "2 + 2 = 4.", "gloss": "G3", "rep": 9, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1231:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Tautology (Math)", "statement": "2 + 2 = 4.", "gloss": "G3", "rep": 0, "response": "```json\n{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1232:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Tautology (Math)", "statement": "2 + 2 = 4.", "gloss": "G3", "rep": 1, "response": "```json\n{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1233:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Tautology (Math)", "statement": "2 + 2 = 4.", "gloss": "G3", "rep": 2, "response": "```json\n{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1234:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Tautology (Math)", "statement": "2 + 2 = 4.", "gloss": "G3", "rep": 3, "response": "```json\n{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1235:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Tautology (Math)", "statement": "2 + 2 = 4.", "gloss": "G3", "rep": 4, "response": "```json\n{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1236:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Tautology (Math)", "statement": "2 + 2 = 4.", "gloss": "G3", "rep": 5, "response": "```json\n{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1237:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Tautology (Math)", "statement": "2 + 2 = 4.", "gloss": "G3", "rep": 6, "response": "```json\n{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1238:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Tautology (Math)", "statement": "2 + 2 = 4.", "gloss": "G3", "rep": 7, "response": "```json\n{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1239:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Tautology (Math)", "statement": "2 + 2 = 4.", "gloss": "G3", "rep": 8, "response": "```json\n{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1240:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Tautology (Math)", "statement": "2 + 2 = 4.", "gloss": "G3", "rep": 9, "response": "```json\n{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1241:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Tautology (Math)", "statement": "2 + 2 = 4.", "gloss": "G3", "rep": 0, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1242:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Tautology (Math)", "statement": "2 + 2 = 4.", "gloss": "G3", "rep": 1, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1243:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Tautology (Math)", "statement": "2 + 2 = 4.", "gloss": "G3", "rep": 2, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1244:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Tautology (Math)", "statement": "2 + 2 = 4.", "gloss": "G3", "rep": 3, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1245:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Tautology (Math)", "statement": "2 + 2 = 4.", "gloss": "G3", "rep": 4, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1246:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Tautology (Math)", "statement": "2 + 2 = 4.", "gloss": "G3", "rep": 5, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1247:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Tautology (Math)", "statement": "2 + 2 = 4.", "gloss": "G3", "rep": 6, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1248:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Tautology (Math)", "statement": "2 + 2 = 4.", "gloss": "G3", "rep": 7, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1249:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Tautology (Math)", "statement": "2 + 2 = 4.", "gloss": "G3", "rep": 8, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1250:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Tautology (Math)", "statement": "2 + 2 = 4.", "gloss": "G3", "rep": 9, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1251:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Tautology (Math)", "statement": "2 + 2 = 4.", "gloss": "G3", "rep": 0, "response": "```json\n{\n  \"T\": 1.0,\n  \"I\": 0.0,\n  \"N\": 0.0,\n  \"F\": 0.0\n}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1252:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Tautology (Math)", "statement": "2 + 2 = 4.", "gloss": "G3", "rep": 1, "response": "```json\n{\n  \"T\": 1.0,\n  \"I\": 0.0,\n  \"N\": 0.0,\n  \"F\": 0.0\n}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1253:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Tautology (Math)", "statement": "2 + 2 = 4.", "gloss": "G3", "rep": 2, "response": "```json\n{\n  \"T\": 1.0,\n  \"I\": 0.0,\n  \"N\": 0.0,\n  \"F\": 0.0\n}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1254:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Tautology (Math)", "statement": "2 + 2 = 4.", "gloss": "G3", "rep": 3, "response": "```json\n{\n  \"T\": 1.0,\n  \"I\": 0.0,\n  \"N\": 0.0,\n  \"F\": 0.0\n}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1255:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Tautology (Math)", "statement": "2 + 2 = 4.", "gloss": "G3", "rep": 4, "response": "```json\n{\n  \"T\": 1.0,\n  \"I\": 0.0,\n  \"N\": 0.0,\n  \"F\": 0.0\n}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1256:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Tautology (Math)", "statement": "2 + 2 = 4.", "gloss": "G3", "rep": 5, "response": "```json\n{\n  \"T\": 1.0,\n  \"I\": 0.0,\n  \"N\": 0.0,\n  \"F\": 0.0\n}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1257:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Tautology (Math)", "statement": "2 + 2 = 4.", "gloss": "G3", "rep": 6, "response": "```json\n{\n  \"T\": 1.0,\n  \"I\": 0.0,\n  \"N\": 0.0,\n  \"F\": 0.0\n}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1258:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Tautology (Math)", "statement": "2 + 2 = 4.", "gloss": "G3", "rep": 7, "response": "```json\n{\n  \"T\": 1.0,\n  \"I\": 0.0,\n  \"N\": 0.0,\n  \"F\": 0.0\n}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1259:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Tautology (Math)", "statement": "2 + 2 = 4.", "gloss": "G3", "rep": 8, "response": "```json\n{\n  \"T\": 1.0,\n  \"I\": 0.0,\n  \"N\": 0.0,\n  \"F\": 0.0\n}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1260:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Tautology (Math)", "statement": "2 + 2 = 4.", "gloss": "G3", "rep": 9, "response": "```json\n{\n  \"T\": 1.0,\n  \"I\": 0.0,\n  \"N\": 0.0,\n  \"F\": 0.0\n}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1261:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Tautology (Definitional)", "statement": "All bachelors are unmarried.", "gloss": "G1", "rep": 0, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1262:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Tautology (Definitional)", "statement": "All bachelors are unmarried.", "gloss": "G1", "rep": 1, "response": "```json\n{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1263:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Tautology (Definitional)", "statement": "All bachelors are unmarried.", "gloss": "G1", "rep": 2, "response": "```json\n{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1264:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Tautology (Definitional)", "statement": "All bachelors are unmarried.", "gloss": "G1", "rep": 3, "response": "```json\n{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1265:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Tautology (Definitional)", "statement": "All bachelors are unmarried.", "gloss": "G1", "rep": 4, "response": "```json\n{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1266:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Tautology (Definitional)", "statement": "All bachelors are unmarried.", "gloss": "G1", "rep": 5, "response": "```json\n{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1267:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Tautology (Definitional)", "statement": "All bachelors are unmarried.", "gloss": "G1", "rep": 6, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1268:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Tautology (Definitional)", "statement": "All bachelors are unmarried.", "gloss": "G1", "rep": 7, "response": "```json\n{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1269:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Tautology (Definitional)", "statement": "All bachelors are unmarried.", "gloss": "G1", "rep": 8, "response": "```json\n{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1270:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Tautology (Definitional)", "statement": "All bachelors are unmarried.", "gloss": "G1", "rep": 9, "response": "```json\n{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1271:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Tautology (Definitional)", "statement": "All bachelors are unmarried.", "gloss": "G1", "rep": 0, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1272:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Tautology (Definitional)", "statement": "All bachelors are unmarried.", "gloss": "G1", "rep": 1, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1273:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Tautology (Definitional)", "statement": "All bachelors are unmarried.", "gloss": "G1", "rep": 2, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1274:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Tautology (Definitional)", "statement": "All bachelors are unmarried.", "gloss": "G1", "rep": 3, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1275:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Tautology (Definitional)", "statement": "All bachelors are unmarried.", "gloss": "G1", "rep": 4, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1276:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Tautology (Definitional)", "statement": "All bachelors are unmarried.", "gloss": "G1", "rep": 5, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1277:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Tautology (Definitional)", "statement": "All bachelors are unmarried.", "gloss": "G1", "rep": 6, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1278:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Tautology (Definitional)", "statement": "All bachelors are unmarried.", "gloss": "G1", "rep": 7, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1279:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Tautology (Definitional)", "statement": "All bachelors are unmarried.", "gloss": "G1", "rep": 8, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1280:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Tautology (Definitional)", "statement": "All bachelors are unmarried.", "gloss": "G1", "rep": 9, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1281:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Tautology (Definitional)", "statement": "All bachelors are unmarried.", "gloss": "G1", "rep": 0, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1282:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Tautology (Definitional)", "statement": "All bachelors are unmarried.", "gloss": "G1", "rep": 1, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1283:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Tautology (Definitional)", "statement": "All bachelors are unmarried.", "gloss": "G1", "rep": 2, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1284:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Tautology (Definitional)", "statement": "All bachelors are unmarried.", "gloss": "G1", "rep": 3, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1285:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Tautology (Definitional)", "statement": "All bachelors are unmarried.", "gloss": "G1", "rep": 4, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1286:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Tautology (Definitional)", "statement": "All bachelors are unmarried.", "gloss": "G1", "rep": 5, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1287:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Tautology (Definitional)", "statement": "All bachelors are unmarried.", "gloss": "G1", "rep": 6, "response": "{\"T\": 0.9, \"I\": 0.05, \"N\": 0.0, \"F\": 0.05}", "T": 0.9, "I": 0.05, "N": 0.0, "F": 0.05, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1288:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Tautology (Definitional)", "statement": "All bachelors are unmarried.", "gloss": "G1", "rep": 7, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1289:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Tautology (Definitional)", "statement": "All bachelors are unmarried.", "gloss": "G1", "rep": 8, "response": "{\"T\": 0.9, \"I\": 0.05, \"N\": 0.0, \"F\": 0.05}", "T": 0.9, "I": 0.05, "N": 0.0, "F": 0.05, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1290:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Tautology (Definitional)", "statement": "All bachelors are unmarried.", "gloss": "G1", "rep": 9, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1291:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Tautology (Definitional)", "statement": "All bachelors are unmarried.", "gloss": "G1", "rep": 0, "response": "```json\n{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1292:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Tautology (Definitional)", "statement": "All bachelors are unmarried.", "gloss": "G1", "rep": 1, "response": "```json\n{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1293:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Tautology (Definitional)", "statement": "All bachelors are unmarried.", "gloss": "G1", "rep": 2, "response": "```json\n{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1294:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Tautology (Definitional)", "statement": "All bachelors are unmarried.", "gloss": "G1", "rep": 3, "response": "```json\n{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1295:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Tautology (Definitional)", "statement": "All bachelors are unmarried.", "gloss": "G1", "rep": 4, "response": "```json\n{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1296:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Tautology (Definitional)", "statement": "All bachelors are unmarried.", "gloss": "G1", "rep": 5, "response": "```json\n{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1297:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Tautology (Definitional)", "statement": "All bachelors are unmarried.", "gloss": "G1", "rep": 6, "response": "```json\n{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1298:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Tautology (Definitional)", "statement": "All bachelors are unmarried.", "gloss": "G1", "rep": 7, "response": "```json\n{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1299:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Tautology (Definitional)", "statement": "All bachelors are unmarried.", "gloss": "G1", "rep": 8, "response": "```json\n{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1300:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Tautology (Definitional)", "statement": "All bachelors are unmarried.", "gloss": "G1", "rep": 9, "response": "```json\n{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1301:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Tautology (Definitional)", "statement": "All bachelors are unmarried.", "gloss": "G1", "rep": 0, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1302:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Tautology (Definitional)", "statement": "All bachelors are unmarried.", "gloss": "G1", "rep": 1, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1303:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Tautology (Definitional)", "statement": "All bachelors are unmarried.", "gloss": "G1", "rep": 2, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1304:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Tautology (Definitional)", "statement": "All bachelors are unmarried.", "gloss": "G1", "rep": 3, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1305:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Tautology (Definitional)", "statement": "All bachelors are unmarried.", "gloss": "G1", "rep": 4, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1306:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Tautology (Definitional)", "statement": "All bachelors are unmarried.", "gloss": "G1", "rep": 5, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1307:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Tautology (Definitional)", "statement": "All bachelors are unmarried.", "gloss": "G1", "rep": 6, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1308:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Tautology (Definitional)", "statement": "All bachelors are unmarried.", "gloss": "G1", "rep": 7, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1309:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Tautology (Definitional)", "statement": "All bachelors are unmarried.", "gloss": "G1", "rep": 8, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1310:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Tautology (Definitional)", "statement": "All bachelors are unmarried.", "gloss": "G1", "rep": 9, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1311:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Tautology (Definitional)", "statement": "All bachelors are unmarried.", "gloss": "G1", "rep": 0, "response": "```json\n{\n  \"T\": 0.99,\n  \"I\": 0.01,\n  \"N\": 0.05,\n  \"F\": 0.0\n}\n```", "T": 0.99, "I": 0.01, "N": 0.05, "F": 0.0, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1312:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Tautology (Definitional)", "statement": "All bachelors are unmarried.", "gloss": "G1", "rep": 1, "response": "```json\n{\n  \"T\": 0.99,\n  \"I\": 0.01,\n  \"N\": 0.0,\n  \"F\": 0.0\n}\n```", "T": 0.99, "I": 0.01, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1313:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Tautology (Definitional)", "statement": "All bachelors are unmarried.", "gloss": "G1", "rep": 2, "response": "```json\n{\n  \"T\": 0.98,\n  \"I\": 0.02,\n  \"N\": 0.0,\n  \"F\": 0.0\n}\n```", "T": 0.98, "I": 0.02, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1314:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Tautology (Definitional)", "statement": "All bachelors are unmarried.", "gloss": "G1", "rep": 3, "response": "```json\n{\n  \"T\": 0.98,\n  \"I\": 0.01,\n  \"N\": 0.01,\n  \"F\": 0.02\n}\n```", "T": 0.98, "I": 0.01, "N": 0.01, "F": 0.02, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1315:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Tautology (Definitional)", "statement": "All bachelors are unmarried.", "gloss": "G1", "rep": 4, "response": "```json\n{\n  \"T\": 0.99,\n  \"I\": 0.01,\n  \"N\": 0.05,\n  \"F\": 0.0\n}\n```", "T": 0.99, "I": 0.01, "N": 0.05, "F": 0.0, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1316:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Tautology (Definitional)", "statement": "All bachelors are unmarried.", "gloss": "G1", "rep": 5, "response": "```json\n{\n  \"T\": 0.98,\n  \"I\": 0.01,\n  \"N\": 0.01,\n  \"F\": 0.02\n}\n```", "T": 0.98, "I": 0.01, "N": 0.01, "F": 0.02, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1317:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Tautology (Definitional)", "statement": "All bachelors are unmarried.", "gloss": "G1", "rep": 6, "response": "```json\n{\n  \"T\": 0.99,\n  \"I\": 0.01,\n  \"N\": 0.05,\n  \"F\": 0.0\n}\n```", "T": 0.99, "I": 0.01, "N": 0.05, "F": 0.0, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1318:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Tautology (Definitional)", "statement": "All bachelors are unmarried.", "gloss": "G1", "rep": 7, "response": "```json\n{\n  \"T\": 0.99,\n  \"I\": 0.01,\n  \"N\": 0.01,\n  \"F\": 0.0\n}\n```", "T": 0.99, "I": 0.01, "N": 0.01, "F": 0.0, "regime": "very_weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1319:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Tautology (Definitional)", "statement": "All bachelors are unmarried.", "gloss": "G1", "rep": 8, "response": "```json\n{\n  \"T\": 0.99,\n  \"I\": 0.01,\n  \"N\": 0.05,\n  \"F\": 0.0\n}\n```", "T": 0.99, "I": 0.01, "N": 0.05, "F": 0.0, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1320:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Tautology (Definitional)", "statement": "All bachelors are unmarried.", "gloss": "G1", "rep": 9, "response": "```json\n{\n  \"T\": 0.99,\n  \"I\": 0.01,\n  \"N\": 0.05,\n  \"F\": 0.0\n}\n```", "T": 0.99, "I": 0.01, "N": 0.05, "F": 0.0, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1321:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Tautology (Definitional)", "statement": "All bachelors are unmarried.", "gloss": "G2", "rep": 0, "response": "```json\n{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1322:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Tautology (Definitional)", "statement": "All bachelors are unmarried.", "gloss": "G2", "rep": 1, "response": "```json\n{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1323:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Tautology (Definitional)", "statement": "All bachelors are unmarried.", "gloss": "G2", "rep": 2, "response": "```json\n{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1324:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Tautology (Definitional)", "statement": "All bachelors are unmarried.", "gloss": "G2", "rep": 3, "response": "```json\n{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1325:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Tautology (Definitional)", "statement": "All bachelors are unmarried.", "gloss": "G2", "rep": 4, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1326:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Tautology (Definitional)", "statement": "All bachelors are unmarried.", "gloss": "G2", "rep": 5, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1327:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Tautology (Definitional)", "statement": "All bachelors are unmarried.", "gloss": "G2", "rep": 6, "response": "```json\n{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1328:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Tautology (Definitional)", "statement": "All bachelors are unmarried.", "gloss": "G2", "rep": 7, "response": "```json\n{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1329:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Tautology (Definitional)", "statement": "All bachelors are unmarried.", "gloss": "G2", "rep": 8, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1330:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Tautology (Definitional)", "statement": "All bachelors are unmarried.", "gloss": "G2", "rep": 9, "response": "```json\n{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1331:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Tautology (Definitional)", "statement": "All bachelors are unmarried.", "gloss": "G2", "rep": 0, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1332:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Tautology (Definitional)", "statement": "All bachelors are unmarried.", "gloss": "G2", "rep": 1, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1333:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Tautology (Definitional)", "statement": "All bachelors are unmarried.", "gloss": "G2", "rep": 2, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1334:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Tautology (Definitional)", "statement": "All bachelors are unmarried.", "gloss": "G2", "rep": 3, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1335:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Tautology (Definitional)", "statement": "All bachelors are unmarried.", "gloss": "G2", "rep": 4, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1336:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Tautology (Definitional)", "statement": "All bachelors are unmarried.", "gloss": "G2", "rep": 5, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1337:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Tautology (Definitional)", "statement": "All bachelors are unmarried.", "gloss": "G2", "rep": 6, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1338:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Tautology (Definitional)", "statement": "All bachelors are unmarried.", "gloss": "G2", "rep": 7, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1339:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Tautology (Definitional)", "statement": "All bachelors are unmarried.", "gloss": "G2", "rep": 8, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1340:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Tautology (Definitional)", "statement": "All bachelors are unmarried.", "gloss": "G2", "rep": 9, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1341:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Tautology (Definitional)", "statement": "All bachelors are unmarried.", "gloss": "G2", "rep": 0, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1342:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Tautology (Definitional)", "statement": "All bachelors are unmarried.", "gloss": "G2", "rep": 1, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1343:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Tautology (Definitional)", "statement": "All bachelors are unmarried.", "gloss": "G2", "rep": 2, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1344:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Tautology (Definitional)", "statement": "All bachelors are unmarried.", "gloss": "G2", "rep": 3, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1345:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Tautology (Definitional)", "statement": "All bachelors are unmarried.", "gloss": "G2", "rep": 4, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1346:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Tautology (Definitional)", "statement": "All bachelors are unmarried.", "gloss": "G2", "rep": 5, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1347:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Tautology (Definitional)", "statement": "All bachelors are unmarried.", "gloss": "G2", "rep": 6, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1348:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Tautology (Definitional)", "statement": "All bachelors are unmarried.", "gloss": "G2", "rep": 7, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1349:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Tautology (Definitional)", "statement": "All bachelors are unmarried.", "gloss": "G2", "rep": 8, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1350:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Tautology (Definitional)", "statement": "All bachelors are unmarried.", "gloss": "G2", "rep": 9, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1351:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Tautology (Definitional)", "statement": "All bachelors are unmarried.", "gloss": "G2", "rep": 0, "response": "```json\n{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1352:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Tautology (Definitional)", "statement": "All bachelors are unmarried.", "gloss": "G2", "rep": 1, "response": "```json\n{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1353:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Tautology (Definitional)", "statement": "All bachelors are unmarried.", "gloss": "G2", "rep": 2, "response": "```json\n{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1354:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Tautology (Definitional)", "statement": "All bachelors are unmarried.", "gloss": "G2", "rep": 3, "response": "```json\n{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1355:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Tautology (Definitional)", "statement": "All bachelors are unmarried.", "gloss": "G2", "rep": 4, "response": "```json\n{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1356:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Tautology (Definitional)", "statement": "All bachelors are unmarried.", "gloss": "G2", "rep": 5, "response": "```json\n{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1357:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Tautology (Definitional)", "statement": "All bachelors are unmarried.", "gloss": "G2", "rep": 6, "response": "```json\n{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1358:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Tautology (Definitional)", "statement": "All bachelors are unmarried.", "gloss": "G2", "rep": 7, "response": "```json\n{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1359:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Tautology (Definitional)", "statement": "All bachelors are unmarried.", "gloss": "G2", "rep": 8, "response": "```json\n{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1360:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Tautology (Definitional)", "statement": "All bachelors are unmarried.", "gloss": "G2", "rep": 9, "response": "```json\n{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1361:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Tautology (Definitional)", "statement": "All bachelors are unmarried.", "gloss": "G2", "rep": 0, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1362:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Tautology (Definitional)", "statement": "All bachelors are unmarried.", "gloss": "G2", "rep": 1, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1363:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Tautology (Definitional)", "statement": "All bachelors are unmarried.", "gloss": "G2", "rep": 2, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1364:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Tautology (Definitional)", "statement": "All bachelors are unmarried.", "gloss": "G2", "rep": 3, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1365:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Tautology (Definitional)", "statement": "All bachelors are unmarried.", "gloss": "G2", "rep": 4, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1366:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Tautology (Definitional)", "statement": "All bachelors are unmarried.", "gloss": "G2", "rep": 5, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1367:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Tautology (Definitional)", "statement": "All bachelors are unmarried.", "gloss": "G2", "rep": 6, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1368:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Tautology (Definitional)", "statement": "All bachelors are unmarried.", "gloss": "G2", "rep": 7, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1369:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Tautology (Definitional)", "statement": "All bachelors are unmarried.", "gloss": "G2", "rep": 8, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1370:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Tautology (Definitional)", "statement": "All bachelors are unmarried.", "gloss": "G2", "rep": 9, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1371:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Tautology (Definitional)", "statement": "All bachelors are unmarried.", "gloss": "G2", "rep": 0, "response": "```json\n{\n  \"T\": 0.99,\n  \"I\": 0.01,\n  \"N\": 0.0,\n  \"F\": 0.0\n}\n```", "T": 0.99, "I": 0.01, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1372:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Tautology (Definitional)", "statement": "All bachelors are unmarried.", "gloss": "G2", "rep": 1, "response": "```json\n{\n  \"T\": 0.99,\n  \"I\": 0.01,\n  \"N\": 0.0,\n  \"F\": 0.0\n}\n```", "T": 0.99, "I": 0.01, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1373:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Tautology (Definitional)", "statement": "All bachelors are unmarried.", "gloss": "G2", "rep": 2, "response": "```json\n{\n  \"T\": 0.99,\n  \"I\": 0.01,\n  \"N\": 0.0,\n  \"F\": 0.0\n}\n```", "T": 0.99, "I": 0.01, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1374:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Tautology (Definitional)", "statement": "All bachelors are unmarried.", "gloss": "G2", "rep": 3, "response": "```json\n{\n  \"T\": 0.98,\n  \"I\": 0.01,\n  \"N\": 0.02,\n  \"F\": 0.01\n}\n```", "T": 0.98, "I": 0.01, "N": 0.02, "F": 0.01, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1375:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Tautology (Definitional)", "statement": "All bachelors are unmarried.", "gloss": "G2", "rep": 4, "response": "```json\n{\n  \"T\": 0.99,\n  \"I\": 0.01,\n  \"N\": 0.0,\n  \"F\": 0.0\n}\n```", "T": 0.99, "I": 0.01, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1376:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Tautology (Definitional)", "statement": "All bachelors are unmarried.", "gloss": "G2", "rep": 5, "response": "```json\n{\n  \"T\": 0.99,\n  \"I\": 0.01,\n  \"N\": 0.0,\n  \"F\": 0.0\n}\n```", "T": 0.99, "I": 0.01, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1377:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Tautology (Definitional)", "statement": "All bachelors are unmarried.", "gloss": "G2", "rep": 6, "response": "```json\n{\n  \"T\": 0.99,\n  \"I\": 0.01,\n  \"N\": 0.0,\n  \"F\": 0.0\n}\n```", "T": 0.99, "I": 0.01, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1378:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Tautology (Definitional)", "statement": "All bachelors are unmarried.", "gloss": "G2", "rep": 7, "response": "```json\n{\n  \"T\": 0.99,\n  \"I\": 0.01,\n  \"N\": 0.0,\n  \"F\": 0.0\n}\n```", "T": 0.99, "I": 0.01, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1379:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Tautology (Definitional)", "statement": "All bachelors are unmarried.", "gloss": "G2", "rep": 8, "response": "```json\n{\n  \"T\": 0.99,\n  \"I\": 0.01,\n  \"N\": 0.0,\n  \"F\": 0.0\n}\n```", "T": 0.99, "I": 0.01, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1380:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Tautology (Definitional)", "statement": "All bachelors are unmarried.", "gloss": "G2", "rep": 9, "response": "```json\n{\n  \"T\": 0.99,\n  \"I\": 0.01,\n  \"N\": 0.0,\n  \"F\": 0.0\n}\n```", "T": 0.99, "I": 0.01, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1381:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Tautology (Definitional)", "statement": "All bachelors are unmarried.", "gloss": "G3", "rep": 0, "response": "```json\n{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1382:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Tautology (Definitional)", "statement": "All bachelors are unmarried.", "gloss": "G3", "rep": 1, "response": "```json\n{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1383:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Tautology (Definitional)", "statement": "All bachelors are unmarried.", "gloss": "G3", "rep": 2, "response": "```json\n{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1384:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Tautology (Definitional)", "statement": "All bachelors are unmarried.", "gloss": "G3", "rep": 3, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1385:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Tautology (Definitional)", "statement": "All bachelors are unmarried.", "gloss": "G3", "rep": 4, "response": "```json\n{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1386:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Tautology (Definitional)", "statement": "All bachelors are unmarried.", "gloss": "G3", "rep": 5, "response": "```json\n{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1387:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Tautology (Definitional)", "statement": "All bachelors are unmarried.", "gloss": "G3", "rep": 6, "response": "```json\n{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1388:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Tautology (Definitional)", "statement": "All bachelors are unmarried.", "gloss": "G3", "rep": 7, "response": "```json\n{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1389:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Tautology (Definitional)", "statement": "All bachelors are unmarried.", "gloss": "G3", "rep": 8, "response": "```json\n{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1390:{"model": "gpt-4o", "vendor": "openai", "model_id": "openai/gpt-4o", "phenomenon": "Tautology (Definitional)", "statement": "All bachelors are unmarried.", "gloss": "G3", "rep": 9, "response": "```json\n{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1391:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Tautology (Definitional)", "statement": "All bachelors are unmarried.", "gloss": "G3", "rep": 0, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1392:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Tautology (Definitional)", "statement": "All bachelors are unmarried.", "gloss": "G3", "rep": 1, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1393:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Tautology (Definitional)", "statement": "All bachelors are unmarried.", "gloss": "G3", "rep": 2, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1394:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Tautology (Definitional)", "statement": "All bachelors are unmarried.", "gloss": "G3", "rep": 3, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1395:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Tautology (Definitional)", "statement": "All bachelors are unmarried.", "gloss": "G3", "rep": 4, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1396:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Tautology (Definitional)", "statement": "All bachelors are unmarried.", "gloss": "G3", "rep": 5, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1397:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Tautology (Definitional)", "statement": "All bachelors are unmarried.", "gloss": "G3", "rep": 6, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1398:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Tautology (Definitional)", "statement": "All bachelors are unmarried.", "gloss": "G3", "rep": 7, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1399:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Tautology (Definitional)", "statement": "All bachelors are unmarried.", "gloss": "G3", "rep": 8, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1400:{"model": "claude-sonnet-4", "vendor": "anthropic", "model_id": "anthropic/claude-sonnet-4", "phenomenon": "Tautology (Definitional)", "statement": "All bachelors are unmarried.", "gloss": "G3", "rep": 9, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1401:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Tautology (Definitional)", "statement": "All bachelors are unmarried.", "gloss": "G3", "rep": 0, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1402:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Tautology (Definitional)", "statement": "All bachelors are unmarried.", "gloss": "G3", "rep": 1, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1403:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Tautology (Definitional)", "statement": "All bachelors are unmarried.", "gloss": "G3", "rep": 2, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1404:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Tautology (Definitional)", "statement": "All bachelors are unmarried.", "gloss": "G3", "rep": 3, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1405:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Tautology (Definitional)", "statement": "All bachelors are unmarried.", "gloss": "G3", "rep": 4, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1406:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Tautology (Definitional)", "statement": "All bachelors are unmarried.", "gloss": "G3", "rep": 5, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1407:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Tautology (Definitional)", "statement": "All bachelors are unmarried.", "gloss": "G3", "rep": 6, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1408:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Tautology (Definitional)", "statement": "All bachelors are unmarried.", "gloss": "G3", "rep": 7, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1409:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Tautology (Definitional)", "statement": "All bachelors are unmarried.", "gloss": "G3", "rep": 8, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1410:{"model": "llama-4-maverick", "vendor": "meta", "model_id": "meta-llama/llama-4-maverick", "phenomenon": "Tautology (Definitional)", "statement": "All bachelors are unmarried.", "gloss": "G3", "rep": 9, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1411:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Tautology (Definitional)", "statement": "All bachelors are unmarried.", "gloss": "G3", "rep": 0, "response": "```json\n{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1412:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Tautology (Definitional)", "statement": "All bachelors are unmarried.", "gloss": "G3", "rep": 1, "response": "```json\n{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1413:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Tautology (Definitional)", "statement": "All bachelors are unmarried.", "gloss": "G3", "rep": 2, "response": "```json\n{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1414:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Tautology (Definitional)", "statement": "All bachelors are unmarried.", "gloss": "G3", "rep": 3, "response": "```json\n{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1415:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Tautology (Definitional)", "statement": "All bachelors are unmarried.", "gloss": "G3", "rep": 4, "response": "```json\n{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1416:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Tautology (Definitional)", "statement": "All bachelors are unmarried.", "gloss": "G3", "rep": 5, "response": "```json\n{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1417:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Tautology (Definitional)", "statement": "All bachelors are unmarried.", "gloss": "G3", "rep": 6, "response": "```json\n{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1418:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Tautology (Definitional)", "statement": "All bachelors are unmarried.", "gloss": "G3", "rep": 7, "response": "```json\n{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1419:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Tautology (Definitional)", "statement": "All bachelors are unmarried.", "gloss": "G3", "rep": 8, "response": "```json\n{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}\n```", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1420:{"model": "deepseek-chat", "vendor": "deepseek", "model_id": "deepseek/deepseek-chat", "phenomenon": "Tautology (Definitional)", "statement": "All bachelors are unmarried.", "gloss": "G3", "rep": 9, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1421:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Tautology (Definitional)", "statement": "All bachelors are unmarried.", "gloss": "G3", "rep": 0, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1422:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Tautology (Definitional)", "statement": "All bachelors are unmarried.", "gloss": "G3", "rep": 1, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1423:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Tautology (Definitional)", "statement": "All bachelors are unmarried.", "gloss": "G3", "rep": 2, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1424:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Tautology (Definitional)", "statement": "All bachelors are unmarried.", "gloss": "G3", "rep": 3, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1425:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Tautology (Definitional)", "statement": "All bachelors are unmarried.", "gloss": "G3", "rep": 4, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1426:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Tautology (Definitional)", "statement": "All bachelors are unmarried.", "gloss": "G3", "rep": 5, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1427:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Tautology (Definitional)", "statement": "All bachelors are unmarried.", "gloss": "G3", "rep": 6, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1428:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Tautology (Definitional)", "statement": "All bachelors are unmarried.", "gloss": "G3", "rep": 7, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1429:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Tautology (Definitional)", "statement": "All bachelors are unmarried.", "gloss": "G3", "rep": 8, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1430:{"model": "qwen3-235b", "vendor": "alibaba", "model_id": "qwen/qwen3-235b-a22b-2507", "phenomenon": "Tautology (Definitional)", "statement": "All bachelors are unmarried.", "gloss": "G3", "rep": 9, "response": "{\"T\": 1.0, \"I\": 0.0, \"N\": 0.0, \"F\": 0.0}", "T": 1.0, "I": 0.0, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1431:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Tautology (Definitional)", "statement": "All bachelors are unmarried.", "gloss": "G3", "rep": 0, "response": "```json\n{\n  \"T\": 0.98,\n  \"I\": 0.01,\n  \"N\": 0.005,\n  \"F\": 0.005\n}\n```", "T": 0.98, "I": 0.01, "N": 0.005, "F": 0.005, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1432:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Tautology (Definitional)", "statement": "All bachelors are unmarried.", "gloss": "G3", "rep": 1, "response": "```json\n{\n  \"T\": 0.99,\n  \"I\": 0.01,\n  \"N\": 0.0,\n  \"F\": 0.0\n}\n```", "T": 0.99, "I": 0.01, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1433:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Tautology (Definitional)", "statement": "All bachelors are unmarried.", "gloss": "G3", "rep": 2, "response": "```json\n{\n  \"T\": 0.98,\n  \"I\": 0.01,\n  \"N\": 0.01,\n  \"F\": 0.0\n}\n```", "T": 0.98, "I": 0.01, "N": 0.01, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1434:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Tautology (Definitional)", "statement": "All bachelors are unmarried.", "gloss": "G3", "rep": 3, "response": "```json\n{\n  \"T\": 0.99,\n  \"I\": 0.01,\n  \"N\": 0.0,\n  \"F\": 0.0\n}\n```", "T": 0.99, "I": 0.01, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1435:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Tautology (Definitional)", "statement": "All bachelors are unmarried.", "gloss": "G3", "rep": 4, "response": "```json\n{\n  \"T\": 0.98,\n  \"I\": 0.01,\n  \"N\": 0.02,\n  \"F\": 0.01\n}\n```", "T": 0.98, "I": 0.01, "N": 0.02, "F": 0.01, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1436:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Tautology (Definitional)", "statement": "All bachelors are unmarried.", "gloss": "G3", "rep": 5, "response": "```json\n{\n  \"T\": 0.95,\n  \"I\": 0.01,\n  \"N\": 0.05,\n  \"F\": 0.0\n}\n```", "T": 0.95, "I": 0.01, "N": 0.05, "F": 0.0, "regime": "very_weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1437:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Tautology (Definitional)", "statement": "All bachelors are unmarried.", "gloss": "G3", "rep": 6, "response": "```json\n{\n  \"T\": 0.99,\n  \"I\": 0.01,\n  \"N\": 0.0,\n  \"F\": 0.0\n}\n```", "T": 0.99, "I": 0.01, "N": 0.0, "F": 0.0, "regime": "classical", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1438:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Tautology (Definitional)", "statement": "All bachelors are unmarried.", "gloss": "G3", "rep": 7, "response": "```json\n{\n  \"T\": 0.98,\n  \"I\": 0.02,\n  \"N\": 0.01,\n  \"F\": 0.01\n}\n```", "T": 0.98, "I": 0.02, "N": 0.01, "F": 0.01, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1439:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Tautology (Definitional)", "statement": "All bachelors are unmarried.", "gloss": "G3", "rep": 8, "response": "```json\n{\n  \"T\": 0.98,\n  \"I\": 0.01,\n  \"N\": 0.02,\n  \"F\": 0.01\n}\n```", "T": 0.98, "I": 0.01, "N": 0.02, "F": 0.01, "regime": "weak", "parsed": true, "error": false}
family1\results\raw_quadruple_pilot.jsonl:1440:{"model": "mistral-medium-3.1", "vendor": "mistral", "model_id": "mistralai/mistral-medium-3.1", "phenomenon": "Tautology (Definitional)", "statement": "All bachelors are unmarried.", "gloss": "G3", "rep": 9, "response": "```json\n{\n  \"T\": 0.98,\n  \"I\": 0.01,\n  \"N\": 0.05,\n  \"F\": 0.01\n}\n```", "T": 0.98, "I": 0.01, "N": 0.05, "F": 0.01, "regime": "weak", "parsed": true, "error": false}

 succeeded in 9775ms:
{"model": "gpt-4o", "vendor": "openai", "item_id": "ethi-01-bare", "pair": "ethi-01", "phenomenon": "ethical", "form": "bare", "statement": "Lying to protect a refugee from deportation is morally permissible.", "gloss": "G1", "response": "```json\n{\"T\": 0.7, \"I\": 0.4, \"N\": 0.3, \"F\": 0.3}\n```", "T": 0.7, "I": 0.4, "N": 0.3, "F": 0.3, "rung": "weak", "parsed": true, "error": false}

 succeeded in 10369ms:
{"condition": "full", "model": "gpt-4o", "vendor": "openai", "item_id": "wkt-01", "construct": "wellknown_true", "is_anchor": false, "truth": true, "statement": "Water freezes at zero degrees Celsius at sea-level pressure.", "wording": "W1", "response": "{\"confidence\": 1.0}", "confidence": 1.0, "parsed": true, "error": false}

 succeeded in 9624ms:
{"model": "gpt-4o", "vendor": "openai", "item_id": "ethi-01-bare", "pair": "ethi-01", "phenomenon": "ethical", "form": "bare", "statement": "Lying to protect a refugee from deportation is morally permissible.", "rep": 0, "response": "```json\n{\"T\": 0.7, \"I\": 0.5, \"F\": 0.3}\n```", "T": 0.7, "I": 0.5, "F": 0.3, "strong": 0, "parsed": true, "error": false}

codex
One of the earlier file-preview commands is still open even though the other previews returned. I’m polling it now so there is no dangling process before I continue.
exec
"C:\\WINDOWS\\System32\\WindowsPowerShell\\v1.0\\powershell.exe" -Command '$code = @'"'
import json, pathlib
for p in sorted(pathlib.Path('.').glob('family*/results/raw*.jsonl')):
    first = next(l for l in p.read_text(encoding='utf-8').splitlines() if l.strip())
    keys = sorted(json.loads(first).keys())
    print(str(p), keys)
'@
python -c "'$code' in C:\Users\HP\Documents\MeasurementScience_Evals\paper11_elicitation_method
 succeeded in 7341ms:
family1\results\raw_bank.jsonl ['F', 'I', 'T', 'error', 'form', 'item_id', 'model', 'pair', 'parsed', 'phenomenon', 'rep', 'response', 'statement', 'strong', 'vendor']
family1\results\raw_neutral_system.jsonl ['F', 'I', 'N', 'T', 'error', 'form', 'gloss', 'item_id', 'model', 'pair', 'parsed', 'phenomenon', 'response', 'rung', 'statement', 'system', 'vendor']
family1\results\raw_nolicense_system.jsonl ['F', 'I', 'N', 'T', 'error', 'form', 'gloss', 'item_id', 'model', 'pair', 'parsed', 'phenomenon', 'response', 'rung', 'statement', 'system', 'vendor']
family1\results\raw_quad_bank.jsonl ['F', 'I', 'N', 'T', 'error', 'form', 'gloss', 'item_id', 'model', 'pair', 'parsed', 'phenomenon', 'response', 'rung', 'statement', 'vendor']
family1\results\raw_quadruple_pilot.jsonl ['F', 'I', 'N', 'T', 'error', 'gloss', 'model', 'model_id', 'parsed', 'phenomenon', 'regime', 'rep', 'response', 'statement', 'vendor']
family2\results\raw_factual_full.jsonl ['condition', 'confidence', 'construct', 'error', 'is_anchor', 'item_id', 'model', 'parsed', 'response', 'statement', 'truth', 'vendor', 'wording']
family2\results\raw_factual_neutral.jsonl ['condition', 'confidence', 'construct', 'error', 'is_anchor', 'item_id', 'model', 'parsed', 'response', 'statement', 'truth', 'vendor', 'wording']
family2\results\raw_factual_nolicense.jsonl ['condition', 'confidence', 'construct', 'error', 'is_anchor', 'item_id', 'model', 'parsed', 'response', 'statement', 'truth', 'vendor', 'wording']

codex
Another figure-level defect surfaced: the code that builds `figC_threshold.pdf` hard-codes “83% of answers are multiples of 0.10”, while the analysis script and manuscript prose report 86.4%. That is a quantitative mismatch in the compiled figure, not just a comment.
exec
"C:\\WINDOWS\\System32\\WindowsPowerShell\\v1.0\\powershell.exe" -Command "rg -n \"83%|86\\.4|95\\.7|37\\.9|0\\.10|0\\.05|0\\.60|0\\.90|0\\.661|0\\.667|0\\.778|0\\.41|0\\.05\" figures paper/main.tex paper/section_replication.tex family2/analyze_factual.py family1/analyze_system_conditions.py" in C:\Users\HP\Documents\MeasurementScience_Evals\paper11_elicitation_method
 succeeded in 5630ms:
paper/main.tex:38:95\% interval half-width of $\pm 0.41$ on a $[0,1]$ rate. A published figure of $0.661$ obtained
paper/main.tex:39:from one sentence becomes $0.223$ over ten, and reaching $\pm 0.05$ would take $69$ items in one
paper/main.tex:46:value adjudicates a large share of cases by rounding: moving one cut from $0.60$ to $0.90$
paper/main.tex:194:standard deviation we measure. One item gives a 95\% interval half-width of $\pm 0.41$ on a
paper/main.tex:199:At one item the 95\% interval half-width is $\pm 0.41$. The interval is wider than most effects
paper/main.tex:202:$\pm 0.13$. Reaching $\pm 0.05$ takes $69$.
paper/main.tex:205:per construct, which reported a rate of $0.661$ for the construct we call ethical conflict
paper/main.tex:207:values run from $0.000$ to $0.667$. The published figure is not a mismeasurement of its
paper/main.tex:216:($\Delta = 0.178$, $[0.058, 0.312]$) while the contrast against the nearest single construct
paper/main.tex:217:does not ($\Delta = 0.107$, $[-0.060, 0.272]$), and only the item-clustered interval reveals
paper/main.tex:294:corpus there are $46$ distinct values; $97.7\%$ are multiples of $0.05$ and $89.5\%$ are
paper/main.tex:301:and the quantity equals exactly $1.00$ in $37.9\%$ of evaluations---the modal value.
paper/main.tex:309:which is the study's control, from $0.000$ to $0.778$. A result that had read as ``the signature
paper/main.tex:345:sampling sets a floor of roughly seventy items for a $\pm 0.05$ estimate in the first family and
paper/main.tex:346:twenty in the second. Threshold placement is worth the difference between $0.000$ and $0.778$ on
paper/main.tex:400:co-authored by the present author, and one published figure re-analysed here ($0.661$) comes
family2/analyze_factual.py:18:                         harian falta para un semiancho de 0.05
family2/analyze_factual.py:55:def k_needed(sd, half=0.05):
family2/analyze_factual.py:93:                     "k_for_0.05": k_needed(per.std(ddof=1)), "n_items": len(per)})
family2/analyze_factual.py:97:    print(f"  k requerido va de {int(t['k_for_0.05'].min())} a {int(t['k_for_0.05'].max())} "
family2/analyze_factual.py:99:          f"{t['k_for_0.05'].max() / max(t['k_for_0.05'].min(), 1):.0f}x dentro del mismo banco")
family2/analyze_factual.py:152:    print(f"  multiplos de 0.05: {100 * np.mean(np.abs(v * 20 - np.round(v * 20)) < 1e-9):.1f}%")
family2/analyze_factual.py:153:    print(f"  multiplos de 0.10: {100 * np.mean(np.abs(v * 10 - np.round(v * 10)) < 1e-9):.1f}%")
family2/analyze_factual.py:168:    for cut in [0.60, 0.70, 0.80, 0.85, 0.90, 0.95, 0.99]:
figures\make_fig1_between_items.py:106:    ax.axvline(0.661, color=ORANGE, lw=1.4, ls=(0, (4, 2)), zorder=1)
figures\make_fig1_between_items.py:107:    ax.annotate("the pilot's single sentence, 0.661,\n"
figures\make_fig1_between_items.py:108:                "lands on the bank's highest item, 0.667",
figures\make_fig1_between_items.py:109:                xy=(0.661, len(order) - 1 + 0.18), xytext=(0.16, len(order) - 0.16),
figures\make_figures.py:69:    ax.axhline(0.05, color=ORANGE, lw=1.2, ls=(0, (4, 2)), zorder=2)
figures\make_figures.py:70:    ax.text(1.05, 0.058, "±0.05 target", color=ORANGE, fontsize=7, ha="left", va="bottom")
figures\make_figures.py:100:    ax.annotate("the threshold sits on\nthe modal value:\nT+F = 1.00 in 37.9%",
figures\make_figures.py:105:    ax.set_xlim(-0.05, 2.05)
paper/section_replication.tex:40:is placed. Moving the cut from $0.60$ to $0.90$ takes the open-question rate from $0.450$ to
paper/section_replication.tex:48:from $0.001$ to $0.112$. Converted to a sample size for a $\pm 0.05$ half-width, that is between
paper/section_replication.tex:70:$[-0.057,\,+0.013]$. That is the first corpus's result again: the sentence that names the
paper/section_replication.tex:74:to $0.533$---a paired difference of $-0.018$, interval $[-0.052,\,+0.016]$. On the first corpus
paper/section_replication.tex:97:intervals $[-0.233,\,-0.050]$ for the full ablation and $[-0.267,\,+0.000]$ for the minimal one.
paper/section_replication.tex:117:elicitations, $95.7\%$ multiples of $0.05$ and $86.4\%$ multiples of $0.1$, with $33\%$ of answers
paper/section_replication.tex:133:genuinely open   & 0.560 & 0.110 & 0.028 & 0.054 \\
paper/section_replication.tex:143:$0.60$, $0.089$ at $0.80$, and $0.028$ at $0.90$. None of those numbers is more correct than the
figures\make_figure_factual.py:97:    for k in (0.60, 0.90):
figures\make_figure_factual.py:110:    ax2.annotate("steps are the response grid:\n83% of answers\nare multiples of 0.10",
figures\make_figure_factual.py:127:          f"rate at 0.60 = {(u>=0.60).mean():.3f}, at 0.90 = {(u>=0.90).mean():.3f}, "
figures\make_figure_factual.py:128:          f"factor {(u>=0.60).mean()/max((u>=0.90).mean(),1e-9):.1f}x")

codex
I’m going to clean up only the generated artifacts created by my verification runs: the tracked figure PDFs that were regenerated and the untracked CSVs emitted by the analysis scripts. I’ll leave the pre-existing untracked `review/` directory alone.
exec
"C:\\WINDOWS\\System32\\WindowsPowerShell\\v1.0\\powershell.exe" -Command 'git restore -- paper/figA_precision.pdf paper/figB_grid.pdf paper/figC_threshold.pdf' in C:\Users\HP\Documents\MeasurementScience_Evals\paper11_elicitation_method
 exited 1 in 14614ms:
fatal: Unable to create 'C:/Users/HP/Documents/MeasurementScience_Evals/paper11_elicitation_method/.git/index.lock': Permission denied

codex
`git restore` cannot update the worktree because this sandbox can read `.git` but cannot create `.git/index.lock`. I’ll restore the three generated PDFs by reading their `HEAD` blobs and writing those bytes directly to the workspace, which avoids touching the Git index.
exec
"C:\\WINDOWS\\System32\\WindowsPowerShell\\v1.0\\powershell.exe" -Command '$code = @'"'
import pathlib
import subprocess
for path in ['paper/figA_precision.pdf', 'paper/figB_grid.pdf', 'paper/figC_threshold.pdf']:
    data = subprocess.check_output(['git', 'show', f'HEAD:{path}'])
    pathlib.Path(path).write_bytes(data)
    print('restored', path)
'@
python -c "'$code' in C:\Users\HP\Documents\MeasurementScience_Evals\paper11_elicitation_method
 succeeded in 14266ms:
restored paper/figA_precision.pdf
restored paper/figB_grid.pdf
restored paper/figC_threshold.pdf

codex
The tracked figure PDFs are back to their `HEAD` bytes. I’m removing only the CSVs that the analysis scripts emitted during this run.
exec
"C:\\WINDOWS\\System32\\WindowsPowerShell\\v1.0\\powershell.exe" -Command "Remove-Item -LiteralPath 'family1\\results\\h5_between_item_variance.csv','family1\\results\\main_phenomenon_x_form.csv','family1\\results\\quad_q1_occupancy.csv','family1\\results\\quad_q2_N_vs_I.csv','family1\\results\\quad_q3_gloss.csv','family1\\results\\quad_q4_between_items.csv'" in C:\Users\HP\Documents\MeasurementScience_Evals\paper11_elicitation_method
 succeeded in 8690ms:
exec
"C:\\WINDOWS\\System32\\WindowsPowerShell\\v1.0\\powershell.exe" -Command 'git status --short' in C:\Users\HP\Documents\MeasurementScience_Evals\paper11_elicitation_method
 succeeded in 11693ms:
warning: unable to access 'C:\Users\HP/.config/git/ignore': Permission denied
warning: unable to access 'C:\Users\HP/.config/git/ignore': Permission denied
?? review/

codex
I’m checking the worktree state after cleanup. The only remaining untracked path should be the pre-existing `review/` directory.
codex
The table-level Wilson intervals are row-level binomial intervals. Since the manuscript argues that item sampling is the dominant uncertainty source, I’m checking how much those intervals change when the ablation rates are resampled by item instead of treating model-item rows as independent Bernoulli trials.
exec
"C:\\WINDOWS\\System32\\WindowsPowerShell\\v1.0\\powershell.exe" -Command '$code = @'"'
import json, pathlib
import pandas as pd
import numpy as np
RES = pathlib.Path('family1/results')
CONT = ['ethical','ignorance','vagueness','contingency','paradox']

def load(path):
    d = pd.DataFrame([json.loads(l) for l in path.read_text(encoding='utf-8').splitlines() if l.strip()])
    d = d[d.parsed & ~d.error].copy()
    for c in 'TINF':
        d[c] = pd.to_numeric(d[c], errors='coerce')
    return d.dropna(subset=list('TINF'))

def boot_item_rate(d, B=5000, seed=0):
    per = d.assign(x=(d.rung == 'strong').astype(int)).groupby('item_id').x.mean().to_numpy()
    rr = np.random.default_rng(seed)
    draws = rr.choice(per, (B, len(per)), True).mean(axis=1)
    return np.percentile(draws, [2.5,97.5])
full0 = load(RES/'raw_quad_bank.jsonl')
conds = {
 'full': full0[(full0.gloss == 'G1') & (full0.form.isin(['bare','anchor']))],
 'nolicense': load(RES/'raw_nolicense_system.jsonl'),
 'neutral': load(RES/'raw_neutral_system.jsonl')
}
for name, d in conds.items():
    c = d[d.phenomenon.isin(CONT)]
    print(name, 'row_rate', round(float((c.rung=='strong').mean()),3), 'item_boot_ci', np.round(boot_item_rate(c),3).tolist(), 'n_items', c.item_id.nunique(), 'n_rows', len(c))
'@
python -c "'$code' in C:\Users\HP\Documents\MeasurementScience_Evals\paper11_elicitation_method
 succeeded in 16986ms:
full row_rate 0.077 item_boot_ci [0.04, 0.12] n_items 50 n_rows 298
nolicense row_rate 0.06 item_boot_ci [0.035, 0.091] n_items 50 n_rows 285
neutral row_rate 0.004 item_boot_ci [0.0, 0.01] n_items 50 n_rows 276

codex
I have enough concrete defects now: several numerical mismatches, one figure mismatch, one source/provenance problem in the agreement section, and two statistical reporting problems. I’m doing a final pass over the findings so the verdict is tied only to reproducible evidence, not reviewer rhetoric.
  ✓ Map manuscript quantitative claims and version differences
  ✓ Run released analysis scripts and recompute targeted quantities from JSONL
  ✓ Check statistical-method/citation support for high-risk claims
  → Assemble numbered hostile-review findings with evidence and fixes
codex
I’m pulling the exact source lines for the final report now: this is just to anchor each finding to the TeX or script line that makes the claim.
exec
"C:\\WINDOWS\\System32\\WindowsPowerShell\\v1.0\\powershell.exe" -Command "rg -n \"0\\.223|0\\.222|equals or exceeds|Target rate, all items|does not replicate at all|moves the shape|one of the two intervals|17\\.5|33\\.4|model versions|83%|def boot_ci|draws =|boot_ci\\(diff|raw_quad_bank.jsonl|three repetitions|model_id|timestamp|date\" paper/main.tex paper/section_replication.tex figures/make_figure_factual.py family2/analyze_factual.py family1/README.md paper/refs.bib" in C:\Users\HP\Documents\MeasurementScience_Evals\paper11_elicitation_method
 succeeded in 3381ms:
family1/README.md:23:| `results/raw_quad_bank.jsonl` | 1,980 | the same bank, three repetitions |
family1/README.md:35:consumed it now computes the same values from `raw_quad_bank.jsonl`, verified identical across all
paper/main.tex:26:\date{August 2026}
paper/main.tex:39:from one sentence becomes $0.223$ over ten, and reaching $\pm 0.05$ would take $69$ items in one
paper/main.tex:50:framing effect does not replicate at all, which sharpens the rule. We state the design rule each result implies and release both item banks, the code and every
paper/main.tex:174:Ethical conflict & 0.222 & 0.211 & 0.95 \\
paper/main.tex:181:\caption{Ten items per construct. The standard deviation between item means equals or exceeds
paper/main.tex:206:\citep{leyva2026ladder}. Measured over ten items the same quantity is $0.222$, and the per-item
paper/main.tex:244:Target rate, all items & 0.077 & 0.060 & \textbf{0.004} \\
paper/main.tex:330:wording land on different labels $17.5\%$ of the time ($n = 4{,}032$ pairs); two different models
paper/main.tex:369:been validated against independent judges. What we can say is
paper/main.tex:397:through a single router at temperature $1.0$. Vendors and model versions are named in
paper/main.tex:399:results are properties of specific model versions at a specific date and should not be assumed
paper/section_replication.tex:73:The second half does not replicate at all. Deleting the entire framing moves the same construct
paper/section_replication.tex:103:effect, and one of the two intervals touches zero. We report it because the direction is identical
paper/section_replication.tex:107:framing does not matter here. It matters; it moves the shape and not the location.
figures/make_figure_factual.py:31:plt.rcParams.update({
figures/make_figure_factual.py:110:    ax2.annotate("steps are the response grid:\n83% of answers\nare multiples of 0.10",
family2/analyze_factual.py:60:def boot_ci(vals, n=5000, seed=0):
family2/analyze_factual.py:66:    draws = rng.choice(vals, size=(n, len(vals)), replace=True).mean(axis=1)
family2/analyze_factual.py:132:            lo, hi = boot_ci(diff.values)
family2/analyze_factual.py:144:            lo, hi = boot_ci(diff.values)

codex
One line has changed from the earlier broad read in the sense that `rg` reveals a parenthetical denominator in the source line. I’m opening that paragraph directly so the final report uses the actual current TeX, not a stale skim.
exec
"C:\\WINDOWS\\System32\\WindowsPowerShell\\v1.0\\powershell.exe" -Command "Get-Content -LiteralPath 'paper\\main.tex' | Select-Object -Skip 322 -First 14" in C:\Users\HP\Documents\MeasurementScience_Evals\paper11_elicitation_method
 succeeded in 7404ms:
One further quantity is worth separating because it is routinely misread \citep{cohen1960, shroutfleiss1979}. Studies that use
several models as raters report an agreement coefficient over their labels. With one generation
per cell at a non-zero temperature, such a coefficient cannot distinguish models disagreeing
from a single model answering differently on a rerun.

Our corpus contains a design that separates them, because the pilot has ten repetitions. Over
the five contested statements, two repetitions of the same item by the same model under the same
wording land on different labels $17.5\%$ of the time ($n = 4{,}032$ pairs); two different models
answering the same item, wording and repetition disagree $32.8\%$ of the time ($n = 2{,}240$
pairs). Roughly half of the disagreement attributed to raters is stochastic variation a single
rater produces on its own. Both rates exclude the three tautological controls, where the label
is almost never in dispute and including them halves both figures without changing their
ratio. The pooled coefficient over the bank, $\kappa = 0.184$ \citep{fleiss1971}, should be read
as a bound on reproducibility rather than as a measure of inter-model disagreement.

codex
That explains the apparent agreement mismatch: the current TeX restricts the pilot rates to the five contested statements and gives denominators. I’m recomputing that exact subset now.
exec
"C:\\WINDOWS\\System32\\WindowsPowerShell\\v1.0\\powershell.exe" -Command '$code = @'"'
import json, pathlib
from itertools import combinations
import pandas as pd
import numpy as np
raw = pd.DataFrame([json.loads(l) for l in pathlib.Path('family1/results/raw_quadruple_pilot.jsonl').read_text(encoding='utf-8').splitlines() if l.strip()])
d = raw[raw.parsed & ~raw.error].copy()
# contested = exclude tautology controls. Consensus? print names.
print('phenomena', sorted(d.phenomenon.unique()))
cont = d[~d.phenomenon.str.contains('Tautology', na=False)].copy()
for label, df in [('exclude_tautology', cont), ('exclude_tautology_and_consensus', cont[~cont.phenomenon.str.contains('Consensus', na=False)])]:
    within=[]
    for _, g in df.groupby(['phenomenon','statement','gloss','model']):
        labs=list(g.sort_values('rep').regime)
        within.extend([a"'!=b for a,b in combinations(labs,2)])
    between=[]
    for _, g in df.groupby(['"'phenomenon','statement','gloss','rep']):
        labs=list(g.set_index('model').regime)
        between.extend([a"'!=b for a,b in combinations(labs,2)])
    print(label, '"'within', round(float(np.mean(within)),3), len(within), 'between', round(float(np.mean(between)),3), len(between))
'@
python -c "'$code' in C:\Users\HP\Documents\MeasurementScience_Evals\paper11_elicitation_method
 succeeded in 13759ms:
phenomena ['Contingency (Future)', 'Contradiction (Ethical)', 'Ignorance (Epistemic)', 'Paradox (Logical)', 'Tautology (Definitional)', 'Tautology (Logical)', 'Tautology (Math)', 'Vagueness (Fuzzy)']
exclude_tautology within 0.175 4032 between 0.328 2240
exclude_tautology_and_consensus within 0.175 4032 between 0.328 2240

codex
The exact current pilot rates are reproducible from the raw file once the three tautology controls are excluded: 0.175 over 4,032 repeat pairs and 0.328 over 2,240 between-model pairs. The remaining problem is that no released analysis script computes those manuscript numbers.
exec
"C:\\WINDOWS\\System32\\WindowsPowerShell\\v1.0\\powershell.exe" -Command '$code = @'"'
import json, pathlib
from itertools import combinations
import pandas as pd
import numpy as np
raw = pd.DataFrame([json.loads(l) for l in pathlib.Path('family1/results/raw_quadruple_pilot.jsonl').read_text(encoding='utf-8').splitlines() if l.strip()])
d = raw[raw.parsed & ~raw.error].copy()
d = d[~d.phenomenon.str.contains('Tautology', na=False)].copy()
def ci(v, B=5000, seed=0):
    rr=np.random.default_rng(seed); v=np.asarray(v,float); return np.percentile(rr.choice(v,(B,len(v)),True).mean(1),[2.5,97.5])
within=[]; within_group=[]
for key,g in d.groupby(['phenomenon','statement','gloss','model']):
    vals=[a"'!=b for a,b in combinations(list(g.sort_values('"'rep').regime),2)]
    within.extend(vals); within_group.append(np.mean(vals))
between=[]; between_group=[]
for key,g in d.groupby(['phenomenon','statement','gloss','rep']):
    vals=[a"'!=b for a,b in combinations(list(g.set_index('"'model').regime),2)]
    between.extend(vals); between_group.append(np.mean(vals))
print('within flat', np.mean(within), len(within), 'cluster_ci', np.round(ci(within_group),3).tolist())
print('between flat', np.mean(between), len(between), 'cluster_ci', np.round(ci(between_group),3).tolist())
'@
python -c "'$code' in C:\Users\HP\Documents\MeasurementScience_Evals\paper11_elicitation_method
 succeeded in 8918ms:
within flat 0.1753472222222222 4032 cluster_ci [0.13, 0.228]
between flat 0.328125 2240 cluster_ci [0.284, 0.373]

codex
I’m checking the two alternative framings for the agreement paragraph as well, because this is the kind of late numerical edit that can drift across generated variants.
exec
"C:\\WINDOWS\\System32\\WindowsPowerShell\\v1.0\\powershell.exe" -Command "rg -n \"17\\.5|33\\.4|32\\.8|4\\{,\\}032|2\\{,\\}240|two different models\" paper/main.tex paper/main_ipm.tex paper/main_nlp.tex" in C:\Users\HP\Documents\MeasurementScience_Evals\paper11_elicitation_method
 succeeded in 370ms:
paper/main.tex:330:wording land on different labels $17.5\%$ of the time ($n = 4{,}032$ pairs); two different models
paper/main.tex:331:answering the same item, wording and repetition disagree $32.8\%$ of the time ($n = 2{,}240$
paper/main_nlp.tex:318:wording land on different labels $17.5\%$ of the time ($n = 4{,}032$ pairs); two different models
paper/main_nlp.tex:319:answering the same item, wording and repetition disagree $32.8\%$ of the time ($n = 2{,}240$
paper/main_ipm.tex:320:wording land on different labels $17.5\%$ of the time ($n = 4{,}032$ pairs); two different models
paper/main_ipm.tex:321:answering the same item, wording and repetition disagree $32.8\%$ of the time ($n = 2{,}240$

codex
One last evidence check: I’m verifying whether the pilot disagreement percentages appear anywhere in released analysis code, excluding the manuscript and the untracked review log.
exec
"C:\\WINDOWS\\System32\\WindowsPowerShell\\v1.0\\powershell.exe" -Command "rg -n \"17\\.5|32\\.8|4\\{,\\}032|2\\{,\\}240|4032|2240\" family1 family2 figures validity paper/refs.bib README.md" in C:\Users\HP\Documents\MeasurementScience_Evals\paper11_elicitation_method
 exited 1 in 4595ms:
codex
The pilot disagreement percentages do not appear in any released analysis script or figure script. They are reproducible from the raw pilot file, but only by writing an extra calculation.
  ✓ Map manuscript quantitative claims and version differences
  ✓ Run released analysis scripts and recompute targeted quantities from JSONL
  ✓ Check statistical-method/citation support for high-risk claims
  ✓ Assemble numbered hostile-review findings with evidence and fixes
codex
1. [SEVERITY: major]  
WHERE: `paper/main.tex:37-38`, `paper/main.tex:181-182`  
CLAIM: “between-item standard deviations equal or exceed the mean.”  
PROBLEM: False for ethical conflict, the largest construct used for the ±0.41 and 69-item derivation.  
EVIDENCE: `python family1/analyze_quad_bank.py` gives ethical conflict mean `0.222`, SD `0.211`, SD/mean `0.95`; the table itself says the same at `paper/main.tex:174`.  
FIX: Replace “equal or exceed” with “are of the same order as the mean”; change the caption’s “in all five cases.”

2. [SEVERITY: minor]  
WHERE: `paper/main.tex:39` versus `paper/main.tex:206`  
CLAIM: The one-sentence figure “becomes 0.223 over ten.”  
PROBLEM: The body and released script give `0.222`, not `0.223`.  
EVIDENCE: `analyze_quad_bank.py` prints ethical conflict strong-rung mean `0.222`; `paper/main.tex:206` also says `0.222`.  
FIX: Change abstract value to `0.222`.

3. [SEVERITY: major]  
WHERE: `paper/main.tex:244`  
CLAIM: “Target rate, all items” is `0.077`, `0.060`, `0.004`.  
PROBLEM: Those are contested-item-only rates, not all-item rates. Including anchors changes all three rates and CIs.  
EVIDENCE: recomputation gives contested only: `23/298=0.077 [0.052,0.113]`, `17/285=0.060 [0.038,0.093]`, `1/276=0.004 [0.001,0.020]`; including anchors: `23/358=0.064 [0.043,0.095]`, `17/337=0.050 [0.032,0.079]`, `1/333=0.003 [0.001,0.017]`.  
FIX: Relabel as “Target rate, contested items” or recompute including anchors.

4. [SEVERITY: major]  
WHERE: `figures/make_figure_factual.py:110`, `paper/section_replication.tex:117`  
CLAIM: Figure C annotates “83% of answers are multiples of 0.10.”  
PROBLEM: The data and manuscript prose give `86.4%`. The compiled figure carries a stale quantitative claim.  
EVIDENCE: `python family2/analyze_factual.py` prints `multiplos de 0.10: 86.4%`; figure code hard-codes `83%`.  
FIX: Compute the annotation from data or change it to `86.4%`.

5. [SEVERITY: major]  
WHERE: `paper/main.tex:50`, `paper/section_replication.tex:73`, `paper/section_replication.tex:103-107`  
CLAIM: The abstract says the framing effect “does not replicate at all.”  
PROBLEM: The replication section later says it changes response shape, then states “It matters; it moves the shape and not the location.” One of the reported shape intervals touches zero, so both the abstract and the conclusion-level wording overstate the evidence.  
EVIDENCE: shape claim is `17/60` to `9/60`, Δ `-0.133`, intervals `[-0.233,-0.050]` and `[-0.267,+0.000]`.  
FIX: Say “does not replicate in the mean; shape evidence is indicative” consistently.

6. [SEVERITY: major]  
WHERE: `family2/analyze_factual.py:60-66`, `family2/analyze_factual.py:132`, `family2/analyze_factual.py:144`  
CLAIM: The paired ablation intervals are bootstrap intervals consistent with the item-resampling rule.  
PROBLEM: The function says item-clustered, but it samples flat `diff.values`; for ablations those are item-model rows, not item clusters.  
EVIDENCE: released output for unsettled mean deltas matches flat-row bootstrap: nolicense `[-0.057,+0.013]`, neutral `[-0.052,+0.016]`. Resampling by item gives different intervals: nolicense `[-0.051,+0.010]`, neutral `[-0.045,+0.008]`; focal-0.50 shape intervals also change.  
FIX: Define the resampling unit and implement it; update intervals and significance language.

7. [SEVERITY: major]  
WHERE: `paper/main.tex:330-333`  
CLAIM: Repeat disagreement is `17.5%`, between-model disagreement is `32.8%`, and κ is `0.184`.  
PROBLEM: κ is produced by a released script, but the two pilot disagreement percentages are not produced by any released analysis script, despite being manuscript results. They also lack intervals.  
EVIDENCE: `rg` over `family1 family2 figures validity` finds no `17.5`, `32.8`, `4032`, or `2240`. Manual recomputation from `raw_quadruple_pilot.jsonl` gives `0.175` over `4,032` pairs and `0.328` over `2,240` pairs; cluster bootstrap CIs are `[0.130,0.228]` and `[0.284,0.373]`. κ bootstrap over bank units gives about `[0.149,0.216]`.  
FIX: Add the pilot-decomposition script and report intervals.

8. [SEVERITY: major]  
WHERE: `paper/main.tex:397-399`, raw JSONL files  
CLAIM: “model versions are named ... and recorded with every generation.”  
PROBLEM: Most raw records do not contain model IDs, version IDs, timestamps, or collection dates.  
EVIDENCE: first-record keys show `model_id` only in `raw_quadruple_pilot.jsonl`; `raw_bank.jsonl`, `raw_quad_bank.jsonl`, both Family I ablation files, and all Family II files lack `model_id` and any timestamp/date field.  
FIX: Add exact router model IDs and collection timestamps to every raw record, or weaken the declaration.

9. [SEVERITY: minor]  
WHERE: `paper/refs.bib`  
CLAIM: Bibliography supports the manuscript.  
PROBLEM: Four bibliography entries are uncited: `farquhar2024`, `manakul2023`, `leyva2026protocol`, `smarandache2026ladder`.  
EVIDENCE: local citation-key check found 23 bib entries, 19 used, 4 unused. External checks of cited sources did not find a fake among the checked references, e.g. arXiv `2605.27752`, arXiv `2606.13685`, ACM Jacobs/Wallach, ACL Rodriguez, ACL Vania, ACL Bowman, PubMed MacCallum.  
FIX: Remove uncited entries or attach them to claims they actually support.

Verdict: reject; the central quantitative presentation contains false headline wording, stale figure text, mismatched denominators, and incomplete reproducibility for reported pilot statistics.
hook: Stop
hook: Stop Completed
tokens used
360,438
1. [SEVERITY: major]  
WHERE: `paper/main.tex:37-38`, `paper/main.tex:181-182`  
CLAIM: “between-item standard deviations equal or exceed the mean.”  
PROBLEM: False for ethical conflict, the largest construct used for the ±0.41 and 69-item derivation.  
EVIDENCE: `python family1/analyze_quad_bank.py` gives ethical conflict mean `0.222`, SD `0.211`, SD/mean `0.95`; the table itself says the same at `paper/main.tex:174`.  
FIX: Replace “equal or exceed” with “are of the same order as the mean”; change the caption’s “in all five cases.”

2. [SEVERITY: minor]  
WHERE: `paper/main.tex:39` versus `paper/main.tex:206`  
CLAIM: The one-sentence figure “becomes 0.223 over ten.”  
PROBLEM: The body and released script give `0.222`, not `0.223`.  
EVIDENCE: `analyze_quad_bank.py` prints ethical conflict strong-rung mean `0.222`; `paper/main.tex:206` also says `0.222`.  
FIX: Change abstract value to `0.222`.

3. [SEVERITY: major]  
WHERE: `paper/main.tex:244`  
CLAIM: “Target rate, all items” is `0.077`, `0.060`, `0.004`.  
PROBLEM: Those are contested-item-only rates, not all-item rates. Including anchors changes all three rates and CIs.  
EVIDENCE: recomputation gives contested only: `23/298=0.077 [0.052,0.113]`, `17/285=0.060 [0.038,0.093]`, `1/276=0.004 [0.001,0.020]`; including anchors: `23/358=0.064 [0.043,0.095]`, `17/337=0.050 [0.032,0.079]`, `1/333=0.003 [0.001,0.017]`.  
FIX: Relabel as “Target rate, contested items” or recompute including anchors.

4. [SEVERITY: major]  
WHERE: `figures/make_figure_factual.py:110`, `paper/section_replication.tex:117`  
CLAIM: Figure C annotates “83% of answers are multiples of 0.10.”  
PROBLEM: The data and manuscript prose give `86.4%`. The compiled figure carries a stale quantitative claim.  
EVIDENCE: `python family2/analyze_factual.py` prints `multiplos de 0.10: 86.4%`; figure code hard-codes `83%`.  
FIX: Compute the annotation from data or change it to `86.4%`.

5. [SEVERITY: major]  
WHERE: `paper/main.tex:50`, `paper/section_replication.tex:73`, `paper/section_replication.tex:103-107`  
CLAIM: The abstract says the framing effect “does not replicate at all.”  
PROBLEM: The replication section later says it changes response shape, then states “It matters; it moves the shape and not the location.” One of the reported shape intervals touches zero, so both the abstract and the conclusion-level wording overstate the evidence.  
EVIDENCE: shape claim is `17/60` to `9/60`, Δ `-0.133`, intervals `[-0.233,-0.050]` and `[-0.267,+0.000]`.  
FIX: Say “does not replicate in the mean; shape evidence is indicative” consistently.

6. [SEVERITY: major]  
WHERE: `family2/analyze_factual.py:60-66`, `family2/analyze_factual.py:132`, `family2/analyze_factual.py:144`  
CLAIM: The paired ablation intervals are bootstrap intervals consistent with the item-resampling rule.  
PROBLEM: The function says item-clustered, but it samples flat `diff.values`; for ablations those are item-model rows, not item clusters.  
EVIDENCE: released output for unsettled mean deltas matches flat-row bootstrap: nolicense `[-0.057,+0.013]`, neutral `[-0.052,+0.016]`. Resampling by item gives different intervals: nolicense `[-0.051,+0.010]`, neutral `[-0.045,+0.008]`; focal-0.50 shape intervals also change.  
FIX: Define the resampling unit and implement it; update intervals and significance language.

7. [SEVERITY: major]  
WHERE: `paper/main.tex:330-333`  
CLAIM: Repeat disagreement is `17.5%`, between-model disagreement is `32.8%`, and κ is `0.184`.  
PROBLEM: κ is produced by a released script, but the two pilot disagreement percentages are not produced by any released analysis script, despite being manuscript results. They also lack intervals.  
EVIDENCE: `rg` over `family1 family2 figures validity` finds no `17.5`, `32.8`, `4032`, or `2240`. Manual recomputation from `raw_quadruple_pilot.jsonl` gives `0.175` over `4,032` pairs and `0.328` over `2,240` pairs; cluster bootstrap CIs are `[0.130,0.228]` and `[0.284,0.373]`. κ bootstrap over bank units gives about `[0.149,0.216]`.  
FIX: Add the pilot-decomposition script and report intervals.

8. [SEVERITY: major]  
WHERE: `paper/main.tex:397-399`, raw JSONL files  
CLAIM: “model versions are named ... and recorded with every generation.”  
PROBLEM: Most raw records do not contain model IDs, version IDs, timestamps, or collection dates.  
EVIDENCE: first-record keys show `model_id` only in `raw_quadruple_pilot.jsonl`; `raw_bank.jsonl`, `raw_quad_bank.jsonl`, both Family I ablation files, and all Family II files lack `model_id` and any timestamp/date field.  
FIX: Add exact router model IDs and collection timestamps to every raw record, or weaken the declaration.

9. [SEVERITY: minor]  
WHERE: `paper/refs.bib`  
CLAIM: Bibliography supports the manuscript.  
PROBLEM: Four bibliography entries are uncited: `farquhar2024`, `manakul2023`, `leyva2026protocol`, `smarandache2026ladder`.  
EVIDENCE: local citation-key check found 23 bib entries, 19 used, 4 unused. External checks of cited sources did not find a fake among the checked references, e.g. arXiv `2605.27752`, arXiv `2606.13685`, ACM Jacobs/Wallach, ACL Rodriguez, ACL Vania, ACL Bowman, PubMed MacCallum.  
FIX: Remove uncited entries or attach them to claims they actually support.

Verdict: reject; the central quantitative presentation contains false headline wording, stale figure text, mismatched denominators, and incomplete reproducibility for reported pilot statistics.
CODEX EXIT=0
