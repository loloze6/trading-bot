import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    bars = data["bars"]; days = data["days"]
    rows = []
    for c in bars:
        for w, b in bars[c].items():
            b = b.reset_index(drop=True)
            cl = b["close"].astype(float)
            r1 = cl.pct_change()
            d = pd.DataFrame({
                "coin": c, "w": w,
                "fc": b["forecast"].astype(float),
                "alloc": b["postRebalance_current_allocation"].astype(float),
                "regime": b["regime"],
                "near": b.get("debug_info.components.near_high.last_history_value"),
                "ret30": cl / cl.shift(30) - 1,
                "ret7p": cl / cl.shift(7) - 1,
                "vol20": r1.rolling(20).std(),
                "vrat": b["volume"] / b["volume"].rolling(20).mean(),
                "fwd7": cl.shift(-7) / cl - 1,
                "fwd1": cl.shift(-1) / cl - 1,
                "wd": pd.to_datetime(b["timestamp"]).dt.weekday,
                "pos": np.arange(len(b)),
            })
            rows.append(d)
    df = pd.concat(rows, ignore_index=True)
    df["near"] = pd.to_numeric(df["near"], errors="coerce")
    g = df[df["pos"] % 7 == 0].dropna(subset=["fwd7"]).copy()
    g["ex7"] = g["fwd7"] - g.groupby("coin")["fwd7"].transform("mean")
    out = {}
    def qtab(col, sub, q=5):
        s = sub.dropna(subset=[col, "ex7"]).copy()
        s["q"] = s.groupby("coin")[col].transform(lambda x: pd.qcut(x.rank(method="first"), q, labels=False))
        t = s.groupby("q")["ex7"].agg(["mean", "count", "std"])
        t["t"] = t["mean"] / (t["std"] / np.sqrt(t["count"]))
        lo, hi = s[s.q == 0]["ex7"], s[s.q == q-1]["ex7"]
        t.loc["hi-lo t", "mean"] = stats.ttest_ind(hi, lo, equal_var=False).statistic
        return t.round(4)
    tr = g[g.regime == "trending"]
    out["fc quint (trending)"] = qtab("fc", tr)
    out["near quint (trending)"] = qtab("near", tr)
    out["ret30 quint all"] = qtab("ret30", g)
    out["ret7p quint all"] = qtab("ret7p", g)
    out["vol20 quint all"] = qtab("vol20", g)
    out["vrat quint all"] = qtab("vrat", g)
    s = g.dropna(subset=["ret30"])
    a, b_ = s[s.ret30 > 0]["ex7"], s[s.ret30 <= 0]["ex7"]
    out["ret30>0 minus <=0"] = f"{a.mean()-b_.mean():.4f} t={stats.ttest_ind(a,b_,equal_var=False).statistic:.2f} n={len(a)},{len(b_)}"
    # weekday daily returns
    d1 = df.dropna(subset=["fwd1"]).copy()
    d1["ex1"] = d1["fwd1"] - d1.groupby("coin")["fwd1"].transform("mean")
    wt = d1.groupby("wd")["ex1"].agg(["mean", "count", "std"]); wt["t"] = wt["mean"]/(wt["std"]/np.sqrt(wt["count"]))
    out["weekday next-day excess"] = wt.round(5)
    # positions
    out["alloc share long/short/flat"] = f"long {(df.alloc>0.01).mean():.3f} short {(df.alloc<-0.01).mean():.3f} flat {(df.alloc.abs()<=0.01).mean():.3f}"
    out["fc<0 share in trending"] = f"{(df[df.regime=='trending'].fc<0).mean():.3f}"
    # book by coin
    bk = []
    for c in days:
        for w, d in days[c].items():
            bk.append(pd.DataFrame({"coin": c, "w": w, "br": d["book_return"], "cr": d["coin_return"]}))
    bk = pd.concat(bk).dropna()
    bt = bk.groupby("coin").agg(book_mean=("br", "mean"), coin_mean=("cr", "mean"), n=("br", "size"))
    bt["book_sharpe"] = bk.groupby("coin")["br"].apply(lambda x: x.mean()/x.std()*np.sqrt(365))
    out["book by coin"] = bt.round(5)
    # gain decomposition, long vs short bars
    d1["gain"] = d1["alloc"] * d1["fwd1"]
    d1["side"] = np.sign(d1["alloc"].round(3))
    out["gain by side"] = d1.groupby("side")["gain"].agg(["mean", "sum", "count"]).round(5)
    return out
