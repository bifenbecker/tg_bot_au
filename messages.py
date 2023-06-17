START_COMMAND_HELLO = """
Приветствуем тебя, Юрист!

Это бот помогает найти Арбитражных управляющих для вашей процедуры банкротства
физического лица по нужным вам параметрам и из нужного вам региона. Или найти
клиентов на банкротство для юристов и АУ!

Мы собрали лучшие команды по арбитражному управлению, которые предоставляют гарантии на:

●  Завершение процедуры строго в срок
●  Снятие ПМ ежемесячно без задержек
●  Защиту спасенного вами имущества

В сервис входит бесплатное обсуждение стратегии по каждому банкроту!

Если вы ищете клиентов на банкротство, то данный бот также поможет их вам найти.

"""

START_COMMAND_DESCRIPTION = """
Чтобы воспользоваться сервисом, выберите опцию из меню или воспользуйтесь навигацией:
> Найти арбитражного управляющего для долгой работы (/partner)
> Найти арбитражного управляющего для конкретного банкрота (/bfl)
> Я сам АУ (или юрист) и мне нужны клиенты на бфл! (/lead)
"""

PARTNER_SET_REGION_NAME = """
*Напишите ваш регион*, согласно справочной информации
_Например, Краснодарский край, или Республика Адыгея_
Если вы работаете в нескольких регионах или по всей России, напишите Россия, или регион, где вам проще всего будет вести переговоры
"""

PARTNER_SET_AMOUNT_DEALS = """
*Укажите примерный объем дел*, который вы подаете в суд ежемесячно (можно примерно)
_Например, до 5, до 10, до 20, до 50, более 50
Варианты ответов кнопками:_
"""

PARTNER_SET_AMOUNT_EXPENSE = """
Отлично! Укажите какую сумму вы готовы тратить на *расходы арбитражного
управляющего, его услуги*, и *гарантии снятия ПМ и завершения процедур без задержек*
(_депозит включаем в сумму_)

_Например, до 50 000 руб., до 60 000 руб., до 70 000 руб. (включаем депозит в эту сумму)._

*Как формируется стоимость*: 25 000 депозит, 15 000 публикации, 15 000 работа = 55 000 рублей

Напоминаем, что *дешевые цены выставляют только молодые АУ*, которые могут
наделать ошибок. Проверенные управляющие с опытом и командой несут расходы на
зарплату специалистов, но _дают гарантии на качество ведения процедуры_ Не выбирайте
слишком низкую цену!

_Варианты ответов кнопками_:
"""

PARTNER_SET_GUARANTEES = """
Отлично! *Мы нашли в базе несколько вариантов*. Почти готово!
*Укажите нужны ли вам гарантии* на снятие ПМ в срок и завершение процедур без задержек?
Это сильно влияет на цену и поиск АУ! *Не каждый АУ дает такие гарантии.*

Варианты ответов кнопками:
"""

PARTNER_SET_EXPERIENCE = """
Последний этап поиска
*Укажите опыт арбитражного управляющего* в завершенных делах, который вас бы
устроил. Помните, что чем выше опыт, тем обычно дороже услуги (но не всегда)

Варианты ответов кнопками:
"""

PARTNER_FINAL = """
Отлично! *Мы собрали всю нужную нам информацию* и готовы предоставить вам
кандидатов. Информация будет преобразована в pdf и отправлена вам в личные сообщения
в скором времени!

Пока вы ожидаете результаты поиска, хотим предложить вам возможность рассмотреть
*получение клиентов на банкротство*, собранных аналогичным методом!

Подробнее на сайте https://myforce.ru/lidy-na-bankrotstvo 
"""