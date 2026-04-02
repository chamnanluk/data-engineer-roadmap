# Lesson Notes: Data Quality Issues and Cleaning Rules

This file captures common issues observed in beginner data projects and the explicit cleaning rules used to solve them.

## 1) Invalid or inconsistent dates

**Issue**
- Raw `order_date` values may have bad formats, impossible dates, or empty values.

**Cleaning rule**
- Parse with tolerant conversion (`errors='coerce'`) so invalid dates become null.
- Drop rows with null `order_date` before downstream loading.

**Why this matters**
- Time-based analytics (monthly trend, daily sales) become unreliable when dates are malformed.

## 2) Non-numeric quantity and price

**Issue**
- `quantity` and `unit_price` can include strings or symbols that fail numeric operations.

**Cleaning rule**
- Convert with numeric coercion.
- Drop rows where conversion fails (null after coercion).

**Why this matters**
- Revenue calculations and aggregations require numeric types.

## 3) Impossible business values

**Issue**
- Quantity may be zero/negative; unit price may be negative.

**Cleaning rule**
- Keep only `quantity > 0` and `unit_price >= 0`.

**Why this matters**
- Prevents invalid transactions from distorting revenue metrics.

## 4) Missing business keys and required identifiers

**Issue**
- Null IDs (`order_id`, `customer_id`, `product_id`) break uniqueness and joins.

**Cleaning rule**
- Drop records missing key identifiers required for pipeline integrity.

**Why this matters**
- Dimensional joins and fact table uniqueness depend on complete keys.

## 5) Text inconsistency in dimensions

**Issue**
- Names/cities/categories can include casing differences and extra whitespace.

**Cleaning rule**
- Trim whitespace, collapse multi-space text, and title-case values.

**Why this matters**
- Standardized text improves deduplication and cleaner reporting groups.

## 6) Duplicate business keys

**Issue**
- Repeated customer or product IDs may appear across source rows.

**Cleaning rule**
- Deduplicate by business key and keep the latest row encountered.

**Why this matters**
- Ensures one dimension row per business entity.

## Practical takeaway

The cleaning stage is not just formatting—it is where analytical correctness is protected. Explicit rules turn messy source data into trustworthy warehouse inputs.
