import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    rows = []
    drift = {}
    for coin, wins in data["bars"].items():
        for h in (1, 2, 3, 5):
            vals = []
            for w, b in wins.items():
                c = b["close"].values
                for i in range(0, len(c) - h, h):
                    vals.append(c[i + h] / c[i] - 1)
            drift[(coin, h)] = np.mean(vals) if vals else 0.0
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c, hi, lo, op = b["close"], b["high"], b["low"], b["open"]
            rr = (hi - lo) / c
            mr = rr.rolling(30, min_periods=30).mean()
            f = pd.DataFrame({
                "coin": coin, "win": w, "pos": np.arange(len(b)),
                "inprof": (b["regime"] != "chop").values,
                "s1": (c / c.shift(1) - 1) / mr,
                "s3": (c / c.shift(3) - 1) / mr,
                "s10": (c / c.shift(10) - 1) / mr,
                "upwick": ((hi - np.maximum(c, op)) / (hi - lo)).replace([np.inf, -np.inf], np.nan),
                "gapup": (op / c.shift(1) - 1) / mr,
                "body": ((c - op) / (hi - lo)).replace([np.inf, -np.inf], np.nan),
                "alloc": b["postRebalance_current_allocation"].values,
                "bret": (b["postRebalance_total_value"] / b["postRebalance_total_value"].shift(1) - 1).values,
            })
            f["upwick_x_s1"] = f["upwick"] * f["s1"].clip(lower=0)
            for h in (1, 2, 3, 5):
                f[f"u{h}"] = c.shift(-h) / c - 1 - drift[(coin, h)]
                f[f"g{h}"] = (f["pos"] % h == 0)
            rows.append(f)
    df = pd.concat(rows, ignore_index=True)
    out = {}
    ip = df[df.inprof]
    res = []
    for feat in ["s1", "s3", "s10", "upwick", "gapup", "body", "upwick_x_s1"]:
        for h in (1, 2, 3, 5):
            s = ip[ip[f"g{h}"]].dropna(subset=[feat, f"u{h}"])
            if len(s) < 40:
                continue
            q = pd.qcut(s[feat].rank(method="first"), 3, labels=False)
            m = s.groupby(q)[f"u{h}"].mean()
            top = s[q == 2][f"u{h}"]
            t = top.mean() / (top.std() / np.sqrt(len(top)))
            sl = stats.linregress(s[feat], s[f"u{h}"])
            res.append([feat, h, len(s)] + list(m.round(4)) + [round(t, 2), round(sl.slope / sl.stderr, 2)])
    out["terciles_inprof"] = pd.DataFrame(res, columns=["feat", "h", "n", "t1", "t2", "t3", "t_top", "t_slope"])
    # by coin: s3 top tercile u3
    s = ip[ip["g3"]].dropna(subset=["s3", "u3"])
    s = s.assign(top=s["s3"] > s["s3"].quantile(2/3))
    out["s3_top_u3_by_coin"] = s.groupby(["coin", "top"])["u3"].agg(["mean", "count"])
    # book: in-position days vs not, largest losses context
    bk = df.dropna(subset=["bret"])
    held = bk[bk["alloc"].shift(1).fillna(0) != 0]
    out["book_bar_stats"] = pd.Series({"held_bars": len(held), "mean": held["bret"].mean(),
                                      "t": held["bret"].mean() / (held["bret"].std() / np.sqrt(len(held)))})
    tr = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            if len(t):
                tr.append(t.assign(coin=coin))
    if tr:
        T = pd.concat(tr)
        out["trades_by_coin"] = T.groupby("coin")["net_profit_loss_percent"].agg(["mean", "median", "count"])
        T["fq"] = pd.qcut(T["entry_forecast"].rank(method="first"), 3, labels=False)
        out["trades_by_entry_fc_tercile"] = T.groupby("fq")["net_profit_loss_percent"].agg(["mean", "count"])
    return out
