import copy
import inspect


def flatten_dict(d):
    out = {}
    for key, val in d.items():
        if isinstance(val, dict):
            val = [val]
        if isinstance(val, list):
            array = []
            for subdict in val:
                if not isinstance(subdict, dict):
                    array.append(subdict)
                else:
                    deeper = flatten_dict(subdict).items()
                    out.update({str(key) + '.' + str(key2): val2 for key2, val2 in deeper})
            if array:
                out.update({str(key): array})
        else:
            out[str(key)] = val
    return out


def reverse_flatten_dict(d: dict) -> dict:
    result = {}
    for key, val in d.items():
        nested_keys = key.split('.')
        d_ = result
        for k in nested_keys[:-1]:
            if k not in d_:
                d_[k] = {}
            d_ = d_[k]
        d_[nested_keys[-1]] = val

    return result


def add_dict(first_dict: dict, second_dict: dict):
    ans_dict = dict()
    for key in first_dict.keys():
        ans_dict[key] = first_dict[key] + second_dict[key]
    return ans_dict


def remove_none_value_dict(a_dict):
    copy_dict = a_dict.copy()
    for key, value in copy_dict.items():
        if value is None:
            a_dict.pop(key)
    return a_dict


def delete_none(_dict):
    """Delete None values recursively from all the dictionaries"""
    for key, value in list(_dict.items()):
        if isinstance(value, dict):
            delete_none(value)
        elif value is None:
            del _dict[key]
        elif isinstance(value, list):
            for v_i in value:
                if isinstance(v_i, dict):
                    delete_none(v_i)

    return _dict


def filter_doc_by_keys(doc, keys):
    doc_ = copy.deepcopy(doc)
    if keys is None:
        return doc_
    return dict(filter(lambda x: x[0] in keys, doc_.items()))


def get_class_constant_keys(cls):
    keys = []
    for attr in inspect.getmembers(cls):
        # to remove private and protected functions
        if not attr[0].startswith('_'):
            # To remove function
            if not inspect.ismethod(attr[1]):
                keys.append(attr[1])

    return keys


def short_address(address: str, n_start=3, n_end=4):
    if not address:
        return ''
    return address[:n_start + 2] + '...' + address[-n_end:]


def all_equal(array):
    return (not array) or (array.count(array[0]) == len(array))
