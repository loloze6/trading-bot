def explore(data):
    import numpy as np, pandas as pd
    out = {}
    # 1) trades: why they end, and what the coin did over the rest of the 10 days after an early exit
    rows = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            if not len(t): continue
            b = data["bars"][coin][w].reset_index(drop=True)
            ts = pd.to_datetime(b["timestamp"])
            c = b["close"].values
            r60 = pd.Series(c).pct_change(60).values
            r30 = b.get("debug_info.components.month_fall.last_history_value", pd.Series([np.nan]*len(b))).values
            for _, tr in t.iterrows():
                et = pd.to_datetime(tr["entry_time"]); xt = pd.to_datetime(tr["exit_time"])
                ie = ts.searchsorted(et); ix = ts.searchsorted(xt)
                if ie >= len(b): continue
                ix = min(ix, len(b)-1)
                d = tr["duration_minutes"]/1440
                regx = b["regime"].iloc[ix]
                why = "window_end" if ix >= len(b)-1 else ("profile_exit" if regx != "unknown" else "forecast_0")
                r60x = r60[ix]
                side_exit = np.nan if np.isnan(r60x) else (1 if r60x > 0.1 else (-1 if r60x < -0.1 else 0))
                # short-direction return from exit to entry+10 bars and entry+20 bars
                rest10 = -(c[ie+10]/c[ix]-1) if (ie+10 < len(b) and ix < ie+10) else np.nan
                full10 = -(c[ie+10]/c[ie]-1) if ie+10 < len(b) else np.nan
                full20 = -(c[ie+20]/c[ie]-1) if ie+20 < len(b) else np.nan
                rows.append(dict(why=why, exit60=side_exit, d=d, pl=tr["net_profit_loss_percent"],
                                 r30e=r30[ie], rest10=rest10, full10=full10, full20=full20))
    T = pd.DataFrame(rows)
    T["exitkind"] = T["why"] + "_" + T["exit60"].astype(str)
    out["trades_by_exit"] = T.groupby("exitkind").agg(n=("pl","size"), days=("d","mean"), pl=("pl","mean"),
                                                     rest10=("rest10","mean"), full10=("full10","mean"), full20=("full20","mean"))
    T["r30b"] = pd.cut(T["r30e"], [-100,-20,-10,-5,0,100])
    out["trades_by_entry_r30"] = T.groupby("r30b").agg(n=("pl","size"), pl=("pl","mean"),
                                                      full10=("full10","mean"), full20=("full20","mean"))
    # 2) grid cases in choppy, short forecast, by raw 30d fall; and same falls outside choppy (condition alone)
    g = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True); c = b["close"].values; n = len(b)
            r30 = pd.Series(c).pct_change(30).values*100
            r60 = pd.Series(c).pct_change(60).values
            for i in range(0, n-10, 10):
                g.append(dict(coin=coin, fwd=c[i+10]/c[i]-1, fwd20=(c[i+20]/c[i]-1) if i+20<n else np.nan,
                              r30=r30[i], r60=r60[i], reg=b["regime"].iloc[i], fc=b["forecast"].iloc[i]))
    G = pd.DataFrame(g)
    dr = G.groupby("coin")["fwd"].transform("mean")
    G["short_unus"] = -(G["fwd"] - dr)
    G["r30b"] = pd.cut(G["r30"], [-100,-20,-10,-5,0,100])
    G["prof"] = np.where(G["r60"]>0.1,"rising",np.where(G["r60"]<-0.1,"falling","choppy"))
    G.loc[G["r60"].isna(),"prof"] = "na"
    def s(x):
        return pd.Series(dict(n=len(x), short_unus=x["short_unus"].mean(),
                              t=x["short_unus"].mean()/(x["short_unus"].std()/np.sqrt(len(x))) if len(x)>2 else np.nan,
                              short_fwd20=-x["fwd20"].mean()))
    out["grid_by_profile_r30"] = G.groupby(["prof","r30b"]).apply(s)
    sh = G[(G["reg"]=="unknown") & (G["fc"]<0)].copy()
    sh["fcb"] = pd.cut(sh["fc"], [-21,-10,-5,-2,0])
    out["choppy_short_by_forecast"] = sh.groupby("fcb").apply(s)
    return out
