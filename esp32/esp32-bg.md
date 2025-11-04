---
lang: bg
permalink: /esp32/esp32.html
page_id: esp32-esp32
layout: default
title: L1&#58; Въведение в ESP32
parent: ESP32
has_toc: true # (по подразбиране)
usemathjax: true
comments: true
usetocbot: true
nav_order: 1
---
# {{ page.title | replace_first:"L",'Lesson '}}
{: .no_toc }

## Съдържание
{: .no_toc .text-delta }

1. Съдържание
{:toc}
---

<!-- Задачи за съдържанието:
1. Направете пример за мигане
2. Направете пример за избледняване. Покажете PWM
3. Аналогов вход
4. Направете пример за сензор за допир?
5. Покажете WiFi? И/или Bluetooth?
6. -->

<!-- Вижте също https://randomnerdtutorials.com/esp32-adc-analog-read-arduino-ide/ - ->

![Изображение на различни ESP32 платки](assets/images/ESP32Boards_MakerAdvisor.png)
Изображение от [makeradvisor.com](https://makeradvisor.com/esp32-development-boards-review-comparison/). Има буквално десетки ESP32 платки. Потърсете онлайн сравнения (*например* [линк](https://makeradvisor.com/esp32-development-boards-review-comparison/)).
{: .fs-1 }
 

[ESP32](https://en.wikipedia.org/wiki/ESP32) е евтина платка "система на чип" с вграден WiFi, Bluetooth, ултра ниска консумация на енергия и бърз микропроцесор, създадена от [Espressif](https://www.espressif.com/en/products/socs/esp32). ESP32 е наследник на изключително успешния [ESP8266](https://en.wikipedia.org/wiki/ESP8266) на Espressif, но е много по-мощен и с по-богати функции.

Оригиналният ESP32 беше пуснат на пазара през 2016 г., но оттогава Espressif създаде десетки варианти и актуализации. Най-новата платка е ESP32-S3, пусната на пазара през 2020 г., която разполага с двуядрен Xtensa® 32-bit LX7 с честота до 240 MHz, вграден WiFi и Bluetooth, до 8 MB флаш памет и поддръжка на много периферни устройства. Освен това, сега има и микроварианти като [серията ESP32-C] (https://www.espressif.com/en/products/devkits/esp32-devkitc), които заемат по-малко място. Вижте [инструмента за сравнение на продуктите на Espressif](https://products.espressif.com/#/product-comparison).

<!-- ESP32 е много по-мощен от ESP8266, както и от 16-битовите микроконтролери в Arduino Uno или Leonardo, които използвахме в нашите [въвеждащи уроци](../arduino/). -->

<!-- На пазара има буквално десетки ESP32 платки, включително [серията ESP32 на Adafruit](https://www.adafruit.com/product/3405) и [серията ESP32 на Sparkfun](https://www.sparkfun.com/products/13907). Потърсете онлайн сравнения (*например* [линк](https://makeradvisor.com/esp32-development-boards-review-comparison/)). -->

### Програмна среда

Можете да програмирате ESP32 на различни езици и в различни програмни среди, включително C/C++, [Micropython](https://github.com/pvanallen/esp32-getstarted), [Lua](https://nodemcu.readthedocs.io/en/dev-esp32/) и др. ESP32 е напълно **независим** от екосистемата на Arduino. Точно както не е необходимо да използвате Arduino, за да програмирате ATmega328P (използван в Arduino Uno) или ATmega32U4 (намерен в Arduino Leonardo), не е необходимо да използвате Arduino, за да програмирате ESP32.

За нашата серия от уроци обаче *ще* използваме Arduino за програмиране на ESP32 – и така по-голямата част от нашите [предишни знания](../arduino/) ще бъдат директно прехвърлени (ура! 🎉 ). Можем да използваме Arduino за програмиране на ESP32, защото Espressif е създал [отворен код Arduino core](https://github.com/espressif/arduino-esp32) за серията ESP32. Вижте [официалното ръководство "Първи стъпки" на Espressif](https://docs.espressif.com/projects/arduino-esp32/en/latest/getting_started.html). Забележка: не всички функции на ESP32 са достъпни чрез тази библиотека, можете да видите [ограниченията тук](https://docs.espressif.com/projects/arduino-esp32/en/latest/libraries.html).

Ако искате да опитате да програмирате ESP32 *без* Arduino, следвайте [Ръководството за програмиране на Espressif ESP-IDF](https://docs.espressif.com/projects/esp-idf/en/stable/esp32/get-started/index.html). Ние никога не сме правили това, така че този подход е извън обхвата на нашата серия за обучение.

<!-- За опции, които не са Arduino, можете да използвате IoT Development Framework ([IDF](https://docs.espressif.com/projects/esp-idf/en/latest/esp32/)) на Espressif или [VSCode с PlatformIO](https://docs.platformio.org/en/latest/ tutorials/espressif32/arduino_debugging_unit_testing.html). Много от платките ESP32 имат библиотеки Arduino, така че можете да използвате и [Arduino IDE](https://www.arduino.cc/en/main/software), което и ние ще направим. Това значително опростява програмирането на ESP32 (но за сметка на гъвкавостта и ефективността). -->

## Сравнителна таблица

Ето сравнителна таблица на Arduino Uno Rev3 и ESP32, извлечена от [официалната документация на Espressif](https://docs.espressif.com/projects/esp-idf/en/v5.0/esp32s3/hw-reference/chip-series-comparison.html) и тази [сравнителна таблица в GitHub Gist] (https://gist.github.com/sekcompsci/2bf39e715d5fe47579fa184fa819f421).

{: .note }
Въпреки че има много разлики между Arduino Uno/Leonardo и ESP32, една от основните е, че ESP32 работи с 3,3 V, а не с 5 V. Това има значение за начина, по който се свързвате с електронни компоненти чрез GPIO пинове.

|Характеристика|Arduino Uno|ESP32|ESP32-S2|ESP32-S3|
|--- |--- |--- |--- |--- |
|Година на пускане на пазара|2010|2016|2020|2020|
|Технически данни| [Технически данни за Uno (PDF)](https://www.arduino.cc/en/uploads/Main/Arduino_Uno_Rev3.pdf) | [Технически данни за ESP (PDF)](https://espressif.com/sites/default/files/documentation/esp32_datasheet_en.pdf) | [ESP-S2 технически спецификации (PDF)](https://www.espressif.com/sites/default/files/documentation/esp32-s2_datasheet_en.pdf) | [ESP-S3 технически спецификации (PDF)](https://www.espressif.com/sites/default/files/documentation/esp32-s3_datasheet_en.pdf) |
|Ядро|ATmega328P|Xtensa® двуядрен/едноядрен 32-битов LX6|Xtensa® едноядрен 32-битов LX7|Xtensa® двуядрен 32-битов LX7|
|Wi-Fi протоколи|✖️|802.11 b/g/n, 2,4 GHz|802.11 b/g/n, 2,4 GHz|802.11 b/g/n, 2,4 GHz|
|Bluetooth®|✖️|Bluetooth v4.2 & BLE |✖️|Bluetooth 5.0|
|Типична честота|16 MHz|240 MHz|240 MHz|240 MHz|
|SRAM|2 KB|520 KB|320 KB|512 KB|
|ROM|32 KB|448 KB |128 KB |384 KB |
|Вградена флаш памет|32 KB|2 MB, 4 MB или няма|2 MB, 4 MB или няма|8 MB или няма|
|Външна флаш памет|✖️|До 16 MB устройство|До 1 GB устройство|До 1 GB устройство|
|Външна RAM памет|✖️|До 8 MB устройство|До 1 GB устройство|До 1 GB устройство|

И периферна поддръжка. Имайте предвид, че АЦП на ESP32 са 12-битови, а не 10-битови, така че очевидно осигуряват много по-голяма точност при преобразуването от аналогово в цифрово: 3,3 V се разделя линейно между 0-4095 (10 бита).

|Периферия|Arduino Uno|ESP32|ESP32-S2|ESP32-S3|
|--- |--- |--- |--- |--- |
|ADC|Един 10-битов, 6 канала|Два 12-битови, 18 канала|Два 12-битови, 20 канала|Два 12-битови SAR ADC, 20 канала|
|DAC|✖️|Два 8-битови канала|Два 8-битови канала|✖️|
|Таймери|Три 16-битови|Четири 64-битови|Четири 64-битови|Четири 54-битови|
|Watchdog таймери|1|Три|Три|Три|
|Температурен сензор|✖️|✖️|1|1|
|Сензор за допир|✖️|10|14|14|
|Сензор на Хол|✖️|1|✖️|✖️|
|GPIO|14|34|43|45|
|SPI|1|4|4|4|
|LCD интерфейс|✖️|1|1|1|
|UART|1|3|2|3|
|I2C|1|2|2|2|
|I2S|✖️|2, може да бъде конфигуриран да работи с 8/16/32/ 40/48-битова резолюция като входен или изходен канал.|1, може да бъде конфигуриран да работи с 8/16/24/32/48/64-битова резолюция като входен или изходен канал.|2, може да бъде конфигуриран да работи с 8/16/24/32-битова резолюция като входен или изходен канал.|
|Камерен интерфейс|✖️|1|1|1|
|Импулсен брояч|✖️|8 канала|4 канала|4 канала|
|LED PWM|✖️|16 канала|8 канала|8 канала|
|PWM за управление на мотор|✖️|2, шест PWM изхода|✖️|2, шест PWM изхода|

<!-- |Характеристика|Серия ESP32|Серия ESP32-S2|Серия ESP32-S3|
|--- |--- |--- |--- |
|Година на пускане на пазара|2016|2020|2020|
|Технически данни| [Технически данни за ESP (PDF)](https://espressif.com/sites/default/files/documentation/esp32_datasheet_en.pdf) | [Технически данни за ESP-S2 (PDF)](https://www.espressif.com/sites/default/files/documentation/esp32-s2_datasheet_en.pdf) | [ESP-S3 технически данни (PDF)](https://www.espressif.com/sites/default/files/documentation/esp32-s3_datasheet_en.pdf) |
|Ядро|Xtensa двуядрен/едноядрен 32-битов LX6|Xtensa едноядрен 32-битов LX7|Xtensa двуядрен 32-битов LX7|
|Wi-Fi протоколи|802.11 b/g/n, 2,4 GHz|802.11 b/g/n, 2,4 GHz|802.11 b/g/n, 2,4 GHz|
|Bluetooth®|Bluetooth v4.2 & Bluetooth LE |✖️|Bluetooth 5.0|
|Типична честота|240 MHz|240 MHz|240 MHz|
|SRAM|520 KB|320 KB|512 KB|
|ROM|448 KB |128 KB |384 KB |
|Вградена флаш памет|2 MB, 4 MB или няма|2 MB, 4 MB или няма|8 MB или няма|
|Външна флаш памет|До 16 MB устройство|До 1 GB устройство|До 1 GB устройство|
|Външна RAM памет|До 8 MB устройство|До 1 GB устройство|До 1 GB устройство|
|**Периферия**||||
|ADC|Два 12-битови, 18 канала|Два 12-битови, 20 канала|Два 12-битови SAR ADC, 20 канала|
|DAC|Два 8-битови канала|Два 8-битови канала|✖️|
|Таймери|Четири 64-битови таймери за общо предназначение|Четири 64-битови таймери за общо предназначение|Четири 54-битови таймери за общо предназначение|
|Таймери за наблюдение|Три|Три|Три|
|Температурен сензор|✖️|1|1|
|Сензор за допир|10|14|14|
|Сензор на Хол|1|✖️|✖️|
|GPIO|34|43|45|
|SPI|4|4|4|
|LCD интерфейс|1|1|1|
|UART|3|2|3|
|I2C|2|2|2|
|I2S|2, може да бъде конфигуриран да работи с 8/16/32/40/48-битова резолюция като входен или изходен канал.|1, може да бъде конфигуриран да работи с 8/16/24/32/48/64-битова резолюция като входен или изходен канал. |2, може да бъде конфигуриран да работи с 8/16/24/32-битова разделителна способност като входен или изходен канал.|
|Камерен интерфейс|1|1|1|
|Импулсен брояч|8 канала|4 канала|4 канала|
|LED PWM|16 канала|8 канала 1|8 канала|
|PWM за управление на мотор|2, шест PWM изхода|✖️|2, шест PWM изхода| -->

## Серията Adafruit ESP32

За нашата поредица от уроци ще използваме **платките ESP32 на Adafruit**. По-конкретно, оригиналната платка ESP32 на Adafruit, наречена [Huzzah32 ESP32 Feather](https://www.adafruit.com/product/3405), която излезе на пазара през май 2017 г., както и платка [ESP32-S3 на Adafruit](https://www.adafruit.com/product/5477), пусната на пазара през ноември 2021 г.

<!-- Тази платка е изградена на базата на модула [ESP32 WROOM](https://www.espressif.com/en/products/modules/esp-wroom-32/overview) на Espressif. -->

Макар че можете да намерите (много) по-евтини алтернативи на ESP32 в [AliExpress](https://www.aliexpress.com/w/wholesale-esp32.html) или [Amazon] (https://www.amazon.com/s?k=esp+32+board) – на цена от само няколко долара – Adafruit произвежда надеждни продукти с високо качество и предлага добра поддръжка на клиентите (вижте [форумите на Adafruit](https://forums.adafruit.com/)). Освен това, точно както стандартизираният форм-фактор на Arduino Uno създаде екосистема от [стекируеми разширителни платки](https://learn.sparkfun.com/tutorials/arduino-shields-v2), така и **Adafruit създаде стекируеми щитове** за платки, съвместими с "Feather", като ESP32. Adafruit нарича тези разширителни платки Wings – вижте [списъка тук](https://www.adafruit.com/category/814) и обзор на [FeatherWings тук](https://learn.adafruit.com/adafruit-feather/featherwings)). Например, можете да добавите [MP3 Player FeatherWing](https://www.adafruit.com/product/3357), [GPS FeatherWing](https://www.adafruit.com/product/3133) или [DC Motor FeatherWing](https://www.adafruit.com/product/2927), за да споменем само няколко.

Независимо от това коя ESP32 платка използвате, нашата серия от уроци би трябвало да ви помогне. Имайте предвид обаче, че местоположението на пиновете може да е различно.

### Спецификации на Adafruit ESP32

| Име | Arduino Uno | Adafruit ESP32 | Adafruit ESP32-S3 |
| ---- | ----------- | -------- | --------- -------- |
| Изображение | ![Arduino Uno]({{ site.baseurl }}/assets/images/ArduinoUno_ArduinoCC_w200.png) | ![ESP32 Huzzah32]({{ site.baseurl }}/assets/images/ESP32Huzzah32_Adafruit_w200.png) | ! [ESP32-S3](assets/images/AdafruitESP32-S3_w200.png) |
| Магазин | [Arduino](https://store.arduino.cc/arduino-uno-rev3) | [Adafruit](https://www.adafruit.com/product/3405) | [Adafruit](https://www.adafruit.com/product/5477) |
| Микроконтролер | 8-битов, 16 MHz [ATmega328P](https://www.microchip.com/wwwproducts/en/ATmega328) | 32-битов, 240 MHz двуядрен Tensilica LX6 | 32-битов, 240 MHz двуядрен Tensilica LX7 |
| Входно напрежение (гранично) | 6-20V | Използвайте USB (5V) или 3.7V LiPoly | 5V (чрез USB) или 3.7V (LiPoly) |
| Работно напрежение | 5V | 3,3V | 3,3V |
| Флаш памет | 32KB | 4MB | До 8MB |
| SRAM | 2KB | 520KB | До 2MB |
| GPIO пинове | 14 | 21 | 25 |
| PWM пинове | 6 | Всички | Всички |
| Аналогови входове | 6 | 14 | 20 |
| Wi-Fi | Н/Д | 802.11b/g/n HT40 Wi-Fi трансивър | 802.11b/g/n HT40 Wi-Fi трансивър |
| Bluetooth | Н/Д | Двоен режим (класически и BLE) | Bluetooth 5.0 (LE) |
| USB връзка | Тип B (правоъгълна връзка, използвана при принтери) | MicroUSB | USB-C |


<!-- | Име | Arduino Uno | Huzzah32 |
| ---- | ----------- | -------- |
| Изображение | ![Arduino Uno]({{ site.baseurl }}/assets/images/ArduinoUno_ArduinoCC_w200.png) | ![ESP32 Huzzah32]({{ site.baseurl }}/assets/images/ESP32Huzzah32_Adafruit_w200.png) |
| Микроконтролер | 8-битов, 16 MHz [ATmega328P](https://www.microchip.com/wwwproducts/en/ATmega328) | 32-битов, 240 MHz двуядрен Tensilica LX6 |
| Производител на микроконтролер | Microchip (Atmel) | Espressif |
| Система на чип | Н/Д | [ESP32](https://www.espressif.com/sites/default/files/documentation/esp32_datasheet_en.pdf) |
| Входно напрежение (гранично) | 6-20V | Използвайте USB (5V) или LiPoly (3.7/4.2V) |
| Работно напрежение | 5V | 3.3V |
| Флаш памет | 32KB (0.5KB използвани от bootloader) | 4MB |
| SRAM | 2KB | 520KB |
| GPIO пинове | 14 | 21 |
| PWM пинове | 6 | Всички |
| Аналогови входове | 6 | 14 |
| Wi-Fi | Н/Д | 802.11b/g/n HT40 Wi-Fi трансивър |
| Bluetooth | Н/Д | Двоен режим (класически и BLE) | -->

<!-- Не забравяйте, че флаш паметта е мястото, където се съхранява компилираната ви програма, а SRAM е мястото, където микроконтролерът ви създава и манипулира променливи, когато работи. -->

<!-- ESP32 също има 2xI2S Audio, 2xDAC, 2xI2C (само един конфигуриран по подразбиране в поддръжката на Feather Arduino IDE), 3xSPI (само един конфигуриран по подразбиране в поддръжката на Feather IDE) . Вижте [преглед на Adafruit](https://learn.adafruit.com/adafruit-huzzah32-esp32-feather/overview). -->

За разлика от чиповете ATmega, използвани в Uno и Leonardo, ESP32 разполага с хардуерна плаваща точка (FPU); въпреки това, има някои критики относно нейната производителност ([link1](https://blog.classycode.com/esp32-floating-point-performance-6e9f6f567a69), [link2](https://www.esp32.com/viewtopic.php?f=14&t=800)). Според нашата информация, производителността на FPU е подобрена в ESP32-S3s (и поддържа както единична, така и двойна точност).

Huzzah32 **не** е проектиран за външни захранвания, така че използвайте USB порта с [5V 1A USB стенен адаптер](https://www.adafruit.com/product/501) или го включете към компютъра си или LiPoly батерия (3.7/4.2V) . За разлика от Arduino Uno и Leonardo, не използвайте 9V батерия, защото може да повредите платка!

### Списък с пинове на ESP32

Официалният списък с пинове на ESP32 е [тук](https://www.espressif.com/sites/default/files/1a-esp32_pin_list_en-v0.1.pdf):

![Официален списък с пинове на ESP32](assets/images/ESP32PinList_Espressif.png)
Снимка на екрана със списъка с пинове на ESP32 [PDF](https://www.espressif.com/sites/default/files/1a-esp32_pin_list_en-v0.1.pdf) .
{: .fs-1 }

В нашия код ще се позоваваме на пиновете въз основа на техния GPIO номер, техния аналогов входен номер (с префикс "A") за аналогов вход или техния сензорен номер (с префикс "T") за използване на капацитивно сензорно засичане. Винаги можем да използваме GPIO номера (който е просто цяло число). ESP32 [datasheet](https://www.espressif.com/sites/default/files/documentation/esp32_datasheet_en.pdf) често използва името на пина (крайната лява колона от горния списък с пинове), за да се позовава на пиновете.

### Диаграма на пиновете на Huzzah32

И така, какво правят всички тези пинове? О, толкова много неща!

Диаграмата на пиновете за Huzzah32 в официалните [документи](https://learn.adafruit.com/adafruit-huzzah32-esp32-feather/pinouts) на Adafruit е доста объркваща. Затова създадохме наша собствена:

![Диаграма на пиновете на Huzzah32](assets/images/AdafruitHuzzah32PinDiagram.png)
За подробности вижте Adafruit Huzzah32 [docs](https://learn.adafruit.com/adafruit-huzzah32-esp32-feather/pinouts). Кликнете с десния бутон и отворете изображението в нов раздел, за да го увеличите.
{: .fs-1 }
 

### Важни бележки

- ESP32 работи с **3,3 V захранване и логика** и, освен ако не е посочено друго, GPIO пиновете не са безопасни за 5 V! **BAT** пинът по принцип не трябва да се използва директно, тъй като Huzzah32 има JST връзка за LiPoly батерията. Абсолютно не трябва да свързвате 9 V връзка тук.
- Има **21 GPIO пина**; обаче на Huzzah32 пиновете 34 (A2), 39 (A3), 36 (A4) не са с изходна способност и затова трябва да се използват само за вход. Така че общо има **18 GPIO пина**. Имайте предвид: пиновете са в странен ред, затова прочетете внимателно диаграмата.
- **PWM** е възможно на всички 18 GPIO пина
- **14 от 21 GPIO пина** могат да се използват като **аналогови входни пинове**; обаче, A13 не е изложен. Той се използва за измерване на напрежението на LiPoly батерията чрез делител на напрежение. Когато четете нивото на батерията с `analogRead(A13)`, не забравяйте да умножите по 2, за да получите правилно четене. Ето една начална програма за четене и отпечатване на нивото на батерията в Serial ([link](https://github.com/makeabilitylab/arduino/blob/master/ESP32/BatteryLevel/BatteryLevel.ino))
- **Разделителната способност на ADC е 12 бита** (0-4095). Това е в контраст с Arduino Uno и Leonardo, които използват ATmega чипове с 10-битови ADC (т.е. 0-1023). Уверете се, че използвате правилната максимална стойност в преобразуванията си (*например* използвайки [`map()`](https://www.arduino.cc/reference/en/language/functions/math/map/))
- **GPIO 13** е `LED_BUILTIN` (червеният LED до микро USB)
- Светлината на веригата за зареждане ще мига бързо, когато няма включена LiPoly батерия. Това е безвредно и не означава нищо. Този LED също ще мига (по-бавно), когато батерията е включена и се зарежда. Батерията се зарежда автоматично, когато е включена и Huzzah32 се захранва от външен източник.
- Захранвайте Huzzah32 само чрез USB щепсел (макс. 5V, 1A) или LiPoly батерия (3,7/4,2V)

![Анимация на всички 18 GPIO изходни пина, които се появяват и изчезват](assets/movies/Huzzah32_GPIOFadeTestAllPinsSimultaneously-Optimized3.gif)

Huzzah32 има 21 GPIO пина; обаче пиновете 34 (A2), 39 (A3) и 36 (A4) не са с изходна способност. В тази анимация се опитваме да избледняваме/появяваме всички 21 GPIO пина и да демонстрираме, че само 18 от тях работят за изход.
{: .fs-1 }
 

### ADC2 може да се използва само когато WiFi не е активиран

Adafruit [docs](https://learn.adafruit.com/adafruit-huzzah32-esp32-feather/pinouts) посочва (малко объркващо), че ADC#1 работи само когато WiFi е стартиран. Ние тествахме това емпирично (вижте видеото по-долу) и установихме, че това **не** е вярно. От друга страна, Espressif [docs](https://docs.espressif.com/projects/esp-idf/en/latest/esp32/api-reference/peripherals/adc.html) посочва, че ADC#2 работи само когато WiFi **не** е стартиран. Ние **установихме**, че това е вярно. Следователно считаме, че Espressif docs е прав, а Adafruit docs е грешен. **Актуализация:** оказва се, че документите на Adafruit _са_ точни, но просто са формулирани погрешно. Всъщност ADC#1 е единственият ADC, който работи при използване на WiFi (вижте [публикацията в Reddit](https://www.reddit.com/r/esp32/comments/gav6mw/huzzah32_pin_diagram_draft/)).

Всъщност, ние проверихме това емпирично. Разгледайте нашите две програми:
- [AnalogInputTest.ino](https://github.com/makeabilitylab/arduino/blob/master/ESP32/Basics/AnalogInputTest/AnalogInputTest.ino) чете от всички аналогови входни пинове и отпечатва стойностите в Serial (така че можете да ги видите в Serial Console или Serial Plotter)
- [WiFiAnalogInputTest.ino](https://github.com/makeabilitylab/arduino/blob/master/ESP32/WiFi/WiFiAnalogInputTest/WiFiAnalogInputTest.ino) разширява AnalogInputTest, но включва WiFi.

В следващото видео използвам [AnalogInputTest.ino](https://github.com/makeabilitylab/arduino/blob/master/ESP32/Basics/AnalogInputTest/AnalogInputTest.ino), за да тествам всички 13 аналогови входни пина (`A0` - `A12`) с помощта на трим потенциометър за вход и Serial Plotter за изход.

<iframe width="736" height="414" src="https://www.youtube.com/embed/8BBY-5n4e5A" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>


<!-- ![ESP32 Huzzah32 pin diagram from Zerynth]({{ site.baseurl }}/assets/images/adafruithuzzah32pin_zerynth.jpg)
Pin diagram from [Zerynth](https://docs.zerynth.com/latest/official/board.zerynth.adafruit_huzzah32/docs/index.html). ICU означава [Input Capture Unit](https://docs.zerynth.com/official/core.zerynth.stdlib/r2.0.9/icu.html).
{: .fs-1 } -->

<!-- Друга полезна диаграма на пиновете: https://people.eecs.berkeley.edu/~boser/courses/49_sp_2019/N_gpio.html#_pin_diagram -->


### Инструкции за инсталиране на Huzzah32 за Arduino IDE

Можете да следвате [официалните инструкции за инсталиране на Adafruit Huzzah32 Arduino IDE](https://learn.adafruit.com/adafruit-huzzah32-esp32-feather/using-with-arduino-ide), които сме разширили малко по-долу.

#### Стъпка 1: Добавете ESP32 към Arduino Board Manager

1. Отворете Arduino IDE

2. Отидете в Preferences
![Снимка на отворените настройки](assets/images/ArduinoIDE_OpenPreferences.png)

3. В настройките намерете полето `Additional Board Manager URLs:`
![Снимка на допълнителния URL адрес на Board Manager в настройките](assets/images/ArduinoIDE_EnterAdditionalBoardManagerJSON.png)

4. Добавете URL адреса на ESP32 JSON `https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json`
![Снимка на въвеждането на ESP32 JSON string](assets/images/ArduinoIDE_EnteringESP32JsonString.png)

5. Отворете Arduino IDE Board Manager
![Снимка на Arduino IDE при отваряне на board manager](assets/images/ArduinoIDE_OpenBoardManager.png)

6. Потърсете `ESP32` и кликнете `Install`
![Снимка, показваща ESP32, добавен към board manager](assets/images/ArduinoIDE_ESP32AddedInBoardManager.png)

#### Стъпка 2: Инсталиране на драйвер за виртуален COM порт USB към UART Bridge

Както е отбелязано в [официалните инструкции за инсталиране на Adafruit Huzzah32 Arduino IDE](https://learn.adafruit.com/adafruit-huzzah32-esp32 -feather/using-with-arduino-ide), втората стъпка е да инсталирате драйвера USB to UART Bridge Virtual COM Port (VCP), за да се свържете с платка ESP32. Можете да изтеглите драйвера за Windows, Mac и Linux [оттук](https://www.silabs.com/products/development-tools/software/usb-to-uart-bridge-vcp-drivers).

#### Стъпка 3: Изберете "Adafruit ESP32 Feather” в менюто на платките

След като го инсталирате, изберете "Adafruit ESP32 Feather” в менюто "Board” (Платки).

![Снимка на екрана, показваща как да изберете Adafruit ESP32 в менюто "Board Manager” (Мениджър на платките)](assets/images/ArduinoIDE_SelectAdafruitESP32Board.png)

#### Стъпка 4: Изберете подходящия порт

Накрая изберете подходящия порт

![Снимка на екрана, показваща как да изберете правилния ESP32 порт](assets/images/ArduinoIDE_SelectESP32Port.png)

## Ресурси

### Официална документация за ESP32

- [API Reference](https://docs.espressif.com/projects/esp-idf/en/latest/esp32/api-reference/index.html)
- [Ръководства за API](https://docs.espressif.com/projects/esp-idf/en/latest/esp32/api-guides/index.html)
- [Arduino core за ESP32](https://github.com/espressif/arduino-esp32)

### Други

- [Ръководство за свързване на Sparkfun ESP32 Thing](https://learn.sparkfun.com/tutorials/esp32-thing-hookup-guide/all). Написано за Sparkfun ESP32 Thing, но съдържа подходящи примери за WiFi и BLE.

<!-- ## Идеи за приложения
- Свържете се с WiFi, вземете времето, отпечатайте го на OLED. Да създадете часовник?
- Свържете се с WiFi, изтеглете статистиките за Covid-19, отпечатайте ги на дисплея
- Очевидно ESP32 може да поддържа Serial.printf? [Вижте линка](https://arduino.stackexchange.com/ a/53751).

### Звук / VUMeters

- [Използване на вградения DAC на ESP32](https://www.reddit.com/r/esp32/comments/bid08m/finally_got_audio_sampling_via_dma_with_no_cpu/) ?
- [Стрийминг на музика с I2S](https://www.reddit.com/r/esp32/comments/dluvgl/streaming_web_radio_to_esp32_playing_it_using_the/)

### Platform IO за VSCode

- https://docs.platformio.org/en/latest/integration/ide/visualstudio.html
- https://maker.pro/arduino/tutorial/how-to-use-platformio-in-visual-studio-code-to-program-arduino -->

## Следващ урок

В [следващия урок](led-blink.md) ще напишете първата си програма за ESP32, използвайки библиотеката ESP32 Arduino.

<span class="fs-6">
[Следващ: Мигане на LED с ESP32](led-blink.md){: .btn .btn-outline }
</span>
