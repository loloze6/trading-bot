import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]; days = data["days"]
    h = 336
    tmp = []
    for coin, ws in bars.items():
        allg = []; parts = []
        for w, df in ws.items():
            c = df["close"].values; n = len(c)
            idx = np.arange(0, n - h, h)
            if len(idx) == 0: continue
            fr = c[idx + h] / c[idx] - 1
            allg.append(fr)
            parts.append(pd.DataFrame({"coin": coin, "w": w, "fr": fr,
                                       "f": df["forecast"].values[idx],
                                       "reg": df["regime"].values[idx]}))
        m = np.concatenate(allg).mean()
        t = pd.concat(parts); t["ex"] = t["fr"] - m
        tmp.append(t)
    d = pd.concat(tmp); d = d[d["reg"] == "trending"].dropna(subset=["f", "ex"])
    out = {}
    sp = stats.spearmanr(d["f"], d["ex"])
    lo, hi = d["ex"].quantile([0.025, 0.975])
    dw = d.copy(); dw["exw"] = dw["ex"].clip(lo, hi)
    rw = stats.linregress(dw["f"], dw["exw"])
    srt = d.sort_values("ex", ascending=False)
    res = []
    for k in [0, 3, 5, 10]:
        dd = srt.iloc[k:]
        r = stats.linregress(dd["f"], dd["ex"])
        res.append({"drop_top_k": k, "slope": r.slope, "t": r.slope / r.stderr, "n": len(dd)})
    out["slope dropping largest excess"] = pd.DataFrame(res)
    out["robust"] = pd.DataFrame({"spearman_rho": [sp.correlation], "spearman_p": [sp.pvalue],
                                  "winsor_slope": [rw.slope], "winsor_t": [rw.slope / rw.stderr]})
    top = d[d["f"] > 10]
    out["top bin by coin"] = top.groupby("coin")["ex"].agg(["count", "mean", "median", lambda s: (s > 0).mean()])
    out["share positive by bin"] = d.assign(q=pd.cut(d["f"], [-0.01, 0, 5, 10, 20.1])).groupby("q")["ex"].apply(lambda s: (s > 0).mean())
    # book daily: gross vs fee, timing
    rows = []
    for coin, ws in bars.items():
        dd = pd.concat([days[coin][w] for w in ws])
        mcr = dd["coin_return"].mean()
        for w, df in ws.items():
            df = df.copy()
            df["day"] = pd.to_datetime(df["timestamp"]).dt.floor("D")
            c = df["close"].values
            a = df["postRebalance_current_allocation"].fillna(0).values
            g = np.r_[a[:-1] * (c[1:] / c[:-1] - 1), 0]
            fee = ((df["total_portfolio_value"] - df["postRebalance_total_value"]) / df["total_portfolio_value"]).fillna(0).values
            df["g"] = g; df["fee"] = fee; df["a"] = a
            agg = df.groupby("day").agg(g=("g", "sum"), fee=("fee", "sum"), a=("a", "mean"))
            agg["mkt"] = agg["a"] * mcr
            agg["coin"] = coin
            rows.append(agg)
    b = pd.concat(rows)
    out["book daily per coin-day"] = pd.DataFrame({"gross_mean": [b["g"].mean()], "fee_mean": [b["fee"].mean()],
                                     "net_approx": [(b["g"] - b["fee"]).mean()], "mkt_part": [b["mkt"].mean()],
                                     "gross_timing": [(b["g"] - b["mkt"]).mean()], "mean_alloc": [b["a"].mean()]})
    out["book gross by coin"] = b.groupby("coin")[["g", "fee", "mkt"]].mean()
    return out
