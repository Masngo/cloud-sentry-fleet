#!/bin/bash
curl -s -X POST http://localhost:8000/v1/alerts/ingest \
  -H "Content-Type: application/json" -H "x-api-key: dev-secret-key" \
  -d '{"service_name": "payment-api", "environment": "prod", "severity": "CRITICAL", "log_trace": "Memory exception user@email.com", "timestamp": "2026-08-18T00:00:00Z"}'
