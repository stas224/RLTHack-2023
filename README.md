# RLT.Hack 2023
&emsp;
**Наша команда "Симпы МИСИС" стала финалистом данного хакатона, заняв 4 место в общем списке** <br /> 

- Тема хакатона: Создание системы интеллектуального поиска потенциальных участников закупок на открытом рынке <br />
- В своей команде я отвечал за парсинг данных для модели машинного обучения <br />
- В общей сложности получилось достать более ***100 000*** наименований товаров с сопутствующими им характеристиками, после чистки данных осталось около 35 тысяч строк<br />
- В данном репозитории представлена только часть проекта, посвященная парсингу данных с сайтов поставщиков

### Используемый стэк технологий:
- Python==3.11 <br />
- bs4==0.0.1 <br />
- requests==2.31.0 <br />
- selenium==4.13.0 <br />
- selenium-stealth==1.0.6 <br />
- fake-useragent==1.3.0 <br />
- pandas==2.1.1 <br />

### Краткое описание 
- Были выбраны такие сайты, как [pulscen.ru](https://msk.pulscen.ru/), [b2b.trade.ru](http://b2btrade.ru/), [supl.biz](https://supl.biz/), [spark-interfax.ru](https://spark-interfax.ru/search), [b2b-center.ru](https://www.b2b-center.ru/) и [rusprofile.ru](https://www.rusprofile.ru/)
- Для первых трех сайтов запускается скрипт из `main.py`, который собирает такие фичи как название товара, поставщик, регион, описание товара и его цена, после чего сопостовляется ИНН поставщиков с сайта spark-interfax.ru
- в скрипте `additional_parsers/parser_b2bcenter.py` собирается информация с b2b-center только о поставщиках и их регионах
- В скрипте `additional_parsers/parser_rusprofile.py` собирается информация с rusprofile о надежности поставщика и отзывы о нем

  

