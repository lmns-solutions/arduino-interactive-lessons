---
lang: bg
permalink: /esp32/capacitive-touch-sensing.html
page_id: esp32-capacitive-touch-sensing
layout: default
title: L6&#58; Капацитивно докосване
parent: ESP32
has_toc: true # (по подразбиране)
usemathjax: true
comments: true
usetocbot: true
nav_order: 6
---
# {{ page.title | replace_first:"L",'Lesson '}}
{: .no_toc }

## Съдържание
{: .no_toc .text-delta }

1. Съдържание
{:toc}
---

ESP32 има вградена схема и софтуер за капацитивно сензорно докосване ([docs](https://github.com/espressif/esp-iot-solution/blob/master/documents/touch_pad_solution/touch_sensor_design_en.md#1-introduction-to-touch-sensor-system)). В този урок ще използваме функцията за сензорно докосване, за да включим светодиод.

## Материали

Ще ви са необходими следните материали:

| Breadboard | ESP32 | LED | Резистор |
| ---------- |:-----:|:-----:|:-----:|
| ![Бретборд]({{ site.baseurl }}/assets/images/Breadboard_Half.png) | ![Huzzah32]({{ site.baseurl }}/assets/images/ESP32Huzzah32_Adafruit_vertical_h200.png) | ![Червен LED]({{ site.baseurl }}/assets/images/RedLED_Fritzing.png) | ![220 Ohm резистор]({{ site.baseurl }}/assets/images/Resistor220_Fritzing.png) |
| Breadboard | Huzzah32 | Червен LED | 220Ω резистор |

## Система за сензори за допир на ESP32

Веригата на сензора за допир на ESP32 измерва общата капацитетност на канала за допир. Когато капацитетността се промени и размерът на промяната надвиши праговата стойност, системата може да открие допир или близост на пръст.

ESP32 има 10 капацитивни пина за допир, но само **осем** са изложени на Huzzah32:

![Диаграма на пиновете на Huzzah32](assets/images/AdafruitHuzzah32PinDiagram.png)
За подробности вижте документацията на Adafruit Huzzah32 [docs](https://learn.adafruit.com/adafruit-huzzah32-esp32-feather/pinouts). Кликнете с десния бутон и отворете изображението в нов раздел, за да го увеличите. За повече подробности относно капацитивните сензорни пинове вижте Espressif [docs](https://github.com/espressif/esp-iot-solution/blob/master/documents/touch_pad_solution/touch_sensor_design_en.md).
{: .fs-1 }

Espressif продава "[ESP32-Sense Kit](https://www.espressif.com/en/media_overview/news/look-out-new-esp32-sense-kit)", за да помогне да се подчертае как капацитивното докосване може да бъде интегрирано в продукти, включително линейни плъзгачи, колелце и матрични бутони.

<!-- TODO: обмисляне на написването на раздел с обща информация за капацитивното сензорно докосване -->

### Сензорно докосване срещу физически бутони

Капацитивното сензорно докосване се използва широко в домакински уреди, потребителска електроника и в промишлени контексти. Както се посочва в ESP32 [docs](https://github.com/espressif/esp-iot-solution/blob/master/documents/touch_pad_solution/touch_sensor_design_en.md#1-introduction-to-touch-sensor-system), в сравнение с механичните бутони, капацитивното сензорно докосване предлага:
- Липса на механични части, които се износват с времето
- Напълно запечатани повърхности (които могат да бъдат водоустойчиви)
- По-малко компоненти
- Модерен вид

Въпреки това, липсата на физически бутони може да намали достъпността, особено за слепи или слабо виждащи потребители.

### API за сензорно засичане на ESP32

API за сензорно засичане на ESP32 е описано [тук](https://docs.espressif.com/projects/esp-idf/en/latest/esp32/api-reference/peripherals/touch_pad.html); обаче Espressif разработи и Arduino wrapper библиотека, за да опрости използването му ([.h файл](https://github.com/espressif/arduino-esp32/blob/a59eafbc9dfa3ce818c110f996eebf68d755be24/cores/esp32/ esp32-hal-touch.h), [.c файл](https://github.com/espressif/arduino-esp32/blob/a59eafbc9dfa3ce818c110f996eebf68d755be24/cores/esp32/esp32-hal-touch.c)). Сензорното докосване е част от основната библиотека ESP32 Arduino, така че ако сте инсталирали платка ESP32 чрез Arduino IDE, ще можете да използвате библиотеката за сензорно докосване.

#### API за сензорно докосване ESP32 Arduino

ESP32 сензорното докосване Arduino [API](https://github.com/espressif/arduino-esp32/blob/a59eafbc9dfa3ce818c110f996eebf68d755be24/cores/esp32/esp32-hal-touch.h) има три метода:

{% highlight C %}
/*
* Задайте циклите, които отнема операцията по измерване
* Резултатът от touchRead, прагът и точността на
* откриването зависят от тези стойности. По подразбиране
* 0x1000 за измерване и 0x1000 за сън.
* С подразбиращите се стойности touchRead отнема 0,5 ms
* */
void touchSetCycles(uint16_t measure, uint16_t sleep);

/*
* Чете сензорния панел (стойности близки до 0 означават, че е засечено докосване)
* Можете да използвате този метод, за да изберете подходяща прагова стойност
* за използване като стойност за touchAttachInterrupt
* */
uint16_t touchRead(uint8_t pin);

/*
* Задайте функция, която да се извиква, ако стойността на сензорния панел падне
* под дадения праг. Използвайте touchRead, за да определите
* подходящ праг между състоянието на докосване и недокосване
* */
void touchAttachInterrupt(uint8_t pin, void (*userFunc)(void), uint16_t threshold);
{% endhighlight C %}

#### Примери за сензорно засичане на ESP32 Arduino

Espressif е създал два примера за Arduino с сензорно докосване: единият използва анкетиране ([TouchRead.ino](https://github.com/espressif/arduino-esp32/blob/a59eafbc9dfa3ce818c110f996eebf68d755be24/libraries/ESP32/examples/Touch/TouchRead/TouchRead. ino)), а другият използва прекъсване ([TouchInterrupt.ino](https://github.com/espressif/arduino-esp32/blob/a59eafbc9dfa3ce818c110f996eebf68d755be24/libraries/ESP32/examples/Touch/TouchInterrupt/TouchInterrupt.ino)) . Те са достъпни и в Arduino IDE: File -> Examples -> ESP32 -> Touch.

## Да направим нещо

Да направим проста, чувствителна на допир LED светлина. Ще проучим `touchRead` и ще определим кога е настъпило докосване въз основа на зададен праг. 

### Веригата

Използваме TOUCH6 (`T6`), който е GPIO пин 14.

![Схема на веригата с кабел, свързан към T6](assets/images/Huzzah32_CapacitiveTouchSensing_CircuitDiagram_Fritzing.png)

### Кодът

Кодът е доста прост. Използваме `touchRead`, за да измерим капацитивната стойност на пина. Стойности, близки до нула, показват докосване. Първоначално написахме бърза програма, за да отпечатаме стойностите на `touchRead` в Serial и установихме, че `touchRead` връща ~60-70, когато проводникът не е докоснат, и 6-15, когато проводникът е докоснат. След това използвахме това, за да настроим `TOUCH_THRESHOLD`. За да подобрим подхода си, можем да използваме основно изглаждане (*например* среден филтър), за да намалим преходните и грешните ниски показания.

Пълната ни реализация е на [github](https://github.com/makeabilitylab/arduino/blob/master/ESP32/Sensors/TouchRead/TouchRead.ino):

<!-- gist-it не работи, затова сега използваме emgithub -->
<!-- <script src="https://gist-it.appspot.com/https://github.com/makeabilitylab/arduino/blob/master/ESP32/Sensors/TouchRead/TouchRead.ino?footer=minimal"></script> -->

<script src="https://emgithub.com/embed.js?target=https%3A%2F%2Fgithub.com%2Fmakeabilitylab%2Farduino%2Fblob%2Fmaster%2FESP32%2FSensors%2FTouchRead%2FTouchRead.ino&style=github&showCopy=on"></script>

Този [изходен код](https://github.com/makeabilitylab/arduino/blob/master/ESP32/Sensors/TouchRead/TouchRead.ino) се намира в GitHub.
{: .fs-1 }

### Видео от работното място

Ето видео от работното място, което демонстрира нашия [TouchRead](https://github.com/makeabilitylab/arduino/blob/master/ESP32/Sensors/TouchRead/TouchRead.ino) код, използващ както проводник, така и алуминиево фолио като проводник. 

<iframe width="736" height="414" src="https://www.youtube.com/embed/RE2mH38e9RI" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
Нашата верига има потенциометър, но той е останал от предишния урок и тук не се използва!
{: .fs-1 }

### Прекъсвания при докосване

Създадохме и два примера за докосване с прекъсвания: [TouchInterrupt](https://github.com/makeabilitylab/arduino/blob/master/ESP32/Sensors/TouchInterrupt/TouchInterrupt.ino) използва `touchAttachInterrupt` на `T6`, за да отпечата на сериен порт, когато бъде засечено докосване, а [TouchInterruptLed](https://github.com/makeabilitylab/arduino/blob/master/ESP32/Sensors/TouchInterruptLed/TouchInterruptLed.ino) разширява това, като включва и LED за определено време след като е засечено докосване.

## Следващ урок

В [следващия урок](iot.md) ще свържем ESP32 с облака чрез WiFi и ще използваме IoT табло, за да видим данните си.

<span class="fs-6">
<!-- [Предишен: Аналогов вход с ESP32](pot-fade.md){: .btn .btn-outline } -->
[Предишен: Възпроизвеждане на тонове](tone.md){: .btn .btn-outline }
[Следващ: Изработване на IoT устройство](iot.md){: .btn .btn-outline }
</span>
