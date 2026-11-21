import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            vol20 = r1.rolling(20).std()
            vsr5 = (c / c.shift(5) - 1) / (vol20 * np.sqrt(5))
            vsr1 = r1 / vol20
            r20 = c / c.shift(20) - 1
            df = pd.DataFrame({
                "coin": coin, "win": w, "pos": np.arange(len(b)),
                "vsr5": vsr5, "vsr1": vsr1, "vol20": vol20, "r20": r20,
                "fc": b["forecast"].astype(float),
                "alloc": b["postRebalance_current_allocation"].astype(float),
                "wd": pd.to_datetime(b["timestamp"]).dt.weekday,
            })
            for h in (1, 3, 5, 10):
                df[f"f{h}"] = c.shift(-h) / c - 1
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    # demean per coin, using non-overlapping grid of each horizon
    for h in (1, 3, 5, 10):
        g = d[d["pos"] % h == 0]
        m = g.groupby("coin")[f"f{h}"].mean()
        sd = g.groupby("coin")[f"f{h}"].std()
        d[f"u{h}"] = d[f"f{h}"] - d["coin"].map(m)
        d[f"s{h}"] = d[f"u{h}"] / d["coin"].map(sd)

    def tab(col, h, q=5, sub=None):
        g = d[d["pos"] % h == 0].dropna(subset=[col, f"u{h}"])
        if sub is not None:
            g = g[sub(g)]
        g = g.copy()
        g["q"] = pd.qcut(g[col], q, labels=False, duplicates="drop")
        t = g.groupby("q").agg(lo=(col, "min"), hi=(col, "max"), n=(f"u{h}", "size"),
                               mean_u=(f"u{h}", "mean"), t=(f"u{h}", lambda x: x.mean() / (x.std() / np.sqrt(len(x)))))
        s = stats.linregress(g[col], g[f"s{h}"])
        t.loc["slope_t"] = [np.nan, np.nan, len(g), s.slope, s.slope / s.stderr]
        return t

    out["vsr5_h3"] = tab("vsr5", 3)
    out["vsr5_h10"] = tab("vsr5", 10)
    out["vsr1_h1"] = tab("vsr1", 1)
    out["vsr1_h3"] = tab("vsr1", 3)
    out["r20_h10"] = tab("r20", 10)
    out["vol20_h3"] = tab("vol20", 3)
    out["vsr5_h3_byvolhigh"] = tab("vsr5", 3, 3, sub=lambda g: g["vol20"] > g["vol20"].median())
    out["vsr5_h3_byvollow"] = tab("vsr5", 3, 3, sub=lambda g: g["vol20"] <= g["vol20"].median())
    g1 = d.dropna(subset=["u1"])
    out["weekday_u1"] = g1.groupby("wd")["u1"].agg(["size", "mean", lambda x: x.mean() / (x.std() / np.sqrt(len(x)))])
    out["by_coin_vsr5_h3"] = d[d.pos % 3 == 0].dropna(subset=["vsr5", "s3"]).groupby("coin").apply(
        lambda g: pd.Series({"n": len(g), "t": (lambda s: s.slope / s.stderr)(stats.linregress(g["vsr5"], g["s3"]))}))
    # book: largest days
    dd = []
    for coin, wins in data["days"].items():
        for w, x in wins.items():
            x = x.copy(); x["coin"] = coin; x["win"] = w; dd.append(x)
    D = pd.concat(dd, ignore_index=True)
    out["book_by_win"] = D.groupby("win").agg(book=("book_return", "mean"), coin=("coin_return", "mean")).describe()
    tr = []
    for coin, wins in data["trades"].items():
        for w, x in wins.items():
            tr.append(x)
    T = pd.concat(tr, ignore_index=True)
    T["days"] = T["duration_minutes"] / 1440
    T["dq"] = pd.qcut(T["days"], 4, labels=False, duplicates="drop")
    out["trades_by_duration"] = T.groupby("dq").agg(n=("days", "size"), dmin=("days", "min"), dmax=("days", "max"),
                                                    pnl=("net_profit_loss_percent", "mean"))
    return out
