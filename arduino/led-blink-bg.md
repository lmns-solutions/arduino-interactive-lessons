---
lang: bg
permalink: /arduino/led-blink.html
page_id: arduino-led-blink
layout: default
title: L2&#58; Мигане на LED
nav_order: 2
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
В нашия [първи урок](led-on.md) директно свързахме LED верига към 5V и 3.3V пиновете на Arduino. Макар че това ни позволи да научим за захранващото напрежение и GND пиновете на Arduino и ни даде практически опит в свързването на електрически компоненти към портовете на Arduino, трябва да признаем, че това беше упражнение за забавление.

В този урок ще направим нещо по-вълнуващо: ще използваме Arduino, за да включим и изключим LED, като *програмно* контролираме изходното напрежение на един от GPIO пиновете на Arduino. С това започваме да се запознаваме с двата ключови аспекта на работата с микроконтролери: (1) изграждане на вериги и (2) писане на код за взаимодействие с тези вериги.

![Анимация, показваща LED, свързан с пин 3 на Arduino, който мига](assets/movies/Arduino_LEDBlink_Pin3.gif)

<!-- TODO: Да се добави версия, която издава тон за достъпност? 
Вижте: https://itp.nyu.edu/physcomp/labs/labs-arduino-digital-and-analog/digital-input-and-output-with-an-arduino/ -->

## Материали

Ще използвате същите материали като [по-рано](led-on.md), но ще ви е необходим и [Arduino IDE](https://www.arduino.cc/en/main/software) и USB кабел, за да качите програмата от компютъра си на Arduino.

| Arduino | LED | Резистор |
|:-----:|:-----:|:-----:|
| ![Arduino Uno]({{ site.baseurl }}/assets/images/ArduinoUno_Fritzing.png) | ![Червен LED]({{ site.baseurl }}/assets/images/RedLED_Fritzing.png) | ![220 Ohm резистор]({{ site.baseurl }}/assets/images/Resistor220_Fritzing.png) |
| Arduino Uno, Leonardo или подобен | Червен светодиод | 220Ω резистор |

## Изработване на веригата

Използвайте същия червен светодиод, обвит с резистор, както [по-рано](led-on.md#step-1-wrap-resistor-around-led-leg), и включете анода + резистора в пин 3, а катода в GND. Вижте схемата на свързване по-долу:

![Схема на свързване, показваща катода на светодиода, свързан към GND, и анода на светодиода, свързан към резистор 220 Ohm, а след това към пин 3](assets/images/Arduino_LEDBlink_Pin3Circuit.png)

{: .highlight }
**СЪВЕТ:**
Проверете отново, за да се уверите, че сте свързали правилно GND и пин 3. При изграждането на вериги е лесно да се объркате с един пин (досадна грешка!).

Макар че не е необходимо да използвате breadboard за тази проста верига, ето две функционално еквивалентни опции за свързване на базата на breadboard. Когато веригите ни станат по-сложни, ще ви е необходима платка за прототипи, затова е добре да започнете (или да продължите!) да се запознавате с нея. Кой дизайн на платка за прототипи ви се струва най-подходящ? Използвайте пръста си, за да проследите потока на тока от Pin 3 до GND. За да увеличите изображенията, можете да кликнете с десния бутон на мишката и да изберете "Отвори изображението в нов раздел".

| Вариант 1 на платка за прототипи | Вариант 2 на платка за прототипи |
|:----:|:-----:|
|![Схема на свързване на платка за прототипи, показваща катода на LED, свързан към GND, и анода на LED, свързан към резистор 220 Ohm, а след това към пин 3](assets/images/Arduino_LEDBlink_Pin3Circuit_Breadboard1.png) | ! [Втора схема на платка за прототипи, показваща катода на LED, свързан към GND, и анода на LED, свързан към резистор 220 ома, а след това към пин 3](assets/images/Arduino_LEDBlink_Pin3Circuit_Breadboard2.png) |

Винаги можете да се върнете към урока ни за [бредборда](../electronics/breadboards.md), за да освежите паметта си!

След това ще напишем код `C/C++` за микроконтролера на Arduino, за да включим LED от пин 3, което програмно ще настрои пин 3 на 5V.

{: .note }
Софтуерът на Arduino е с отворен код и се състои от среда за разработка (наречена IDE) и основни библиотеки. Основните библиотеки са написани на езиците за програмиране `C` и `C++` и са компилирани с avr-gcc и AVR libc. Изходният код за Arduino се хоства на [GitHub](https://github.com/arduino) . Библиотеките за AVR микроконтролери като ATmega328 (който използва Arduino Uno) се намират в [GitHub тук](https://github.com/arduino/ArduinoCore-avr).

## Получаване на Arduino IDE

Но първо трябва да изтеглим и инсталираме [Arduino IDE](https://www.arduino.cc/en/software/) (ако все още не сте го направили). Моля, следвайте нашите инструкции за инсталиране и персонализиране стъпка по стъпка [тук](arduino-ide.md).

## Въведение в цифровия изход

Сега ще напишем код, за да включим LED, като настроим Pin 3 на HIGH (или 5V). След това ще модифицираме този код, за да мига LED както при включване, така и при изключване. За да направим това, трябва да въведем **цифров изход.**

Arduino Uno има **20 пина за вход/изход с общо предназначение** ([GPIO](https://en.wikipedia.org/wiki/General-purpose_input/output)), които могат да се използват за цифров вход/изход (I/O) — т.е. за четене или записване на цифрова информация (`HIGH` или `LOW`) с помощта на [`digitalRead() `](https://www.arduino.cc/reference/en/language/functions/digital-io/digitalread/) и [`digitalWrite()`](https://www.arduino.cc/reference/en/language/functions/digital-io/digitalwrite/), съответно.

Можехме да изберем *което и да е* от тези пинове за този урок, но избрахме пин 3 (отчасти защото искаме да използваме същия пин в [Урок 4](led-fade.md) и използването му сега опростява нещата!).

<!-- ![Близък план на 14-те цифрови I/O пина на Arduino Uno](assets/images/ArduinoUno_CloseUp_DigitalIOPins.png) -->

![Близък план на 20-те цифрови I/O пина на Arduino Uno](assets/images/ArduinoUno_DigitalIOPins.png)

Можете да контролирате всеки от тези 20 цифрови I/O пина с три функции:

1. [`pinMode(int pin, int mode)`](https://www.arduino.cc/reference/en/language/functions/digital-io/pinmode/) конфигурира определен пин като `INPUT` или `OUTPUT`. В този случай искаме да зададем `OUTPUT`, защото искаме да **изведем** сигнал, за да включим LED.
2. [`digitalRead(int pin)`](https://www.arduino.cc/reference/en/language/functions/digital-io/digitalread/) чете цифров вход от зададения пин, или `HIGH`, или `LOW`. Ще разгледаме `digitalRead` в нашата поредица от уроци [Въведение във входа](intro-input.md).
3. [`digitalWrite(int pin, int value)`](https://www.arduino.cc/reference/en/language/functions/digital-io/digitalwrite/) записва цифров изход към посочения пин, или `HIGH`, или `LOW`. Ще използваме `digitalWrite` в този урок.

### Как преброихме 20 цифрови I/O пина?

Макар че бялата ситопечат върху Uno и Leonardo създава впечатлението, че тези платки имат само **14 цифрови I/O пина** (в горната част на платката), всъщност те имат **20**! Можете да проверите официалната [схема на пиновете на Arduino Uno](https://docs.arduino.cc/resources/pinouts/A000066-full-pinout.pdf) за проверка.

![Официалната схема на пиновете на Arduino Uno](assets/images/ArduinoUno_OfficialPinOutDiagram.png)

А ето и версия, в която цифровите I/O пинове са подчертани за по-голяма яснота:

![Официалната диаграма на Arduino Uno с маркирани 20 цифрови I/O пина](assets/images/ArduinoUno_OfficialPinOutDiagram_DigitalIOPinsMarked.png)

Същото важи и за Arduino Leonardo (вижте [официалната "схема на изводите" тук](https://content.arduino.cc/assets/Pinout-Leonardo_latest.pdf)):

![Официалната диаграма на Arduino Leonardo с маркирани 20 цифрови I/O пина](assets/images/ArduinoLeonardo_OfficialPinOutDiagram_DigitalIOPinsMarked.png)

Накрая, ето [симулация на верига Tinkercad](https://www.tinkercad.com/things/djhZYuYyqOR-using-all-20-gpio-pins-as-digital-out), която демонстрира използването на всички 20 цифрови I/O пина като цифров изход.

<video autoplay loop muted playsinline style="margin:0px">
<source src="assets/movies/ArduinoUno_UsingAll20GPIOPinsAsDigitalOutput.mp4" type="video/mp4" />
</video>
**Видео.** [Симулация на верига Tinkercad](https://www.tinkercad.com/things/djhZYuYyqOR-using-all-20-gpio-pins-as-digital-out), показваща как да използвате всички 20 GPIO пина като цифров изход на Arduino Uno. Можете да опитате симулацията сами [тук](https://www.tinkercad.com/ things/djhZYuYyqOR-using-all-20-gpio-pins-as-digital-out) и да видите кода в [GitHub тук](https://github.com/makeabilitylab/arduino/blob/master/Basics/digitalWrite/BlinkAll20Pins/BlinkAll20Pins.ino).
{: .fs-1 }

### Какво разбираме под HIGH и LOW?

Захранващото напрежение на Arduino често се обозначава като $$V_S$$, $$V_{CC}$$ и $$V_ {DD}$$ в техническите спецификации. За съжаление, не изглежда да има последователна конвенция за наименование ([link1](https://forum.arduino.cc/index.php?topic=374042.0), [link2](https://electronics.stackexchange.com/questions/17382/ what-is-the-difference-between-v-cc-v-dd-v-ee-v-ss)). Ще се опитаме да използваме последователно $$V_{CC}$$ или $$V_S$$, но понякога ще видите и други (например $$V_{DD}$$).

При Arduino Uno и Leonardo захранващото напрежение ($$V_{CC}$$) е **5V** . Така че, когато един пин е конфигуриран като изход чрез `pinMode(<pin>, OUTPUT)`, пинът може да предостави или `HIGH` напрежение ($$V_{CC}$$), или `LOW` напрежение (0V). Някои микроконтролери работят при 3.3V. В този случай, `HIGH` състоянието ще бъде 3.3V, но `LOW` състоянието ще остане 0V.

По-късно в този урок ще разгледаме реалните цифрови изходни сигнали на осцилоскоп (в раздела ["Как изглежда цифровият изход?"](#как-изглежда-цифровият-изход)).

### За какво можем да използваме цифровите изходни пинове?

Като цяло, цифровите изходни пинове на микроконтролерите са проектирани да изпращат **контролни сигнали**, а не да действат като **източници на захранване**. Така че, макар тези пинове да могат да доставят достатъчно ток за използване на светодиоди, пиезо високоговорители или за управление на серво мотори, ако трябва да управлявате високотоков DC товар, като например DC мотор, ще трябва да използвате транзистор – който е електронно управляван превключвател. 

Курсът ITP на NYU има [хубав урок](https://itp.nyu.edu/physcomp/labs/motors-and-transistors/using -a-transistor-to-control-high-current-loads-with-an-arduino/) за това как да използвате транзистор, външно захранване и Arduino за задвижване на DC мотор. За студентите, записани в нашите курсове, ще ви информираме кога ще ви е необходимо да направите това. Бъдете сигурни, че нито един от въвеждащите уроци не изисква тази конфигурация на веригата.

### Какъв е максималният ток, който може да подаде цифров изходен пин?

Arduino Uno използва микроконтролера [ATmega328P](http://ww1.microchip.com/downloads/en/DeviceDoc/Atmel-7810-Automotive-Microcontrollers-ATmega328P_Datasheet.pdf), а Leonardo използва [ATmega32U4](https://ww1. microchip.com/downloads/en/DeviceDoc/Atmel-7766-8-bit-AVR-ATmega16U4-32U4_Datasheet.pdf) – и двата могат да доставят абсолютен максимум от 0,04 A (40 mA) на цифров изходен пин или около ~4 LED паралелно (с 10 mA на клон).

Съгласно раздел 28.1 в [техническото описание на ATmega328P](http://ww1.microchip.com/downloads/en/DeviceDoc/Atmel-7810-Automotive-Microcontrollers-ATmega328P_Datasheet.pdf), всичко над тези граници "*може да причини трайно увреждане на чипа*". Максималният общ ток, консумиран **от всички I/O пинове** заедно, не трябва да надвишава 200mA. Това е същата граница за [ATmega32U4](https://ww1.microchip.com/downloads/en/DeviceDoc/Atmel-7766-8-bit-AVR-ATmega16U4-32U4_Datasheet.pdf).

Отново, тази граница не е от значение за нашите въвеждащи уроци (освен ако не се отклоните значително от тях).

Важно е, след като конфигурирате цифров I/O пин като `OUTPUT`, да не го свързвате директно с `GND` или $$V_{CC}$$, защото може да повредите микроконтролера (обикновено само този конкретен пин ще бъде повреден). Така например, ако случайно сте свързали пин 3 директно с 5V и напишете `pinMode (3, OUTPUT); digitalWrite(3, LOW);`, голямо количество ток ще "потъне" в пин 3 и потенциално ще повреди пина.

Може би си мислите: "А, какво?" Няма проблем. През годините, в които преподаваме, имаме много малко случаи на повредени Arduino поради претоварване с ток (въпреки че си струва да гледате това видео на ["5 Ways to Destroy an Arduino"](https://youtu.be/WmcMrKELkcs)). И не е нужно да се притеснявате за тези ограничения в нито един от въвеждащите уроци.

### Как Arduino вътрешно задава пина HIGH или LOW?

Въпреки че не е необходимо да разбирате следното, за да *използвате* Arduino, може би ви е любопитно как Arduino контролира напрежението на изхода на пина? Чрез транзистори. Както показва (опростената) схема по-долу, цифровият изходен пин осигурява $$V_{DD}$$ (5V на Uno и Leonardo) или $$GND$$ (0V) чрез динамично включване/изключване на транзистори (инвертор гарантира, че само един транзистор може да бъде включен едновременно).

![Опростена схема от Chuan-Zheng Lee, показваща, че изходният пин осигурява VDD или 0 V, като се свързва с VDD или земята чрез транзистор](assets/images/Arduino_DigitalOutputPin_Schematic.png)
Схема от Chuan-Zheng Lee за курса му ["Intro to Arduino"](https://web.stanford.edu/class/archive/engr/engr40m.1178/slides/arduino.pdf) в Станфорд.
{: .fs-1 }

## Включване на LED чрез пин 3

Добре, нека напишем първоначална програма, за да настроим пин 3 на `HIGH` (5V). Все още не мигаме – просто използваме код, за да настроим изходното напрежение на пин 3 на $$V_{CC}$$. 

### Стъпка 1: Стартирайте нов скиц в Arduino IDE

Стартирайте нов скиц в Arduino IDE:

![Снимка на Arduino IDE, показваща нов празен скиц](assets/images/ArduinoIDE_FreshSketch.png)

### Стъпка 2: Настройте pinMode за пин 3

Тъй като 20-те цифрови I/O пина могат да се използват **или** за **вход**, или за **изход**, трябва да посочим, че пин 3 трябва да се използва за *изход*. Това означава, че искаме Arduino да **изведе** 5V сигнал на пин 3, за да включи нашия LED. Конфигурираме пиновете в блока `setup()` и използваме командата [`pinMode(int pin, int mode)`](https://www.arduino.cc/reference/en/language/functions/digital-io/pinmode/), която приема пин като първи параметър и режим (`INPUT` или `OUTPUT`) като втори.

{% highlight C %}
void setup() {
    // поставете тук кода за настройка, който да се изпълни веднъж:
    pinMode(3, OUTPUT);
}
{% endhighlight C %}

### Стъпка 3: Настройте пин 3 на HIGH

Накрая, трябва да настроим сигнала на пин 3 на `HIGH`. За целта използваме командата [`digitalWrite(int pin, int value)`](https://www.arduino.cc/reference/en/language/functions/digital-io/digitalwrite/), която приема пин като първи параметър и стойност (`HIGH` или `LOW`) като втори. Можем да направим това или в `setup()`, или в `loop()`, но тъй като в момента не променяме изходния сигнал, няма причина да го поставяме в `loop()`, така че нека го поставим в `setup()` заедно с кода `pinMode`.

{% highlight C %}
void setup() {
    // поставете тук кода за настройка, който да се изпълни веднъж:
    pinMode(3, OUTPUT);
    digitalWrite(3, HIGH); // включете LED (изход 5V)
}
{% endhighlight C %}

### Стъпка 4: Компилиране на кода

Успяхме! Сега е време да компилираме и качим кода в Arduino.

Компилирайте кода, като кликнете върху бутона с отметка "verify" в горния ляв ъгъл на Arduino IDE. Ако все още не сте го направили, Arduino IDE ще ви помоли да запазите скицата си. Ако има синтаксисни или други идентифицируеми грешки в кода, Arduino IDE ще ги отпечата в прозореца на конзолата в долната част.

![Анимация, показваща как да компилирате и запазите скица в Arduino IDE](assets/movies/ArduinoIDE_Compile.gif)

### Стъпка 5: Качете кода в Arduino

Накрая, качете кода в Arduino, като кликнете върху бутона "дясна стрелка" (до бутона "verify"). Важно е да сте настроили вашата Arduino платка и порт съответно в `Tools->Board` и `Tools->Port`.

![Снимка на екрана, показваща къде се намира бутонът за качване (вдясно от бутона за потвърждение)](assets/images/ArduinoIDE_UploadCodeButton.png)

След като качването приключи, кодът автоматично се изпълнява на Arduino и LED индикаторът трябва да се включи веднага!

<video controls="controls">
<source src="assets/movies/ArduinoUno_TurnOnLEDPin3_WorkbenchWithCode-Cropped.mov" type="video/mp4">
</video>
**Забележка:** На моя Windows компютър използвам [тъмна тема](https://create.arduino.cc/projecthub/konradhtc/one-dark-arduino-modern-dark-theme-for-arduino-ide-2fca81) за Arduino IDE.
{: .fs-1 }

Ето една илюстративна анимация на това, което се случва във вашата верига, когато Arduino задвижва Pin 3 `HIGH`—надяваме се, че това съответства и на вашето концептуално разбиране:

![Анимация, показваща включването на LED на Pin 3)](assets/movies/Arduino_LEDTurnOn_Pin3ArduinoPluggedIn-Cropped.gif)

## Включване и изключване на LED чрез пин 3

Сега нека модифицираме кода си, за да включваме *и* изключваме LED чрез програмата. По-конкретно, ще редуваме включването на LED за една секунда и изключването му за една секунда. За да направим това, ще използваме функцията [`delay(int ms)`](https://www.arduino.cc/ reference/en/language/functions/time/delay/), която спира програмата за определено време (в милисекунди).

### Стъпка 1: Преместете кода digitalWrite от setup() в loop()

Първо, преместете кода digitalWrite от `setup()` в `loop()`:

{% highlight C %}
void setup() {
    // задайте Pin 3 като изход
    pinMode (3, OUTPUT);
}

void loop() {
    digitalWrite(3, HIGH); // включете LED (изход 5V)
}
{% endhighlight C %}

### Стъпка 2: Добавете закъснения и код за изключване на LED

Сега добавете код за пауза (за една секунда) и след това изключете LED (за една секунда) с помощта на `delay()`. Не забравяйте, че когато `loop()` приключи, той автоматично се извиква отново (което кара LED да мига непрекъснато).

{% highlight C %}
void setup() {
    // задайте Pin 3 като изход
    pinMode(3, OUTPUT);
}

void loop() {
    digitalWrite(3, HIGH); // включете LED (изход 5V)
    delay(1000); // изчакайте една секунда
    digitalWrite(3, LOW); // изключете LED (изход 0V)
    delay(1000); // изчакайте още една секунда
}
{% endhighlight C %}

### Стъпка 3: Компилиране и качване

Готово! Сега компилирайте и качите кода и вижте как работи!

<video controls="controls">
<source src="assets/movies/BlinkWithCodeAndWorkbenchCamera.mp4" type="video/mp4">
</video>

### Стъпка 4: Заменете константите

Обикновено искаме да ограничим използването на *литерални константи* в кода си и да ги заменим с променливи. В този случай нека заменим `3` с `LED_OUTPUT_PIN`, дефинирана като глобална променлива в началото на програмата ни (`const int LED_OUTPUT_PIN = 3;`). Това ще направи кода ни по-лесен за поддръжка, по-разбираем и по-малко податлив на случайни грешки. Опитайте се да правите това за всички литерали в бъдеще.

{% highlight C %}
const int LED_OUTPUT_PIN = 3;
void setup() {
    // задайте Pin 3 за изход
    pinMode(LED_OUTPUT_PIN, OUTPUT);
}

void loop() {
    digitalWrite(LED_OUTPUT_PIN, HIGH); // включване на LED (изход 5V)
    delay(1000); // изчакване една секунда
    digitalWrite(LED_OUTPUT_PIN, LOW); // изключване на LED (изход 0V)
    delay(1000); // изчакване още една секунда
}
{% endhighlight C %}

### Разглеждане на кода

Как работи това? Вижте видеото с разглеждане на кода по-долу:

<video controls="controls">
<source src="assets/movies/Arduino_BlinkWithCode_Pin3.mp4" type="video/mp4">
</video>

### Нашият код Blink е в GitHub

Можете да получите достъп до нашия код Blink в нашето [Arduino GitHub хранилище](https://github.com/jonfroehlich/arduino). "Жива” версия е вградена директно от GitHub хранилището по-долу.

<!-- gist-it не работи, затова сега използваме emgithub -->
<!-- <script src="https://gist-it.appspot.com/https://github.com/jonfroehlich/arduino/blob/master/Basics/digitalWrite/Blink/Blink.ino?footer=minimal"></script> -->
<script src="https://emgithub.com/embed.js?target=https%3A%2F%2Fgithub.com%2Fjonfroehlich%2Farduino%2Fblob%2Fmaster%2FBasics%2FdigitalWrite%2FBlink%2FBlink.ino&style=github&showCopy=on"></script>

Този [изходен код](https://github.com/jonfroehlich/arduino/blob/master/Basics/digitalWrite/Blink/Blink.ino) се намира в GitHub.
{: .fs-1 }

## Как изглежда цифровият изход?

Често задаван и важен въпрос при първата работа с микроконтролери е: как изглежда цифровият изход?

Представете си как изглежда напрежението на изход 3 във времето (ос Х е времето, а ос Y е изходното напрежение). Трябва да си представите изходен сигнал 5V `HIGH` за продължителността на закъснението, последван от изходен сигнал 0V, който е `LOW` продължителност на закъснението. Всъщност, този тип графика е точно това, за което служи осцилоскопът – той изобразява стойностите на напрежението във времето.

С помощта на Tinkercad Circuits създадохме същата LED-базирана верига като горната, на която работи програмата Blink, и я свързахме с осцилоскоп. След това записахме различни стойности на "забавяне" (400, 200 и 50) и създадохме този филм. Графиката отговаря ли на очакванията ви? Защо да или защо не? Препоръчваме да отворите видеото в отделен прозорец или да го гледате на цял екран, за да видите подробностите.

<video autoplay loop muted playsinline style="margin:0px">
<source src="assets/movies/LedBlinkOscilliscope_TinkercadCircuits_Trim.mp4" type="video/mp4" />
</video>
**Видео.** Видео на този [проект в Tinkercad](https://www.tinkercad.com/things/17q2GFeYwP9) с три различни стойности на `забавяне` за `HIGH` и `LOW`: 400, 200 и 50.
{: .fs-1 }

Препоръчваме ви да си поиграете с този [Tinkercad проект](https://www.tinkercad.com/things/17q2GFeYwP9) и да проучите различните закъснения и тяхното изходно ниво на осцилоскопа.
 

<iframe width="725" height="453" src="https://www.tinkercad.com/embed/17q2GFeYwP9?editbtn=1" frameborder="0" marginwidth="0" marginheight="0" scrolling="no"></iframe>

### Настройка и визуализация на различни честоти на мигане

Ние дублирахме горната настройка на Tinkercad (верига + осцилоскоп) в нашата лаборатория и записахме видео. Забележително е, че използвахме малко по-различен [код](https://github.com/ makeabilitylab/arduino/blob/master/Basics/digitalWrite/SettableBlinkWithoutDelay/SettableBlinkWithoutDelay.ino), който ни позволява да настроим честотата на мигане чрез завъртане на [потенциометър](../electronics/variable-resistors.md).

<iframe width="736" height="414" src="https://www.youtube.com/embed/_ByA8Q-hL8I" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

**Видео** [Видео](https://youtu.be/_ByA8Q-hL8I), показващо цифровата форма на напрежението на изхода при различни честоти на "мигане".
{: .fs-1 }

Можете да си поиграете с Tinkercad версията на този експеримент [тук](https://www.tinkercad.com/things/42O2UlRJFrZ):

![](assets/images/SettableBlinkLedOnAndOffWithOscilliscope_Tinkercad.png)
**Фигура**. Tinkercad Circuits версия на настройваемата верига за забавяне + код ([link](https://www.tinkercad.com/things/42O2UlRJFrZ)).
{: .fs-1 }

## Проверка на менталния модел: кодът е зареден и работи на Arduino

Като бърза проверка на менталния модел, си струва да се подчертае, че след като качите кода на Arduino, вече нямате нужда от USB кабел. Защо? Защото компилираната версия на кода се съхранява **локално** на Arduino и остава там, дори когато Arduino загуби захранване. Вашият Arduino *е* компютърът! Така че можете да използвате друг източник на захранване, като 9V батерия, включена в портът за барел жак.

<video controls="controls">
<source src="assets/movies/Arduino_LEDBlink_Pin3-9VPower.mp4" type="video/mp4">
</video>

## Мигане без използване на delays()

Преди да продължим, струва си да подчертаем, че като цяло дългите `delay ()` трябва да се избягват. Защо? Защото докато е в `delay()`, Arduino вече не отговаря. Така че, например, представете си, че актуализирате програмата си Blink, за да реагира и на натискане на бутон от потребителя. Ако потребителят натисне бутона, докато Arduino е в `delay()`, програмата ви никога няма да може да обработи, че бутонът е бил натиснат! Това е проблем.

---
**ЗАБЕЛЕЖКА:**

Можете да спрете дотук и да преминете към [следващия урок](serial-print. md). Достатъчно е да **знаете**, че дългите `delay()` повиквания могат да бъдат опасни и вероятно трябва да се избягват. Ако обаче сте любопитни, можете да продължите с тази подсекция, за да видите пример за Blink, който работи без забавяния. Ще се върнем към тази концепция в последния ни урок [Въведение в изхода](intro-output.md) за [светодиоди с многоскоростно мигане](led-blink3.md).

Ако искате да знаете как всъщност работи `delay()`, прочетете ["Какво всъщност прави delay()"](inside-arduino.md#what-does-delay-actually-do) в нашето [ръководство Inside Arduino](#inside-arduino).

---

Тъй като използването на `delay()` може да бъде толкова проблематично, като част от своята серия от въвеждащи уроци, Arduino публикува друг пример за мигане с урок, наречен [BlinkWithoutDelay](https://www.arduino.cc/en/Tutorial/BlinkWithoutDelay). Както и при обичайното [Blink](http://www.arduino.cc/en/Tutorial/Blink), този пример може да бъде достъпен директно в Arduino IDE:

![Снимка на екрана с директен достъп до официалния пример BlinkWithoutDelay от Arduino IDE](assets/images/ArduinoIDE_FileMenuToBlinkWithoutDelayExample.png)

За да се избегнат извикванията на `delay()`, кодът проследява **времето**, **промените в състоянието на LED** (когато LED преминава от `HIGH` към `LOW` или от `LOW` към `HIGH`) и **кога** се случват тези промени в състоянието. Основният цикъл на [BlinkWithoutDelay](https://www.arduino.cc/en/Tutorial/BlinkWithoutDelay) е показан по-долу. Обърнете внимание, че няма `delay ()`!

{% highlight C %}
void loop() {
    // проверете дали е време да мигне LED; т.е. дали разликата
    // между текущото време и последното мигане на LED е по-голяма от
    // интервала, в който искате да мига LED.
    unsigned long currentMillis = millis();

    if (currentMillis - previousMillis >= interval) {
        // запазете последния път, когато сте мигали LED
        previousMillis = currentMillis;

        // ако LED е изключен, включете го и обратното:
        if (ledState == LOW) {
            ledState = HIGH;
        } else {
            ledState = LOW;
        }

        // настройте LED с ledState на променливата:
        digitalWrite(ledPin, ledState);
    }
}
{% endhighlight C %}

Също така създадохме наша собствена версия [BlinkWithoutDelay](https://github.com/makeabilitylab/arduino/blob/master/Basics/digitalWrite/BlinkWithoutDelay/BlinkWithoutDelay.ino), която е достъпна на [GitHub](https://github.com/makeabilitylab/arduino/blob/master/Basics/digitalWrite/BlinkWithoutDelay/BlinkWithoutDelay.ino) и е показана по-долу. Тази версия е функционално еквивалентна на официалния пример на Arduino, но използва нашия собствен стил на кодиране и, по наше мнение, е по-разбираема.

<!-- gist-it не работи, затова сега използваме emgithub -->
<!-- <script src="https://gist-it.appspot.com/https://github.com/makeabilitylab/arduino/blob/master/Basics/digitalWrite/BlinkWithoutDelay/BlinkWithoutDelay.ino?footer=minimal"></script> -->

<script src="https://emgithub.com/embed.js?target=https%3A%2F%2Fgithub.com%2Fmakeabilitylab%2Farduino%2Fblob%2Fmaster%2FBasics%2FdigitalWrite%2FBlinkWithoutDelay%2FBlinkWithoutDelay.ino&style=github&showCopy=on"></script>

Този [изходен код](https://github.com/makeabilitylab/arduino/blob/master/Basics/digitalWrite/BlinkWithoutDelay/BlinkWithoutDelay.ino) се намира в GitHub.
{: .fs-1 }

## Следващ урок

В [следващия урок](serial-print.md) ще научим няколко основни стратегии за отстраняване на грешки, преди да преминем към [аналоговия изход](led-fade.md), който ни позволява да контролираме изходното напрежение не само на две нива, `LOW` (0V) или `HIGH` (5V), но и на по-фини нива между 0 и 5V, използвайки [`analogWrite(int pin, int value)`](https://www.arduino.cc/reference/en/language/functions/analog-io/analogwrite/). 

<!-- В [следващия урок](led-fade.md) ще научим как да контролираме изходното напрежение не само на две нива, `LOW` (0V) или `HIGH` (5V), но и на по-фини нива между 0 и 5V, използвайки [`analogWrite(int pin, int value)`] (https://www.arduino.cc/reference/en/language/functions/analog-io/analogwrite/). -->

<span class="fs-6">
[Предишна: Включване на LED с Arduino](led-on.md){: .btn .btn-outline }
[Следващо: Отстраняване на грешки в кода на Arudino с Serial.print](serial-print.md){: .btn .btn-outline }
<!-- [Следващо: Затъмняване на LED с Arduino](led-fade.md){: .btn .btn-outline } -->
</span>

