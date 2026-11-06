#!/bin/bash
cd /home/user/trading-bot/strategy_designer_v2
until [ "$(grep -c '^===== exit' /home/user/trading-bot/strategy_designer_v2/runs/_night_2026-11-06_batch4.log 2>/dev/null)" -ge 1 ]; do sleep 30; done
for pair in "n06_range_break_continuation_other_coins_1h A" "n14_dollar_volume_regime_memecoins_1d A" "n16_day_of_week_other_coins_1d A" "n17_vol_channel_breakout_daily_1d B" "n18_payment_coins_hourly_shock_1h A"; do
  set -- $pair; echo "===== $1 fold $2 $(date -u +%H:%M)"
  timeout 3600 python3 /home/user/trading-bot/strategy_designer_v2/run.py /home/user/trading-bot/strategy_designer_v2/briefs/$1.md --fold $2 --rounds 2 2>&1 | grep -vE "^(INFO|DEBUG|WARNING)|^\s*$|^\s+(File |~|\^)"
  echo "===== exit $? $(date -u +%H:%M)"
done
