# TIMEFRAME_CHANGE_PLAYBOOK.md — RETIRED (2026-09-11, E-045)

**This file's content has been fully redistributed. It is kept only as a
pointer so existing cross-links keep resolving — it is not updated any
more.** Read `strategy-research/DOC_INDEX.md` first for the current map.

Per section, where the content actually lives now:

| Old section | New home |
| --- | --- |
| §1 Warmup mechanics | `trading-bot/DOC/USER_GUIDE.md` §5.1 |
| §2 Assumption-sweep checklist — bar-count/signal-shape half | `strategy-research/docs/DATA_AVAILABILITY.md` §4 |
| §2(c) Assumption-sweep checklist — metric-basis half | `strategy-research/docs/VERIFICATION_DOCTRINE.md` §1 |
| §3 Shakedown doctrine | `strategy-research/docs/VERIFICATION_DOCTRINE.md` §3 |
| §4 Cross-check doctrine | `strategy-research/docs/VERIFICATION_DOCTRINE.md` §4 |
| §5 Read-back verification doctrine | `strategy-research/docs/VERIFICATION_DOCTRINE.md` §5 |
| §6 Concealment-instruction doctrine | `strategy-research/docs/CONCEALMENT_INSTRUCTION_DOCTRINE.md` |
| §7 Three-role model for fragment data | `strategy-research/docs/VERIFICATION_DOCTRINE.md` §2 |
| Checklist addition (doc-index maintenance) | folded into `strategy-research/DOC_INDEX.md`'s own header |
| §8 "Derive, never enumerate" | `strategy-research/docs/DATA_AVAILABILITY.md` §2, §5 |
| §8a Bars derived from a finer cache | `strategy-research/docs/DATA_AVAILABILITY.md` §2 (also `trading-bot/DOC/USER_GUIDE.md` §3.2 for the full engine mechanism) |
| §8b Zero data is not a finding | `strategy-research/docs/DATA_AVAILABILITY.md` §5 |

This split was done per Jeremy's 2026-09-03 ruling (E-045): documentation
splits into (1) small "light" docs forced-read from a skill's required
inputs, (2) engineering-history docs, and (3) general-capability reference
docs — this file mixed all three, hence the split.

Historical artifacts that still cite this file by name (session logs,
`campaign_knowledge_base.yaml`, archived run artifacts, `research/ledger/`)
are left untouched — they are records of what was true when written, not
live documentation.
