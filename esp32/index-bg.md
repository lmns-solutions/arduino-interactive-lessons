---
lang: bg
permalink: /esp32/index.html
page_id: esp32-index
layout: default
title: ESP32
nav_order: 6
has_toc: false # включено по подразбиране
has_children: true
nav_exclude: false
usetocbot: true
---
# {{ page.title }}
{: .no_toc }

## Съдържание
{: .no_toc .text-delta }

1. Съдържание
{:toc}
---

![Колаж от ESP32 платки](assets/images/ESP32Variants_FromS1-S3.png)
**Фигура.** [ESP32](https://www.espressif.com/en/products/socs/esp32) бързо се превърна в **най-популярната** платформа за изучаване и използване в проекти за Интернет на нещата (IoT). ESP32 са бързи, имат WiFi и Bluetooth, а много от тях струват около 10 щатски долара! А най-хубавото е, че можете да ги програмирате с Arduino! Така че всичко, което сте научили от [предишните уроци](../arduino/index.md), може да се приложи тук!
{: .fs-1 }

Тези уроци са интерактивни и са предназначени да се завършват **поред**. Целият код на ESP32 е с отворен код и се намира в това [GitHub хранилище](https://github.com/makeabilitylab/arduino/tree/master/ESP32).

{: .note }
Ако посещавате нашия уебсайт за първи път, добре дошли 👋🏽! Следващите уроци за ESP32 предполагат, че сте завършили и двете ни серии от уроци [Въведение в електрониката](../electronics/index.md) и [Въведение в Arduino](../arduino/index.md). Макар да не е абсолютно необходимо, препоръчваме ви да започнете оттам!

<!-- TODO: добавете тук линк към веригите на Tinkercad... -->

## [Урок 1: Въведение в ESP32](esp32.md)

В [този урок](esp32.md) ще научите за ESP32, как се различава от платформата Arduino и как се свързва с нея, както и как да програмирате и използвате платка Huzzah32 ESP32.

## [Урок 2: Мигане на LED](led-blink.md)

Въвежда как да програмирате ESP32, използвайки Arduino IDE и библиотеката ESP32 Arduino ([линк](led-blink.md))

## [Урок 3: Затъмняване на LED с PWM](led-fade.md)

В този [урок](led-fade.md) ще научите как да използвате PWM изхода на ESP32, за да затъмнявате и изключвате LED. Библиотеката ESP32 Arduino не разполага с метод `analogWrite`, затова ще научите как да използвате PWM чрез алтернативен метод.

## [Урок 4: Аналогов вход](pot-fade.md)

В този [урок](pot-fade.md) ще научите как да използвате аналоговия вход на ESP32, като създадете LED фейдър на базата на потенциометър.

## [Урок 5: Възпроизвеждане на тонове](tone.md)

Методът [`tone()`](https://www.arduino.cc/reference/en/language/functions/advanced-io/tone/) на Arduino не се поддържа на ESP32. В този [урок](tone.md) ще научите как да възпроизвеждате тонове, използвайки `ledcWriteTone` и `ledcWriteNote` в [esp32-hal-ledc.c](https://github.com/espressif/arduino-esp32/blob/master/cores/esp32/esp32-hal-ledc.c).

## [Урок 6: Капацитивно докосване](capacitive-touch-sensing.md)

ESP32 има вградена схема и софтуер за капацитивно докосване ([docs](https://github.com/espressif/esp-iot-solution/blob/master/documents/touch_pad_solution/touch_sensor_design_en.md#1-introduction-to-touch-sensor-system)). В [този урок](capacitive-touch-sensing.md) ще използваме функцията за сензорно докосване, за да включим LED.

## [Урок 7: Интернет на нещата](iot.md)

ESP32 е вълнуващ не само заради скоростта, паметта и GPIO възможностите си, но и защото е истинска модерна платка за интернет на нещата (IoT) с Wi-Fi и Bluetooth поддръжка. В този урок ще научим как да използваме WiFi и IoT платформата [Adafruit IO](https://learn.adafruit.com/welcome-to-adafruit-io), за да качваме данни от сензори в реално време.
