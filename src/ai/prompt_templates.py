"""Prompt templates for future AI-powered product marketing modules."""

TITLE_GENERATION_TEMPLATE = """
Create a concise, high-intent ecommerce product title.
Product: {title}
Category: {category}
Constraints: accurate, no unsupported claims, no promotional pricing language.
""".strip()

DESCRIPTION_GENERATION_TEMPLATE = """
Write an SEO-friendly Shopify product description.
Product: {title}
Category: {category}
Audience: shoppers looking for quality and giftable home products.
Constraints: factual, clear, scannable, and compliant with marketplace policies.
""".strip()

ADS_COPY_TEMPLATE = """
Create search ad copy for a product campaign.
Product: {title}
Category: {category}
Use benefits without exaggeration or policy-sensitive claims.
""".strip()
