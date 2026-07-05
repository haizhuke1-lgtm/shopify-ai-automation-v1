"""SEO product description generator placeholder with no external calls."""

from __future__ import annotations

from src.ai.prompt_templates import DESCRIPTION_GENERATION_TEMPLATE
from src.core.schema import ProductInput


class ProductDescriptionGenerator:
    """Generate deterministic SEO descriptions until an AI provider is added."""

    def generate(self, product: ProductInput) -> tuple[str, list[str], str]:
        """Return HTML description, keywords, and future-AI prompt."""
        prompt = DESCRIPTION_GENERATION_TEMPLATE.format(title=product.title, category=product.category)
        keywords = [
            product.title.lower(),
            product.category.lower(),
            "shopify product",
            "gift decor",
            "home accent",
        ]
        description = (
            f"<p>{product.title} is a thoughtfully selected {product.category} item "
            "designed for shoppers who value meaningful decorative accents.</p>"
            "<ul>"
            f"<li>Category: {product.category.title()}</li>"
            f"<li>Price-ready for merchandising at ${product.price:.2f}</li>"
            "<li>Prepared for Shopify, Google Merchant Center, and ads workflows</li>"
            "</ul>"
            "<p>Use this modular description as a compliant baseline before adding "
            "brand-specific product facts, materials, dimensions, and care details.</p>"
        )
        return description, keywords, prompt
