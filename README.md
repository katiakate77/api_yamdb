Проект YaMDb
=================

### О проекте (backend + создание API с использованием Django REST Framework)

Проект YaMDb собирает отзывы пользователей на произведения.
* Произведения делятся на категории, такие как «Книги», «Фильмы», «Музыка». Список категорий может быть расширен (например, можно добавить категорию «Изобразительное искусство»).
* Произведению может быть присвоен жанр из списка предустановленных (например, «Сказка», «Рок»).
* Добавлять произведения, категории и жанры может только администратор.
* Пользователи оставляют к произведениям текстовые отзывы и ставят произведению оценку в диапазоне от одного до десяти; из пользовательских оценок формируется рейтинг. На одно произведение пользователь может оставить только один отзыв.
* Пользователи могут оставлять комментарии к отзывам.
* Добавлять отзывы, комментарии и ставить оценки могут только аутентифицированные пользователи.

### Запуск проекта


* Клонировать репозиторий:

```
git clone https://github.com/katiakate77/api_yamdb.git
```

* В папке с репозиторием создать виртуальное окружение и активировать его:

```
python3 -m venv venv
```

```
source venv/bin/activate
```

* Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

* Выполнить миграции:

```
python3 manage.py migrate
```

* Запустить проект:

```
python3 manage.py runserver
```

### Документация

http://localhost:8000/redoc/

### Дополнительные возможности

Реализована management-команда, добавляющая данные в БД из файлов `csv`.
