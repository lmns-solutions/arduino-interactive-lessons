---
lang: bg
permalink: /esp32/tone.html
page_id: esp32-tone
layout: default
title: L5&#58; Възпроизвеждане на тонове
parent: ESP32
has_toc: true # (по подразбиране)
usemathjax: true
comments: true
usetocbot: true
nav_order: 5
---
# {{ page.title | replace_first:"L",'Урок '}}
{: .no_toc }

## Съдържание
{: .no_toc .text-delta }

1. Съдържание
{:toc}
---

<iframe width="736" height="414" src="https://www.youtube.com/embed/zFg1fSFGL7o" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
**Видео.** Видео, демонстриращо класа [Tone32.hpp](https://github.com/makeabilitylab/arduino/blob/master/MakeabilityLab_Arduino_Library/ src/Tone32.hpp), който поддържа продължителност на възпроизвеждане на ESP32. Кодът, който се изпълнява на ESP32, е достъпен [тук](https://github.com/makeabilitylab/arduino/blob/master/ESP32/Tone/AnalogInputTone32WithOLED/AnalogInputTone32WithOLED.ino). Уверете се, че звукът ви е включен.
{: .fs-1 }

В Arduino функцията [`tone()`](https://www.arduino.cc/reference/en/language/functions/advanced-io/tone/) генерира правоъгълна вълна с определена честота на пин и се използва за "възпроизвеждане" на тонове на пиезо зумери или високоговорители; обаче, тя [е известна с това, че не се поддържа](https://www.thomascountz.com/2021/02/21/arduino-tone-for-esp32) на ESP32. В този урок ще ви предоставим малко контекст за този проблем и след това ще ви покажем как да възпроизвеждате тонове на ESP32, използвайки [LEDC PWM библиотеката](https://github.com/espressif/arduino-esp32/blob/master/cores/esp32/esp32-hal-ledc.c), която използвахме и в урока [ESP32 LED Fade](led-fade.md).

## Проблемът с тоновете на ESP32

Arduino библиотеката на ESP32, наречена [arduino-esp32](https://github.com/espressif/arduino-esp32/), се опитва да имитира и/или директно да възпроизведе функционалността на [core Arduino](https://github.com/arduino/ArduinoCore-avr); обаче, както видяхме в нашия [урок за затъмняване на LED на ESP32](../esp32/ led-fade.md), това не винаги е възможно и ключови функции, като `analogWrite`, са различни.

Точно както `analogWrite` не се поддържа в [arduino-esp32](https://github.com/espressif/arduino-esp32/), така и [`tone()`](https://www.arduino.cc/reference/en/ language/functions/advanced-io/tone/) не е налична. Припомнете си, че в Arduino `tone()` генерира квадратна вълна с определена честота (с фиксиран 50% работен цикъл) на пин и се използва за "възпроизвеждане" на тонове на пиезо зумери или високоговорители. В нашата [Въведение в Arduino](../arduino/index.md) например, ние използвахме [`tone()`](https://www.arduino.cc/reference/en/language/functions/advanced-io/tone/), за да създадем [пиано](../arduino/piano.md).

Ако обаче опитате да компилирате код с `tone()`, използвайки ESP32, ще получите следната грешка на компилатора: `"tone" не е деклариран в този обхват`. По този начин дори основните примери за тонове, вградени в Arduino IDE, като `Примери -> Цифрово -> toneMelody`, се провалят, както е показано по-долу.

![](assets/images/ESP32_CompilerError_ToneNotDeclaredInThisScope.png)
**Фигура.** Пример за това как дори основни примери за тон, като [toneMelody.ino](https://github.com/arduino/arduino-examples/blob/main/examples/02.Digital/toneMelody/toneMelody.ino), който се доставя като вграден пример с Arduino IDE, се провалят при избрана платка ESP32.
{: .fs-1 }

Липсата на поддръжка на [`tone()`](https://www.arduino.cc/reference/en/language/functions/advanced-io/tone/) е причинила много разочарование и объркване в общността на производителите, включително [Issue #980](https://github.com/espressif/arduino-esp32/ issues/980) и [Issue #1720](https://github.com/espressif/arduino-esp32/issues/1720) в [arduino-esp32](https://github.com/espressif/arduino-esp32/) GitHub репозитория, както и [форума](https://community.platformio.org/t/tone-not-working-on-espressif32-platform/7587) и [блога](https://www.thomascountz.com/2021/02/21/ arduino-tone-for-esp32).

Какво можем да направим по този въпрос? И защо тонът не се поддържа? Нека разгледаме по-подробно.

<!-- В този урок ще ви покажем как да възпроизвеждате тонове с помощта на [`arduino-esp32`](https://github.com/espressif/arduino-esp32). -->

## Как работи тонът на Arduino?

Припомнете си, че [тонът](https://www.arduino.cc/reference/en/language/functions/advanced-io/tone/) на Arduino предоставя три основни метода:

{% highlight C %}
void tone(uint8_t pin, unsigned int frequency)
void tone(uint8_t pin, unsigned int frequency, unsigned long duration)
void noTone(uint8_t pin)
{% endhighlight C %}

И двата метода за тон управляват PWM вълнова форма на предоставения пин с дадената честота, използвайки таймер прекъсвания. Втората версия добавя параметър `duration`, който ви позволява да определите колко *дълго* (в милисекунди) да се възпроизвежда тонът. И в двата случая можете да извикате `noTone (pin)`, за да спрете излъчването на PWM вълната и да изключите тона.

<!-- С коментари:

{% highlight C %}
/**
* @brief Задвижва PWM вълна с дадената честота на предоставения изходен пин
* за дадената продължителност, в милисекунди.
*
* @param pin Arduino пинът, на който да се генерира тонът.
* @param frequency Честотата на PWM вълната (задвижвана при 50% работен цикъл)
* @param duration Продължителността на тона в милисекунди (по избор).
*/
void tone(uint8_t pin, unsigned int frequency, unsigned long duration)

/**
* @brief Задвижва PWM вълнова форма с дадената честота на предоставения изходен пин.
* Извикайте noTone(), за да спрете.
*
* @param pin Arduino пинът, на който да се генерира тонът.
* @param frequency Честотата на PWM вълновата форма (задвижвана при 50% работен цикъл) 
*/
void tone(uint8_t pin, unsigned int frequency)

/**
* @brief Спира PWM вълната на предоставения пин
*
* @param pin Arduino пинът, на който да се спре тонът.
*/
void noTone(uint8_t pin)
{% endhighlight C %} 

** Код.** За имплементации на тона, вижте [Tone.cpp](https://github.com/arduino/ArduinoCore-avr/blob/master/cores/arduino/Tone.cpp) за [ArduinoCore-avr](https://github.com/arduino/ArduinoCore-avr) и [Tone.cpp](https://github.com/arduino/ArduinoCore-samd/blob/master/cores/arduino/Tone.cpp) за [ArduinoCore-samd](https://github.com/arduino/ArduinoCore-samd) . Вижте също [бележките на Брет Хагман](https://github.com/bhagman/Tone#ugly-details).
{: .fs-1 }
-->

Този тон API е прост и лесно разбираем. Той е имплементиран в ядрото на Arduino, включително за микроконтролери на базата на AVR—[ArduinoCore-avr](https://github.com/arduino/ArduinoCore-avr) ( [Tone.cpp](https://github.com/arduino/ArduinoCore-avr/blob/master/cores/arduino/Tone.cpp))—и микроконтролери на базата на SAMD— [ArduinoCore-samd](https://github.com/arduino/ArduinoCore-samd) ([Tone.cpp](https://github.com/ arduino/ArduinoCore-samd/blob/master/cores/arduino/Tone.cpp)). Когато използваме Arduino, очакваме [`tone()`](https://www.arduino.cc/reference/en/language/functions/advanced-io/tone/) да е налице!

За да генерира PWM вълни и да проследява продължителността на възпроизвеждането на тона, библиотеката tone използва хардуерни таймери (известни още като таймерни прекъсвания). Тези хардуерни таймери и функционалността им обаче се различават значително в зависимост от микроконтролерния чип. Микроконтролерите Atmel AVR като [ATmega328](https://www.microchip.com/wwwproducts/en/ ATmega328), използван в Arduino Uno, и [ATmega32u4](https://www.microchip.com/wwwproducts/en/atmega32u4), използван в Arduino Leonardo, ги обработват по един начин, докато микроконтролерите Atmel [SAMD21](https://www.seeedstudio.com/blog/ 2020/01/09/samd21-arduino-boards-which-one-should-you-use/) ги обработват по друг начин. Дори само за микроконтролерите на базата на AVR има много нюанси и разлики – вижте `#ifdef` в [Tone.cpp](https://github.com/arduino/ArduinoCore-avr/ blob/master/cores/arduino/Tone.cpp) за [ArduinoCore-avr](https://github.com/arduino/ArduinoCore-avr).

Най-важното за нас е, че Expressif реши **да не** имплементира `tone()` в [arduino-esp32](https://github.com/espressif/arduino-esp32). Макар да не сме сигурни защо, какво можем да направим по въпроса?

## Възпроизвеждане на тонове на ESP32

Не се страхувайте, нещата не са толкова зле, колкото изглеждат. Както посочва Томас Каунц в [GitHub Issue #1720](https://github.com/espressif/arduino-esp32/issues/1720#issuecomment-782876308), библиотеката [LEDC PWM](https://github.com/espressif/arduino-esp32/blob/master/cores/esp32/esp32-hal-ledc.c) — която използвахме в урока [ESP32 LED Fade](led-fade.md) — всъщност има методи, свързани с тоновете, включително:

{% highlight C %}
double ledcWriteTone (uint8_t chan, double freq)
double ledcWriteNote(uint8_t chan, note_t note, uint8_t octave)
{% endhighlight C %}

където `note_t` е дефиниран както следва в [esp32-hal-ledc.h](https://github.com/espressif/arduino-esp32/blob/master/cores/esp32/esp32-hal-ledc.h):

{% highlight C %}
typedef enum {
NOTE_C, NOTE_Cs, NOTE_D, NOTE_Eb, NOTE_E, NOTE_F, NOTE_Fs, 
NOTE_G, NOTE_Gs, NOTE_A, NOTE_Bb, NOTE_B, NOTE_MAX
} note_t;
{% endhighlight C %}

**Код.** Вижте [esp32-hal-ledc.h](https://github.com/espressif/arduino-esp32/blob/master/cores/esp32/esp32-hal-ledc.h) и [esp32-hal-ledc.c](https://github.com/ espressif/arduino-esp32/blob/master/cores/esp32/esp32-hal-ledc.c) от [arduino-esp32 repo](https://github.com/espressif/arduino-esp32).
{: .fs-1 }

За да използваме `ledcWriteTone` и `ledcWriteNote`, можем да следваме подход, подобен на този, който използвахме за затъмняване на LED. Първо, нека да изградим нашата верига.

### Примерна верига

Нашата верига е максимално опростена. Просто свържете пиезо зумера към GPIO пин. В този случай използваме GPIO пин 26. В нашите курсове често използваме [TDK PS1240 ](https://product.tdk.com/system/files/dam/doc/product/sw_piezo/sw_piezo/piezo-buzzer/catalog/piezoelectronic_buzzer_ps_en. pdf) пиезо зумери (около 0,46 $ [Mouser](https://www.mouser.com/ProductDetail/810-PS1240P02BT) или 1,35 $ в [Adafruit](https://www.adafruit. com/product/160)). Тези зумери работят както с 3V, така и с 5V правоъгълни вълни. Резонансната им честота (най-силен тон) е 4kHz, но можете да ги задвижите с много по-голям диапазон (ние сме тествали от 32Hz до 10Khz, при което звукът е пронизващ). Като неполяризирани устройства, те могат да бъдат свързвани в двете посоки (като резистори).

![](assets/images/ESP32_Tone_PiezoBuzzerCircuit.png)
**Фигура.** Схема за свързване на [PS1240](https://www.adafruit.com/product/160) пиезо зумер с ESP32. Свързахме зумера към GPIO Pin 26. Изображението е направено в Fritzing и PowerPoint.
{: .fs-1 }

### Пример за код

Сега нека напишем кода.

Първо, трябва да "прикачим" пиезо зумера към един от 16-те PWM канала, налични на ESP32, като използваме функцията `ledcAttachPin`. В този случай ще използваме Pin 26 и PWM канал 0. Припомнете си, че ESP32 има 16 PWM канала (0-15) и всеки от тях може да бъде конфигуриран независимо, за да управлява различни PWM вълни. В софтуера "прикачваме" пинове към тези PWM канали, за да получим вълната.

{% highlight C %}
// Променете това в зависимост от мястото, където сте поставили пиезо зумера
const int TONE_OUTPUT_PIN = 26;

// ESP32 има 16 канала, които могат да генерират 16 независими вълни
// Тук ще изберем PWM канал 0
const int TONE_PWM_CHANNEL = 0; 

void setup() {
// ledcAttachPin(uint8_t pin, uint8_t channel);
ledcAttachPin(TONE_OUTPUT_PIN, TONE_PWM_CHANNEL);
}
{% endhighlight C %}

Чудесно, сега сме свързали Pin 26 с PWM канал 0.

Сега можем просто да възпроизведем нота, използвайки `ledcWriteNote`, или сурова честота, използвайки `ledcWriteTone`. Например, кодът по-долу повтаря възпроизвеждането на средното до с `ledcWriteNote`, а след това честотата 800 Hz с `ledcWriteTone` с 500 ms паузи между тях.

{% highlight C %}
void loop() {
// Възпроизвежда средната C скала
ledcWriteNote(TONE_PWM_CHANNEL, NOTE_C, 4);
delay(500);
ledcWriteTone(TONE_PWM_CHANNEL, 800);
delay(500);
}
{% endhighlight C %}

Това е всичко! 

Сега, тези с остър поглед може би са забелязали, че няма функции, които приемат параметър `duration`. Да, това е малък проблем. Да, ще се заемем с него!

<!-- С коментари:

{% highlight C %}

/**
* Този typedef note_t се използва във функцията ledcWriteNote
*/
typedef enum {
NOTE_C, NOTE_Cs, NOTE_D, NOTE_Eb, NOTE_E, NOTE_F, NOTE_Fs, NOTE_G, NOTE_Gs, NOTE_A, NOTE_Bb, NOTE_B, NOTE_MAX
} note_t;

/**
* @brief Записва PWM вълнова форма с дадена честота на предоставения PWM канал
*
* @param chan PWM каналът, на който да се възпроизведе тона (0 - 15)
* @param freq Честотата на PWM вълновата форма (задвижвана при 50% работен цикъл)
*/
double ledcWriteTone(uint8_t chan, double freq)

/**
* @brief Записва PWM вълнова форма с дадена нота и октава на предоставения PWM канал
*
* @param chan PWM каналът, на който да се възпроизведе тона (0 - 15)
* @param note Нотата, която да се възпроизведе
* @param octave Октавата, на която да се възпроизведе (0 - 8)
*/
double ledcWriteNote(uint8_t chan, note_t note, uint8_t octave)
{% endhighlight C %}

**Код.** Вижте [esp32-hal-ledc.h](https://github.com/espressif/arduino-esp32/blob/master/cores/esp32/esp32-hal-ledc.h) и [esp32-hal-ledc.c](https://github.com/espressif/arduino-esp32/blob/master/ cores/esp32/esp32-hal-ledc.c) от [ардуино-esp32 репо](https://github.com/espressif/arduino-esp32).
{: .fs-1 } -->

Да започнем да творим!

## Да направим нещо

В дейностите по-долу първо ще възпроизведем гама и различни сурови честоти, преди да въведем класа Tone32.hpp, който помага да се абстрахираме от някои сложности. Обикновено се опитваме да вграждаме mp4 видеоклипове директно в нашите уроци. За да контролираме по-лесно възпроизвеждането и звука, тук ще използваме вградени клипове от YouTube. Затова се уверете, че сте включили звука (и евентуално носете слушалки, за да не притеснявате околните).


### Възпроизвеждане на гамата C

Използвайки същата верига като преди, нека напишем код за възпроизвеждане на проста гама C мажор, въз основа на коментара на Thomas Countz в [GitHub Issue 1720](https://github.com/Thomascountz). Макар че бихме могли да използваме масив, за да преминаваме през нотите, нека запазим нещата супер прости и просто да напишем всяка нота директно. Пълният код е:

{% highlight C %}
// Променете това в зависимост от мястото, където сте поставили пиезо зумера
const int TONE_OUTPUT_PIN = 26;

// ESP32 има 16 канала, които могат да генерират 16 независими вълнови форми
// Тук ще изберем PWM канал 0
const int TONE_PWM_CHANNEL = 0; 

void setup() {
ledcAttachPin(TONE_OUTPUT_PIN, TONE_PWM_CHANNEL);
}

void loop() {
// Възпроизвежда средната C скала
ledcWriteNote(TONE_PWM_CHANNEL, NOTE_C, 4);
delay(500);
ledcWriteNote(TONE_PWM_CHANNEL, NOTE_D, 4);
delay(500);
ledcWriteNote(TONE_PWM_CHANNEL, NOTE_E, 4);
delay(500);
ledcWriteNote(TONE_PWM_CHANNEL, NOTE_F, 4);
delay(500);
ledcWriteNote(TONE_PWM_CHANNEL, NOTE_G, 4);
забавяне(500);
ledcWriteNote(TONE_PWM_CHANNEL, NOTE_A, 4);
забавяне(500);
ledcWriteNote(TONE_PWM_CHANNEL, NOTE_B, 4);
забавяне(500);
ledcWriteNote(TONE_PWM_CHANNEL, NOTE_C, 5);
забавяне(500);
}
{% endhighlight C %}

И видео демонстрация по-долу:

<iframe width="736" height="414" src="https://www.youtube.com/embed/H7MOhibjOO0" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
**Видео. ** Видео демонстрация на [PlayScale.ino](https://github.com/makeabilitylab/arduino/blob/master/ESP32/Tone/PlayScale/PlayScale.ino). Действителната версия, показана във видеото, е [PlayScaleWithOLED.ino](https://github.com/makeabilitylab/arduino/blob/master/ESP32/Tone/PlayScaleWithOLED/PlayScaleWithOLED.ino). Уверете се, че звукът ви е включен.
{: .fs-1 }

### Четене на аналогов вход, извеждане на сурови честоти

Добре, сега нека направим малко по-сложна версия, която чете аналогов вход и преобразува тази стойност в изходна честота. За нашата демонстрация използваме потенциометър. Но, разбира се, всеки аналогов вход би свършил работа!

#### Изграждане на веригата

Трябва да модифицираме леко веригата си, като добавим потенциометър – в този случай 10K потенциометър.

![](assets/images/ESP32_Tone_PiezoBuzzerWithPotentiometerCircuit.png)
**Фигура.** Схема на веригата на Huzzah32 с пиезо зумер и потенциометър. Изображението е създадено в Fritzing и PowerPoint.
{: .fs-1 }

#### Напишете кода

Сега нека напишем код, който да приема аналоговия вход и да го използва за настройка на честотата на изходната вълнова форма на PWM.

{% highlight C %}
// Променете това в зависимост от мястото, където сте поставили пиезо зумера
const int TONE_OUTPUT_PIN = 26;

// Променете това в зависимост от мястото, където сте свързали сензора
const int SENSOR_INPUT_PIN = A1;

// ESP32 има 16 канала, които могат да генерират 16 независими вълни
// Тук ще изберем PWM канал 0
const int TONE_PWM_CHANNEL = 0;
 

const int MIN_FREQ = 32; // минимална честота в херци
const int MAX_FREQ = 1500; // максимална честота в херци (1500 е малко пронизваща за ушите; по-високата честота е още по-пронизваща)
const int MAX_ANALOG_VAL = 4095;

void setup() {
ledcAttachPin(TONE_OUTPUT_PIN, TONE_PWM_CHANNEL);
}

void loop() {

int sensorVal = analogRead(SENSOR_INPUT_PIN);
int pwmFreq = map(sensorVal, 0, MAX_ANALOG_VAL, MIN_FREQ, MAX_FREQ);

// Сигнатурата на ledcWriteTone: double ledcWriteTone(uint8_t chan, double freq)
// Вижте: https://github.com/espressif/arduino-esp32/blob/master/cores/esp32/esp32-hal-ledc.c
ledcWriteTone(TONE_PWM_CHANNEL, pwmFreq);

delay(50);
}
{% endhighlight C %}

Ето видео демонстрация.

<iframe width="736" height="414" src="https://www.youtube.com/embed/xr_G_fkHcSo" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
**Видео.** Видео демонстрация на [AnalogInputTone.ino](https://github.com/makeabilitylab/arduino/blob/master/ESP32/Tone/AnalogInputTone/AnalogInputTone.ino) . Действителната версия, показана във видеото, е [AnalogInputToneWithOLED.ino](https://github.com/makeabilitylab/arduino/blob/master/ESP32/Tone/AnalogInputToneWithOLED/AnalogInputToneWithOLED.ino). Уверете се, че звукът ви е включен.
{: .fs-1 }

### Представяне на класа Tone32.hpp

Примерите по-горе демонстрират как да използвате `ledcWriteTone` и `ledcWriteNote` от [esp32-hal-ledc.c](https://github.com/espressif/arduino-esp32/blob/master/cores/ esp32/esp32-hal-ledc.c), за да управлявате конкретни PWM честоти на изходните пинове — тези правоъгълни вълни се проявяват като звук с пиезо зумери.

Въпреки това, тези методи не са толкова лесни за използване, колкото библиотеката Arduino [`tone()`](https://www.arduino.cc/ reference/en/language/functions/advanced-io/tone/) и не поддържат продължителност на възпроизвеждане. За да преодолеем тези ограничения, създадохме [Tone32.hpp](https://github.com/makeabilitylab/arduino/blob/master/MakeabilityLab_Arduino_Library/src/Tone32.hpp). Tone32.hpp е част от [Makeability Lab Arduino Library](https://github.com/makeabilitylab/arduino/tree/master/MakeabilityLab_Arduino_Library). Следвайте инструкциите [тук](https://github.com/makeabilitylab/arduino/tree/master/MakeabilityLab_Arduino_Library) за инсталиране и употреба.

#### Основни разлики между Tone32 и библиотеката tone

Има няколко основни разлики с библиотеката [`tone()`](https://www.arduino.cc/reference/en/language/functions/advanced-io/tone/):

- Първо, ние използваме обектно-ориентиран подход. За да създадете обект Tone32, просто извикайте `Tone32 tone32 (pin, pwmChannel)`, което създава обект Tone32 с дадения изходен пин и PWM канал.

- Второ, докато [`tone()`](https://www.arduino.cc/reference/en/language/functions/advanced-io/tone/) използва прекъсвания на таймера, за да проследява продължителността на възпроизвеждането – и автоматично спира възпроизвеждането след изтичане на продължителността – ние използваме подход на "проверка". Затова трябва да извикате `update()` на всеки `loop ()`. Това е от съществено значение, ако използвате параметрите за продължителност. Забележка: Насърчавам другите да адаптират Tone32, за да използват прекъсвания на таймера, но за нашите цели анкетирането е подходящо (стига да извиквате update() последователно с ограничено време между извикванията)

- Трето, за разлика от [`tone()`](https://www.arduino.cc/reference/en/language/functions/advanced-io/tone/), вие възпроизвеждате тонове чрез `playNote` или `playTone`, като и двете са претоварени функции с опции за `duration`.

#### Основни методи на Tone32

Ето основните методи на Tone32:

{% highlight C %}
Tone32(uint8_t outputPin, uint8_t pwmChannel) // конструктор

// Възпроизвеждане на честота при зададена нота и октава
void playNote(note_t note, uint8_t octave)
void playNote(note_t note, uint8_t octave, unsigned long duration)

// Възпроизвеждане на честота
void playTone(double freq)
void playTone (double freq, unsigned long duration)

void stopPlaying() // спира възпроизвеждането
void update() // извиква се при всяко преминаване през loop()
{% endhighlight C %}

<!-- С коментари:

{% highlight C %}
/**
* @brief Създаване на нов обект Tone32
*
* @param outputPin Пинът, свързан с вашия пиезо зумер
* @param pwmChannel PWM каналът, който искате да използвате: ESP32 поддържа 0 - 15
*/
Tone32(uint8_t outputPin, uint8_t pwmChannel)

/**
* @brief Възпроизвежда текущата note_t в дадената октава
* note_t е дефиниран тук:
*https://github.com/espressif/arduino-esp32/blob/master/cores/esp32/esp32-hal-ledc.h
* @param note нотата, която да се възпроизведе
* @param octave трябва да е между 0 и 8
*/
void playNote(note_t note, uint8_t octave)

/**
* @brief Възпроизвежда текущата note_t в дадената октава за дадена продължителност в милисекунди
* За да работи това, трябва да извикате update() при всяко извикване на loop()
*
* @param note нотата, която да се възпроизведе
* @param octave трябва да е между 0 и 8
* @param duration продължителност на възпроизвеждането в милисекунди
*/
void playNote (note_t note, uint8_t octave, unsigned long duration)

/**
* @brief Възпроизвежда дадената честота. За да спрете, извикайте stopPlaying()
*
* @param freq
*/
void playTone(double freq)

/**
* @brief Възпроизвежда дадената честота за дадена продължителност в милисекунди
*
* @param freq
* @param duration продължителност на възпроизвеждането в милисекунди
*/
void playTone(double freq, unsigned long duration)

/**
* @brief Спира възпроизвеждането
*/
void stopPlaying()

/**
* @brief За да работи някой от параметрите за продължителност, трябва да извикате update()
* при всеки цикъл ()
*/
void update()
{% endhighlight C %} -->

Има и други полезни функции, като:

{% highlight C %}

// Връща true, ако в момента се възпроизвежда, и false в противен случай
bool isPlaying() const

// Получава текущата продължителност на възпроизвеждането в милисекунди. Ако нищо не се възпроизвежда, връща 0
unsigned long getPlayDuration () const

// Получава оставащата продължителност на възпроизвеждането в милисекунди. Ако нищо не се възпроизвежда, връща 0
unsigned long getPlayDurationRemaining() const
{% endhighlight C %}

Нека опитаме да създадем нещо с [Tone32.hpp](https://github.com/makeabilitylab/arduino/blob/master/MakeabilityLab_Arduino_Library/src/Tone32.hpp)!

#### Демонстрация на продължителността на тоновете в Tone32

За да демонстрираме използването на продължителността, написахме [AnalogInputTone32.ino](https://github.com/makeabilitylab/arduino/blob/master/ESP32/Tone/AnalogInputTone32/AnalogInputTone32.ino), който преминава нагоре и надолу по скалата на до, използвайки аналогов вход (използвахме потенциометър). Когато "кацнете" на нова нота, възпроизвеждаме честотата на нотата за 500 ms. Ще използваме същата верига с пиезо зумер + потенциометър като преди, но с нов код.

Ето целия код:

{% highlight C %}
#include <Tone32.hpp>

const int NUM_NOTES_IN_SCALE = 8;
const note_t C_SCALE[NUM_NOTES_IN_SCALE] = { NOTE_C, NOTE_D, NOTE_E, NOTE_F, NOTE_G, NOTE_A, NOTE_B, NOTE_C };
 
const int C_SCALE_OCTAVES[NUM_NOTES_IN_SCALE] = { 4, 4, 4, 4, 4, 4, 4, 5 };
const char C_SCALE_CHARS[NUM_NOTES_IN_SCALE] = { "C", "D", "E", "F", "G", "A", "B", "C" }; 
note_t _lastNote = NOTE_C;

// Променете това в зависимост от мястото, където свързвате вашия пиезо зумер
const int TONE_OUTPUT_PIN = 26;

// Променете това в зависимост от мястото, където свързвате вашия вход
const int SENSOR_INPUT_PIN = A1;

// ESP32 има 16 канала, които могат да генерират 16 независими вълнови форми
// Тук ще изберем PWM канал 0
const int TONE_PWM_CHANNEL = 0; 

// Възпроизвеждайте всяка нота за 500 ms
const int PLAY_NOTE_DURATION_MS = 500;

// ESP32 има 12-битов ADC, така че нашата максимална аналогова стойност е 4095
const int MAX_ANALOG_VAL = 4095;

// Създайте нашия Tone32 обект
Tone32 _tone32(TONE_OUTPUT_PIN, TONE_PWM_CHANNEL);

void setup() {
// празно!
}

void loop() {

int sensorVal = analogRead(SENSOR_INPUT_PIN);
int scaleIndex = map(sensorVal, 0, MAX_ANALOG_VAL, 0, NUM_NOTES_IN_SCALE - 1);

// Просто се движете нагоре или надолу по скалата въз основа на позицията на sensorVal
note_t note = C_SCALE[scaleIndex];
int octave = C_SCALE_OCTAVES[scaleIndex];
if(_lastNote != note){
_tone32.playNote(note, octave, PLAY_NOTE_DURATION_MS);
}

// ВАЖНО: За разлика от обичайната функция tone на Arduino, която използва прекъсвания на таймера
// за проследяване на времето и автоматично изключване на PWM вълните след изтичане на продължителността
// интервал, ние използваме "polling". Затова трябва да извикате update(), за да изключите
// звука автоматично след изтичане на продължителността на възпроизвеждане
_tone32.update();

// Проследяване на последната нота (възпроизвеждаме нота само при промяна на нотата)
// Да, това означава, че в тази проста демонстрация не можем да повторим една и съща
// нота два пъти последователно!
_lastNote = note;
}
{% endhighlight C %}

Ето видео демонстрация. Обърнете внимание как показваме оставащото време за всеки тон на OLED дисплея – това е, за да подчертаем функционалността на [Tone32.hpp](https://github.com/makeabilitylab/arduino/blob/master/MakeabilityLab_Arduino_Library/src/ Tone32.hpp).

<iframe width="736" height="414" src="https://www.youtube.com/embed/zFg1fSFGL7o" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
**Видео.** Видео, демонстриращо [AnalogInputTone32](https://github.com/makeabilitylab/arduino/blob/master/ESP32/Tone/AnalogInputTone32/AnalogInputTone32.ino). Имайте предвид, че това видео показва лека вариация с OLED изход, наречена [AnalogInputTone32WithOLED.ino](https://github.com/makeabilitylab/arduino/blob/master/ESP32/Tone/AnalogInputTone32WithOLED/AnalogInputTone32WithOLED.ino). Уверете се, че звукът ви е включен.
{: .fs-1 }

#### Бонус видео с отскачаща топка

Накрая, включихме бонус [проста демонстрация с отскачаща топка](https://github.com/makeabilitylab/arduino/blob/master/ ESP32/Tone/BallBounceTone32WithOLED/BallBounceTone32WithOLED.ino), използвайки библиотеката Tone32.hpp, като отново подчертаваме функционалността на `duration`. Тук възпроизвеждаме кратък тон, когато топката отскача от пода или тавана.

<iframe width="736" height="414" src="https://www.youtube.com/embed/cy7Jeri7vOA" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
**Видео.** Видео, демонстриращо [BallBounceTone32WithOLED.ino](https://github.com/makeabilitylab/arduino/blob/master/ESP32/Tone/BallBounceTone32WithOLED/BallBounceTone32WithOLED.ino). Уверете се, че звукът ви е включен.
{: .fs-1 }

## Ресурси

- [Тонът не е деклариран в този обхват](https://github.com/espressif/arduino-esp32/issues/1720), arduino-esp32 GitHub Issue #1720

- [Arduino Tone за ESP32](https://www. thomascountz.com/2021/02/21/arduino-tone-for-esp32), Thomas Countz

- [ESP32Servo](https://github.com/madhephaestus/ESP32Servo), библиотека Servo на трета страна за ESP32, която се опитва да имитира точно [библиотеката Arduino Servo](https://www.arduino.cc/ reference/en/libraries/servo/), но също така има [tone](https://github.com/madhephaestus/ESP32Servo/blob/master/src/ESP32Tone.h) функционалност.
 

## Следващ урок

В [следващия урок](capacitive-touch-sensing.md) ще научим и ще използваме вградения модул за капацитивно докосване на ESP32.

<span class="fs-6">
[Предишен: Аналогов вход с ESP32](pot-fade.md){: .btn .btn-outline }
[Следващ: Капацитивно сензорно докосване с ESP32](capacitive-touch-sensing.md){: .btn .btn-outline }
</span>
