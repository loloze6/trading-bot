def explore(data):
    import numpy as np, pandas as pd
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        g_sum = 0; fee_sum = 0; n = 0; turn = 0; mkt = []; pos_all = []
        corr_rsi = []; agree = []; fc_std_mean = []
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"]; a = b["postRebalance_current_allocation"].fillna(0)
            r = c.shift(-1) / c - 1
            gross = (a * r).dropna()
            fee = (b["total_portfolio_value"] - b["postRebalance_total_value"]) / b["total_portfolio_value"]
            g_sum += gross.sum(); fee_sum += fee.fillna(0).sum(); n += len(gross)
            turn += (a - b["previous_allocation"].fillna(0)).abs().sum()
            # recompute RSI 336 wilder
            d = c.diff(); up = d.clip(lower=0); dn = (-d).clip(lower=0)
            au = up.ewm(alpha=1/336, adjust=False).mean(); ad = dn.ewm(alpha=1/336, adjust=False).mean()
            rsi = 100 - 100 / (1 + au / ad)
            raw = b["debug_info.components.rsi_mid.last_history_value"]
            ok = raw.notna() & rsi.notna()
            if ok.sum() > 50:
                corr_rsi.append(np.corrcoef(rsi[ok] - 50, b.loc[ok, "forecast"])[0, 1])
                agree.append((np.sign(rsi[ok] - 50) == np.sign(b.loc[ok, "forecast"])).mean())
                corr_raw = np.corrcoef(raw[ok], 50 - rsi[ok])[0, 1]
                fc_std_mean.append(corr_raw)
            pos_all.append(a.mean())
        rows.append(dict(coin=coin, gross_per_bar=g_sum / n, fee_per_bar=fee_sum / n,
                         turnover_per_bar=turn / n, mean_pos=np.mean(pos_all),
                         corr_fc_rsi50=np.mean(corr_rsi), sign_agree=np.mean(agree),
                         corr_raw_vs_50mRSI=np.mean(fc_std_mean)))
    out["per coin"] = pd.DataFrame(rows)
    # daily book vs coin, by window
    dr = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            dr.append(dict(coin=coin, w=w, book=d["book_return"].mean(), coin_ret=d["coin_return"].mean()))
    D = pd.DataFrame(dr)
    out["by window mean daily"] = D.groupby("w")[["book", "coin_ret"]].mean()
    # forecast autocorrelation / persistence
    pers = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            f = b["forecast"]
            pers.append(dict(coin=coin, flips_per_day=(np.sign(f).diff().abs() > 0).sum() / len(f) * 24,
                             ac24=f.autocorr(24), mean_abs_fc=f.abs().mean()))
    out["forecast persistence"] = pd.DataFrame(pers).groupby("coin").mean()
    return out
