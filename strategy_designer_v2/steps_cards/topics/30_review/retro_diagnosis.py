"""The diagnosis on every record with bar files; one JSON line per record with its step 5 and step 6 results."""
import sys, json, pathlib, subprocess
from concurrent.futures import ThreadPoolExecutor
ST = pathlib.Path("/home/user/trading-bot/strategy_designer_v2/steps_cards")
PY = sys.executable
OUT = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else pathlib.Path("/tmp/retro_out")
sys.path.insert(0, str(ST / "common"))
from book_diagnosis import horizon_of
def res(path):
    try: return json.loads(path.read_text())
    except Exception: return None
def one(rec):
    run = rec.parent.parent.name; pid = rec.name
    v = res(ST/"05_verification"/run/"verdicts"/pid/"result.json") or next((res(p) for p in (ST/"05_verification"/run).glob(f"**/{pid}/result.json")), None)
    c = res(ST/"06_profitability"/run/"checks"/pid/"result.json")
    row = {"run": run, "pid": pid, "step5": (v or {}).get("status"), "step6": (c or {}).get("status")}
    if c: row.update({m["measure"]: m["value"] for m in c["measures"]})
    try: H = horizon_of(rec)
    except (SystemExit, OSError):
        import re
        plan = ST/"03_test_plan"/run/"plans"/f"{pid}.md"
        if not plan.exists(): plan = next(iter(ST.glob(f"03_test_plan/*/plans/{pid}.md")), None)
        m = re.search(r"Horizon:\s*(\d+)", plan.read_text()) if plan else None
        if not m: row["error"] = "no plan or no horizon line"; return row
        H = int(m.group(1))
    o = OUT / run / pid
    if not (o / "diagnosis.json").exists():
        r = subprocess.run([PY, str(ST/"common/book_diagnosis.py"), str(rec), "--horizon", str(H), "--out-dir", str(o)], capture_output=True, text=True)
        if r.returncode: row["error"] = r.stderr.strip().splitlines()[-1][:120] if r.stderr.strip() else "failed"; return row
    w = json.loads((o/"diagnosis.json").read_text())["whole_book"]
    row.update(H=H, bets=w["bets_read"], move=w["1_big_enough"]["move_over_horizon"], trip=w["1_big_enough"]["round_trip_cost"],
               bar0=w["2_opening_time"]["move_on_bar_0"], peak_bar=w["3_closing_time"]["peak_bar"], at2H=w["3_closing_time"]["move_at_2H"],
               past=w["4_holding_past_the_bets"]["share_past_the_bets"], market=w["5_trend"]["market_share"], book_day=w["5_trend"]["book_mean_daily_gain"])
    return row
recs = [d for r in sorted((ST/"04_backtest").iterdir()) if r.name.endswith("_run") for d in sorted((r/"backtests").glob("*")) if (d/"run.md").exists() and list(d.glob("*/w*/bars.csv.gz"))]
with ThreadPoolExecutor(3) as ex, open(OUT.parent/"rows.jsonl", "w") as f:
    for row in ex.map(one, recs):
        f.write(json.dumps(row) + "\n"); f.flush()
print("done", len(recs))
