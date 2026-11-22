import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    H = [2, 6, 12, 24]
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
            d = pd.DataFrame({"z": r / sd, "vr": vr,
                              "yr": pd.to_datetime(b["timestamp"]).dt.year,
                              "pos": np.arange(len(b))})
            cv = c.values
            for h in H:
                fr = np.full(len(b), np.nan)
                fr[:len(b) - h] = cv[h:] / cv[:len(b) - h] - 1
                d["u%d" % h] = fr - drift[(coin, h)]
                d["sd%d" % h] = sd * np.sqrt(h)
            d["coin"] = coin; d["w"] = w
            rows.append(d)
    D = pd.concat(rows, ignore_index=True).dropna(subset=["z", "vr"])
    D["az"] = D["z"].abs(); D["sgn"] = np.sign(D["z"])

    def summ(sub, h, name):
        sub = sub.assign(cell=sub.pos // h).groupby(["coin", "w", "cell"]).head(1)
        x = (sub["u%d" % h] * sub["sgn"]).dropna()
        st = (x / sub.loc[x.index, "sd%d" % h]).mean()
        return pd.Series({"n": len(x), "mean%": round(x.mean() * 100, 3),
                          "t": round(x.mean() / (x.std() / np.sqrt(len(x))), 2),
                          "strength": round(st, 3)}, name=name)

    out = {}
    for h in [2, 6, 24]:
        res = []
        for side, s in [("down", -1), ("up", 1)]:
            S = D[(D.sgn == s) & (D.az >= 3)]
            for lo, hi in [(0, 1.5), (1.5, 3), (3, 6), (6, 1e9)]:
                res.append(summ(S[(S.vr >= lo) & (S.vr < hi)], h, "%s z3 vr[%g,%g)" % (side, lo, hi)))
        out["by side and volume ratio, h=%d" % h] = pd.DataFrame(res)

    # graded: rank corr of z*vr with continuation, up and down, over 24h, among |z|>=2
    res = []
    for side, s in [("down", -1), ("up", 1)]:
        S = D[(D.sgn == s) & (D.az >= 2)]
        for h in [2, 6, 24]:
            sub = S.assign(cell=S.pos // h).groupby(["coin", "w", "cell"]).head(1)
            x = (sub["u%d" % h] * sub["sgn"]); ok = x.notna()
            rho, p = stats.spearmanr((sub.az * sub.vr)[ok], x[ok])
            rho2, p2 = stats.spearmanr(sub.vr[ok], x[ok])
            res.append(pd.Series({"n": ok.sum(), "rho_zvr": round(rho, 4), "p": round(p, 3),
                                  "rho_vr": round(rho2, 4), "p_vr": round(p2, 3)}, name="%s h%d" % (side, h)))
    out["graded rank corr |z|>=2"] = pd.DataFrame(res)

    S = D[(D.sgn == 1) & (D.az >= 3) & (D.vr >= 3)]
    out["up z3vr3 h24 by year"] = pd.DataFrame([summ(S[S.yr == y], 24, str(y)) for y in sorted(S.yr.unique())])
    out["up z3vr3 h24 by coin"] = pd.DataFrame([summ(S[S.coin == k], 24, k) for k in S.coin.unique()])
    S = D[(D.sgn == -1) & (D.az >= 3) & (D.vr >= 3)]
    out["down z3vr3 h2 by coin"] = pd.DataFrame([summ(S[S.coin == k], 2, k) for k in S.coin.unique()])
    return out
