#!/bin/bash
# waits for the resume job to finish (three exit lines), then runs batch 2 sequentially
cd /home/user/trading-bot/strategy_designer_v2
until [ "$(grep -c '^===== exit' runs/_night_2026-11-06_resume.log 2>/dev/null)" -ge 3 ]; do sleep 20; done
for pair in "n06_range_break_continuation_other_coins_1h B" "n07_calendar_daily_three_coins_1d B" "n08_opening_range_breakout_eth_1h C" "n09_long_horizon_reversal_book_1d A" "n10_hourly_trend_with_vol_gate_1h C"; do
  set -- $pair; echo "===== $1 fold $2 $(date -u +%H:%M)"
  timeout 3600 python3 run.py briefs/$1.md --fold $2 --rounds 2 2>&1 | grep -vE "^(INFO|DEBUG|WARNING)|^\s*$|^\s+(File |~|\^)"
  echo "===== exit $? $(date -u +%H:%M)"
done
