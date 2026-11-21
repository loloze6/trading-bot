def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []; drift = {}
    for coin, wins in bars.items():
        for h in [18, 36]:
            rs = []
            for w, df in wins.items():
                c = df["close"].values
                idx = np.arange(0, len(c) - h, h)
                rs.extend(c[idx + h] / c[idx] - 1)
            drift[(coin, h)] = np.mean(rs)
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values; hi = df["high"].values; lo = df["low"].values
            f = df["forecast"].fillna(0).values; n = len(df)
            Hh = pd.Series(hi).shift(1).rolling(12).max().values
            Ll = pd.Series(lo).shift(1).rolling(12).min().values
            B = pd.Series(hi - lo).rolling(180, min_periods=45).mean().values
            brk = (c - Hh) / c * 100
            brkB = (c - Hh) / B
            r7 = pd.Series(c).pct_change(42).values
            vol = pd.Series(np.log(c)).diff().rolling(180).std().values
            vm = np.nanmedian(vol)
            ts = pd.to_datetime(df["timestamp"])
            seen = set()
            for t in range(1, n):
                if f[t] >= 2 and f[t-1] < 2:
                    cell = t // 18
                    if cell in seen or t + 18 >= n: continue
                    seen.add(cell)
                    rec = dict(coin=coin, year=ts.iloc[t].year, brk=brk[t], brkB=brkB[t],
                               narrow=B[t]/(Hh[t]-Ll[t]), r7=r7[t], hv=vol[t] > vm,
                               x18=c[t+18]/c[t]-1-drift[(coin,18)])
                    rec["x36"] = c[t+36]/c[t]-1-drift[(coin,36)] if t+36 < n else np.nan
                    rows.append(rec)
    d = pd.DataFrame(rows).dropna(subset=["r7", "brk"])
    def summ(g, col="x18"):
        x = g[col].dropna()
        return pd.Series({"n": len(x), "mean%": x.mean()*100,
                          "t": x.mean()/(x.std()/np.sqrt(len(x))) if len(x) > 2 else np.nan})
    out = {}
    d["r7q"] = pd.qcut(d["r7"], 5, labels=False)
    out["by_r7_q"] = d.groupby("r7q").apply(summ).join(d.groupby("r7q")["r7"].median())
    out["by_r7_q_x36"] = d.groupby("r7q").apply(lambda g: summ(g, "x36"))
    d["bq"] = pd.qcut(d["brk"], 3, labels=False)
    out["brk3_x_r7sign"] = d.groupby([d["r7"] > 0, "bq"]).apply(summ)
    d["bBq"] = pd.qcut(d["brkB"], 5, labels=False)
    out["by_brkB_q"] = d.groupby("bBq").apply(summ).join(d.groupby("bBq")["brkB"].median())
    pos = d[d["r7"] > 0]
    out["r7pos_by_year"] = pos.groupby("year").apply(summ)
    out["r7pos_by_coin"] = pos.groupby("coin").apply(summ)
    sp = {}
    for col in ["brk", "brkB", "narrow", "r7"]:
        for y in ["x18", "x36"]:
            s = d[[col, y]].dropna()
            sp[f"{col}~{y}"] = stats.spearmanr(s[col], s[y])[0]
    s = pos[["r7", "x18"]].dropna()
    sp["r7pos: r7~x18"] = stats.spearmanr(s["r7"], s["x18"])[0]
    s = pos[["brk", "x18"]].dropna()
    sp["r7pos: brk~x18"] = stats.spearmanr(s["brk"], s["x18"])[0]
    out["spearman"] = pd.Series(sp)
    out["r7_x_hv"] = d.groupby([d["r7"] > 0, "hv"]).apply(summ)
    return out
