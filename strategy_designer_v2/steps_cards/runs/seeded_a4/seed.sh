#!/bin/bash
# Seeds one strategy into seeded_a4_run and runs its steps 4 and 5 by their own helpers (no model call).
# Usage: VENV_PYTHON=... seed.sh SOURCE_run PLAN_ID S|W
#   S: step 7's index lines (and outputs) copied for every line; W: for every line but 7.d (its entry is evaluated for real).
# Then: step 4 on the run's data (--data-use), step 5 with the plan's stored measure.py (--measure), and for W step 6,
# to read its count of failed measures before run_idea is called.
set -e
S=$1; R=$2; KIND=$3; RUN=seeded_a4_run
V=${VENV_PYTHON:?a venv with trading-bot/requirements.txt}
SC=$(cd "$(dirname "$0")/../.." && pwd); cd $SC
mkdir -p 03_test_plan/$RUN/plans
cp 03_test_plan/$S/plans/$R.md 03_test_plan/$S/plans/${R}_config.json 03_test_plan/$RUN/plans/
for d in 07?_*/; do
  [ "$KIND" = W ] && [ "$d" = 07d_not_profitable/ ] && continue
  if grep -q "^$R:" $d$S/INDEX.md 2>/dev/null; then
    mkdir -p $d$RUN; { grep -v "^$R:" $d$RUN/INDEX.md 2>/dev/null || true; grep "^$R:" $d$S/INDEX.md; } | sort > $d$RUN/INDEX.tmp
    mv $d$RUN/INDEX.tmp $d$RUN/INDEX.md
    [ -d $d$S/$R ] && cp -r $d$S/$R $d$RUN/
  else
    echo "no index line for $R in $d$S: this line would be called by run_idea"
  fi
done
PLAN=03_test_plan/$RUN/plans/$R.md
$V 04_backtest/helper/run_backtest.py $PLAN --python $V --out-root 04_backtest/$RUN/backtests \
   --data-use orchestration/loop/$RUN/data_use.json
$V 05_verification/helper/make_verdict.py $PLAN --python $V --records-root 04_backtest/$RUN/backtests \
   --verdicts-dir 05_verification/$RUN/verdicts --measure 05_verification/$S/verdicts/$R/measure.py
if [ "$KIND" = W ]; then
  $V 06_profitability/helper/check_profitability.py 04_backtest/$RUN/backtests/$R --checks-dir 06_profitability/$RUN/checks
fi
