"""VatRates class."""


class VatRates:
    """Lookup for VAT Rate IDs."""

    vat_rates = {5: 2, 20: 5, 0: 1}
    vat_rate_ids = {value: key for key, value in vat_rates.items()}

    @classmethod
    def get_vat_rate_by_id(cls, vat_rate_id):
        """Return VAT rate for given VAT rate ID."""
        return cls.vat_rate_ids[vat_rate_id]

    @classmethod
    def get_vat_rate_id_by_rate(cls, vat_rate):
        """Return VAT rate ID for given VAT rate."""
        return cls.vat_rates[vat_rate]
