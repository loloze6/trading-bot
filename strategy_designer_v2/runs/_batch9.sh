#!/bin/bash
# exact replication of the engine-passing claims on other coins, same fold, same code, no model call
R=/home/user/trading-bot/strategy_designer_v2; cd $R
until [ "$(grep -c '^===== exit' $R/runs/_night_2026-11-06_batch8.log 2>/dev/null)" -ge 3 ]; do sleep 30; done
rep() { echo "===== replicate $2 on $5 fold $3 $(date -u +%H:%M)"; timeout 3600 python3 $R/steps/replicate.py "$1" "$2" "$3" "$4" "$R/runs/_replications/$2" $5 2>&1 | grep -vE "^(INFO|DEBUG|WARNING)|^\s*$"; echo "===== exit $? $(date -u +%H:%M)"; }
rep $R/runs/fake_01_btc_overreaction/001/claims.yaml breakout_spike_continues_inside_spike_reverts A 1h "ETHUSD LTCUSD XRPUSD ADAUSD"
rep $R/runs/n04_btc_daily_vol_timing_1d/001/claims.yaml low_vol_regime_momentum C 1d "ETHUSD LTCUSD XRPUSD"
rep $R/runs/n10_hourly_trend_with_vol_gate_1h/001/claims.yaml donchian_72h_breakout C 1h "LTCUSD XRPUSD"
rep $R/runs/n23_weekday_gated_trend_hourly_1h/001/claims.yaml gated_cross_pays_net C 1h "LTCUSD XRPUSD"
rep $R/runs/n07_calendar_daily_three_coins_1d/001/claims.yaml friday_long_net_profit B 1d "XRPUSD ADAUSD XMRUSD"
