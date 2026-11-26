def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    bars = data["bars"]

    def cl_ols(X, y, g):
        X = np.column_stack([np.ones(len(y))] + [np.asarray(x, float) for x in X]); y = np.asarray(y, float)
        XtX = np.linalg.inv(X.T @ X); b = XtX @ X.T @ y; e = y - X @ b
        S = pd.DataFrame(X * e[:, None]).groupby(np.asarray(g)).sum().values; G = len(S)
        V = XtX @ (S.T @ S) @ XtX * G / (G - 1)
        return b[1:], b[1:] / np.sqrt(np.diag(V)[1:]), G

    def build(h):
        recs = []
        for coin, ws in bars.items():
            per = []
            for w, b in ws.items():
                c = b["close"].values.astype(float); n = len(c)
                r1 = np.r_[np.nan, np.diff(np.log(c))]
                for p in range(0, n - h, h):
                    if p < 60: continue
                    per.append(dict(coin=coin, w=w, ts=b["timestamp"].iloc[p],
                                    yr=pd.Timestamp(b["timestamp"].iloc[p]).year,
                                    regime=b["regime"].iloc[p],
                                    fwd=c[p + h] / c[p] - 1,
                                    vol10=np.nanstd(r1[p - 9:p + 1]), vol60=np.nanstd(r1[p - 59:p + 1]),
                                    vol30=np.nanstd(r1[p - 29:p + 1]),
                                    p10=c[p] / c[p - 10] - 1))
            if not per: continue
            d = pd.DataFrame(per)
            d["exz"] = (d["fwd"] - d["fwd"].mean()) / d["fwd"].std()
            d["ex"] = d["fwd"] - d["fwd"].mean()
            recs.append(d)
        D = pd.concat(recs, ignore_index=True)
        D["vratio"] = np.log(D["vol10"] / D["vol60"])
        D["volz"] = D.groupby("coin")["vol30"].transform(lambda s: s / s.mean())
        D["vr_r"] = D.groupby("coin")["vratio"].rank(pct=True)
        D["vz_r"] = D.groupby("coin")["volz"].rank(pct=True)
        D["p10_r"] = D.groupby("coin")["p10"].rank(pct=True)
        D["up"] = np.sign(D["p10"])
        return D

    rows = []; halves = []; quint = []; yrs = []
    for h in [7, 14, 21, 30]:
        D = build(h).dropna(subset=["vratio", "volz", "exz"])
        b, t, G = cl_ols([D["vr_r"]], D["exz"], D["ts"])
        b2, t2, _ = cl_ols([D["vr_r"], D["vz_r"]], D["exz"], D["ts"])
        b3, t3, _ = cl_ols([D["vr_r"], D["p10_r"]], D["exz"], D["ts"])
        rows.append(dict(h=h, vr_slope=b[0], vr_t=t[0], vr_with_volz=b2[0], t_=t2[0], volz_with_vr=b2[1], tv=t2[1],
                         vr_with_p10=b3[0], t3=t3[0], n=len(D), days=G))
        D["half"] = np.where(D["yr"] <= 2021, "early", "late")
        for hf, s in D.groupby("half"):
            bb, tt, GG = cl_ols([s["vr_r"]], s["exz"], s["ts"])
            halves.append(dict(h=h, half=hf, slope=bb[0], t=tt[0], n=len(s), days=GG))
        if h == 14:
            D["q"] = D.groupby("coin")["vratio"].transform(lambda s: pd.qcut(s.rank(method="first"), 5, labels=False))
            for q, s in D.groupby("q"):
                y = s["ex"]; dev = y - y.mean(); g = dev.groupby(s["ts"]).sum(); GG = len(g)
                se = np.sqrt((g ** 2).sum() * GG / (GG - 1)) / len(y)
                quint.append(dict(q=q, vratio=s["vratio"].mean(), ex=y.mean(), exz=s["exz"].mean(), t=y.mean() / se, n=len(s), days=GG))
            for y_, s in D.groupby("yr"):
                yrs.append(dict(yr=y_, rho=stats.spearmanr(s["vratio"], s["exz"])[0], n=len(s)))
            # direction of the vol rise: after rising-vol up moves vs down moves
            dir_ = []
            for sg, s in D.groupby("up"):
                bb, tt, GG = cl_ols([s["vr_r"]], s["exz"], s["ts"])
                dir_.append(dict(p10_sign=sg, slope=bb[0], t=tt[0], n=len(s)))
            out["h14_vr_by_p10_sign"] = pd.DataFrame(dir_)
    out["vr_slopes_by_h"] = pd.DataFrame(rows)
    out["vr_by_half"] = pd.DataFrame(halves)
    out["h14_vr_quintiles_withincoin"] = pd.DataFrame(quint)
    out["h14_vr_rho_by_year"] = pd.DataFrame(yrs)
    return out
