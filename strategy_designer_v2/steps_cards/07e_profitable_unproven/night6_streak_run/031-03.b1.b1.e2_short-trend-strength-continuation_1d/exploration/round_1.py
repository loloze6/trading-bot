import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    out = {}
    bars = data["bars"]
    rows = []
    for c in bars:
        for w, b in bars[c].items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            cl = b["close"].astype(float)
            r = cl.pct_change()
            alloc = b["postRebalance_current_allocation"].astype(float)
            pv = b["postRebalance_total_value"].astype(float)
            br = pv.pct_change()
            vol = r.rolling(60, min_periods=30).std()
            s10 = (cl / cl.shift(10) - 1) / vol
            ts = pd.to_datetime(b["timestamp"])
            df = pd.DataFrame({"coin": c, "win": w, "pos": np.arange(len(b)), "ts": ts,
                               "year": ts.dt.year, "r": r, "br": br, "alloc_prev": alloc.shift(1),
                               "s10": s10, "fc": b["forecast"].astype(float), "cl": cl})
            for h in (1, 5, 10, 20):
                df[f"f{h}"] = cl.shift(-h) / cl - 1
            rows.append(df)
    D = pd.concat(rows, ignore_index=True)
    mu = D.groupby("coin")["r"].mean()
    D["mu"] = D["coin"].map(mu)
    D["mkt"] = D["alloc_prev"] * D["mu"]
    D["timing"] = D["alloc_prev"] * (D["r"] - D["mu"])
    day = D.dropna(subset=["br"]).groupby(["win", "ts"]).agg(br=("br", "mean"), hold=("r", "mean"),
                                                              mkt=("mkt", "mean"), tim=("timing", "mean"),
                                                              year=("year", "first"))
    n = len(day)
    out["book split"] = pd.Series({
        "days": n, "book mean": day.br.mean(), "book sharpe": day.br.mean()/day.br.std()*np.sqrt(365),
        "market part": day.mkt.mean(), "timing part": day.tim.mean(),
        "timing t": day.tim.mean()/(day.tim.std()/np.sqrt(n)),
        "hold mean": day.hold.mean(), "hold sharpe": day.hold.mean()/day.hold.std()*np.sqrt(365)})
    # by coin
    bc = D.dropna(subset=["br"]).groupby("coin").agg(book=("br", "mean"), mkt=("mkt", "mean"),
                                                     tim=("timing", "mean"), hold=("r", "mean"),
                                                     inpos=("alloc_prev", lambda x: (x.abs() > 1e-9).mean()))
    out["by coin (daily means)"] = bc.round(5)
    out["by year"] = day.groupby("year").agg(book=("br", "mean"), hold=("hold", "mean"),
                                             mkt=("mkt", "mean"), tim=("tim", "mean"), n=("br", "size")).round(5)
    # top days concentration
    s = day.br.sort_values(ascending=False)
    out["book sum, share from top 1% days"] = float(s.head(int(n*0.01)).sum() / s.sum())
    # in vs out: daily coin return by position state
    D["state"] = np.where(D["alloc_prev"].abs() > 1e-9, "in", "out")
    st = D.dropna(subset=["r"]).groupby("state")["r"].agg(["mean", "std", "count"])
    out["coin daily return by state"] = st
    out["in minus out welch t"] = float(stats.ttest_ind(D.loc[D.state=="in","r"].dropna(),
                                                       D.loc[D.state=="out","r"].dropna(), equal_var=False).statistic)
    # forward excess by scaled 10d return bins, non-overlapping grid per horizon
    res = []
    for h in (1, 5, 10, 20):
        g = D[(D.pos % h == 0)].dropna(subset=["s10", f"f{h}"]).copy()
        drift = g.groupby("coin")[f"f{h}"].mean()
        g["ex"] = g[f"f{h}"] - g["coin"].map(drift)
        g["bin"] = pd.qcut(g["s10"], 5, labels=False)
        for bi, gg in g.groupby("bin"):
            res.append({"h": h, "bin": bi, "s10 mid": gg.s10.median(), "ex mean": gg.ex.mean(),
                        "t": gg.ex.mean()/(gg.ex.std()/np.sqrt(len(gg))), "n": len(gg)})
        sl = stats.linregress(g["s10"], g["ex"])
        res.append({"h": h, "bin": "slope all", "s10 mid": sl.slope, "ex mean": np.nan,
                    "t": sl.slope/sl.stderr, "n": len(g)})
        neg = g[g.s10 < 0]
        sl = stats.linregress(neg["s10"], neg["ex"])
        res.append({"h": h, "bin": "slope neg", "s10 mid": sl.slope, "ex mean": np.nan,
                    "t": sl.slope/sl.stderr, "n": len(neg)})
    out["fwd excess by s10 quintile"] = pd.DataFrame(res).round(5)
    return out
