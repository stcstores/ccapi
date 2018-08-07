"""This module contains the URL class."""


class URLs:
    """Class containing methods for generating Cloud Commerce Pro URLs."""

    cloud_commerce_domain = "cloudcommercepro.com"

    @classmethod
    def get_url(cls, subdomain=None, uri="", params=""):
        """
        Return URL.

        Kwargs:
            subdomain: If not None adds subdomain to url. Default: None.
            uri: If not None adds uri to domain. Iterable of path elements.
            params: Dict containing paramaters for get request.

        Returns (str) URL.

        """
        domain = cls.get_full_domain(subdomain=subdomain)
        if len(uri) > 0:
            uri = cls.get_uri(uri)
        if len(params) > 0:
            params = cls.get_get(params)
        return "{}{}.aspx{}".format(domain, uri, params)

    @classmethod
    def get_uri(cls, uri):
        """Return URI from iterable of path elements."""
        return "/{}".format("/".join(uri))

    @classmethod
    def get_get(cls, params):
        """Return get request string from dict of key, value pairs."""
        param_strings = ["{}={}".format(key, value) for key, value in params.items()]
        return "?{}".format("&".join(param_strings))

    @classmethod
    def get_full_domain(cls, subdomain=None):
        """
        Return URL of cloud commerce.

        Kwargs:
            subdomain: If not None adds subdomain to domain.

        Return str.

        """
        if subdomain is None:
            return "http://{}".format(cls.cloud_commerce_domain)
        return "http://{}.{}".format(subdomain, cls.cloud_commerce_domain)

    @classmethod
    def range_url(cls, subdomain, range_id):
        """Return URL of Product Range."""
        uri = ("Admin", "ProductRange")
        params = {"ProdRangeID": str(range_id)}
        return cls.get_url(subdomain=subdomain, uri=uri, params=params)

    @classmethod
    def product_url(cls, subdomain, range_id, product_id, channel_id=0):
        """Return URL of Product."""
        uri = ("Admin", "Product")
        params = {
            "ProdRangeID": range_id,
            "ProductID": product_id,
            "ChannelID": channel_id,
        }
        return cls.get_url(subdomain=subdomain, uri=uri, params=params)

    @classmethod
    def order_url(cls, subdomain, order_id, customer_id):
        """Return URL of Order."""
        uri = ("Admin", "OrderDetails")
        params = {"OrderID": order_id, "CustomerID": customer_id}
        return cls.get_url(subdomain=subdomain, uri=uri, params=params)
