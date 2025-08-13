# 🚀 Публикация проекта на GitHub

## 📋 Пошаговая инструкция

### **1. Настройка Git (если еще не настроен)**

```bash
# Настройте ваше имя и email
git config --global user.name "Ваше Имя"
git config --global user.email "your.email@example.com"

# Проверьте настройки
git config --list
```

### **2. Создание репозитория на GitHub**

1. Перейдите на [GitHub](https://github.com)
2. Нажмите кнопку "New repository" (зеленый плюс)
3. Заполните форму:
   - **Repository name**: `servisdesk`
   - **Description**: `Сервис-деск система на Django с автоматическим развертыванием`
   - **Visibility**: Public (или Private)
   - **Initialize with**: НЕ ставьте галочки (у нас уже есть файлы)
4. Нажмите "Create repository"

### **3. Подключение к GitHub репозиторию**

```bash
# Добавьте удаленный репозиторий (замените YOUR_USERNAME на ваше имя пользователя)
git remote add origin https://github.com/YOUR_USERNAME/servisdesk.git

# Проверьте подключение
git remote -v
```

### **4. Первый коммит и отправка**

```bash
# Создайте первый коммит
git commit -m "Initial commit: Complete servisdesk system with deployment scripts"

# Отправьте в GitHub
git push -u origin master
```

### **5. Настройка ветки main (опционально)**

```bash
# Переименуйте ветку master в main (современный стандарт)
git branch -M main

# Отправьте ветку main
git push -u origin main
```

## 🔧 Дополнительные настройки

### **Настройка SSH ключей (рекомендуется)**

```bash
# Генерируйте SSH ключ
ssh-keygen -t ed25519 -C "your.email@example.com"

# Добавьте ключ в ssh-agent
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519

# Скопируйте публичный ключ
cat ~/.ssh/id_ed25519.pub
```

Затем добавьте ключ в GitHub:
1. Перейдите в Settings → SSH and GPG keys
2. Нажмите "New SSH key"
3. Вставьте скопированный ключ

### **Использование SSH вместо HTTPS**

```bash
# Измените URL репозитория на SSH
git remote set-url origin git@github.com:YOUR_USERNAME/servisdesk.git
```

## 📝 Настройка GitHub Pages (опционально)

Если хотите создать сайт проекта:

1. Перейдите в Settings → Pages
2. Source: Deploy from a branch
3. Branch: main
4. Folder: / (root)
5. Нажмите Save

## 🏷️ Создание релизов

### **Создание тега**

```bash
# Создайте тег для версии
git tag -a v1.0.0 -m "Release version 1.0.0"

# Отправьте тег
git push origin v1.0.0
```

### **Создание релиза на GitHub**

1. Перейдите в Releases
2. Нажмите "Create a new release"
3. Выберите тег v1.0.0
4. Заполните описание
5. Нажмите "Publish release"

## 🔄 Обновление репозитория

```bash
# Добавьте изменения
git add .

# Создайте коммит
git commit -m "Update: описание изменений"

# Отправьте изменения
git push origin main
```

## 📚 Полезные команды

```bash
# Проверить статус
git status

# Посмотреть историю коммитов
git log --oneline

# Посмотреть ветки
git branch -a

# Переключиться на ветку
git checkout branch-name

# Создать новую ветку
git checkout -b new-feature

# Объединить изменения
git merge branch-name
```

## 🎯 Готово!

После выполнения всех шагов ваш проект будет доступен по адресу:
```
https://github.com/YOUR_USERNAME/servisdesk
```

## 📋 Чек-лист

- [ ] Настроен Git (имя и email)
- [ ] Создан репозиторий на GitHub
- [ ] Подключен удаленный репозиторий
- [ ] Выполнен первый коммит
- [ ] Код отправлен в GitHub
- [ ] Настроены SSH ключи (опционально)
- [ ] Создан первый релиз (опционально)

---

**🎉 Проект успешно опубликован на GitHub!**
