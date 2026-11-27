import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    bars = data["bars"]
    rows = []
    allret = {}
    for coin, wins in bars.items():
        allret[coin] = pd.concat([w["close"].reset_index(drop=True).pct_change().dropna() for w in wins.values()])
    for coin, wins in bars.items():
        mu1 = allret[coin].mean()
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c, h, l = df["close"], df["high"], df["low"]
            r = c.pct_change()
            sd30 = r.rolling(30).std()
            width = (h - l) / c / sd30
            loc = (c - l) / (h - l)
            ts = pd.to_datetime(df["timestamp"])
            nxt = c.shift(-1) / c - 1
            nxt2 = c.shift(-2) / c - 1
            for i in range(len(df) - 1):
                if df["regime"].iloc[i] not in ("unknown", "mean_reversion"):
                    continue
                rows.append({"coin": coin, "win": w, "year": ts.iloc[i].year, "day": ts.iloc[i].normalize(),
                             "width": width.iloc[i], "loc": loc.iloc[i], "active": df["regime"].iloc[i] == "mean_reversion",
                             "ex1": -(nxt.iloc[i]) + mu1, "ex2": -(nxt2.iloc[i]) + 2*mu1 if not np.isnan(nxt2.iloc[i]) else np.nan})
    d = pd.DataFrame(rows).dropna(subset=["width", "loc", "ex1"])
    def summ(g, col="ex1"):
        g = g.dropna(subset=[col])
        dd = g.groupby("day")[col].sum()
        t = dd.mean() / (dd.std() / np.sqrt(len(dd))) if len(dd) > 2 else np.nan
        return pd.Series({"n": len(g), "days": len(dd), "mean": g[col].mean(), "hit": (g[col] > 0).mean(), "t_day": t})
    out = {}
    out["regime_counts"] = d["active"].value_counts()
    d["wbin"] = pd.cut(d["width"], [0, 1, 1.5, 2, 3, 100])
    d["lbin"] = pd.cut(d["loc"], [-0.01, 0.25, 0.5, 0.75, 0.9, 1.01])
    out["fc_by_loc_all_widths"] = d.groupby("lbin").apply(summ)
    out["fc_by_width_loc_ge075"] = d[d["loc"] >= 0.75].groupby("wbin").apply(summ)
    out["fc_by_width_loc_ge090"] = d[d["loc"] >= 0.9].groupby("wbin").apply(summ)
    hi = d[(d["loc"] >= 0.75) & (d["width"] >= 1.5)]
    out["loc075_width15_byyear"] = hi.groupby("year").apply(summ)
    out["loc075_width15_bycoin"] = hi.groupby("coin").apply(summ)
    out["active_loc_ge09"] = summ(d[d["active"] & (d["loc"] >= 0.9)])
    out["active_loc_lt09"] = summ(d[d["active"] & (d["loc"] < 0.9)])
    out["active_ex2"] = summ(d[d["active"]], "ex2")
    out["spearman_fc_loc_ex1"] = stats.spearmanr(d["loc"], d["ex1"])[0]
    out["spearman_fc_locwidth_ex1"] = stats.spearmanr(d["loc"] * d["width"], d["ex1"])[0]
    return out
