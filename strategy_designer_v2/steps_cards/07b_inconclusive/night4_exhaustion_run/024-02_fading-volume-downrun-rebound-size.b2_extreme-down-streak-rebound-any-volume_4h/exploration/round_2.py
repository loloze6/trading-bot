def explore(data):
    import numpy as np, pandas as pd
    H = [6, 18, 36]
    bars = data["bars"]
    drift = {}
    for c in bars:
        for h in H:
            rs = []
            for w, b in bars[c].items():
                cl = b["close"].values
                idx = np.arange(0, len(cl) - h, h)
                rs.extend(cl[idx + h] / cl[idx] - 1)
            drift[(c, h)] = np.mean(rs)
    rows = []
    for c in bars:
        for w, b in bars[c].items():
            b = b.reset_index(drop=True)
            cl = b["close"].values.astype(float)
            f = b["forecast"].fillna(0).values
            r = np.r_[np.nan, cl[1:] / cl[:-1] - 1]
            usual = pd.Series(np.abs(r)).rolling(180, min_periods=45).mean().values
            ssum = np.zeros(len(cl)); nbar = np.zeros(len(cl))
            for i in range(1, len(cl)):
                if r[i] < 0:
                    ssum[i] = ssum[i-1] + r[i]; nbar[i] = nbar[i-1] + 1
            z = -ssum / usual
            tr30 = pd.Series(cl).pct_change(180).values
            yr = pd.to_datetime(b["timestamp"]).dt.year.values
            low = 0.0; taken = set()
            for i in range(len(cl)):
                if f[i] < low: low = f[i]
                if f[i] - low >= 2 and f[i] > 0:
                    cell = i // 18
                    if cell not in taken:
                        taken.add(cell)
                        d = {"coin": c, "year": yr[i], "fc": f[i], "z": z[i], "nbar": nbar[i], "tr30": tr30[i]}
                        for h in H:
                            d[f"u{h}"] = (cl[i+h]/cl[i]-1 - drift[(c, h)]) if i + h < len(cl) else np.nan
                        rows.append(d)
                    low = f[i]
                if f[i] == 0: low = 0.0
    df = pd.DataFrame(rows)
    def summ(g):
        out = {"n": g["u18"].notna().sum()}
        for h in H:
            x = g[f"u{h}"].dropna()
            out[f"m{h}"] = x.mean(); out[f"t{h}"] = x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan
        return pd.Series(out)
    res = {}
    df["zd"] = pd.qcut(df["z"], 10, labels=False, duplicates="drop")
    res["by_z_decile"] = df.groupby("zd").apply(summ).join(df.groupby("zd")["z"].mean().rename("zmean"))
    top = df[df["z"] >= df["z"].quantile(0.8)].copy()
    res["top_z_by_coin"] = top.groupby("coin").apply(summ)
    res["top_z_by_year"] = top.groupby("year").apply(summ)
    top["trend"] = np.where(top["tr30"] > 0, "up30", np.where(top["tr30"] <= 0, "down30", "na"))
    res["top_z_by_trend"] = top.groupby("trend").apply(summ)
    rest = df[df["z"] < df["z"].quantile(0.8)]
    res["rest_by_year"] = rest.groupby("year").apply(summ)
    res["corr_z_u36_top"] = float(top[["z", "u36"]].dropna().corr().iloc[0, 1])
    res["share_fc20"] = float((df["fc"] >= 19.9).mean())
    return res
