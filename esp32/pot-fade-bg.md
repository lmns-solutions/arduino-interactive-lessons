---
lang: bg
permalink: /esp32/pot-fade.html
page_id: esp32-pot-fade
layout: default
title: L4&#58; Аналогов вход
parent: ESP32
has_toc: true # (по подразбиране)
usemathjax: true
comments: true
usetocbot: true
nav_order: 4
---
# {{ page.title | replace_first:"L",'Урок '}}
{: .no_toc }

## Съдържание
{: .no_toc .text-delta }

1. Съдържание
{:toc}
---

В този урок ще научим как да използваме аналоговия вход на ESP32, като изградим LED фейдър на базата на потенциометър.

![Анимация на използването на потенциометър за затъмняване на LED на ESP32](assets/movies/Huzzah32_PotFade-optimized.gif)

## Материали

Ще ви са необходими същите материали като в [последния урок](led-fade.md), но също и трим потенциометър 10kΩ.

| Breadboard | ESP32 | LED | Резистор | Trimpot |
| ---------- |:-----:|:-----:|:-----:|
| ![Бретборд]({{ site.baseurl }}/assets/images/Breadboard_Half.png) | ![Huzzah32]({{ site.baseurl }}/assets/images/ESP32Huzzah32_Adafruit_vertical_h200.png) | ![Червен LED]({{ site.baseurl }}/assets/images/RedLED_Fritzing.png) | ![220 Ohm резистор]({{ site.baseurl }}/assets/images/Resistor220_Fritzing.png) | ![Изображение на тримпот 10 kΩ]({{ site.baseurl }}/assets/images/Trimpot_100h.png) | 
| Breadboard | Huzzah32 | Червен светодиод | Резистор 220 Ω | Тримпот 10 kΩ |

## АЦП на ESP32

Чиповете ATmega, използвани от Arduino Uno ([ATmega328](http://ww1.microchip.com/downloads/en/DeviceDoc/Atmel-7810-Automotive-Microcontrollers-ATmega328P_Datasheet.pdf)) и Arduino Leonardo ([ATmega32U4] (http://ww1.microchip.com/downloads/en/DeviceDoc/Atmel-7766-8-bit-AVR-ATmega16U4-32U4_Datasheet.pdf)) имат 10-битови АЦП, които осигуряват аналогово-цифрова резолюция от $$2^{10}=1024$$.
 

За разлика от тях, ESP32 интегрира два **12-битови** АЦП (разделителна способност: $$2^{12}=4096$$), поддържащи общо 18 канала за измерване (аналогови пинове). Официалните документи за ESP32 са [тук](https://docs.espressif.com/projects/esp-idf/en/latest/esp32/api-reference/peripherals/adc.html).

![Huzzah32 диаграма на пиновете](assets/images/AdafruitHuzzah32PinDiagram.png)
ADC пиновете са маркирани в тюркоазено. Кликнете с десния бутон и отворете изображението в нов раздел, за да го увеличите.
{: .fs-1 }

Разпределение на пиновете:
- **ADC1** има 8 канала, свързани с GPIO пинове 32-39, което се превежда като A7 (32), A9 (33), A2 (34), A4 (36) и A3 (39); GPIO пиновете са в скоби. Имайте предвид, че GPIO 35, 37 и 38 не са изложени на Huzzah32.
- **ADC2** има 10 канала, свързани с GPIO 0, 2, 4, 12 - 15 и 25 - 27, което се превежда като A5(4), A11 (12), A12 (13), A6 (14), A8 (15), A1 (25), A0 (26), A10 (27). GPIO пиновете 0, 2 не са изложени на Huzzah32.
 

Така че, общо Huzzah32 има 13 използваеми аналогови входа (A0-A12).

### Ограничения на ADC2
ADC2 има някои ограничения:
1. ADC2 се използва от Wi-Fi драйвера, така че ADC2 може да се използва само когато Wi-Fi драйверът **не** е стартирал.
2. Три от пиновете на ADC2 са пинове за свързване и затова трябва да се използват с повишено внимание. Пиновете за свързване се използват по време на включване/ресет, за да конфигурират режима на стартиране на устройството, работното напрежение и други начални настройки ([link](https://www.esp32.com/viewtopic.php?t=5970)).

Важно е да се отбележи, че официалните [документи](https://learn.adafruit.com/adafruit-huzzah32-esp32-feather/pinouts) на Adafruit за Huzzah32 са объркващи: в тях се посочва, че "можете да четете аналогови входове на ADC #1 само след като WiFi е стартирал". Чрез експерименти и [публикация в Reddit](https://www.reddit.com/r/esp32/comments/gav6mw/huzzah32_pin_diagram_draft/fp1zcz5?utm_source=share& utm_medium=web2x&context=3) установихме, че Adafruit е искал да каже просто, че ADC#2 не е достъпен, след като WiFi е стартирал (така че можете да използвате само ADC#1).

В следващото видео тествам всички 13 аналогови входни пина (`A0` - `A12`) с помощта на трим потенциометър за вход и Serial Plotter за изход. WiFi е изключен и всички пинове работят.

<iframe width="736" height="414" src="https://www.youtube.com/embed/8BBY-5n4e5A" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

## Да направим нещо!

Нека направим LED фейдър на базата на потенциометър.

### Веригата

Веригата е почти същата като в [предишните уроци](led-fade.md); обаче, трябва да добавим и свържем потенциометър. Затова ще изградим две прости вериги:
1. **Входната** верига, използваща потенциометъра, която ще свържем към `A6` (GPIO 14)
2. **Изходна** верига, която е същата като в [предходните уроци](led-fade.md)

![Схема и диаграма на веригата за фейдър на базата на потенциометър](assets/images/Huzzah32_PotFade_CircuitDiagramAndSchematic_Fritzing.png)

### Кодът

Кодът просто адаптира кода за затъмняване на LED от предишния урок, за да използва аналоговата стойност на входа на потенциометъра на `A6` за контрол на PWM цикъла (вместо да се повтаря нагоре и надолу).

Ето нашата реализация на [github](https://github.com/makeabilitylab/arduino/tree/master/ESP32/Basics/PotFade):

<!-- gist-it не работи, затова сега използваме emgithub -->
<!-- <script src="https://gist-it.appspot.com/https://github.com/makeabilitylab/arduino/blob/master/ESP32/Basics/PotFade/PotFade.ino?footer=minimal"></script> -->

<script src="https://emgithub.com/embed.js?target=https%3A%2F%2Fgithub.com%2Fmakeabilitylab%2Farduino%2Fblob%2Fmaster%2FESP32%2FBasics%2FPotFade%2FPotFade.ino&style=github&showCopy=on"></script>

Този [изходен код](https://github.com/makeabilitylab/arduino/blob/master/ESP32/Basics/PotFade/PotFade.ino) се намира в GitHub.
{: .fs-1 }

### Видео от работната маса

Ето видео от работната маса с сериен плотер, който изобразява аналоговата входна стойност от потенциометъра и преобразуваната стойност на работния цикъл, използвана в метода `ledcWrite`.

<iframe width="736" height="414" src="https://www.youtube.com/embed/E5YFtm0CLFY" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

## Следващ урок

В [следващия урок](tone.md) ще научим как да възпроизвеждаме тонове на ESP32.

<!-- В [следващия урок](capacitive-touch-sensing.md) ще научим и ще използваме вградения модул за капацитивно докосване на ESP32. -->

<span class="fs-6">
[Предишен: Затъмняване на LED с ESP32](led-fade.md){: .btn .btn-outline }
[Следващ: Възпроизвеждане на тонове](tone.md){: .btn .btn-outline }
<!-- [Следващ: Капацитивно сензорно докосване с ESP32](capacitive-touch-sensing.md){: .btn .btn-outline } -->
</span>
