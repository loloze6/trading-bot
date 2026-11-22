def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = [6, 12, 18, 36]
    bars = data["bars"]
    # normal drift per coin per horizon, non-overlapping
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
            # case: forecast rises >= 2 above its low since last bet; first per grid cell
            low = 0.0; armed = True
            taken = set()
            for i in range(len(cl)):
                if f[i] < low: low = f[i]
                if f[i] - low >= 2 and f[i] > 0:
                    cell = i // 18
                    if cell not in taken:
                        taken.add(cell)
                        d = {"coin": c, "win": w, "year": yr[i], "fc": f[i], "z": z[i],
                             "nbar": nbar[i], "tr30": tr30[i]}
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
    res["all"] = summ(df).to_frame().T
    res["by_coin"] = df.groupby("coin").apply(summ)
    res["by_year"] = df.groupby("year").apply(summ)
    df["zq"] = pd.qcut(df["z"], 5, labels=False, duplicates="drop")
    res["by_z_quintile"] = df.groupby("zq").apply(summ).join(df.groupby("zq")["z"].mean().rename("zmean"))
    df["fq"] = pd.qcut(df["fc"].rank(method="first"), 5, labels=False)
    res["by_fc_quintile"] = df.groupby("fq").apply(summ).join(df.groupby("fq")["fc"].mean().rename("fcmean"))
    df["trend"] = np.where(df["tr30"] > 0, "up30", np.where(df["tr30"] <= 0, "down30", "na"))
    res["by_trend30"] = df.groupby("trend").apply(summ)
    df["nb"] = pd.cut(df["nbar"], [0, 2, 3, 4, 6, 100])
    res["by_streak_len"] = df.groupby("nb").apply(summ)
    res["corr_z_u18"] = float(df[["z", "u18"]].dropna().corr().iloc[0, 1])
    return res
