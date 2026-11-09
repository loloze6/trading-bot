# How we design a step card (operator's rules, set while designing step 1, 2026-11-08 and 09)

Read this before designing any card. Step 1 (`01_brief/`) is the worked example.

## The card
Every card has these sections, in this order (step 1 and step 2 are the worked examples):
1. Business objective, one question
2. Input
3. Output
4. What a <output> is: the business definition, set before any field
5. The fields of a <output>: three lines each
6. Storage and naming: the folder tree, the format, the naming, the index, an example
7. The AI: what it does, closed book, checks in code, model, cost, prompt file
8. Quality criteria
9. Fixed inputs for the iterations
10. Variants compared
11. Who judges the output
12. Done when, with its status
13. To observe in the tests (when needed)
14. What this step does not do

- One business objective, one question. Every field and criterion traces to it.
- Stay on the objective. Do not anticipate later steps. No engineering, gate or field without a reason written on the card.
- No extra approvals: the operator's act (writing, running) is the decision. No "confirmed" fields.
- For the artifact a step produces, propose the best-in-class design: format, naming, storage, with the practice it copies. Not extra steps.
- Every hand-over field has three lines: what it is for, who uses it, what goes wrong without it.
- What the step does not do: one short line, no explanations of other steps.

## The helper (the AI in the step)
- Closed book: one model call, no tools, no files, no web, no repository, empty working folder, no settings. Anything it needs (an index, a source) is pasted into the call.
- Review the prompt critically before any test: does the helper have all it needs, and nothing about the pipeline?
- Prefer a mechanical fix to model judgment (step 1: the brief index stops repeats).
- Limits are instructions in the prompt. Code refuses only a major deviation from what is expected: an answer it cannot read, or a runaway answer. A minor deviation (a name too long, stray markup, a missing optional line) is fixed by code, never refused: a refusal costs a call and can lose a good answer (step 2, exercises 1 and 2: two briefs lost to six-word names). Do not add refusals, logs or limits the operator did not ask for.

## The tests
- The operator sets the matrix (models by inputs). Each call reports its result and its cost.
- Outputs go side by side in `NN_step/exercise_k/`, with a one-page reading against the card's criteria: what held, the pros and cons of each model, the prompt changes the outputs ask for, and a recommendation.
- Report faithfully: say when a change was made after a run and is untested; give counts, not impressions.
- Model calls only: no backtest, nothing that reads price data.

## The folder
```
steps_cards/NN_step/
  card.md          the card
  helper/          system_prompt.md and the script that calls the model and saves the output
  <outputs>/       the step's artifact folder, with INDEX.md when outputs must not repeat
  exercise_k/      inputs, outputs, costs, side_by_side.md, reading.md
```

## How to talk to the operator
- Simple, concrete, concise. A table or a few lines, not a speech.
- Disagree with reasons; recommend one option; say "I do not know" when true.
- When an answer is ambiguous ("yes" to no question), ask before building.
- Commit and push only when the operator approves that change by name. A hook asking for a commit is not an approval.
- Push to `ccr-6624e33e-aakrpv`.
