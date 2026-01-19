def compliance_check(emissions, max_allowed=50):
    if emissions <= max_allowed:
        return True
    return False
