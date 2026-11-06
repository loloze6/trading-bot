#!/bin/bash
R=/home/user/trading-bot/strategy_designer_v2; cd $R
until [ "$(grep -c '^===== exit' $R/runs/_night_2026-11-06_batch10.log 2>/dev/null)" -ge 2 ]; do sleep 30; done
echo "===== replicate friday_long_net_profit on XRPUSD ADAUSD XMRUSD fold B $(date -u +%H:%M)"
timeout 3600 python3 $R/steps/replicate.py $R/runs/n07_calendar_daily_three_coins_1d/001/claims.yaml friday_long_net_profit B 1d $R/runs/_replications/friday_long_net_profit XRPUSD ADAUSD XMRUSD 2>&1 | grep -vE "^(INFO|DEBUG|WARNING)|^\s*$"
echo "===== exit $? $(date -u +%H:%M)"
echo "===== replicate volume_burst_stretch_pullback_bar_continues on ETHUSD ADAUSD fold C $(date -u +%H:%M)"
timeout 3600 python3 $R/steps/replicate.py $R/runs/n28_hourly_stretch_reversion_older_coins_1h/001/claims.yaml volume_burst_stretch_pullback_bar_continues C 1h $R/runs/_replications/volume_burst_stretch_pullback_bar_continues ETHUSD ADAUSD 2>&1 | grep -vE "^(INFO|DEBUG|WARNING)|^\s*$"
echo "===== exit $? $(date -u +%H:%M)"
