"""Standard product data models for the ecommerce automation pipeline."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


def utc_now_iso() -> str:
    """Return an ISO-8601 UTC timestamp for traceable pipeline events."""
    return datetime.now(timezone.utc).isoformat()


@dataclass(frozen=True)
class ProductInput:
    """Canonical product input accepted by the pipeline."""

    title: str
    price: float
    category: str
    description: str = ""
    sku: str = ""
    brand: str = ""
    attributes: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class AIEnrichment:
    """AI-ready marketing fields generated without external API calls."""

    title: str
    description: str
    seo_keywords: list[str]
    prompt_used: str


@dataclass(frozen=True)
class ShopifyProduct:
    """Shopify-ready product representation."""

    title: str
    body_html: str
    vendor: str
    product_type: str
    tags: list[str]
    variants: list[dict[str, Any]]


@dataclass(frozen=True)
class GMCFeedItem:
    """Google Merchant Center feed item representation."""

    title: str
    description: str
    price: str
    availability: str
    condition: str
    product_type: str


@dataclass(frozen=True)
class AdsCopy:
    """Ad copy variants for future campaign integrations."""

    headlines: list[str]
    descriptions: list[str]
    keywords: list[str]


@dataclass(frozen=True)
class PipelineOutput:
    """Full end-to-end pipeline result."""

    input_product: ProductInput
    ai_enrichment: AIEnrichment
    shopify_product: ShopifyProduct
    gmc_feed_item: GMCFeedItem
    ads_copy: AdsCopy
    trace: list[dict[str, Any]]
