# cgi.py - minimal shim for libraries expecting the old stdlib cgi module
# This is enough for httpx / googletrans which only need parse_header.

def parse_header(line):
    """
    Very small reimplementation of cgi.parse_header.
    Returns (value, params_dict).
    Example:
        'text/html; charset=utf-8'
        -> ('text/html', {'charset': 'utf-8'})
    """
    if not line:
        return '', {}

    parts = [p.strip() for p in line.split(';')]
    value = parts[0]
    params = {}

    for item in parts[1:]:
        if '=' in item:
            k, v = item.split('=', 1)
            k = k.strip()
            v = v.strip().strip('"')
            params[k] = v

    return value, params
