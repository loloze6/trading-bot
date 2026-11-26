def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    H = [1, 3, 5, 10, 20]
    rows = []
    drift = {}
    for coin, wins in bars.items():
        for h in H:
            rs = []
            for w, df in wins.items():
                c = df["close"].values
                for i in range(0, len(c) - h, h):
                    rs.append(c[i + h] / c[i] - 1)
            drift[(coin, h)] = np.mean(rs) if rs else np.nan
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"]
            ch = (c - c.shift(60)).abs()
            vol = c.diff().abs().rolling(60).sum()
            er = (ch / vol).rolling(5).mean()
            plow = df["low"].shift(1).rolling(60).min()
            phigh = df["high"].shift(1).rolling(60).max()
            dlow = c / plow - 1
            dhigh = c / phigh - 1
            rec = df["regime"] == "mean_reversion"
            rdepth = df.get("debug_info.components.depth.last_history_value")
            for h in H:
                for side, cond, dep in [("down_rec", rec, (-rdepth / 100) if rdepth is not None else -dlow),
                                        ("down_all", dlow < 0, -dlow),
                                        ("up_all", dhigh > 0, dhigh)]:
                    cells = {}
                    for i in np.where(cond.fillna(False).values)[0]:
                        cell = i // h
                        if cell in cells or i + h >= len(c):
                            continue
                        cells[cell] = i
                    for cell, i in cells.items():
                        r = c.iloc[i + h] / c.iloc[i] - 1
                        rows.append(dict(coin=coin, w=w, h=h, side=side, day=str(df["timestamp"].iloc[i])[:10],
                                         ex=r - drift[(coin, h)], tot=r, er=er.iloc[i], dep=dep.iloc[i] if dep is not None else np.nan,
                                         year=str(df["timestamp"].iloc[i])[:4]))
    R = pd.DataFrame(rows)

    def tclus(g):
        s = g.groupby("day")["ex"].sum()
        dev = g.groupby("day")["ex"].apply(lambda x: (x - g["ex"].mean()).sum())
        G = len(s)
        if G < 3: return np.nan
        se = np.sqrt((dev ** 2).sum() * G / (G - 1)) / len(g)
        return g["ex"].mean() / se

    def summ(g):
        return pd.Series(dict(n=len(g), mean_ex=g["ex"].mean(), t=tclus(g), mean_tot=g["tot"].mean(), hit=(g["tot"] > 0).mean()))

    out = {}
    out["by_side_h"] = R.groupby(["side", "h"]).apply(summ)
    d10 = R[(R.side == "down_all") & (R.h == 10)].copy()
    d10["erb"] = pd.cut(d10["er"], [0, 0.15, 0.3, 0.5, 1.0])
    out["down_all_10_by_er"] = d10.groupby("erb").apply(summ)
    d10["depq"] = pd.qcut(d10["dep"], 3, labels=["shallow", "mid", "deep"])
    out["down_all_10_by_depth"] = d10.groupby("depq").apply(summ)
    rr = R[(R.side == "down_rec") & (R.h == 10)].copy()
    out["rec10_by_coin"] = rr.groupby("coin").apply(summ)
    out["rec10_by_year"] = rr.groupby("year").apply(summ)
    rr["depq"] = pd.qcut(rr["dep"], 3, labels=["shallow", "mid", "deep"], duplicates="drop")
    out["rec10_by_depth"] = rr.groupby("depq").apply(summ)
    u10 = R[(R.side == "up_all") & (R.h == 10)].copy()
    u10["erb"] = pd.cut(u10["er"], [0, 0.15, 0.3, 0.5, 1.0])
    out["up_all_10_by_er"] = u10.groupby("erb").apply(summ)
    for s in ["down_all", "up_all"]:
        g = R[(R.side == s) & (R.h == 10)].dropna(subset=["er"])
        out[f"corr_ex_er_{s}"] = float(stats.spearmanr(g["er"], g["ex"])[0])
    return out
