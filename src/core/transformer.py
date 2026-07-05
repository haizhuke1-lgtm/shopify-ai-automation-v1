"""Data conversion utilities between pipeline modules."""

from __future__ import annotations

import re
from dataclasses import asdict
from typing import Any

from src.core.schema import AdsCopy, AIEnrichment, GMCFeedItem, ProductInput, ShopifyProduct


def product_from_mapping(data: dict[str, Any]) -> ProductInput:
    """Normalize loose input dictionaries into the canonical product model."""
    return ProductInput(
        title=str(data.get("title", "")).strip(),
        price=float(data.get("price", 0)),
        category=str(data.get("category", "uncategorized")).strip(),
        description=str(data.get("description", "")).strip(),
        sku=str(data.get("sku", "")).strip(),
        brand=str(data.get("brand", "")).strip(),
        attributes=dict(data.get("attributes", {})),
    )


def to_shopify_product(product: ProductInput, enrichment: AIEnrichment) -> ShopifyProduct:
    """Convert enriched data into a Shopify product payload."""
    tags = sorted({product.category.lower(), *enrichment.seo_keywords[:5]})
    return ShopifyProduct(
        title=enrichment.title,
        body_html=enrichment.description,
        vendor=product.brand or "Future Brand",
        product_type=product.category,
        tags=tags,
        variants=[{"sku": product.sku, "price": f"{product.price:.2f}", "inventory_policy": "deny"}],
    )


def to_gmc_feed_item(product: ProductInput, enrichment: AIEnrichment) -> GMCFeedItem:
    """Convert enriched data into a Google Merchant Center feed item."""
    plain_description = re.sub(r"<[^>]+>", " ", enrichment.description)
    plain_description = " ".join(plain_description.split())
    return GMCFeedItem(
        title=enrichment.title[:150],
        description=plain_description[:5000],
        price=f"{product.price:.2f} USD",
        availability="in_stock",
        condition="new",
        product_type=product.category,
    )


def to_ads_copy(product: ProductInput, enrichment: AIEnrichment) -> AdsCopy:
    """Create deterministic ads copy for future ad-platform integrations."""
    return AdsCopy(
        headlines=[
            enrichment.title[:30],
            f"Shop {product.category.title()} Decor"[:30],
            "Meaningful Home Accent",
        ],
        descriptions=[
            f"Discover {product.title} for curated home styling."[:90],
            "Ready for modular Shopify, GMC, and ads automation."[:90],
        ],
        keywords=enrichment.seo_keywords,
    )


def serialize_dataclass(value: Any) -> Any:
    """Serialize dataclass pipeline objects for display or JSON output."""
    return asdict(value) if hasattr(value, "__dataclass_fields__") else value
