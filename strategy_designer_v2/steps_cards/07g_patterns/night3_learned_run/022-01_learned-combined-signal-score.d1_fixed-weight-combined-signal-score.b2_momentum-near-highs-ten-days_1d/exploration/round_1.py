import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]; days = data["days"]
    rows = []
    for coin, wins in bars.items():
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            c = b["close"].astype(float)
            r1 = c.pct_change()
            df = pd.DataFrame({
                "coin": coin, "win": w, "pos": np.arange(len(b)),
                "fc": b["forecast"].astype(float),
                "mom": b.get("debug_info.components.mom28.post_pipeline_value", np.nan),
                "nh": b.get("debug_info.components.near_high90.post_pipeline_value", np.nan),
                "nhraw": b.get("debug_info.components.near_high90.last_history_value", np.nan),
                "alloc": b["postRebalance_current_allocation"].astype(float),
                "r1": r1,
                "z1": r1 / r1.rolling(30, min_periods=15).std().shift(1),
                "vol30": r1.rolling(30, min_periods=15).std(),
                "r5back": c / c.shift(5) - 1,
                "wd": pd.to_datetime(b["timestamp"]).dt.weekday,
                "year": pd.to_datetime(b["timestamp"]).dt.year,
            })
            for h in (1, 3, 10, 20):
                df[f"f{h}"] = c.shift(-h) / c - 1
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    for col in ["mom", "nh", "nhraw"]:
        A[col] = pd.to_numeric(A[col], errors="coerce")
    out = {}
    # drifts per coin per horizon on own grid
    for h in (1, 3, 10, 20):
        g = A[A["pos"] % h == 0]
        d = g.groupby("coin")[f"f{h}"].mean()
        A[f"u{h}"] = A[f"f{h}"] - A["coin"].map(d)
        A[f"g{h}"] = (A["pos"] % h == 0)
    A["volrank"] = A.groupby("coin")["vol30"].rank(pct=True)
    A["fcrank"] = A.groupby("coin")["fc"].rank(pct=True)
    def qtab(var, h, nq=5):
        g = A[A[f"g{h}"]].dropna(subset=[var, f"u{h}"]).copy()
        g["q"] = g.groupby("coin")[var].transform(lambda s: pd.qcut(s.rank(method="first"), nq, labels=False))
        t = g.groupby("q")[f"u{h}"].agg(["mean", "std", "count"])
        t["t"] = t["mean"] / (t["std"] / np.sqrt(t["count"]))
        return t.drop(columns="std")
    out["fc_q_u10"] = qtab("fc", 10)
    out["fc_q_u20"] = qtab("fc", 20)
    out["mom_q_u10"] = qtab("mom", 10)
    out["nh_q_u10"] = qtab("nh", 10)
    out["z1_q_u3"] = qtab("z1", 3)
    out["z1_q_u10"] = qtab("z1", 10)
    out["r5_q_u10"] = qtab("r5back", 10)
    out["vol_q_u10"] = qtab("vol30", 10)
    # regressions
    g = A[A["g10"]].dropna(subset=["mom", "nh", "u10"])
    res = {}
    for xs in (["mom"], ["nh"], ["mom", "nh"]):
        X = np.column_stack([np.ones(len(g))] + [g[x].values for x in xs])
        y = g["u10"].values
        beta, *_ = np.linalg.lstsq(X, y, rcond=None)
        e = y - X @ beta
        s2 = e @ e / (len(y) - X.shape[1])
        se = np.sqrt(np.diag(s2 * np.linalg.inv(X.T @ X)))
        for i, x in enumerate(xs):
            res["+".join(xs) + ":" + x] = {"slope": beta[i+1], "t": beta[i+1]/se[i+1], "n": len(y)}
    out["regs"] = pd.DataFrame(res).T
    # per coin slope of fc
    pc = {}
    for coin, gg in A[A["g10"]].dropna(subset=["fc", "u10"]).groupby("coin"):
        s = stats.linregress(gg["fc"], gg["u10"])
        pc[coin] = {"slope": s.slope, "t": s.slope/s.stderr, "n": len(gg)}
    out["per_coin_fc"] = pd.DataFrame(pc).T
    # side
    g = A[A["g10"]].dropna(subset=["fc", "u10"]).copy()
    g["side"] = np.sign(g["fc"])
    g["signed"] = g["u10"] * g["side"]
    t = g.groupby("side")["signed"].agg(["mean", "std", "count"]); t["t"] = t["mean"]/(t["std"]/np.sqrt(t["count"]))
    out["side_signed_u10"] = t.drop(columns="std")
    # weekday next-day
    g = A.dropna(subset=["u1"])
    t = g.groupby("wd")["u1"].agg(["mean", "std", "count"]); t["t"] = t["mean"]/(t["std"]/np.sqrt(t["count"]))
    out["weekday_u1"] = t.drop(columns="std")
    # vol regime x fc interaction
    g = A[A["g10"]].dropna(subset=["fc", "u10", "volrank"]).copy()
    g["vh"] = (g["volrank"] > 0.5).astype(int)
    vi = {}
    for k, gg in g.groupby("vh"):
        s = stats.linregress(gg["fc"], gg["u10"]); vi[k] = {"slope": s.slope, "t": s.slope/s.stderr, "n": len(gg)}
    out["fc_slope_by_vol_half"] = pd.DataFrame(vi).T
    # book by year
    D = []
    for coin, wins in days.items():
        for w, d in wins.items():
            d = d.copy(); d["coin"] = coin; d["win"] = w; D.append(d)
    D = pd.concat(D, ignore_index=True)
    D["year"] = pd.to_datetime(D["day"]).dt.year
    bk = D.groupby(["year", "day"])[["book_return", "coin_return"]].mean().groupby("year").agg(["mean", "std", "count"])
    out["book_by_year"] = bk
    return out
