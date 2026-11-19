def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []; grid = []
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            pos = b.postRebalance_current_allocation
            prev = b.previous_allocation
            fee = (b.total_portfolio_value - b.postRebalance_total_value) / b.total_portfolio_value
            chg = (pos - prev).abs()
            entry = (prev == 0) & (pos != 0)
            exitf = (prev != 0) & (pos == 0)
            resize = (prev != 0) & (pos != 0) & (chg > 0)
            r = b.close.shift(-1) / b.close - 1
            lr = np.log(b.close).diff()
            volr = lr.rolling(72).std() / lr.rolling(720).std()
            rows.append(pd.DataFrame({"coin": c, "fee": fee, "chg": chg, "entry": entry, "exit": exitf,
                                      "resize": resize, "gross": pos * r, "volr": volr, "pos": pos,
                                      "f": b.forecast}))
            n = len(b); idx = np.arange(0, n, 72)
            fwd = b.close.shift(-72) / b.close - 1
            ret720 = b.close / b.close.shift(720) - 1
            ret72 = b.close / b.close.shift(72) - 1
            grid.append(pd.DataFrame({"coin": c, "f": b.forecast.values[idx], "fwd": fwd.values[idx],
                                      "volr": volr.values[idx], "ret720": ret720.values[idx],
                                      "ret72": ret72.values[idx]}))
    R = pd.concat(rows)
    tot = len(R)
    out["trading_per_bar"] = pd.DataFrame({
        "fee_per_bar": [R.fee.mean()], "fee_per_day_x24": [R.fee.mean() * 24],
        "gross_per_day_x24": [R.gross.mean() * 24],
        "share_bars_traded": [(R.chg > 0).mean()], "entries_per_day": [R.entry.mean() * 24],
        "exits_per_day": [R.exit.mean() * 24], "resizes_per_day": [R.resize.mean() * 24],
        "fee_share_from_resize": [R.fee[R.resize].sum() / R.fee.sum()],
        "fee_share_from_entry_exit": [R.fee[R.entry | R.exit].sum() / R.fee.sum()],
        "mean_abs_pos_active": [R.pos[R.pos != 0].abs().mean()]})
    # forecast distribution when active
    act = R[R.f < 0]
    out["forecast_active_dist"] = act.f.describe()
    # active run length (bars short consecutively)
    # bar-level gross by vol ratio among short bars
    S = R[R.pos < 0].dropna(subset=["volr"]).copy()
    S["vq"] = pd.qcut(S.volr, 4, labels=False)
    out["short_bars_by_volr"] = S.groupby("vq").agg(volr=("volr", "mean"), gross_x24=("gross", lambda s: s.mean() * 24),
                                                     fee_x24=("fee", lambda s: s.mean() * 24), n=("gross", "size"))
    X = pd.concat(grid).dropna(subset=["fwd"])
    X["ex"] = X.fwd - X.groupby("coin").fwd.transform("mean")
    A = X[X.f < 0].dropna(subset=["volr"]).copy()
    A["calm"] = (A.volr < A.volr.median()).astype(int)
    out["calm_x_grind"] = A.groupby(["calm", pd.qcut(A.f.rank(method="first"), 2, labels=False)]).ex.agg(["mean", "size"])
    A["vq"] = pd.qcut(A.volr, 4, labels=False)
    out["calm_by_coin"] = A.groupby(["coin", "calm"]).ex.mean().unstack()
    # graded: correlation of volr with excess among active
    out["corr_volr_ex"] = pd.DataFrame({"spearman": [stats.spearmanr(A.volr, A.ex).correlation],
                                        "n": [len(A)],
                                        "slope_t": [stats.linregress(A.volr, A.ex).rvalue * np.sqrt(len(A) - 2) /
                                                    np.sqrt(1 - stats.linregress(A.volr, A.ex).rvalue ** 2)]})
    # same in flat-forecast bars (all grid): does calm predict excess regardless of fall?
    F = X.dropna(subset=["volr"]).copy()
    F["down"] = (F.ret72 < 0).astype(int)
    F["vq"] = F.groupby("down").volr.transform(lambda s: pd.qcut(s, 4, labels=False))
    out["all_by_down_volr"] = F.groupby(["down", "vq"]).ex.agg(["mean", "size"])
    return out
