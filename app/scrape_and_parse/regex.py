# Built-in imports
import re
# These functions are for parsing the scraping :tm:

"""
Example:
    NOV
    11
    Text

    Returns: 
        Nov
        11
"""
re_three_letter_two_digit_date = r"^[a-zA-Z]{3}\W\d{1,2}$"

"""
Example:
    Fri 19:00 UTC+01 · 84 guests

    returns: Fri 19:00 UTC+01
"""
re_utc_time = r".*UTC\+\d{2}"

"""
Example:
    NOV
    19
    Name - 32 guests

    Returns: Name - 32 guests 
"""
re_guests = r".*guest.*"

# Matches any line with 1 or more characters
re_line_with_characters = r"^.{1,}$"

def find_and_remove(data, pattern):
    found = re.search(pattern, data, flags=re.MULTILINE).group()
    data = data.replace(found, "")
    return data, found
