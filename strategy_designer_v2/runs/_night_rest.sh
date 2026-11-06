#!/bin/bash
# everything that was queued when the container restarted, in one chain, one process at a time
cd /home/user/trading-bot/strategy_designer_v2
R=/home/user/trading-bot/strategy_designer_v2
for pair in "n10_hourly_trend_with_vol_gate_1h C" "n11_daily_gate_hourly_entry_1h A" "n12_short_horizon_daily_reversion_1d B" "n13_quiet_period_then_move_btc_1h C" "n14_dollar_volume_regime_memecoins_1d B" "n15_eth_hourly_momentum_horizons_1h A"; do
  set -- $pair; echo "===== $1 fold $2 $(date -u +%H:%M)"
  timeout 3600 python3 $R/run.py $R/briefs/$1.md --fold $2 --rounds 2 2>&1 | grep -vE "^(INFO|DEBUG|WARNING)|^\s*$|^\s+(File |~|\^)"
  echo "===== exit $? $(date -u +%H:%M)"
done
echo "===== engine two sizes: n04 low_vol_regime_momentum $(date -u +%H:%M)"
rm -rf $R/runs/n04_btc_daily_vol_timing_1d/001/engine_r0_low_vol_regime_momentum_BTCUSD
timeout 3600 python3 $R/steps/engine/backtest.py $R/runs/n04_btc_daily_vol_timing_1d/001/claims.yaml low_vol_regime_momentum C 1d BTCUSD $R/runs/n04_btc_daily_vol_timing_1d/001/engine_r0_low_vol_regime_momentum_BTCUSD 2>&1 | grep -vE "^(INFO|DEBUG|WARNING)|^\s*$"
echo "===== exit $? $(date -u +%H:%M)"
for pair in "n06_range_break_continuation_other_coins_1h A" "n14_dollar_volume_regime_memecoins_1d A" "n16_day_of_week_other_coins_1d A" "n17_vol_channel_breakout_daily_1d B" "n18_payment_coins_hourly_shock_1h A"; do
  set -- $pair; echo "===== $1 fold $2 $(date -u +%H:%M)"
  timeout 3600 python3 $R/run.py $R/briefs/$1.md --fold $2 --rounds 2 2>&1 | grep -vE "^(INFO|DEBUG|WARNING)|^\s*$|^\s+(File |~|\^)"
  echo "===== exit $? $(date -u +%H:%M)"
done
