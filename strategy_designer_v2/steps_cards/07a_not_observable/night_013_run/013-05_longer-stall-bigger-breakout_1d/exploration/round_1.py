import pandas as pd, numpy as np

def explore(data):
    bars = data["bars"]
    rows = []
    grid = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            n = len(df)
            tr = (df["regime"] == "trending")
            yr = pd.to_datetime(df["timestamp"].iloc[0]).year
            col = "debug_info.components.stall.post_pipeline_value"
            rawc = "debug_info.components.stall.last_history_value"
            st = df[col] if col in df.columns else pd.Series(np.nan, index=df.index)
            raw = df[rawc] if rawc in df.columns else pd.Series(np.nan, index=df.index)
            # trending episodes
            starts = int((tr & ~tr.shift(1, fill_value=False)).sum())
            rows.append(dict(coin=coin, window=w, year=yr, n=n, trend=int(tr.sum()),
                             episodes=starts, active=int((df["forecast"] > 0).sum()),
                             raw_pos=int((raw > 0).sum())))
            c = df["close"].values
            for i in range(0, n, 30):
                full = i + 30 < n
                fr = c[i+30]/c[i]-1 if full else np.nan
                grid.append(dict(coin=coin, window=w, year=yr, trend=bool(tr.iloc[i]),
                                 full=full, fr=fr, st=st.iloc[i], raw=raw.iloc[i]))
    R = pd.DataFrame(rows); G = pd.DataFrame(grid)
    out = {}
    out["window length"] = R["n"].describe()
    out["per coin"] = R.groupby("coin")[["n","trend","episodes","active","raw_pos"]].sum()
    out["per year"] = R.groupby("year")[["n","trend","episodes","active"]].sum()
    out["trend share all bars"] = R["trend"].sum()/R["n"].sum()
    out["grid counts"] = pd.Series({"grid": len(G), "full": int(G.full.sum()),
        "trend": int(G.trend.sum()), "trend_full": int((G.trend & G.full).sum()),
        "trend_full_st": int((G.trend & G.full & G.st.notna()).sum())})
    gt = G[G.trend & G.full]
    out["trend grid fr"] = gt["fr"].describe()
    out["trend grid raw stall"] = gt["raw"].describe()
    out["all grid fr std"] = G.loc[G.full, "fr"].std()
    # episode lengths
    lens = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            tr = (df["regime"] == "trending").astype(int).values
            run = 0
            for v in list(tr)+[0]:
                if v: run += 1
                elif run: lens.append(run); run = 0
    out["trend episode length"] = pd.Series(lens).describe()
    return out
