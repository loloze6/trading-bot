import numpy as np
import pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]; days = data["days"]; trades = data["trades"]
    out = {}
    # --- book daily returns: mean over coins per day, inside windows
    rows = []
    for c in days:
        for w, d in days[c].items():
            dd = d[["day", "book_return", "coin_return"]].copy()
            dd["coin"] = c; dd["w"] = w
            rows.append(dd)
    D = pd.concat(rows)
    D["wn"] = D["w"].str[1:].astype(int)
    daily = D.groupby(["wn", "day"])[["book_return", "coin_return"]].mean().dropna().reset_index().sort_values(["wn", "day"])
    daily["year"] = pd.to_datetime(daily["day"]).dt.year
    # per window summary
    pw = daily.groupby("wn").agg(n=("book_return", "size"), book_mean=("book_return", "mean"),
                                 coin_mean=("coin_return", "mean"),
                                 book_sum=("book_return", lambda x: np.log1p(x).sum()),
                                 coin_sum=("coin_return", lambda x: np.log1p(x).sum()))
    out["per_window"] = pw
    # chain and drawdown
    eq = (1 + daily["book_return"]).cumprod().values
    peak = np.maximum.accumulate(eq); dd = eq / peak - 1
    i = dd.argmin(); j = eq[:i + 1].argmax()
    out["deepest_fall"] = f"dd={dd[i]:.3f}, from window w{daily['wn'].iloc[j]} to w{daily['wn'].iloc[i]}, {i-j} days"
    daily["dd"] = dd
    out["dd_by_window_min"] = daily.groupby("wn")["dd"].min()
    # --- per bar: position, gain, split long/short, trend state
    rb = []
    for c in bars:
        for w, b in bars[c].items():
            b = b.copy()
            cl = b["close"]
            b["r1"] = cl.shift(-1) / cl - 1
            b["pos"] = b["postRebalance_current_allocation"]
            b["gain"] = b["pos"] * b["r1"]
            hi = cl.rolling(30).max(); lo = cl.rolling(30).min()
            b["rpos"] = (cl - (hi + lo) / 2) / ((hi - lo) / 2)
            b["width"] = (hi - lo) / ((hi + lo) / 2)
            b["ret30"] = cl / cl.shift(30) - 1
            b["fwd10"] = cl.shift(-10) / cl - 1
            b["i"] = np.arange(len(b))
            b["coin"] = c; b["wn"] = int(w[1:])
            b["fee"] = (b["total_portfolio_value"] - b["postRebalance_total_value"]) / b["total_portfolio_value"]
            rb.append(b[["coin", "wn", "i", "pos", "gain", "r1", "rpos", "width", "ret30", "fwd10", "fee", "forecast"]])
    B = pd.concat(rb)
    B["side"] = np.sign(B["pos"])
    out["by_side"] = B.groupby("side").agg(bars=("gain", "size"), mean_gain=("gain", "mean"),
                                           mean_r1=("r1", "mean"), mean_abs_pos=("pos", lambda x: x.abs().mean()),
                                           fee_mean=("fee", "mean"))
    out["fee_total_per_bar"] = float(B["fee"].mean())
    out["gain_per_bar_before_fee"] = float(B["gain"].mean())
    # grid samples
    G = B[(B["i"] % 10 == 0)].dropna(subset=["fwd10", "forecast"])
    mu = G["fwd10"].mean()
    G = G.copy(); G["ex"] = G["fwd10"] - G.groupby("coin")["fwd10"].transform("mean")
    G["fq"] = pd.qcut(G["forecast"].rank(method="first"), 5, labels=False)
    out["fwd10_by_forecast_quintile"] = G.groupby("fq").agg(n=("ex", "size"), fc=("forecast", "mean"),
                                                            ex=("ex", "mean"), t=("ex", lambda x: x.mean() / x.std() * np.sqrt(len(x))))
    G2 = G.dropna(subset=["width", "ret30"]).copy()
    G2["sgn_ex"] = np.sign(G2["forecast"]) * G2["ex"]
    G2["trend"] = pd.qcut(G2["ret30"].abs(), 3, labels=["flat", "mid", "trend"])
    G2["wid"] = pd.qcut(G2["width"], 3, labels=["narrow", "mid", "wide"])
    f = lambda x: pd.Series({"n": len(x), "signed_ex": x["sgn_ex"].mean(),
                             "t": x["sgn_ex"].mean() / x["sgn_ex"].std() * np.sqrt(len(x)),
                             "corr": x[["forecast", "ex"]].corr().iloc[0, 1]})
    out["signed_move_by_abs_ret30"] = G2.groupby("trend").apply(f)
    out["signed_move_by_width"] = G2.groupby("wid").apply(f)
    G2["dir30"] = np.sign(G2["ret30"])
    G2["agree"] = np.sign(G2["forecast"]) == G2["dir30"]
    out["signed_move_by_fc_side_x_ret30_side"] = G2.groupby([np.sign(G2["forecast"]), "dir30"]).apply(f)
    # book by coin
    out["book_by_coin"] = D.groupby("coin")[["book_return", "coin_return"]].mean()
    # trades
    T = pd.concat([t.assign(coin=c) for c in trades for t in trades[c].values()])
    out["trades"] = T.groupby("side").agg(n=("side", "size"), gross=("profit_loss_percent", "mean"),
                                          net=("net_profit_loss_percent", "mean"),
                                          dur_days=("duration_minutes", lambda x: x.mean() / 1440))
    return out
