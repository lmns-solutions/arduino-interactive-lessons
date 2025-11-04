---
lang: bg
permalink: /arduino/led-fade.html
page_id: arduino-led-fade
layout: default
title: L4&#58; Затъмняване на LED
nav_order: 4
parent: Изход
grand_parent: Въведение в Arduino
usemathjax: true
has_toc: true # (по подразбиране)
коментари: true
usetocbot: true
---
# {{ page.title | replace_first:"L",'Урок '}}
{: .no_toc }

## Съдържание
{: .no_toc .text-delta }

1. Съдържание
{:toc}
---

В [предходния урок](led-blink.md) научихме как да включваме и изключваме LED с помощта на [`digitalWrite`](https://www.arduino.cc/reference/en/language/functions/digital-io/digitalwrite/) — което работи чрез алтернативно настройване на Pin 3 на 5V (`HIGH`) и 0V (`LOW`) . В този урок ще научим как да контролираме програмно изходното напрежение с по-фини градации, използвайки [`analogWrite`](https://www.arduino.cc/reference/en/language/functions/analog-io/analogwrite/). По-конкретно, ще постепенно затъмняваме и изключваме LED, както е показано в анимацията по-долу.

![Анимация, показваща LED на пин 3, който постепенно се включва и изключва](assets/movies/Arduino_LEDFade_Pin3.gif)
Тази илюстративна анимация не показва тока (жълтите кръгчета) само поради моите ограничени умения за анимация. Но се надявам, че можете да си представите (в ума си) как LED променя яркостта си с тока по същия начин. :)
{: .fs-1 }

## Материали

Ще използвате същите материали като [по-рано](led-blink.md), включително [Arduino IDE](https://www.arduino.cc/en/main/software) и USB кабел, за да качите програмата си от компютъра си на Arduino.

| Arduino | LED | Резистор |
|:-----:|:-----:|:-----:|
| Arduino Uno, Leonardo или подобен | Червен LED | 220Ω резистор |
| ![Arduino Uno]({{ site.baseurl }}/assets/images/ArduinoUno_Fritzing.png) | ![Червен LED]({{ site.baseurl }}/assets/images/RedLED_Fritzing.png) | ![220 Ohm резистор]({{ site.baseurl }}/assets/images/Resistor220_Fritzing.png) |
| Arduino Uno, Leonardo или подобен | Червен LED | 220Ω резистор |

## Изработване на веригата

Както е отбелязано в урока ["Въведение в цифровия изход"](./led-blink.md), Arduino Uno има **20 пина за вход/изход с общо предназначение** ([GPIO](https://en.wikipedia.org/wiki/General-purpose_input/output)), които могат да се използват за цифров вход/изход (I/O) с помощта на [`digitalRead()`](https://www.arduino. cc/reference/en/language/functions/digital-io/digitalread/) и [`digitalWrite()`](https://www.arduino.cc/reference/en/language/functions/digital-io/digitalwrite/), съответно.

![Близък план на 20-те цифрови I/O пина на Arduino Uno](assets/images/ArduinoUno_DigitalIOPins.png)

Въпреки това, **6** от 20-те I/O пина могат **също** да се използват за **"аналогов" изход** — изход на напрежение, който не е само `HIGH` (5V) или `LOW` (0V), а между тези две крайности. Тези аналогови изходни пинове са обозначени с тилда (`~`) отпечатана до пина на Arduino (отпечатана директно върху печатната платка на Arduino).

![Близък план на Arduino Uno, подчертаващ шестте аналогови изходни пина](assets/images/ArduinoUno_CloseUp_AnalogOutputPins.png)

Така че за този урок **не** е необходимо да променяме веригата изобщо! Можете да запазите същата верига като в [урока за мигане на LED](led-blink.md). Всъщност това е причината, поради която избрахме пин 3 в първия случай.

![Схема на свързване, показваща катода на LED, свързан към GND, и анода на LED, свързан към резистор 220 Ohm, а след това към пин 3](assets/images/Arduino_LEDFade_Pin3Circuit.png)

### Често срещано объркване: аналоговите I/O пинове са различни!

Често срещано объркване сред начинаещите е смесването на аналоговите **изходни** пинове и аналоговите **входни** пинове. За цифровите I/O входните и изходните пинове са еднакви и могат да се конфигурират като `INPUT` или `OUTPUT` с помощта на командата [`pinMode`](https://www.arduino.cc/reference/en/language/functions/digital-io/pinmode/), но аналоговите I/O пинове са различни! Вижте фигурата по-долу:

![Анотирана картинка на Arduino Uno, показваща разликата между аналоговите входни и изходни пинове](assets/images/ArduinoUno_AnalogInputAndOutputPinsAreDifferent.png)

В този урок ще научим за аналоговия изход (използвайки [`analogWrite`](https://www.arduino.cc/ reference/en/language/functions/analog-io/analogwrite/)). В бъдещ урок ще научим за аналоговия вход (използвайки [`analogRead`](https://www.arduino.cc/reference/en/language/functions/analog-io/analogread/))

## Използване на analogWrite

За да постепенно затъмним LED, ще използваме функцията [`analogWrite(int pin, int value)`](https://www.arduino.cc/reference/en/language/functions/analog-io/analogwrite/), която приема пин като първи параметър и 8-битова стойност между 0-255 като втори. 

### Модулация на ширината на импулса (PWM)

Въпреки името си, Arduino Uno, Leonardo, Nano, Mega и много други Arduino платки всъщност не осигуряват **истински аналогов** изход чрез [цифрово-аналогов преобразувател (DAC)](https://en.wikipedia.org/wiki/Digital-to-analog_converter). Вместо това те използват метод, наречен импулсно-широчинна модулация (PWM), за да *емулират* аналогов изход. За повечето цели – като промяна на яркостта на LED или контрол на скоростта на мотор – това няма значение; обаче, ако искате да изведете високочестотна синусоидална вълна – истински аналогов изходен сигнал – като възпроизвеждане на музика, тогава ще трябва да намерите Arduino микроконтролер с вграден DAC като [Due](https://store.arduino.cc/usa/due) (вижте това [SimpleAudioPlayer упътване](https://www.arduino.cc/en/Tutorial/SimpleAudioPlayer)), или да свържете Uno към външна DAC платка, като тази [SparkFun MP3 Player Shield](https://learn.sparkfun.com/tutorials/mp3-player-shield-hookup-guide-v15/all).

За да разберем PWM, нека първо си припомним характеристиките на квадратната вълна: има продължителност на един пълен цикъл (период), честота (колко пъти цикълът се повтаря в секунда), амплитуда (разстояние от върха до дъното на вълната; в този случай 5V) и работен цикъл (времето, през което вълната е HIGH *срещу* НИСКА в един период).

![Пример за квадратна вълна](assets/images/SquareWaveWithDutyCycle.png)

След това вижте [това видео](https://www.youtube.com/watch?v=YmPziPfaByw) от Afrotechmods:

<iframe width="736" height="414" src="https://www.youtube.com/embed/YmPziPfaByw?si=ECb8GM_a0wfC-8U3" frameborder="0" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

И така, какво точно прави функцията [`analogWrite`](https://www.arduino.cc/reference/en/language/functions/analog-io/analogwrite/)? Тя просто променя **работния цикъл** на изходния пин. Това означава, че 8-битовата стойност (0-255) директно контролира колко дълго се прилага стойност 5V към изходния пин по време на един период на "аналогово записване”. Така че `analogWrite(<pin>, 127)` ще изведе стойност 5V за половината от периода (тъй като 127/255 = ~50%), а `analogWrite(<pin>, 191) ` ще изведе 5V за 75% от периода (тъй като 191/255 = ~75%). Тази част от времето, през която сигналът е `HIGH`, се нарича работен цикъл.

![Примери за импулсно-широчинна модулация](assets/images/PulseWidthModulationSlide_ByJonEFroehlich.png)

<!-- ![Графика на работния цикъл на импулсно-широчинната модулация](assets/images/PulseWidthModulation_FromSparkfun.jpg)

Графика на работния цикъл на импулсно-широчинната модулация от [PWM Tutorial](https://learn.sparkfun.com/tutorials/pulse-width-modulation/all) на Sparkfun
{: .fs-1 } -->

### Защо Uno има само шест PWM изхода?

Защо Arduino Uno има само шест PWM изхода? Защото микроконтролерът ATmega328 има три хардуерни таймера, които контролират шестте PWM изхода.

Arduino Leonardo има седем PWM пина (с един повече от Uno), защото има четири хардуерни таймера (новият се нарича `timer4`). Вижте диаграмите на пиновете по-долу.

![Диаграма на пиновете, показваща шестте PWM пина на Uno и седемте на Leonardo](assets/images/ArduinoUnoVsLeonardo_PWM_PinOuts_ByJonEFroehlich.png)

### Каква е честотата на PWM изходите?

При Uno и Leonardo PWM изходите са или 490Hz, или 980Hz (в зависимост от основните хардуерни таймери) — **не можете да промените честотата** на тези вълни, използвайки [`analogWrite`](https://www.arduino.cc/reference/en/language/functions/analog-io/analogwrite/) . За Uno PWM пиновете са 3, 5, 6, 9, 10, 11 (всички пинове са 490Hz, с изключение на 5 и 6, които са 980Hz). За Leonardo, PWM пиновете са 3, 5, 6, 9, 10, 11, 13 (всички пинове са 490Hz, с изключение на 3 и 11, които са 980Hz).

Вижте изображението по-долу (и [Arduino Docs](https://www.arduino.cc/reference/en/language/functions/analog-io/analogwrite/)).

![Диаграма на изводите, показваща шестте PWM пина на Uno и седемте на Leonardo, заедно с техните честоти](assets/images/ArduinoUnoVsLeonardo_PWM_PinOutFrequencies_ByJonEFroehlich.png)

### Ръчно имплементиране на PWM

Мога ли ръчно да имплементирам PWM на всеки пин, просто като бързо включвам и изключвам пина с желаната честота и цикъл на работа? Да, но PWM вълната може да бъде нестабилна (освен ако не деактивирате прекъсванията). Вижте: [SecretsOfArduinoPWM](https://www.arduino.cc/en/Tutorial/SecretsOfArduinoPWM) и [примерния код](https://playground.arduino.cc/Main/PWMallPins/), който ръчно имплементира PWM цикъл.

### Научете повече за PWM

За да научите повече за PWM, прочетете това [ръководство от ITP NYU](https://itp.nyu.edu/physcomp/lessons/microcontrollers/analog-output/) и гледайте видеото им "аналогов изход”:

<div style="padding:56.25% 0 0 0;position:relative;"><iframe src="https://player. vimeo.com/video/93554355" style="position:absolute;top:0;left:0;width:100%;height:100%;" frameborder="0" allow="autoplay; fullscreen" allowfullscreen></iframe></div><script src="https://player.vimeo.com/api/player.js"></script>

<!- - TODO: в бъдеще би било добре да се свърже OLED, за да се покаже analogOut стойност + да се покаже PWM сигнал на осцилоскоп с
камера отгоре надолу. Могат да се направят две версии: (1) с кода, който работи както е написан, и друга (2) с потенциометър
за контрол на PWM сигнала -->

## Написване на кода

Добре, да напишем малко код!

### Стъпка 1: Стартирайте нов скиц в Arduino IDE

Стартирайте нов скиц в Arduino IDE:

![Снимка на екрана на Arduino IDE, показваща нов празен скиц](assets/images/ArduinoIDE_FreshSketch.png)

### Стъпка 2: Напишете код за инициализация

Нашият код за инициализация е същият като за [LED blink](led-blink.md), с изключение на добавянето на `const int MAX_ANALOG_OUT = 255;` и константа за забавяне от 5 милисекунди (`const int DELAY_MS = 5;`).

{% highlight C %}
const int LED_OUTPUT_PIN = 3;
const int MAX_ANALOG_OUT = 255; // максималният аналогов изход на Uno е 255
const int DELAY_MS = 5;

void setup() {
    // задайте Pin 3 за изход
    pinMode(LED_OUTPUT_PIN, OUTPUT);
}
{% endhighlight C %}

### Стъпка 3: Напишете цикъл за затъмняване

Сега напишете код, който извежда постоянно нарастващи стойности за [`analogWrite`](https://www.arduino.cc/reference/en/language/functions/analog-io/analogwrite/) (за затъмняване), последвани от постоянно намаляващи стойности (за изсветляване).

{% highlight C %}
void loop(){
    // избледняване
    for(int i = 0; i <= MAX_ANALOG_OUT; i += 1){
        analogWrite(LED_OUTPUT_PIN, i);
        delay(DELAY_MS);
    }

    // избледняване
    for(int i = MAX_ANALOG_OUT; i >= 0; i -= 1){
        analogWrite(LED_OUTPUT_PIN, i);
        delay(DELAY_MS);
    }
}
{% endhighlight C %}

Пълният код е вграден по-долу:

<!-- gist-it не работи, затова сега използваме emgithub -->
<!-- от нашето [GitHub репо](https://github.com/jonfroehlich/arduino/blob/master/Basics/analogWrite/FadeOnAndOffForLoop/FadeOnAndOffForLoop.ino) е:
<script src="https://gist-it.appspot.com/https://github.com/jonfroehlich/arduino/blob/master/Basics/analogWrite/FadeOnAndOffForLoop/FadeOnAndOffForLoop.ino?footer=minimal"></script> -->
<script src="https://emgithub.com/embed.js?target=https%3A%2F%2Fgithub.com%2Fmakeabilitylab%2Farduino%2Fblob%2Fmaster%2FBasics%2FanalogWrite%2FFadeOnAndOffForLoop%2FFadeOnAndOffForLoop.ino&style=github&showCopy=on"></script>

Този [изходен код](https://github.com/makeabilitylab/arduino/blob/master/Basics/analogWrite/FadeOnAndOffForLoop/FadeOnAndOffForLoop.ino) се намира в GitHub.
{: .fs-1 }

### Стъпка 4: Компилирайте, качите и стартирайте!

Сега компилирайте, качите и изпълнете кода. След като качването приключи, LED индикаторът трябва веднага да започне да затъмнява и след това да угасне. Вижте видеото по-долу.

<iframe width="736" height="414" src="https://www.youtube.com/embed/Y0mSFmW7G4U" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

## Визуализиране на изходното напрежение

Какво всъщност се случва на пин 3, когато записваме различни стойности в `analogWrite`? Е, не забравяйте, че основните Arduino платки като Uno и Leonardo нямат възможност да записват междинни напрежения (те нямат цифро-аналогови преобразуватели или DAC). Затова, вместо това, те "фалшифицират” чрез използване на импулсно-широчинна модулация (PWM) и модулиране на *фракцията* от времето, през което 5V изходна вълнова форма е `HIGH` спрямо `LOW`. Това се нарича **работен цикъл**.

### Визуализиране на PWM вълната

За да видите как се променя PWM вълната с различни `analogWrite` стойности на Arduino Leonardo, написахме [проста програма](https://github.com/makeabilitylab/arduino/blob/master/Basics/analogRead/TrimpotLEDSmoothed/TrimpotLEDSmoothed.ino), която приема аналогов вход (в този случай от потенциометър) и го използва, за да зададе стойност `analogWrite` на пин 3. Припомнете си, че на Leonardo честотата на PWM на пин 3 е 980Hz ([вижте документацията](https://www.arduino.cc/reference/en/language/functions/analog-io/analogwrite/)).

Освен потенциометъра, нашата верига не се е променила (все още имаме LED с резистор за ограничаване на тока на пин 3).

Нека да разгледаме:

<iframe width="736" height="414" src="https://www.youtube.com/embed/h-K0q18BRIE" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

За да създадем тази [програма](https://github.com/makeabilitylab/arduino/blob/master/Basics/analogRead/TrimpotLEDSmoothed/TrimpotLEDSmoothed.ino), трябваше да използваме както `analogRead`, така и `analogWrite`. До края на този урок трябва да имате добро разбиране за `analogWrite` и PWM. Но няма да научим повече за `analogRead`, докато не стигнем до уроците за микроконтролери [Въведение във входа](intro-input.md).

### Визуализиране на ефективното напрежение на изхода

В допълнение към визуализирането на **действителното** напрежение на изхода от `analogWrite` (PWM вълновата форма), можем да визуализираме и (ефективното) напрежение на изхода. За целта можем да използваме [Serial Plotter](https://learn.adafruit.com/experimenters-guide-for-metro/circ08-using%20the%20arduino%20serial%20plotter) на Arduino. За да го отворите, изберете Tools -> Serial Plotter. Плотерът ще се опита да визуализира всички стойности, разделени със запетая, които извеждате чрез `Serial.print`.

В клипа по-долу виждаме симулация на нашия [fade code](https://github.com/jonfroehlich/arduino/blob/master/Basics/analogWrite/FadeOnAndOffForLoop/FadeOnAndOffForLoop.ino) + верига, работеща в Tinkercad. Вдясно, в прозореца [Serial Monitor](https://www.programmingelectronics.com/ using-the-print-function-with-arduino-part-1/) прозореца, отпечатваме и графично представяме ефективните напрежения в реално време, изхождащи от Pin 3.

<video controls="controls">
<source src="assets/movies/Arduino_LEDFadeWithGraph_Pin3.mp4" type="video/mp4">
</video>

## Изчисляване на тока през нашия LED

Разбира се, именно **токът** през LED определя яркостта. Но как можем да изчислим (ефективния) ток с PWM?

Отново, според закона на Ом ($$I = \frac{V}{R}$$), можем да определим тока през нашата верига при различни изходи на пин 3. Припомнете си, че токът не преминава през LED, докато не бъде изпълнено условието за неговото напрежение в права посока $$V_f$$. При червен LED обичайното напрежение в права посока е $$V_f=2V$$. С [`analogWrite`] (https://www.arduino.cc/reference/en/language/functions/analog-io/analogwrite/), GPIO пинът все още се задвижва `HIGH` (5V), но само за част от времето поради PWM (тази част се нарича работен цикъл) . Така че изискването $$V_f$$ все още е изпълнено и нашите **очи** възприемат LED-а като включен, но всъщност той **мига** незабележимо бързо!

За да изчислим тока през нашата LED верига с PWM, нека $$DF$$ да е равно на **фракцията на работния цикъл**, фракцията от периода на вълната, която е HIGH. Тогава можем да използваме следното уравнение: $$I = \frac{V_s - V_f}{R} * DF$$, за да изчислим тока. Така например, ако използваме `analogWrite` с `51`, тогава $$DF=\frac{51}{255}=0.2$$. С 220Ω токът ни ще бъде: $$I=\frac{5V - 2V}{220Ω}*0.2=2.7mA$$.
 

Вижте таблицата по-долу за примерни 8-битови изходни стойности за `analogWrite` на пин 3 и ефективния ток.

| Резистор | Напрежение на пин 3 | Стойност на пин 3 | PWM цикъл на работа | Резултатен ток |
|:-------------|:-------------|:-------------|:-------------|:---------- ------|
| 220Ω | 5V | 0 | $$\frac{0}{255}=0.0$$ | $$I = \frac{5V-2V}{220Ω} * 0.0=0.0mA $$ |
| 220Ω | 5V | 45 | $$\frac{45} {255}=0,176$$ | $$I = \frac{5V-2V}{220Ω} * 0,176=2,4mA $$ |
| 220Ω | 5V | 103 | $$\frac{103}{255}=0,404$$ | $$I = \frac{5V-2V}{220Ω} * 0,404=5,5mA $$ |
| 220Ω | 5V | 128 | $$\frac{128}{255}=0,502$$ | $$I = \frac{5V-2V}{220Ω} * 0,780=6,8mA $$ |
| 220Ω | 5V | 199 | $$\ frac{199}{255}=0,780$$ | $$I = \frac{5V-2V}{220Ω} * 0,780=10,5mA $$ |
| 220Ω | 5V | 255 | $$\frac{255}{255}=1.0$$ | $$I = \frac{5V-2V}{220Ω} * 1.0=13.4mA $$ |

## Подобрен подход за затихване: премахване на for цикъла

Спомнете си в [урока за мигане на LED](led-blink.md), където споменахме, че искаме да избегнем дълги `for` цикли и дълги `забавяния` в кода си. Защо? Защото докато сме в забавяне, не можем да правим нищо друго: не можем да четем или да отговаряме на други входни данни (бележка: бихме могли да използваме прекъсвания, но засега нека отложим този въпрос). Вижте ["Какво всъщност прави delay()?"](inside-arduino.md#what-does-delay-actually-do) в нашето ръководство [Inside Arduino](inside-arduino.md).

Така че, нека пренапишем примера за избледняване, но без for цикли, а вместо това да разчитаме на факта, че `loop()` вече е `loop` :). Макар кодът по-долу да е различен, резултатът от затъмняването на LED е същият (така че няма да забележите разлика, ако опитате и двата варианта).

{: .note }
Имам навика да поставям префикс `_` пред глобалните си променливи, но това е просто моя собствена конвенция и ми помага лесно да разграничавам локалните променливи от глобалните. Разбира се, не е необходимо да правите същото! 😊

{% highlight C %}
const int LED_OUTPUT_PIN = 3;
const int MAX_ANALOG_OUT = 255; // максималният аналогов изход на Uno е 255
const int DELAY_MS = 5;

int _fadeAmount = 5; // степента на затъмняване на LED при всяка стъпка
int _curBrightness = 0; // колко ярък е LED

// Функцията setup се изпълнява веднъж, когато натиснете бутона за ресет или включите платка
void setup() {
    // задайте LED пина като изход
    pinMode(LED_OUTPUT_PIN, OUTPUT);
    Serial.begin(9600); // за използване на Serial.println
}

// Функцията loop се изпълнява отново и отново безкрайно
void loop() {

    // задайте яркостта на LED пина
    analogWrite(LED_OUTPUT_PIN, _curBrightness);

    // променете яркостта за следващия път през цикъла
    _curBrightness = _curBrightness + _fadeAmount;

    // обърнете посоката на затъмняването в края на всяка посока на затъмняване
    if (_curBrightness <= 0 || _curBrightness >= MAX_ANALOG_OUT) {
        _fadeAmount = -_fadeAmount; // обръща посоката на затъмняване
    }

    // изчакайте няколко милисекунди, за да видите ефекта на затъмняване
    delay(DELAY_MS);
}
{% endhighlight C %}

Можете да намерите [този код в GitHub](https://github.com/makeabilitylab/arduino/blob/master/Basics/analogWrite/FadeOnAndOff/FadeOnAndOff.ino).

## Подобрен подход за избледняване 2: елиминиране на забавянията

Можете ли да подобрите още повече горния код? Какво ще кажете да елиминирате изцяло `delay()`, но все пак да оставите зададен интервал за "пауза" при всяка стойност на избледняване на LED?

Опитайте се да напишете решение сами, а след това погледнете [нашето](https://github.com/makeabilitylab/arduino/blob/master/Basics/analogWrite/FadeOnAndOffWithoutDelay/FadeOnAndOffWithoutDelay.ino). Същите ли са или се различават? По какъв начин?

## Следващ урок

В [следващия урок](led-blink2.md) ще научим за разликата между **токови източници** и **токови поглъщатели**, за да затвърдим разбирането си за това как микроконтролерите могат да контролират изхода.

<span class="fs-6">
<!-- [Предишен: Мигащ LED](led-blink.md){: .btn .btn-outline } -->
[Предишен: Сериен дебъг](serial-print.md){: .btn .btn-outline }
[Следващ: LED Blink 2](led-blink2.md){: .btn .btn-outline }
</span>
