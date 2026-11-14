#!/bin/bash
R=/home/user/trading-bot/strategy_designer_v2; cd $R
until [ "$(grep -c '^===== exit' $R/runs/_night_2026-11-06_repair.log 2>/dev/null)" -ge 3 ]; do sleep 30; done
for pair in "n19_altcoin_daily_momentum_1d A" "n20_compression_breakout_alts_daily_1d A" "n21_candle_patterns_daily_1d C" "n22_friday_effect_hourly_resolution_1h B" "n23_weekday_gated_trend_hourly_1h C"; do
  set -- $pair; echo "===== $1 fold $2 $(date -u +%H:%M)"
  timeout 3600 python3 $R/run.py $R/briefs/$1.md --fold $2 --rounds 2 2>&1 | grep -vE "^(INFO|DEBUG|WARNING)|^\s*$|^\s+(File |~|\^)"
  echo "===== exit $? $(date -u +%H:%M)"
done
