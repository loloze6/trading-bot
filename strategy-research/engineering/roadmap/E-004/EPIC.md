# E-004 — Settle the shared record taxonomy with the fork

**Moved to Linear.** This epic's status, findings, and decisions now live there:
https://linear.app/culito/project/e-004-settle-the-shared-record-taxonomy-with-the-fork-e6629c6855ee

This file is kept only as a pointer so existing cross-links (`../E-004/EPIC.md`) keep resolving — it is not updated any more.

---

**Resolved 2026-09-07 (closed).** The premise this epic was opened for turned
out to be stale, not live: `git fetch dorian` +
`git ls-tree -r --name-only dorian/master | grep briefs` shows Dorian's fork
still uses `strategy-research/briefs/` everywhere, identical to current
master — no divergence. The `briefs_record/` name exists only inside
Jeremy's own parked commit `4adb7403` ("PARK: strategy-research restructure,
parked pending fork unification", branch `restructure/parked-20260731`,
message: "DO NOT MERGE THIS BRANCH"), which was never shown to or contested
by Dorian. There was nothing to jointly settle.

**Decision (Jeremy, final):** keep `strategy-research/briefs/` exactly as-is;
do not rename it to `briefs_record/`. The `_record` suffix convention used
elsewhere in the same parked restructure (`campaign_record/` holding
`campaign_state.yaml`/`campaign_log.md`/`campaign_summary.md`/
`feed_wishlist.yaml`) is ratified, but scoped only to folders holding mutable
run state/logs — not to `briefs/`, which holds authored, largely-static
research documents.

Full rationale, the mapping-file forward-note, and the closed Log entry live
in the Linear project (canonical for this epic):
https://linear.app/culito/project/e-004-settle-the-shared-record-taxonomy-with-the-fork-e6629c6855ee
