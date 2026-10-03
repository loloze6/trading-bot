# CLAIM_NOTE.md: the card's `claim` and your block manifest (E-068)

You are reading this note because `orchestrator.claim_tests.enabled` is on; it is added to
step 1b's inputs only under that flag. Nothing else in your skill changes.

`hypothesis_card.yaml` may carry a `claim` block (written by step 1a). Its `kind` and tests are
1a's view of what the idea could be: a forecast block, a regime block, or a finding only.

- **You decide** whether the idea is a block, and of which kind, from the config you write, in
  `block_manifest.yaml` exactly as your skill describes. Do not bend the config or the manifest
  to match the claim.
- The orchestrator compares the two after this stage and records any mismatch as a warning
  (`artifacts/claim_match.yaml`). It never sends you back for it and never stops the run.
