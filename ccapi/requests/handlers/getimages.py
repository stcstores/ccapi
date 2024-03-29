"""
getImages request.

Gets images for a Product.
"""
from bs4 import BeautifulSoup

from ccapi.cc_objects import ProductImage
from ccapi.requests import APIRequest


class GetImages(APIRequest):
    """getImages request."""

    uri = "Handlers/getImages.ashx"

    def __new__(self, range_id="", product_id=""):
        """Create getImages request.

        Kwargs:
            range_id: ID of Product Range.
            product_id: ID of Product.
        """
        self.range_id = range_id
        self.product_id = product_id
        return super().__new__(self)

    def process_response(self, response):
        """Handle request response."""
        html = response.text
        if "NoRecFound" in html:
            return []
        soup = BeautifulSoup(html, "html.parser")
        images = []
        image_divs = soup.findAll("li", {"class": "ui-state-default"})
        for image_div in image_divs:
            image_id = image_div["id"]
            image_name = image_div["data-masterid"]
            url = image_div.find("img")["src"]
            image = ProductImage(url=url, image_id=image_id, image_name=image_name)
            images.append(image)
        return images

    def get_data(self):
        """Get data for request."""
        return {
            "ProgType": "DisplaySortableImages",
            "ProductID": self.product_id,
            "rID": self.range_id,
            "cID": "",
        }

    def get_params(self):
        """Get parameters for get request."""
        return {"d": "155"}
