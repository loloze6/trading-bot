# A pre-filled claim (E-068 slice 5)

This brief was written by decide-next from a reader's side finding: something a reader noticed
in an earlier run's evidence. Its claim is already written and checked by code:
`research_brief.yaml` -> `candidate.claim`.

- Copy `candidate.claim` into your hypothesis card's `claim` **unchanged**: the same statement,
  kind, tests, pass_if, fail_if and rationale. The tests are the point of this run.
- Write the rest of the card (thesis, signal, criteria from the menu, assumptions) around that
  claim, as for any decide-next candidate.
- **The block is the source run's.** When the brief carries `candidate.start_config` (the
  earlier run's base config, with the finding's `config_change` applied if it has one), that
  config is the block the claim is about: describe THAT block in `signal_concept`, never a
  different signal. Step 1b starts from it and records any change it makes as a deviation.
- If the claim cannot be kept as it is (for example, a test the slots no longer accept), change
  only what you must and say why in the card's `rationale`. Code compares your claim with the
  pre-filled one after this step and records any difference; the run continues either way.
