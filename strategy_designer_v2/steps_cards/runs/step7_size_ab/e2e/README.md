# The step 7 A/B ideas, end to end: two lists run side by side (2026-11-21)

Each line is an idea file, starting with `STEPS`: replace it by the absolute path of `strategy_designer_v2/steps_cards`
in the clone (`sed "s#^STEPS#$PWD#" runs/step7_size_ab/e2e/Bp.txt > /tmp/Bp.txt`, from `steps_cards`). Each idea runs
through `orchestration/run_idea/helper/run_idea.py` (steps 3 to 7, the unseen test for a confirmed and paying idea).
Purpose and expected outcomes: `runs/STEP7_SIZE_AB_RUN.md`, "End to end".

| List | Ideas | Run | Runs in |
|---|---|---|---|
| `B.txt` | B's 11 (the size information and the instruction paragraph) | `step7ab_b_run` | the designer session |
| `Bp.txt` | B′'s 9 (the size information only) | `step7ab_bp_run` | a session of its own (branch `step7ab-bp`) |
