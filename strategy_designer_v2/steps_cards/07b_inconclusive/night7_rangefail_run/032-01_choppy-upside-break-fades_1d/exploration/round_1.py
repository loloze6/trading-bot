def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    H = [1,3,5,10]
    rows = []
    drift = {h: [] for h in H}
    for coin, ws in bars.items():
        for w, df in ws.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            c = df["close"].values; hi = df["high"].values; lo = df["low"].values
            n = len(df)
            ph = pd.Series(hi).rolling(20).max().shift(1).values
            pl = pd.Series(lo).rolling(20).min().shift(1).values
            tr = (pd.Series(c)/pd.Series(c).shift(60)-1).values*100
            for h in H:
                for i in range(0, n-h, h):
                    drift[h].append((coin, c[i+h]/c[i]-1))
            for i in range(n):
                if np.isnan(ph[i]) or np.isnan(tr[i]): continue
                up = (c[i]/ph[i]-1)*100; dn = (c[i]/pl[i]-1)*100
                if up <= 0 and dn >= 0: continue
                prof = "choppy" if -10 <= tr[i] <= 10 else ("rising" if tr[i] > 10 else "falling")
                r = {"coin": coin, "w": w, "i": i, "side": "up" if up > 0 else "down",
                     "over": up if up > 0 else -dn, "prof": prof, "yr": df["timestamp"].iloc[i].year if hasattr(df["timestamp"].iloc[i],'year') else pd.Timestamp(df["timestamp"].iloc[i]).year}
                for h in H:
                    r[f"r{h}"] = c[i+h]/c[i]-1 if i+h < n else np.nan
                rows.append(r)
    R = pd.DataFrame(rows)
    dm = {h: pd.DataFrame(drift[h], columns=["coin","r"]).groupby("coin")["r"].mean() for h in H}
    for h in H:
        R[f"u{h}"] = R[f"r{h}"] - R["coin"].map(dm[h])
        # direction: fade = against break
        R[f"f{h}"] = np.where(R.side=="up", -R[f"u{h}"], R[f"u{h}"])
    # keep first break per 5-bar block to reduce overlap
    R["cell"] = R["i"]//5
    Rg = R.groupby(["coin","w","side","cell"]).first().reset_index()
    def summ(g):
        out = {"n": len(g)}
        for h in H:
            x = g[f"f{h}"].dropna()
            out[f"fade{h}%"] = x.mean()*100
            out[f"t{h}"] = x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan
        return pd.Series(out)
    res = {}
    res["by side x profile (fade = against break)"] = Rg.groupby(["side","prof"]).apply(summ).round(3)
    ch = Rg[Rg.prof=="choppy"].copy()
    ch["q"] = ch.groupby("side")["over"].transform(lambda s: pd.qcut(s, 3, labels=["small","mid","large"]))
    res["choppy by side x overshoot tercile"] = ch.groupby(["side","q"]).apply(summ).round(3)
    res["choppy up by coin"] = ch[ch.side=="up"].groupby("coin").apply(summ).round(3)
    res["choppy up by year"] = ch[ch.side=="up"].groupby("yr").apply(summ).round(3)
    res["choppy down by coin"] = ch[ch.side=="down"].groupby("coin").apply(summ).round(3)
    return res
