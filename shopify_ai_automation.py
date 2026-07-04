#!/usr/bin/env python3
"""Generate Shopify SEO and Google Merchant Center-ready content with OpenAI.

Input is a CSV of Shopify products. Output is a CSV with AI-generated titles,
descriptions, meta fields, and Google Merchant Center-friendly attributes.
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from openai import OpenAI


DEFAULT_MODEL = "gpt-4.1-mini"

SYSTEM_PROMPT = """You are an ecommerce SEO and Google Merchant Center compliance specialist.
Create content that is accurate, specific, non-misleading, and suitable for Shopify.
Follow Google Merchant Center content principles: no gimmicky capitalization, no
unsupported claims, no promotional shipping/discount language, no policy-violating
claims, and no keyword stuffing. Return only valid JSON matching the requested schema.
"""


@dataclass(frozen=True)
class ProductInput:
    """Normalized product data read from a Shopify export or custom CSV."""

    handle: str
    title: str
    product_type: str
    vendor: str
    tags: str
    body_html: str
    variant_sku: str
    variant_price: str
    option_values: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate SEO and Google Merchant Center compliant product content using OpenAI."
    )
    parser.add_argument("--input", required=True, help="Path to input product CSV.")
    parser.add_argument("--output", required=True, help="Path to write enriched output CSV.")
    parser.add_argument("--model", default=DEFAULT_MODEL, help=f"OpenAI model to use. Default: {DEFAULT_MODEL}.")
    parser.add_argument("--brand", default="", help="Optional store or private-label brand to use when appropriate.")
    parser.add_argument("--market", default="United States", help="Target market for localization. Default: United States.")
    parser.add_argument("--language", default="English", help="Output language. Default: English.")
    parser.add_argument("--max-products", type=int, default=0, help="Optional limit for test runs. 0 means all rows.")
    parser.add_argument("--sleep", type=float, default=0.0, help="Seconds to sleep between API calls.")
    return parser.parse_args()


def first_present(row: dict[str, str], *names: str) -> str:
    for name in names:
        value = row.get(name, "")
        if value:
            return value.strip()
    return ""


def product_from_row(row: dict[str, str]) -> ProductInput:
    option_values = ", ".join(
        value
        for value in [
            first_present(row, "Option1 Value"),
            first_present(row, "Option2 Value"),
            first_present(row, "Option3 Value"),
        ]
        if value
    )
    return ProductInput(
        handle=first_present(row, "Handle", "handle"),
        title=first_present(row, "Title", "title", "Product Title"),
        product_type=first_present(row, "Type", "Product Type", "product_type"),
        vendor=first_present(row, "Vendor", "Brand", "vendor"),
        tags=first_present(row, "Tags", "tags"),
        body_html=first_present(row, "Body (HTML)", "Description", "body_html"),
        variant_sku=first_present(row, "Variant SKU", "SKU", "sku"),
        variant_price=first_present(row, "Variant Price", "Price", "price"),
        option_values=option_values,
    )


def build_user_prompt(product: ProductInput, brand: str, market: str, language: str) -> str:
    schema = {
        "seo_title": "50-70 characters, readable, high-intent, brand included only when useful",
        "product_title": "Shopify product title, clear and variant-aware, no promotional text",
        "meta_description": "140-160 characters, benefit-led, no unsupported claims",
        "product_description_html": "HTML with one short intro paragraph, bullet list, and use-case paragraph",
        "google_title": "Google Merchant Center title, under 150 characters, no all caps or promo language",
        "google_description": "Accurate plain-text GMC description, under 5000 characters",
        "google_product_category_hint": "Best-fit category hint, not a numeric taxonomy unless certain",
        "product_highlights": ["3-5 short factual highlights"],
        "search_keywords": ["5-10 relevant non-stuffed keywords"],
        "compliance_notes": ["brief notes about assumptions or missing product facts"],
    }
    payload = {
        "target_market": market,
        "language": language,
        "store_brand": brand,
        "product": product.__dict__,
        "json_schema": schema,
    }
    return json.dumps(payload, ensure_ascii=False, indent=2)


def generate_content(client: OpenAI, model: str, product: ProductInput, brand: str, market: str, language: str) -> dict[str, Any]:
    response = client.responses.create(
        model=model,
        input=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": build_user_prompt(product, brand, market, language)},
        ],
        text={"format": {"type": "json_object"}},
    )
    return json.loads(response.output_text)


def flatten_generated(generated: dict[str, Any]) -> dict[str, str]:
    flattened: dict[str, str] = {}
    for key, value in generated.items():
        if isinstance(value, list):
            flattened[f"AI {key}"] = " | ".join(str(item) for item in value)
        else:
            flattened[f"AI {key}"] = str(value)
    return flattened


def run() -> int:
    args = parse_args()
    if not os.environ.get("OPENAI_API_KEY"):
        print("OPENAI_API_KEY is required.", file=sys.stderr)
        return 2

    input_path = Path(args.input)
    output_path = Path(args.output)
    client = OpenAI()

    with input_path.open(newline="", encoding="utf-8-sig") as source:
        reader = csv.DictReader(source)
        source_fields = reader.fieldnames or []
        generated_fields = [
            "AI seo_title",
            "AI product_title",
            "AI meta_description",
            "AI product_description_html",
            "AI google_title",
            "AI google_description",
            "AI google_product_category_hint",
            "AI product_highlights",
            "AI search_keywords",
            "AI compliance_notes",
        ]
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with output_path.open("w", newline="", encoding="utf-8") as destination:
            writer = csv.DictWriter(destination, fieldnames=source_fields + generated_fields, extrasaction="ignore")
            writer.writeheader()
            for index, row in enumerate(reader, start=1):
                if args.max_products and index > args.max_products:
                    break
                product = product_from_row(row)
                generated = generate_content(client, args.model, product, args.brand, args.market, args.language)
                writer.writerow({**row, **flatten_generated(generated)})
                if args.sleep:
                    time.sleep(args.sleep)
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
