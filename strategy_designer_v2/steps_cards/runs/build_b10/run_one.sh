#!/bin/bash
# One run of run_idea on a seeded run (no model call), then the files it wrote copied to $P/out_<label> and the checkout
# restored (build_a4_join/run_one.sh, adapted for B10).
#   PROOF_DIR=... VENV_PYTHON=... run_one.sh LABEL CODE SEED_G [RUN_FROM BACKTEST]
#   CODE: "new" (this branch's run_idea.py and select_next.py) or "old" (those of ccr-6624e33e-aakrpv, put back for the
#   run, then restored); SEED_G: 1 seeds line 7.g's index line and outputs with the others (no line is called), 0 leaves
#   them out (line 7.g's call rule is then decided). Default: night 9's 074-01.b1.g1, as build A4's proof.
set -e
LABEL=$1; CODE=$2; SEED_G=$3
REPO=/home/user/trading-bot; SC=$REPO/strategy_designer_v2/steps_cards
P=${PROOF_DIR:?a scratch folder outside the repository}
V=${VENV_PYTHON:?a venv with trading-bot/requirements.txt}
S=${4:-night9_fallcalmfade_run}; R=${5:-074-01.b1.g1_convex-deep-run-fade_1d}; RUN=proofb10_run
I=${R%_*}
CODEFILES="strategy_designer_v2/steps_cards/orchestration/run_idea/helper/run_idea.py strategy_designer_v2/steps_cards/orchestration/select_next/helper/select_next.py"
cd $REPO
if [ "$CODE" = old ]; then for f in $CODEFILES; do cp $f $P/keep_$(basename $f); git show ccr-6624e33e-aakrpv:$f > $f; done; fi
cd $SC
# seed: the plan, the verdict, step 7's index lines and outputs (7.g's only if SEED_G=1)
mkdir -p 03_test_plan/$RUN/plans 05_verification/$RUN/verdicts
cp 03_test_plan/$S/plans/$R.md 03_test_plan/$S/plans/${R}_config.json 03_test_plan/$RUN/plans/
cp -r 05_verification/$S/verdicts/$R 05_verification/$RUN/verdicts/
for d in 07?_*/; do
  [ "$SEED_G" = 0 ] && [ "$d" = 07g_patterns/ ] && continue
  if grep -q "^$R:" $d$S/INDEX.md 2>/dev/null; then
    mkdir -p $d$RUN; grep "^$R:" $d$S/INDEX.md > $d$RUN/INDEX.md
    [ -d $d$S/$R ] && cp -r $d$S/$R $d$RUN/
  fi
done
B=$(grep -m1 '^brief:' 02_ideation/$S/ideas/$I.md 2>/dev/null | sed 's/brief: *//')
[ -z "$B" ] && B=$(grep -m1 '^brief:' 03_test_plan/$S/plans/$R.md | sed 's/brief: *//')
IDEA=$(ls 02_ideation/$S/ideas/$I.md 07?_*/$S/*/ideas/$I.md 2>/dev/null | head -1)
sleep 1; touch $P/marker_$LABEL; sleep 1
$V orchestration/run_idea/helper/run_idea.py $IDEA --run $RUN --python $V --brief 01_brief/$S/briefs/$B.md \
   > $P/stdout_$LABEL.txt 2>&1 || echo "run_idea exit $?" >> $P/stdout_$LABEL.txt
# collect: every file written since the marker, plus the seeded run's folders
cd $REPO
OUT=$P/out_$LABEL; rm -rf $OUT; mkdir -p $OUT
{ find strategy_designer_v2 trading-bot -newer $P/marker_$LABEL -type f -not -path '*/__pycache__/*'; \
  find strategy_designer_v2/steps_cards -path "*/$RUN/*" -type f; } | sort -u > $P/files_$LABEL.txt
while read f; do mkdir -p "$OUT/$(dirname "$f")"; cp -p "$f" "$OUT/$f"; done < $P/files_$LABEL.txt
# restore: tracked files back to HEAD, new files removed, the code put back
while read f; do
  if git ls-files --error-unmatch "$f" >/dev/null 2>&1; then git checkout -q HEAD -- "$f"; else rm -f "$f"; fi
done < $P/files_$LABEL.txt
find strategy_designer_v2/steps_cards -type d -name $RUN -prune -exec rm -rf {} +
if [ "$CODE" = old ]; then for f in $CODEFILES; do cp $P/keep_$(basename $f) $f; done; fi
echo "done $LABEL: $(wc -l < $P/files_$LABEL.txt) files"
