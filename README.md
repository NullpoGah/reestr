# Сбор сведений о ПО с сайта оператора реестра российских программ для электронных вычислительных машин и баз данных в информационно-телекоммуникационной сети «Интернет»
---
Простой скрипт для сбора данных о ПО с сайта реестра министерства связи https://reestr.minsvyaz.ru
---
**Скрипт собирает информацию о:**
* Название ПО
* Название организации
* ФИО владельца (при наличии)
* ИНН организации/владельца
* Сайт организации
* Альтернативное название продукта
* Класс ПО

---
## Сведения о скрипте
Скрипт использует библиотеки Pandas, requests, BeautifulSoup.
---
Вся юридическая информация записывается в файл Excel.
---
Собранные данные на момент января 2019 года присутсвуют в корневой папке проекта.
Данная информация может быть актуальна при наличии задач о поиске программного обеспечения,
в качестве замены импортного ( в качестве импорт замещения)
