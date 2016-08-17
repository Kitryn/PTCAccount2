def tag_email(email_address, tag):

    combined_length = len(email_address) + len(tag)

    if combined_length > 74:
        # Combined email address too long, truncating tag
        # Max email length is 75, but this takes into account the extra "+"
        diff = combined_length - 74
        tag = tag[0:-diff]

    return email_address.replace('@', '+{}@'.format(tag), 1)
