# Design notes

## User
Frontline sales representative visiting retailers.

## Core jobs-to-be-done
1. Find product/category information quickly.
2. Verify that a statement is supported by company material.
3. Translate internal/product language into retailer-friendly language.
4. Know when the system does not have enough evidence.

## Deliberate non-goals
- generating real commercial schemes
- exposing confidential pricing
- making autonomous order decisions
- pretending public documents are internal documents

## Production data model
Every chunk should carry:
- document_id
- document_version
- publication_date
- page
- category
- brand
- channel
- geography
- access_scope
- source_url

This enables access control, temporal retrieval and precise citations.
