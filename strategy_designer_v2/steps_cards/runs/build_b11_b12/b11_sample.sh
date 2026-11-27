#!/bin/bash
# B11's proof, part 2 (runs/BUILD_B11_B12.md): for a few of night 9's plans, step 4 rebuilt in a scratch folder (the
# record's bars are not committed), then step 5 with the plan's stored measure.py (--measure: no model call) and the new
# code; result.json compared with the committed one. Usage: PROOF_DIR=... VENV_PYTHON=... b11_sample.sh RUN PLAN_ID...
set -e
P=${PROOF_DIR:?a scratch folder outside the repository}; V=${VENV_PYTHON:?a venv with trading-bot/requirements.txt}
SC=/home/user/trading-bot/strategy_designer_v2/steps_cards; cd $SC
RUN=$1; shift
for R in "$@"; do
  $V 04_backtest/helper/run_backtest.py 03_test_plan/$RUN/plans/$R.md --python $V --out-root $P/records > $P/step4_$R.txt 2>&1
  $V 05_verification/helper/make_verdict.py 03_test_plan/$RUN/plans/$R.md --python $V --records-root $P/records \
     --verdicts-dir $P/verdicts --measure 05_verification/$RUN/verdicts/$R/measure.py > $P/step5_$R.txt 2>&1
  python3 - "$SC/05_verification/$RUN/verdicts/$R/result.json" "$P/verdicts/$R/result.json" "$R" <<'PY'
import json, sys
a, b = (json.load(open(f)) for f in sys.argv[1:3])
diff = sorted(k for k in set(a) | set(b) if a.get(k) != b.get(k))
print(f"{sys.argv[3]}: committed {a['status']} -> rerun {b['status']}; fields that differ: {diff or 'none'}")
for k in diff:
    print(f"   {k}: committed {json.dumps(a.get(k))[:200]} | rerun {json.dumps(b.get(k))[:200]}")
PY
done
