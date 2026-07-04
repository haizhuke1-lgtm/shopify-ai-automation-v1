# shopify-ai-automation-v1

AI-powered Shopify automation system for generating SEO products, Google Merchant Center feeds, and ad copy for cross-border e-commerce.

## Shopify AI SEO Automation Script

`shopify_ai_automation.py` reads a Shopify product CSV and appends AI-generated content fields for:

- SEO optimized product titles
- Shopify-ready product descriptions in HTML
- Meta descriptions
- Google Merchant Center compliant titles and descriptions
- Product highlights, search keywords, category hints, and compliance notes

The script uses the OpenAI Python SDK and the Responses API. Set `OPENAI_API_KEY` before running it.

### Install

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Run

```bash
export OPENAI_API_KEY="your_api_key_here"
python shopify_ai_automation.py \
  --input sample_products.csv \
  --output enriched_products.csv \
  --brand "Example Apparel" \
  --market "United States" \
  --language "English"
```

### Useful options

- `--model`: OpenAI model name. Defaults to `gpt-4.1-mini`.
- `--max-products`: Limit rows for a test run.
- `--sleep`: Add a delay between API calls for rate-limit control.
- `--brand`: Store or private-label brand to include when it is useful and accurate.

### Input columns

The script supports standard Shopify export columns such as `Handle`, `Title`, `Body (HTML)`, `Vendor`, `Type`, `Tags`, `Variant SKU`, `Variant Price`, and option values. It also accepts common lowercase alternatives such as `title`, `sku`, and `price`.
