import numpy as np, pandas as pd

def explore(data):
    H = [1, 2, 3, 6, 12, 24]
    drift = {}
    for coin, ws in data["bars"].items():
        for h in H:
            g = []
            for w, b in ws.items():
                c = b["close"].values
                idx = np.arange(0, len(c) - h, h)
                g.append(c[idx + h] / c[idx] - 1)
            drift[(coin, h)] = np.concatenate(g).mean()
    rows = []
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            c = b["close"]; v = b["volume"]
            r = c.pct_change()
            sd = r.rolling(720, min_periods=240).std()
            vr = v / v.rolling(720, min_periods=240).mean()
            d = pd.DataFrame({"z": r / sd, "vr": vr, "fc": b["forecast"],
                              "yr": pd.to_datetime(b["timestamp"]).dt.year,
                              "cell": np.arange(len(b)) // 6})
            cv = c.values
            for h in H:
                fr = np.full(len(b), np.nan)
                fr[:len(b) - h] = cv[h:] / cv[:len(b) - h] - 1
                d["u%d" % h] = fr - drift[(coin, h)]
            d["coin"] = coin; d["w"] = w
            rows.append(d)
    D = pd.concat(rows, ignore_index=True).dropna(subset=["z", "vr"])
    D["az"] = D["z"].abs(); D["sgn"] = np.sign(D["z"])

    def summ(sub, name, sgn=None):
        sub = sub.groupby(["coin", "w", "cell"]).head(1)
        s = sub["sgn"] if sgn is None else sgn
        out = {"n": len(sub)}
        for h in H:
            x = (sub["u%d" % h] * (s if np.isscalar(s) else s.loc[sub.index])).dropna()
            out["m%d%%" % h] = round(x.mean() * 100, 3)
            out["t%d" % h] = round(x.mean() / (x.std() / np.sqrt(len(x))), 2) if len(x) > 2 else np.nan
        return pd.Series(out, name=name)

    res = []
    for side, s in [("down", -1), ("up", 1)]:
        S = D[D.sgn == s]
        res.append(summ(S[(S.az >= 3) & (S.vr >= 3)], side + " z3 vr3"))
        res.append(summ(S[(S.az >= 4) & (S.vr >= 5)], side + " z4 vr5"))
        res.append(summ(S[(S.az >= 3) & (S.vr < 1.5)], side + " z3 vr<1.5"))
    T1 = pd.DataFrame(res)

    F = D[D.fc <= -2].copy()
    F["fb"] = pd.cut(-F.fc, [2, 4, 8, 15, 20.01], include_lowest=True).astype(str)
    T2 = pd.DataFrame([summ(F[F.fb == k], k, sgn=-1) for k in sorted(F.fb.unique())])

    S = D[(D.sgn == -1) & (D.az >= 3) & (D.vr >= 3)]
    T3 = pd.DataFrame([summ(S[S.yr == y], str(y)) for y in sorted(S.yr.unique())])
    T4 = pd.DataFrame([summ(S[S.coin == k], k) for k in S.coin.unique()])
    return {"groups (continuation +)": T1, "strategy short cases by |forecast|": T2,
            "down z3vr3 by year": T3, "down z3vr3 by coin": T4}
