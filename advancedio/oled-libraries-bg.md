---
lang: bg
permalink: /advancedio/oled-libraries.html
page_id: advancedio-oled-libraries
layout: default
title: Инсталиране на библиотеки Adafruit OLED
# nav_order: 1
# parent: Изход
# grand_parent: Разширени I/O
has_toc: true # (включено по подразбиране)
comments: true
usemathjax: true
usetocbot: true
nav_exclude: true
---
# {{ page.title }}
{: .no_toc }

## Съдържание
{: .no_toc .text-delta }

1. Съдържание
{:toc}
---

За да използваме OLED дисплея на Adafruit, са ни необходими две библиотеки:

- Библиотеката с драйвери за дисплея [Adafruit_SSD1306](https://github.com/adafruit/Adafruit_SSD1306), която се занимава с комуникацията с дисплея, картирането на паметта и нисконивовите рутинни операции по рисуване
- Графичната библиотека [Adafruit_GFX](https://github.com/adafruit/Adafruit-GFX-Library), която предоставя основни графични процедури за всички дисплеи Adafruit, като рисуване на точки, линии, кръгове. 

За да инсталирате и двете, следвайте инструкциите по-долу:

## Стъпка 1: Отворете "Управление на библиотеки"

Отворете Arduino IDE, след което отидете на `Инструменти -> Управление на библиотеки`.

![](assets/images/ArduinoIDE_ManageLibrariesScreenshot.png)

## Стъпка 2: Търсене на Adafruit SSD1306

В Library Manager (Управление на библиотеки) потърсете "Adafruit SSD1306”. Има и други SSD1306 библиотеки, затова се уверете, че сте намерили тази на Adafruit. На тази екранна снимка текущата версия е 2.4.4, но към април 2024 г. те са на [версия 2.5.9](https://github.com/adafruit/Adafruit_SSD1306/releases).

![](assets/images/ArduinoIDE_LibraryManager_SearchForAdafruitSSD1306.png)

## Стъпка 3: Инсталиране на библиотеката Adafruit SSD1306
Кликнете върху бутона "Инсталирай".

![](assets/images/ArduinoIDE_LibraryManager_ClickInstallAdafruitSSD1306.png)

## Стъпка 4: Инсталиране на всички зависимости

Библиотеката Adafruit SSD1306 зависи от две други библиотеки, които също трябва да инсталираме. За щастие, Library Manager открива това и изрично пита за зависимостите. Изберете "Инсталирай всички".

![](assets/images/ArduinoIDE_LibraryManager_AdafruitSSD1306Dependencies.png)

<!-- Библиотечният мениджър на Arduino IDE позволява на дизайнерите на библиотеки да идентифицират други зависимости на библиотеки в техните метаданни. Това позволява на IDE да пита потребителите за зависимостите автоматично. -->

## Стъпка 5: Потвърдете инсталирането

Ако библиотеката SSD1306 е инсталирана правилно, до нея трябва да видите синьо-зелен етикет "INSTALLED", както е показано по-долу:

![](assets/images/ArduinoIDE_LibraryManager_SSD1306Installed.png)

## Местоположение на папката за инсталиране на библиотеката в операционната система

Всички библиотеки се инсталират в папката "Документи" на вашата операционна система. Полезно е да знаете местоположението на тази директория, в случай че искате да инсталирате библиотека ръчно (като [Makeability Lab Arduino Library](https://github.com/makeabilitylab/arduino/tree/master/MakeabilityLab_Arduino_Library)) или искате да видите изходния код на библиотеката.
 

В зависимост от операционната ви система, можете да видите инсталираната папка "libraries" на Arduino във вашата файлова система тук:

- В Windows, по подразбиране това е "C:\Users\<username>\Documents\Arduino\libraries"
- В Mac, "/Users/<username>/Documents/Arduino/libraries"

| Директория на библиотеката Arduino в Windows | Директория на библиотеката Arduino в Mac |
|:------------------------------------:|:------------------------------- -:|
| ![](assets/images/Arduino_LibraryDirectory_Windows.png) | ![](assets/images/Arduino_LibraryDirectory_Mac.png) |

Ще забележите, че папката "libraries" съдържа сурови изходни файлове, а **не** предварително компилирани бинарни файлове. Arduino IDE компилира основните библиотечни файлове по различен начин в зависимост от избраната платка.

## Върнете се към урока за OLED

Сега се върнете към [урока за OLED](oled.md) и започнете да свързвате дисплея си!

