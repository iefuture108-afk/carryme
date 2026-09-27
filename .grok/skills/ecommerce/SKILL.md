---
name: ecommerce
description: Builds and audits e-commerce projects — product catalogs, cart and checkout flows, payments, inventory, order management, and storefront UX. Use when the user mentions ecommerce, e-commerce, store, shop, cart, checkout, product listing, payment gateway, inventory, orders, or asks to add a skill for all e-commerce projects. Trigger with "/ecommerce" or "build my store".
when-to-use: ecommerce, e-commerce, storefront, product catalog, shopping cart, checkout, payment integration, inventory management, order tracking, marketplace, Shopify, WooCommerce
user-invocable: true
argument-hint: "[feature or audit target]"
---

# Ecommerce Skill

Apply this skill to any e-commerce project. Follow the steps in order and do not skip validation.

## 1. Scope the store
- Identify product type (physical, digital, subscription), target market, and currency.
- Confirm payment providers (Stripe, Razorpay, PayPal, Cashfree, etc.) and tax rules.
- List required integrations: shipping, email, analytics, inventory sync.

## 2. Data model
- Products: id, sku, name, description, price, currency, stock, images, variants, categories, tags, status.
- Cart: line items, quantities, subtotal, tax, shipping, total, expiry.
- Orders: id, customer, items, payment status, fulfillment status, timestamps.
- Customers: id, email, name, addresses, order history.
- Use UUIDs for all primary keys. Never expose sequential ids.

## 3. Catalog and search
- Paginate product listings (default 24 per page). Support filters by category, price range, and attributes.
- Full-text search on name and description. Index variants separately.
- SEO: unique title, meta description, canonical URL, structured data (Product schema) per page.

## 4. Cart and checkout
- Cart persists server-side (cookie/session) and syncs on login. Guest carts merge on authentication.
- Checkout steps: contact, shipping, payment, review. One concern per step.
- Validate stock at checkout time, not just add-to-cart. Reserve inventory on order creation.
- Idempotent order creation: duplicate requests must not double-charge.

## 5. Payments
- Never store raw card data. Use provider tokens and webhooks.
- Verify webhook signatures. Handle success, failure, and pending states.
- Support refunds and partial refunds. Log every payment event with provider reference.
- Currency conversion only via provider rates; never hardcode exchange rates.

## 6. Inventory and fulfillment
- Track stock per variant. Decrement on paid order, restore on cancel or refund.
- Low-stock alerts below a configurable threshold.
- Fulfillment states: pending, processing, shipped, delivered, returned. Each transition logged.

## 7. Security and compliance
- HTTPS everywhere. CSRF tokens on state-changing forms.
- Rate-limit checkout and payment endpoints. CAPTCHA on repeated failures.
- PCI-DSS scope minimized. GDPR/DPDP: consent for marketing, data export and delete on request.
- Secrets in environment variables only. Never commit keys.

## 8. Performance and reliability
- Cache product pages and catalog queries. Invalidate on update.
- Image optimization: responsive srcset, WebP, lazy load.
- Database indexes on sku, category, status, and order timestamps.
- Health check endpoint and structured error logging with request ids.

## 9. Validation checklist
Before shipping, confirm:
- [ ] Checkout is idempotent under double-submit
- [ ] Webhook signature verified
- [ ] Stock never goes negative
- [ ] Prices shown match charged amount including tax
- [ ] Guest and logged-in carts both work
- [ ] Refund restores inventory
- [ ] No secrets in the repository

## 10. Output
Report what was built or audited, the files changed, and any open risks. Do not claim a feature works without evidence from the code or tests.
