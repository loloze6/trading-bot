#!/bin/bash
# after the rest chain (12 exit lines): resume the three runs that died (n06 AVAX warm-up, n12 and n15 malformed next claim)
R=/home/user/trading-bot/strategy_designer_v2; cd $R
until [ "$(grep -c '^===== exit' $R/runs/_night_2026-11-06_rest.log 2>/dev/null)" -ge 12 ]; do sleep 30; done
for pair in "n06_range_break_continuation_other_coins_1h A" "n12_short_horizon_daily_reversion_1d B" "n15_eth_hourly_momentum_horizons_1h A"; do
  set -- $pair; echo "===== resume $1 fold $2 $(date -u +%H:%M)"
  timeout 3600 python3 $R/run.py $R/briefs/$1.md --fold $2 --rounds 2 2>&1 | grep -vE "^(INFO|DEBUG|WARNING)|^\s*$|^\s+(File |~|\^)"
  echo "===== exit $? $(date -u +%H:%M)"
done
