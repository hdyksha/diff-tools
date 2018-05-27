def join_json_by_key(json_A, json_B):
    joined_json = {}

    all_keys = set(json_A.keys()).union(set(json_B.keys()))
    for key in sorted(all_keys):
        val_A = json_A[key] if key in json_A else None
        val_B = json_B[key] if key in json_B else None
        joined_json[key] = (val_A, val_B)

    return joined_json
