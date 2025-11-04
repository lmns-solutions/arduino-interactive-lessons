---
lang: bg
permalink: /cpx/cpx-notes.html
page_id: cpx-cpx-notes
layout: default
title: L2&#58; Програмиране на CPX с MakeCode
parent: Платката Circuit Express (CPX)
has_toc: true # (по подразбиране)
comments: true
nav_exclude: true
usetocbot: true
search_exclude: true
---
# {{ page.title | replace_first:"L",'Урок '}}
{: .no_toc }

## Съдържание
{: .no_toc .text-delta }

1. Съдържание
{:toc}
---

Продължение на мозъчната атака:

[Готово] Урок 3: дискретно пиано
[Готово] Урок 4: основен аналогов сензор с конзолно записване и термен [направено]
[Готово] Урок 4 или 5: Може би тук, да се добавят още сензори – току-що добавих още към Урок 4
[Готово] Урок 5: капацитивен сензор + сензорно пиано
- Имайте един капацитивен сензор. Използвайте пространствената клавиша. Накарайте ги да играят Flappy Bird.
- След това покажете по-сложен пример. Можете да споделите нашата Capacitive Touch Playground
- Може би да въведем функция тук?

[Направено] Урок 6: CPX като клавиатура
[Направено] Урок 7: CPX като мишка

Урок 8: резистивни сензори
- Първо използвайте потенциометър и използвайте графика, за да покажете стойността заедно с конзолното логване
- След това може би слайд потенциометър
- След това сензор за налягане
- След това може би сензор за огъване?
- Направете мишката CPX и играйте pong

Урок 9: lofi резистивни сензори
- Lo-fi резистивни сензори
- Референции:
- https://makeabilitylab.github.io/physcomp/electronics/variable-resistors.html#activity-build-your-own-diy-variable-resistor
- Документацията на Adafruit за направата на lo-fi плъзгащ потенциометър:
- https://makecode.adafruit.com/learnsystem/pins-tutorial/analog-input/read-analog

Урок 10: Neopixels

Урок 11: други сензори?
Урок 12: сервомеханизми?

други неща:
- звук като вход / силен звук
- искаме ли да въведем променливи? Ако да, можем да направим прелистване на цветовете https://makecode.com/_WsCHuiTjeUoD
- а инфрачервените? ако направим това, искам да направя дистанционно управление на серво мотор
- https://learn.adafruit.com/infrared-ir-receive-transmit-circuit-playground-express-circuit-python
- https://learn.adafruit.com/circuit-playground-express-laser-tag
- ултразвукови сензори
- Пример: https://youtu.be/NIKu0-Tgh2M?t=3076

----
Урок 1: Нашата първа програма MakeCode
В този урок ще научим как да програмираме CPX с MakeCode, включително:

- Общ преглед на интерфейса на MakeCode
- https://makecode.adafruit.com/courses/maker/general/coding/environment
- https://makecode.adafruit.com/courses/maker/general/load-manage-programs
- Създаване на първата ни програма: blinky
- Използване на симулатора
- Запазване и споделяне на програми
- Игра с Neopixels
- Създаване на първата програма със стартиращ звук и вечна линия
- Може би да имам пълен видеозапис на себе си, докато правя това, и да го публикувам в YouTube?

----
Урок 2: Още светлини и конзолно логване
- Пример за CrossFade с конзолно логване: https://makecode.com/_WsCHuiTjeUoD
- Въвеждане на превключвател, който помага при отстраняването на грешки или не

-----
Урок 3: Взаимодействие, звук и конзолно логване

За начало нека направим проста пиано клавиатура, която светва, когато кликнем върху бутоните

https://makecode.com/_1pPDhAFx55u3

- Да покажем нашата хартиена клавиатура? Подобно на: https://makecode.adafruit.com/courses/maker/projects/music-maker

-----
Урок 3: Сензори?

- Пример за проект: магическа пръчка с ускорение + високоговорител: https://makecode.adafruit.com/projects/magic-wand
- https://learn.adafruit.com/sensors-in-makecode

------
Урок 4: Докосване

- https://makecode.adafruit.com/learnsystem/pins-tutorial/touch-input

-----
Урок 5: Клавиатура и мишка

- Покажете примери

- Какво можем да използваме като мишка? Натискане на бутони? Необходим е аналогов вход. Може да се използва потенциометър (но може би това е за седмица 4?)

-------
Neopixel
- Всеки Neopixel се състои от миниатюрни RGB LED диоди: https://youtu.be/Bo0cM2qmuAE?t=137
- Можем да използваме директния цвят на MakeCode, за да изберем конкретни цветове
- Или да преминаваме през нашите собствени цветове
- Говорете за Neopixel ленти: https://youtu.be/Bo0cM2qmuAE?t=238 в края
- Може би говорете за фотони и писалки и т.н. (вижте https://youtu.be/NIKu0-Tgh2M?t=1338)

ДРУГИ НЕЩА
- А какво ще кажете за хаптиката?
- А какво ще кажете за захранването на вашите проекти: https://makecode.adafruit.com/courses/maker/general/maker-tools-techniques
- Проекти: https://makecode.adafruit.com/projects/
- А какво ще кажете за инфрачервената комуникация?

----

Други неща:
https://makecode.adafruit.com/behind-the-makecode-hardware

----
Акселерометър (зад MakeCode Series): https://www.youtube.com/watch?v=byngcwjO51U.
 
- Чудесно обяснение на акселерометъра тук: https://youtu.be/2HzNKz-QlV0?t=65 (Шон Хаймъл зад MakeCode Hardware)
- Има и блок за събития, който използва Accel: при разклащане, при накланяне нагоре и т.н.
- Накланящо се пиано: https://youtu.be/NIKu0-Tgh2M?t=780 (MakeCode Derek Banas)

----
Серво мотор (Behind MakeCode Series): https://www.youtube.com/watch?v=okxooamdAP4
- Подробен поглед към серво мотора: https://youtu.be/okxooamdAP4?t=183 (а точно преди това се показва как работи DC мотор)
- Серво с MakeCode демо: https://youtu.be/cofElsolYk4
- Готино състезание с мраморни топчета със серво мотори: https://makecode.adafruit.com/courses/maker/projects/marble-run
- https://makecode.adafruit.com/courses/maker/projects/servo-box
- Серво в MakeCode урок от Derek Banas: https://youtu.be/NIKu0-Tgh2M?t=1784

Бутони (серия Behind MakeCode): https://www.youtube.com/watch?v=t_Qujjd_38o
- Ясно изрязан бутон: https://youtu.be/t_Qujjd_38o?t=217

Високоговорител (серия "Зад MakeCode”): https://youtu.be/JjJ-KGwKh_4
-- Хубаво обяснение за високоговорителя тук: https://youtu.be/JjJ-KGwKh_4
-- Създава "Twinkle Twinkle Little Star" тук: https://youtu.be/JjJ-KGwKh_4?t=257

Използване на светлинен сензор за създаване на трипър (Behind MakeCode Series): https://youtu.be/9LrWQ68lO20?t=157
