import re


def get_number(input):
    if not input:
        return None
    """ Extracts the first float value from a string """
    ret = re.findall( r'-?[\d,]+\.?\d*', str(input))
    return float(ret[0].replace(',', '')) if len(ret) > 0 else None
