"""Placeholder AI product title generator.

This module intentionally avoids real API calls. It exposes a deterministic
interface that can later be backed by an LLM provider.
"""

from __future__ import annotations

from src.ai.prompt_templates import TITLE_GENERATION_TEMPLATE
from src.core.schema import ProductInput


class ProductTitleGenerator:
    """Generate Shopify-ready product titles using a swappable interface."""

    def generate(self, product: ProductInput) -> tuple[str, str]:
        """Return a deterministic title and the prompt prepared for future AI use."""
        prompt = TITLE_GENERATION_TEMPLATE.format(title=product.title, category=product.category)
        normalized_category = product.category.title()
        if normalized_category.lower() in product.title.lower():
            return product.title, prompt
        return f"{product.title} - {normalized_category}", prompt
