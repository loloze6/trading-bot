#!/bin/bash
# Build A12, proof: one run of run_idea on a seeded run (no model call: the plan, the verdict and step 7's outputs are
# copied from night 9's 074-01.b1.g1, as in runs/build_a4_join/run_one.sh), in a checkout of its own (a git worktree
# outside the repository), then every file the run wrote or changed copied to $P/out_<label>.
# Usage: run_one.sh LABEL CHECKOUT PROOF_DIR VENV_PYTHON     (LABEL: old = the base commit's checkout, new = this build's)
set -e
LABEL=$1; REPO=$2; P=$3; V=$4
SC=$REPO/strategy_designer_v2/steps_cards
S=night9_fallcalmfade_run; RUN=proofa12_run; R=074-01.b1.g1_convex-deep-run-fade_1d
cd $SC
mkdir -p 03_test_plan/$RUN/plans 05_verification/$RUN/verdicts
cp 03_test_plan/$S/plans/$R.md 03_test_plan/$S/plans/${R}_config.json 03_test_plan/$RUN/plans/
cp -r 05_verification/$S/verdicts/$R 05_verification/$RUN/verdicts/
for d in 07?_*/; do
  if grep -q "^$R:" $d$S/INDEX.md 2>/dev/null; then
    mkdir -p $d$RUN; grep "^$R:" $d$S/INDEX.md > $d$RUN/INDEX.md
    [ -d $d$S/$R ] && cp -r $d$S/$R $d$RUN/
  fi
done
$V orchestration/run_idea/helper/run_idea.py 02_ideation/$S/ideas/074-01.b1.g1_convex-deep-run-fade.md --run $RUN \
   --python $V --brief 01_brief/$S/briefs/074_falling-market-run-break-fade.md > $P/stdout_$LABEL.txt 2>&1 || echo "run_idea exit $?" >> $P/stdout_$LABEL.txt
cd $REPO
OUT=$P/out_$LABEL; rm -rf $OUT; mkdir -p $OUT
{ git status --porcelain -uall | cut -c4-; git ls-files -o -i --exclude-standard | grep -v "__pycache__\|\.pytest_cache" || true; } | sort -u > $P/files_$LABEL.txt
while read f; do [ -f "$f" ] && mkdir -p "$OUT/$(dirname "$f")" && cp -p "$f" "$OUT/$f"; done < $P/files_$LABEL.txt
echo "done $LABEL: $(wc -l < $P/files_$LABEL.txt) files"
