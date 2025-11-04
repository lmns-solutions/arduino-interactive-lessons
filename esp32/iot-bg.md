---
lang: bg
permalink: /esp32/iot.html
page_id: esp32-iot
layout: default
title: L7&#58; Интернет на нещата
parent: ESP32
has_toc: false # (по подразбиране)
usemathjax: true
comments: true
usetocbot: true
nav_order: 7
---
# {{ page.title | replace_first:"L",'Lesson '}}
{: .no_toc }

## Съдържание
{: .no_toc .text-delta }

1. Съдържание
{:toc}
---

ESP32 е вълнуващ не само заради скоростта, паметта и GPIO възможностите си, но и защото е истинска модерна платка за интернет на нещата (IoT) с Wi-Fi и Bluetooth поддръжка. И никога не е било по-лесно да се извличат данни от тези свързани с интернет устройства и да се прехвърлят в "облака" (за добро или за лошо). :)

## IoT платформи

Има **огромно** количество IoT платформи – значително повече, отколкото дори преди няколко години – включително [Adafruit IO](https://learn.adafruit.com/welcome-to-adafruit-io), [Blynk](https://blynk.io/), [ThingsSpeak](https://thingspeak.com/) и [Losant](https://www.losant.com/). Вижте [Hackaday](https://hackaday.com/ 2017/10/31/review-iot-data-logging-services-with-mqtt/) и [bigmessowires](https://www.bigmessowires.com/2017/06/29/esp8266-freeboard-io-blynk-and-iot/) за рецензии.

Ако не искате да разработвате свой собствен бекенд или просто искате платформа, на която бързо да създадете прототип на идеята си, тогава тези IoT сайтове са удобни, лесни за използване, гъвкави и с доста богати функции. Можете да получавате данни в реално време, да контролирате и да взаимодействате с тези данни и устройства, свързани с интернет, да свързвате проектите си с уеб услуги като Twitter и др. Много от IoT платформите също се свързват с услуги като IFTTT и/или предлагат свои собствени събития, които да ви уведомяват, например чрез имейл, когато бъде открита аномалия.

Много от тези платформи поддържат както REST API – с които вероятно сте запознати, ако сте се занимавали с уеб разработка – така и протокола Message Queuing Telemetry Transport ([MQTT](https://en.wikipedia.org/wiki/MQTT)), който е отворен стандарт за леки мрежи от типа "публикувай-абонирай се". Вижте [MQTT](http://mqtt.org/).

## Adafruit IO

За нашия урок ще използваме [Adafruit.io](https://learn.adafruit.com/welcome-to-adafruit-io), което значително опростява взаимодействието с облачен бекенд от ESP32 и предоставя богат набор от функции. Безплатният пакет предлага 10 емисии, 5 табла, ограничение на скоростта на качване от 30 точки данни/минута, 30 дни съхранение и контрол на поверителността. Платеният пакет, наречен [Adafruit IO Plus,](https://io.adafruit.com/plus) струва 99 долара/година и предлага неограничени емисии, неограничени табла, 60 точки данни/минута и 60 дни съхранение.

Трябва да се регистрирате за Adafruit IO на уебсайта им. Следвайте стъпка по стъпка инструкциите [тук](https://learn.adafruit.com/welcome-to-adafruit-io/overview). Ако не ограничите качването до максимум 1 качване на 2 секунди (30 качвания/минута), ще получите това предупреждение и временно блокиране от Adafruit IO

![Снимка на предупреждението на Adafruit IO за ограничаване на качванията](assets/images/AdafruitIO_TemporaryBlockWarning.png)

### Инсталиране на Adafruit IO в Arduino IDE

За да инсталирате библиотеката Adafruit IO за Arduino, отворете Arduino IDE и отидете на Tools -> Library -> Manage Libraries. Когато се отвори Library Manager, потърсете "Adafruit IO Arduino” и превъртете, за да намерите съвпадението:

![Снимка на екрана на Library Manager, показваща Adafruit IO Arduino](assets/images/ArduinoIDE_InstallAdafruitIOLibrary.png)

Когато ви бъде поискано да инсталирате зависимости, кликнете върху "Инсталирай всички"

![Снимка на екрана, показваща опцията "Инсталирай всички", когато ви бъде поискано да инсталирате зависимости](assets/images/ArduinoIDE_InstallAllAdafruitIODependencies.png)

### Използване на Adafruit IO

Adafruit е публикувала 7-степенно ръководство, което обхваща всичко от качването на [данни от сензори](https://learn.adafruit.com/adafruit-io-basics-analog-input) и преглеждането им на табло (отне ни около 5 минути да го настроим) до изпращането на данни от Adafruit IO за управление на [RGB LED](https://learn.adafruit.com/adafruit-io-basics-color) или [серво мотор](https://learn.adafruit.com/adafruit-io-basics-servo). Можете да получите достъп до тези примери (и много други) в Arduino IDE, като отидете на File -> Examples -> Adafruit IO Arduino:

![Снимка на Arduino IDE, показваща къде да намерите примерите за Adafruit IO](assets/images/ArduinoIDE_ScreenshotOfAdafruitIOExamples.png)

## Да направим нещо!

Препоръчваме да следвате [ръководството](https://learn.adafruit.com/adafruit-io-basics-analog-input) на Adafruit IO, за да научите всички аспекти на IoT платформата. Като начало обаче създадохме прост сензор в реално време, базиран на примера Analog Input Adafruit. Изходният код е [тук](https://github.com/adafruit/Adafruit_IO_Arduino/tree/master/examples/adafruitio_08_analog_in) или можете да го намерите чрез File -> Examples -> Adafruit IO Arduino -> adafruitio_08_analog_in.

Тъй като максималната скорост на качване е 30 точки данни/минута (1 точка данни на всеки две секунди), ние ограничаваме качването. Ако стойността на фоторезистора се е променила, качваме с максимална скорост на всеки две секунди. Ако стойността на фоторезистора не се е променила, качваме с честота веднъж на всеки 10 секунди.

### Веригата

Имаме фоторезистор в делител на напрежение с резистор 10k, свързан към `A7` (можем да използваме само пинове ADC1, защото ще използваме WiFi). Аналоговото входно напрежение ще се увеличава с увеличаването на нивото на яркост. Задвижваме PWM изход на пин GPIO 21, чийто работен цикъл е обратно пропорционален на нивото на осветеност, като по този начин включваме LED, който свети по-ярко с намаляването на нивото на осветеност.

![Схема и диаграма на веригата за LED фоторезистор с Huzzah32](assets/images/Huzzah32_Photoresistor_CircuitDiagramAndSchematic_Fritzing.png)

### Кодът

<!-- https://github.com/makeabilitylab/arduino/blob/master/ESP32/WiFi/IoTPhotoresistorLed/IoTPhotoresistorLed.ino -->

Кодът се намира в [github](https://github.com/makeabilitylab/arduino/tree/master/ESP32/WiFi/IoTPhotoresistorLed). Забележка: има два файла. Файлът [IotPhotoresistorLed.ino] (https://github.com/makeabilitylab/arduino/blob/master/ESP32/WiFi/IoTPhotoresistorLed/IoTPhotoresistorLed.ino) и [config.h](https://github.com/makeabilitylab/arduino/blob/master/ESP32/WiFi/IoTPhotoresistorLed/config.h).
 

В файла `config.h` трябва да промените следното:

{% highlight C %}
// посетете io.adafruit.com, ако трябва да създадете акаунт
// или ако ви е необходим ключът за Adafruit IO.
#define IO_USERNAME "вашето_потребителско_име"
#define IO_KEY "вашият_ключ"

#define WIFI_SSID "вашият_ssid"
#define WIFI_PASS "your_pass"
{% endhighlight C %}

А ето и пълният код [IotPhotoresistorLed.ino](https://github.com/makeabilitylab/arduino/blob/master/ESP32/WiFi/IoTPhotoresistorLed/IoTPhotoresistorLed.ino):

<!-- gist-it не работи, затова сега използвам emgithub -->
<!-- <script src="https://gist-it.appspot.com/https://github.com/makeabilitylab/arduino/blob/master/ESP32/WiFi/IoTPhotoresistorLed/IoTPhotoresistorLed.ino ?footer=minimal"></script> -->

<script src="https://emgithub.com/embed.js?target=https%3A%2F%2Fgithub.com%2Fmakeabilitylab%2Farduino%2Fblob%2Fmaster%2FESP32%2FWiFi%2FIoTPhotoresistorLed%2FIoTPhotoresistorLed.ino&style=github&showCopy=on"></script>

Този [изходен код](https://github.com/makeabilitylab/arduino/blob/master/ESP32/WiFi/IoTPhotoresistorLed/IoTPhotoresistorLed.ino) се намира в GitHub.
{: .fs-1 }

### Видео за Workbench

Ето кратко видео, което показва запис с Workbench, съчетан с екранен запис на Adafruit IO.

<iframe width="736" height="414" src="https://www.youtube.com/embed/DgCFUHGSKSM" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

## Предишна лекция

<span class="fs-6">
[Предишна: Капацитивно докосване](capacitive-touch-sensing.md){: .btn .btn-outline }
</span>
