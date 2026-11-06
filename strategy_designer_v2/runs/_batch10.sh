#!/bin/bash
R=/home/user/trading-bot/strategy_designer_v2; cd $R
until [ "$(grep -c '^===== exit' $R/runs/_night_2026-11-06_batch9.log 2>/dev/null)" -ge 5 ]; do sleep 30; done
for pair in "real_01b_daily_breadth_ltc B" "real_01b_daily_breadth_ltc C"; do
  set -- $pair; echo "===== $1 fold $2 $(date -u +%H:%M)"
  timeout 3600 python3 $R/run.py $R/briefs/$1.md --fold $2 --rounds 2 2>&1 | grep -vE "^(INFO|DEBUG|WARNING)|^\s*$|^\s+(File |~|\^)"
  echo "===== exit $? $(date -u +%H:%M)"
done
