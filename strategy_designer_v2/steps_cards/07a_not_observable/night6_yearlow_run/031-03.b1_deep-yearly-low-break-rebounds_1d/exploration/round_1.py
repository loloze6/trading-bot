def explore(data):
    import pandas as pd, numpy as np
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.copy()
            ts = pd.to_datetime(df["timestamp"])
            yr = ts.dt.year
            mr = df["regime"] == "mean_reversion"
            fc = df["forecast"].fillna(0)
            dep_col = "debug_info.components.depth.last_history_value"
            post_col = "debug_info.components.depth.post_pipeline_value"
            dep = df[dep_col] if dep_col in df.columns else pd.Series(np.nan, index=df.index)
            post = df[post_col] if post_col in df.columns else pd.Series(np.nan, index=df.index)
            # cases: forecast rise >= 2 on long side, first per 10-bar grid cell, with room for 10 bars
            n = len(df)
            rise = fc.diff().fillna(fc) >= 2
            pos = np.arange(n)
            cell = pos // 10
            ok = (pos + 10) < n
            case_idx = []
            seen = set()
            for i in range(n):
                if rise.iloc[i] and fc.iloc[i] > 0 and ok[i] and cell[i] not in seen:
                    seen.add(cell[i]); case_idx.append(i)
            for y in sorted(yr.unique()):
                m = (yr == y).values
                rows.append(dict(coin=coin, window=w, year=y, bars=int(m.sum()),
                                 mr_bars=int((mr & m).sum()),
                                 fc_pos=int(((fc > 0) & m).sum()),
                                 mr_fc_zero=int((mr & (fc == 0) & m).sum()),
                                 depth_recorded=int((dep.notna() & m).sum()),
                                 post_nan_in_mr=int((mr & post.isna() & m).sum()),
                                 cases=int(sum(1 for i in case_idx if m[i])),
                                 mr_episodes=int(((mr & ~mr.shift(1, fill_value=False)) & m).sum())))
    t = pd.DataFrame(rows)
    by_coin = t.groupby("coin")[["bars","mr_bars","mr_episodes","fc_pos","mr_fc_zero","post_nan_in_mr","cases"]].sum()
    by_year = t.groupby("year")[["bars","mr_bars","mr_episodes","fc_pos","mr_fc_zero","cases"]].sum()
    by_win = t.groupby("window")[["bars","mr_bars","mr_episodes","fc_pos","cases"]].sum()
    by_win = by_win[by_win["mr_bars"] > 0]
    # forecast and depth distribution in MR
    fcs, deps, posts = [], [], []
    for coin, wins in bars.items():
        for w, df in wins.items():
            mr = df["regime"] == "mean_reversion"
            fcs.append(df.loc[mr, "forecast"])
            c = "debug_info.components.depth.last_history_value"
            if c in df.columns: deps.append(df.loc[mr, c])
            c2 = "debug_info.components.depth.post_pipeline_value"
            if c2 in df.columns: posts.append(df.loc[mr, c2])
    fdesc = pd.concat(fcs).describe() if fcs else "none"
    ddesc = pd.concat(deps).describe() if deps else "none"
    pdesc = pd.concat(posts).describe() if posts else "none"
    wl = t.groupby(["coin","window"])["bars"].sum().describe()
    return {"by coin": by_coin, "by year": by_year, "by window (active)": by_win,
            "forecast in MR": fdesc, "depth raw in MR": ddesc, "depth post in MR": pdesc,
            "window length bars": wl}
