# Evaluation report (LLM_PROVIDER=none)

- Briefs run: 27
- Briefs with an expected service area: 24
- **Hit rate** (at least one expected service suggested): 20/24 = 83%
- **Average recall** (share of expected services found): 75%
- Analyzer modes seen: keyword_fallback

Expected services are my own judgement of what a TechAbout analyst would pick; they are a rough benchmark, not ground truth.

| # | Brief | Expected | Suggested | Result |
|---|-------|----------|-----------|--------|
| 1 | Multi-tenant inventory SaaS + offline mobile | enterprise-mobile, saas-platforms, enterprise-software, cybersecurity | saas-platforms, web-mobile, enterprise-software, enterprise-mobile, data-analytics | PASS |
| 2 | RAG chatbot for internal knowledge base | ai-ml | ai-ml, cloud-devops | PASS |
| 3 | WordPress to Next.js migration (Express scale) | express-web-migration | web-mobile, data-analytics, express-seo | MISS |
| 4 | Shopify store launch | express-ecommerce | data-analytics, express-ecommerce | PASS |
| 5 | Legacy ERP modernisation | digital-transformation, enterprise-software | enterprise-software, cloud-devops, ai-ml, data-analytics | PASS |
| 6 | Computer vision for quality inspection | ai-ml, iot | ai-ml, iot | PASS |
| 7 | Kubernetes platform & CI/CD | cloud-devops | cloud-devops, enterprise-software, saas-platforms, ai-ml, data-analytics | PASS |
| 8 | SOC 2 Type II readiness | cybersecurity | cybersecurity, cloud-devops, web-mobile, saas-platforms | PASS |
| 9 | Field service mobile app | enterprise-mobile, web-mobile | web-mobile, enterprise-mobile, data-analytics | PASS |
| 10 | Data warehouse & executive dashboards | data-analytics | data-analytics, enterprise-mobile, ai-ml, web-mobile | PASS |
| 11 | Blockchain supply-chain provenance | blockchain | blockchain, enterprise-software, ai-ml | PASS |
| 12 | Website malware cleanup (Express) | express-security | cybersecurity, express-wordpress, express-security | PASS |
| 13 | Multi-brand headless commerce | saas-platforms, web-mobile | saas-platforms, enterprise-software, web-mobile | PASS |
| 14 | IoT cold-chain monitoring | iot | iot, cloud-devops, data-analytics, web-mobile, enterprise-mobile | PASS |
| 15 | Test automation suite for fintech app | qa-automation | qa-automation, web-mobile, ai-ml | PASS |
| 16 | Very short / vague brief | - | enterprise-software | n/a (edge case) |
| 17 | Pure marketing fluff | - | iot, ai-ml | n/a (edge case) |
| 18 | Non-English brief (Urdu mixed) | express-ecommerce | ai-ml, data-analytics | MISS |
| 19 | Healthcare patient portal | enterprise-software, web-mobile, cybersecurity | web-mobile | PASS |
| 20 | AdSense approval rescue | express-seo | cybersecurity, express-seo | PASS |
| 21 | Internal process automation | digital-transformation | enterprise-software, data-analytics, cybersecurity, ai-ml | MISS |
| 22 | Cross-platform MVP for marketplace | web-mobile, saas-platforms | web-mobile, saas-platforms, data-analytics | PASS |
| 23 | Cloud cost optimisation | cloud-devops | data-analytics, cloud-devops, web-mobile | PASS |
| 24 | Document intelligence for contracts | ai-ml | ai-ml, data-analytics | PASS |
| 25 | Empty / minimal | - | - | rejected (422) |
| 26 | Large enterprise multi-workstream | ai-ml, data-analytics, cybersecurity, enterprise-mobile | ai-ml, cybersecurity, enterprise-software, digital-transformation, saas-platforms | PASS |
| 27 | Simple landing page (Express) | web-mobile, express-wordpress | saas-platforms, data-analytics | MISS |
