"""Per judged record: the idea's strength = its average move after the signal over its horizon (net of the coin's
drift, in its direction), divided by the coin's typical move over the same horizon (the standard deviation of H-bar
returns over all windows). A pure number: 0.05 means the idea predicts 5 % of a typical move."""
import sys, json, math, pathlib, numpy as np, pandas as pd
from concurrent.futures import ProcessPoolExecutor
sys.path.insert(0, "/home/user/trading-bot/strategy_designer_v2/steps_cards/common")
from book_diagnosis import bets, band_of
ST = pathlib.Path("/home/user/trading-bot/strategy_designer_v2/steps_cards")
def one(a):
    run, pid, H = a; rec = ST/"04_backtest"/run/"backtests"/pid; band = band_of(rec); x = []; sig = []
    for cd in (p for p in rec.iterdir() if p.is_dir()):
        frames = [pd.read_csv(f, usecols=["close", "forecast"]) for f in cd.glob("w*/bars.csv.gz")]
        if not frames: continue
        hr = np.concatenate([fr.close.to_numpy()[H::H] / fr.close.to_numpy()[:-H:H][:len(fr.close.to_numpy()[H::H])] - 1 for fr in frames if len(fr) > 2 * H])
        if len(hr) < 3: continue
        drift, sd = hr.mean(), hr.std(ddof=1)
        for fr in frames:
            c = fr.close.to_numpy(); fc = fr.forecast.fillna(0).to_numpy(); seen = set()
            for t in bets(fc, band):
                if t + H >= len(c) or t // H in seen: continue
                seen.add(t // H); x.append(np.sign(fc[t]) * (c[t + H] / c[t] - 1 - drift) / sd); sig.append(sd)
    return run, pid, float(np.mean(x)) if x else float("nan"), float(np.median(sig)) if sig else float("nan")
if __name__ == "__main__":
    d = pd.read_csv(sys.argv[1])
    with ProcessPoolExecutor(3) as ex:
        res = list(ex.map(one, [(r.run, r.pid, int(r.H)) for r in d.itertuples()]))
    pd.DataFrame(res, columns=["run", "pid", "strength", "typical_move"]).to_csv(sys.argv[2], index=False)
