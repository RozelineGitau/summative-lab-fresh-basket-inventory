
import requests

BASE_URL = "https://world.openfoodfacts.org/cgi/search.pl"

HEADERS = {
    "User-Agent": "FreshBasketInventory/1.0 (inventory management project)"
}


def search_products(query, page_size=10):
    """Search OpenFoodFacts for food products."""

    if not query or not query.strip():
        raise ValueError("Search query cannot be empty")

    params = {
        "search_terms": query,
        "search_simple": 1,
        "action": "process",
        "json": 1,
        "page_size": page_size,
        "fields": "code,product_name,brands,categories,image_url"
    }

    try:
        response = requests.get(
            BASE_URL,
            params=params,
            headers=HEADERS,
            timeout=15
        )

        response.raise_for_status()
        data = response.json()

        products = []

        for product in data.get("products", []):
            products.append({
                "barcode": product.get("code"),
                "name": product.get("product_name"),
                "brand": product.get("brands"),
                "category": product.get("categories"),
                "image": product.get("image_url")
            })

        return products

    except requests.RequestException as error:
        raise RuntimeError(
            f"OpenFoodFacts API error: {error}"
        ) from error

    except ValueError as error:
        raise RuntimeError(
            "Could not read the API response"
        ) from error


def get_product_by_barcode(barcode):
    """Fetch one OpenFoodFacts product using its barcode."""

    if not barcode or not str(barcode).strip():
        raise ValueError("Barcode cannot be empty")

    url = (
        f"https://world.openfoodfacts.org/"
        f"api/v2/product/{barcode}.json"
    )

    try:
        response = requests.get(
            url,
            headers=HEADERS,
            timeout=(5, 30)
        )

        response.raise_for_status()
        data = response.json()

        if data.get("status") != 1:
            return None

        product = data.get("product", {})

        return {
            "barcode": product.get("code"),
            "name": product.get("product_name"),
            "brand": product.get("brands"),
            "category": product.get("categories"),
            "image": product.get("image_url")
        }

    except requests.Timeout as error:
        raise RuntimeError(
            "OpenFoodFacts request timed out. Please try again."
        ) from error

    except requests.RequestException as error:
        raise RuntimeError(
            f"OpenFoodFacts API error: {error}"
        ) from error

    except ValueError as error:
        raise RuntimeError(
            "Could not read the API response"
        ) from error
