import re

DID_REGEX=re.compile(r'^(Test|Unit)[A-Z]_[0-9]{3}_[0-9]{4}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01])$')
DID_REGEX_L=re.compile(r'^(Test|Unit)[A-Z]_[0-9]{3}_[0-9]{4}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01])')

CANON_C_REEL_REGEX=re.compile(r'^Canon[A-Z][0-9]{3}$')
ARRI_ALEXA_REEL_REGEX=re.compile(r'^[A-Z][0-9]{3}[A-Z0-9]{4}$')
ARRI_ALEXA_35_REEL_REGEX=re.compile(r'^[A-Z][A-Z_][0-9]{4}_[A-Z0-9]{4}$')

