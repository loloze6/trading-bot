import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    bars = data["bars"]
    H = [3, 5, 10]
    rows = []
    for coin, wins in bars.items():
        d = {}
        for h in H + [30]:
            rs = []
            for w, df in wins.items():
                c = df["close"].values
                for i in range(0, len(c) - h, h):
                    rs.append(c[i + h] / c[i] - 1)
            d[h] = (np.mean(rs), np.std(rs, ddof=1))
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            ts = pd.to_datetime(df["timestamp"])
            n = len(df)
            ret30 = pd.Series(c).pct_change(30).values
            low30 = pd.Series(c).shift(1).rolling(30).min().values
            reg = (df["regime"] == "mean_reversion").values
            for h in H:
                used = set()
                for i in range(n):
                    if np.isnan(low30[i]) or not (c[i] < low30[i]) or i + h >= n:
                        continue
                    cell = i // h
                    key = cell
                    if key in used:
                        continue
                    used.add(key)
                    rows.append({"coin": coin, "win": w, "year": ts[i].year, "day": ts[i].normalize(), "h": h,
                                 "inreg": reg[i], "ret30": ret30[i], "z30": ret30[i] / d[30][1],
                                 "u": c[i + h] / c[i] - 1 - d[h][0]})
    R = pd.DataFrame(rows).dropna(subset=["ret30"])
    def summ(g):
        x = g["u"]
        dd = g.groupby("day")["u"].sum()
        G = len(dd)
        t = x.mean() / (dd.std(ddof=1) * np.sqrt(G) / len(x)) if G > 1 else np.nan
        return pd.Series({"n": len(x), "days": G, "mean": x.mean(), "t": t,
                          "rho_z30": stats.spearmanr(g["z30"], x)[0] if len(x) > 3 else np.nan})
    out = {}
    out["newlow_by_h_reg"] = R.groupby(["h", "inreg"]).apply(summ)
    R = R.copy()
    R["zq"] = R.groupby(["h", "inreg"])["z30"].transform(lambda s: pd.qcut(s.rank(method="first"), 3, labels=False))
    out["newlow_by_h_reg_zq"] = R.groupby(["h", "inreg", "zq"]).apply(summ)
    out["z30_tercile_bounds_inreg"] = R[R.inreg & (R.h == 5)].groupby("zq")["z30"].agg(["min", "max", "mean"])
    D = R[R.inreg & (R.zq == 0)]
    out["deep_inreg_by_coin_h5"] = D[D.h == 5].groupby("coin").apply(summ)
    out["deep_inreg_by_year_h5"] = D[D.h == 5].groupby("year").apply(summ)
    A = R[R.h == 5]
    out["all_newlow_h5_by_year_rho"] = A.groupby(["inreg", "year"]).apply(summ)
    return out
