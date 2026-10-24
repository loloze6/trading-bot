# A pre-filled claim (E-068 slice 5)

This brief was written by decide-next from a reader's side finding: something a reader noticed
in an earlier run's evidence. Its claim is already written and checked by code:
`research_brief.yaml` -> `candidate.claim`.

- Copy `candidate.claim` into your hypothesis card's `claim` **unchanged**: the same statement,
  kind, tests, pass_if, fail_if and rationale. The tests are the point of this run. Code keeps
  this claim in your card after this step, as it is, and records any difference in yours.
- Write the rest of the card (thesis, idea quantities, statement, criteria from the menu) around that
  claim, as for any decide-next candidate.
- **The block is the source run's.** When the brief carries `candidate.start_config` (the
  earlier run's base config, with the finding's `config_change` applied if it has one), that
  config is the block the claim is about: describe THAT block in `idea_quantities` and the `statement`, never a
  different signal. Step 1b starts from it and records any change it makes as a deviation.
- Exception: when the brief's config changes only the regime detector (a gate on the source
  run's unchanged strategies), the claim is about that gate: in `idea_quantities` and the `statement` describe the
  gate's condition and the source run's block it gates; keep the strategies as the source
  run's; the ungated twin (the same config without the gate) is the design variant, and code
  derives it, so do not write it.
