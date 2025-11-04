---
lang: bg
permalink: /arduino/inside-arduino.html
page_id: arduino-inside-arduino
layout: default
title: Как работи Arduino отвътре
parent: Въведение в Arduino
has_toc: true # включено по подразбиране
nav_exclude: false
nav_order: 4
usetocbot: true
---
# {{ page.title }}
{: .no_toc }

## Съдържание
{: .no_toc .text-delta }

1. Съдържание
{:toc}
---

Тази страница има за цел да предостави по-подробна информация за Arduino. Не се притеснявайте, не е необходимо да четете или разбирате тази страница, за да използвате Arduino! :)

## Как мога да отпечатам няколко променливи с Serial.println?

Често задаван въпрос в нашите курсове и, разбира се, онлайн, като например в [Arduino StackExchange](https://arduino.stackexchange.com/) и [Arduino форумите](https://forum.arduino.cc/), е някаква вариация на: "* Как мога да отпечатам няколко променливи в един ред код, използвайки* `Serial.println`?" 

Ето някои често срещани отговори. Забележка: Не съм ги тествал всички и съм сигурен, че много от решенията са бавни и неефективни по отношение на паметта (но ако нито едно от тези неща не ви притеснява, тогава не се колебайте да ги използвате!).

**Първо**, може би най-простият начин е да преобразувате всичко в String и да използвате конкатенация на низове:

``` C
Serial.println((String)"Var 1:" + var1 + " Var 2:" + var2 + " Var 3:" + var3);
```
[Източник](https://arduino.stackexchange.com/a/69566)
{: .fs-1 }

Забележка: трябва да правите това само за бързи прототипи, поради неефективното използване на паметта при създаването на Strings в `C`; вижте ["The Evils of Arduino Strings"](https://hackingmajenkoblog.wordpress.com/2016/02/04/the-evils-of-arduino-strings/)

**Второ**, можете да използвате външна библиотека като [PrintEx](https://github.com/Chris--A/PrintEx#printex-library-for-arduino-).

**Трето**, можете да пренасочите `printf` към сериен изход:

{% highlight C %}
// Функция, която printf и свързаните с нея ще използват за печат
int serial_putchar(char c, FILE* f) {
if (c == "\n") serial_putchar("\r", f);
    return Serial.write(c) == 1? 0 : 1;
}

FILE serial_stdout;

void setup(){
    Serial.begin(9600);

    // Настройка на stdout
    fdev_setup_stream(&serial_stdout, serial_putchar, NULL, _FDEV_SETUP_WRITE);
    stdout = &serial_stdout;

    printf("Любимото ми число е %6d!\n", 12);
}

void loop() {
    static long counter = 0;
    if (millis()%300==0){
        printf("millis(): %ld\tcounter: %ld (%02X)\n", millis(), counter, counter++);
        delay(1); 
    }
}
{% endhighlight C %}
[Източник](https://arduino.stackexchange.com/a/480) и [дискусия](https://forum.arduino.cc/index.php/topic,120440.0.html)

## Какво извиква loop() и колко бързо?

Тъй като Arduino е [отворен код](https://github.com/arduino), можем да потърсим в изходния код, за да отговорим на този въпрос.

Накратко, `loop()` се извиква в рамките на безкраен `for` (или `while` цикъл). Единствената допълнителна натоварване е проверката дали има налични данни на сериен порт и след това четенето на серийните буфери. Цялата функция `int main(void)` в [main.cpp](https://github.com/arduino/ArduinoCore-avr/blob/2f67c916f6ab6193c404eebe22efe901e0f9542d/cores/arduino/main.cpp) е:

{% highlight C %}
int main(void)
{
    init();
    initVariant();

    #if defined(USBCON)
        USBDevice.attach();
    #endif

    setup();

    for (;;) {
        loop();
        if (serialEventRun) serialEventRun();
    }
    return 0;
}
{% endhighlight C %}

Интересното е, че тази [публикация във форума на Arduino](https://forum.arduino.cc/index.php?topic=615714.0) предполага, че тъй като `serialEventRun()` е слабо дефинирана в ядрото, можете да я дефинирате локално в скицата си, за да преопределите дефиницията по подразбиране, което според OP ще "спести малко памет и ще направи loop() да работи малко по-бързо!" Можете да направите това, ако не се нуждаете от серийна комуникация.

{% highlight C %}
void serialEventRun() {}

void setup() {
}

void loop() {
}
{% endhighlight C %}

## Преобразуване на analogRead в напрежения

За да преобразуваме стойността `analogRead` в напрежение, трябва ли да я разделим на 1023 или 1024?

В [Arduino форумите](https://forum.arduino.cc/index.php?topic=303189.msg2109121) има интересна дискусия за предимствата на 1023 спрямо 1024 като делители. Максималната стойност на `analogRead` е 1023, но има 1024 "стъпки" между 0 и 5V. Официалният [урок на Arduino използва 1023](https://www.arduino.cc/en/Tutorial/ReadAnalogVoltage) – което ефективно преобразува 0 – 1023 в 0 до 5V; обаче други твърдят, че това е грешно.

Мисля, че ключът тук е да се помни, че ADC преобразуването представлява диапазон от стойности с размер на стъпката `5V/1024 = 0.0048828125V`. Така че, ако `analogRead` върне 0, това всъщност е диапазон от 0V до 0.0048828125V, а 1 е диапазон от 0.0048828125V до 0.009765625V, *и т.н.* В тази връзка бихме искали да разделим analogRead на 1024 и ако analogRead върне 1023, 1023/1024 * 5V = 4.9951171875V **до** 5V.

В [техническото описание на ATmega](https://www.sparkfun.com/datasheets/Components/SMD/ATMega328.pdf) се казва:

![](assets/images/ATMegaDatasheet_ADCConversionResult.png)

За повечето практически цели разделянето на 1023 или 1024 няма значение. :)

За повече информация по тази горещо обсъждана тема прочетете:
- [Аналогов входен шум](https://forum.arduino.cc/t/analog-input-noise/597713/6)

- [ADC преобразуване на Arduino](https://www.gammon.com.au/adc), от Ник Гамон

- [Прецизно измерване на напрежение с Arduino](http://www.skillbank.co.uk/arduino/measure.htm), от Джон Ерингтън

## Какво всъщност прави delay()?

Както може да се очаква – предвид нашите предупреждения да се избягва прекомерната употреба на [`delay(int ms)`](https://www.arduino.cc/reference/en/language/functions/time/delay/) – кодът за забавяне се състои от `while` цикъл, който просто изчаква да изтече даденото време за забавяне. В цикъла `while` има извикване на `yield()`, но по подразбиране това е празна функция – въпреки че можете да я имплементирате, за да създадете "истински кооперативен планировчик". Кодът за `yield()` е [тук](https://github.com/arduino/ArduinoCore-avr/blob/2f67c916f6ab6193c404eebe22efe901e0f9542d/cores/arduino/hooks.c).

Функцията [`delay(int ms)`](https://www.arduino.cc/reference/en/language/functions/time/delay/) се намира в [wiring.c] (https://github.com/arduino/ArduinoCore-avr/blob/2f67c916f6ab6193c404eebe22efe901e0f9542d/cores/arduino/wiring.c) и е копирана изцяло по-долу:

{% highlight C %}
void delay(unsigned long ms)
{
    uint32_t start = micros();

    while (ms > 0) {
        yield();
        while ( ms > 0 && (micros() - start) >= 1000) {
            ms--;
            start += 1000;
        }
    }
}
{% endhighlight C %}

## Как точно работи ADC на Arduino Uno?

За да преобразува аналоговите сигнали в цифрови, ATmega328 използва ADC с последователно приближение, което [Wikipedia](https://en.wikipedia.org/wiki/Successive_approximation_ADC) добре обобщава като: "*тип аналого-цифров преобразувател, който преобразува непрекъсната аналогова вълна в дискретно цифрово представяне чрез бинарно търсене през всички възможни нива на квантизация, преди да се сближи с цифров изход за всяко преобразуване*."

В "Енциклопедия на електронните компоненти, том 3" Плат твърди, че "*преобразувателят с последователно приближение използва един компаратор, който сравнява входното напрежение с изхода от DAC. Двоичното число, което се подава към DAC, се определя по един бит наведнъж, от най-значимия към най-малко значимия бит, като се използва резултатът от компаратора, за да се определи дали битът трябва да бъде 0 или 1. Тези битове се съхраняват в регистър, наречен регистър за последователно приближение (SAR). Когато процесът приключи, SAR съдържа двоично представяне на входното напрежение. Този тип ADC може да постигне висока разделителна способност (много битове) за сметка на по-ниска скорост на преобразуване.*"

## Какво е съпротивлението на аналоговия входен пин на ATmega328?

В [техническото описание на ATmega328](http://ww1.microchip.com/downloads/en/DeviceDoc/ATmega48A-PA-88A-PA-168A-PA-328-P-DS-DS40002061A.pdf) се посочва, че съпротивлението на аналоговия вход е 100 мегаома:

![Снимка на таблица 29-16 в техническата спецификация на ATmega328, описваща ADC](assets/images/ATmega328_Datasheet_Screenshot_ADCCharacteristics.png)

<!-- Допълнителна подробна тема, описваща това тук: https://www.avrfreaks.net/forum/input-impedance-digital-ios-atmega328p -->

## Референции
- https://electronics.stackexchange.com/a/67173
- http://www.gammon.com.au/adc
- http://www.skillbank.co.uk/arduino/adc.htm

## Тайните на Arduino PWM

- https://www.arduino.cc/en/Tutorial/SecretsOfArduinoPWM

<!-- Друга интересна статия е "Защита на входовете в цифровата електроника": https://www.digikey.com/en/articles/protecting-inputs-in-digital-electronics -->
