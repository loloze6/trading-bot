#!/bin/bash
# after batch 3: re-run the engine on n04's book with both sizes (the n04 ask), then the n03 books for the record
cd /home/user/trading-bot/strategy_designer_v2
until [ "$(grep -c '^===== exit' /home/user/trading-bot/strategy_designer_v2/runs/_night_2026-11-06_batch3.log 2>/dev/null)" -ge 5 ]; do sleep 30; done
echo "===== engine two sizes: n04 low_vol_regime_momentum $(date -u +%H:%M)"
rm -rf runs/n04_btc_daily_vol_timing_1d/001/engine_r0_low_vol_regime_momentum_BTCUSD
timeout 3600 python3 steps/engine/backtest.py runs/n04_btc_daily_vol_timing_1d/001/claims.yaml low_vol_regime_momentum C 1d BTCUSD runs/n04_btc_daily_vol_timing_1d/001/engine_r0_low_vol_regime_momentum_BTCUSD 2>&1 | grep -vE "^(INFO|DEBUG|WARNING)|^\s*$"
echo "===== exit $? $(date -u +%H:%M)"
