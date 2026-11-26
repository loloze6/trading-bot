def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        allr = []
        for w, df in wins.items():
            allr.append(df["close"].astype(float).pct_change().dropna())
        mu = pd.concat(allr).mean()
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float)
            ts = pd.to_datetime(df["timestamp"])
            n = len(df)
            r1 = c.pct_change()
            sd30 = r1.rolling(30).std()
            er = (c - c.shift(30)).abs() / c.diff().abs().rolling(30).sum()
            r7 = c / c.shift(7) - 1
            r30 = c / c.shift(30) - 1
            z7 = r7 / (sd30 * np.sqrt(7))
            agree = np.sign(r7) == np.sign(r30)
            # run length of chop regime from each bar onward
            chop = (df["regime"] == "chop").values
            for h in [1, 3, 5, 7, 10, 14]:
                fwd = c.shift(-h) / c - 1
                for i in range(0, n, h):
                    if np.isnan(fwd.iloc[i]) or np.isnan(z7.iloc[i]) or np.isnan(er.iloc[i]):
                        continue
                    if r7.iloc[i] == 0:
                        continue
                    if chop[i]:
                        grp = "chop_agree"
                    elif er.iloc[i] < 0.3:
                        grp = "chop_disagree"
                    else:
                        grp = "trend_er"
                    # days chop persists in the next h
                    stay = chop[i:i + h].mean()
                    rows.append(dict(coin=coin, w=w, year=ts.iloc[i].year, day=ts.iloc[i].date(), h=h, grp=grp,
                                     z=z7.iloc[i], sx=np.sign(r7.iloc[i]) * (fwd.iloc[i] - ((1 + mu) ** h - 1)),
                                     stay=stay))
    d = pd.DataFrame(rows)
    out = {}
    def tday(g):
        pdv = g.groupby("day").sx.sum()
        return pd.Series(dict(cases=len(g), days=len(pdv), mean=g.sx.mean(),
                              t_day=pdv.mean() / (pdv.std() / np.sqrt(len(pdv)))))
    out["by_h_group"] = d.groupby(["h", "grp"]).apply(tday).unstack(level=-1) if False else d.groupby(["h", "grp"]).apply(tday)
    d7 = d[(d.h == 7) & (d.grp == "chop_agree")].copy()
    d7["zq"] = pd.qcut(d7.z.abs(), 3, labels=["zlo", "zmid", "zhi"])
    out["h7_chop_by_absz"] = d7.groupby("zq").apply(tday)
    out["h7_chop_by_coin"] = d7.groupby("coin").apply(tday)
    out["h7_chop_by_year"] = d7.groupby("year").apply(tday)
    out["h7_chop_by_side"] = d7.assign(side=np.where(d7.z > 0, "long", "short")).groupby("side").apply(tday)
    d7["stq"] = pd.cut(d7.stay, [-0.01, 0.5, 0.99, 1.01], labels=["breaks_early", "breaks_late", "stays_all"])
    out["h7_chop_by_persistence"] = d7.groupby("stq").apply(tday)
    d7["zs"] = d7.z.abs() * np.sign(d7.sx)  # placeholder
    out["h7_chop_corr_absz_sx"] = float(np.corrcoef(d7.z.abs(), d7.sx)[0, 1])
    d14 = d[(d.h == 14) & (d.grp == "chop_agree")].copy()
    d14["zq"] = pd.qcut(d14.z.abs(), 3, labels=["zlo", "zmid", "zhi"])
    out["h14_chop_by_absz"] = d14.groupby("zq").apply(tday)
    return out
