import re

EMAIL_PATTERN = re.compile(
    r"^[A-Za-z0-9](?:[\w\.-]*[A-Za-z0-9])?"
    r"@"
    r"[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?"
    r"((?:\.[A-Za-z]{2,})+)$"
    )

PASSWORD_PATTERN = re.compile(r"^(?=.*\d).{8,}$")