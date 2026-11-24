def explore(data):
    import pandas as pd, numpy as np
    bars = data["bars"]
    PP = "debug_info.components.break_depth.post_pipeline_value"
    LH = "debug_info.components.break_depth.last_history_value"
    rows = []; allf = []; alllh = []
    case_rows = []
    drift = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            c = df["close"].values
            for i in range(0, len(c) - 10, 10):
                rets.append(c[i + 10] / c[i] - 1)
        drift[coin] = (np.mean(rets) if rets else np.nan, np.std(rets, ddof=1) if len(rets) > 1 else np.nan)
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            mr = (df["regime"] == "mean_reversion")
            f = df["forecast"].fillna(0)
            yr = int(pd.to_datetime(df["timestamp"]).dt.year.iloc[0])
            ep = int((mr & ~mr.shift(1, fill_value=False)).sum())
            n = len(df)
            cells = n // 10
            cell_id = np.arange(n) // 10
            cells_mr = len(set(cell_id[mr.values]))
            cells_f2 = len(set(cell_id[(f >= 2).values]))
            # cases as step 5: forecast rise >= 2 from lowest since last bet (0 after flat)
            low = 0.0; last_cell = -1
            for i in range(n):
                fi = f.iloc[i]
                if fi <= 0:
                    low = 0.0; continue
                if fi - low >= 2 and cell_id[i] != last_cell:
                    last_cell = cell_id[i]
                    if i + 10 < n:
                        r = df["close"].iloc[i + 10] / df["close"].iloc[i] - 1
                        case_rows.append(dict(coin=coin, window=w, year=yr, f=fi,
                                              depth=df[LH].iloc[i] if LH in df else np.nan,
                                              unusual=r - drift[coin][0]))
                    else:
                        case_rows.append(dict(coin=coin, window=w, year=yr, f=fi, depth=np.nan, unusual=np.nan))
                    low = fi
                else:
                    low = min(low, fi)
            if mr.any():
                allf.append(f[mr])
                if LH in df: alllh.append(df.loc[mr, LH])
            rows.append(dict(coin=coin, window=w, year=yr, bars=n, cells=cells, mr_bars=int(mr.sum()),
                             episodes=ep, cells_mr=cells_mr, cells_f2=cells_f2,
                             f_ge2=int((f >= 2).sum()), f_max=float(f.max())))
    t = pd.DataFrame(rows)
    cols = ["bars", "cells", "mr_bars", "episodes", "cells_mr", "cells_f2", "f_ge2"]
    by_coin = t.groupby("coin")[cols].sum()
    by_year = t.groupby("year")[cols].sum()
    allf = pd.concat(allf); alllh = pd.concat(alllh) if alllh else pd.Series(dtype=float)
    fbins = pd.cut(allf, [-0.01, 0, 0.5, 1, 2, 5, 10, 20]).value_counts().sort_index()
    dist = pd.DataFrame({"forecast": allf.describe(), "raw_depth": alllh.describe()})
    cs = pd.DataFrame(case_rows)
    summ = {}
    if len(cs):
        u = cs["unusual"].dropna()
        summ = pd.Series({"cases_total": len(cs), "cases_with_10_ahead": len(u),
                          "mean_unusual": u.mean(), "sd_unusual": u.std(ddof=1),
                          "median_unusual": u.median(), "share_pos": (u > 0).mean(),
                          "n_needed_for_t2_at_this_mean_sd": (2 * u.std(ddof=1) / u.mean()) ** 2 if u.mean() != 0 else np.nan,
                          "mean_f_at_case": cs["f"].mean(), "mean_depth_at_case": cs["depth"].mean()})
        cby = cs.groupby("year")["unusual"].agg(["count", "mean"])
        cbc = cs.groupby("coin")["unusual"].agg(["count", "mean"])
    else:
        cby = cbc = "none"
    usual = pd.DataFrame(drift, index=["drift10", "usual10"]).T
    tot = pd.Series({"coin_windows": len(t), "total_bars": t.bars.sum(), "regime_bars": t.mr_bars.sum(),
                     "episodes": t.episodes.sum(), "cells": t.cells.sum(), "cells_with_regime": t.cells_mr.sum(),
                     "cells_with_f>=2": t.cells_f2.sum(), "share_regime_bars": t.mr_bars.sum() / t.bars.sum()})
    return {"totals": tot, "by_coin": by_coin, "by_year": by_year, "forecast_bins_regime": fbins,
            "dist_regime": dist, "cases_summary": summ, "cases_by_year": cby, "cases_by_coin": cbc,
            "usual_move": usual}
