# Mixpanel Connector — Connector Discovery

**Vendor API Baseline:** https://mixpanel.com

## Архитектура API
- **Базовый адрес:** `https://mixpanel.com/api/2.0`
- **Протокол:** REST / HTTPS (JSON)
- **Аутентификация:** Service Account Username + Secret (Basic Auth)
- **Ключевые эндпоинты:**
  - профили пользователей (/engage)
  - события (/track)
  - когорты (/cohorts)
  - воронки (/funnels)
- **Тестовая точка проверки подключения:** `GET /api/app/me`.
