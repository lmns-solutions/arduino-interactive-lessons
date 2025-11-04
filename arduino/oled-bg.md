---
lang: bg
permalink: /arduino/oled.html
page_id: arduino-oled
layout: default
title: L1&#58; Включване на OLED
nav_order: 1
parent: Разширени изходи
grand_parent: Въведение в Arduino
usemathjax: true
has_toc: true # (по подразбиране)
comments: true
nav_exclude: true
usetocbot: true
search_exclude: true
---

<!-- обмислете добавянето на родител "Разширено Arduino" или Разширено I/O -->

Тези инструкции са за [графичния дисплей Adafruit 128x64 OLED](https://www.adafruit.com/product/938). Можете да следвате официалното [упътване на Adafruit тук](https://learn.adafruit.com/monochrome-oled-breakouts/arduino-library-and-examples).

## Инсталиране на библиотеки Arduino

### Стъпка 1: Отворете Manage Libraries (Управление на библиотеки) в менюто на файловете на Arduino IDE

![Снимка на екрана при избор на Tools->Manage Libraries... (Инструменти->Управление на библиотеки...) от менюто на файловете на Arduino IDE](assets/images/ArduinoIDE_InstallLibraries.png)

### Стъпка 2: Търсене и инсталиране на Adafruit SSD1306

Търсете и инсталирайте библиотеката Adafruit SSD1306.

![Снимка на екрана при търсене на библиотеката Adafruit SSD1306 в мениджъра на библиотеки на Arduino IDE](assets/images/ArduinoIDE_InstallSSD1306Library.png)

### Стъпка 3: Инсталиране на всички зависимости
Когато бъдете попитани, инсталирайте всички зависимости на библиотеката SSD1306:

![](assets/images/ArduinoIDE_InstallAllSSD1306Dependencies.png)

## Заредете и изпълнете примерния код

След като библиотеката SSD1306 и зависимостите са инсталирани, свържете и тествайте дисплея, използвайки примерния код `ssd1306_128x64`.

![Снимка на екрана при използване на менюто на Arduino IDE за зареждане на примера за код SSD1306](assets/images/ArduinoIDE_LoadingSSD1306SampleCode.png)

## Ресурси:
- https://learn.adafruit.com/monochrome-oled-breakouts/overview
- https://lastminuteengineers.com/oled-display-arduino-tutorial/
- https://learn.adafruit.com/adafruit-gfx-graphics-library/graphics-primitives

## SPI срещу I2C
- SPI е много по-бърз: https://www.youtube.com/watch?v=SvOX-xs9v8M
 

