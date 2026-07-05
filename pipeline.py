"""End-to-end AI ecommerce pipeline controller.

Workflow: Product Input → AI Enrichment → Shopify Format → GMC Feed → Ads Copy.
No real API calls are made; AI modules are deterministic placeholders designed
for future provider integration.
"""

from __future__ import annotations

from src.ai.description_generator import ProductDescriptionGenerator
from src.ai.title_generator import ProductTitleGenerator
from src.core.logger import PipelineLogger
from src.core.schema import AIEnrichment, PipelineOutput, ProductInput
from src.core.transformer import to_ads_copy, to_gmc_feed_item, to_shopify_product


class EcommercePipeline:
    """Coordinate modular product enrichment and channel formatting stages."""

    def __init__(self, logger: PipelineLogger | None = None) -> None:
        self.logger = logger or PipelineLogger()
        self.title_generator = ProductTitleGenerator()
        self.description_generator = ProductDescriptionGenerator()

    def run(self, product: ProductInput) -> PipelineOutput:
        """Execute the complete production-oriented pipeline for one product."""
        self.logger.success("Product Input", "ProductInput", "Product accepted", title=product.title)

        try:
            generated_title, title_prompt = self.title_generator.generate(product)
            description, keywords, description_prompt = self.description_generator.generate(product)
            enrichment = AIEnrichment(
                title=generated_title,
                description=description,
                seo_keywords=keywords,
                prompt_used=f"{title_prompt}\n\n{description_prompt}",
            )
            self.logger.success("AI Enrichment", "src.ai", "Generated placeholder AI enrichment")
        except Exception as exc:
            self.logger.failure("AI Enrichment", "src.ai", str(exc))
            raise

        try:
            shopify_product = to_shopify_product(product, enrichment)
            self.logger.success("Shopify Format", "src.core.transformer", "Created Shopify payload")
        except Exception as exc:
            self.logger.failure("Shopify Format", "src.core.transformer", str(exc))
            raise

        try:
            gmc_feed_item = to_gmc_feed_item(product, enrichment)
            self.logger.success("GMC Feed", "src.core.transformer", "Created GMC feed item")
        except Exception as exc:
            self.logger.failure("GMC Feed", "src.core.transformer", str(exc))
            raise

        try:
            ads_copy = to_ads_copy(product, enrichment)
            self.logger.success("Ads Copy", "src.core.transformer", "Created ads copy")
        except Exception as exc:
            self.logger.failure("Ads Copy", "src.core.transformer", str(exc))
            raise

        return PipelineOutput(product, enrichment, shopify_product, gmc_feed_item, ads_copy, self.logger.events)
