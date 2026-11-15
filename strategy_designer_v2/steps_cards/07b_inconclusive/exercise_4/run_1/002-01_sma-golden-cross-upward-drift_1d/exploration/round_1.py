def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    hs = [5, 10, 20, 40]
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            f = df["forecast"].fillna(0).values
            raw = df.get("debug_info.components.sma_cross.last_history_value")
            raw = raw.values if raw is not None else np.full(len(df), np.nan)
            ts = pd.to_datetime(df["timestamp"])
            # days since spread turned positive inside window
            pos = (raw > 0)
            since = np.full(len(df), np.nan); cnt = np.nan
            for i in range(len(df)):
                if i > 0 and pos[i] and not pos[i-1]:
                    cnt = 0
                elif pos[i] and not np.isnan(cnt):
                    cnt += 1
                elif not pos[i]:
                    cnt = np.nan
                since[i] = cnt
            r20 = pd.Series(c).pct_change(20).values
            for h in hs:
                for i in range(0, len(df) - h, h):
                    rows.append(dict(coin=coin, w=w, h=h, f=f[i], raw=raw[i],
                                     since=since[i], r20=r20[i],
                                     year=ts[i].year, ret=c[i+h]/c[i]-1))
    S = pd.DataFrame(rows)
    S["ex"] = S["ret"] - S.groupby(["coin", "h"])["ret"].transform("mean")
    def slope(d, x="f"):
        d = d.dropna(subset=[x, "ex"])
        if len(d) < 10 or d[x].std() == 0: return (np.nan, np.nan, len(d))
        r = stats.linregress(d[x], d["ex"]); return (r.slope, r.slope/r.stderr, len(d))
    out = {}
    out["by_h"] = pd.DataFrame({h: slope(S[S.h==h]) for h in hs}, index=["slope","t","n"]).T
    def onoff(d):
        a = d[d.f>0]["ex"]; b = d[d.f==0]["ex"]
        t = stats.ttest_ind(a, b, equal_var=False).statistic
        return pd.Series(dict(on=a.mean(), off=b.mean(), t=t, n_on=len(a), n_off=len(b)))
    out["onoff_by_h"] = pd.DataFrame({h: onoff(S[S.h==h]) for h in hs}).T
    S10 = S[S.h==10]
    out["by_coin_10"] = pd.DataFrame({c: list(slope(g)) + list(onoff(g)[["on","off","t"]]) for c, g in S10.groupby("coin")},
                                     index=["slope","t","n","on","off","t_onoff"]).T
    out["by_year_10"] = pd.DataFrame({y: list(slope(g)) + list(onoff(g)[["on","off","t"]]) for y, g in S10.groupby("year")},
                                     index=["slope","t","n","on","off","t_onoff"]).T
    on = S10[S10.f>0].copy()
    on["fb"] = pd.cut(on.f, [0,5,10,15,19.99,20.01])
    out["fbucket_10"] = on.groupby("fb")["ex"].agg(["mean","count",lambda x: x.mean()/(x.std()/np.sqrt(len(x)))])
    out["slope_on_only_10"] = str(slope(on))
    out["raw_slope_all_10"] = str(slope(S10, "raw"))
    # recency of cross
    rec = S[(S.raw>0)].copy()
    rec["sb"] = pd.cut(rec.since, [-1,20,60,120,1000])
    out["since_cross"] = rec.groupby(["h","sb"])["ex"].agg(["mean","count"]).unstack("h")
    rec["unk"] = rec.since.isna()
    out["since_unknown_share"] = rec.groupby("h")["unk"].mean()
    # momentum regime: 20d return sign
    S10m = S10.dropna(subset=["r20"]).copy()
    S10m["mom"] = np.where(S10m.r20>0, "up", "down")
    out["mom_x_on_10"] = S10m.groupby(["mom", S10m.f>0])["ex"].agg(["mean","count"])
    out["r20_slope_by_h"] = pd.DataFrame({h: slope(S[S.h==h], "r20") for h in hs}, index=["slope","t","n"]).T
    return out
