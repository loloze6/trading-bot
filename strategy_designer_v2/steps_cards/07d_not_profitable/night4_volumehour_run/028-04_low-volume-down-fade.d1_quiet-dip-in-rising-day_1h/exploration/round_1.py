def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    trows = []
    drift = {}
    for coin, wins in data["bars"].items():
        # drift per horizon over all windows
        for h in [3, 6, 12, 24, 48]:
            rs = []
            for w, b in wins.items():
                c = b["close"].values
                idx = np.arange(0, len(c) - h, h)
                rs.append(c[idx + h] / c[idx] - 1)
            rs = np.concatenate(rs)
            drift[(coin, h)] = (rs.mean(), rs.std())
        for w, b in wins.items():
            c = b["close"].values
            f = b["forecast"].fillna(0).values
            v = b["volume"].values
            n = len(c)
            ts = pd.to_datetime(b["timestamp"])
            hr = ts.dt.hour.values
            yr = ts.dt.year.values
            r1 = np.r_[np.nan, c[1:] / c[:-1] - 1]
            r24 = pd.Series(c).pct_change(24).values
            mabs = pd.Series(np.abs(r1)).rolling(720, min_periods=200).mean().shift(1).values
            vol30 = pd.Series(r1).rolling(720, min_periods=200).std().values
            vol7 = pd.Series(r1).rolling(168, min_periods=50).std().values
            r7d = pd.Series(c).pct_change(168).values
            # cases: first bar of 6-grid with forecast rise >=2 from min since last bet
            last_min = 0.0
            cell_done = -1
            for i in range(n):
                fi = f[i]
                if fi <= 0:
                    last_min = 0.0
                    continue
                if fi - last_min >= 2:
                    cell = i // 6
                    if cell != cell_done and i + 48 < n:
                        cell_done = cell
                        rec = dict(coin=coin, w=w, f=fi, hour=hr[i], year=yr[i],
                                   fall=-r1[i] / mabs[i] if mabs[i] else np.nan,
                                   rise24=r24[i - 1] if i > 0 else np.nan,
                                   volratio=vol7[i] / vol30[i] if vol30[i] else np.nan,
                                   r7d=r7d[i])
                        for h in [3, 6, 12, 24, 48]:
                            rec[f"t{h}"] = c[i + h] / c[i] - 1
                            rec[f"u{h}"] = rec[f"t{h}"] - drift[(coin, h)][0]
                        rows.append(rec)
                    last_min = fi
                else:
                    last_min = min(last_min, fi)
        for w, t in data["trades"][coin].items():
            if len(t):
                trows.append(t.assign(coin=coin, w=w))
    df = pd.DataFrame(rows)
    out["n_cases"] = len(df)
    hz = []
    for h in [3, 6, 12, 24, 48]:
        x = df[f"u{h}"]; tt = df[f"t{h}"]
        hz.append(dict(h=h, total_mean=tt.mean(), unusual_mean=x.mean(),
                       t=x.mean() / (x.std() / np.sqrt(len(x))), usual_move=np.mean([drift[(c, h)][1] for c in data["bars"]])))
    out["by_horizon"] = pd.DataFrame(hz)
    def grp(col, q=5):
        g = pd.qcut(df[col], q, duplicates="drop")
        return df.groupby(g).agg(n=("t6", "size"), mean_x=(col, "mean"), t6=("t6", "mean"), u6=("u6", "mean"), t24=("t24", "mean"), u24=("u24", "mean"))
    out["by_forecast_q"] = grp("f")
    out["by_fall_q"] = grp("fall")
    out["by_rise24_q"] = grp("rise24")
    out["by_volratio7_30_q"] = grp("volratio")
    out["by_r7d_q"] = grp("r7d")
    out["by_coin"] = df.groupby("coin")[["t6", "u6", "t24", "u24"]].mean()
    out["by_year"] = df.groupby("year").agg(n=("t6", "size"), t6=("t6", "mean"), u6=("u6", "mean"))
    tr = pd.concat(trows)
    tr["dur_h"] = tr["duration_minutes"] / 60
    out["trades"] = pd.DataFrame(dict(n=[len(tr)], gross_mean=[tr["profit_loss_percent"].mean()],
                                      net_mean=[tr["net_profit_loss_percent"].mean()],
                                      dur_h_mean=[tr["dur_h"].mean()], dur_h_med=[tr["dur_h"].median()],
                                      win_gross=[(tr["profit_loss_percent"] > 0).mean()]))
    tr["dq"] = pd.qcut(tr["dur_h"], 4, duplicates="drop")
    out["trades_by_dur"] = tr.groupby("dq").agg(n=("dur_h", "size"), gross=("profit_loss_percent", "mean"), net=("net_profit_loss_percent", "mean"))
    # book daily
    bd = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            bd.append(d.assign(coin=coin, w=w))
    bd = pd.concat(bd)
    out["book_by_window_mean_daily"] = bd.groupby("w")["book_return"].mean().describe()
    return out
