import pandas as pd, numpy as np

def explore(data):
    bars = data["bars"]
    H = [3, 5, 10]
    drift = {}
    for c, ws in bars.items():
        for h in H:
            r = []
            for w, df in ws.items():
                cl = df["close"].values
                idx = np.arange(0, len(cl) - h, h)
                r += list(cl[idx + h] / cl[idx] - 1)
            drift[(c, h)] = np.mean(r)
    rows = []
    for c, ws in bars.items():
        for w, df in ws.items():
            df = df.reset_index(drop=True)
            cl = df["close"].values
            reg = df["regime"].astype(str).values
            ts = pd.to_datetime(df["timestamp"])
            dr = pd.Series(cl).pct_change().values
            n = len(df)
            for h in H:
                for i in range(0, n - h, h):
                    if reg[i] != "unknown" or i < 30:
                        continue
                    sd = np.nanstd(dr[i-29:i+1], ddof=1)
                    z = (cl[i] / cl[i-3] - 1) / sd
                    tot = -(cl[i + h] / cl[i] - 1)
                    rows.append({"coin": c, "h": h, "day": ts[i].normalize(), "year": ts[i].year,
                                 "z": z, "unu": tot + drift[(c, h)], "tot": tot})
    d = pd.DataFrame(rows)

    def clt(s, col):
        if len(s) < 3: return (len(s), np.nan, np.nan, np.nan)
        dev = s[col] - s[col].mean()
        g = dev.groupby(s["day"]).sum(); G = len(g)
        se = np.sqrt((g**2).sum() * G / (G - 1)) / len(s)
        return (len(s), G, s[col].mean(), s[col].mean() / se if se > 0 else np.nan)

    out = {}
    bins = [-np.inf, -1.5, -0.5, 0, 0.5, 1.0, 1.6, np.inf]
    for h in H:
        s = d[d.h == h].copy()
        s["zb"] = pd.cut(s["z"], bins)
        res = []
        for k, g in s.groupby("zb", observed=True):
            n, G, m, t = clt(g, "unu")
            res.append({"zbin": str(k), "cases": n, "days": G, "short_unusual": m, "t": t,
                        "short_total": g["tot"].mean()})
        n, G, m, t = clt(s, "unu")
        res.append({"zbin": "all profile bars", "cases": n, "days": G, "short_unusual": m, "t": t,
                    "short_total": s["tot"].mean()})
        n, G, m, t = clt(s[s.z > 0], "unu")
        res.append({"zbin": "rises only", "cases": n, "days": G, "short_unusual": m, "t": t,
                    "short_total": s[s.z > 0]["tot"].mean()})
        n, G, m, t = clt(s[s.z <= 0], "unu")
        res.append({"zbin": "falls only", "cases": n, "days": G, "short_unusual": m, "t": t,
                    "short_total": s[s.z <= 0]["tot"].mean()})
        out[f"profile_h{h}"] = pd.DataFrame(res)
        out[f"corr_z_unu_h{h}"] = float(s[["z", "unu"]].corr().iloc[0, 1])
    return out
