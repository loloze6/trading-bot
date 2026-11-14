#!/bin/bash
R=/home/user/trading-bot/strategy_designer_v2; cd $R
for pair in "n38_daily_range_cycles_1d C" "n39_daily_typical_price_anchor_1d B" "n40_multi_day_volume_climax_1d C"; do
  set -- $pair; echo "===== $1 fold $2 $(date -u +%H:%M)"
  timeout 3600 python3 $R/run.py $R/briefs/$1.md --fold $2 --rounds 2 2>&1 | grep -vE "^(INFO|DEBUG|WARNING)|^\s*$|^\s+(File |~|\^)"
  echo "===== exit $? $(date -u +%H:%M)"
done
