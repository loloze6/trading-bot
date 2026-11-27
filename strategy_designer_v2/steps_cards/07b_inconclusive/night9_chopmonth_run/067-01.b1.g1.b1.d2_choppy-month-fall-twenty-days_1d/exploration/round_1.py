def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    out = {}
    H = [5, 10, 20]
    rows = []
    # drift per coin per horizon over all windows (non-overlapping grid)
    drift = {}
    for c, ws in bars.items():
        for h in H:
            rs = []
            for w, b in ws.items():
                cl = b["close"].values
                for i in range(0, len(cl) - h, h):
                    rs.append(cl[i + h] / cl[i] - 1)
            drift[(c, h)] = (np.mean(rs) if rs else np.nan, np.std(rs) if rs else np.nan)
    for c, ws in bars.items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            cl = b["close"].values
            n = len(cl)
            r60 = pd.Series(cl).pct_change(60).values * 100
            r30 = pd.Series(cl).pct_change(30).values * 100
            reg = b["regime"].values
            fc = b["forecast"].values
            lr = np.log(pd.Series(cl)).diff()
            vol30 = lr.rolling(30).std().values
            vol_med = lr.rolling(30).std().rolling(90, min_periods=30).median().values
            year = pd.to_datetime(b["timestamp"]).dt.year.values
            for h in H:
                for i in range(0, n - h, h):
                    chop = (reg[i] == "mean_reversion") if np.isnan(r60[i]) else (-10 <= r60[i] <= 10)
                    if not chop or np.isnan(r30[i]):
                        continue
                    fwd = cl[i + h] / cl[i] - 1
                    d, s = drift[(c, h)]
                    rows.append(dict(coin=c, win=w, year=year[i], h=h, r30=r30[i], fc=fc[i],
                                     fwd=fwd, unus=fwd - d, sd=s,
                                     agit=(vol30[i] > vol_med[i]) if not np.isnan(vol_med[i]) else np.nan))
    df = pd.DataFrame(rows)
    def summ(g):
        x = -g["unus"]
        return pd.Series(dict(n=len(g), mean_short_unus=x.mean(), t=x.mean() / (x.std(ddof=1) / np.sqrt(len(g))) if len(g) > 2 else np.nan,
                              mean_total_short=-g["fwd"].mean()))
    # falls vs rises by horizon (continuation signed: short after fall, long after rise)
    df["side"] = np.where(df["r30"] < 0, "fall", "rise")
    df["cont"] = np.where(df["side"] == "fall", -df["unus"], df["unus"])
    def summc(g):
        x = g["cont"]
        return pd.Series(dict(n=len(g), mean_cont=x.mean(), t=x.mean() / (x.std(ddof=1) / np.sqrt(len(g))),
                              corr_r30_unus=np.corrcoef(g["r30"], g["unus"])[0, 1]))
    out["by_h_side"] = df.groupby(["h", "side"]).apply(summc)
    f = df[df.side == "fall"].copy()
    f["q"] = f.groupby("h")["r30"].transform(lambda s: pd.qcut(s, 4, labels=["q1_bigfall", "q2", "q3", "q4_smallfall"]))
    out["fall_by_h_quartile"] = f.groupby(["h", "q"]).apply(summc)
    f20 = f[f.h == 20]
    out["fall20_by_coin"] = f20.groupby("coin").apply(summc)
    out["fall20_by_win"] = f20.groupby("win").apply(summc)
    out["fall20_by_agit"] = f20.dropna(subset=["agit"]).groupby("agit").apply(summc)
    f10 = f[f.h == 10]
    out["fall10_by_win"] = f10.groupby("win").apply(summc)
    out["fall10_by_agit"] = f10.dropna(subset=["agit"]).groupby("agit").apply(summc)
    return out
