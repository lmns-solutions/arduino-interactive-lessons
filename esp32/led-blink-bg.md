---
lang: bg
permalink: /esp32/led-blink.html
page_id: esp32-led-blink
layout: default
title: L2&#58; Мигане на LED
parent: ESP32
has_toc: true # (по подразбиране)
usemathjax: true
comments: true
usetocbot: true
nav_order: 2
---
# {{ page.title | replace_first:"L",'Урок '}}
{: .no_toc }

## Съдържание
{: .no_toc .text-delta }

1. Съдържание
{:toc}
---

В този урок ще преразгледаме стария [урок за мигане](../arduino/led-blink.md) от поредицата [Въведение в изхода](../arduino/intro-output.md), но с **ESP32**.

![Анимация на Blink на ESP32](assets/movies/Huzzah32_Blink-optimized.gif)

## Материали

Всички наши примери за ESP32 ще използват Huzzah32, но всяка ESP32 платка ще работи, стига да сте инсталирали подходящата Arduino библиотека в Arduino IDE. Освен това, ако не използвате Huzzah32, пиновете също ще бъдат различни, така че се консултирайте с вашата специфична диаграма на пиновете.

| Breadboard | ESP32 | LED | Резистор |
| ---------- |:-----:|:-----:|:-----:|
| ![Breadboard]({{ site.baseurl }}/assets/images/Breadboard_Half.png) | ![Huzzah32]({{ site.baseurl }}/assets/images/ESP32Huzzah32_Adafruit_vertical_h200.png) | ![Червен LED]({{ site.baseurl }}/assets/images/RedLED_Fritzing.png) | ![220 Ohm резистор]({{ site.baseurl }}/assets/images/Resistor220_Fritzing.png) |
| Breadboard | Huzzah32 | Червен LED | 220Ω резистор |

## Верига

ESP32 има голям брой пинове и всеки от тях може да се използва за множество функции. Затова е важно да имате лесно достъпна диаграма на пиновете. Препоръчваме да я разпечатате (обикновено раздаваме такива диаграми в нашите курсове). Ако нямате принтер, препоръчваме да отворите диаграмата на втори монитор или да я държите наблизо.

![Диаграма на пиновете на Huzzah32](assets/images/AdafruitHuzzah32PinDiagram.png)
За подробности вижте Adafruit Huzzah32 [docs](https://learn.adafruit.com/adafruit-huzzah32-esp32-feather/pinouts). Кликнете с десния бутон и отворете изображението в нов раздел, за да го увеличите и отпечатате.
{: .fs-1 }

### Изграждане на веригата

Нашата верига е толкова проста, колкото може да бъде.

![Верига, показваща LED, свързан с GPIO #21 чрез резистор за ограничаване на тока](assets/images/Huzzah32_Blink_CircuitDiagramAndSchematic_Fritzing.png)

Поставянето на Huzzah32 в платка за прототипи може да отнеме известно усилие. Моля, внимавайте да не огънете пиновете при поставянето и изваждането на платка. Тъй като Huzzah32 заема много място, може да обмислите да използвате платка за прототипи с пълен размер, вместо такава с половин размер.

Имайте предвид, че все още използваме резистор 220Ω, точно като в оригиналния [урок за мигане](../arduino/led-blink.md). Но сега използваме платка 3,3V, а не 5V (като Uno или Leonardo), така че ще доставяме по-малко ток с една и съща стойност на резистора. За да получим прогнозирания ток в нашата верига, приемете ~2V напрежение в права посока ($$V_f$$) за червен LED. По този начин, 

$$I=V/R \\
I = \frac{V_{cc} - V_f}{R} \\
I = \frac{3.3V - 2V}{220Ω} \\
I = 5.9mA$$

## Код

Кодът е същият като в оригиналния урок на Arduino [Blink lesson](../arduino/led-blink.md) (предупреждаваме ви: той няма да е за урока [fade](led-fade.md)). Трудното тук е просто да направите правилното окабеляване и да разберете кои пинове съответстват на какво!

Тъй като това трябва да е преговор, опитайте се да напишете Blink имплементация, без да се консултирате с нашето решение по-долу. Можете да го направите!

<!-- https://github.com/makeabilitylab/arduino/blob/master/ESP32/Basics/Blink/Blink.ino -->

<!-- gist-it не работи, затова сега използваме emgithub -->
<!-- <script src="https://gist-it.appspot.com/https://github.com/makeabilitylab/arduino/blob/master/ESP32/Basics/Blink/Blink.ino?footer=minimal"></script> -->

<script src="https://emgithub.com/embed.js?target=https%3A%2F%2Fgithub.com%2Fmakeabilitylab%2Farduino%2Fblob%2Fmaster%2FESP32%2FBasics%2FBlink%2FBlink.ino&style=github&showCopy=on"></script>

Този [изходен код](https://github.com/makeabilitylab/arduino/blob/master/ESP32/Basics/Blink/Blink.ino) се намира в GitHub.
{: .fs-1 }

## Видео

![Анимация на Blink на ESP32](assets/movies/Huzzah32_Blink-optimized.gif)

<!-- TODO: вмъкване на видео от Workbench -->

## Следващ урок

В [следващия урок](led-fade.md) ще научим как да използваме "аналоговия изход” на ESP32, за да регулираме яркостта на LED диода. Това е подобно на нашия оригинален урок за Arduino [LED fade](../arduino/led-fade.md), но няма да използваме `analogWrite`!

<span class="fs-6">
[Предишен: Въведение в ESP32](esp32.md){: .btn .btn-outline }
[Следващ: Използване на PWM на ESP32](led-fade.md){: .btn .btn-outline }
</span>
