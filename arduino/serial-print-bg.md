---
lang: bg
permalink: /arduino/serial-print.html
page_id: arduino-serial-print
layout: default
title: L3&#58; Отстраняване на грешки със сериен порт
nav_order: 3
parent: Изход
grand_parent: Въведение в Arduino
has_toc: true # (по подразбиране)
usemathjax: true
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

<video autoplay loop muted playsinline style="margin:0px">
<source src="assets/movies/BlinkWithSerialPrint-IMG_5777_Trim_720p.mp4" type="video/mp4" />
</video>
**Видео.** Видео, показващо как да използвате Serial.println(), за да отстраните грешки в кода. За целта модифицирахме простата програма за мигане, за да добавим серийни отпечатвания ([изходен код](https://github.com/makeabilitylab/arduino/blob/master/Basics/digitalWrite/BlinkWithSerialPrint/BlinkWithSerialPrint.ino)).
{: .fs-1 }

Отстраняването на грешки в кода винаги е трудно. Отстраняването на грешки в кода + вериги е още по-трудно! 💪🏽 Въпреки че сме едва на **третия** урок по Arduino (ура!), е време да представим някои стратегии за отстраняване на грешки в Arduino.

За **отстраняване на грешки в хардуера** са полезни мултиметрите и осцилоскопите. Разбираме, че много от вас може би (все още) не разполагат със собствени мултиметри или осцилоскопи. В този случай ви препоръчваме да изградите веригите си в симулационен инструмент като [Tinkercad Circuits](tinkercad.com/) и да използвате техните виртуални инструменти (*например* мултиметри). Ако физически изграждате нещо и то не работи, можете да опитате да го възпроизведете в Tinkercad или друг симулационен инструмент.

За **отстраняване на грешки в кода** обикновено се използват изрази "printline" (да, знам! 🤣) – вижте видеото по-горе. Понастоящем Arduino IDE не поддържа отстраняване на грешки в кода (*например* точки на прекъсване, стъпково изпълнение на код, извличане на паметта); обаче, в [Tinkercad Circuits](tinkercad.com/) има елементарна поддръжка за отстраняване на грешки (*например* стъпково изпълнение на код).

{: .note }
С въвеждането на Arduino IDE 2.0 има [поддръжка за отстраняване на грешки](https://docs.arduino.cc/software/ide-v2/tutorials/ide-v2-debugger/); обаче се поддържат само определени Arduino платки и е необходим специализиран хардуер.

<!-- TODO: обмислете да включите тук препоръки за основен мултицет и осцилоскоп. -->

## Използване на Serial.print за отстраняване на грешки

Използването на команди "print out” към "console” е може би най-старата (и вероятно най-надеждна) техника за отстраняване на грешки. Това е стандартната техника и за Arduino (въпреки че понякога може да бъде досадна).

За разлика от JavaScript, Java, C# или друг код, който се изпълнява във вашия уеб браузър или на вашите настолни/преносими компютри, вашият Arduino код се изпълнява на микроконтролера на Arduino (*например,* Uno използва [ATmega328P](https://ww1.microchip.com/downloads/en/DeviceDoc/Atmel -7810-Automotive-Microcontrollers-ATmega328P_Datasheet.pdf); Leonardo използва [ATmega32u4](https://ww1.microchip.com/downloads/en/DeviceDoc/Atmel-7766-8-bit-AVR-ATmega16U4-32U4_Datasheet.pdf)). Следователно, когато "печатаме на конзолата", всъщност трябва да прехвърлим данните от микроконтролера на Arduino на вашия компютър за разработка. За тази цел Arduino използва [серийния](https://www.arduino.cc/reference/en/language/functions/communication/serial/) протокол. По-конкретно, функцията [`Serial.print ()`](https://www.arduino.cc/reference/en/language/functions/communication/serial/print/) и [`Serial.println()`](https://www.arduino.cc/reference/en/language/functions/communication/serial/println/).

![Абстрактна диаграма, показваща как работи Serial.println](assets/images/ArduinoSerialPrintlnDiagram_ByJonEFroehlich.png)

Тези две функции отпечатват данни към сериен порт като ASCII текст, четим за човека (версията `println` просто вмъква връщане на каретката `\r`, последвано от символ за нов ред `\n`). За да изпратите данни, без да ги преобразувате в ASCII текст, трябва да използвате [`Serial.write()`](https://www.arduino.cc/reference/en/language/functions/communication/serial/write).

В по-късните уроци ще видим как да използваме серийната комуникация не само за целите на отстраняването на грешки, но и за двупосочна комуникация с компютъра (вижте [L1: Въведение в серийната комуникация](../communication/serial-intro.md) и [тези ITP примери](https://itp.nyu.edu/physcomp/labs/labs-serial-communication/)). За нашите въвеждащи уроци обаче ще го използваме само за отпечатване на информация за работата на програмата ни.

{: .warning }
> След като включите сериалния порт (чрез `Serial.begin()`), **вече не можете да използвате** цифровите пинове 0 или 1 за вход/изход, защото тези пинове се използват за сериална комуникация (цифровият пин 0 е RX, а пин 1 е TX). Вижте [документацията на Arduino](https://www.arduino.cc/en/reference/serial).
>
> Ето защо много от нашите "начални” примери използват **пин 3**, а не пинове 0 или 1 (пин 3 има и допълнителното предимство, че може да се конфигурира за аналогов изход, което ще разгледаме в [следващия урок](led-fade.md)).

### Създаване на проста програма "Hello World!” Serial.print

Нека създадем проста програма "Hello World!”, която използва функционалността `Serial.print`, за да получава ASCII данни през сериен порт. За това дори не ни е необходим външен хардуер: само нашият Arduino Leonardo и USB кабел.

#### Стъпка 1: Инициализирайте сериен порт

За да използваме сериен порт, първо трябва да го инициализираме с [`Serial.begin(BAUD_RATE)`](https://www.arduino.cc/reference/en/language/functions/communication/serial/begin/). Скоростта на предаване е скоростта на предаване в битове в секунда (bps) и обикновено се задава на `9600`, освен ако не са необходими по-високи скорости. Тъй като [Serial library](https://www.arduino.cc/reference/en/language/functions/communication/serial/) използва асинхронна комуникация, както предавателят, така и приемникът трябва да се съгласят за скоростта на комуникация (скоростта на предаване). Затова ще трябва да зададете скоростта на предаване и в прозореца "Serial Monitor" (вижте стъпка 3 по-долу).

Обикновено инициализираме сериалния порт в `setup()`, тъй като той трябва да се изпълни само веднъж.

{% highlight C %}
void setup() {
    Serial.begin(9600); // отваря сериен порт, задава скорост на предаване на данни 9600 bps
}

void loop() {}
{% endhighlight C %}

#### Стъпка 2: Използвайте Serial.print и Serial.println за записване на данни

Ето цялостна програма, която записва "Hello world!” веднъж на всеки 500 ms.

{% highlight C %}
void setup() {
    Serial.begin(9600); // отваря сериен порт, задава скорост на предаване на данни 9600 bps
}

void loop() {
    Serial.println("Hello world!");
    delay(500);
}
{% endhighlight C %}

#### Стъпка 3: Отворете "Serial Monitor" в Arduino IDE

Накрая, за да видите входящите серийни данни, отворете Serial Monitor в Arduino IDE.

![](assets/images/BlinkWithSerialPrint_OpenSerialMonitor.png)

И трябва да видите нещо подобно на това:

![](assets/images/SerialPrintHelloWorld_SerialMonitor.png)

Пълният код е в GitHub [тук](https://github.com/makeabilitylab/arduino/blob/master/Basics/serial/SerialPrintHelloWorld/SerialPrintHelloWorld.ino).

### Отпечатване на променливи

Очевидно ще искате да отпечатате нещо повече от просто низове. Как да отпечатате променливи?

Простият отговор е да използвате няколко израза `Serial.print` и `Serial.println`. За да отпечатате променливи, поставете променливата като единствен параметър (вижте по-долу). По-сложен отговор можете да намерите в нашето ръководство [Inside Arduino] (inside-arduino.md). Можете да видите и примерния код на страницата на API [`Serial.print`](https://www.arduino.cc/reference/en/language/functions/communication/serial/print/).

По-долу сме написали проста програма за отпечатване на текущото време (в милисекунди) от момента, в който Arduino е бил включен и програмата ни е започнала да работи:

{% highlight C %}
void setup() {
    Serial.begin(9600); // отваря сериен порт, задава скорост на предаване на данни 9600 bps
}

void loop() {
    // Получава текущото време от стартирането на Arduino на нашата програма (в ms)
    unsigned long currentTimestampMs = millis();

    Serial.print("Време от стартирането на Arduino: ");
    Serial.print(currentTimestampMs);
    Serial.println(" ms");
    delay(500);
}
{% endhighlight C %}

![](assets/images/SerialPrintTimeStamp_ArduinoSerialMonitorScreenshot.png)

Този код е и в GitHub [тук](https://github.com/makeabilitylab/arduino/blob/master/Basics/serial/SerialPrintTimestamp/SerialPrintTimestamp.ino)

<!-- Форматиране на низ: https://cpp4arduino.com/2020/02/07/how-to-format-strings-without-the-string-class.html -->

## Модифицирайте кода си за мигане, за да използвате Serial.print

Сега нека се върнем към кода си за мигане и го модифицираме, за да използваме `Serial.print`, за да отпечатваме кога LED-ът е включен и кога е изключен. Ето моят пример.

<video autoplay loop muted playsinline style="margin:0px">
<source src="assets/movies/BlinkWithSerialPrint-IMG_5777_Trim_720p.mp4" type="video/mp4" />
</video>
**Видео.** Видео на програмата за мигане със сериен печат ([изходен код](https://github.com/makeabilitylab/arduino/blob/master/Basics/digitalWrite/BlinkWithSerialPrint/BlinkWithSerialPrint.ino)).
{: .fs-1 }

<!-- TODO: само за да подчертаем, че има и сериен плотер, покажете основен FSR с LED и сериен плотер -->

## Използване на вградения LED

В допълнение към `Serial.print`, можем да използваме и вградения LED на Arduino за бързо отстраняване на грешки (*например,* включете вградения LED, за да покажете състоянието на програмата, без да свързвате външна LED верига). При Arduino Uno и Leonardo вграденият LED е на пин 13. Така че, ако напишете `digitalWrite(13, HIGH);` в кода си, вграденият LED ще се включи. Тъй като не всички Arduino платки имат вграден LED на пин 13, трябва да използвате константата `LED_BUILTIN`, а не буквалния номер на пина.

![Изображение, показващо местоположението на вградения контролируем LED на Arduino Uno](assets/images/ArduinoUno_BuiltInLEDLocation.png)

Всъщност официалният [пример Arduino Blink](http://www.arduino.cc/en/Tutorial/Blink) използва вградения LED и константата `LED_BUILTIN`, за да демонстрира мигане. Това е и програмата, която се доставя с вашия Arduino и се изпълнява, когато го включите за първи път.

{% highlight C %}
// функцията setup се изпълнява веднъж, когато натиснете бутона за ресет или включите платка
void setup() {
    // инициализирайте цифровия пин LED_BUILTIN като изход.
    pinMode(LED_BUILTIN, OUTPUT);
}

// функцията loop се изпълнява отново и отново завинаги
void loop() {
    digitalWrite(LED_BUILTIN, HIGH); // включване на LED (HIGH е нивото на напрежението)
    delay(1000); // изчакване за една секунда
    digitalWrite(LED_BUILTIN, LOW); // изключване на LED чрез намаляване на напрежението до LOW
    delay (1000); // изчакайте една секунда
}
{% endhighlight C %}

Можете да достъпите този пример директно в Arduino IDE:

![Снимка на екрана с достъп до официалния пример Blink директно от Arduino IDE](assets/images/ArduinoIDE_FileMenuToBlinkExample.png)

## Следващ урок

Сега, когато знаем малко за отстраняването на грешки и [`Serial.print()`](https://www.arduino.cc/reference/en/language/functions/communication/serial/print/), е време да научим за ["аналоговия изход"]((led-fade.md)) на Arduino. Ще използваме `Serial.print()` през останалата част от нашите уроци.

<!-- В [следващия урок](led-fade.md) ще научим как да контролираме изходното напрежение не само на две нива, `LOW` (0V) или `HIGH` (5V), но и на по-фини нива между 0 и 5V, използвайки [`analogWrite(int pin, int value) `](https://www.arduino.cc/reference/en/language/functions/analog-io/analogwrite/). -->

<span class="fs-6">
[Предишна: Включване на LED с Arduino](led-on.md){: .btn .btn-outline }
[Следващо: Затъмняване на LED с Arduino](led-fade.md){: .btn .btn-outline }
</span>
