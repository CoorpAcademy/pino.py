
def merge_dicts(dict_a, dict_b):
    """Return dict issue from merge from dict_a and dict_b, dict_a having precedence"""
    # inspired from https://stackoverflow.com/questions/7204805/dictionaries-of-dictionaries-merge/7205107#7205107
    if not dict_a:
        return dict_b
    if not dict_b:
        return dict_a
    merged_dict = dict(dict_a)
    for key in dict_b:
        if key in dict_a:
            if isinstance(dict_a[key], dict) and isinstance(dict_b[key], dict):
                merged_dict[key] = merge_dicts(dict_a[key], dict_b[key])
        else:
            merged_dict[key] = dict_b[key]
    return merged_dict
