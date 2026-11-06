#!/bin/bash
# code only: the two-size policy applied to the books judged before it existed; one more replication
R=/home/user/trading-bot/strategy_designer_v2; cd $R
until [ "$(grep -c '^===== exit' $R/runs/_night_2026-11-06_batch12.log 2>/dev/null)" -ge 1 ]; do sleep 30; done
eng() { echo "===== engine two sizes: $2 on $5 fold $3 $(date -u +%H:%M)"; rm -rf "$6"; timeout 3600 python3 $R/steps/engine/backtest.py "$1" "$2" "$3" "$4" "$5" "$6" 2>&1 | grep -vE "^(INFO|DEBUG|WARNING)|^\s*$"; echo "===== exit $? $(date -u +%H:%M)"; }
eng $R/runs/fake_01_btc_overreaction/001/claims.yaml breakout_spike_continues_inside_spike_reverts A 1h BTCUSD $R/runs/fake_01_btc_overreaction/001/engine_r0_breakout_spike_continues_inside_spike_reverts_BTCUSD
eng $R/runs/n07_calendar_daily_three_coins_1d/001/claims_r1.yaml friday_long_net_profit B 1d BTCUSD $R/runs/n07_calendar_daily_three_coins_1d/001/engine_r1_friday_long_net_profit_BTCUSD
eng $R/runs/n07_calendar_daily_three_coins_1d/001/claims_r1.yaml friday_long_net_profit B 1d LTCUSD $R/runs/n07_calendar_daily_three_coins_1d/001/engine_r1_friday_long_net_profit_LTCUSD
echo "===== replicate volume_burst_stretch_pullback_bar_continues on BTCUSD LINKUSD fold C $(date -u +%H:%M)"
timeout 3600 python3 $R/steps/replicate.py $R/runs/n28_hourly_stretch_reversion_older_coins_1h/001/claims.yaml volume_burst_stretch_pullback_bar_continues C 1h $R/runs/_replications/volume_burst_stretch_pullback_bar_continues_2 BTCUSD LINKUSD 2>&1 | grep -vE "^(INFO|DEBUG|WARNING)|^\s*$"
echo "===== exit $? $(date -u +%H:%M)"
