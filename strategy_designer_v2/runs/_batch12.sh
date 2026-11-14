#!/bin/bash
R=/home/user/trading-bot/strategy_designer_v2; cd $R
until [ "$(grep -c '^===== exit' $R/runs/_night_2026-11-06_batch11.log 2>/dev/null)" -ge 2 ]; do sleep 30; done
echo "===== lite books for every judge-passed return claim $(date -u +%H:%M)"
timeout 3600 python3 $R/records/lite_books.py 2>&1 | grep -vE "^(INFO|DEBUG|WARNING)|^\s*$"
echo "===== exit $? $(date -u +%H:%M)"
