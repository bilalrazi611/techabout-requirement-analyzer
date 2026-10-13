"""
TechAbout service catalogue derived from https://www.techabout.com/services
Updated: 2026-10 (matches live site structure)
"""

from typing import List, Dict

ENTERPRISE_SERVICES: List[Dict] = [
    {
        "id": "ai-ml",
        "name": "AI & Machine Learning",
        "keywords": [
            "ai", "machine learning", "ml", "llm", "rag", "gpt", "openai",
            "computer vision", "document intelligence", "fine-tuning",
            "model", "predictive", "forecasting", "nlp", "chatbot",
            "generative", "embedding", "vector", "langchain"
        ],
        "description": "Custom model development, RAG/LLM systems, computer vision, forecasting, MLOps."
    },
    {
        "id": "enterprise-software",
        "name": "Enterprise Software Development",
        "keywords": [
            "enterprise software", "custom software", "internal tool", "platform",
            "erp", "crm", "workflow", "business application", "legacy modernization",
            "system integration", "api gateway"
        ],
        "description": "Custom enterprise applications, platforms, API design and third-party integrations."
    },
    {
        "id": "cloud-devops",
        "name": "Cloud Infrastructure & DevOps",
        "keywords": [
            "cloud", "aws", "azure", "gcp", "kubernetes", "k8s", "docker",
            "devops", "ci/cd", "infrastructure", "terraform", "ansible",
            "monitoring", "observability", "scaling", "serverless"
        ],
        "description": "Cloud architecture (AWS/GCP/Azure), Kubernetes, CI/CD, reliability and cost optimisation."
    },
    {
        "id": "web-mobile",
        "name": "Web & Mobile App Development",
        "keywords": [
            "web app", "mobile app", "react", "next.js", "flutter", "react native",
            "ios", "android", "pwa", "frontend", "backend", "full-stack",
            "dashboard", "portal", "spa"
        ],
        "description": "Web apps (React/Next.js), cross-platform mobile (React Native/Flutter), API & backend."
    },
    {
        "id": "data-analytics",
        "name": "Data Engineering & Analytics",
        "keywords": [
            "data pipeline", "etl", "elt", "warehouse", "lakehouse", "analytics",
            "bi", "dashboard", "reporting", "data modelling", "snowflake",
            "bigquery", "redshift", "dbt", "airflow"
        ],
        "description": "Data pipelines, warehouse/lakehouse architecture, single source of truth, analytics."
    },
    {
        "id": "cybersecurity",
        "name": "Cybersecurity & Compliance",
        "keywords": [
            "security", "penetration testing", "pen test", "red team", "hardening",
            "soc 2", "iso 27001", "gdpr", "pci", "compliance", "vulnerability",
            "audit", "encryption", "zero trust"
        ],
        "description": "Penetration testing, application & cloud hardening, SOC2/ISO/GDPR/PCI readiness."
    },
    {
        "id": "digital-transformation",
        "name": "Digital Transformation",
        "keywords": [
            "digital transformation", "legacy", "modernisation", "modernization",
            "process automation", "workflow redesign", "business process",
            "change management", "digitization"
        ],
        "description": "Legacy system migration, process automation, systems & data integration."
    },
    {
        "id": "saas-platforms",
        "name": "SaaS & Digital Platforms",
        "keywords": [
            "saas", "multi-tenant", "subscription", "billing", "marketplace",
            "platform", "tenant", "usage-based", "permissions", "rbac"
        ],
        "description": "Multi-tenant SaaS architecture, subscription/usage billing, roles & admin tooling."
    },
    {
        "id": "enterprise-mobile",
        "name": "Enterprise Mobile Apps",
        "keywords": [
            "offline", "field app", "warehouse", "driver app", "sync",
            "enterprise mobile", "offline-first"
        ],
        "description": "Offline-first mobile tools for field teams, warehouses, drivers with ERP/CRM integration."
    },
    {
        "id": "qa-automation",
        "name": "QA & Test Automation",
        "keywords": [
            "qa", "testing", "test automation", "selenium", "cypress", "playwright",
            "performance testing", "load testing", "security testing", "regression"
        ],
        "description": "UI/API/load test automation, manual & exploratory testing, performance & security testing."
    },
    {
        "id": "iot",
        "name": "IoT & Connected Systems",
        "keywords": [
            "iot", "sensor", "firmware", "edge", "connected device", "mqtt",
            "industrial iot", "fleet", "smart building"
        ],
        "description": "Device connectivity, firmware, secure data ingestion, real-time processing."
    },
    {
        "id": "blockchain",
        "name": "Blockchain & Web3",
        "keywords": [
            "blockchain", "web3", "smart contract", "solidity", "token", "nft",
            "defi", "dapp", "ethereum", "solana", "tokenisation"
        ],
        "description": "Smart contract development & auditing, tokenisation, dApp & DeFi development."
    },
]

EXPRESS_SERVICES: List[Dict] = [
    {
        "id": "express-web-migration",
        "name": "Website Migration (Express)",
        "keywords": ["migrate website", "wordpress migration", "shopify migration", "next.js migration"],
        "description": "Fixed-price platform-to-platform website migrations."
    },
    {
        "id": "express-ecommerce",
        "name": "E-commerce Store Setup (Express)",
        "keywords": ["shopify store", "woocommerce", "ecommerce store", "online store setup"],
        "description": "Ready-to-sell Shopify or WooCommerce stores with payments & shipping."
    },
    {
        "id": "express-wordpress",
        "name": "WordPress Development (Express)",
        "keywords": ["wordpress website", "wordpress site", "wp theme", "wordpress development"],
        "description": "Fixed-price professional WordPress websites."
    },
    {
        "id": "express-mobile",
        "name": "Cross-Platform Mobile App (Express)",
        "keywords": ["simple mobile app", "mvp app", "flutter mvp"],
        "description": "Fixed-price cross-platform Android/iOS app packages."
    },
    {
        "id": "express-seo",
        "name": "Digital Marketing & SEO (Express)",
        "keywords": ["seo", "google ads", "meta ads", "digital marketing", "content writing"],
        "description": "SEO, paid ads, content writing and growth packages."
    },
    {
        "id": "express-security",
        "name": "Website Security & Maintenance (Express)",
        "keywords": ["malware removal", "wordpress security", "website maintenance", "care plan"],
        "description": "Malware cleanup, hardening and monthly care plans."
    },
]

ALL_SERVICES = ENTERPRISE_SERVICES + EXPRESS_SERVICES


def get_service_by_id(service_id: str) -> Dict | None:
    for s in ALL_SERVICES:
        if s["id"] == service_id:
            return s
    return None
