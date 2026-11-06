#!/bin/bash
R=/home/user/trading-bot/strategy_designer_v2; cd $R
until [ "$(grep -c '^===== exit' $R/runs/_night_2026-11-06_repair2.log 2>/dev/null)" -ge 3 ]; do sleep 30; done
for pair in "n24_hourly_donchian_other_coins_1h A" "n25_low_vol_momentum_other_coins_1d A" "n26_session_reversal_hourly_1h C" "n27_drawdown_state_daily_1d B" "n28_hourly_stretch_reversion_older_coins_1h C"; do
  set -- $pair; echo "===== $1 fold $2 $(date -u +%H:%M)"
  timeout 3600 python3 $R/run.py $R/briefs/$1.md --fold $2 --rounds 2 2>&1 | grep -vE "^(INFO|DEBUG|WARNING)|^\s*$|^\s+(File |~|\^)"
  echo "===== exit $? $(date -u +%H:%M)"
done
