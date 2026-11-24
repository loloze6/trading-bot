def explore(data):
    import pandas as pd, numpy as np
    rows = []
    case_rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            yr = pd.to_datetime(b["timestamp"]).dt.year
            mr = (b["regime"] == "mean_reversion")
            fpos = b["forecast"] > 0
            depth = b.get("debug_info.components.depth.last_history_value")
            # grid cells of 10 bars with a break
            cell = np.arange(len(b)) // 10
            cells_break = pd.Series(mr.values).groupby(cell).any().sum()
            cells_fpos = pd.Series(fpos.values).groupby(cell).any().sum()
            rows.append(dict(coin=coin, window=w, year=int(yr.iloc[0]), bars=len(b),
                             break_bars=int(mr.sum()), fpos_bars=int(fpos.sum()),
                             cells=int(cell.max()+1), cells_break=int(cells_break),
                             cells_fpos=int(cells_fpos)))
            # forward 10-bar return on break bars, first per cell
            fwd = b["close"].shift(-10) / b["close"] - 1
            d = pd.DataFrame({"cell": cell, "mr": mr, "fpos": fpos, "fwd": fwd,
                              "depth": depth if depth is not None else np.nan,
                              "fc": b["forecast"]})
            first = d[d.mr].groupby("cell").first()
            for _, r in first.iterrows():
                case_rows.append(dict(coin=coin, window=w, year=int(yr.iloc[0]),
                                      fwd=r.fwd, depth=r.depth, fc=r.fc, fpos=r.fpos))
    R = pd.DataFrame(rows); C = pd.DataFrame(case_rows)
    out = {}
    out["by coin"] = R.groupby("coin")[["bars","break_bars","fpos_bars","cells","cells_break","cells_fpos"]].sum()
    out["by year"] = R.groupby("year")[["bars","break_bars","fpos_bars","cells","cells_break","cells_fpos"]].sum()
    out["by window"] = R.groupby("window")[["bars","break_bars","fpos_bars","cells_break","cells_fpos"]].sum()
    out["totals"] = R[["bars","break_bars","fpos_bars","cells","cells_break","cells_fpos"]].sum()
    if len(C):
        out["break-cell cases: fwd stats"] = C["fwd"].describe()
        out["break-cell cases: forecast>0 share"] = float(C["fpos"].mean())
        out["break-cell cases: fc stats"] = C["fc"].describe()
        out["break-cell cases: depth stats"] = C["depth"].describe()
        Cc = C.dropna(subset=["fwd"])
        out["break-cell cases with fwd, by fpos"] = Cc.groupby("fpos")["fwd"].agg(["count","mean","std"])
    return out
