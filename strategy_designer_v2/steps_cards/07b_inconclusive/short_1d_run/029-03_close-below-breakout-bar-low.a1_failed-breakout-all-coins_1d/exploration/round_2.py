def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    H = [1, 3, 5, 10, 20]
    drift, usual = {}, {}
    for c, ws in bars.items():
        for h in H:
            rs = []
            for w, df in ws.items():
                cl = df["close"].values
                idx = np.arange(0, len(cl) - h, h)
                rs.extend(cl[idx + h] / cl[idx] - 1)
            drift[(c, h)] = np.mean(rs) if rs else np.nan
            usual[(c, h)] = np.std(rs) if rs else np.nan
    col = "debug_info.components.fail_depth.post_pipeline_value"
    rows = []
    for c, ws in bars.items():
        for w, df in ws.items():
            df = df.reset_index(drop=True)
            cl = df["close"].values
            f = df["forecast"].fillna(0).values
            dep = df[col].abs().fillna(0).values if col in df else np.zeros(len(df))
            ts = pd.to_datetime(df["timestamp"])
            r60 = pd.Series(cl).pct_change(60).values
            r20 = pd.Series(cl).pct_change(20).values
            bet = np.zeros(len(cl), bool)
            base = 0.0
            for i in range(len(cl)):
                s = -f[i]
                if f[i] >= 0:
                    base = 0.0
                    continue
                if s - base >= 2:
                    bet[i] = True
                    base = s
                else:
                    base = min(base, s)
            for h in H:
                for start in range(0, len(cl), h):
                    seg = np.where(bet[start:start + h])[0]
                    if len(seg) == 0:
                        continue
                    t = start + seg[0]
                    if t + h >= len(cl):
                        continue
                    ret = cl[t + h] / cl[t] - 1
                    rows.append(dict(coin=c, win=w, h=h, year=ts[t].year, depth=dep[t],
                                     r60=r60[t], r20=r20[t], tot=-ret,
                                     unus=-(ret - drift[(c, h)]),
                                     strength=-(ret - drift[(c, h)]) / usual[(c, h)]))
    d = pd.DataFrame(rows)
    def summ(g):
        n = len(g); m = g["unus"].mean(); s = g["unus"].std()
        return pd.Series(dict(n=n, unus=m, t=m / (s / np.sqrt(n)) if n > 1 else np.nan,
                              tot=g["tot"].mean(), strength=g["strength"].mean(),
                              hit=(g["unus"] > 0).mean(), median=g["unus"].median()))
    out = {}
    out["bets_by_horizon"] = d.groupby("h").apply(summ)
    d5 = d[d.h == 5].copy()
    out["h5_by_year"] = d5.groupby("year").apply(summ)
    d5["trend60"] = np.where(d5["r60"] > 0, "up60", np.where(d5["r60"] <= 0, "down60", "na"))
    out["h5_by_trend60"] = d5.groupby("trend60").apply(summ)
    d5["trend20"] = np.where(d5["r20"] > 0, "up20", np.where(d5["r20"] <= 0, "down20", "na"))
    out["h5_by_trend20"] = d5.groupby("trend20").apply(summ)
    d5["dq"] = pd.qcut(d5["depth"].rank(method="first"), 3, labels=["low", "mid", "high"])
    out["h5_by_depth3"] = d5.groupby("dq").apply(summ)
    d5["grp"] = np.where(d5.coin.isin(["BTCUSD","ETHUSD","LTCUSD","XMRUSD","XRPUSD","ZECUSD"]), "default6", "others")
    out["h5_by_coingroup"] = d5.groupby("grp").apply(summ)
    out["h5_robust"] = pd.Series(dict(trim5=stats.trim_mean(d5["unus"], 0.05),
                                      max=d5["unus"].max(), min=d5["unus"].min(),
                                      sp_depth=stats.spearmanr(d5["depth"], d5["unus"])[0],
                                      wilcoxon_p=stats.wilcoxon(d5["unus"])[1]))
    d10 = d[d.h == 10].copy()
    d10["trend60"] = np.where(d10["r60"] > 0, "up60", np.where(d10["r60"] <= 0, "down60", "na"))
    out["h10_by_trend60"] = d10.groupby("trend60").apply(summ)
    return out
