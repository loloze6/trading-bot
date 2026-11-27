#!/bin/bash
# B11, B12 (runs/BUILD_B11_B12.md): one run of run_idea on a seeded run (no model call), copied from build_a4_join/run_one.sh;
# "old" runs the code of 7b7f0e8 (before B11, B12). Usage: PROOF_DIR=... VENV_PYTHON=... run_one.sh new|old
set -e
LABEL=$1                                   # "new" or "old"
REPO=/home/user/trading-bot; SC=$REPO/strategy_designer_v2/steps_cards
P=${PROOF_DIR:?a scratch folder outside the repository}   # out_new/, out_old/, the file lists
V=${VENV_PYTHON:?a venv with trading-bot/requirements.txt}
S=night9_fallcalmfade_run; RUN=proofb11_run; R=074-01.b1.g1_convex-deep-run-fade_1d
CODE="common/lib.py 05_verification/helper/make_verdict.py 07_common/helper/analyse.py 07c_rejected/helper/line.yaml
 07c_rejected/helper/line_prompt.md 07d_not_profitable/helper/line.yaml orchestration/run_idea/helper/run_idea.py"
cd $SC
[ "$LABEL" = old ] && for f in $CODE; do git show 7b7f0e8:strategy_designer_v2/steps_cards/$f > $f; done
# seed: the plan, the verdict, step 7's index lines and outputs
mkdir -p 03_test_plan/$RUN/plans 05_verification/$RUN/verdicts
cp 03_test_plan/$S/plans/$R.md 03_test_plan/$S/plans/${R}_config.json 03_test_plan/$RUN/plans/
cp -r 05_verification/$S/verdicts/$R 05_verification/$RUN/verdicts/
for d in 07?_*/; do
  if grep -q "^$R:" $d$S/INDEX.md 2>/dev/null; then
    mkdir -p $d$RUN; grep "^$R:" $d$S/INDEX.md > $d$RUN/INDEX.md
    [ -d $d$S/$R ] && cp -r $d$S/$R $d$RUN/
  fi
done
sleep 1; touch $P/marker_$LABEL; sleep 1
$V orchestration/run_idea/helper/run_idea.py 02_ideation/$S/ideas/074-01.b1.g1_convex-deep-run-fade.md --run $RUN \
   --python $V --brief 01_brief/$S/briefs/074_falling-market-run-break-fade.md > $P/stdout_$LABEL.txt 2>&1 || echo "run_idea exit $?" >> $P/stdout_$LABEL.txt
# collect: every file written since the marker, plus the seeded run's folders
cd $REPO
OUT=$P/out_$LABEL; rm -rf $OUT; mkdir -p $OUT
{ find strategy_designer_v2 trading-bot -newer $P/marker_$LABEL -type f -not -path '*/__pycache__/*'; \
  find strategy_designer_v2/steps_cards -path "*/$RUN/*" -type f; } | sort -u > $P/files_$LABEL.txt
while read f; do mkdir -p "$OUT/$(dirname "$f")"; cp -p "$f" "$OUT/$f"; done < $P/files_$LABEL.txt
# restore: tracked files back to HEAD, new files removed
while read f; do
  if git ls-files --error-unmatch "$f" >/dev/null 2>&1; then git checkout -q HEAD -- "$f"; else rm -f "$f"; fi
done < $P/files_$LABEL.txt
find strategy_designer_v2/steps_cards -type d -name $RUN -prune -exec rm -rf {} +
[ "$LABEL" = old ] && (cd $SC && git checkout -q HEAD -- $CODE)
echo "done $LABEL: $(wc -l < $P/files_$LABEL.txt) files"
