import re

from dateparser import parse


def table_to_list(table):
    rows = []
    for row in table:
        current_row = {}
        for heading in row.headings:
            (value, field_name) = convert_to_type(heading, row[heading])
            current_row[field_name] = value
        rows.append(current_row)
    return rows


def convert_to_type(full_field_name, value):
    """ Converts the value from a behave table into its correct type based on the name
        of the column (header).  If it is wrapped in a convert method, then use it to
        determine the value type the column should contain.

        Returns: a tuple with the newly converted value and the name of the field (without the
                 conversion method specified).  E.g. int(size) will return size as the new field
                 name and the value will be converted to an int and returned.
        https://stackoverflow.com/questions/38275023/how-can-i-specify-the-type-of-a-column-in-a-python-behave-step-data-table
    """
    field_name = full_field_name.strip()
    matchers = [(re.compile('int\((.*)\)'), lambda val: int(val)),
                (re.compile('float\((.*)\)'), lambda val: float(val)),
                (re.compile('date\((.*)\)'), lambda val: parse(val, settings={'TIMEZONE': 'Asia/Shanghai'}))]
    for (matcher, func) in matchers:
        matched = matcher.match(field_name)
        if matched:
            return (func(value), matched.group(1))
    return (value, full_field_name)
