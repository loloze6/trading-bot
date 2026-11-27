def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    usual = {}
    for coin, wins in bars.items():
        rets3 = []
        for w, df in wins.items():
            c = df["close"].values
            n = len(c)
            for i in range(0, n - 3, 3):
                rets3.append(c[i+3]/c[i]-1)
        drift = np.mean(rets3); usual[coin] = (drift, np.std(rets3, ddof=1))
        for w, df in wins.items():
            c = df["close"].values
            n = len(c)
            ts = pd.to_datetime(df["timestamp"]).values
            yr = pd.to_datetime(df["timestamp"]).dt.year.values
            up = np.r_[False, c[1:] > c[:-1]]
            dn = np.r_[False, c[1:] < c[:-1]]
            runlen = np.zeros(n, int)
            for i in range(1, n):
                if up[i]:
                    k = 0; j = i-1
                    while j >= 1 and dn[j]:
                        k += 1; j -= 1
                    runlen[i] = k
            for cell in range(0, n, 3):
                for i in range(cell, min(cell+3, n)):
                    if runlen[i] >= 1:
                        rec = dict(coin=coin, w=w, yr=yr[i], run=runlen[i],
                                   upsize=c[i]/c[i-1]-1, day=ts[i])
                        for h in (1, 2, 3, 5, 7, 10):
                            rec["r%d" % h] = -(c[i+h]/c[i]-1) if i+h < n else np.nan
                        # 20-day trend within window
                        rec["tr20"] = c[i]/c[i-20]-1 if i >= 20 else np.nan
                        rec["vol20"] = np.std(np.diff(np.log(c[i-20:i+1]))) if i >= 20 else np.nan
                        rows.append(rec)
                        break
    d = pd.DataFrame(rows)
    d["drift"] = d.coin.map(lambda x: usual[x][0])
    d["u3"] = d["r3"] + d["drift"]   # short-signed unusual: -(r) - (-drift)... r3 already short-signed, unusual = r3 + drift
    def tday(s, dd):
        x = pd.DataFrame({"v": s, "day": dd}).dropna()
        g = x.groupby("day")["v"].sum()
        nd = len(g); m = x.v.mean(); n = len(x)
        se = np.sqrt(((g - g.mean()*0)**2).sum())/n if n else np.nan
        dev = x.v - m
        se = np.sqrt((dev.groupby(x.day).sum()**2).sum())/n
        return pd.Series({"mean": m, "t": m/se, "n": n, "days": nd})
    out = {}
    out["all"] = tday(d.u3, d.day)
    d["runb"] = d.run.clip(upper=5)
    out["by_run"] = d.groupby("runb").apply(lambda g: tday(g.u3, g.day))
    out["by_coin"] = d.groupby("coin").apply(lambda g: tday(g.u3, g.day))
    out["by_window"] = d.groupby("w").apply(lambda g: tday(g.u3, g.day))
    out["by_year"] = d.groupby("yr").apply(lambda g: tday(g.u3, g.day))
    hz = {}
    for h in (1, 2, 3, 5, 7, 10):
        dr = d.coin.map(lambda x: usual[x][0]) * h / 3
        hz["h%d" % h] = tday(d["r%d" % h] + dr, d.day)
    out["by_horizon_all"] = pd.DataFrame(hz).T
    hz3 = {}
    l = d[d.run >= 3]
    for h in (1, 2, 3, 5, 7, 10):
        dr = l.coin.map(lambda x: usual[x][0]) * h / 3
        hz3["h%d" % h] = tday(l["r%d" % h] + dr, l.day)
    out["by_horizon_run3plus"] = pd.DataFrame(hz3).T
    d["trq"] = pd.qcut(d.tr20, 3, labels=["down", "mid", "up"])
    out["by_trend20"] = d.groupby("trq").apply(lambda g: tday(g.u3, g.day))
    d["vq"] = pd.qcut(d.vol20, 2, labels=["calm", "agit"])
    out["by_vol20"] = d.groupby("vq").apply(lambda g: tday(g.u3, g.day))
    d["upq"] = pd.qcut(d.upsize, 3, labels=["small", "mid", "large"])
    out["by_upsize"] = d.groupby("upq").apply(lambda g: tday(g.u3, g.day))
    out["corr_run_u3"] = float(d[["run", "u3"]].corr().iloc[0, 1])
    return out
