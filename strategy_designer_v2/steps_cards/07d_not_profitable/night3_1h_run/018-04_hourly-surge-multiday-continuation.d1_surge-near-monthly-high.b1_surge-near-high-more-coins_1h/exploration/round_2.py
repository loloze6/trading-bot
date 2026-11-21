def explore(data):
    import numpy as np, pandas as pd
    out = {}
    # book daily series to locate deepest falls
    rows = []
    for c, ws in data["days"].items():
        for w, d in ws.items():
            dd = d[["day", "book_return"]].copy(); dd["coin"] = c; dd["wn"] = int(w[1:]); rows.append(dd)
    D = pd.concat(rows)
    B = D.groupby(["wn", "day"])["book_return"].mean().reset_index().sort_values(["wn", "day"]).dropna().reset_index(drop=True)
    eq = (1 + B["book_return"]).cumprod(); dd = eq / eq.cummax() - 1
    # mark days inside the 4 deepest fall-to-trough stretches
    fall_days = set()
    inside = False; eps = []
    for i in range(len(B)):
        if dd.iat[i] < 0 and not inside: inside = True; s = i
        if inside and (dd.iat[i] == 0 or i == len(B) - 1):
            seg = dd.iloc[s:i + 1]; j = seg.idxmin(); eps.append((seg.min(), s, j)); inside = False
    eps = sorted(eps)[:4]
    for _, s, j in eps:
        for k in range(s, j + 1): fall_days.add((B["wn"].iat[k], B["day"].iat[k]))
    # per bar states
    P = []
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            cl = b["close"]; a = b["postRebalance_current_allocation"].fillna(0)
            g = a * (cl.shift(-1) / cl - 1)
            r720 = cl / cl.shift(720) - 1
            ma2160 = cl.rolling(2160, min_periods=720).mean()
            ma720 = cl.rolling(720, min_periods=360).mean()
            r168 = cl / cl.shift(168) - 1
            dist = cl / cl.rolling(720, min_periods=200).max() - 1
            # age of position: bars since allocation turned from 0 to >0
            on = (a.abs() > 1e-9).astype(int)
            grp = (on.diff().fillna(on) == 1).cumsum()
            age = on.groupby(grp).cumsum()
            day = pd.to_datetime(b["timestamp"]).dt.strftime("%Y-%m-%d")
            df = pd.DataFrame(dict(g=g, a=a, r720=r720, vs2160=cl / ma2160 - 1, ma_slope=ma720 / ma720.shift(168) - 1,
                                   r168=r168, dist=dist, age=age, coin=c, wn=int(w[1:]), day=day))
            P.append(df[df["a"].abs() > 1e-9].dropna(subset=["g"]))
    P = pd.concat(P)
    try:
        P["fall"] = [(x, y) in fall_days for x, y in zip(P["wn"], P["day"].astype(type(B["day"].iat[0])) )]
    except Exception:
        P["fall"] = False
    out["fall_flag_share"] = pd.Series(dict(share_bars_in_falls=P["fall"].mean(), n=len(P)))
    def tab(f, bins=None):
        x = P.dropna(subset=[f])
        q = pd.qcut(x[f], 5, duplicates="drop") if bins is None else pd.cut(x[f], bins)
        gg = x.groupby(q, observed=True).agg(bars=("g", "size"), mean_alloc=("a", "mean"), sum_gain=("g", "sum"),
                                              gain_per_bar_bps=("g", lambda s: s.mean() * 1e4),
                                              fall_sum=("g", lambda s: s[x.loc[s.index, "fall"]].sum() if x["fall"].any() else np.nan),
                                              other_sum=("g", lambda s: s[~x.loc[s.index, "fall"]].sum()))
        gg.index = [str(i) for i in gg.index]
        return gg
    for f in ["r720", "vs2160", "ma_slope", "dist", "r168"]:
        out["gain_by_" + f] = tab(f)
    out["gain_by_age_h"] = tab("age", [0, 24, 120, 240, 480, 1000, 100000])
    # sign split on ma_slope and vs2160
    for f in ["ma_slope", "vs2160", "r720"]:
        x = P.dropna(subset=[f])
        out["sign_" + f] = x.groupby(x[f] > 0).agg(bars=("g", "size"), sum_gain=("g", "sum"),
                                                     bps=("g", lambda s: s.mean() * 1e4),
                                                     t=("g", lambda s: s.mean() / s.std() * np.sqrt(len(s))))
    return out
