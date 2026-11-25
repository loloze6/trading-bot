def explore(data):
    import pandas as pd
    out = {}
    out["type_data"] = str(type(data))
    try:
        keys = list(data.keys())
    except Exception as e:
        out["keys_error"] = str(e)
        return out
    out["top_keys"] = ", ".join(map(str, keys)) if keys else "empty dict"
    rows = []
    for k in keys:
        v = data[k]
        info = {"key": str(k), "type": type(v).__name__}
        try:
            info["len"] = len(v)
        except Exception:
            info["len"] = -1
        if isinstance(v, dict):
            sub = list(v.keys())[:10]
            info["subkeys"] = ", ".join(map(str, sub))
            for sk in sub[:1]:
                vv = v[sk]
                info["sub_type"] = type(vv).__name__
                if isinstance(vv, dict):
                    info["sub_subkeys"] = ", ".join(map(str, list(vv.keys())[:10]))
                    for ssk in list(vv.keys())[:1]:
                        t = vv[ssk]
                        info["leaf_type"] = type(t).__name__
                        if isinstance(t, pd.DataFrame):
                            info["leaf_shape"] = str(t.shape)
                            info["leaf_cols"] = ", ".join(map(str, t.columns[:15]))
                elif isinstance(vv, pd.DataFrame):
                    info["leaf_shape"] = str(vv.shape)
                    info["leaf_cols"] = ", ".join(map(str, vv.columns[:15]))
        elif isinstance(v, pd.DataFrame):
            info["shape"] = str(v.shape)
            info["cols"] = ", ".join(map(str, v.columns[:15]))
        rows.append(info)
    out["structure"] = pd.DataFrame(rows) if rows else "no entries"
    return out
