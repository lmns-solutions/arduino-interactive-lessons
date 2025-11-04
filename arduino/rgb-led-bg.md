---
lang: bg
permalink: /arduino/rgb-led.html
page_id: arduino-rgb-led
layout: default
title: L6&#58; RGB LEDs
parent: Изход
grand_parent: Въведение в Arduino
usemathjax: true
has_toc: true # (по подразбиране)
comments: true
usetocbot: true
---
# {{ page.title | replace_first:"L",'Урок '}}
{: .no_toc }

## Съдържание
{: .no_toc .text-delta }

1. Съдържание
{:toc}
---

В този урок ще използваме RGB LED (RGB означава червено, зелено, синьо), за да прожектираме поредица от цветове и да научим разликата между дизайна на RGB LED с общ анод и общ катод.

![Анимация, показваща RGB LED, настроен на различни цветове въз основа на цифров изход на пинове 3, 5 и 6](assets/movies/Arduino_RGBLED_CommonCathode-Optimized.gif)

## Материали

Ще ви бъдат необходими следните материали. Важно е да знаете, че има **два типа** RGB LED диоди – описани по-долу – затова се уверете, че **определяте** кои RGB LED диоди използвате, тъй като това ще повлияе на конфигурирането на веригата. Но не се притеснявайте, ще разгледаме и двата типа RGB LED диоди.

| Breadboard | Arduino | RGB LED | Резистори |
|:---- -:|:-----:|:-----:|:-----:|
| ![Бредоборд]({{ site.baseurl }}/assets/images/Breadboard_Half.png) | ![Arduino Uno]({{ site.baseurl }}/assets/images/ArduinoUno_Fritzing.png) | ![RGB LED]({{ site.baseurl }}/assets/images/RgbLED_Fritzing.png) | ![220 Ohm резистор]({{ site.baseurl }}/assets/images/Resistor220_Fritzing.png) |
| Breadboard | Arduino Uno, Leonardo или подобен | RGB LED (или с общ катод, или с общ анод) | **Три** резистора 220Ω |

### Общ анод срещу общ катод

Въпреки че са способни да показват хиляди цветови комбинации, RGB LED диодите всъщност са доста прости; те съдържат три отделни LED диода в един пакет: червен, зелен и син. Важно, но и малко объркващо, е, че има два дизайна на RGB LED диоди – **общ анод** и **общ катод** – които се различават по крачето, което се споделя между трите вградени LED диода.

1. При **общия анод** трите вградени LED споделят анодния извод. За да контролирате цвета на RGB LED, трябва да свържете анода към източника с по-високо напрежение и да свържете червения, зеления и синия извод към по-ниски нива на напрежение (*например* заземяване). Например, при източник на напрежение 5 V, свързан към общия аноден извод, настройването на другите три извода (червен, зелен, син) на 5 V би, малко противоречиво, **изключило** LED диода.
 

<!-- Например, с източник на напрежение 5V, свързан към общия аноден крак, настройването на другите три крака (червен, зелен, син) на 5V би, малко противоречиво, изключило светодиода. За разлика от това, настройването на червения крак на 0V, например, и на другите два крака на 5V би включило RGB светодиода в червено. -->

2. За разлика от това, **общият катод** работи много по-скоро като типичен светодиод (*например* като червения светодиод от предишните ни уроци). Тук и трите вградени светодиода споделят катодния крак. Така че, всеки отделен цветен крак се задвижва с по-висок източник на напрежение. 

<!-- Например, за да включите RGB светодиода с общ катод в червено, трябва да настроите катодния крак на земя, а червения крак на 5V -->

![Изображение, показващо схематично обща анодна RGB LED и обща катодна RGB LED. При общата анода вторият крак на RGB LED трябва да бъде свързан към източника с по-високо напрежение. При общата катода вторият крак на RGB LED трябва да бъде свързан към източника с по-ниско напрежение]({{ site.baseurl }}/assets/images/RgbLEDS_CommonAnodeVsCommonCathode.png)

### Как мога да разбера дали имам RGB LED с общ анод или общ катод?

Не можете да разберете дали имате RGB LED с общ анод или общ катод чрез визуална проверка. Вместо това, консултирайте се с уебсайта на доставчика, техническата спецификация или експериментирайте сами с LED (не забравяйте, че диодите работят само в една посока, така че стига да включите резистори за ограничаване на тока, всичко ще бъде наред!).

| Общ анод | Общ катод |
|:-----:|:---- -:|
| ![Снимка на RGB LED с общ анод]({{ site.baseurl }}/assets/images/RgbLED_CommonAnode_Adafruit.png) | ![Снимка на RGB LED с общ катод]({{ site.baseurl }}/assets/images/RgbLED_CommonCathode_Sparkfun.png) |
| Дифузен RGB LED с **общ анод** от [Adafruit](https://www.adafruit.com/product/159). Нарича се дифузен, защото епоксидният корпус е грапав и не е напълно прозрачен | Прозрачен RGB LED с **общ катод** от [Sparkfun](https://www.sparkfun.com/products/105). |

Ето две снимки на екрана от уебсайтовете на доставчиците ([Sparkfun](https://sparkfun.com) и [Adafruit](https://adafruit.com)). Обърнете внимание как типът RGB LED е ясно обозначен.

![Снимки на екрана от уебсайтовете на Sparkfun и Adafruit, показващи RGB LED диоди](assets/images/RgbLEDs_SparkfunAndAdafruitSupplierScreenshots.png)

## Обща катода

Ще започнем с верига с обща катода + код, защото е по-интуитивна (и подобна на нашите уроци за червени LED диоди), преди да преминем към версията с обща анода.

### Изработване на веригата

При дизайн с общ катод, вторият крак трябва да бъде свързан с пина `GND`, а първият (червен), третият (син) и четвъртият (зелен) крак трябва да бъдат свързани с цифрови I/O пинове (**не забравяйте** да поставите резистор за ограничаване на тока за всеки от тях). Можехме да използваме всеки цифров I/O пин, но избрахме пинове 6, 5 и 3 за червено, синьо и зелено съответно (тези пинове поддържат PWM и по този начин ще можем да използваме същата верига за следващия ни урок за [преливане на цветове с RGB LED-ове](rgb-led-fade.md)).

Ето окабеляването без breadboard (не се препоръчва, но може би е по-лесно да се види самата верига):

![Окабеляване на верига за RGB LED с общ катод, където катодът е свързан към GND](assets/images/ArduinoUno_RgbLEDCommonCathode_WiringDiagram.png)

А ето окабеляването с breadboard (схемата вдясно е еднаква и в двата случая). Забележете как схемата подчертава как токът тече от I/O пиновете, през резисторите, в RGB LED и след това надолу към земята.

![Схема на свързване на платка за RGB LED с общ катод, където катодът е свързан към GND](assets/images/ArduinoUno_RgbLEDCommonCathode_WiringDiagramWithBreadboard.png)

### Написване на кода

Ще напишем код, който мига в последователност от цветове. Припомнете си, че вграденият червен LED е свързан към пин 6, синият LED към пин 5, а зеленият LED към пин 3. Ще контролираме цвета на RGB LED, като извеждаме `HIGH` (5V) или `LOW` (0V) с помощта на [`digitalWrite` ](https://www.arduino.cc/reference/en/language/functions/digital-io/digitalwrite/) към тези пинове.

Например, за да RGB LED светодиодът да свети в червено, ще напишем:
{% highlight C %}
digitalWrite(RGB_RED_LED_PIN, HIGH);
digitalWrite(RGB_GREEN_LED_PIN, LOW);
digitalWrite(RGB_BLUE_LED_PIN, LOW);
{% endhighlight C %}

По същия начин, за да направим RGB LED зелен, ще напишем:
{% highlight C %}
digitalWrite(RGB_RED_LED_PIN, LOW);
digitalWrite(RGB_GREEN_LED_PIN, HIGH);
digitalWrite(RGB_BLUE_LED_PIN, LOW);
{% endhighlight C %}

В този пример ще мигаме следната последователност:

| Цвят | Червено, зелено, синьо Стойности на пина
|:----|:-----|
| <span style="background-color:#FF0000">&nbsp;&nbsp;</span> Червено | `HIGH`, `LOW`, `LOW` |
| <span style="background-color:#00FF00">&nbsp;&nbsp;</span> Зелено | `LOW`, `HIGH`, `LOW` |
| <span style="background-color:#0000FF">&nbsp;&nbsp;</span> Синьо | `LOW`, `LOW`, `HIGH` |
| <span style="background-color:#FF00FF">&nbsp;&nbsp;</span> Лилаво | `ВИСОКО`, `НИСКО`, `ВИСОКО` |
| <span style="background-color:#00FFFF">&nbsp;&nbsp;</span> Тюркоазено | `НИСКО`, `ВИСОКО`, `ВИСОКО` |
| <span style="background-color:#FFFFFF">&nbsp;&nbsp;</span> Бяло | `HIGH`, `HIGH`, `HIGH` |

---

**ЗАБЕЛЕЖКА:** За тези, които са запознати с html, това е много подобно на шестнадесетичните цветови кодове в html, където червеното, например, се определя с <span style="background-color:#FF0000; color:white">#FF0000</span>, зелено с <span style="background-color:#00FF00; color:black">#00FF00</span>, 
синьо с <span style="background-color:#0000FF; color:white">#0000FF</span> и т.н.

---

#### Стъпка 1: Напишете код за инициализация

Както обикновено, въвеждаме някои константи за нашите литерални присвоявания и след това настройваме нашите пинове като `OUTPUT`.

{% highlight C %}
const int DELAY_MS = 1000; // забавяне между промените в цвета в милисекунди
const int RGB_RED_LED_PIN = 6; // обозначен с оранжев проводник
const int RGB_GREEN_LED_PIN = 5; // обозначен със зелен проводник
const int RGB_BLUE_LED_PIN = 3; // обозначен със син проводник

void setup()
{
    // Настройте червения, зеления и синия RGB LED пинове на изход
    pinMode(RGB_RED_LED_PIN, OUTPUT);
    pinMode(RGB_BLUE_LED_PIN, OUTPUT);
    pinMode(RGB_GREEN_LED_PIN, OUTPUT);
}
{% endhighlight C %}

#### Стъпка 2: Напишете нова помощна функция, наречена setRgbLedColor

За да помогнем за настройката на цветовете на RGB LED, ще напишем нова функция, наречена `setRgbLedColor(int red, int green, int blue)`, която приема `HIGH` или `LOW` за червения, зеления и синия int параметър.

{% highlight C %}
// Функцията очаква HIGH или LOW за всеки параметър
void setRgbLedColor(int red, int green, int blue){
    digitalWrite(RGB_RED_LED_PIN, red);
    digitalWrite(RGB_GREEN_LED_PIN, green);
    digitalWrite(RGB_BLUE_LED_PIN, blue);
}
{% endhighlight C %}

#### Стъпка 3: Напишете последователността от цветове

Сега, в `loop()`, ще напишем конкретната последователност от цветове, която искаме:

{% highlight C %}
void loop()
{
    // червено
    setRgbLedColor(HIGH, LOW, LOW);
    delay(DELAY_MS);

    // зелено
    setRgbLedColor(LOW, HIGH, LOW);
    delay(DELAY_MS);

    // синьо
    setRgbLedColor(LOW, LOW, HIGH);
    delay(DELAY_MS);

    // лилаво
    setRgbLedColor(HIGH, LOW, HIGH);
    delay(DELAY_MS);

    // тюркоазен
    setRgbLedColor(LOW, HIGH, HIGH);
    delay(DELAY_MS);

    // бял
    setRgbLedColor(HIGH, HIGH, HIGH);
    delay(DELAY_MS);
}
{% endhighlight C %}

#### Стъпка 4: Компилиране, качване и стартиране

Това е всичко. Сега компилирайте, качите и изпълнете кода си!

В клипа по-долу изпълнявам нашия код [BlinkRGB](https://github.com/makeabilitylab/arduino/tree/master/Basics/digitalWrite/BlinkRGB), който е същият като горния, но включва някои [`Serial.print`](https://www.arduino.cc/ reference/en/language/functions/communication/serial/print/) за отстраняване на грешки (вижте този [мини-урок](https://create.arduino.cc/projecthub/glowascii/serial-monitor-arduino-basics-399eb6) за използването на Serial.print и Serial Monitor на Arduino IDE за отстраняване на грешки)

<iframe width="736" height="414" src="https://www.youtube.com/embed/ASez28rPjRU" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
Контейнерът за кисело мляко се използва за разсейване на светлината. Кърпички, бяла хартия или топка за пинг-понг (с отвор за LED) също вършат работа!
{: .fs-1 }

По-долу показваме видео анимация на изпълнението на кода и резултатното поведение на веригата. Обърнете специално внимание на посоката на тока – той ще тече в обратна посока при дизайна с общ анод (разгледан по-нататък).

<video controls="controls">
<source src="assets/movies/Arduino_RGBLED_CommonCathode_Animation.mp4" type="video/mp4">
</video>

## Общ анод

Сега нека да се заемем с версията с общ анод. Схемата на веригата е почти същата като преди: първият крак (червен), третият крак (син) и четвъртият крак (зелен) на RGB LED се свързват съответно с цифровите I/O пинове 6, 5 и 3 (заедно с резистор за ограничаване на тока за всеки от тях); вторият крак обаче сега е **общ анод** и следователно трябва да бъде свързан с 5V (а не с `GND`, както беше при общия катод).

За да прокараме ток през нашата верига и да включим вградения LED – да речем червения LED – трябва да настроим съответния червен LED пин на `LOW` (в този случай пин 6) и другите LED пинове на `HIGH` (пинове 5 и 3) . Защо? Не забравяйте, че токът винаги тече от **висок потенциал** към **нисък потенциал**. При общ анод вторият крак е анодът (висок потенциал или, в този случай, 5V), така че трябва да свържем другите крака към по-нисък потенциал, за да създадем разлика в напрежението и да позволим на тока да тече.

---

**Забележка:**
Тази настройка ви изглежда ли позната? Трябва да ви изглежда. При RGB LED с общ анод цифровите I/O пинове стават *токови поглъщатели*, точно като LED верига 2 в [урока LED Blink 2](led-blink2.md).

---

### Изработване на веригата

Както и преди, ето схема на веригата без платка за прототипи (която показва по-ясно връзките, но на практика би било трудно да се направи надеждно):

![Схема на веригата за RGB LED с общ анод, където катодът е свързан към GND](assets/images/ArduinoUno_RgbLEDCommonAnode_WiringDiagram.png)

А ето и по-практичната версия с breadboard (отново, схемата на веригата е еднаква и в двете версии – без breadboard и с breadboard):

![Схема на веригата с breadboard за RGB LED с общ анод, където анодът е свързан към 5V](assets/images/ArduinoUno_RgbLEDCommonAnode_WiringDiagramWithBreadboard.png)

### Написване на кода

RGB LED с общ анод работи **обратно** на версията с общ катод – за да включим определен цвят, пишем `LOW`, а не `HIGH`. Например, за да RGB LED да свети в червено, бихме написали:

{% highlight C %}
digitalWrite(RGB_RED_LED_PIN, LOW);
digitalWrite(RGB_GREEN_LED_PIN, HIGH);
digitalWrite(RGB_BLUE_LED_PIN, HIGH);
{% endhighlight C %}

По същия начин, за да направим RGB LED зелен, ще напишем:
{% highlight C %}
digitalWrite(RGB_RED_LED_PIN, HIGH);
digitalWrite(RGB_GREEN_LED_PIN, LOW);
digitalWrite(RGB_BLUE_LED_PIN, HIGH);
{% endhighlight C %}

Ще мигаме същата последователност като преди, но отново нашите `HIGH` и `LOW` са обърнати:

| Цвят | Червено, зелено, синьо Стойности на пина
|:----|:-----|
| <span style="background-color:#FF0000">&nbsp;&nbsp;</span> Червено | `LOW`, `HIGH`, `HIGH` |
| <span style="background-color:#00FF00">&nbsp;&nbsp;</span> Зелено | `HIGH`, `LOW`, `HIGH` |
| <span style="background-color:#0000FF">&nbsp;&nbsp;</span> Синьо | `HIGH`, `HIGH`, `LOW` |
| <span style="background-color:#FF00FF">&nbsp;&nbsp;</span> Лилаво | `НИСКО`, `ВИСОКО`, `НИСКО` |
| <span style="background-color:#00FFFF">&nbsp;&nbsp;</span> Тюркоазено | `ВИСОКО`, `НИСКО`, `НИСКО` |
| <span style="background-color:#FFFFFF">&nbsp;&nbsp;</span> Бяло | `НИСКО`, `НИСКО`, `НИСКО` |

Ето една анимация. Обърнете специално внимание на посоката на тока – той тече от 5V надолу през LED, резисторите за ограничаване на тока и в цифровите I/O пинове.

<video controls="controls">
<source src="assets/movies/Arduino_RGBLED_CommonAnode_Animation.mp4" type="video/mp4">
</video>

Няма да включваме код специално за RGB LED с общ анод. Вместо това ще покажем как да адаптираме предишния ни код за общ катод с само няколко допълнителни реда.

## Кодиране както за общ катод, така и за анод

Тъй като единствената разлика между кода за общ катод и кода за общ анод е обръщането на `HIGH` и `LOW`, можем просто да актуализираме предишния код за общ катод, като добавим `boolean`, за да проверим коя версия на RGB LED използваме. Ако е общ анод, ще обърнем сигналите `HIGH` и `LOW` – вижте функцията `setRgbLedColor`. Пълният код е в [GitHub](https://github.com/makeabilitylab/arduino/blob/master/Basics/digitalWrite/BlinkRGB/BlinkRGB.ino) и е показан по-долу:

<!-- gist-it не работи, затова сега използваме emgithub -->
<script src="https://gist-it.appspot.com/https://github.com/makeabilitylab/arduino/blob/master/Basics/digitalWrite/BlinkRGB/BlinkRGB.ino?footer=minimal"></script>

<script src="https://emgithub.com/embed.js?target=https%3A%2F%2Fgithub.com%2Fmakeabilitylab%2Farduino%2Fblob%2Fmaster%2FBasics%2FdigitalWrite%2FBlinkRGB%2FBlinkRGB.ino& style=github&showCopy=on"></script>

Този [изходен код](https://github.com/makeabilitylab/arduino/blob/master/Basics/digitalWrite/BlinkRGB/BlinkRGB.ino) се намира в GitHub.
{: .fs-1 }

<!-- TODO добави линк към схемата в Tinkercad за общ катод -->
<!-- TODO: добави точка за това, че Vf е различен за всеки цвят и следователно резисторите за всеки крак трябва да са различни? -->

<!-- TODO: добави видео от Workbench за версията с общ анод -->

## Следващ урок

В следващия урок ще научим как да преливаме между RGB цветовете и как да конвертираме в [HSL цветовото пространство](https://en.wikipedia.org/wiki/HSL_and_HSV), за да контролираме по-лесно (и независимо) да контролираме оттенъка и яркостта.

<span class="fs-6">
[Предишен: LED Blink 2](led-blink2.md){: .btn .btn-outline }
[Следващ: Cross-fading RGB LEDs](rgb-led-fade.md){: .btn .btn-outline }
</span>
