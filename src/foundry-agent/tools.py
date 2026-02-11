"""
Contoso Electronics -- Custom function tools for the Foundry agent.

Each function here becomes a tool the agent can call. The SDK reads
the function name, docstring, and type hints to build the JSON schema
automatically via FunctionTool.

TODO: Replace mock data with real API calls, database lookups, etc.
"""

import json


def lookup_order(order_id: str) -> str:
    """
    Look up the current status of a customer order.

    :param order_id: The order identifier (e.g. CT-991100).
    :return: JSON string with order status details.
    """
    # TODO: Replace with real order system API call
    orders = {
        "CT-991100": {
            "status": "Shipped",
            "carrier": "FedEx",
            "tracking": "1234567890",
            "eta": "2026-02-14",
        },
        "CT-991101": {
            "status": "Processing",
            "payment": "confirmed",
            "estimated_ship": "2026-02-12",
        },
        "CT-991102": {
            "status": "Delivered",
            "delivered_date": "2026-02-08",
            "signed_by": "J. Smith",
        },
    }
    result = orders.get(order_id, {"error": f"Order {order_id} not found"})
    return json.dumps(result)


def check_return_eligibility(order_id: str, reason: str) -> str:
    """
    Check whether an order is eligible for return or refund.

    :param order_id: The order identifier.
    :param reason: The customer's reason for returning.
    :return: JSON string with eligibility details.
    """
    # TODO: Replace with real returns policy engine
    return json.dumps({
        "order_id": order_id,
        "eligible": True,
        "policy": "30-day satisfaction guarantee",
        "restocking_fee": "15% for opened items",
        "reason_acknowledged": reason,
        "next_step": "Provide return shipping label via email",
    })


def check_warranty(product_name: str) -> str:
    """
    Check warranty coverage and expiration for a Contoso product.

    :param product_name: The product name to look up.
    :return: JSON string with warranty details.
    """
    # TODO: Replace with real warranty database lookup
    warranties = {
        "Contoso Pro X15": {
            "coverage": "2-year limited",
            "expires": "2028-03-15",
            "includes": ["hardware defects", "battery replacement"],
        },
        "Contoso Elite 17": {
            "coverage": "2-year limited + accidental damage",
            "expires": "2028-06-01",
            "includes": ["hardware defects", "battery", "screen", "accidental damage"],
        },
    }
    result = warranties.get(
        product_name,
        {"error": f"No warranty record found for '{product_name}'"},
    )
    return json.dumps(result)


# ---------------------------------------------------------------
# Collect all tool functions in a set for FunctionTool registration
# ---------------------------------------------------------------
ALL_TOOLS: set = {lookup_order, check_return_eligibility, check_warranty}
