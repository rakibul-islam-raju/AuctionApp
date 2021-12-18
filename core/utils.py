from datetime import date


def get_auction_expired_or_not(end_date):
    expired = False
    if end_date >= date.today():
        expired = False
    else:
        expired = True
    return expired
