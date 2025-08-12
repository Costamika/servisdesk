# ⚡ Быстрое развертывание в локальной сети

## 🎯 3 способа развертывания

### 1. **Автоматическое развертывание (рекомендуется)**
```bash
# Создать пакет развертывания
./create_deployment_package.sh 1.0.0

# Развернуть на сервере
./deploy_local.sh 192.168.1.100
```

### 2. **Docker развертывание**
```bash
# На сервере
docker-compose up -d
```

### 3. **Ручное развертывание**
Следуйте инструкциям в `LOCAL_DEPLOYMENT.md`

## 📋 Требования к серверу

- **ОС**: Ubuntu 20.04+ / Debian 11+
- **RAM**: 2GB минимум
- **Диск**: 10GB свободного места
- **Сеть**: SSH доступ с правами root

## 🚀 Пошаговое развертывание

### Шаг 1: Подготовка
```bash
# На локальной машине
./create_deployment_package.sh 1.0.0
```

### Шаг 2: Развертывание
```bash
# Автоматическое развертывание
./deploy_local.sh 192.168.1.100
```

### Шаг 3: Проверка
```bash
# Проверить доступность
curl -I http://192.168.1.100/

# Войти в систему
# URL: http://192.168.1.100
# Логин: admin
# Пароль: admin123
```

## 🔧 Управление системой

### На сервере:
```bash
# Статус
systemctl status servisdesk

# Управление
servisdesk-manage start
servisdesk-manage stop
servisdesk-manage restart
servisdesk-manage status
servisdesk-manage logs

# Резервное копирование
servisdesk-manage backup
```

### Обновление:
```bash
# Автоматическое обновление
servisdesk-update

# Ручное обновление
systemctl stop servisdesk
git pull origin main
pip install -r requirements.txt
python manage.py migrate --settings=servisdesk.settings_production
python manage.py collectstatic --noinput --settings=servisdesk.settings_production
systemctl start servisdesk
```

## 🌐 Доступ к системе

- **URL**: http://192.168.1.100
- **Администратор**: admin / admin123
- **Пользователи**: ivanov / user123, petrova / user123, sidorov / user123

## 📊 Мониторинг

```bash
# Логи приложения
journalctl -u servisdesk -f

# Логи Nginx
tail -f /var/log/nginx/error.log

# Статус процессов
ps aux | grep gunicorn
ps aux | grep nginx
```

## 🔐 Безопасность

1. **Измените пароль администратора** после первого входа
2. **Настройте файрвол** (уже настроен автоматически)
3. **Ограничьте доступ** только из локальной сети
4. **Настройте резервное копирование**

## 🆘 Устранение неполадок

### 502 Bad Gateway:
```bash
systemctl status servisdesk
nginx -t
chown -R servisdesk:servisdesk /opt/servisdesk
```

### Статические файлы не загружаются:
```bash
python manage.py collectstatic --noinput --settings=servisdesk.settings_production
```

### Ошибки базы данных:
```bash
python manage.py migrate --settings=servisdesk.settings_production
```

## 📞 Поддержка

- **Документация**: `LOCAL_DEPLOYMENT.md`
- **Примеры**: `USAGE_EXAMPLE.md`
- **Быстрый старт**: `QUICK_START.md`

---

**🎉 Система готова к использованию!**
