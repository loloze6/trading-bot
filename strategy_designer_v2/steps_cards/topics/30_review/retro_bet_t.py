"""Candidate D on the records: the t of the move per bet (the bets of core/holding_period.py: a rise of the forecast of
at least the band; one bet per grid cell of H bars, so moves are not counted twice), from the close of the signal's bar
over H bars, net of the coin's mean H-bar return over all its windows (measures.md), in the bet's direction."""
import sys, json, math, pathlib, numpy as np, pandas as pd
from concurrent.futures import ProcessPoolExecutor
sys.path.insert(0, "/home/user/trading-bot/strategy_designer_v2/steps_cards/common")
from book_diagnosis import bets, band_of
ST = pathlib.Path("/home/user/trading-bot/strategy_designer_v2/steps_cards")
def one(a):
    run, pid, H = a; rec = ST/"04_backtest"/run/"backtests"/pid; band = band_of(rec); x = []
    for cd in (p for p in rec.iterdir() if p.is_dir()):
        frames = [pd.read_csv(f, usecols=["close", "forecast"]) for f in cd.glob("w*/bars.csv.gz")]
        if not frames: continue
        hr = np.concatenate([fr.close.to_numpy()[H:] / fr.close.to_numpy()[:-H] - 1 for fr in frames if len(fr) > H])
        drift = hr.mean() if len(hr) else 0.0
        for fr in frames:
            c = fr.close.to_numpy(); fc = fr.forecast.fillna(0).to_numpy(); seen = set()
            for t in bets(fc, band):
                if t + H >= len(c) or t // H in seen: continue
                seen.add(t // H); x.append(np.sign(fc[t]) * (c[t + H] / c[t] - 1 - drift))
    x = np.array(x); n = len(x)
    t = x.mean() / (x.std(ddof=1) / math.sqrt(n)) if n > 2 and x.std() > 0 else float("nan")
    return run, pid, n, float(x.mean()) if n else float("nan"), float(t)
if __name__ == "__main__":
    d = pd.read_csv(sys.argv[1]); d = d[d.step5.isin(["confirmed", "inconclusive", "rejected"])]
    args = [(r.run, r.pid, int(r.H)) for r in d.itertuples()]
    with ProcessPoolExecutor(3) as ex, open(sys.argv[2], "w") as f:
        for run, pid, n, m, t in ex.map(one, args):
            f.write(json.dumps({"run": run, "pid": pid, "bets_nonoverlap": n, "bet_mean": m, "bet_t": t}) + "\n"); f.flush()
