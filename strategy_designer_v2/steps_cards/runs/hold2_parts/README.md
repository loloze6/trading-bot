# The books left of the corrected-rule reruns, in 3 parts run side by side (2026-11-20)

The operator's test (topic 37): spread one queue across cloud sessions, each on its own machine (4 cores each), with
the designer session coordinating. Each part runs `topics/30_review/hold_rerun.py PART --run hold2_rerun` (step 4,
step 5 with the saved measure, step 6, the unseen-dates test for a confirmed and profitable book). The results are the
same wherever they run (one engine, one commit). Purpose and expected outcomes: `runs/HOLD2_AND_PILOT_RUN.md`, part B.

Each line is `STEPS|RUN|PLAN_ID`: replace `STEPS` by the absolute path of `strategy_designer_v2/steps_cards` in the clone
(for example `sed "s#^STEPS#$PWD#" part_b.txt > /tmp/part_b.txt`, from `steps_cards`).

| Part | Runs in | Books |
|---|---|---|
| A | the designer session | dual momentum 1h, rsi side predicts next week 1d, heavy-volume follow-through 1d, above-average drift 1d |
| B | a session of its own | golden-cross momentum more coins 1h, rsi above streak 1d, nearness to highs more coins 1d |
| C | a session of its own | nearness to highs more coins 1h, nearness without the short side 1d |
