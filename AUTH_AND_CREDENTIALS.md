# Mixpanel Connector — Auth & Credentials Standard

**Compliance:** AUTH_AND_CREDENTIALS_STANDARD.md (B1–B10)

## Схема аутентификации
- **Метод:** Service Account Username + Secret (Basic Auth)
- **Хранение:** Секреты сохраняются изолированно в хранилище секретов платформы Imperal.
- **Валидация:** При сохранении ключа выполняется тестовый запрос `GET /api/app/me`.
- **Отключение:** Удаление локальных ключей без воздействия на аккаунт вендора.
