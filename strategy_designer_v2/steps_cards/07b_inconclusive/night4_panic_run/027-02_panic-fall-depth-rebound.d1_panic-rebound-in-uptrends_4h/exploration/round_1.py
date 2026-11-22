import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    bars = data["bars"]
    rows = []
    drift = {}
    for H in (42, 84):
        for coin, ws in bars.items():
            r = []
            for w, df in ws.items():
                c = df["close"].values
                idx = np.arange(0, len(c) - H, H)
                r += list(c[idx + H] / c[idx] - 1)
            drift[(coin, H)] = (np.mean(r), np.std(r))
    for coin, ws in bars.items():
        for w, df in ws.items():
            df = df.reset_index(drop=True)
            c = df["close"]; rng = (df["high"] - df["low"]) / df["close"]
            ratio = rng.rolling(180).mean() / rng.rolling(6).mean()
            panic = ratio <= 0.3333
            r6 = c / c.shift(6) - 1
            fall_z = -r6 / r6.abs().rolling(180).mean()
            r540 = c / c.shift(540) - 1
            r42 = c / c.shift(42) - 1
            f = df["forecast"].fillna(0)
            sig = (f >= 2) & (f.shift(1).fillna(0) < 2)
            n = len(df)
            yr = pd.to_datetime(df["timestamp"]).dt.year
            for kind, mask in (("bet", sig), ("panic", panic)):
                cell = np.arange(n) // 84
                seen = set()
                for i in np.where(mask.values)[0]:
                    if cell[i] in seen: continue
                    seen.add(cell[i])
                    rec = dict(coin=coin, w=w, kind=kind, year=yr[i], fall=fall_z[i],
                               r90=r540[i], r7pre=r42[i], fc=f[i], yr=yr[i])
                    for H in (42, 84):
                        if i + H < n:
                            m, s = drift[(coin, H)]
                            rec[f"u{H}"] = c[i + H] / c[i] - 1 - m
                            rec[f"s{H}"] = rec[f"u{H}"] / s
                    rows.append(rec)
    d = pd.DataFrame(rows)
    def summ(g, col="u84"):
        x = g[col].dropna()
        return pd.Series(dict(n=len(x), mean=x.mean(), median=x.median(),
                              t=x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan,
                              hit=(x > 0).mean()))
    bet = d[d.kind == "bet"]; pan = d[d.kind == "panic"]
    out = {}
    out["bets all u84"] = summ(bet).to_frame().T
    out["bets all u42"] = summ(bet, "u42").to_frame().T
    out["bets by coin"] = bet.groupby("coin").apply(summ)
    out["bets by year"] = bet.groupby("year").apply(summ)
    out["bets forecast dist"] = bet["fc"].describe()
    out["bets trimmed (drop top/bottom 5%)"] = summ(bet[(bet.u84 > bet.u84.quantile(.05)) & (bet.u84 < bet.u84.quantile(.95))]).to_frame().T
    pan = pan.assign(up=np.where(pan.r90 > 0, "r90>0", "r90<=0"))
    out["panic by r90 sign u84"] = pan.groupby("up").apply(summ)
    out["panic by r90 sign u42"] = pan.groupby("up").apply(lambda g: summ(g, "u42"))
    pf = pan[pan.fall > 0].copy()
    pf["fallq"] = pd.qcut(pf.fall, 3, labels=["low", "mid", "high"])
    out["panic falls by depth u84"] = pf.groupby("fallq").apply(summ)
    out["panic falls by depth u42"] = pf.groupby("fallq").apply(lambda g: summ(g, "u42"))
    out["panic rises (fall<=0) u84"] = summ(pan[pan.fall <= 0]).to_frame().T
    pfu = pf[pf.r90 > 0].copy()
    pfu["r90q"] = pd.qcut(pfu.r90, 3, labels=["low", "mid", "high"])
    out["panic falls in uptrend by r90 u84"] = pfu.groupby("r90q").apply(summ)
    out["panic all by coin u84"] = pan.groupby("coin").apply(summ)
    out["panic falls by year u84"] = pf.groupby("year").apply(summ)
    return out
