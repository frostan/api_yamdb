# Проект YAMDB
Проект YaMDb собирает отзывы пользователей на произведения, они делятся на категории.
Произведению может быть присвоен жанр из списка предустановленных.

Аутетифицированые пользователи могут оставить к произведениям отзывы и ставить оценку в диапазоне от одного до десяти; из пользовательских оценок формируется усреднённая оценка произведения — рейтинг. На одно произведение пользователь может оставить только один отзыв.

Пользователи могут добавлять отзывы и комментарии, а так же оставлять комментарии к отзывам.


Только администратор может добавлять произведения, категории и жанры

---

# API для проекта YAMDB
* Сериализация данных для всех моделей проекта:
   * Title - Произведения
   * Genre - Жанры
   * Review - Отзывы
   * Comment - Комментарии

* Написана модель CustomUser c ролями:
   * Администратор
   * Модератор
   * Пользователь

* Аутентицикация пользователей по JWT-токену
* Предоставляет данные в JSON-формате
* Обрабатываются GET, POST, PATCH, DELETE запросы к бд.



## Стек технологий:

![Static Badge](https://img.shields.io/badge/Python-3.8-green)
![Static Badge](https://img.shields.io/badge/Django-green)
![Static Badge](https://img.shields.io/badge/REST_framework-red)
![Static Badge](https://img.shields.io/badge/Simple_JWT-blue)
![Static Badge](https://img.shields.io/badge/SQLite-blue)
---

##### Документация проекта http://127.0.0.1:8000/redoc/

# Как запустить проект:

### Клонируйте репозиторий и перейдите в корневую папку проекта:

```
git clone https://github.com/frostan/api_yamdb.git

cd api_yamdb
```

### Создайте и активируйте вирутальное окружение:


```
python3 -m venv venv

source venv/bin/activate
```

### Установите зависимости:

```
pip install -r requirements.txt
```
<sub>при необходимости обновите менеджер командой:</sub>
```
pip install --upgrade pip
```

### Выполните миграции:

```
python3 manage.py migrate
```

### Запустите проект:

```
python3 manage.py runserver
```
---
## Примеры:
![Static Badge](https://img.shields.io/badge/GET-1fa7)
![Static Badge](https://img.shields.io/badge/POST-00BFFF)
![Static Badge](https://img.shields.io/badge/PATCH-FF8C00)
![Static Badge](https://img.shields.io/badge/DEL-FF0000)

### Получение всех записей:

![Static Badge](https://img.shields.io/badge/GET-1fa7)```http://127.0.0.1:8000/api/v1/titles/```

##### Ответ:```200```
```
{
  "count": 0,
  "next": "string",
  "previous": "string",
  "results": [
    {
      "id": 0,
      "name": "string",
      "year": 0,
      "rating": 0,
      "description": "string",
      "genre": [
        {
          "name": "string",
          "slug": "^-$"
        }
      ],
      "category": {
        "name": "string",
        "slug": "^-$"
      }
    }
  ]
}
```

![Static Badge](https://img.shields.io/badge/POST-00BFFF)```http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/```

##### Ответ:```201```
```
{
  "id": 0,
  "text": "string",
  "author": "string",
  "score": 1,
  "pub_date": "2019-08-24T14:15:22Z"
}
```

![Static Badge](https://img.shields.io/badge/PATCH-FF8C00)```http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/```

##### Ответ:```200```
```
{
  "id": 0,
  "text": "string",
  "author": "string",
  "pub_date": "2019-08-24T14:15:22Z"
}
```


![Static Badge](https://img.shields.io/badge/DEL-FF0000)```http://127.0.0.1:8000/api/v1/users/{username}/```

##### Ответ:```404```
```
```



### Авторы проекта:
```
https://github.com/krympyr
https://github.com/Unga62
https://github.com/frostan
```