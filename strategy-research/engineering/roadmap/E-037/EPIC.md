# E-037 — Rationalize the workflow, using a USER_GUIDE review as the vehicle

**State:** new
**Owner:** Jérémy
**Updated:** 2026-08-29

## Why

The workflow was built one module, feature and step at a time. The
documentation grew the same way — by addition. The result is that the
operator can no longer answer, from one place, the question that matters
most:

> *"What does this step do, what does it consume, what does it produce,
> and why does it exist?"*

Jérémy's words, 2026-08-29: *"I do not understand what is doing what, what
are the rationales and logic behind each step, how they are
interconnected."*

This is not a knowledge gap. **The knowledge exists and is largely
correct** — it is spread across four sections of a 976-line document, in
build order rather than reading order, so assembling any one answer
requires reading the whole thing.

### The concrete symptom this explains

The feeling of losing control was strongest **while working the bug list**.
That is not a coincidence and it is the strongest argument for this epic:

`USER_GUIDE.md` §2.2's stage table has four columns — `#`, `Stage`,
`Engine`, `Objective`. **There is no input/output contract anywhere.** So
before touching a feature there is no way to see which sub-steps it
reaches. Every fix therefore surprises the operator with consequences that
could not be predicted up front.

Independent confirmation from the same week: issues #50, #63, #64 and #66
turned out to be **one defect with six consumers** — the prescreen holds a
time series as a plain list and every consumer assumed list-position
adjacency meant time adjacency. Nobody saw that until someone asked "why do
these keep appearing?" A per-stage input/output contract is exactly the
artifact that would have made it visible on day one.

---

## ⚠️ HARD CONSTRAINT — do not lose information

**The problem is STRUCTURAL, not informational.** The guide's content is
hard-won: it encodes amendment history (A8.6, A2.3, A6.2 …), measured
counts, decisions and their reasons, and traps found the expensive way.

**A restructure that reads better but says less is a NET LOSS and must be
rejected**, however much nicer the result looks.

Binding rules for every stage of this epic:

1. **Nothing is deleted, only relocated.** Content that leaves a section
   must reappear somewhere and be shown to have done so.
2. **A reduction in line count is not a success metric.** The goal is
   *findability*, not brevity. If shortening costs a fact, keep the fact.
3. **Every rewrite is diffed for information loss before it lands** — an
   explicit inventory of "this sentence moved here", not an eyeball pass.
4. **Amendment codes, measured numbers, dates and rationales are
   load-bearing** and survive verbatim. `"of 25 unconstrained expansion
   runs, 21 land in [3,6]"` is evidence, not filler.
5. **When in doubt, keep it.** A slightly long section beats a lost reason.

The failure mode to design against: an agent optimising for a tidy document
and quietly dropping the sentence that explains why a guard exists — which
is precisely the sentence that stops someone removing that guard next year.

---

## What "done" looks like

An operator can answer, for **any** stage, from **one** table row:
what goes in, what comes out, what logic runs, and why the stage exists.
And for any artifact: why the file exists at all.

---

## Scope

### In

- `docs/USER_GUIDE.md` — restructure and enrich, under the constraint above.
- **Challenge the implementation while documenting it.** Filling in
  "stage 7's input is X, output is Y, logic is Z" *forces* a read of the
  code. Every place the document and the code disagree is a finding.
  Documenting and auditing are the same activity here, not two jobs.

### Out

- Fixing what the audit finds. Findings are **recorded, never silently
  fixed** — no drive-by changes. They become cards; Jérémy decides which
  get worked.
- Code refactors. This epic changes documentation and produces a findings
  list. Any code change is a separate ticket.

---

## Operator's specific observations (2026-08-29) — the seed list

Verified against the document before writing this epic:

**Philosophy (§1)**
- Falsification-first is stated as *the* philosophy. It is **a feature, not
  the key alpha.** Demote it.
- **Missing principle to add:** *understand the observation — do not run
  tries without knowing what happened in the previous run and why.* The
  three current principles (structured artifacts, automated routing,
  campaign memory) do not cover it. Its absence is visible in the results:
  35 runs before anyone asked why the kills kept recurring.

**Stage map (§2.1)**
- Simplify to **steps and links only**. It currently carries flow, gates,
  amendment codes and commentary in one ASCII block.

**Stage objectives (§2.2)**
- Several "objectives" are **call-logic descriptions**. Stage 7 reads
  *"A8.6 pre-flight first. Then: active-bar IC, block-bootstrap
  significance, cost_check"* — that is a call sequence. The objective
  ("decide cheaply whether this idea deserves an expensive backtest") is
  never stated.
- **Add three columns:** `stage input`, `stage output`,
  `features / logic in place` (simple but concrete).

**Artifacts (§3)**
- **Add a one-line rationale headliner per artifact** — why this file
  exists — to ensure coherence.
- **Metadata is inconsistent:** early entries carry Created by / Read by /
  Schema; later ones do not. `trade_diagnostics.json` has no schema line
  and no "updated by". Normalise to created by / updated by / read by.
- The **"logic" prose inside some YAML artifact entries belongs in the
  stage table's new logic column**, not with the artifact.

**Glossary (§6)**
- Terms defined in the glossary should be **underlined and intra-document
  hyperlinked** at use, so a reader knows a definition exists.

**Overall**
- The document is good. It needs **restructuring so a reader knows where to
  find things** — subject to the hard constraint above.

---

## Stages

- [ ] **S1 — Design the target shape and prove it on one example.**
      Write the stage-row template (input / output / logic) and the
      artifact-entry template (rationale headliner + normalised metadata).
      Fill in **exactly one stage and one artifact** as a worked sample.
      Also draft the information-loss checklist that S2 and S4 are held to.
      **STOP for Jérémy's approval before touching anything else.**
      Rationale: agreeing the shape first is what prevents the rewrite
      itself becoming another uncontrolled accretion. It is cheap and
      reversible; a full rewrite is neither.

- [ ] **S2 — (blocked on S1) Fill in all stages and artifacts.**
      Against the approved template, reading the code for each. Produce
      `E-037/FINDINGS.md`: every doc-vs-code disagreement, with `file:line`.
      Record, do not fix. Carry an explicit relocation inventory proving no
      content was lost.

- [ ] **S3 — (blocked on S2) Triage the findings.**
      Each becomes a card or issue. Jérémy decides what gets worked. Some
      will be doc errors, some real defects.

- [ ] **S4 — (blocked on S2) Restructure and cross-link.**
      Simplify the stage map to steps and links. Move artifact "logic"
      prose into the stage table. Hyperlink glossary terms. Improve
      findability. Re-run the information-loss checklist before landing.

Sequencing note: S3 and S4 are independent of each other and both depend on
S2. S4 must not start before S2 is complete, or the restructure will be
done against a document still being corrected.

---

## Risks

- **Information loss.** The main one. Mitigated by the hard constraint
  above; it is the primary review criterion for S2 and S4.
- **Scope creep into code fixes.** Mitigated by the record-don't-fix rule.
- **The findings list is itself demoralising** — this epic will surface
  implementation problems, adding to a bug list that already feels out of
  control. Mitigated by *how* they arrive: grouped by stage, each with an
  input/output contract attached, so their blast radius is visible. That
  visibility is the cure, not more findings.

## Log

- 2026-08-29 — `new`. Raised by Jérémy after reading `USER_GUIDE.md` to
  regain control and finding the information present but not assemblable.
  Observations verified against the document before this epic was written:
  §2.2 has no input/output columns; stage 7's objective is a call sequence;
  `trade_diagnostics.json` lacks schema and updated-by lines while
  `research_brief.yaml` has full metadata; §1 lists three principles, none
  of which is "understand the observation". Hard constraint on information
  loss added at Jérémy's explicit instruction: *"the problem is more
  structural than knowledge, and I am afraid that we would weaken the
  information quality if we do not take care."*
