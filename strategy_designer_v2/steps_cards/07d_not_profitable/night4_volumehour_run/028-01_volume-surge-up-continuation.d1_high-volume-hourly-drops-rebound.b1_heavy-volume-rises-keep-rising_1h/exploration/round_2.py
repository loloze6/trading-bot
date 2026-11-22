import numpy as np, pandas as pd

def explore(data):
    out = {}
    bars = data["bars"]; days = data["days"]
    coins = list(bars.keys())
    rows = []
    for c in coins:
        drifts = {}
        for H in (6, 24):
            dl = []
            for w in bars[c]:
                cl = bars[c][w]["close"].values
                idx = np.arange(0, len(cl) - H, H)
                dl.append(cl[idx + H] / cl[idx] - 1)
            dd = np.concatenate(dl); drifts[H] = (dd.mean(), dd.std())
        for w in bars[c]:
            b = bars[c][w]; cl = b["close"].values; f = b["forecast"].values
            for k in range(0, len(cl) - 24, 24):
                cell = np.where(f[k:k + 24] >= 2)[0]
                if len(cell) == 0: continue
                t = k + cell[0]
                if t + 24 >= len(cl) or t < 720: continue
                u24 = cl[t + 24] / cl[t] - 1 - drifts[24][0]
                u6 = cl[t + 6] / cl[t] - 1 - drifts[6][0]
                p7 = cl[t] / cl[t - 168] - 1
                p30 = cl[t] / cl[t - 720] - 1
                r1 = np.diff(np.log(cl[t - 168:t + 1]))
                p7s = p7 / (r1.std() * np.sqrt(168))
                rows.append((c, w, f[t], u24, u6, u6 / drifts[6][1], u24 / drifts[24][1], p7, p7s, p30))
    cs = pd.DataFrame(rows, columns=["coin", "w", "f", "u24", "u6", "s6", "s24", "p7", "p7s", "p30"])
    def summ(g):
        return pd.Series({"n": len(g), "u24": g.u24.mean(), "t24": g.u24.mean() / g.u24.std() * np.sqrt(len(g)),
                          "u6": g.u6.mean(), "t6": g.u6.mean() / g.u6.std() * np.sqrt(len(g)),
                          "str24": g.s24.mean()})
    out["all"] = summ(cs)
    cs["q7"] = pd.qcut(cs.p7, 5, labels=list("12345"))
    out["by_7d_ret_quint"] = cs.groupby("q7").apply(summ)
    cs["q7s"] = pd.qcut(cs.p7s, 5, labels=list("12345"))
    out["by_7d_scaled_quint"] = cs.groupby("q7s").apply(summ)
    cs["q30"] = pd.qcut(cs.p30, 5, labels=list("12345"))
    out["by_30d_quint"] = cs.groupby("q30").apply(summ)
    out["by_7d_x_coin"] = cs.groupby(["coin", pd.qcut(cs.p7, 3, labels=["dn", "md", "up"])]).apply(summ)
    # in-market share by coin 7d return state, and book in down weeks
    rec = []
    for c in coins:
        for w in bars[c]:
            b = bars[c][w]; cl = b["close"]
            r = cl.shift(-1) / cl - 1
            a = b["postRebalance_current_allocation"]
            p7 = cl / cl.shift(168) - 1
            rec.append(pd.DataFrame({"r": r, "a": a, "p7": p7, "g": a * r}))
    R = pd.concat(rec).dropna()
    R["q"] = pd.qcut(R.p7, 3, labels=["dn", "md", "up"])
    out["bars_by_7d"] = R.groupby("q").agg(alloc=("a", "mean"), coin_r=("r", "mean"), pos_gain=("g", "mean"), n=("r", "size"))
    out["share_bars_forecast_pos"] = float(pd.concat([bars[c][w]["forecast"] > 0 for c in coins for w in bars[c]]).mean())
    return out
