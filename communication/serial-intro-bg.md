---
lang: bg
permalink: /communication/serial-intro.html
page_id: communication-serial-intro
layout: default
title: L1&#58; Въведение в серийната комуникация
nav_order: 1
parent: Комуникация
has_toc: true # (по подразбиране)
comments: true
usemathjax: true
usetocbot: true
---
# {{ page.title }}
{: .no_toc }

## Съдържание
{: .no_toc .text-delta }

1. Съдържание
{:toc}
---

Устройствата трябва да комуникират. Сензорите с микроконтролерите. Микроконтролерите с компютрите. Компютрите с интернет. И не само! Създадени са много различни протоколи за поддържане на комуникацията между устройствата, от [Ethernet](https://en.wikipedia.org/wiki/Ethernet) и [Zigbee](https://en.wikipedia.org/wiki/ Zigbee) до WiFi и Bluetooth. В този урок ще се съсредоточим върху асинхронната серийна комуникация, по-специално TTL серийна (Transistor-Transistor Logic Serial) — траен стандарт, който преобладава от началото на персоналните компютри и се използва от [Arduino Serial library](https://www.arduino.cc/reference/en/language/functions/communication/serial/). 

За разлика от други популярни протоколи за серийна комуникация като [I<sup>2</sup>C] (https://learn.sparkfun.com/tutorials/i2c/all) и [SPI](https://learn.sparkfun.com/tutorials/serial-peripheral-interface-spi/all), TTL серийната комуникация е *асинхронна*, което означава, че не разчита на споделен часовников сигнал (точно синхронизирани импулси на напрежение) в комбинация с линиите за данни. Това има предимството на по-малко кабели, но води до малко допълнителна комуникационна натоварване за всеки предаден "пакет" или рамка данни.

В този урок ще се запознаем с асинхронната серийна комуникация и как можем да я използваме за двупосочна комуникация `Компютър ↔ Arduino`.
 

<!-- TODO:
- В бъдеще добавете паралелен срещу сериен преглед
- Добавете някои диаграми, които показват как работи сериен с напрежението на вълната
- https://www.circuitbasics.com/basics-uart-communication/
- https://en.wikipedia.org/wiki/Universal_asynchronous_receiver-transmitter
- https://www.analog.com/en/analog-dialogue/articles/uart-a-hardware-communication-protocol.html -->

## Серийна комуникация с Arduino

<!-- Arduino използва стандартен [асинхронен сериен комуникационен протокол](https://learn.sparkfun.com/tutorials/serial-communication/all) за серийна комуникация. -->

Използваме [серийната функционалност на Arduino](https://www.arduino.cc/reference/en/language/functions/communication/serial/) още от първите ни уроци (*например* [L3: Серийно отстраняване на грешки](../arduino/serial-print.md)). Въпреки това, ние сме пренебрегнали подробностите и сме използвали серийната комуникация предимно за отстраняване на грешки, а не за комуникация между `компютър ↔ Arduino`.

В Arduino инициализираме серийния порт с помощта на [`Serial.begin()`](https://www.arduino.cc/en/Serial.Begin). Функцията [`Serial.begin()`](https://github.com/arduino/ArduinoCore-avr/blob/master/cores/arduino/HardwareSerial.cpp) има две претоварени опции:

{% highlight C %}
begin(unsigned long baud)
begin(unsigned long baud, byte config)
{% endhighlight C %}

Досега в нашите уроци използвахме първата функция — `begin(unsigned long baud)` — която задава скоростта на предаване на данни в битове в секунда (baud). Но какво представлява втората функция с `byte config` и какво означава този параметър? Ще разгледаме и двете по-долу.

{: .warning }
След като се извика `Serial.begin()`, Arduino Uno и Leonardo поемат пинове 1 и 0 за серийно предаване и приемане, съответно. LED индикаторите RX и TX на платка светват в съответствие с комуникацията. Така че, след като се извика `Serial.begin()`, **не трябва да използвате пинове 1 и 0** (освен ако не ги използвате за комуникация между устройства или за свързване на вашия [логически анализатор](https://en.wikipedia.org/wiki/Logic_analyzer)!).

### Бодова скорост

Бодовата скорост определя колко бързо се изпращат данните по сериен порт, изразена в битове в секунда (bps). За комуникация с компютър, [документацията на Arduino](https://www.arduino.cc/en/Serial.Begin) препоръчва: 300 bps, 600, 1200, 2400, 4800, 9600, 14400, 19200, 28800, 38400, 57600 или 115200. И двете устройства – в този случай Arduino и компютърът – трябва да бъдат настроени на **една и съща** скорост на предаване, за да могат да комуникират.

Досега скоростта не е била проблем. Обикновено използваме 9600 bps (или 9,6 kbps) за предаване на нашата информация за отстраняване на грешки. При 9600 bps предавателят предава един нов импулс на напрежение (*например* HIGH, съответстващ на +5V, и LOW, съответстващ на 0V) на всеки 1/9600 от секундата, което се интерпретира като бит (1 или 0) от приемника. Arduino препоръчва до 115200 или 115,2 kbps, което е 12 пъти по-бързо от 9600 (но все пак бавно според днешните мрежови стандарти, разбира се).

![](assets/images/SerialMonitorShowingBaudRate.png)
{: .mx-auto .align-center }
**Фигура.** [Сериен монитор](../arduino/serial-print.md) на Arduino IDE, който има падащо меню за скоростта на предаване. Скоростта на предаване, използвана в `Serial.begin(<baud>)`, трябва да съответства на настройката в това падащо меню, в противен случай Serial Monitor няма да комуникира правилно с Arduino.
{: .fs-1 }

#### Каква е най-бързата скорост на предаване?

Това зависи от микроконтролера. Arduino Uno използва микроконтролер ATmega328P, който има максимална скорост на предаване 2 000 000 бода (2 Mbps). В [Stack Overflow](https://arduino.stackexchange.com/a/299/63793) Конър Уолф открива, че въпреки че Uno е способен да комуникира при 2 Mbps, серийната библиотека на Arduino води до ефективна скорост на комуникация от само 500 kbps.

### Асинхронната серийна комуникационна рамка

Втората функция, `begin(unsigned long baud, byte config)`, позволява опционален аргумент, който конфигурира серийния пакет или рамка за предаване. Серийната рамка за предаване се състои от три части: **данни**, **паритет** и **битове за синхронизация** (старт и стоп). 

![](assets/images/SerialFrame_FromSparkfun.png)

**Фигура.** Асинхронна серийна комуникационна рамка.
{: .fs-1 }

[битът данни](https://en.wikipedia.org/wiki/Asynchronous_serial_communication) определя дължината на частта данни от рамката на предаване (5-9), [битът четност](https://en.wikipedia.org/wiki/Parity_bit) е проста форма на код за откриване на грешки (и може да бъде включен с "1” или изключен с "0”), а битовете за синхронизация помагат за разграничаване на рамката. Винаги има *един* стартиращ бит в началото на рамката, но в края може да има един или два стоп бита (въпреки че най-често се среща един). В Arduino стандартната конфигурация на рамката за предаване е: 8 бита данни, без четност, един стоп бит – това е обичайна конфигурация.

Важно е да се отбележи, че ако настройките за скорост и конфигурация на Arduino и компютъра не съвпадат, комуникацията няма да работи. Ако нещо не работи, това е първото нещо, което трябва да проверите!

<!-- TODO: би било добре да има някои диаграми тук, показващи рамката и напреженията и т.н. Подобно на това, което има тук: https://itp.nyu.edu/physcomp/lessons/serial-communication-the-basics/ -->

### Едновременно само една компютърна програма може да отвори сериен порт

Едновременно само една компютърна програма може да отвори сериен порт. Например, ако се опитате да отворите Serial Monitor на същия COM порт, който е отворен от друга програма, ще получите следната грешка: `Грешка при отваряне на сериен порт "COM7". (Портът е зает)`.

![](assets/images/SerialMonitorErrorOpeningSerialPort.png)
**Фигура.** Демонстрация на това, което се случва, ако се опитате да отворите Serial Monitor на COM порт, който вече е отворен от друга програма. Arduino IDE показва грешка с текст "Грешка при отваряне на сериен порт "COM7". (Портът е зает)`.
{: .fs-1 }

По същия начин, ако се опитаме да получим достъп до вече отворен сериен порт с [PowerShell](https://docs.microsoft.com/en-us/powershell/scripting/overview), получаваме съобщение за грешка: `Достъпът до порт "COM7" е отказан.`

![](assets/images/PowerShellAccessToPortIsDenied.png)
**Фигура.** Едновременно само една софтуерна програма може да има достъп до сериен порт.
{: .fs-1 }

### Серийни буфери

Входящите серийни данни се съхраняват в сериен буфер, който се чете като опашка от типа "първи влязъл, първи излязъл" (FIFO). В Arduino този буфер е 64 байта (дефиниран в [USBAPI.h](https://github.com/arduino/ArduinoCore-avr/blob/master/cores/arduino/USBAPI.h)) и е реализиран като цикличен или пръстенен буфер. При 9600 бода този буфер се запълва за 53 милисекунди (9600 бода са 1200 байта/секунда или 1 байт на всеки 0,83 милисекунди).

### Сериен към USB? USB към сериен?

През 80-те и 90-те години компютрите имаха сериен порт като [RS -232 връзки](https://en.wikipedia.org/wiki/RS-232), за да поддържат асинхронна сериална комуникация. Сега използваме USB (Universal Serial Bus) – много по-усъвършенстван и ефективен стандарт за сериална комуникация, който позволява на няколко устройства да комуникират по едни и същи кабели. Въпреки това, тъй като асинхронната сериална комуникация продължава да съществува, USB драйверите и нашите операционни системи поддържат асинхронна сериална комуникация през USB. Устройствата, като Arduino, включват USB-сериен преобразувател, който се показва като сериен порт, когато ги включите (точно както ако използвате старо серийно свързване). Можете да видите устройството Arduino, например, като USBtoUART устройство (UART е Universal Asynchronous Receiver-Transmitter).

## Разработване на софтуерни приложения за серийна комуникация

Как можем да проектираме и реализираме компютърна програма за комуникация с Arduino чрез сериен порт? За да отговорим на този въпрос, нека разделим серийната комуникация на три високо ниво слоя:

- **Хардуерен слой:** Как се комуникират данните през хардуера? Колко кабела се използват? Как изглежда сигналът на напрежението? За щастие, Arduino се занимава с това вместо нас. А за серийната комуникация `Компютър ↔ Arduino`, серийните данни се предават чрез USB кабел.
- **Сериен протокол:** Какъв е форматът на пакета за серийно предаване (*например* данните и битовете за четност)? Как съставяме този пакет? Отново, не е нужно да се притесняваме за това. Arduino използва стандартния [асинхронен сериен протокол](https://learn.sparkfun.com/tutorials/serial-communication/all) и включва софтуерната библиотека [`Serial`](https://www.arduino.cc/reference/en/language/functions/communication/serial/), за да поддържа това. Трябва само да се уверим, че и двете комуникиращи устройства използват една и съща скорост на предаване и конфигурация на пакета данни.
- **Приложен слой:** Как приложенията комуникират помежду си чрез сериен порт? Аха, това е ключовият въпрос за тази подсекция!

Отговорът – за добро или за лошо – зависи изцяло от вас! Ако пишете код за серийна комуникация и за двете устройства (приложението на Arduino и приложението на вашия компютър), вие решавате как тези приложения да комуникират – вие имате пълен контрол. Има обаче някои важни съображения, включително: двоични срещу ASCII-кодирани данни, форматиране на съобщения, ръкуване и потвърждения на съобщения (повикване и отговор).

### Двоични срещу ASCII-кодирани данни

При серийната комуникация можем да предаваме/получаваме данни като поредица от битове (сурови двоични данни) или като буквено-цифрови символи (ASCII-кодирани данни).

#### Четене и записване на двоични данни

За да четете бинарни данни с Arduino, използвайте [`readBytes()`](https://www.arduino.cc/reference/en/language/functions/communication/serial/readbytes/) или [`readBytesUntil()`](https://www.arduino.cc/reference/en/language/functions/communication/serial/readbytesuntil/).

{% highlight C %}
size_t readBytes(byte *buffer, size_t length)
size_t readBytesUntil(byte terminator, byte *buffer, size_t length)
{% endhighlight C %}

[`Serial.readBytes()`](https://www.arduino.cc/ reference/en/language/functions/communication/serial/readbytes/) чете байтове от сериен порт в буфер и приключва, ако определената дължина е прочетена или изтече времето за изчакване (виж [`Serial.setTimeout()`](https://www.arduino.cc/reference/en/language/functions/communication/serial/settimeout/)). [`Serial. readBytesUntil()`](https://www.arduino.cc/reference/en/language/functions/communication/serial/readbytesuntil/) е подобна, но има и параметър за терминатор — ако се открие байт терминатор, функцията връща всички байтове до последния байт преди терминатора. И двете функции връщат броя на прочетените байтове.

За да запишем бинарни данни, можем да използваме [`Serial.write()`](https://www.arduino.cc/reference/en/language/functions/communication/serial/write/), която е претоварена функция:

{% highlight C %}
size_t write(byte val); // стойност, която да се изпрати като един байт
size_t write(String str); // низ, който да се изпрати като поредица от байтове
size_t write(byte *buffer, size_t length); // масив и брой байтове в буфера
{% endhighlight C %}

И трите [`Serial.write()`](https://www.arduino.cc/reference/en/language/functions/communication/serial/write/) функции връщат броя на записаните байтове.

#### Четене и записване на ASCII-кодирани данни

Четенето и записването на ASCII-кодирани данни би трябвало да ви е по-познато. Всъщност, за нашия случай на [серийно базиран дебъгинг](../arduino/serial-print.md), ние използваме [`Serial.print()`](https://www.arduino.cc/reference/en/language/functions/communication/serial/print/) и [`Serial.println()`](https://www.arduino.cc/reference/en/language/functions/communication/serial/println/), които предават данни като ASCII текст, четим за човека. 

За да четем ASCII данни, можем да използваме [`Serial.readString()`](https://www.arduino.cc/reference/ en/language/functions/communication/serial/readstring/) и [`Serial.readStringUntil()`](https://www.arduino.cc/reference/en/language/functions/communication/serial/readstringuntil/):

{% highlight C %}
String readString();
String readStringUntil(char terminator)
{% endhighlight C %}

И двете функции четат символи от серийния буфер и ги съхраняват в String, който се връща. [`Serial.readString()`](https://www.arduino.cc/reference/en/language/functions/communication/serial/readstring/) се прекратява, ако изтече времето (вижте [`Serial.setTimeout()`](https://www.arduino.cc/reference/en/language/functions/communication/serial/settimeout/)). [`Serial.readStringUntil()`](https://www.arduino.cc/reference/en/language/functions/communication/serial/readstringuntil/) се прекратява, ако изтече времето за изчакване или ако бъде идентифициран терминационен символ.

За да запишем ASCII данни, използваме [`Serial.print()`](https://www.arduino.cc/reference/ en/language/functions/communication/serial/print/) и [`Serial.println()`](https://www.arduino.cc/reference/en/language/functions/communication/serial/println/):

{% highlight C %}
size_t print(const __FlashStringHelper *);
size_t print(const String &);
size_t print(const char[]);
size_t print(char);
size_t print(unsigned char, int = DEC);
size_t print(int, int = DEC);
size_t print(unsigned int, int = DEC);
size_t print(long, int = DEC);
size_t print(unsigned long, int = DEC);
size_t print(double, int = 2);
size_t print(const Printable&);

size_t println(const __FlashStringHelper *);
size_t println(const String &s);
size_t println(const char[]);
size_t println(char);
size_t println(unsigned char, int = DEC);
size_t println(int, int = DEC);
size_t println(unsigned int, int = DEC);
size_t println(long, int = DEC);
size_t println(unsigned long, int = DEC);
size_t println(double, int = 2);
size_t println(const Printable&);
size_t println(void);
{% endhighlight C %}

И двете функции връщат броя на записаните байтове. За повече подробности вижте съответните им документационни страници: [`Serial.print()`](https://www.arduino.cc/reference/en/language/functions/communication/serial/print/) и [`Serial.println()`](https://www.arduino.cc/reference/en/language/functions/communication/serial/println/)

<!-- Вижте: https://github.com/arduino/ArduinoCore-avr/blob/master/cores/arduino/Stream.cpp -->

#### Защо да използваме двоичен формат вместо ASCII?

Защо бихме искали да използваме **двоичен** *вместо* **текстов** **кодиране**? Е, ако се опитваме да предадем бинарни данни – като изображение, видео или песен – тогава е за предпочитане да комуникираме чрез бинарни данни. Те са и по-ефективни от гледна точка на честотната лента (използват по-малко битове). Въпреки това, в нашите курсове обикновено предаваме/получаваме малки количества данни и за целите на отстраняването на грешки (и за по-доброто разбиране от страна на хората) е по-изгодно да използваме ASCII-кодиран формат.

#### Пример за бинарни данни срещу ASCII

Нека разгледаме един пример. Да предположим, че искаме да предадем сигнал в диапазона от 0 до 255 от Arduino към компютъра ни. Тъй като стойността варира само от 0 до 255, можем да я кодираме с 8 бита или един байт (от `0000 0000` до `1111 1111` или `0x00` и `0xFF` в шестнадесетичен формат). Изпращането чрез бинарен формат изглежда така:

{% highlight C %}
byte signalVal = getSignal ();
Serial.write(signalVal)
{% endhighlight C %}

Така например, ако `getSignal()` върне 15, ще предадем `0000 1111` (или `0x0F`). Ако `getSignal()` върне 127, ще предадем `0111 1111` (`0x7`). Ако е 255, тогава `1111 1111` (`0xFF`). И така нататък.

Въпреки това, бихме могли да предадем това и чрез ASCII-кодирани данни с [`Serial.println()`](https://www.arduino.cc/reference/en/language/functions/communication/serial/println/):

{% highlight C %}
byte signalVal = getSignal();
Serial.println(signalVal)
{% endhighlight C %}

Въпреки това, ако `getSignal()` върне 15, ще трябва да предадем **четири байта**, а не само един байт. Използвайки [таблицата за ASCII кодиране](https://www.asciichart.com/), можем да видим, че ASCII кодирането за "1” е ASCII 49 или `0011 0001` (`0x31`), а за "5” е ASCII 53 или `0011 0101` (`0x35`). След това, за разлика от [`Serial.print()`](https://www.arduino.cc/reference/en/language/functions/communication/serial/print/), [`Serial.println()`](https://www.arduino.cc/reference/en/ language/functions/communication/serial/println/) добавя символ за връщане на каретката "\r", който е ASCII 13 или `0000 1101` (`0x0D`), и след това символ за нов ред (или пренос на ред) "\n", който е ASCII 10 или `0000 1010` (`0x0A`).

По същия начин, ако искаме да предадем 127 или 255 с помощта на `Serial.println()`, ще ни трябват **пет байта**. Например, за 127 ще предадем "1" (ASCII 49 или `0011 0001`), "2" (ASCII 50 или `0011 0010`), "7" (ASCII 55 или `0011 0111`), "\r" (ASCII 13 или `0000 1101`), "\n" (ASCII 10 или `0000 1010`).

#### И двете приложения трябва да използват една и съща кодировка

Имайте предвид, че получателят трябва да знае дали данните са предадени с бинарна или ASCII кодировка. В последния случай получателят може просто да използва метод като [`Serial.readStringUntil("\n")`](https://www.arduino.cc/reference/en/language/functions/communication/serial/readstringuntil/) и данните автоматично ще бъдат преобразувани в ASCII-кодиран низ. В първия случай е необходим метод като [`Serial.readBytes() `](https://www.arduino.cc/reference/en/language/functions/communication/serial/readbytes/) и получателят трябва да знае колко байта се изпращат и как да ги декодира.

За нашите цели почти винаги използваме ASCII кодиране, защото ползата от четимостта за човека (*например* изпращане и получаване на текст) надвишава ефективността. Въпреки това, трябва да обмислите това за всеки отделен случай в зависимост от контекста на приложението, средството за комуникация (безжично *срещу* кабелно) и изискванията за захранване (*например* приложенията с ниска консумация на енергия трябва да минимизират предаването и приемането).

### Форматиране на съобщения

В горния пример просто се изпраща една стойност на предаване. За двоичен код изпращаме един байт на всеки прочетен нов сигнал; за ASCII кодиране изпращаме един ред на всеки прочетен нов сигнал. Въпреки това, вероятно ще искате да предавате и получавате *няколко* стойности. Как да го направим?

Отново, това зависи изцяло от вас! Ако използвате предаване и приемане с ASCII кодиране, можете да използвате [формат с разделители запетая (CSV)](https://en.wikipedia.org/wiki/Comma-separated_values), [JSON](https://en.wikipedia.org/wiki/JSON) или друг формат за съобщения, който сте създали сами.

Както често ще видите в нашия демонстрационен код, ние използваме прост CSV формат като този:

{% highlight C %}
int sensorVal1 = analogRead(SENSOR1_INPUT_PIN);
int sensorVal2 = analogRead (SENSOR2_INPUT_PIN);
int sensorVal3 = analogRead(SENSOR3_INPUT_PIN);
Serial.print(sensorVal1);
Serial.print(",");
Serial.print(sensorVal1);
Serial.print(",");
Serial.println(sensorVal1);
{% endhighlight C %}

Например, ако `sensorVal1` е 896, `sensorVal1` е 943, а `sensorVal3` е 349, тогава горният код ще изпрати текстов низ, който изглежда така: `896, 943, 349\r\n`.

На приемащата страна можем да използваме [regex](https://en.wikipedia.org/wiki/Regular_expression) за анализиране или да напишем наш собствен код за анализиране, като този:

{% highlight C %}

if(Serial.available() > 0){
    // Ако сме тук, тогава са получени серийни данни
    // Четете данни от серийния порт, докато стигнете до разделителя на края на реда ("\n")
    String rcvdSerialData = Serial.readStringUntil("\n");

    // Анализирайте низът, разделен със запетая
    int startIndex = 0;
    int endIndex = rcvdSerialData.indexOf(","); // Намерете първия индекс на запетая в низа
    if(endIndex != -1){

        // Анализирайте първата стойност на сензора
        String strSensorVal1 = rcvdSerialData.substring(startIndex, endIndex);
        int sensorVal1 = strSensorVal1.toInt();

        // Разделяне на втората стойност на сензора
        startIndex = endIndex + 1;
        endIndex = rcvdSerialData.indexOf(",", startIndex);
        String strSensorVal2 = rcvdSerialData.substring(startIndex, endIndex);
        int sensorVal2 = strSensorVal2.toInt();

        // Разделяне на третата стойност на сензора
        startIndex = endIndex + 1;
        endIndex = rcvdSerialData.length();
        String strSensorVal3 = rcvdSerialData.substring(startIndex, endIndex);
        int sensorVal3 = strSensorVal2.toInt();

        // Извършване на действия със стойностите на сензора
    } 
}
{% endhighlight C %}

Този пример предполага, че данните са в реда `sensorVal1, sensorVal2, sensorVal3` и че всеки получен ред е същият. За да направите тази схема на комуникация по-гъвкава, можете да предавате модифициран CSV с променливи имена (като двойки ключ, стойност) или да използвате JSON. За първото можете да предавате двойките ключ, стойност като: "`sensorVal1=896, sensorVal2=943, sensorVal3=349`". Получателят ще анализира както имената на променливите, така и техните стойности.

Във всички наши примери използваме много прост CSV формат с ASCII кодиране. Но не се колебайте да направите нещата по различен начин!

### Ръкостискане

Когато две устройства започват да комуникират – чрез сериен или друг протокол – обичайно е да се извърши [ръкостискане](https://en.wikipedia.org/wiki/Handshaking). Тоест, да се предадат и получат няколко начални съобщения, за да се установят параметрите за комуникация и да се синхронизират статусите. Например, при установяване на връзката, двете устройства могат да обменят текущия набор от съхранени стойности.

### Потвърждаване на данни

По същия начин, ако искате да се уверите, че данните са пристигнали и са били анализирани правилно. Можете да решите да предавате обратно съобщение "OK" след всеки ред от получените данни, заедно с хеш (този хеш може да бъде използван от първоначалния предавател, за да провери пристигането на данните).

## Примери за серийни програми

По-долу ще покажем няколко различни примера, използващи командния ред, Python и JavaScript. За да опростим нещата, в този урок ще се фокусираме върху **еднопосочната комуникация** от компютъра към Arduino (`Компютър → Arduino`). Тоест, компютърът ще изпраща данни, а Arduino ще ги получава. По-късно ще разгледаме `Arduino → Компютър` и двупосочната (дуплексна) комуникация `Компютър ↔ Arduino`.

Всъщност, във всички наши уроци по сериен порт, включително и в този, ще накараме Arduino да предава нещо обратно към компютъра, за да помогне с отстраняването на грешки и да се уверим, че Arduino е получил това, което очаквахме. Наричаме това ехо съобщение. Ще видите!

### Проста програма за сериен приемник на Arduino

За нашите примери по-долу ще изпълним проста програма на нашия Arduino, която чете ASCII-кодирани данни от сериен порт, анализира тези данни в цяло число и използва `analogWrite`, за да изведе това цяло число към изходен пин. В този случай сме свързали червен LED с резистор за ограничаване на тока към `OUTPUT_PIN`, който е настроен на `LED_BUILTIN` (пин 13 на Arduino Uno и Leonardo). Цялата програма изглежда така:

{% highlight C %}
const int DELAY_MS = 5;
const int OUTPUT_PIN = LED_BUILTIN;

void setup() {
    Serial.begin(9600);
    pinMode(OUTPUT_PIN, OUTPUT);
}

void loop() {
    // Проверява дали има входящи серийни данни
    if(Serial.available() > 0){
        // Ако сме тук, тогава са получени серийни данни
        // Прочетете данните от сериен порт, докато стигнете до крайния разделител ("\n")
        // Запишете всички тези данни в низ
        String rcvdSerialData = Serial.readStringUntil("\n"); 

        // Преобразувайте данните от низа в цяло число
        int ledValue = rcvdSerialData.toInt();

        // Уверете се, че стойността е между 0 и 255 (нашите максимални изходни стойности)
        ledValue = constrain(ledValue, 0, 255);
        analogWrite(OUTPUT_PIN, ledValue);

        // Само за отстраняване на грешки, отразяване на данните обратно на сериен порт
        Serial.print("Arduino received: "");
        Serial.print(rcvdSerialData);
        Serial.println(""");
    }

    delay(DELAY_MS);
}
{% endhighlight C %}

**Код.** Този код е достъпен като [SimpleSerialIn.ino](https://github.com/makeabilitylab/arduino/blob/master/Serial/SimpleSerialIn/SimpleSerialIn.ino) в GitHub. Всъщност ще използваме [SimpleSerialInOLED.ino] (https://github.com/makeabilitylab/arduino/blob/master/Serial/SimpleSerialInOLED/SimpleSerialInOLED.ino) във видеоклиповете си.
{: .fs-1}

#### Демонстрационна верига

А ето и съответната верига за горната програма, която се състои от резистор за ограничаване на тока и LED, свързан към пин 13. Разбира се, можете да изградите почти всякаква верига, която да отговаря на сериен вход. Но нека не усложняваме нещата!

![](assets/images/SimpleSerialIn_LEDCircuit.png)
**Фигура.** Съответстващата верига за [SimpleSerialIn.ino](https://github.com/makeabilitylab/arduino/blob/master/Serial/SimpleSerialIn/SimpleSerialIn.ino). Изработена в Fritzing и PowerPoint.
{: .fs-1}

### Използване на сериен монитор

Нека започнем с използването на вече познатия ни инструмент Arduino IDE [Serial Monitor](../arduino/serial-print.md). След като заредите [SimpleSerialIn.ino](https://github.com/makeabilitylab/arduino/blob/master/Serial/SimpleSerialIn/SimpleSerialIn.ino) на вашия Arduino и свържете Arduino с компютъра си, отворете сериен монитор и изпратете данни към вашия Arduino. Уверете се, че сте избрали същата скорост на предаване, използвана в `Serial.begin (<скорост на предаване>)`.

![](assets/images/ArduinoIDESerialMonitor_AnnotatedScreenShot.png)
**Фигура** Анотиран екранен снимок на инструмента [Serial Monitor](../arduino/serial-print.md) на Arduino IDE за изпращане и получаване на серийни данни. Данните, "отпратени" обратно към Arduino, се показват в текстовото поле с автоматично превъртане (където пише "Arduino received...").
{: .fs-1}

#### Видео демонстрация с използване на Serial Monitor

Ето видео демонстрация на изпращане на ASCII-кодиран текст чрез [Serial Monitor](../arduino/serial-print.md) към Arduino, работещ с [SimpleSerialInOLED.ino](https://github.com/makeabilitylab/arduino/blob/master/Serial/SimpleSerialInOLED/SimpleSerialInOLED.ino).
 

<video autoplay loop muted playsinline style="margin:0px">
<source src="assets/videos/SimpleSerialIn-NoTalking-TrimmedAndSpedUp720p.mp4" type="video/mp4" />
</video>
**Видео.** Видео, демонстриращо използването на инструмента Arduino IDE [Serial Monitor](../arduino/serial-print.md) за комуникация с Arduino, работещ с [SimpleSerialIn.ino](https://github.com/makeabilitylab/arduino/blob/master/Serial/SimpleSerialIn/SimpleSerialIn.ino). За това видео използваме леко модифицирана програма, наречена [SimpleSerialInOLED.ino](https://github.com/makeabilitylab/arduino/blob/master/Serial/SimpleSerialInOLED/SimpleSerialInOLED.ino) заедно с [OLED дисплей](../advancedio/oled.md). Това ви позволява по-лесно да видите получените стойности.
{: .fs-1 }

Забележете как можем да отпечатаме това, което Arduino получава, защото Arduino cpde отразява получените данни обратно през сериен порт, използвайки `Serial.print`. Това е опционално, но полезно!

{% highlight C %}
// Само за отстраняване на грешки, отразявате данните обратно по сериен порт
Serial.print("Arduino received: "");
Serial.print(rcvdSerialData);
Serial.println(""");
{% endhighlight C %}

### Инструменти за командния ред

Досега наблягахме на [Serial Monitor](../arduino/serial-print.md) на Arduino IDE, но този инструмент няма нищо специално или уникално. Можем да използваме всякакви приложения или езици за програмиране, които поддържат сериен порт. По-долу ще покажем как да използвате инструменти за командния ред за Windows и Mac/Linux, преди да покажем пример с Python (но C#, Objective C, Java и *други* също биха работили!).

<!-- https://itp.nyu.edu/physcomp/lab-intro-to-serial-communications/#Connecting_via_the_Command_Line
https://learn.sparkfun.com/tutorials/terminal-basics/command-line-windows-mac-linux -->

#### Windows

В Windows можем да използваме терминала [PowerShell](https://docs.microsoft.com/en-us/powershell/scripting/overview?view=powershell-7.1), който е вграден в Windows 10, за да четем и записваме данни от сериен порт. За целта ще следваме официалния [блога на PowerShell](https://devblogs.microsoft.com/powershell/writing-and-reading-info-from-serial-ports/).

Първо, за да намерим наличните серийни портове, можем да използваме `getportnames()`.

```
PS> [System.IO.Ports.SerialPort]::getportnames()
COM7
```

След това ще създадем обект `SerialPort`, който приема COM порта, скоростта на предаване, параметрите на серийната конфигурация (паритетен бит, дължина на данните и стоп бит). 

```
PS> $port= new-Object System.IO.Ports.SerialPort COM7,9600,None,8,one
```

Сега отворете този порт.

```
PS> $port.open()
```

Запишете в порта, използвайки ASCII-кодиран текст с `WriteLine(<str>)`:

```
PS> $port.WriteLine("Hello!")
```

По същия начин, за да четете от порта, използвайте `ReadLine()`:

```
PS> $port.ReadLine()
Arduino received: "Hello!"
```
Накрая, за да затворите порта, използвайте `Close()`. 

```
PS> $port.Close()
```

Така цялата програма е просто:

```
PS> $port= new-Object System.IO.Ports.SerialPort COM7,9600,None,8,one
PS> $port.open()
PS> $port.WriteLine("Hello!")
PS> $port.ReadLine()
PS> $port.Close ()
```

##### Видео демонстрация с Windows PowerShell

Ето видео демонстрация:

<video autoplay loop muted playsinline style="margin:0px">
<source src="assets/videos/SimpleSerialIn-NoTalking-WindowsPowerShell-TrimmedAndSpedUp720p.mp4" type="video/mp4" />
</video>
**Видео.** Видео, демонстриращо използването на [Windows PowerShell](https://docs.microsoft.com/en-us/powershell/scripting/overview) за комуникация с Arduino, работещ с [SimpleSerialIn.ino](https://github.com/makeabilitylab/arduino/blob/master/Serial/SimpleSerialIn/SimpleSerialIn.ino). За това видео използваме леко модифицирана програма, наречена [SimpleSerialInOLED.ino](https://github.com/makeabilitylab/arduino/blob/master/Serial/SimpleSerialInOLED/SimpleSerialInOLED.ino), заедно с [OLED дисплей](../advancedio/oled.md). Това ви позволява по-лесно да видите получените стойности.
{: .fs-1 }

#### Mac и Linux

На Mac и Linux можем да използваме командата `screen`, както е описано в този [урок на Sparkfun](https://learn.sparkfun.com/tutorials/terminal-basics/command-line-windows-mac-linux). Screen трябва да е инсталиран по подразбиране на Mac. Ако не е инсталиран на Linux, инсталирайте го с `sudo apt-get install screen`.

Първо, трябва да изброим наличните портове. Напишете:

```
> ls /dev/tty.*

/dev/tty.Bluetooth-Incoming-Port /dev/tty.SLAB_USBtoUART
/dev/tty.MALS /dev/tty.SOC
```

В този случай Arduino е изброен като `/dev/tty.SLAB_USBtoUART`. Можем да се свържем с него чрез screen, като въведем `screen <port_name> <baud_rate>`:

```
> screen /dev/tty.SLAB_USBtoUART 9600
```

Терминалът ви трябва да стане празен с мигащ курсор. Сега сте свързани с този порт. Всичко, което напишете, ще бъде незабавно изпратено до Arduino като ASCII-кодиран текст.

За да се отключите, трябва да въведете `control-a`, последвано от `control-\`. Програмата screen ще ви попита дали искате да излезете. Въведете `y`.

### Python

Накрая, нека направим проста програма в [Python](https://www.python.org/), за да пишем и четем данни от сериен порт. Това е просто за да демонстрираме общите концепции на програмирането, преди да се впуснем по-дълбоко в JavaScript решенията за другите ни уроци. Отново, можете да използвате всеки програмен език, който харесвате!

За серийна комуникация с Python ще използваме библиотеката [pySerial](https://pyserial.readthedocs.io/en/latest/). С инсталиран Python3, отворете терминала си и въведете:

```
> pip3 install pyserial
```

Това ще инсталира библиотеката [pySerial](https://pyserial.readthedocs.io/en/latest/). pySerial е доста проста и документацията ["бързо въведение" на pySerial](https://pyserial.readthedocs.io/en/latest/shortintro.html) предоставя редица примери.

Нека напишем кратка програма на Python за комуникация с [SimpleSerialIn.ino](https://github.com/makeabilitylab/arduino/blob/master/Serial/SimpleSerialIn/SimpleSerialIn.ino).

Първо, импортирайте необходимите библиотеки, след което създайте и инициализирайте обект pySerial `Serial`.

{% highlight Python %}
import serial # от https://pyserial.readthedocs.io
import time

# Създайте сериен обект на COM13 с 9600 бода и време за изчакване при четене
# от една секунда (може да бъде плаваща стойност, така че 1,5 ще бъде 1,5 секунди)
ser = serial.Serial(port="COM13", baudrate=9600, timeout=1)
{% endhighlight Python %}

Сега напишете код, който да поиска от потребителя да въведе число между 0 и 255:

{% highlight Python %}
# Помолете потребителя да въведе число между 0 и 255 и го запишете в num
num = input("Въведете число (0 - 255): ")
{% endhighlight Python %}

След това кодирайте тези данни като низ. Можете да ги превърнете в ASCII чрез `num.encode("ascii", "ignore")`

{% highlight Python %}
# Кодирайте числовата стойност като низ
strNum = str.encode(num)
{% endhighlight Python %}

Сега сме готови да изпратим данните, използвайки функцията [`write(<data>)`](https://pyserial.readthedocs.io/en/latest/pyserial_api.html#serial.Serial.write) на pySerial.

{% highlight Python %}
# Изпращане на данните с помощта на метода write на pyserial
print("Изпращане...", strNum)
ser.write(strNum)
time.sleep(0.05) # изчакване за 0.05 секунди
{% endhighlight Python %}

Накрая прочетете отговора от Arduino и го отпечатайте:

{% highlight Python %}
# Прочетете данните обратно от Arduino
echoLine = ser.readline()

print(echoLine);
print(); # празен ред
{% endhighlight Python %}

И това е всичко! Този код е достъпен като [serial_demo.py](https://github.com/makeabilitylab/arduino/blob/master/Python/Serial/serial_demo.py) в нашия GitHub. Имайте предвид, че след създаването на обекта `Serial`, ние обхващаме всичко в израза `While True:`, за да се повтаря безкрайно и да се изискват нови потребителски данни. Вижте видеото по-долу.

#### Видео демонстрация с Python

<video autoplay loop muted playsinline style="margin:0px">
<source src="assets/videos/SimpleSerialIn-Python-NoTalking2-TrimmedAndSpedUp720p.mp4" type="video/mp4" />
</video>
**Видео.** Видео, демонстриращо използването на [Python3](https://www.python.org/downloads/) с [pySerial](https://pypi.org/project/pyserial/) за комуникация с Arduino, работещ с [SimpleSerialIn.ino](https://github.com/makeabilitylab/arduino/blob/master/Serial/SimpleSerialIn/SimpleSerialIn.ino). За това видео използваме леко модифицирана програма, наречена [SimpleSerialInOLED.ino](https://github.com/makeabilitylab/arduino/blob/master/Serial/SimpleSerialInOLED/SimpleSerialInOLED.ino), заедно с [OLED дисплей](../advancedio/oled.md). Това ви позволява по-лесно да видите получените стойности.
{: .fs-1 }

#### Използване на Python за разпознаване на жестове в реално време

Разбира се, можем да направим много по-интересни неща, използвайки серийна комуникация. В клипа по-долу, например, демонстрираме Python програма, която чете в реално време данни от акселерометъра, изпратени чрез Arduino по серийния порт, и класифицира жестовете (използвайки шаблонно съпоставяне).

<iframe width="736" height="414" src="https://www.youtube.com/embed/nnTyqCwYVbA" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

**Видео.** Видео, демонстриращо разпознаване на жестове в реално време, използвайки данни от 3-осев акселерометър, изпратени чрез Arduino по сериен порт. Написахме разпознавателя на жестове на Python, но не предоставяме линк към кода, защото го използваме като задача в някои от нашите курсове. Можете да научите повече в нашата поредица от уроци [Класификация на сигнали](../signals/classification.md).
{: .fs-1 }

Тук има безкрайни възможности. И ще започнем да ги изследваме в тази серия от уроци!

## Дейност

За вашите дневници за прототипиране, стартирайте [SimpleSerialIn.ino](https://github.com/makeabilitylab/arduino/blob/master/Serial/SimpleSerialIn/SimpleSerialIn.ino) или [SimpleSerialInOLED.ino](https://github.com/makeabilitylab/arduino/blob/master/Serial/SimpleSerialInOLED/SimpleSerialInOLED.ino) с подходящата верига и изберете един от горните подходи (или разработете свой собствен!), за да комуникирате с Arduino. Заснемете видео и обмислете какво сте научили в този урок.

## Ресурси

- [Въведение в асинхронната серийна комуникация](https://itp.nyu.edu/physcomp/lab-intro-to-serial-communications/), курс по физическо програмиране на NYU ITP

- [Серийна комуникация](https://learn.sparkfun.com/tutorials/serial-communication/all), Sparkfun.com

- [Асинхронна серийна комуникация: основи](https://itp.nyu.edu/physcomp/lessons/serial-communication-the-basics/), курс по физическо компютърно инженерство на NYU ITP

### Видеоклипове

- [Сериен 1: Въведение](https://vimeo.com/380355568), видео от курса по физическо компютърно инженерство на NYU ITP

- [Сериен 2: Логически анализатор и ASCII](https://vimeo.com/380355716), видео от курса по физическо компютърно инженерство на NYU ITP 

## Следващ урок

В [следващия урок](web-serial) ще приложим новопридобитите си знания за серийната комуникация, за да комуникираме с Arduino чрез уеб браузърите си, използвайки [Web Serial API](https://web.dev/serial/).

<span class="fs-6">
[Следващ: Web Serial](web-serial.md){: .btn .btn-outline }
</span>

<!-- #### DisplayTextSerialIn

За всеки от тях ще изпълним [DisplayTextSerialIn.ino] (https://github.com/makeabilitylab/arduino/blob/master/Serial/DisplayTextSerialIn/DisplayTextSerialIn.ino) на Arduino, който чете текстови данни от сериен порт, ги показва на свързан [OLED](../advancedio/oled.md) и отразява данните обратно на сериен порт.

По същество, [DisplayTextSerialIn.ino](https://github.com/makeabilitylab/arduino/blob/master/Serial/DisplayTextSerialIn/DisplayTextSerialIn.ino) прави следното:

{% highlight C %}
// Декларация за SSD1306 дисплей, свързан към I2C (SDA, SCL пинове)
#define OLED_RESET 4 // Пин за нулиране (или -1, ако се споделя пин за нулиране на Arduino)
Adafruit_SSD1306 _display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);

void setup() {
Serial.begin(9600);

initializeOledScreen();
}

void loop(){
// Проверка за наличие на входящи серийни данни
if(Serial.available() > 0){
// Ако сме тук, значи са получени серийни данни
// Четене на данни от серийния порт, докато стигнем до разделителя на края на реда ("\n")
// Съхранение на всички тези данни в низ
String rcvdSerialData = Serial.readStringUntil("\n"); 

// Покажете получените данни на OLED
_display.clearDisplay();
_display.print(rcvdSerialData);
_display.display();

// Отправете данните обратно по сериен порт (за целите на отстраняване на грешки)
Serial.print("Arduino received: '");
Serial.print(rcvdSerialData);
Serial.println("'");
}
{% endhighlight C %} -->
