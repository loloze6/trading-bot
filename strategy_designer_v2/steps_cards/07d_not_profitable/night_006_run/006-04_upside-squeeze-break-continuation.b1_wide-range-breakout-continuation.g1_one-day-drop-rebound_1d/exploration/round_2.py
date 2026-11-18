import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    out = {}
    bars = data["bars"]; days = data["days"]
    coins = list(bars.keys())
    wins = [f"w{i}" for i in range(1, 25)]
    R = []
    for c in coins:
        for w in wins:
            if w not in bars[c]: continue
            b = bars[c][w]
            cl = b.close
            r1 = cl.pct_change()
            fwd = cl.shift(-1) / cl - 1
            vol20 = r1.rolling(20).std()
            vol60 = r1.rolling(60, min_periods=20).std()
            rng = (b.high - b.low) / cl
            rng_ratio = rng.rolling(10).mean() / rng.rolling(60, min_periods=20).mean()
            alloc = b.postRebalance_current_allocation
            R.append(pd.DataFrame({"coin": c, "w": w, "pos": np.arange(len(b)), "f": b.forecast,
                                   "fwd": fwd, "volratio": vol20 / vol60, "rngratio": rng_ratio,
                                   "alloc": alloc, "gain": alloc * fwd}))
    R = pd.concat(R).dropna()
    cm = R.groupby("coin").fwd.mean()
    R["ex"] = R.fwd - R.coin.map(cm)
    A = R[R.f > 0].copy()
    q = A.volratio.quantile([0.2, 0.4, 0.6, 0.8]).values
    A["vol_q"] = np.searchsorted(q, A.volratio)
    # slope of ex on f within each volratio quintile
    rows = []
    for k, g in A.groupby("vol_q"):
        s = stats.linregress(g.f, g.ex)
        rows.append({"vol_q": k, "n": len(g), "slope": s.slope, "t": s.slope / s.stderr,
                     "gain_sum": g.gain.sum(), "loss_days_share": (g.gain < 0).mean()})
    out["slope by volratio q"] = pd.DataFrame(rows).set_index("vol_q")
    # range-compression quintile
    A["rng_q"] = pd.qcut(A.rngratio, 5, labels=False)
    out["by range ratio q"] = A.groupby("rng_q").agg(n=("ex", "size"), ex=("ex", "mean"),
                                                     gain=("gain", "mean"), alloc=("alloc", "mean"))
    # interaction regression
    X = np.column_stack([np.ones(len(A)), A.f, A.volratio, A.f * A.volratio])
    y = A.ex.values
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    res = y - X @ beta
    cov = np.linalg.inv(X.T @ X) * (res @ res) / (len(y) - 4)
    out["interaction f*volratio"] = pd.Series(beta / np.sqrt(np.diag(cov)), index=["c", "f", "vr", "f_x_vr"]).rename("t").to_frame().assign(beta=beta)
    # simulated book: gain scaled by volratio (clipped 0..2) vs original, daily per window mean over coins
    R["vr_scale"] = R.volratio.clip(0, 2)
    R["gain_s"] = R.gain * R.vr_scale
    def book(col):
        D = R.groupby(["w", "pos"])[col].mean().reset_index()
        D["wn"] = D.w.str[1:].astype(int)
        D = D.sort_values(["wn", "pos"])
        eq = (1 + D[col]).cumprod()
        dd = (eq / eq.cummax() - 1).min()
        yr = eq.iloc[-1] ** (365 / len(D)) - 1
        return {"mean": D[col].mean(), "sharpe": D[col].mean() / D[col].std() * np.sqrt(365),
                "maxdd": dd, "yearly": yr, "calmar": yr / -dd}
    out["sim books (pre-fee)"] = pd.DataFrame({"orig": book("gain"), "vr_scaled": book("gain_s")})
    # share of loss in worst 10% book days by vol_q
    D = R.groupby(["w", "pos"]).gain.mean()
    worst = D[D <= D.quantile(0.05)].index
    Rw = R.set_index(["w", "pos"]).loc[worst]
    Rw = Rw[Rw.f > 0]
    Rw["vol_q"] = np.searchsorted(q, Rw.volratio)
    out["worst 5% book days: loss by vol_q"] = Rw.groupby("vol_q").gain.agg(["size", "sum"])
    return out
