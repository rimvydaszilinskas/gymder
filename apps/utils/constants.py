# Mathematical Constants for calculations
EARTH_RADIUS = 6371
EARTH_RADIUS_METERS = EARTH_RADIUS * 1000

class Currencies:
    DKK = 'dkk'
    SEK = 'sek'
    NOK = 'nok'
    EUR = 'eur'
    GBP = 'gbp'
    USD = 'usd'
    CAD = 'cad'

    CHOICES = (
        (DKK, 'Danish Krona'),
        (SEK, 'Swedish Krona'),
        (NOK, 'Norwegian Krona'),
        (EUR, 'Euros'),
        (GBP, 'Pounds'),
        (USD, 'US Dollars'),
        (CAD, 'Canadian Dollars'),
    )

    ALL = (
        DKK,
        SEK,
        NOK,
        EUR,
        GBP,
        USD,
        CAD
    )