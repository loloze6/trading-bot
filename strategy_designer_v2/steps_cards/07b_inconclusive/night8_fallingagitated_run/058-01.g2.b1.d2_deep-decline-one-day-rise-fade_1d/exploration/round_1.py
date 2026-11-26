import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]
    H = [1, 3, 5, 10]
    rows = []
    drift = {}
    for coin, wins in bars.items():
        # coin drift per horizon over all visible windows, non-overlapping
        d = {}
        for h in H:
            rr = []
            for w, df in wins.items():
                c = df["close"].values
                for i in range(0, len(c) - h, h):
                    rr.append(c[i + h] / c[i] - 1)
            d[h] = (np.mean(rr), np.std(rr, ddof=1))
        drift[coin] = d
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            n = len(c)
            ret1 = pd.Series(c).pct_change()
            sd30 = ret1.rolling(30, min_periods=20).std()
            r3 = pd.Series(c).pct_change(3)
            r60 = pd.Series(c).pct_change(60)
            reg = df["regime"].astype(str).values
            fc = df["forecast"].values
            ts = pd.to_datetime(df["timestamp"])
            for i in range(n):
                inprof = reg[i] in ("trending", "unknown")
                if not inprof:
                    continue
                row = dict(coin=coin, win=w, i=i, grid3=(i % 3 == 0), year=ts.iloc[i].year,
                           day=ts.iloc[i].floor("D"), fc=fc[i], reg=reg[i],
                           z1=ret1.iloc[i] / sd30.iloc[i] if sd30.iloc[i] > 0 else np.nan,
                           z3=r3.iloc[i] / (sd30.iloc[i] * np.sqrt(3)) if sd30.iloc[i] > 0 else np.nan,
                           r60=r60.iloc[i])
                for h in H:
                    if i + h < n:
                        tr = c[i + h] / c[i] - 1
                        row[f"u{h}"] = -(tr - d[h][0])  # short direction
                        row[f"s{h}"] = row[f"u{h}"] / d[h][1]
                    else:
                        row[f"u{h}"] = np.nan
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

    # first short bet in each 3-bar grid cell
    S = A[A.fc <= -2].copy()
    S["cell"] = S.i // 3
    cases = S.sort_values("i").groupby(["coin", "win", "cell"]).head(1)
    out = {}
    out["cases_by_horizon"] = pd.DataFrame({f"h{h}": ct(cases, f"u{h}") for h in H}).T
    out["by_coin_u3"] = cases.groupby("coin").apply(lambda s: ct(s, "u3"))
    out["by_window_u3"] = cases.groupby("win").apply(lambda s: ct(s, "u3"))
    out["by_year_u3"] = cases.groupby("year").apply(lambda s: ct(s, "u3"))
    cases["fcq"] = pd.qcut(cases.fc.rank(method="first"), 4, labels=["strong", "q2", "q3", "weak"])
    out["by_forecast_quartile"] = cases.groupby("fcq").apply(lambda s: pd.concat([ct(s, "u3"), ct(s, "u5").add_prefix("h5_")]))
    cases["z1q"] = pd.qcut(cases.z1.rank(method="first"), 4, labels=["z1_low", "q2", "q3", "z1_high"])
    out["by_rise_quartile"] = cases.groupby("z1q").apply(lambda s: pd.concat([ct(s, "u3"), ct(s, "u5").add_prefix("h5_")]))
    cases["r60q"] = pd.qcut(cases.r60.rank(method="first"), 4, labels=["deepest", "q2", "q3", "shallow"])
    out["by_fall_quartile"] = cases.groupby("r60q").apply(lambda s: pd.concat([ct(s, "u3"), ct(s, "u5").add_prefix("h5_")]))
    # multi-day rise: all profile days on 3-day grid, graded by z3
    P = A[A.grid3].dropna(subset=["z3"]).copy()
    P["z3b"] = pd.cut(P.z3, [-np.inf, -1, 0, 0.5, 1, 1.5, np.inf])
    out["profile_grid_by_3day_rise_z"] = P.groupby("z3b").apply(lambda s: pd.concat([ct(s, "u3"), ct(s, "u5").add_prefix("h5_")]))
    P["z1b"] = pd.cut(P.z1, [-np.inf, -1, 0, 0.5, 1, 2, np.inf])
    out["profile_grid_by_1day_rise_z"] = P.groupby("z1b").apply(lambda s: pd.concat([ct(s, "u3"), ct(s, "u5").add_prefix("h5_")]))
    pos = P[P.z3 > 0]
    out["corr_z3_u3_u5"] = pd.Series(dict(n=len(pos), r_u3=stats.spearmanr(pos.z3, pos.u3, nan_policy="omit")[0],
                                          r_u5=stats.spearmanr(pos.z3, pos.u5, nan_policy="omit")[0]))
    out["corr_case_fc_u"] = pd.Series({f"h{h}": stats.spearmanr(-cases.fc, cases[f"u{h}"], nan_policy="omit")[0] for h in H})
    out["profile_days_all_u3"] = ct(P, "u3")
    return out
