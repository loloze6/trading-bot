import pandas as pd, numpy as np

def explore(data):
    def build(H):
        per = []
        for coin, wins in data["bars"].items():
            gg = []
            for w, b in wins.items():
                b = b.reset_index(drop=True)
                o, h, l, c = b["open"], b["high"], b["low"], b["close"]
                rng = h - l
                rr = rng / rng.rolling(20, min_periods=20).mean()
                r1 = c / c.shift(1) - 1
                r20 = c / c.shift(20) - 1
                vol20 = r1.rolling(20).std()
                hi20 = c.rolling(20).max()
                fwd = c.shift(-H) / c - 1
                idx = np.arange(0, len(b), H)
                idx = idx[idx + H < len(b)]
                gg.append(pd.DataFrame({"coin": coin,
                    "day": b["timestamp"].iloc[idx].astype(str).str[:10].values,
                    "rr": rr.iloc[idx].values, "r1": r1.iloc[idx].values, "r20": r20.iloc[idx].values,
                    "r20v": (r20 / (vol20 * np.sqrt(20))).iloc[idx].values,
                    "athi": (c / hi20).iloc[idx].values,
                    "fwd": fwd.iloc[idx].values}))
            g = pd.concat(gg)
            g["un"] = g["fwd"] - g["fwd"].mean()
            g["str"] = g["un"] / g["fwd"].std()
            per.append(g)
        return pd.concat(per, ignore_index=True).dropna(subset=["rr", "r20", "r20v"])

    def summ(df, key):
        out = []
        for k, s in df.groupby(key, observed=True):
            d = s.groupby("day")["un"].sum(); n = len(s); nd = len(d)
            t = (d.sum() / n) / (np.sqrt(nd) * d.std(ddof=1) / n) if nd > 2 else np.nan
            out.append({"grp": str(k), "n": n, "days": nd, "mean_un": round(s["un"].mean(), 5),
                        "strength": round(s["str"].mean(), 4), "t": round(t, 2)})
        return pd.DataFrame(out)

    res = {}
    for H in [3, 10]:
        G = build(H)
        nw = G[G["rr"] < 1.5].copy()
        nw["r20v_q"] = pd.qcut(nw["r20v"], 5)
        res[f"H{H}_notwide_by_r20v_q"] = summ(nw, "r20v_q")
        wu = G[(G["rr"] >= 1.5) & (G["r20"] > 0)].copy()
        wu["r20v_q"] = pd.qcut(wu["r20v"], 3)
        res[f"H{H}_wide_up_by_r20v_t3"] = summ(wu, "r20v_q")
        wu["rr_q"] = pd.qcut(wu["rr"], 3)
        res[f"H{H}_wide_up_by_rr_t3"] = summ(wu, "rr_q")
    G = build(10)
    wu = G[(G["rr"] >= 1.5) & (G["r20"] > 0)]
    res["H10_wide_up_by_year"] = summ(wu.assign(year=wu["day"].str[:4]), "year")
    return res
