
import pytest
import requests
from unittest.mock import patch, Mock

from external_api import search_products, get_product_by_barcode


SAMPLE_PRODUCT = {
    "code": "20208639",
    "product_name": "Smoothie mela, banana, mango",
    "brands": "Solevita",
    "categories": "Smoothies",
    "image_url": "https://example.com/image.jpg"
}


def test_search_products_success():
    mock_response = Mock()

    mock_response.json.return_value = {
        "products": [SAMPLE_PRODUCT]
    }

    mock_response.raise_for_status.return_value = None

    with patch("external_api.requests.get", return_value=mock_response):
        result = search_products("mango")

    assert len(result) == 1
    assert result[0]["name"] == "Smoothie mela, banana, mango"
    assert result[0]["barcode"] == "20208639"
    assert result[0]["brand"] == "Solevita"


def test_search_products_empty_query():
    with pytest.raises(ValueError, match="Search query cannot be empty"):
        search_products("")


def test_search_products_api_error():
    with patch(
        "external_api.requests.get",
        side_effect=requests.RequestException("Connection failed")
    ):
        with pytest.raises(RuntimeError, match="OpenFoodFacts API error"):
            search_products("mango")


def test_search_products_invalid_json():
    mock_response = Mock()
    mock_response.raise_for_status.return_value = None
    mock_response.json.side_effect = ValueError("Invalid JSON")

    with patch("external_api.requests.get", return_value=mock_response):
        with pytest.raises(RuntimeError, match="Could not read the API response"):
            search_products("mango")


def test_get_product_by_barcode_success():
    mock_response = Mock()

    mock_response.json.return_value = {
        "status": 1,
        "product": SAMPLE_PRODUCT
    }

    mock_response.raise_for_status.return_value = None

    with patch("external_api.requests.get", return_value=mock_response):
        result = get_product_by_barcode("20208639")

    assert result["barcode"] == "20208639"
    assert result["name"] == "Smoothie mela, banana, mango"
    assert result["brand"] == "Solevita"


def test_get_product_by_barcode_not_found():
    mock_response = Mock()

    mock_response.json.return_value = {
        "status": 0
    }

    mock_response.raise_for_status.return_value = None

    with patch("external_api.requests.get", return_value=mock_response):
        result = get_product_by_barcode("0000000000000")

    assert result is None


def test_get_product_by_barcode_empty():
    with pytest.raises(ValueError, match="Barcode cannot be empty"):
        get_product_by_barcode("")


def test_get_product_by_barcode_timeout():
    with patch(
        "external_api.requests.get",
        side_effect=requests.Timeout("Request timed out")
    ):
        with pytest.raises(RuntimeError, match="request timed out"):
            get_product_by_barcode("20208639")


def test_get_product_by_barcode_invalid_json():
    mock_response = Mock()
    mock_response.raise_for_status.return_value = None
    mock_response.json.side_effect = ValueError("Invalid JSON")

    with patch("external_api.requests.get", return_value=mock_response):
        with pytest.raises(RuntimeError, match="Could not read the API response"):
            get_product_by_barcode("20208639")
