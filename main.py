"""Demo runner for the modular Shopify AI automation pipeline."""

from __future__ import annotations

import json

from pipeline import EcommercePipeline
from src.core.transformer import product_from_mapping, serialize_dataclass


SAMPLE_PRODUCT = {
    "title": "Chinese Lucky Gourd Ornament",
    "price": 89,
    "category": "home decor",
}


def main() -> int:
    """Run the sample product through every pipeline stage and print results."""
    product = product_from_mapping(SAMPLE_PRODUCT)
    output = EcommercePipeline().run(product)

    stages = [
        ("Product Input", output.input_product),
        ("AI Enrichment", output.ai_enrichment),
        ("Shopify Format", output.shopify_product),
        ("GMC Feed", output.gmc_feed_item),
        ("Ads Copy", output.ads_copy),
        ("Pipeline Trace", output.trace),
    ]
    for stage, payload in stages:
        print(f"\n=== {stage} ===")
        print(json.dumps(serialize_dataclass(payload), indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
