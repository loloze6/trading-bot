#!/bin/bash
R=/home/user/trading-bot/strategy_designer_v2; cd $R
for pair in "n30_round_numbers_hourly_1h B" "n31_weekly_reversal_daily_1d A" "n32_vol_term_structure_hourly_1h A" "n33_volume_price_divergence_daily_1d B" "n34_hour_of_day_drift_hourly_1h C"; do
  set -- $pair; echo "===== $1 fold $2 $(date -u +%H:%M)"
  timeout 3600 python3 $R/run.py $R/briefs/$1.md --fold $2 --rounds 2 2>&1 | grep -vE "^(INFO|DEBUG|WARNING)|^\s*$|^\s+(File |~|\^)"
  echo "===== exit $? $(date -u +%H:%M)"
done
