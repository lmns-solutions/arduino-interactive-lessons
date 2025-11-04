---
lang: bg
permalink: /arduino/rgb-led-fade.html
page_id: arduino-rgb-led-fade
layout: default
title: L7&#58; Кръстосано преливане на RGB LED
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

В този урок ще научите как да преливате между RGB цветове, използвайки [`analogWrite`](https://www.arduino.cc/reference/en/language/functions/analog-io/analogwrite/), как да използвате [HSL цветовото пространство](https://en.wikipedia.org/wiki/HSL_and_HSV), за да контролирате по-лесно (и независимо) оттенъка и яркостта, както и как да използвате и зареждате локални `C/C++` библиотеки.

---
**ЗАБЕЛЕЖКА:**

Това е най-сложният ни урок досега. От гледна точка на схемата нещата са лесни – схемата е същата като [по-рано](rgb-led.md) (ура!). От гледна точка на кодирането нещата са по-сложни. Ако нямате опит в кодирането, няма проблем, ако кодът не (напълно) смисъл. Опитайте се да го прочетете и разберете според настоящите си способности. Независимо от нивото ви на разбиране, опитайте да копирате кода и да си поиграете с него!

---

## Материали

Ще ви трябват същите материали като в предишния [урок за RGB LED](rgb-led.md). Припомнете си, че има **два типа** RGB LED: **дизайн с общ катод** и **дизайн с общ анод**, така че се уверете, че знаете кой от двата имате, тъй като това ще повлияе на схемата, която ще направите, и на кода, който ще напишете.

| Breadboard | Arduino | RGB LED | Резистори |
|:-----:|:-----:|:-----:|:-----:|
| ![Breadboard]({{ site.baseurl }}/assets/images/Breadboard_Half.png) | ![Arduino Uno]({{ site.baseurl }}/assets/images/ArduinoUno_Fritzing.png) | ![RGB LED]({{ site.baseurl }}/assets/images/RgbLED_Fritzing.png) | ![220 Ohm резистор]({{ site.baseurl }}/assets/images/Resistor220_Fritzing.png) |
| Breadboard | Arduino Uno, Leonardo или подобен | RGB LED (или с общ катод, или с общ анод) | **Три** резистора 220Ω |

## Изработване на веригата

Веригата е същата като в предишния [урок за RGB LED](rgb-led.md). Уверете се, че следвате подходящото окабеляване в зависимост от това дали използвате RGB LED с **общ катод** или **общ анод**.

| Окабеляване на RGB с общ катод | Окабеляване на RGB с общ анод |
|:-----:|:-----:|
| ![Окабеляване на платка за RGB LED с общ катод, където катодът е свързан към GND](assets/images/ArduinoUno_RgbLEDCommonCathode_WiringDiagramWithBreadboard.png) | ![Схема на свързване на платка за RGB LED с общ анод, където анодът е свързан към 5V](assets/images/ArduinoUno_RgbLEDCommonAnode_WiringDiagramWithBreadboard.png) |

## Написване на кода

Ще проучим и приложим два различни подхода за RGB преливане.

1. Първо, ще използваме `for` цикли, за да преминем през двойни комбинации между червени, зелени и сини LED цветове. Този подход се базира на [вече изтекъл gist](https://gist.github.com/jamesotron/766994) от потребителя `jamesotron`.
2. Второ, ще използваме HSL цветовото пространство, за да манипулираме **оттенъка** — това, което обикновено наричаме *цвят* — и след това ще го конвертираме в RGB цветовото пространство за нашите `analogWrite` повиквания. Този подход е по-ясен и по-малко сложен, но изисква използването на [отделна библиотека](https://github.com/ratkins/RGBConverter) за конвертиране от HSL в RGB.

С максималната изходна стойност на `analogWrite` от `255`, всеки вграден червен, зелен и син LED може да бъде настроен от `0` до `255`, което позволява 16 777 216 комбинации (256^3). Въпреки това, само малка част от тях се различават по възприятие. Всъщност, в първото ни решение за преливане, по подразбиране, преливаме само между 156 комбинации.

### Кросфейдинг в RGB цветовото пространство

Кодът (https://github.com/makeabilitylab/arduino/blob/master/Basics/analogWrite/CrossFadeRGB/CrossFadeRGB.ino) за преливане на RGB LED е най-сложният, който сме разглеждали досега (и ако нямате опит в програмирането, няма проблем, ако не го разбирате напълно). За тези, които посещават нашите инженерни курсове (като "Уbiquitous Computing”, "Physical Computing” или "Prototyping Interactive Systems”), се очаква да прочетете и разберете този код.

Има много различни начини за преливане на RGB LED в зависимост от цветовете, които искате да осветите, и от скоростта, с която искате да го направите. Ако искате да експериментирате и да изследвате RGB цветовото пространство, вижте [тази интерактивна визуализация](https://makeabilitylab.github.io/p5js/Color/ColorExplorer3D/), която създадохме в p5js.

Нашият конкретен метод за преливане работи чрез **увеличаване** на стойността на цвета на един LED (от `0` до `255`) и **намаляване** на стойността на друг (от `255` до `0`). Например, кодът започва с намаляване на стойността на червения LED и увеличаване на стойността на зеления LED. Когато стойността на червения LED достигне `0`, започваме да намаляваме стойността на друг LED (в този случай зеления). По същия начин, когато стойността на зеления LED достигне `255`, започваме да увеличаваме стойността на друг LED (в този случай синия LED) и т.н. 

По-конкретно, имаме масив `int _rgbLedValues[3]`, който съхранява нашите стойности `{int red, int green, int blue}`. Инициализираме масива на `{255, 0, 0}`—така че `red=255`, `green=0` и `blue=0`. Така че нашият RGB LED ще започне с червено.

{% highlight C %}
int _rgbLedValues[] = {255, 0, 0}; // Червено, зелено, синьо
{% endhighlight C %}

За да улесним индексирането в този масив и проследяването на състоянието, създаваме следния `enum`:

{% highlight C %}
enum RGB{
    RED,
    GREEN,
    BLUE,
    NUM_COLORS
};
{% endhighlight C %}

Този enum ни позволява да получим достъп до нашите RGB LED стойности, като пишем `_rgbLedValues[RED]`, `_rgbLedValues[GREEN]` и `_rgbLedValues[BLUE]`, вместо `_rgbLedValues[0]`, `_rgbLedValues[1]` и `_rgbLedValues[2]`. Enum не само подобрява четимостта на кода и помага да се избегнат ненужни грешки в индекса на масива, но се използва и за проследяване на състоянието с две променливи за проследяване на състоянието: `_curFadingUpColor` и `_curFadingDownColor`.
 

Нашият алгоритъм за преливане използва две `for` цикли, за да увеличи едновременно един цвят, докато намалява друг. Започваме с **увеличаване на зеленото** и **намаляване на червеното**, както се контролира от `enum RGB _curFadingUpColor = GREEN;`) и (`enum RGB _curFadingDownColor = RED;`), съответно.
 

След като достигнем максималната стойност на цвета `255` за текущия `_curFadingUpColor`, избираме следващия цвят, който да увеличим (започвайки с `RED`, след това `GREEN`, след това `BLUE` и обратно към `RED`). По същия начин, след като достигнем минималната стойност на цвета `0` за `_curFadingDownColor`, избираме следващия цвят, който да намалим (в същия ред като преди: от `RED` към `GREEN` към `BLUE` и после обратно към `RED`).

Пълният алгоритъм за избледняване е заложен в `loop()`:

{% highlight C %}
// Код, базиран на https://gist.github.com/jamesotron/766994 (вече не е наличен)
void loop() {

    // Увеличаване и намаляване на RGB LED стойностите за текущия
    // цвят на избледняване и текущия цвят на избледняване
    _rgbLedValues[_curFadingUp] += FADE_STEP;
    _rgbLedValues[_curFadingDown] -= FADE_STEP;

    // Проверка дали сме достигнали максималната стойност на цвета за избледняване
    // Ако е така, преминаване към следващия цвят за избледняване (преминаваме от ЧЕРВЕНО към ЗЕЛЕНО към СИНЬО
    // както е посочено в RGB enum)
    if(_rgbLedValues[_curFadingUp] > MAX_COLOR_VALUE){
        _rgbLedValues[_curFadingUp] = MAX_COLOR_VALUE;
        _curFadingUp = (RGB)((int)_curFadingUp + 1);

        if(_curFadingUp > (int)BLUE){
            _curFadingUp = RED;
        }
    }

    // Проверяваме дали текущият LED, който затъмняваме, е стигнал до нула
    // Ако е така, избираме следващия LED, който да започне да се затъмнява (отново преминаваме от ЧЕРВЕНО към 
    // ЗЕЛЕНО към СИНЬО, както е посочено в RGB enum)
    if(_rgbLedValues[_curFadingDown] < 0){
        _rgbLedValues [_curFadingDown] = 0;
        _curFadingDown = (RGB)((int)_curFadingDown + 1);

        if(_curFadingDown > (int)BLUE){
            _curFadingDown = RED;
        }
    }

    // Задайте цвета и след това забавете
    setColor(_rgbLedValues[RED], _rgbLedValues[GREEN], _rgbLedValues[BLUE]);
    delay(DELAY_MS);
}
{% endhighlight C %}

Контролираме стъпката на избледняване — *количеството*, което се избледнява при всяка итерация на `loop()` — с `const int FADE_STEP`. С `FADE_STEP=1` избледняваме между 768 цветови комбинации (`3*256`). По подразбиране `FADE_STEP=5`, което води до 156 цветови комбинации.

#### Пълен код на RGB-базиран кросфейдър

Ето кода в неговата цялост:

<!-- gist-it не работи, затова сега използвам emgithub -->
<!-- <script src="https://gist-it.appspot.com/https://github.com/makeabilitylab/arduino/blob/master/Basics/analogWrite/CrossFadeRGB/CrossFadeRGB.ino?footer=minimal"></script> -->

<script src="https://emgithub.com/embed.js?target=https%3A%2F%2Fgithub.com%2Fmakeabilitylab%2Farduino%2Fblob%2Fmaster%2FBasics%2FanalogWrite%2FCrossFadeRGB%2FCrossFadeRGB.ino&style=github&showCopy=on"></script>

Този [изходен код](https://github.com/makeabilitylab/arduino/blob/master/Basics/analogWrite/CrossFadeRGB/CrossFadeRGB.ino) се намира в GitHub.
{: .fs-1 }

#### Видеоклипове с RGB-базиран кросфейдър

Ето два видеоклипа, показващи кода, изпълняван на Arduino Uno. Първо, в симулатора Tinkercad. Можете да видите цветовете на кросфейда и графиката на съответните стойности на `analogWrite`.

<iframe width="736" height="414" src="https://www.youtube.com/embed/ZyfHRQFwmeg" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

Второ, видео от работен плот на кода, изпълняван на Arduino Uno:

<iframe width="736" height="414" src="https://www.youtube.com/embed/zL7xIWHqVaY" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

<!--TODO: да се добави p5js, който демонстрира как работи това? И може би да позволим на читателя да си играе с различни цветови стойности? -->

### Кръстосано преливане в цветовото пространство HSL

Вторият метод за преливане на RGB LED използва [Hue, Saturation, Lightness (HSL)](https://en.wikipedia.org/wiki/HSL_and_HSV) цветовото пространство. За да променим "цвета" на RGB LED, всъщност говорим за промяна на неговия **цветови тон**. Много по-лесно е да направим това, като използваме HSL и след това конвертираме в RGB, за да зададем цвета на RGB LED.
 

![Цветови пространства RGB и HSL](assets/images/RGBVsHSLColorSpace_Wikipedia.png)
Визуализации на цветовите пространства RGB и HSL от [Wikipedia](https://en.wikipedia.org/wiki/HSL_and_HSV).
{: .fs-1 }

Ето видео с различни оттенъци, наситеност и нива на светлина, използвайки HSL Color Picker на Hunor Marton. Опитайте го сами на [codepen.io](https://codepen.io/HunorMarton/pen/dvXVvQ/). Можете също да отворите почти всяка програма за рисуване или графики, за да си поиграете и да превключвате между цветовите пространства от MSPaint до Adobe Photoshop и Illustrator до [GIMP](https://www.gimp.org/) и [Inkscape](https://inkscape.org/).

<iframe width="736" height="414" src="https://www.youtube.com/embed/a0j8qyBJE2E" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
Запис на екрана на [HSL Color Picker на Hunor Marton](https://codepen.io/HunorMarton/pen/dvXVvQ/).
{: .fs-1 }

В нашия случай извършваме това преобразуване от HSL в RGB, като използваме библиотеката [RGBConverter](https://github.com/ratkins/RGBConverter). С този HSL подход нашият код е сравнително много по-опростен, нещо като следния псевдокод:

{% highlight C %}
// Основен преглед на нашия подход (псевдокод)
float hue = 0, saturation = 0.8, lightness = 1.0;
float hueStepValue = 0.1f; // увеличаване на оттенъка, но запазване на наситеността и светлостта
float MAX_HUE = 1.0f;
loop(){
    hue += stepValue; // увеличаване на оттенъка
    RGB rgb = convertHslToRgb(hue, saturation, lightness) // преобразуване на HSL в RGB
    setColor(rgb.red, rgb.green, rgb.blue); // задаване на цвета
    if(hue > MAX_HUE){ // нулиране на оттенъка, ако е достигнат MAX_HUE
        hue = 0;
    }
}
{% endhighlight C %}

Недостатъкът на тази реализация е, че трябва да използваме [`floats`](https://www.arduino.cc/en/pmwiki.php?n=Reference/Float), защото библиотеката [RGBConverter](https://github.com/ratkins/RGBConverter) използва функции с плаваща запетая. Защо floats са лоши? Две причини: с микроконтролера ATmega328 аритметиката с плаваща запетая е **бавна** (делителното действие с `float` може да бъде 2-4 пъти по-бавно от делителното действие с `integer`) и **[неточна](https://www.arduino.cc/en/pmwiki.php?n=Reference/Float)** (floats могат да изглеждат безкрайно точни, като се има предвид използването на десетични знаци, но при ATmega328 плаващите числа имат ~6-7 десетични знака точност).

Въпреки това, тези ограничения няма да имат значение за нашата програма – или за някой от нашите въвеждащи уроци – защото не сме ограничени от скоростта и не се нуждаем от математика с висока точност. Ако искате да знаете повече за *защо* вградените програмисти се опитват да избягват операции с плаваща запетая, прочетете бележката по-долу. В противен случай, прескочете напред.

---
**БЕЛЕЖКА:**

Чипът ATmega328 (използван от Arduino Uno, Leonardo и др.) не поддържа по подразбиране плаваща запетая (т.е. няма специализиран хардуер за ускоряване на тези операции с плаваща запетая). Това е често срещано ограничение при микроконтролерите. За да избегнат използването на плаващи точки, докато все пак изчисляват същите математически операции, вградените програмисти използват [аритметика с фиксирана запетая](https://en.wikipedia.org/wiki/Fixed-point_arithmetic).

Някои интересни дискусии и примери включват:
- [Изглаждане на сензора и оптимизирана математика на Arduino](http://bleaklow.com/2012/06/20/sensor_smoothing_and_optimised_maths_on_the_arduino.html), блогът на Алън Бърлисън
- [Сравнение между фиксирана и плаваща запетая в AVR GCC](https://ucexperiment.wordpress.com/2015/03/31/avr-gcc-fixed-point-vs-floating-point-comparison/), блог на ucexperiment
- [Скорост на операциите с плаваща запетая](https://forum.arduino.cc/index.php?topic=40901.0), форуми на Arduino.

<!-- TODO: разширение на темата защо плаващите точки могат да бъдат скъпи за вградено програмиране с микроконтролери? -->
---

#### Пълен код на кросфейдър на базата на HSL

Пълният код за нашия кросфейдър на базата на HSL е по-долу. **Важно** е да знаете, че не можете просто да копирате/поставите този код в Arduino IDE. Трябва да имате кода RGBConverter в подпапка, наречена `src`, в основната директория на скицата. Използвайте същата директория като нашата [GitHub](https://github.com/makeabilitylab/arduino/tree/master/Basics/analogWrite/CrossFadeHue). Можете да прочетете повече за зареждането на библиотеки в Arduino IDE по-долу.

<!-- gist-it не работи, затова сега използвам emgithub -->
<!-- <script src="https://gist-it.appspot.com/https://github.com/makeabilitylab/arduino/blob/master/Basics/analogWrite/CrossFadeHue/CrossFadeHue.ino?footer=minimal"></script> -->

<script src="https://emgithub.com/embed.js?target=https%3A%2F%2Fgithub.com%2Fmakeabilitylab%2Farduino%2Fblob% 2Fmaster%2FBasics%2FanalogWrite%2FCrossFadeHue%2FCrossFadeHue.ino&style=github&showCopy=on"></script>

Този [изходен код](https://github.com/makeabilitylab/arduino/blob/master/Basics/analogWrite/CrossFadeHue/CrossFadeHue.ino) се намира в GitHub.
{: .fs-1 }

#### Видео от работната маса

Ето видео от работната маса на [CrossFadeHue.ino](https://github.com/makeabilitylab/arduino/tree/master/Basics/analogWrite/CrossFadeHue) с RGB LED с общ катод.

<iframe width="736" height="414" src="https://www.youtube.com/embed/ROfJge7bsfI" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

<!-- TODO потърси минималната стойност на стъпката, която има смисъл с нашата квантизация -->

<!-- TODO: Би било забавно да се напише p5js скица, която показва как работи първоначалният наивен код на RGB LED и след това HSL версията -->

### Зареждане на библиотеки в Arduino IDE

Има няколко начина за зареждане на външни библиотеки в Arduino IDE (вижте този [официален Arduino урок](https://www.arduino.cc/en/guide/libraries)); обаче, повечето са фокусирани върху **глобални библиотеки**—тоест, библиотеки, до които имат достъп **всички** ваши скици. Ами ако искате да заредите само локална библиотека само за текущата скица?

Оказва се, че тази фундаментална функция има дълга и мрачна история в общността на Arduino (например: [линк](https://stackoverflow.com/questions/4705790/keeping-all-libraries-in-the-arduino-sketch-directory), [линк](https://arduino.stackexchange.com/questions/8651/loading-local-libraries)). Намерих три начина за зареждане на **локален** `.h` и `.cpp` код:

**Първият** и най-лесен начин е да поставите всички `.h` и `.cpp` файлове в основната папка с скици (където се намира вашият `.ino` файл):

```
CrossFadeHue
|-CrossFadeHue.ino
|-RGBConverter.cpp
|-RGBConverter.h
```

**Втори**, поставете всички `.h` и `.cpp` файлове в подпапка на вашата основна папка с име по ваш избор (*например* `lib`):

```
CrossFadeHue
|-CrossFadeHue.ino
|-lib
|-RGBConverter.cpp
|-RGBConverter.h
```

**Трето**, ако имате много `.h` и `.cpp` файлове и искате да ги организирате в отделни подпапки, тогава... това може да бъде разочароващо! Но има решение от версия ~Arduino 1.6: трябва да поставите тези подпапки в подпапка, наречена `src` ([link](https://github.com/arduino/Arduino/issues/4936#issuecomment-312953260)) в основната папка с скици. Всъщност, това е точно нашата настройка за използване на библиотеката [RGBConverter](https://github.com/ratkins/RGBConverter). Тя се намира в `CrossFadeHue\src\RGBConverter`. Така че вашата директория трябва да изглежда по следния начин:

```
CrossFadeHue
|-CrossFadeHue.ino
|-src
|-RGBConverter
|-RGBConverter.cpp
|-RGBConverter.h
```
---

## Упражнения

- **Нови алгоритми за преливане**. Разработете свой собствен алгоритъм за преливане между цветовете. Експериментирайте с оттенък, наситеност и светлина. Как изглежда, че те влияят на RGB LED?
- **Избледняване на няколко RGB LED-а**. Как можем да модифицираме кода си, за да избледняваме няколко RGB LED-а с различна скорост? **Подсказка:** Ще работим върху едно възможно решение в [следващия урок](led-blink3.md)

## Следващ урок

В следващия и последен [урок "Въведение в изхода"](intro-output. md) ще научим как да мигаме няколко LED с различна честота, което е един от най-често задаваните въпроси във форумите на Arduino — вероятно поради начина, по който [официалният урок на Arduino Blink](https://www.arduino.cc/en/tutorial/blink) използва `delay()` за контрол на скоростта на мигане (което е подходящо за един LED, но не се мащабира). Преди да започнете урока, си струва да помислите как *вие* бихте мигали с няколко честоти при различни скорости. :)

<span class="fs-6">
[Предишна: RGB светодиоди](rgb-led.md){: .btn .btn-outline }
[Следваща: Мигане на няколко светодиода с различна честота](led-blink3.md){: .btn .btn-outline }
</span>
