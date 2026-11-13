import re

# Check if messege contains non clarke emoji using regex
def check_clarke_nonEmoji(text: str) -> bool:
    return bool(_EMOJI_PATTERN.search(text))


# will NOT pick up emojis create from other channels
# TODO: check for other channel emoji that dont start with :clarke*
_EMOJI_PATTERN = re.compile(
"["
"\U0001F1E6-\U0001F1FF" # regional indicators (flags)
"\U0001F300-\U0001F5FF" # symbols & pictographs
"\U0001F600-\U0001F64F" # emoticons
"\U0001F680-\U0001F6FF" # transport & map
"\U0001F700-\U0001F77F" # alchemical
"\U0001F780-\U0001F7FF" # geometric shapes extended
"\U0001F800-\U0001F8FF" # supplemental arrows-C
"\U0001F900-\U0001F9FF" # supplemental symbols & pictographs
"\U0001FA00-\U0001FA6F" # chess symbols
"\U0001FA70-\U0001FAFF" # symbols & pictographs extended-A
"\u2600-\u26FF" # misc symbols
"\u2700-\u27BF" # dingbats
"\u2B00-\u2BFF" # misc symbols & arrows
"\u2300-\u23FF" # misc technical
"]"
)


