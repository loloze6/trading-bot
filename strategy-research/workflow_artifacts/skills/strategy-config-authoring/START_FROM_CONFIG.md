# START_FROM_CONFIG.md: start from the source run's config (E-068, CUL-412)

You are reading this note because this run tests a claim a reader noticed in an earlier run's
evidence, and that claim is about the earlier run's block. It is added to your inputs only for
such a run. Where it differs from your skill, this note wins.

- **Start from `artifacts/start_config.json`.** It is the earlier run's base config (with the
  finding's config change applied, if it has one): the block the claim is about. Your
  `backtest_spec.yaml` `config` is that config, unchanged, unless the card truly needs a change.
- **Keep the block.** `artifacts/start_block_manifest.yaml` says which part of that config is
  the block and which is scaffolding. Write the same `block_manifest.yaml` unless you change the
  block.
- **Never build a different signal.** If the card's wording describes another signal, the claim
  and the start config win: the run exists to test this claim on this block.
- **Record every change.** Each change you make is a difference from the start: list it in
  `decision.yaml` `deviations` (clause, built_instead, missing, effect), as for any approximation.
  Code also compares your config and manifest with the start and records every difference, so an
  unlisted change is still visible in the run's finding.
