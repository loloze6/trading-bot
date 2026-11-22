def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; days = data["days"]
    rows = []; drift = {}; usual = {}
    for coin, wins in bars.items():
        r5 = []
        for w, df in wins.items():
            c = df["close"].values
            idx = np.arange(0, len(c) - 5, 5)
            r5 += list(c[idx + 5] / c[idx] - 1)
        drift[coin] = np.mean(r5); usual[coin] = np.std(r5)
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values; f = df["forecast"].fillna(0).values; n = len(df)
            d90 = df["debug_info.components.depth90.last_history_value"]
            r1 = np.r_[np.nan, c[1:] / c[:-1] - 1]
            r20 = pd.Series(c).pct_change(20).values
            sd20 = pd.Series(r1).rolling(20).std().values
            low = 0.0; seen = set()
            for t in range(n):
                if f[t] >= 0:
                    low = 0.0; continue
                if f[t] <= low - 2:
                    low = f[t]; cell = t // 5
                    if cell in seen or t + 10 >= n: continue
                    seen.add(cell)
                    rec = dict(coin=coin, d90=d90.iloc[t], r1=r1[t], z=r1[t] / sd20[t] if sd20[t] > 0 else np.nan, r20=r20[t], fc=f[t])
                    for h in (5, 10):
                        rec[f"unu{h}"] = -(c[t + h] / c[t] - 1 - drift[coin] * h / 5)
                        rec[f"tot{h}"] = -(c[t + h] / c[t] - 1)
                        rec[f"s{h}"] = rec[f"unu{h}"] / (usual[coin] * np.sqrt(h / 5))
                    rows.append(rec)
    cs = pd.DataFrame(rows)
    def summ(g):
        return pd.Series({"n": len(g), "unu5": g.unu5.mean(), "t5": stats.ttest_1samp(g.unu5, 0).statistic,
                          "tot5": g.tot5.mean(), "s5": g.s5.mean(), "unu10": g.unu10.mean(),
                          "t10": stats.ttest_1samp(g.unu10, 0).statistic, "tot10": g.tot10.mean()})
    out = {}
    cs["dd"] = pd.qcut(cs.d90, 8, labels=False)
    out["by_depth8"] = cs.groupby("dd").apply(summ).join(cs.groupby("dd").d90.mean())
    cs["deep"] = np.where(cs.d90 < -40, "deep<-40", "mild>=-40")
    cs["big"] = np.where(cs.z > cs.z.median(), "bigz", "smallz")
    out["depth_x_z"] = cs.groupby(["deep", "big"]).apply(summ)
    cs["m20"] = np.where(cs.r20 < 0, "r20neg", "r20pos")
    out["depth_x_r20"] = cs.groupby(["deep", "m20"]).apply(summ)
    m = cs[cs.d90 >= -40]
    sl = stats.linregress(m.d90, m.unu5)
    out["slope_mild"] = pd.Series({"slope": sl.slope, "t": sl.slope / sl.stderr, "n": len(m)})
    sl = stats.linregress(cs.d90, cs.unu5)
    out["slope_all"] = pd.Series({"slope": sl.slope, "t": sl.slope / sl.stderr, "n": len(cs)})
    # book by depth of fall on held days
    br = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            b = df.copy(); b["day"] = pd.to_datetime(b["timestamp"]).dt.floor("D")
            g = b.groupby("day").agg(al=("postRebalance_current_allocation", "last"),
                                     d90=("debug_info.components.depth90.last_history_value", "last"))
            dd = days[coin][w].copy(); dd["day"] = pd.to_datetime(dd["day"])
            dd["al"] = dd.day.map(g.al).shift(1); dd["d90"] = dd.day.map(g.d90).shift(1); dd["coin"] = coin
            br.append(dd)
    B = pd.concat(br)
    mcr = B.groupby("coin").coin_return.mean()
    B["mkt"] = B.al * B.coin.map(mcr)
    S = B[B.al < 0].copy()
    S["deep"] = np.where(S.d90 < -40, "deep<-40", "mild>=-40")
    out["book_short_days_by_depth"] = S.groupby("deep").agg(n=("book_return", "size"), book=("book_return", "mean"),
                                                            mkt=("mkt", "mean"), sd=("book_return", "std"))
    return out
