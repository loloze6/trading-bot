#!/bin/bash
R=/home/user/trading-bot/strategy_designer_v2; cd $R
until [ "$(grep -c '^===== exit' $R/runs/_night_2026-11-06_batch15.log 2>/dev/null)" -ge 1 ]; do sleep 30; done
for pair in "n35_privacy_coins_hourly_shock_1h A" "n36_ltc_xmr_hourly_weekday_1h A" "n37_zec_ltc_hourly_trend_1h A"; do
  set -- $pair; echo "===== $1 fold $2 $(date -u +%H:%M)"
  timeout 3600 python3 $R/run.py $R/briefs/$1.md --fold $2 --rounds 2 2>&1 | grep -vE "^(INFO|DEBUG|WARNING)|^\s*$|^\s+(File |~|\^)"
  echo "===== exit $? $(date -u +%H:%M)"
done
