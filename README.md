# flask_token
-  Python приложение редактирования пользователей: Сайт для просмотра списка пользователей, просматривать список можно на соответсвующей вкладке только зарегистрированным пользователям Тем, кто не зарегистрирован, просмотр недоступен. Редактировать и создавать пользователей может только администратор
- Регистрировать новых пользователей может только администратор 
- Токен авторизация

Для старта проекта нужно:

Установить пайтон, postgres и необходимые библиотеки из requirement
Создать в postgres БД с именем postgres и привязать ее к питоновскому проекту, обычно IDE делает это автоматически
Запустить в терминале python new_db.py который создаст таблицу и администратора "admin",почтой 'admin@admin.com', и паролем '1'
Запускаем фласк
