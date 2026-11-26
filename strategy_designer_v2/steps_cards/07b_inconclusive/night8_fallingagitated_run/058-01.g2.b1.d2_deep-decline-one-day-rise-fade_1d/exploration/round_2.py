import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]
    H = [1, 2, 3]
    rows = []
    for coin, wins in bars.items():
        d = {}
        for h in H:
            rr = []
            for w, df in wins.items():
                c = df["close"].values
                for i in range(0, len(c) - h, h):
                    rr.append(c[i + h] / c[i] - 1)
            d[h] = (np.mean(rr), np.std(rr, ddof=1))
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            n = len(c)
            ret1 = pd.Series(c).pct_change()
            sd30 = ret1.rolling(30, min_periods=20).std()
            r60 = pd.Series(c).pct_change(60)
            reg = df["regime"].astype(str).values
            fc = df["forecast"].values
            ts = pd.to_datetime(df["timestamp"])
            for i in range(n):
                if reg[i] not in ("trending", "unknown"):
                    continue
                row = dict(coin=coin, win=w, i=i, year=ts.iloc[i].year, day=ts.iloc[i].floor("D"),
                           fc=fc[i], reg=reg[i],
                           z1=ret1.iloc[i] / sd30.iloc[i] if sd30.iloc[i] > 0 else np.nan, r60=r60.iloc[i])
                for h in H:
                    if i + h < n:
                        row[f"u{h}"] = -(c[i + h] / c[i] - 1 - d[h][0])
                        row[f"s{h}"] = row[f"u{h}"] / d[h][1]
                    else:
                        row[f"u{h}"] = np.nan; row[f"s{h}"] = np.nan
                rows.append(row)
    A = pd.DataFrame(rows)

    def ct(sub, col):
        sub = sub.dropna(subset=[col])
        if len(sub) < 5:
            return pd.Series(dict(n=len(sub), mean=np.nan, t=np.nan, days=0))
        g = sub.groupby("day")[col].apply(lambda x: (x - sub[col].mean()).sum())
        G = len(g)
        se = np.sqrt((g ** 2).sum() * G / (G - 1)) / len(sub)
        return pd.Series(dict(n=len(sub), mean=sub[col].mean(), t=sub[col].mean() / se, days=G))

    out = {}
    # 1-day grid: every profile day, rises only (short bets)
    S = A[A.fc <= -2].copy()
    out["short_days_h1_h2"] = pd.DataFrame({"h1": ct(S, "u1"), "h2": ct(S[S.i % 2 == 0], "u2"),
                                            "h1_strength": ct(S, "s1")}).T
    R = A[A.z1 > 0].copy()
    R["z1b"] = pd.cut(R.z1, [0, 0.5, 1, 1.5, 2, np.inf])
    out["rise_days_h1_by_z1"] = R.groupby("z1b").apply(lambda s: ct(s, "u1"))
    out["all_profile_days_h1_by_z1"] = A.assign(z1b=pd.cut(A.z1, [-np.inf, -1, 0, 0.5, 1, 2, np.inf])).groupby("z1b").apply(lambda s: ct(s, "u1"))
    S["r60q"] = pd.qcut(S.r60.rank(method="first"), 4, labels=["deepest", "q2", "q3", "shallow"])
    out["short_h1_by_fall"] = S.groupby("r60q").apply(lambda s: ct(s, "u1"))
    out["short_h1_by_window"] = S.groupby("win").apply(lambda s: ct(s, "u1"))
    out["short_h1_by_year"] = S.groupby("year").apply(lambda s: ct(s, "u1"))
    out["short_h1_by_coin"] = S.groupby("coin").apply(lambda s: ct(s, "u1"))
    out["spearman_rise_z1_u1"] = pd.Series(dict(n=len(R.dropna(subset=["u1"])),
        r=stats.spearmanr(R.z1, R.u1, nan_policy="omit")[0],
        r_fall=stats.spearmanr(-S.r60, S.u1, nan_policy="omit")[0]))
    return out
