#!/bin/bash
R=/home/user/trading-bot/strategy_designer_v2; cd $R
until [ "$(grep -c '^===== exit' $R/runs/_night_2026-11-06_batch6.log 2>/dev/null)" -ge 5 ]; do sleep 30; done
for pair in "n06_range_break_continuation_other_coins_1h A" "n12_short_horizon_daily_reversion_1d A" "n15_eth_hourly_momentum_horizons_1h A"; do
  set -- $pair; echo "===== repair2 $1 fold $2 $(date -u +%H:%M)"
  timeout 3600 python3 $R/run.py $R/briefs/$1.md --fold $2 --rounds 2 2>&1 | grep -vE "^(INFO|DEBUG|WARNING)|^\s*$|^\s+(File |~|\^)"
  echo "===== exit $? $(date -u +%H:%M)"
done
