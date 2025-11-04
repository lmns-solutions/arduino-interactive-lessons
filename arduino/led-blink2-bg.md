---
lang: bg
permalink: /arduino/led-blink2.html
page_id: arduino-led-blink2
layout: default
title: L5&#58; Мигане на два светодиода
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

В този урок ще научим разликата между **токов източник** и **токов поглъщател**, като преразгледаме примера ни [LED Blink](led-blink.md). Ще включим и използването на [breadboard](../electronics/breadboards.md).

Ще изградим две прости LED вериги:

1. **LED верига 1** ще бъде същата като преди, с анода на LED насочен към пин 3 и катода насочен към земята. Когато задвижим пин 3 `HIGH` (5V), токът ще премине през LED към `GND`. В тази верига пин 3 е източникът на ток.
2. **LED верига 2** е подобна, но различна. Тук ще свържем втори LED с анода, насочен *настрани* от пин 4 (вместо към 5V), а катодът ще бъде насочен към пин 4. Когато задвижим пин 4 на `HIGH` (5V), LED ще се *изключи*, защото няма разлика в напрежението между двата края на веригата. Ако обаче задвижим пин 4 на `LOW` (0V), LED ще се включи. В тази верига пин 4 е токопоглъщател.

Да, това може да е малко объркващо в началото ("*чакай, светодиодът се изключва, когато пин 4 е "HIGH"?!?!*"). Но ще разберете, като завършите този урок. В анимацията по-долу обърнете внимание на посоката на тока във всяка верига. Забележете как са противоположни!

![Анимация, показваща как задействането на пин 3 и 4 HIGH ще включи LED верига 1 и ще изключи LED верига 2, а задействането на тези пинове LOW ще изключи LED верига 1 и ще включи LED верига 2](assets/movies/Arduino_Blink2Animation_Pins3And4-NoSchematic-Optimized.gif)

## Материали

Нашите материали са *почти* същите като преди, но този път ще направим две отделни LED вериги (със същите компоненти). Затова ни трябват **два червени LED** и **два 220Ω резистора**. Сега, когато използваме повече компоненти, ще ни е необходима и **бредборда**, която ще улесни създаването на чиста и организирана верига.

| Плоча за прототипи | Arduino | LED | Резистор |
|:-----:|:-----:|:-----:|:-----:|
| ![Прототипна платка]({{ site.baseurl }}/assets/images/Breadboard_Half.png) | ![Arduino Uno]({{ site.baseurl }}/assets/images/ArduinoUno_Fritzing.png) | ![Червен LED]({{ site.baseurl }}/assets/images/RedLED_Fritzing.png) | ![220 Ohm резистор]({{ site.baseurl }}/assets/images/Resistor220_Fritzing.png) |
| Breadboard | Arduino Uno, Leonardo или подобен | **2** червени LED | **2** 220Ω резистори |

## Преди да започнете: схеми на breadboard

В тези уроци ще използваме все по-често нашите breadboards, така че сега е добър момент да преговорим как се използват. Ако не сте запознати с тях, моля прочетете нашето [ръководство за breadboard](../electronics/breadboards.md) и гледайте следното [видео](https://youtu.be/6WReFkfrUIk):

<iframe width="736" height="414" src="https://www.youtube.com/embed/6WReFkfrUIk" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

## Изработване на веригата

### Стъпка 1: Свържете захранващите и GND релсите

![Диаграма, показваща захранващите и заземяващите релси на breadboard, свързани към 5V и GND портовете на Arduino Uno](assets/images/ArduinoUno_LEDBlink2_Circuit_Step1.png)

### Стъпка 2: Свържете първата LED верига

Сега нека свържем същата верига като преди (*например,* [LED Blink](led-blink.md) и [LED Fade](led-fade.md)), но този път ще използваме breadboard. Уверете се, че анодът на LED (дългият крак) е обърнат към Pin 3.

![Диаграма, показваща LED веригата с LED анода, свързан към пин 3, и резистора, свързан към LED катода и след това към GND](assets/images/ArduinoUnoLEDBlink2_Circuit_Step2WithSchematic.png)

### Стъпка 3: Свържете втората LED верига

Сега свържете втората LED верига. Този път обаче свържете катода на светодиода (късата крачка) към пин 4, а резистора към 5V шината.

![Диаграма, показваща LED веригата с катода на светодиода свързан към пин 4 и резистора свързан към анода на светодиода и след това към GND](assets/images/ArduinoUno_LEDBlink2_Circuit_Step3WithSchematic.png.png)

## Написване на кода: мигащи пинове 3 и 4

Нека напишем код, който да кара LED диодите, свързани към пинове 3 и 4, да мигат.

Важно е да се отбележи, че веригата на пин 3 (**LED верига 1** i) ще се включи с `digitalWrite(3, HIGH)`, докато веригата на пин 4 (**LED верига 2**) ще се изключи с `digitalWrite(4, HIGH)`. Защо? Припомнете си, че токът винаги тече от **високо** напрежение към **ниско** напрежение.
 

Когато пин 3 е `HIGH` (5V), има разлика в напрежението между пин 3 и `GND`, така че токът тече от пин 3 към земята. Когато пин 4 е `HIGH` (5V), обаче, няма разлика в напрежението в веригата (от пин 4 до 5V) и следователно няма ток. Това поведение е илюстрирано в анимацията по-долу.

<video controls="controls">
<source src="assets/movies/Arduino_Blink2Animation_Pins3And4.mp4" type="video/mp4">
</video>

Да напишем кода!

### Стъпка 1: Напишете кода за настройка и инициализация

{% highlight C %}
const int LED1_OUTPUT_PIN = 3; // Анодът е обърнат към пин 3 (катодът е свързан към 0V)
const int LED2_OUTPUT_PIN = 4; // Катодът е обърнат към пин 4 (анодът е свързан с 5V)
const int DELAY_MS = 1000; // забавяне от 1 секунда между миганията

// Функцията за настройка се изпълнява веднъж, когато натиснете бутона за нулиране или включите платка
void setup() {
    // Настройте нашите LED пинове като изход
    pinMode(LED1_OUTPUT_PIN, OUTPUT);
    pinMode(LED2_OUTPUT_PIN, OUTPUT);
}
{% endhighlight C %}

### Стъпка 2: Напишете кода за мигане в loop()

{% highlight C %}
// Функцията loop се изпълнява отново и отново безкрайно
void loop() {
    // По-долу ще видите, че задействането на Pin 3 HIGH ще включи LED1
    // но задействането на Pin 4 HIGH всъщност ще изключи LED2
    digitalWrite(LED1_OUTPUT_PIN, HIGH); // включва LED1
    digitalWrite(LED2_OUTPUT_PIN, HIGH); // изключва LED2
    delay(DELAY_MS); // забавянето е в милисекунди; изчакайте една секунда

    digitalWrite(LED1_OUTPUT_PIN, LOW); // изключва LED1 (Pin 3 сега е 0V, а другият крак на LED е 0V)
    digitalWrite(LED2_OUTPUT_PIN, LOW); // включва LED2 (Pin 4 сега е 0V, а другият крак на LED е 5V)
    delay(DELAY_MS); // изчакайте една секунда
}
{% endhighlight C %}

### Стъпка 3: Компилирайте, качите и стартирайте кода!

Успяхме! Сега компилирайте и качете кода.

![Анимиран GIF отгоре надолу на работната маса с веригата, работеща с Arduino](assets/movies/ArduinoUno_Blink2_Workbench.gif)

А ето и видео отгоре надолу с прозореца на кода:

<iframe width="736" height="414" src="https://www.youtube.com/embed/q6KcPYfum7c" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

<!-- ![Анимация, показваща LED верига 1 (свързана към пин 3), която се включва с HIGH изход, и LED верига 2 (свързана към пин 4), която се изключва, а след това обратното, когато пиновете са LOW (LED верига 1 се изключва и LED верига 2 се включва)](assets/movies/Arduino_Blink2Animation_Pins3And4-Trimmed.gif) -->

## Нашият код Blink2 в GitHub

Можете да получите достъп до нашия код Blink2 в нашето [Arduino GitHub хранилище](https://github.com/jonfroehlich/arduino). Той е показан и по-долу:

<!-- gist-it не работи, затова сега използваме emgithub -->
<!-- <script src="https://gist-it.appspot.com/{{ site.arduino_github_baseurl }}/blob/master/Basics/digitalWrite/Blink2LEDs/Blink2LEDs.ino?footer=minimal"></script> -->

<script src="https://emgithub.com/embed.js?target=https%3A%2F%2Fgithub.com%2Fmakeabilitylab%2Farduino%2Fblob%2Fmaster%2FBasics%2FdigitalWrite%2FBlink2LEDs%2FBlink2LEDs.ino&style=github&showCopy=on"></script>

Този [изходен код](https://github.com/makeabilitylab/arduino/blob/master/Basics/digitalWrite/Blink2LEDs/Blink2LEDs.ino) се намира в GitHub.
{: .fs-1 }

## Следващ урок

В [следващия урок](rgb-led.md) ще използваме нов компонент – RGB LED – за да изведем различни цветове на LED освен червено и ще научим за разликата и как да използваме дизайни на RGB LED с общ анод *срещу* общ катод.

<span class="fs-6">
[Предишен: LED Fade](led-fade.md){: .btn .btn-outline }
[Следващ: RGB LEDs](rgb-led.md){: .btn .btn-outline }
</span>
