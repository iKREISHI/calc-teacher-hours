# Расчет почасовки преподавателей ШГПУ

Для работы веб-приложения нужно прописать подключение к базе данных университета в `.env`:
```bash
# Main PostgreSQL Database Configuration
DB_NAME=main-db
DB_USER=user
DB_PASSWORD=password123
DB_HOST=localhost
DB_PORT=5433

# Read-Only PostgreSQL Database Configuration
DB_NAME_RO=schedule
DB_USER_RO=test
DB_PASSWORD_RO=test123
DB_HOST_RO=localhost
DB_PORT_RO=5435
```