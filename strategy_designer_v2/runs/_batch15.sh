#!/bin/bash
R=/home/user/trading-bot/strategy_designer_v2; cd $R
until [ "$(grep -c '^===== exit' $R/runs/_night_2026-11-06_batch14.log 2>/dev/null)" -ge 5 ]; do sleep 30; done
echo "===== n33_volume_price_divergence_daily_1d fold A $(date -u +%H:%M)"
timeout 3600 python3 $R/run.py $R/briefs/n33_volume_price_divergence_daily_1d.md --fold A --rounds 2 2>&1 | grep -vE "^(INFO|DEBUG|WARNING)|^\s*$|^\s+(File |~|\^)"
echo "===== exit $? $(date -u +%H:%M)"
