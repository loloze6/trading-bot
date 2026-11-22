def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; days = data["days"]
    rows = []
    drift = {}
    usual = {}
    for coin, wins in bars.items():
        r5 = []
        for w, df in wins.items():
            c = df["close"].values
            idx = np.arange(0, len(c) - 5, 5)
            r5 += list(c[idx + 5] / c[idx] - 1)
        drift[coin] = np.mean(r5); usual[coin] = np.std(r5)
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values; f = df["forecast"].fillna(0).values
            n = len(df)
            d90 = df.get("debug_info.components.depth90.last_history_value")
            bnc = df.get("debug_info.components.bounce.last_history_value")
            r1 = np.r_[np.nan, c[1:] / c[:-1] - 1]
            low = 0.0; seen = set()
            for t in range(n):
                if f[t] >= 0:
                    low = 0.0; continue
                if f[t] <= low - 2:
                    low = f[t]
                    cell = t // 5
                    if cell in seen or t + 10 >= n: continue
                    seen.add(cell)
                    rec = dict(coin=coin, win=w, year=pd.Timestamp(df["timestamp"].iloc[t]).year,
                               fc=f[t], d90=d90.iloc[t] if d90 is not None else np.nan,
                               bz=bnc.iloc[t] if bnc is not None else np.nan, r1=r1[t])
                    for h in (1, 2, 3, 5, 10):
                        rec[f"tot{h}"] = -(c[t + h] / c[t] - 1)
                        rec[f"unu{h}"] = -(c[t + h] / c[t] - 1 - drift[coin] * h / 5)
                    rows.append(rec)
                else:
                    low = min(low, f[t]) if f[t] > low else low
    cs = pd.DataFrame(rows)
    def summ(g):
        return pd.Series({"n": len(g), "unu5": g.unu5.mean(), "t5": stats.ttest_1samp(g.unu5, 0).statistic if len(g) > 2 else np.nan,
                          "tot5": g.tot5.mean(), "unu1": g.unu1.mean(), "unu2": g.unu2.mean(), "unu10": g.unu10.mean()})
    out = {}
    out["all"] = summ(cs)
    out["horizon"] = pd.DataFrame({h: [cs[f"unu{h}"].mean(), stats.ttest_1samp(cs[f"unu{h}"], 0).statistic, cs[f"tot{h}"].mean()] for h in (1, 2, 3, 5, 10)}, index=["unu", "t", "tot"])
    cs["dq"] = pd.qcut(cs.d90, 5, labels=False)
    out["by_depth_q"] = cs.groupby("dq").apply(summ).join(cs.groupby("dq").d90.mean())
    cs["fq"] = pd.qcut(cs.r1, 4, labels=False, duplicates="drop")
    out["by_bounce_q"] = cs.groupby("fq").apply(summ).join(cs.groupby("fq").r1.mean())
    out["by_coin"] = cs.groupby("coin").apply(summ)
    out["by_year"] = cs.groupby("year").apply(summ)
    out["drift5"] = pd.Series(drift)
    # book decomposition
    br = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            dd = days[coin][w]
            b = df.copy(); b["day"] = pd.to_datetime(b["timestamp"]).dt.floor("D")
            al = b.groupby("day")["postRebalance_current_allocation"].last()
            dd = dd.copy(); dd["day"] = pd.to_datetime(dd["day"])
            dd["alloc_prev"] = dd["day"].map(al).shift(1)
            dd["coin"] = coin; dd["win"] = w
            br.append(dd)
    B = pd.concat(br)
    mcr = B.groupby("coin").coin_return.mean()
    B["mkt"] = B.alloc_prev * B.coin.map(mcr)
    B["year"] = B.day.dt.year
    out["book"] = pd.Series({"mean_book": B.book_return.mean(), "mkt_part": B.mkt.mean(), "share_days_short": (B.alloc_prev < 0).mean(),
                             "mean_alloc_when_short": B.alloc_prev[B.alloc_prev < 0].mean(),
                             "book_on_short_days": B.book_return[B.alloc_prev < 0].mean()})
    out["book_by_year"] = B.groupby("year").agg(book=("book_return", "mean"), mkt=("mkt", "mean"), coin=("coin_return", "mean"), short=("alloc_prev", lambda x: (x < 0).mean()))
    return out
