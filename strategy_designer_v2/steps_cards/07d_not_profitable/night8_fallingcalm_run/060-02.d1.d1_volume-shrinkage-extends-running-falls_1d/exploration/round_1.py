def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    bars = data["bars"]; days = data["days"]
    H = [5, 10, 20]
    rows = []
    drift = {}
    for c in bars:
        for h in H:
            rs = []
            for w, b in bars[c].items():
                cl = b["close"].values
                idx = np.arange(0, len(cl) - h, h)
                rs += list(cl[idx + h] / cl[idx] - 1)
            drift[(c, h)] = np.mean(rs)
        for w, b in bars[c].items():
            b = b.reset_index(drop=True)
            cl = b["close"]; vol = b["volume"]
            r1 = cl.pct_change()
            sd30 = r1.rolling(30).std()
            ret20 = cl / cl.shift(20) - 1
            ret5p = cl / cl.shift(5) - 1
            vr = np.log(vol.rolling(30).mean() / vol.shift(30).rolling(30).mean())
            n = len(b)
            for i in range(0, n, 5):
                d = dict(coin=c, w=w, i=i, regime=b["regime"].iat[i], fc=b["forecast"].iat[i],
                         alloc=b["postRebalance_current_allocation"].iat[i],
                         ret20=ret20.iat[i], ret5p=ret5p.iat[i], sd30=sd30.iat[i], vr=vr.iat[i],
                         ts=b["timestamp"].iat[i])
                for h in H:
                    d[f"f{h}"] = (cl.iat[i + h] / cl.iat[i] - 1 - drift[(c, h)]) if i + h < n else np.nan
                rows.append(d)
    g = pd.DataFrame(rows)
    g["sdrel"] = g["sd30"] / g.groupby("coin")["sd30"].transform("median")
    tr = g[g.regime == "trending"].copy()
    tr["fcb"] = pd.cut(tr["fc"], [-100, -10, -3, -1e-9, 1e-9], labels=["strong", "mid", "weak", "zero"])
    def summ(df, by):
        res = {}
        for k, s in df.groupby(by, observed=True):
            r = {"n": len(s)}
            for h in H:
                x = -s[f"f{h}"].dropna()
                r[f"short_unusual_{h}"] = x.mean()
                r[f"t_{h}"] = x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan
            res[k] = r
        return pd.DataFrame(res).T
    out["trending_by_forecast"] = summ(tr, "fcb")
    neg = tr[tr.fc < 0].copy()
    neg["depth20"] = pd.qcut(neg["ret20"], 3, labels=["deep", "mid", "shallow"])
    out["neg_by_ret20"] = summ(neg, "depth20")
    neg["agit"] = np.where(neg["sdrel"] > 1, "agitated", "calm")
    out["neg_by_agit"] = summ(neg, "agit")
    zero = tr[tr.fc == 0].copy()
    zero["agit"] = np.where(zero["sdrel"] > 1, "agitated", "calm")
    out["zero_by_agit"] = summ(zero, "agit")
    neg["last5"] = np.where(neg["ret5p"] < 0, "fell5", "rose5")
    out["neg_by_last5"] = summ(neg, "last5")
    zero["last5"] = np.where(zero["ret5p"] < 0, "fell5", "rose5")
    out["zero_by_last5"] = summ(zero, "last5")
    neg["yr"] = pd.to_datetime(neg["ts"]).dt.year
    out["neg_by_year"] = summ(neg, "yr")
    # book daily
    dd = []
    for c in days:
        for w, d in days[c].items():
            x = d[["day", "book_return", "coin_return"]].copy(); x["w"] = w; x["coin"] = c
            dd.append(x)
    dd = pd.concat(dd)
    bk = dd.groupby(["w", "day"])[["book_return", "coin_return"]].mean().reset_index()
    bk["wn"] = bk["w"].str[1:].astype(int)
    bk = bk.sort_values(["wn", "day"]).dropna()
    bw = bk.groupby("w").agg(mean_book=("book_return", "mean"), sd_book=("book_return", "std"),
                             mean_coin=("coin_return", "mean"), n=("book_return", "size"))
    out["book_by_window"] = bw
    v = (1 + bk["book_return"]).cumprod()
    ddn = v / v.cummax() - 1
    bk["dd"] = ddn.values
    out["deepest_fall"] = float(ddn.min())
    out["dd_by_window_min"] = bk.groupby("w")["dd"].min()
    # trades
    trs = []
    for c in data["trades"]:
        for w, t in data["trades"][c].items():
            if len(t): trs.append(t.assign(coin=c, w=w))
    t = pd.concat(trs)
    t["dur_d"] = t["duration_minutes"] / 1440
    out["trades"] = pd.DataFrame({"n": [len(t)], "mean_net": [t.net_profit_loss_percent.mean()],
                                  "mean_gross": [t.profit_loss_percent.mean()],
                                  "med_dur_d": [t.dur_d.median()], "win": [(t.net_profit_loss_percent > 0).mean()]})
    t["durb"] = pd.cut(t["dur_d"], [0, 5.5, 10, 20, 1000])
    out["trades_by_dur"] = t.groupby("durb", observed=True)["net_profit_loss_percent"].agg(["count", "mean"])
    return out
