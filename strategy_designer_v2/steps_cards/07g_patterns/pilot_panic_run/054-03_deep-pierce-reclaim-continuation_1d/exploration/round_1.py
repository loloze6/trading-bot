import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            d = df.reset_index(drop=True).copy()
            n = len(d)
            if n < 40: continue
            c, h, l, o = d["close"], d["high"], d["low"], d["open"]
            L30 = l.shift(1).rolling(30, min_periods=30).min()
            H30 = h.shift(1).rolling(30, min_periods=30).max()
            r1 = c.pct_change()
            r5p = c / c.shift(5) - 1
            r10p = c / c.shift(10) - 1
            vol30 = r1.rolling(30, min_periods=20).std()
            fwd1 = c.shift(-1) / c - 1
            fwd5 = c.shift(-5) / c - 1
            fwd3 = c.shift(-3) / c - 1
            rng = (h - l) / c
            clv = (c - l) / (h - l).replace(0, np.nan)
            dfo = pd.DataFrame({
                "coin": coin, "win": w, "pos": np.arange(n),
                "day": pd.to_datetime(d["timestamp"]).dt.floor("D"),
                "wd": pd.to_datetime(d["timestamp"]).dt.weekday,
                "year": pd.to_datetime(d["timestamp"]).dt.year,
                "fa": d["regime"].isin(["trending", "unknown"]).astype(int),
                "pierce_lo": np.where((l < L30) & (c >= L30), (L30 - l) / L30 * 100, 0.0),
                "newlo_close": ((c < L30)).astype(int),
                "pierce_hi": np.where((h > H30) & (c <= H30), (h - H30) / H30 * 100, 0.0),
                "newhi_close": ((c > H30)).astype(int),
                "r1": r1, "r5p": r5p, "r10p": r10p, "z1": r1 / vol30, "z5": r5p / (vol30 * np.sqrt(5)),
                "rngz": rng / vol30, "clv": clv, "fwd1": fwd1, "fwd3": fwd3, "fwd5": fwd5,
                "fwd5z": fwd5 / (vol30 * np.sqrt(5)), "valid30": L30.notna().astype(int)})
            rows.append(dfo)
    A = pd.concat(rows, ignore_index=True)
    A = A[A.valid30 == 1]
    drift5 = A[A.pos % 5 == 0].groupby("coin")["fwd5"].mean()
    drift1 = A.groupby("coin")["fwd1"].mean()
    A["u5"] = A["fwd5"] - A["coin"].map(drift5)
    A["u1"] = A["fwd1"] - A["coin"].map(drift1)

    def summ(sub, col="u5"):
        s = sub.dropna(subset=[col])
        if len(s) < 3: return pd.Series({"n": len(s), "days": 0, "mean%": np.nan, "t": np.nan})
        g = s.groupby("day")[col].sum()
        G = len(g)
        m = s[col].mean()
        dev = s.assign(dv=s[col] - m).groupby("day")["dv"].sum()
        se = np.sqrt((dev**2).sum() * G / max(G - 1, 1)) / len(s)
        return pd.Series({"n": len(s), "days": G, "mean%": 100 * m, "t": m / se if se > 0 else np.nan})

    out = {}
    ev = A[A.pierce_lo > 0]
    tab = {}
    tab["pierce_lo all"] = summ(ev)
    tab["pierce_lo FA"] = summ(ev[ev.fa == 1])
    tab["pierce_lo notFA"] = summ(ev[ev.fa == 0])
    q = ev.pierce_lo.median()
    tab["pierce_lo deep"] = summ(ev[ev.pierce_lo > q])
    tab["pierce_lo shallow"] = summ(ev[ev.pierce_lo <= q])
    tab["close new 30d low"] = summ(A[A.newlo_close == 1])
    tab["close new low FA"] = summ(A[(A.newlo_close == 1) & (A.fa == 1)])
    eh = A[A.pierce_hi > 0]
    tab["pierce_hi all"] = summ(eh)
    tab["close new 30d high"] = summ(A[A.newhi_close == 1])
    tab["grid all"] = summ(A[A.pos % 5 == 0])
    tab["grid FA"] = summ(A[(A.pos % 5 == 0) & (A.fa == 1)])
    out["events_u5"] = pd.DataFrame(tab).T

    G5 = A[A.pos % 5 == 0].dropna(subset=["u5", "z5"]).copy()
    G5["z5q"] = pd.qcut(G5["z5"], 5, labels=False)
    out["grid_by_past5z_quint"] = G5.groupby("z5q").apply(summ).reset_index()
    G5["z1q"] = pd.qcut(G5["z1"], 5, labels=False)
    out["grid_by_past1z_quint"] = G5.groupby("z1q").apply(summ).reset_index()
    G5["clvq"] = pd.qcut(G5["clv"], 5, labels=False, duplicates="drop")
    out["grid_by_clv_quint"] = G5.groupby("clvq").apply(summ).reset_index()
    G5["rq"] = pd.qcut(G5["rngz"], 5, labels=False)
    out["grid_by_rangez_quint"] = G5.groupby("rq").apply(summ).reset_index()

    B = A.dropna(subset=["u1", "z1"]).copy()
    B["z1q"] = pd.qcut(B["z1"], 10, labels=False)
    out["next1_by_z1_decile"] = B.groupby("z1q").apply(lambda s: summ(s, "u1")).reset_index()
    out["next1_by_weekday"] = B.groupby("wd").apply(lambda s: summ(s, "u1")).reset_index()
    out["next1_by_fa"] = B.groupby("fa").apply(lambda s: summ(s, "u1")).reset_index()
    out["share_FA_bars"] = float(A.fa.mean())
    out["n_pierce_lo_events"] = int(len(ev))
    return out
