import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    out = {}
    # book daily returns
    rows = []
    for c, ws in data["days"].items():
        for w, d in ws.items():
            t = d[["day", "book_return", "coin_return"]].copy()
            t["coin"] = c; t["w"] = w
            rows.append(t)
    D = pd.concat(rows)
    D["day"] = pd.to_datetime(D["day"])
    book = D.groupby(["w", "day"]).agg(br=("book_return", "mean"), cr=("coin_return", "mean")).reset_index().dropna()
    book = book.sort_values(["w", "day"])
    res = []
    for w, g in book.groupby("w"):
        eq = (1 + g.br).cumprod()
        dd = (eq / eq.cummax() - 1).min()
        ceq = (1 + g.cr).cumprod()
        res.append({"w": w, "n": len(g), "book_tot": eq.iloc[-1] - 1, "book_maxdd": dd,
                    "coin_tot": ceq.iloc[-1] - 1, "coin_maxdd": (ceq / ceq.cummax() - 1).min(),
                    "sharpe": g.br.mean() / g.br.std() * np.sqrt(365)})
    R = pd.DataFrame(res)
    R["wn"] = R.w.str[1:].astype(int)
    out["per_window"] = R.sort_values("wn").drop(columns="wn").round(4)
    allb = book.sort_values("day")
    eq = (1 + allb.br).cumprod()
    out["overall_maxdd"] = float((eq / eq.cummax() - 1).min())

    # bar-level conditions
    B = []
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.copy()
            b["r"] = b.close.pct_change()
            b["fwd"] = b.close.shift(-1) / b.close - 1
            b["r20"] = b.close / b.close.shift(20) - 1
            b["r5"] = b.close.shift(1) / b.close.shift(6) - 1
            b["sma50"] = b.close / b.close.rolling(50).mean() - 1
            b["vol20"] = b.r.abs().rolling(20).mean()
            b["prevf"] = b.forecast.shift(1)
            b["coin"] = c; b["w"] = w
            B.append(b[["coin", "w", "r", "fwd", "r20", "r5", "sma50", "vol20", "forecast", "prevf"]])
    B = pd.concat(B)
    B["vrel"] = B.vol20 / B.groupby("coin").vol20.transform("median")
    cm = B.groupby("coin").fwd.mean()
    B["ex"] = B.fwd - B.coin.map(cm)
    A = B[(B.forecast > 0) & B.fwd.notna()].copy()
    A["wex"] = A.ex * A.forecast / 20  # position-weighted contribution
    def summ(g):
        return pd.Series({"n": len(g), "hit": (g.fwd > 0).mean(), "mean_ex": g.ex.mean(),
                          "t": g.ex.mean() / g.ex.std() * np.sqrt(len(g)) if len(g) > 2 else np.nan,
                          "wcontrib_sum": g.wex.sum(), "loss_q10": g.fwd.quantile(0.1)})
    A["fbin"] = pd.cut(A.forecast, [0, 5, 12, 16, 20.01])
    out["by_forecast"] = A.groupby("fbin").apply(summ).round(4)
    out["by_r20_sign"] = A.groupby(np.sign(A.r20)).apply(summ).round(4)
    out["by_sma50"] = A.groupby(pd.cut(A.sma50, [-9, -0.2, -0.1, 0, 0.1, 9])).apply(summ).round(4)
    out["by_r5"] = A.groupby(pd.cut(A.r5, [-9, -0.1, -0.03, 0, 0.03, 9])).apply(summ).round(4)
    out["by_prev_drop"] = A.groupby(A.prevf > 5).apply(summ).round(4)
    out["by_vrel"] = A.groupby(pd.cut(A.vrel, [0, 0.7, 1, 1.4, 2, 99])).apply(summ).round(4)
    out["by_coin"] = A.groupby("coin").apply(summ).round(4)
    # worst book days: what was held
    worst = book.nsmallest(30, "br")
    m = D.merge(worst[["w", "day"]], on=["w", "day"])
    out["worst30_book_day_mean"] = float(worst.br.mean())
    out["worst30_coin_mean"] = float(worst.cr.mean())
    out["worst30_share_book_neg_coins"] = float((m.book_return < 0).mean())
    return out
