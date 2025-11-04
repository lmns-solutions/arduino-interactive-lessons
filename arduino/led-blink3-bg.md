---
lang: bg
permalink: /arduino/led-blink3.html
page_id: arduino-led-blink3
layout: default
title: L8&#58; Мигащи светодиоди
parent: Изход
grand_parent: Въведение в Arduino
usemathjax: false
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

В този урок ще научим как да мигаме няколко светодиода с различна честота и да създадем първия си [C/C++ клас](http://www.cplusplus.com/doc/tutorial/classes/), който значително ще опрости кода ни и, като допълнителен бонус, ще намали размера му, като елиминира излишния код! 

Както и в предишния урок за [преливане на RGB светодиоди](rgb-led-fade.md), този урок включва **прости вериги**, но сравнително **сложен код**. Често, когато използваме микроконтролери, кодът ни е магическата съставка – веригите са прости, но кодът може да бъде сложен.

![Анимиран GIF от видеозапис на работна маса, показващ BlinkMultiple.ino](assets/movies/ArduinoUno_BlinkMultiple_Workbench.gif)

## Контекст

Каноничният и обичан **първи Arduino скиц**, [Blink](https://www.arduino.cc/en/tutorial/blink), позволява на начинаещите бързо да създават и пишат код за верига. Кодът изглежда нещо като това, което разгледахме в нашия [урок за Blink](led-blink.md):

{% highlight C %}
void setup() {
    // задайте Pin 3 за изход
    pinMode(3, OUTPUT);
}

void loop() {
    digitalWrite(3, HIGH); // включете LED (изход 5V)
    delay(1000); // изчакайте една секунда
    digitalWrite(3, LOW); // изключете LED (изход 0V)
    delay(1000); // изчакайте още една секунда
}
{% endhighlight C %}

Мигането е лесно. Това е удовлетворяващо. Но... то създава погрешен ментален модел за това как да структурираме програми и кога/как да използваме [`delay()`](https://www.arduino.cc/reference/en/language/functions/time/delay/).

Ами ако искате да мигате няколко LED-а с **различна честота**? Как бихте направили това с `delay()`? Е, **не можете.** Докато сте в `delay()`, програмата ви буквално *не прави нищо* (е, заседнала е в `while` цикъл, чакайки да приключи периодът на забавяне, но това по същество е нищо).

И така, какво да направим вместо това? **Елиминираме всички закъснения** и проследяваме времето и състоянието с помощта на [състоятелни машини](https://en.wikipedia.org/wiki/Finite-state_machine). Като алтернатива можем да използваме прекъсвания (но ще разгледаме това по-късно).

## Материали

Ще ви трябват **три LED диода** – ние ще използваме червен, син и жълт, но можете да използвате каквито LED диоди искате – заедно с резистори за ограничаване на тока, платка за прототипи и Arduino.

| Платка за прототипи | Arduino | Три LED диода | Три резистора |
|:-----:|:-----:|:-----:|:-----:|
| ![Платка за прототипи]({{ site.baseurl }}/assets/images/Breadboard_Half.png) | ![Arduino Uno]({{ site.baseurl }}/assets/images/ArduinoUno_Fritzing.png) | ![RGB светодиод]({{ site.baseurl }}/assets/images/RedBlueYellowLEDs_Fritzing_120w.png) | ![220-ом резистор]({{ site.baseurl }}/assets/images/Resistor220_Fritzing.png) |
| Breadboard | Arduino Uno, Leonardo или подобен | Три LED (ще използваме червен, син и жълт) | **Три** 220Ω резистори |

## Верига

Веригата е същата като в нашия основен [урок за мигане на светодиоди](led-blink.md), но я дублираме три пъти – по веднъж за всеки светодиод. Можем да използваме всеки от GPIO пиновете на Arduino, но избрахме пинове 2, 5 и 9, просто за да разделим веригата и да я направим по-лесна за четене.

Досега тази схема и окабеляване би трябвало да ви са познати. Всъщност, може би дори нямате нужда от такава схема за окабеляване!

![Схема за окабеляване на три LED, свързани към пинове 2, 5 и 9 (с аноди, обърнати към пиновете, и катоди, свързани към GND с резистори за ограничаване на тока)](assets/images/ArduinoUno_LEDBlink3_WiringDiagramWithSchematic.png)

Припомнете си, че всеки цвят LED има уникално напрежение Vf. В този случай, нашият червен LED има Vf между 2,0-2,4V, нашият син LED между 3,0-3,4V, а нашият жълт LED между 2,0-2,4V. За да опростим нещата, ще използваме същия резистор за всяка LED верига (220Ω); обаче, можете да използвате различни резистори за всеки LED, за да опитате да балансирате нивата на яркост.

![Изображение на многоцветния LED пакет на Sparkfun, показващ различни Vfs за различните цветове LED](assets/images/SparkfunMulticolorLEDPack.png)
[Асортиран пакет LED ](https://www.sparkfun.com/products/12062) от Sparkfun.com, който показва Vdrop (или Vf) за всеки LED.
{: .fs-1 }

## Написване на код

Ще приложим два подхода за мигане с няколко скорости:

1. Първият въвежда общата идея за използване на променливи за проследяване на състоянието и времеви отметки за промяна на състоянието, за да се контролира изходът на времето без `delays()`.
2. Вторият ще използва същия подход, но опростен чрез обектно-ориентирано програмиране. Тук ще ви покажем и как да създадете и използвате клас `C++` в Arduino.

### Многоскоростно мигане: първоначален подход

За нашия първоначален подход се нуждаем от четири неща за всеки светодиод:

1. **Номер на пин:** Целочислена стойност, определяща изходния пин.
2. **Интервал на мигане:** *Интервал* за всеки светодиод, който контролира колко дълго да се включва (`HIGH`) и изключва (`LOW`) светодиодът.
3. **Времева марка на превключване:** *последният път, когато светодиодът е бил превключен* от `HIGH` на `LOW` или от `LOW` на `HIGH`.
4. **Текущо състояние на светодиода:** *текущото състояние на светодиода* (`HIGH` или `LOW`), което се превключва на всеки интервал на мигане.

#### Интервал на мигане

За **интервала на мигане** ще използваме `const` променливи като `LED1_BLINK_INTERVAL_MS`, `LED2_BLINK_INTERVAL_MS` и `LED3_BLINK_INTERVAL_MS`

{% highlight C %}
const int LED1_OUTPUT_PIN = 2;
const int LED1_BLINK_INTERVAL_MS = 200; // интервал, през който да мига LED1 (в милисекунди)

const int LED2_OUTPUT_PIN = 5;
const int LED2_BLINK_INTERVAL_MS = 333; // интервал, през който да мига LED2 (в милисекунди)

const int LED3_OUTPUT_PIN = 9;
const int LED3_BLINK_INTERVAL_MS = 1111; // интервал, през който да мига LED3 (в милисекунди)
{% endhighlight C %}

#### Превключване на времеви отметки и състояния на LED

За **превключването на времеви отметки** и **състояния на LED** ще използваме променливи като `_led1LastToggledTimestampMs` и `_led1State`. Можем да превключим `ledState` просто с: `ledState = !ledState`.

{% highlight C %}
unsigned long _led1LastToggledTimestampMs = 0; // проследява последния път, когато LED1 е бил актуализиран
int _led1State = LOW; // ще превключва между LOW и HIGH

unsigned long _led2LastToggledTimestampMs = 0; // проследява последния път, когато LED2 е бил актуализиран
int _led2State = LOW; // ще превключва между LOW и HIGH

unsigned long _led3LastToggledTimestampMs = 0; // проследява последния път, когато LED3 е бил актуализиран
int _led3State = LOW; // ще превключва между LOW и HIGH
{% endhighlight C %}

За да заснемем времевите отметки, ще използваме функцията [`millis()` ](https://www.arduino.cc/reference/en/language/functions/time/millis/) на Arduino, която връща "*броя **милисекунди**, изминали от момента, в който Arduino платка е започнала да изпълнява текущата програма*” като `unsigned long`.
 

В Arduino типът данни `unsigned long` е 32 бита (4 байта), който варира от `0` до `4,294,967,295` (2^32 - 1) . По този начин `millis()` ще прелее – ще се върне на нула и ще започне отново – след `4,294,967,295` милисекунди (или приблизително 50 дни). Ако се нуждаете от по-прецизно време, можете да използвате `micros()`, която осигурява **микросекундна резолюция**, а не милисекундна, но `micros()` прелива на всеки ~70 минути.

#### Мигане без логика за забавяне

След това използваме същата обща логика като "мигане без забавяне" [разгледано по-рано](led-blink#blink-without-using-delays) за всеки LED:

{% highlight C %}
unsigned long currentTimestampMs = millis();

// Проверяваме дали сме достигнали интервала на превключване за LED1 
if (currentTimestampMs - _led1LastToggledTimestampMs >= LED1_BLINK_INTERVAL_MS) {
    _led1LastToggledTimestampMs = millis();
    _led1State = !_led1State;
    digitalWrite(LED1_OUTPUT_PIN, _led1State);
}

// Проверка дали сме достигнали интервала на превключване за LED2
if (currentTimestampMs - _led2LastToggledTimestampMs >= LED2_BLINK_INTERVAL_MS) {
    _led2LastToggledTimestampMs = millis();
    _led2State = !_led2State;
    digitalWrite(LED2_OUTPUT_PIN, _led2State);
}...

 // и така нататък, копирайте горния блок код за всеки LED, който искате да мига
{% endhighlight C %}

#### Проследяване на времеви отметки и препълване

Тази подсекция предоставя повече информация за проследяването на времеви отметки и препълване. Можете да пропуснете тази част, ако желаете.

Важен въпрос, който трябва да си зададете, е: какво ще се случи, ако Arduino трябва да работи повече от ~50 дни и аз разчитам на `millis() ` за проследяване на времето? Ще продължи ли да работи математическото изваждане (`currentTimestampMs - _lastToggledTimestampMs >= LED_BLINK_INTERVAL_MS`)? Дори при препълване?

Отличен въпрос! И да, ще продължи да работи! Причината е, че използваме `unsigned` типове данни, които информират компилатора, че тези стойности никога не могат да бъдат `< 0`. Това е от решаващо значение.

Например, представете си, че `_lastToggledTimestampMs` е `4,294,967,290` или `0xFFFFFFFA` в шестнадесетичен формат (32 бита), което е на 5 милисекунди от препълване. А след това си представете, че `millis()` се препълва (връща се обратно на 0) и `currentTimestampMs` става, да речем, `1` или `0x00000001`. Така че нашето изваждане е: `0x00000001 - 0xFFFFFFFA`. Между тези две числа има разлика от `7` милисекунди, така че бихме искали изваждането да даде резултат `7`:

```
1. 0xFFFFFFFA
2. 0xFFFFFFFB
3. 0xFFFFFFFC
4. 0xFFFFFFFD
5. 0xFFFFFFFE
-. (0xFFFFFFFF) <-- препълване
6. 0x00000000
7. 0x00000001
```

И ето какво получаваме! Можете да експериментирате сами, като изпълните кода по-долу на вашия Arduino. Препоръчваме ви също така [тази статия](https://www.baldengineer.com/arduino-millis-plus-addition-does-not-add-up.html) от Джеймс Луис за `millis()`, препълване и аритметика за повече информация.
 

{% highlight C %}
unsigned long _lastToggledTimestampMs = 4294967290; // променете това, за да експериментирате с препълване

void setup() {
    Serial.begin(9600);
    delay(2000);
}

void loop() {

    unsigned long currentTimestampMs = 1;
    unsigned long diff = currentTimestampMs - _lastToggledTimestampMs;

    Serial.println("Разликата между: currentTimestampMs - lastToggledTimestampMs е: ");
    Serial.print(currentTimestampMs);
    Serial.print(" - ");
    Serial.print(_lastToggledTimestampMs);
    Serial.print(" = ");
    Serial.println(diff);
    wait(1000);

    _lastToggledTimestampMs++;
}
{% endhighlight C %}

#### Пълен код за мигане с няколко скорости

Добре, сега обратно към кода. Ето пълният код за мигане с няколко скорости:

<!-- gist-it не работи, затова сега използваме emgithub -->
<!-- <script src="https://gist-it.appspot.com/https://github.com/makeabilitylab/arduino/blob/master/Basics/digitalWrite/BlinkMultiple/BlinkMultiple.ino?footer=minimal"></script> -->

<script src="https://emgithub.com/embed.js?target=https%3A%2F%2Fgithub.com%2Fmakeabilitylab%2Farduino%2Fblob%2Fmaster%2FBasics%2FdigitalWrite%2FBlinkMultiple%2FBlinkMultiple.ino&style=github& showCopy=on"></script>

Този [изходен код](https://github.com/makeabilitylab/arduino/blob/master/Basics/digitalWrite/BlinkMultiple/BlinkMultiple.ino) се намира в GitHub.
{: .fs-1 }

#### Видео на Workbench

<iframe width="736" height="414" src="https://www.youtube.com/embed/8DHhmXr3mC8" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

### Мигане с няколко скорости: обектно-ориентиран подход

Предвид количеството излишен код и споделената логика и структура, горното решение е силен кандидат за преструктуриране във функции или класове. Да го направим! 

Ще дефинираме нов клас, наречен `Blinker`, който значително ще опрости кода ни, ще намали излишъка (и потенциала за човешка грешка) и дори ще направи компилирания ни код по-малък (от 1118 на 1042 байта програмно пространство за съхранение). 

След като създадем класа `Blinker`, основният ни код се редуцира до:

{% highlight C++ %}
Blinker _led1Blinker(2, 200); // задайте пин и интервал на мигане (200 ms)
Blinker _led2Blinker(5, 333); // задайте пин и интервал на мигане (333 ms)
Blinker _led3Blinker(9, 1111); // определяне на пин и интервал на мигане (1111 ms)

// Функцията setup се изпълнява веднъж, когато натиснете бутона за ресет или включите платка
void setup() {
    // празно 
}

// Функцията loop се изпълнява отново и отново безкрайно
void loop() {
    _led1Blinker.update();
    _led2Blinker.update();
    _led3Blinker.update();
}
{% endhighlight C++ %}

Но първо трябва да създадем класа `Blinker`, което правим по-долу!

#### Създаване на класа Blinker

Ако сте запознати с обектно-ориентираното програмиране и декларирането и използването на класове в `Java`, `C#`, `Python` и дори до известна степен `JavaScript`, тъй като [ECMAScript 2015](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Classes), тогава класовете в `C++` ще ви се сторят познати (но със сигурност имат свои особености). Класовете в `C++` имат име на клас, променливи членове, функции членове и, подобно на `C#` и `Java`, спецификатори за достъп (*например* private, public). За кратко упътване вижте тези връзки ([link1](https://www.geeksforgeeks.org/c-classes-and-objects/), [link2](http://www.cplusplus.com/doc/tutorial/classes/)).

За да създадем нашия клас Blinker, не забравяйте, че ни трябват четири неща за всеки LED:
1. **Номер на пин:** Целочислена стойност, определяща изходния пин.
2. **Интервал на мигане:** *Интервал на мигане*, който контролира колко дълго да се включва (`HIGH`) и изключва (`LOW`) всеки LED.
3. **Време на превключване:** *последният път, когато светодиодът е бил превключен* от `HIGH` на `LOW` или от `LOW` на `HIGH`. 
4. **Текущо състояние на светодиода:** *текущото състояние на светодиода* (`HIGH` или `LOW`), което се превключва на всеки интервал на мигане.

За класа `Blinker` просто ще превърнем тези четири неща в променливи на членовете:

{% highlight C++ %}
class Blinker{

private:
    const int _pin; // изходен пин
    const unsigned long _interval; // интервал на мигане в ms

    int _state; // текущо състояние (HIGH или LOW)
    unsigned long _lastToggledTimestamp; // последно превключване на състоянието в ms...

// още тук
{% endhighlight C++ %}

Накрая, имаме нужда от две функции: `constructor` и `update()`—последната се занимава с основната ни логика и кода за превключване и е предназначена да се извиква веднъж на всеки цикъл `loop()`. Ще ги декларираме в самата дефиниция на класа:

{% highlight C++ %}
public:
    // Конструктор
    Blinker(int pin, unsigned long blinkInterval) :
    _pin(pin), _interval(blinkInterval) // инициализирайте const по този начин в C++
    {
        _state = LOW;
        _lastToggledTimestamp = 0;
        pinMode(_pin, OUTPUT);
    }

    /**
    * Изчислява дали да превключи състоянието на изхода въз основа на зададения интервал
    * Извикайте тази функция веднъж на loop()
    */ 
    void update(){
        unsigned long currentTimestampMs = millis();

        if (currentTimestampMs - _lastToggledTimestamp >= _interval) {
            _lastToggledTimestamp = currentTimestampMs;
            _state = !_state;
            digitalWrite(_pin, _state);
        }
    }
}
{% endhighlight C++ %}

За да използвате класа `Blinker` (както е показано по-горе), той трябва да бъде дефиниран във вашия `.ino` скиц в началото на файла (преди да опитате да инстанциирате обект Blinker). По-късно ще покажем и как да създадете клас, който съществува в собствените си `.h` и `.cpp` файлове.

#### Пълен код на Blinker

Така че целият код изглежда така:

<!-- gist-it не работи, затова сега използваме emgithub -->
<!-- <script src="https://gist-it.appspot.com/https://github.com/makeabilitylab/arduino/blob/master/Basics/digitalWrite/BlinkMultipleWithInternalClass/BlinkMultipleWithInternalClass.ino?footer=minimal"></script> -->

<script src="https://emgithub.com/embed.js?target=https%3A%2F%2Fgithub.com%2Fmakeabilitylab%2Farduino%2Fblob%2Fmaster%2FBasics%2FdigitalWrite%2FBlinkMultipleWithInternalClass%2FBlinkMultipleWithInternalClass.ino& style=github&showCopy=on"></script>

Този [изходен код](https://github.com/makeabilitylab/arduino/blob/master/Basics/digitalWrite/BlinkMultipleWithInternalClass/BlinkMultipleWithInternalClass.ino) се намира в GitHub.
{: .fs-1 }

### Многоскоростно мигане: използване на външен клас

В `C++`, вие декларирате променливи членове и сигнатури на функции в `.h` файл, а имплементациите на функциите в `.cpp` файл. Това често е по-чисто решение, отколкото вграждането на класове в самия `.ino`. 

Всъщност, ако преместим `Blinker` в отделни `.h` и `.cpp` файлове, тогава пълният `.ino` скиц просто изглежда така:

<!-- gist-it не работи, затова сега използвам emgithub -->
<!-- <script src="https://gist-it.appspot.com/https://github.com/makeabilitylab/arduino/blob/master/Basics/digitalWrite/BlinkMultipleWithExternalClass/BlinkMultipleWithExternalClass.ino?footer=minimal"></script> -->

<script src="https://emgithub.com/embed.js?target=https%3A%2F%2Fgithub.com%2Fmakeabilitylab%2Farduino%2Fblob%2Fmaster%2FBasics%2FdigitalWrite%2FBlinkMultipleWithExternalClass%2FBlinkMultipleWithExternalClass.ino&style=github&showCopy=on"></script>

Вижте [кода в нашето хранилище GitHub](https://github.com/makeabilitylab/arduino/tree/master/Basics/digitalWrite/BlinkMultipleWithExternalClass).
{: .fs-1 }

#### Видео за Workbench

<iframe width="736" height="414" src="https://www.youtube.com/embed/vb5l8Tncedo" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

## Упражнения

Искате да продължите? Ето няколко предизвикателства в областта на дизайна, които ще ви помогнат да подобрите уменията си:

- **Динамично променящи се интервали.** Какво ще стане, ако искаме да поддържаме динамично променящи се интервали на мигане, т.е. след като обектът Blinker е инстанцииран. Как бихте направили това?
- **Морзов код**. Опитайте да адаптирате класа Blinker, за да поддържа последователност от интервали на включване и изключване, като [Морзов код](https://en.wikipedia.org/wiki/Morse_code)
- **Избледняване**. А какво ще кажете за *избледняване* на светодиодите, вместо да мигат? Как бихте го направили? **Затруднени ли сте?** Ник Гамон е написал клас за това в своя [блог](https://www.gammon.com.au/blink), наречен LedFader, но не гледайте неговото решение, докато не опитате свое собствено!

## Референции

Някои допълнителни референции:

- [Мултитаскинг с Arduino: Част 1 - Мигане без забавяне](https://learn.adafruit.com/multi-tasking-the-arduino-part-1/overview), Adafruit Learn
- [Мултитаскинг с Arduino: Част 2 - Използване на прекъсвания](https://learn.adafruit.com/multi-tasking-the-arduino-part-2/overview), Adafruit Learn
- [Мултитаскинг с Arduino: Част 3](https://learn.adafruit.com/multi-tasking-the-arduino-part-3/overview), Adafruit Learn
- [Как да правите няколко неща едновременно](https://www.gammon.com.au/blink), Nick Gammon

## Следващ урок

Успяхме! С това приключва серията ни [Въведение в изхода](intro-output.md). Сега да започнем [Въведение във входа](intro-input.md), за да научим за бутони, сензори, делители на напрежение и други!

<!-- В следващия урок ще научим как да създаваме звук с пасивни пиезоелектрически зумери и [`tone()`](https://www.arduino.cc/reference/en/language/functions/advanced-io/tone/).

<span class="fs-6">
[Предишна: LED Blink 2](led-blink2.md){: .btn .btn-outline }
[Следваща: Cross-fading RGB LEDs](rgb-led-fade.md){: .btn .btn-outline }
</span> -->
