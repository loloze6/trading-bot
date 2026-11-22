import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    out = {}
    rows = []
    cases = []
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True).copy()
            b["ts"] = pd.to_datetime(b["timestamp"])
            cl = b["close"]
            r = cl.pct_change()
            alloc = b["postRebalance_current_allocation"].fillna(0)
            b["gain"] = alloc * (cl.shift(-1) / cl - 1)
            b["ret30"] = cl / cl.shift(180) - 1
            b["vol30"] = r.rolling(180, min_periods=60).std()
            b["vol5"] = r.rolling(30, min_periods=15).std()
            b["vratio"] = b["vol5"] / b["vol30"]
            b["dd60"] = cl / cl.rolling(360, min_periods=60).max() - 1
            b["fwd18"] = cl.shift(-18) / cl - 1
            b["coin"] = c; b["wn"] = int(w[1:]); b["alloc"] = alloc; b["r1"] = cl.shift(-1) / cl - 1
            rows.append(b[["coin", "wn", "alloc", "gain", "r1", "ret30", "vratio", "dd60", "fwd18", "forecast"]])
            # cases on grid: first bar per 18-grid cell with forecast rise
            f = b["forecast"].fillna(0).values
            grid = np.arange(len(b)) // 18
            seen = set()
            for k in range(1, len(b) - 18):
                if f[k] >= 2 and f[k] - f[k - 1] >= 2 and grid[k] not in seen:
                    seen.add(grid[k])
                    cases.append(dict(coin=c, wn=int(w[1:]), fwd=b["fwd18"].iloc[k], ret30=b["ret30"].iloc[k],
                                      vratio=b["vratio"].iloc[k], dd60=b["dd60"].iloc[k], fc=f[k]))
    B = pd.concat(rows).dropna(subset=["gain"])
    drift = B.groupby("coin").r1.mean()
    B["mkt"] = B["alloc"] * B["coin"].map(drift)
    out["exposure"] = pd.Series({"mean_alloc": B.alloc.mean(), "share_bars_in": (B.alloc.abs() > 0.01).mean(),
                                 "mean_gain_bar": B.gain.mean(), "mkt_part": B.mkt.mean(),
                                 "timing_part": B.gain.mean() - B.mkt.mean()})
    for col in ["ret30", "vratio", "dd60"]:
        g = B.dropna(subset=[col]).copy()
        g["q"] = pd.qcut(g[col], 5, labels=False, duplicates="drop")
        a = g.groupby("q").agg(lo=(col, "min"), hi=(col, "max"), alloc=("alloc", "mean"), gain_bp=("gain", lambda v: v.mean() * 1e4),
                               coin_bp=("r1", lambda v: v.mean() * 1e4), gain_sd_bp=("gain", lambda v: v.std() * 1e4))
        a["timing_bp"] = (g.groupby("q").apply(lambda x: (x.gain - x.alloc * x.coin.map(drift)).mean()) * 1e4)
        out["book_by_" + col] = a.round(3)
    C = pd.DataFrame(cases)
    cd = C.coin.map(B.groupby("coin").apply(lambda x: np.nan))  # placeholder
    # normal 18-bar drift per coin approximated by 18*mean bar return
    C["ex"] = C.fwd - C.coin.map(drift * 18)
    out["cases_n"] = len(C)
    for col in ["ret30", "vratio", "dd60", "fc"]:
        g = C.dropna(subset=[col, "ex"]).copy()
        g["q"] = pd.qcut(g[col], 5, labels=False, duplicates="drop")
        out["case_ex_by_" + col] = g.groupby("q").agg(lo=(col, "min"), hi=(col, "max"), n=("ex", "size"),
                                                      ex_pct=("ex", lambda v: v.mean() * 100),
                                                      t=("ex", lambda v: v.mean() / (v.std() / np.sqrt(len(v)))),
                                                      p10=("ex", lambda v: v.quantile(.1) * 100)).round(3)
    # deepest fall windows 16-17: book by coin
    F = B[B.wn.isin([16, 17])]
    out["w16_17_by_coin"] = F.groupby(["wn", "coin"]).agg(alloc=("alloc", "mean"), gain_sum=("gain", "sum"), coin_sum=("r1", "sum")).round(3)
    return out
