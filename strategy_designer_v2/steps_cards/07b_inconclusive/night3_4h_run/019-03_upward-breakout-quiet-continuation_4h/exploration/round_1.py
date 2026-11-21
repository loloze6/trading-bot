def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    H_LIST = [6, 12, 18, 36]
    rows = []
    drift = {}
    usual = {}
    for coin, wins in bars.items():
        # normal drift per horizon
        for h in H_LIST:
            rs = []
            for w, df in wins.items():
                c = df["close"].values
                idx = np.arange(0, len(c) - h, h)
                rs.extend(c[idx + h] / c[idx] - 1)
            drift[(coin, h)] = np.mean(rs); usual[(coin, h)] = np.std(rs)
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values; hi = df["high"].values; lo = df["low"].values
            f = df["forecast"].fillna(0).values
            n = len(df)
            Hh = pd.Series(hi).shift(1).rolling(12).max().values
            Ll = pd.Series(lo).shift(1).rolling(12).min().values
            S = Hh - Ll
            B = pd.Series(hi - lo).rolling(180, min_periods=45).mean().values
            narrow = B / S
            brk = (c - Hh) / c * 100
            r30 = pd.Series(c).pct_change(180).values
            r7 = pd.Series(c).pct_change(42).values
            vol = pd.Series(np.log(c)).diff().rolling(180).std().values
            vol_med = np.nanmedian(vol)
            ts = pd.to_datetime(df["timestamp"])
            seen = set()
            for t in range(1, n):
                if f[t] >= 2 and f[t - 1] < 2:
                    cell = t // 18
                    if cell in seen: continue
                    if t + 18 >= n: continue
                    seen.add(cell)
                    rec = dict(coin=coin, win=w, year=ts.iloc[t].year, f=f[t],
                               narrow=narrow[t], brk=brk[t], r30=r30[t], r7=r7[t],
                               hv=vol[t] > vol_med, hour=ts.iloc[t].hour,
                               fol=c[t+1]/c[t]-1)
                    for h in H_LIST:
                        if t + h < n:
                            rec[f"x{h}"] = c[t + h] / c[t] - 1 - drift[(coin, h)]
                            rec[f"s{h}"] = rec[f"x{h}"] / usual[(coin, h)]
                    rows.append(rec)
    d = pd.DataFrame(rows)
    def summ(g, col="x18"):
        x = g[col].dropna()
        return pd.Series({"n": len(x), "mean%": x.mean()*100,
                          "t": x.mean()/(x.std()/np.sqrt(len(x))) if len(x) > 2 else np.nan,
                          "hit": (x > 0).mean()})
    out = {}
    out["all_by_horizon"] = pd.DataFrame({h: summ(d, f"x{h}") for h in H_LIST}).T
    out["strength_by_h"] = d[[f"s{h}" for h in H_LIST]].mean()
    out["by_coin"] = d.groupby("coin").apply(summ)
    out["by_year"] = d.groupby("year").apply(summ)
    out["by_window"] = d.groupby("win").apply(summ)
    out["forecast_desc"] = d["f"].describe()
    d["nq"] = pd.qcut(d["narrow"], 5, labels=False, duplicates="drop")
    d["bq"] = pd.qcut(d["brk"], 5, labels=False, duplicates="drop")
    out["by_narrow_q"] = d.groupby("nq").apply(summ).join(d.groupby("nq")["narrow"].median())
    out["by_break_q"] = d.groupby("bq").apply(summ).join(d.groupby("bq")["brk"].median())
    out["by_r30_sign"] = d.groupby(np.sign(d["r30"])).apply(summ)
    d["r30q"] = pd.qcut(d["r30"], 5, labels=False, duplicates="drop")
    out["by_r30_q"] = d.groupby("r30q").apply(summ).join(d.groupby("r30q")["r30"].median())
    out["by_r30_q_x36"] = d.groupby("r30q").apply(lambda g: summ(g, "x36"))
    out["by_r7_sign"] = d.groupby(np.sign(d["r7"])).apply(summ)
    out["by_highvol"] = d.groupby("hv").apply(summ)
    out["next_bar_mean%"] = d["fol"].mean()*100
    return out
