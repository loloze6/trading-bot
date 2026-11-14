#!/bin/bash
cd /home/user/trading-bot/strategy_designer_v2
until [ "$(grep -c '^===== exit' /home/user/trading-bot/strategy_designer_v2/runs/_night_2026-11-06_batch2.log 2>/dev/null)" -ge 5 ]; do sleep 30; done
for pair in "n11_daily_gate_hourly_entry_1h A" "n12_short_horizon_daily_reversion_1d B" "n13_quiet_period_then_move_btc_1h C" "n14_dollar_volume_regime_memecoins_1d B" "n15_eth_hourly_momentum_horizons_1h A"; do
  set -- $pair; echo "===== $1 fold $2 $(date -u +%H:%M)"
  timeout 3600 python3 /home/user/trading-bot/strategy_designer_v2/run.py /home/user/trading-bot/strategy_designer_v2/briefs/$1.md --fold $2 --rounds 2 2>&1 | grep -vE "^(INFO|DEBUG|WARNING)|^\s*$|^\s+(File |~|\^)"
  echo "===== exit $? $(date -u +%H:%M)"
done
