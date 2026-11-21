import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    H = 10
    rows = []
    usual = {}
    for coin, wins in data["bars"].items():
        # coin's 10-day grid returns over all windows -> drift and usual move
        allr = []
        for w, b in wins.items():
            c = b["close"].values
            idx = np.arange(0, len(c) - H, H)
            allr.extend(list(c[idx + H] / c[idx] - 1))
        allr = np.array(allr)
        drift, sd = allr.mean(), allr.std(ddof=1)
        usual[coin] = (drift, sd, len(allr))
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"]
            r1 = c.pct_change()
            f = pd.DataFrame({
                "coin": coin, "win": w,
                "fwd": c.shift(-H) / c - 1,
                "past10": c / c.shift(10) - 1,
                "past3": c / c.shift(3) - 1,
                "past1": r1,
                "past30": c / c.shift(30) - 1,
                "vol20": r1.rolling(20).std(),
                "d_sma20": c / c.rolling(20).mean() - 1,
                "d_hi30": c / b["high"].rolling(30).max() - 1,
                "d_lo30": c / b["low"].rolling(30).min() - 1,
                "range1": (b["high"] - b["low"]) / c,
                "below50": (b["regime"] == "trending").astype(float),
                "fc": b["forecast"],
                "pos": b["postRebalance_current_allocation"],
                "wd": pd.to_datetime(b["timestamp"]).dt.dayofweek,
            })
            f = f.iloc[np.arange(0, len(f), H)]
            rows.append(f)
    g = pd.concat(rows).dropna(subset=["fwd"])
    g["un"] = g.apply(lambda r: (r["fwd"] - usual[r["coin"]][0]) / usual[r["coin"]][1], axis=1)
    out = {}
    def by_q(col, q=5):
        d = g.dropna(subset=[col]).copy()
        d["q"] = d.groupby("coin")[col].transform(lambda s: pd.qcut(s.rank(method="first"), q, labels=False))
        t = d.groupby("q")["un"].agg(["mean", "count", "std"])
        t["t"] = t["mean"] / (t["std"] / np.sqrt(t["count"]))
        t["raw_fwd_mean"] = d.groupby("q")["fwd"].mean()
        hi, lo = d[d.q == q - 1]["un"], d[d.q == 0]["un"]
        t["top_minus_bottom_t"] = stats.ttest_ind(hi, lo, equal_var=False).statistic
        return t.drop(columns="std")
    for col in ["past1", "past3", "past10", "past30", "vol20", "d_sma20", "d_hi30", "d_lo30", "range1"]:
        out["q_" + col] = by_q(col)
    # regime splits
    t = g.groupby("below50")["un"].agg(["mean", "count"])
    out["below50_split"] = t
    # within below50, past10 quintiles
    d = g[g.below50 == 1].dropna(subset=["past10"]).copy()
    d["q"] = d.groupby("coin")["past10"].transform(lambda s: pd.qcut(s.rank(method="first"), 5, labels=False))
    out["below50_past10_q"] = d.groupby("q")["un"].agg(["mean", "count"])
    d = g[g.below50 == 0].dropna(subset=["past10"]).copy()
    d["q"] = d.groupby("coin")["past10"].transform(lambda s: pd.qcut(s.rank(method="first"), 5, labels=False))
    out["above50_past10_q"] = d.groupby("q")["un"].agg(["mean", "count"])
    # forecast groups
    g["fcg"] = pd.cut(g["fc"], [-21, -2, -1e-9, 1e-9, 21], labels=["<=-2", "(-2,0)", "0", ">0"])
    out["fc_groups"] = g.groupby("fcg")["un"].agg(["mean", "count"])
    out["usual"] = pd.DataFrame(usual, index=["drift10", "sd10", "n"]).T
    # book: daily per coin
    bk = []
    for coin, wins in data["days"].items():
        for w, dd in wins.items():
            bk.append(pd.DataFrame({"coin": coin, "br": dd["book_return"], "cr": dd["coin_return"]}))
    bk = pd.concat(bk).dropna()
    out["book_by_coin"] = bk.groupby("coin").agg(br_mean=("br", "mean"), cr_mean=("cr", "mean"), n=("br", "count"))
    # trades
    tr = pd.concat([t.assign(coin=c) for c, ws in data["trades"].items() for t in ws.values()])
    out["trades"] = tr.groupby("coin").agg(n=("net_profit_loss_percent", "count"),
                                           net_mean=("net_profit_loss_percent", "mean"),
                                           gross_mean=("profit_loss_percent", "mean"),
                                           win=("net_profit_loss_percent", lambda s: (s > 0).mean()))
    return out
