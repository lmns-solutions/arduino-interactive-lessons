---
lang: bg
permalink: /advancedio/oled.html
page_id: advancedio-oled
layout: default
title: L1&#58; OLED дисплеи
nav_order: 1
parent: Изход
grand_parent: Разширени входно-изходни устройства
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

<!-- ## Серийни комуникационни протоколи

TODO: въведение i2c и SPI.
- Може ли Leonardo да използва i2c пин объркване на студентите: https://forum.arduino.cc/t/can-leonardo-actually-use-its-i2c-pins/417516

### Терминология

Master/slave

### i2C

- С 7-битово адресиране, 112 устройства. С 10-битово адресиране, 1008 устройства
- Всяко устройство има уникален идентификационен номер
- Необходими са пул-ъп резистори (важно е, че разклонителните платки, които използваме в клас, **вече** имат тези пул-ъп резистори вградени в печатните платки) 

- Свържете няколко устройства едновременно с верижно свързване. Връзка към видео за цветния сензор

Завърши: в бъдеще сравнете i2c и SPI. Смятам, че SPI е по-бърз

- -->

<video autoplay loop muted playsinline style="margin:0px">
<source src="assets/videos/OLED_Pong720p.mp4" type="video/mp4" />
</video>
**Видео.** Игра на Pong на монохромен 1,3-инчов 128x64 пиксела [OLED дисплей](https://www.adafruit.com/product/938) на Adafruit с [2-осов джойстик Parallax](https://www.adafruit.com/product/245) и тактилни бутони. Изходният код за Pong е [тук](https://github.com/makeabilitylab/arduino/blob/master/OLED/Pong/Pong.ino). Части от това видео са ускорени 4 пъти.
{: .fs-1 }

В този урок ще научите за дисплеите с органични светодиоди (OLED), основното програмиране на графики и кратко въведение в два протокола за серийна комуникация, наречени [I<sup>2</sup>C](https://en.wikipedia.org/wiki/I%C2%B2C) (Inter-Integrated Circuit) и [SPI](https://en.wikipedia.org/wiki/Serial_Peripheral_Interface) (Serial Peripheral Interface)

## OLED дисплеи

Дисплеите с органични светодиоди ([OLED](https://en.wikipedia.org/wiki/OLED)) са сравнително нова технология, която все по-често се използва в телевизори, компютърни монитори, смартфони и преносими игрови конзоли. За разлика от LCD дисплеите, които изискват задно осветяване, всеки OLED пиксел генерира собствена светлина, осигурявайки превъзходен контраст и контрол на цветовете.

В този урок ще използваме [монохромни (черно-бели) OLED дисплеи](https://learn.adafruit.com/monochrome-oled-breakouts) от Adafruit, заедно с техните библиотеки за управление на дисплея и графики. За да направим това, трябва да инсталираме някои [библиотеки](oled-libraries.md).

<!-- TODO: добавете примери за местата, където се използват OLED дисплеи. Като Fitbit Charge: https://www.microcontrollertips.com/inside-fitbit-charge/ -->

### Инсталиране на Arduino библиотеки

За да използваме Adafruit OLED дисплея, се нуждаем от две библиотеки:

- Библиотеката [Adafruit_SSD1306] (https://github.com/adafruit/Adafruit_SSD1306) библиотека за драйвери на дисплеи, която се занимава с комуникацията на дисплея, картографирането на паметта и нисконивовите рутинни операции по рисуване
- Графичната библиотека [Adafruit_GFX](https://github.com/adafruit/Adafruit-GFX-Library), която предоставя основни графични рутинни операции за всички дисплеи на Adafruit, като рисуване на точки, линии, кръгове.
 

За щастие, Arduino IDE улеснява инсталирането на библиотеки. Можем да го направим директно от IDE. Следвайте нашето стъпка по стъпка [ръководство за инсталиране тук](oled-libraries.md).

### Свързване на дисплея Adafruit OLED

След като инсталирате необходимите библиотеки, сте готови да свържете дисплея!

Чипът [SSD1306] (https://github.com/adafruit/Adafruit_SSD1306) и придружаващата го библиотека предоставят два различни метода за комуникация, всеки от които изисква различно свързване: [I<sup>2</sup>C](https://en.wikipedia.org/wiki/I%C2%B2C) (Inter-Integrated Circuit) и [SPI](https://en.wikipedia.org/ wiki/Serial_Peripheral_Interface) (Serial Peripheral Interface). По подразбиране се използва I2C, който ще използваме в този урок. За повече информация за SPI режима вижте [официалните документи на Adafruit](https://learn.adafruit.com/monochrome-oled-breakouts/wiring-128x64-oleds).

Докато OLED дисплеят изисква 3,3 V захранване и 3,3 V логически нива за комуникация, разклонителната платка на Adafruit включва 3,3 V регулатор и ниво на превключване на всички пинове, така че можете да се свържете с 3 V или 5 V устройства. Освен това, не забравяйте, че I<sup>2</sup>C изисква пул-ъп резистори на линиите на часовника (SCL) и линиите за данни (SDA), така че и двете да бъдат изтеглени до логическо ниво "HIGH" по подразбиране. За щастие, разклонителната платка Adafruit също включва тези резистори. Така че окабеляването е доста просто и се състои само от четири кабела!

Схемата на окабеляването и електрическата схема са показани по-долу. Използвахме системата за цветово кодиране [Qwiic](https://www.sparkfun.com/qwiic) за нашите кабели: синьо за данни (SDA), жълто за часовник (SCL), черно за заземяване (GND) и червено за захранване (5V). I<sup>2</sup>C пиновете се различават в зависимост от вашата платка. Например, на Arduino Uno те са A4 (SDA) и A5 (SCL), а не цифрови пинове 2 (SDA) и 3 (SCL), както е на Leonardo.

![](assets/images/ArduinoLeonardo_OLEDWiring_FritzingSchematics.png)
**Фигура** За свързването на OLED дисплея Adafruit са необходими само четири кабела (и нищо друго). Използвах стандартното цветово кодиране STEMMA QT за кабелите си: синьо за данни (SDA), жълто за часовник (SCL), черно за заземяване (GND) и червено за захранване (5V). Имайте предвид, че I<sup>2</sup>C пиновете се различават в зависимост от вашата платка. Например, на Arduino Uno те са A4 (SDA) и A5 (SCL), а не цифрови пинове 2 (SDA) и 3 (SCL), както е при Leonardo.
{: .fs-1 }

#### Физическо свързване с кабели за превключване

Ето снимка на действителното свързване на OLED с кабели за превключване.

![](assets/images/ArduinoLeonardo_OLEDWiring_Breadboard.png)
** Фигура** Физическо свързване на OLED дисплея с преходни кабели. Arduino изпълнява този демо код ["BitmapBounce.ino"](https://github.com/makeabilitylab/arduino/blob/master/OLED/BitmapBounce/BitmapBounce.ino)
{: .fs-1 }

#### Свързване на ESP32

Някои студенти попитаха за окабеляването на ESP32, така че ето го. Платката ESP32 работи при 3,3 V *в сравнение с* 5V, доставяни от Arduino Leonardo и Uno; обаче, OLED самото се нуждае само от 3V за работа. Можете да научите повече за [ESP32 тук](../esp32/index.md).

![](assets/images/Huzzah32_OLEDWiring_FritzingSchematics.png)
**Фигура. ** Схема на окабеляването за [Adafruit Huzzah32](../esp32/index.md) ESP32 платка с OLED.
{: .fs-1 }

#### STEMMA QT окабеляване

От ~2017 г. много от платките Adafruit и SparkFun започнаха да включват стандартизирани конектори, за да се улесни свързването на множество електронни устройства без запояване или работа с много отделни кабели. Това е особено полезно, защото I<sup>2</sup>C ни позволява да свързваме последователно I<sup>2</sup>C-съвместими устройства. Стандартът за свързване Sparkfun за I<sup>2</ sup>C устройства, наречен [Qwicc](https://www.sparkfun.com/qwiic), по-късно беше приет от Adafruit, които го наричат [STEMMA QT](https://learn.adafruit.com/introducing-adafruit-stemma-qt/what-is-stemma-qt) .

Както [Sparkfun](https://www.sparkfun.com/categories/tags/qwiic-cables), така и Adafruit продават разнообразие от Qwiic/STEMMA QT кабели, включително тази [женска-към-женска](https://www.adafruit.com/ product/4210) версия (за ~0,95 $) и този [женски към мъжки](https://www.adafruit.com/product/4209) джъмпер кабел (0,95 $). Можете да използвате женски към женски кабел, за да свържете няколко устройства в верига.

| STEMMA QT / Qwiic женски към женски кабел | STEMMA QT / Qwiic женски към мъжки скачащ кабел |
|:------------------------------------:|:--------------------------------:|
| ![](assets/images/Adafruit_STEMMA-QT_FemaleToFemale.png) | ! [](assets/images/Adafruit_STEMMA-QT_FemaleToMale_Cable.png) |

Видеото по-долу показва OLED дисплея, свързан към STEMMA QT [кабел с женски към мъжки конектор] (https://www.adafruit.com/product/4209):

<video autoplay loop muted playsinline style="margin:0px">
<source src="assets/videos/AdafruitSTEMMAQT_IMG_6163-TrimmedAndCropped720p.mov" type="video/mp4" />
</video>
**Видео** Изпълнение на демото [`ssd1306_128x64_i2c`](https://github.com/adafruit/ Adafruit_SSD1306/blob/master/examples/ssd1306_128x64_i2c/ssd1306_128x64_i2c.ino) с кабел STEMMA QT.
{: .fs-1 }

### Тестване на OLED дисплея

След като сте свързали OLED дисплея, сме готови да го тестваме с малко код!

Ще изпълним един от примерите, който се доставя с библиотеката [Adafruit_SSD1306](https://github.com/adafruit/Adafruit_SSD1306), наречен [`ssd1306_128x64_i2c`](https:// github.com/adafruit/Adafruit_SSD1306/blob/master/examples/ssd1306_128x64_i2c/ ssd1306_128x64_i2c.ino). Този пример преминава през различни демонстрации на рисуване, включително: рисуване на линии, очертаване и запълване на правоъгълници, кръгове, заоблени правоъгълници и триъгълници, рендиране на текст с различни стилове, както и рисуване и анимиране на битови карти. Можете да видите примера [изходния код тук](https://github.com/adafruit/Adafruit_SSD1306/blob/master/examples/ssd1306_128x64_i2c/ssd1306_128x64_i2c.ino).

За да отворите и стартирате примера, следвайте тези стъпки.

#### Стъпка 1: Отворете примера

В Arduino IDE отидете на `File -> Examples -> Adafruit SSD1306` и изберете `ssd1306_128x64_i2c`. Може да се наложи да превъртите надолу в менюто `Examples`, за да го видите.

![](assets/images/ArduinoIDE_SelectingSSD1306ExampleFromFileMenu.png)

#### Стъпка 2: Компилирайте и качите примера

Сега компилирайте и качите примера.

![](assets/images/ArduinoIDE_CompileAndUploadSSD1306Example.png)

#### Стъпка 3: Гледайте демото

След като кодът е компилиран и качен, той трябва да изглежда по следния начин:

<video autoplay loop muted playsinline style="margin:0px">
<source src="assets/videos/AdafruitOLEDOfficialDemo0x3D-IMG_6160-Rotated-TrimmedAndSpedUp720p-Optimized.mp4" type="video/mp4" />
</video>
** Видео** Изпълнение на демото [`ssd1306_128x64_i2c`](https://github.com/adafruit/Adafruit_SSD1306/blob/master/examples/ssd1306_128x64_i2c/ssd1306_128x64_i2c.ino) . Части от това видео са ускорени 4 пъти.
{: .fs-1 }

Ако сте любопитни как са направили рендеринга, моля, разгледайте [изходния код](https://github.com/adafruit/Adafruit_SSD1306/blob/master/examples/ssd1306_128x64_i2c/ssd1306_128x64_i2c.ino). Няма нищо магично тук и четенето на кода може да ви помогне при създаването на бъдещи прототипи!

## Библиотеката Adafruit GFX

Сега, след като сме свързали правилно OLED дисплея и сме проверили, че работи, нека поговорим за **как** да рисуваме на екрана.

За да предостави общ API за рисуване на всички LCD и OLED дисплеи на Adafruit, Adafruit създаде библиотека за графично рендиране с общо предназначение, наречена [Adafruit GFX] (https://learn.adafruit.com/adafruit-gfx-graphics-library/overview). Просто казано, вместо да се налага да включвате/изключвате индивидуално OLED дисплеите в OLED матрицата – което би било досадно (макар и може би полезно упражнение за учене) – библиотеката Adafruit GFX предоставя рутинни процедури за рисуване на по-високо ниво, които правят това за вас, като например рисуване на правоъгълници, кръгове, текст и битови карти.

{: .note }
Въпреки че ги препоръчваме горещо, вие със сигурност не *трябва* да използвате библиотеките Adafruit [SSD1306](https://github.com/adafruit/Adafruit_SSD1306) и [GFX](https:/ /github.com/adafruit/Adafruit-GFX-Library) за използване на OLED дисплеи. Има много онлайн уроци, които описват как да се свържете директно с SSD1306 OLED драйвера и да създадете рутинни процедури за рисуване. Например, това "[Първи стъпки с OLED дисплеи](https://www.instructables.com/Getting-Started-With-OLED-Displays/)" от JayconSystems в Instructables. Не забравяйте, инженерите на Adafruit просто са създали своите библиотеки, за да улеснят програмирането на OLED дисплеите... и ние им сме благодарни! Но можете също да следвате спецификациите на [SSD1306](https://cdn-shop.adafruit.com/datasheets/SSD1306.pdf) и I<sup>2</sup>C и да създадете свои собствени библиотеки!

### Координатна система и пиксели

Ако сте запознати с графичните API в други програмни рамки – като [библиотеката System.Drawing на C#](https://docs.microsoft.com/en-us/dotnet/api/system.drawing.graphics.drawline), [библиотеката за рисуване на Processing в Java](https://processing.org/), [библиотеката за рисуване на p5js в JavaScript](https://p5js.org/) и др., библиотеката Adafruit GFX работи по същия начин (на високо ниво).

Черно-бялата OLED се състои от матрица от OLEDS, наречени пиксели, които могат да се адресират индивидуално, за да се включват/изключват (или, в случая на цветни дисплеи, да се контролират индивидуални RGB OLED, за да се създават цветове). Както при всички други библиотеки за рисуване, координатната система за тези пиксели поставя началната точка `(0,0)` в горния ляв ъгъл, като `x-осът` се увеличава надясно, а `y-осът` се увеличава надолу.

![](assets/images/AdafruitOLEDDisplay_CoordinateSystemAndPixels_ByJonFroehlich.png)
**Фигура** Общ преглед на 128x64 матрицата от светодиоди – всеки светодиод наричаме "пиксел". Забелязали сме, че понякога учениците обръщат ос Y в съзнанието си. Затова обърнете внимание, че началната точка е `(0,0)`, а `ос X` се увеличава надясно, а `ос Y` се увеличава надолу. Изображението е създадено в PowerPoint и използва изображения от Fritzing и урокът [Adafruit GFX](https://learn.adafruit.com/adafruit-gfx-graphics-library/coordinate-system-and-units).
{: .fs-1 }

Следователно, за да включите LED на пиксел `(18, 6)`, използвайки [Adafruit GFX](https://learn.adafruit.com/adafruit-gfx-graphics-library/overview), бихме написали: `drawPixel(18, 6, SSD1306_WHITE)`. За черно-бели дисплеи последният аргумент може да бъде или `SSD1306_WHITE`, за да се нарисува бял пиксел, или `SSD1306_BLACK`, за да се нарисува черен пиксел (тези параметри са дефинирани в [Adafruit_SSD1306.h](https: //github.com/adafruit/Adafruit_SSD1306/blob/master/Adafruit_SSD1306.h)). За цветни дисплеи можете вместо това да предавате 16-битова стойност без знак, представляваща RGB цветове (вижте [docs](https://learn.adafruit.com/adafruit-gfx-graphics-library/coordinate-system-and-units)).

## Подсистема за рисуване

По-долу описваме как да рисувате фигури, текст и битови карти. Важно е да знаете, че когато извиквате някоя от рутините за рисуване – от `drawLine` до `drawTriangle` – вие **не** рисувате директно върху OLED дисплея. Вместо това рисувате върху буфер извън екрана, управляван от драйвера SSD1306. След като извикате рутините за рисуване, трябва да извикате функцията `void Adafruit_SSD1306:: display()`, за да прехвърлите данните от RAM към дисплея. Ще покажем как да направите това стъпка по стъпка в примерите по-долу.

![](assets/images/OLEDDisplay_DrawingCircleAt5020With10Radius.png)
**Фигура.** Нека започнем с рисуването на прост кръг в точката `x,y` с координати `50,20` и радиус `10`. Този код също е в GitHub като [DrawCircle.ino](https://github.com/makeabilitylab/arduino/blob/master/OLED/DrawCircle/DrawCircle.ino)); обаче, този код е малко по-различен, тъй като центрира кръга в средата на екрана. 
{: .fs-1 }

Нека започнем с изчертаване на кръг в точка `x,y` с координати `50,20` и радиус `10`. Първо ще започнем с псевдокод, за да разберем процеса на изчертаване, а след това ще преминем към действителния C++.

```
// Еднократна инициализация
Adafruit_SSD1306 _disp = new Display(); // Създаване на нов SSD1306 дисплей обект
_disp.begin(SSD1306_SWITCHCAPVCC, 0x3D); // Разпределяне на RAM за буфер на изображението, настройка на VCC и адрес

// Рисуване
_disp.clearDisplay(); // Задаване на всички пиксели на изключено
_disp.fillCircle(50, 20, 10, SSD1306_WHITE); // Рисуване в буфера извън екрана
_disp.display(); // Рендиране на буфера извън екрана за показване
```

А ето и действителната C++ имплементация (пълният код е в GitHub като [DrawCircle.ino](https://github.com/makeabilitylab/arduino/blob/master/OLED/DrawCircle/DrawCircle.ino)).

{% highlight C++ %}
// Инстанцииране на SSD1306 драйвер дисплей обект
Adafruit_SSD1306 _display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);

void setup(){
    Serial.begin(9600);

    // Инициализиране на дисплея с begin () 
    // Първият параметър е изборът на VCC. Обикновено се предава SSD1306_SWITCHCAPVCC.
    // Вторият е адресът на дисплея за i2c. Дори ако дисплеят е конфигуриран
    // за SPI (който не използва адреси), все пак трябва да предадете параметър тук (може да бъде 0)
    if (!_display.begin(SSD1306_SWITCHCAPVCC, 0x3D)) { // Адрес 0x3D за 128x64
        Serial.println(F("SSD1306 allocation failed"));
        for (;;); // Не продължавайте, цикъл завинаги
    }
}

void loop(){
    // Изчистете дисплея
    _display.clearDisplay();

    // Поставете рутинни процедури за рисуване
    // В този случай нарисувайте кръг в точка x,y с координати 50,20 и радиус 10
    _display.fillCircle(50, 20, 10, SSD1306_WHITE);

    // Рендирайте графичния буфер на екрана
    _display.display();
}
{% endhighlight C++ %}

Сега, тъй като рисуваме едно и също нещо при всяко извикване на `loop()`, можем просто да поставим този код за рисуване в `setup()` и да го нарисуваме веднъж и само веднъж (графичното съдържание ще се запази).

{% highlight C++ %}
// Инстанцииране на обект за дисплей на драйвера SSD1306
Adafruit_SSD1306 _display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);

void setup(){
    Serial.begin(9600);

    // Инициализирайте дисплея. Ако се провали, отпечатайте грешката в Serial
    // и влезте в безкраен цикъл
    if (!_display.begin(SSD1306_SWITCHCAPVCC, 0x3D)) { // Адрес 0x3D за 128x64
        Serial.println(F("SSD1306 allocation failed"));
        for (;;); // Не продължавайте, цикъл завинаги
    }

    // Изчистете дисплея
    _display.clearDisplay();

    // Нарисувайте кръг в точка x,y с координати 50,20 и радиус 10
    _display.fillCircle (50, 20, 10, SSD1306_WHITE);

    // Рендиране на графичния буфер на екрана
    _display.display();
}

void loop(){
    // Умишлено празен, за да се подчертае как графичното съдържание остава
    // на екрана
}
{% endhighlight C++ %}

Въпреки това, от практическа гледна точка, винаги искаме да поставяме нашите методи за рисуване в `loop()`, защото искаме да поддържаме **динамична графика**, която е анимирана (*например* графика, която се променя с времето) и/или отзивчива (*например* графика, която се променя в отговор на въвеждане).

{: .highlight }
> **Важно напомняне**
>
> Трябва да извикате `_display.display()`, за да рендерите графичния буфер на екрана. Не е достатъчно просто да извикате `drawCircle`, `fillRect`, `drawBitmap`, тъй като тези функции "рисуват" в буфер извън екрана. Всъщност, ако погледнете [изходния код Adafruit_SSD1306.cpp](https://github.com/adafruit/Adafruit_SSD1306/blob/ 1d52453e3b722e4c7a7bc6b81128138d721b5c27/Adafruit_SSD1306.cpp#L992) (достъпен онлайн в GitHub), ще видите, че функцията [`void Adafruit_SSD1306::display (void)`](https://github.com/adafruit/Adafruit_SSD1306/blob/1d52453e3b722e4c7a7bc6b81128138d721b5c27/Adafruit_SSD1306.cpp#L992) "прехвърля данните, които в момента се намират в RAM паметта, към дисплея SSD1306".

### Рисуване на фигури

Библиотеката Adafruit GFX понастоящем поддържа рисуване на линии, правоъгълници, кръгове, заоблени правоъгълници и триъгълници. За всички фигури можете да нарисувате контурна версия (*например* `drawRect`) или запълнена версия (*например* `fillRect`). Изображенията по-долу са взети от [урока по Adafruit GFX](https://learn.adafruit.com/adafruit-gfx-graphics-library/graphics-primitives).

| Фигура и API извикване | Резултат |
|-------|:--------:|
|**Линии**<br> `void drawLine(uint16_t x0, uint16_t y0, uint16_t x1, uint16_t y1, uint16_t color); ` | ![](https://cdn-learn.adafruit.com/assets/assets/000/001/268/large1024/lcds___displays_line.png) `drawLine(5, 10, 3, 19, SSD1306_WHITE)` |
|**Правоъгълници**<br> `void drawRect(uint16_t x0, uint16_t y0, uint16_t w, uint16_t h, uint16_t color); ` <br><br> `void fillRect(uint16_t x0, uint16_t y0, uint16_t w, uint16_t h, uint16_t color); ` | ![](https://cdn-learn.adafruit.com/assets/assets/000/001/270/large1024/lcds___displays_rect.png) `drawRect(3, 2, 13, 10, SSD1306_WHITE)` |
|**Кръгове**<br> `void drawCircle(uint16_t x0, uint16_t y0, uint16_t r, uint16_t color);` <br><br> `void fillCircle(uint16_t x0, uint16_t y0, uint16_t r, uint16_t color); ` | ![](https://cdn-learn.adafruit.com/assets/assets/000/001/272/large1024/lcds___displays_circle.png) `drawCircle(14, 8, 7, SSD1306_WHITE)` |
|**Заоблени правоъгълници**<br> `void drawRoundRect(uint16_t x0, uint16_t y0, uint16_t w, uint16_t h, uint16_t radius, uint16_t color);` <br><br> `void fillRoundRect(uint16_t x0, uint16_t y0, uint16_t w, uint16_t h, uint16_t radius, uint16_t color);` | ![](https://cdn-learn.adafruit.com/assets/assets/000/001/274/large1024/lcds___displays_roundrect.png) `drawRoundRect(3, 1, 17, 12, 5, SSD1306_WHITE)` |
|**Триъгълници**<br> `void drawTriangle(uint16_t x0, uint16_t y0, uint16_t x1, uint16_t y1, uint16_t x2, uint16_t y2, uint16_t color); ` <br><br> `void fillTriangle(uint16_t x0, uint16_t y0, uint16_t x1, uint16_t y1, uint16_t x2, uint16_t y2, uint16_t color);` | ![](https://cdn -learn.adafruit.com/assets/assets/000/001/275/large1024/lcds___displays_triangle.png) `drawTriangle(6, 13, 9, 2, 18, 9, SSD1306_WHITE)` |

#### Рисуване на потребителски форми

Разбира се, можете да създавате потребителски форми, като комбинирате умело основни форми (*например* правоъгълник и триъгълник, за да направите основна къща) или като имплементирате свой собствен алгоритъм за рисуване и извикате `drawPixel`. API-то `drawPixel` изглежда така:

| Форма и API извикване | Изход |
| -------|:--------:| 
|**Пиксели**<br> `void drawPixel(uint16_t x, uint16_t y, uint16_t color);` | ![](https://cdn-learn.adafruit.com/assets/assets/000/001/264/medium800/ lcds___displays_coordsys.png?1396770439) `drawPixel(0, 0, SSD1306_WHITE)` <br> `drawPixel(18, 6, SSD1306_WHITE)` <br> `drawPixel(6, 13, SSD1306_WHITE)` |

#### Оптимизиран оптимизирано рисуване на вертикални и хоризонтални линии

Ако рисувате чисто вертикални или хоризонтални линии, можете да използвате оптимизирани функции за рисуване на линии, които избягват ъглови изчисления. Например, ние използваме `drawFastVLine` в нашите [демонстрации за аналогови графики](#demo-3-basic-real-time-analog-graph) по-долу.

За повече информация и примери вижте [раздела "Основно рисуване"](https://lastminuteengineers.com/oled-display-arduino-tutorial/# arduino-code-basic-drawings) на урока за OLED дисплей на Last Minute Engineer.

### Рисуване на текст

Има два метода за рендиране на текст: рисуване на единичен символ с `drawChar` и използване на подсистемата за рендиране `print`, която имитира познатата [`Serial.print()`](https://www.arduino.cc/reference/ en/language/functions/communication/serial/print/) функционалност, описана в нашата серия "Въведение в Arduino" [тук](../arduino/serial-print.md).

#### Метод 1: drawChar

За да нарисувате един символ, трябва да зададете местоположението `(x, y)`, символа, цвета на предния план и фона, както и размера. По подразбиране символите са с размер 5x8 пиксела, но може да се предаде опционален параметър за размер (последният аргумент), за да се мащабира шрифтът (*например* размер 2 ще рендерира 10x16 пиксела на символ).

| Извикване на Text API | Изход |
|-------|:--------:|
|**Char**<br> `void drawChar(uint16_t x, uint16_t y, char c, uint16_t color, uint16_t bg, uint8_t size);` | ! [](https://cdn-learn.adafruit.com/assets/assets/000/001/276/large1024/lcds___displays_char.png) `drawChar(3, 4, "A", SSD1306_WHITE, SSD1306_BLACK, 1)` |

#### Метод 2: Отпечатване

По-разпространеният и богат на функции метод за рисуване на текст е чрез подсистемата `print`. Интересното е, че класът [Adafruit_GFX](https://github.com/adafruit/ Adafruit-GFX-Library/blob/master/Adafruit_GFX.h) всъщност разширява [класа Print](https://github.com/arduino/ArduinoCore-avr/blob/master/cores/arduino/Print.h) от основната библиотека на Arduino. Можете да видите документацията за `Serial.print()` [тук](https://www.arduino.cc/reference/en/language/functions/communication/serial/print/); API е същото за OLED.

Вместо да извикате `Serial.print("Hello World")`, с OLED дисплея и библиотеката Adafruit GFX, бихте извикали `_display.print("Hello World")`. Тук `_display` е обектът `Adafruit_SSD1306`.

За да използвате функцията за печат на OLED, първо можете да зададете опционални параметри като цвят на текста, размер и пренос:

{% highlight C++ %}
void setTextColor(uint16_t color);
void setTextColor(uint16_t color, uint16_t backgroundcolor);
void setTextSize(uint8_t size);
void setTextWrap(boolean w);
{% endhighlight C++ %}

След това, за да позиционирате текста, задайте курсора за печат с:
{% highlight C++ %}
void setCursor(uint16_t x0, uint16_t y0);
{% endhighlight C++ %}

Накрая, за да отпечатате текста на позицията на курсора, можете да извикате някоя от стандартните методи [`Serial.print`](https://github.com/arduino/ArduinoCore-avr/blob/master/cores/arduino/Print.h), включително тази подгрупа:

{% highlight C++ %}
size_t print(const String &);
size_t print(const char[]);
size_t print(char);

size_t println(const String &s);
size_t println(const char[]);
size_t println(char);
{% endhighlight C++ %}

Вижте [Serial.print() docs](https://www.arduino.cc/reference/en/language/functions/communication/serial/print/) или [Print.h](https://github.com/arduino/ArduinoCore-avr/ blob/master/cores/arduino/Print.h) за повече информация за API-то `print` или прочетете по-нататък за пример.

##### Центриране на текст

В творческото кодиране, визуализацията и разработката на игри често искаме да центрираме или да подравним текста по друг начин. За да го направим, трябва да го **измерим**. За щастие, библиотеката [Adafruit GFX](https://github.com/adafruit/Adafruit-GFX-Library/blob/master/Adafruit_GFX.h) има метод, наречен `getTextBounds`, който прави точно това!

{% highlight C++ %}
/************************************************** ************************/
/*!
@brief Помощник за определяне на размера на низ с текущия шрифт/размер.
Предава низ и позиция на курсора, връща горния ляв ъгъл, ширина и височина
@param str ASCII низът, който трябва да се измери
@param x Текущата X на курсора
@param y Текущата Y на курсора
@param x1 Координатата X на границата, върната от функцията
@param y1 Координатата Y на границата, върната от функцията
@param w Ширината на границата, върната от функцията
@param h Височината на границата, върната от функцията
*/
/**************************************************************************/
void getTextBounds(String &str, int16_t x, int16_t y, int16_t *x1, int16_t *y1, uint16_t *w, uint16_t *h);
{% endhighlight C++ %}

Например, в нашия пример [HelloWorld.ino](https://github.com/makeabilitylab/arduino/blob/master/OLED/HelloWorld/HelloWorld.ino) ние центрираме текста "Hello Makers!” както вертикално, така и хоризонтално на OLED екрана. Ключовият откъс е тук:

{% highlight C++ %}
int16_t x, y;
uint16_t textWidth, textHeight;
const char strHello[] = "Hello Makers!";

// Настройка на параметрите за рендиране на текст
_display.setTextSize(1);
_display.setTextColor(WHITE, BLACK);

// Измерване на текста с тези параметри. Предаване на x, y, textWidth и textHeight
// чрез препратка, така че да бъдат зададени в самата функция.
_display.getTextBounds(strHello, 0, 0, &x, &y, &textWidth, &textHeight);

// Центриране на текста на дисплея (както хоризонтално, така и вертикално)
_display.setCursor(_display.width() / 2 - textWidth / 2, _display.height() / 2 - textHeight / 2);

// Отпечатване на низ
_display.print(strHello);

// Рендиране на графичния буфер на екрана
_display.display();
{% endhighlight C++ %}

##### Обръщане на текста

Можем също да обърнем текста, като просто сменим цветовете в `setTextColor(uint16_t color, uint16_t backgroundcolor)`. За да нарисуваме черен текст на бял фон, ще напишем `_display.setTextColor(BLACK, WHITE);`

| setTextColor(WHITE, BLACK) | setTextColor(BLACK, WHITE) |
|----------------------------|----------------------------|
| ![](assets/images/OLED_setTextColor_WhiteBlack.png) | ![](assets/images/OLED_setTextColor_BlackWhite.png) |

#### Рисуване на вградените графики на шрифтове

Можете да рисувате вградените графики на шрифтове, като използвате `drawChar` или, подобно на [`Serial.write()`](https://www.arduino.cc/reference/en/language/functions/communication/serial/write/), библиотеката Adafruit GFX също поддържа функцията `write()`.

Макар че можете да използвате както `drawChar`, така и `write`, последната използва текущо зададените параметри `setText`, като `setTextSize` и `setTextColor`, което е полезно. По-долу отпечатвам всички глифи, вградени в шрифта по подразбиране, който включва вградени графики като усмивки, сърца, пики и др.

![](assets/images/OLED_UsingWriteToDisplayGraphicalCharacters.png)
**Фигура.** Изчертаване на вградените глифи в шрифта по подразбиране с помощта на `_display.write()`. Този код се нарича [DrawAllChars.ino](https://github.com/makeabilitylab/arduino/blob/master/OLED/DrawAllChars/DrawAllChars.ino) в нашия GitHub.
{: .fs-1 }

За да нарисуваме усмихнато лице – което е индекс на символ `2` в средата на екрана, например, можем да използваме `drawChar`:

{% highlight C++ %}
const int CHAR_WIDTH = 5;
const int CHAR_HEIGHT = 8;

int charSize = 3;
int charWidth = charSize * CHAR_WIDTH;
int charHeight = charSize * CHAR_WIDTH;
int charIndex = 2; // за усмихнато лице

uint16_t yText = _display.height() / 2 - charHeight / 2;
uint16_t xText = _display.width() / 2 - charWidth / 2;

_display.drawChar(xText, yText, (char)charIndex, SSD1306_WHITE, SSD1306_BLACK, charSize);
{% endhighlight C++ %}

Или можем да използваме метода `write()`:

{% highlight C++ %}
int16_t x1, y1;
uint16_t textWidth, textHeight;
int charIndex = 2; // за усмивка

_display.setTextSize(3);
_display.getTextBounds("X", 0, 0, &x1, &y1, &textWidth, &textHeight);
uint16_t yText = _display.height() / 2 - textHeight / 2;
uint16_t xText = _display.width() / 2 - textWidth / 2;
_display.setCursor(xText, yText);
_display.write(charIndex);
{% endhighlight C++ %}

Ето един [пример](https://github.com/makeabilitylab/arduino/blob/master/OLED/DrawChar/DrawChar.ino), който преминава през всички глифи поотделно и демонстрира горния код. Отново, можете да използвате или `drawChar`, или `write`, а аз демонстрирам и двете в [DrawChar.ino](https://github.com/makeabilitylab/arduino/blob/master/OLED/DrawChar/DrawChar.ino)

<video autoplay loop muted playsinline style="margin:0px">
<source src="assets/videos/OLED_DrawChar-IMG_6308-Optimized.mp4" type="video/mp4" />
</video>
**Видео** Демонстрация на [DrawChar.ino](https://github.com/makeabilitylab/arduino/blob/master/OLED/DrawChar/DrawChar.ino), показваща как да рисувате вградените графики от стандартния шрифт.
{: .fs-1 }

#### Зареждане на персонализирани шрифтове

В допълнение към шрифта с фиксиран размер и моноспецифично разстояние по подразбиране, можете да заредите и визуализирате алтернативен шрифт. Вижте раздела ["Зареждане на шрифтове"](https://learn.adafruit.com/adafruit-gfx-graphics-library/using-fonts) от [урока на Adafruit GFX](https://learn.adafruit.com/ adafruit-gfx-graphics-library/overview). 

Можете също да създадете собствен шрифт или персонализирани символи за вашия шрифт. Вижте упътването на Adafruit: "Създаване на персонализирани символни шрифтове за библиотеката Adafruit GFX" (https://learn.adafruit.com/creating-custom-symbol-font-for-adafruit-gfx-library/overview).

### Рисуване на битови карти

Накрая, можете да заредите и визуализирате персонализирани битови карти на дисплея. Вижте ["Displaying Bitmaps"](https://lastminuteengineers.com/oled-display-arduino-tutorial/#arduino-code-displaying-bitmap) в Last Minute Engineers.

<!-- TODO: обмислете да запишете видеоклип как се прави това или поне да покажете видеоклип или снимка как работи -->

### Ресурси за Adafruit GFX

Преди да продължите, силно ви препоръчваме да прочетете официалното [упътване за Adafruit GFX](https://learn.adafruit.com/adafruit-gfx-graphics-library/graphics-primitives) и [упътването за OLED](https://lastminuteengineers.com/oled-display-arduino-tutorial/) на Last Minute Engineers — и двете предлагат чудесен обзор на библиотеката Adafruit GFX и как да [показвате текст](https://lastminuteengineers.com/oled-display-arduino-tutorial/#arduino-code-displaying-text), [рисувате фигури](https://lastminuteengineers.com/oled-display-arduino-tutorial/# arduino-code-basic-drawings) и [зареждане и показване на битови карти](https://lastminuteengineers.com/oled-display-arduino-tutorial/#arduino-code-displaying-bitmap).

Освен това можете да:

- Разгледате изходния код на библиотеката Adafruit GFX [тук](https://github.com/adafruit/Adafruit-GFX-Library), включително [Adafruit_GFX.h](https://github.com/adafruit/Adafruit-GFX-Library/blob/master/Adafruit_GFX.h), който показва наличния API. Да, в зависимост от това колко сте запознати с C++ и четенето на .h файлове, това може да ви се стори плашещо или прекалено сложно, но е важно да разгадаете тези библиотеки. Те са просто изходен код, написан от разработчици. И с опит, вие също можете да го направите!

- Разгледайте нашите примери за OLED [тук](https://github.com/makeabilitylab/arduino/tree/master/OLED), включително споменатия по-горе пример [Hello World](https://github.com/makeabilitylab/arduino/blob/master/OLED/HelloWorld/HelloWorld.ino), прост пример за анимация, наречен [BallBounce] (https://github.com/makeabilitylab/arduino/blob/master/OLED/BallBounce/BallBounce.ino), [обектно-ориентирана версия] (https://github.com/makeabilitylab/arduino/blob/master/OLED/BallBounceObjectOriented/BallBounceObjectOriented.ino) на тази анимация, използваща класа [Shape.hpp](https://github.com/makeabilitylab/arduino/blob/master/MakeabilityLab_Arduino_Library/src/Shape. hpp) клас от [Makeability Lab Arduino библиотеката](https://github.com/makeabilitylab/arduino/tree/master/MakeabilityLab_Arduino_Library) и прости игри като [тест за сблъсък](https://github.com/makeabilitylab/arduino/blob/master/OLED/CollisionTest/CollisionTest.ino), [Pong](https://github.com/makeabilitylab/arduino/blob/master/OLED/Pong/Pong.ino) и [Flappy Bird](https://github.com/makeabilitylab/arduino/blob/master/OLED/FlappyBird/FlappyBird.ino). Ще разгледаме някои от тях по-долу.

## Да създадем нещо!

В тази част от урока ще направим различни творения на базата на OLED. Това ще бъде забавно! Както споменахме, имаме [GitHub репозиторий с OLED примери](https://github.com/makeabilitylab/arduino/tree/master/OLED), някои от които описваме по-долу.

### Дейност: рисуване на фигури и текст

Първо, за да се запознаете с Adafruit GFX API и координатната система, нека просто нарисуваме малко текст и фигури на екрана. Можете да изберете какво искате да нарисувате и къде. Мислете за това като за [абстрактно изкуство с фигури](https://www.google.com/search?q=abstract+shape+art)! 

Не забравяйте, че в `loop()` трябва да:

{% highlight C++ %}
// Изчистите дисплея. Ако не го направим, просто ще рисуваме върху
// предишните си изображения (което понякога може да е желателно, но като цяло не е)
_display.clearDisplay();

// Поставете рутинни команди за рисуване
drawStuff();

// Рендерирайте графичния буфер на екрана
_display.display();
{% endhighlight C++ %}

Направих версия, наречена [SimpleDrawingDemo.ino](https://github.com/makeabilitylab/arduino/blob/master/OLED/SimpleDrawingDemo/SimpleDrawingDemo.ino), която рисува фигури с произволни размери и местоположения на **всеки кадър**, но можете да направите нещо още по-просто (или по-сложно)!

<video autoplay loop muted playsinline style="margin:0px">
<source src="assets/videos/OLEDSimpleDrawingDemo-IMG_6188-TrimmedAndOptimized720p.mp4" type="video/mp4" />
</video>
**Видео** Демонстрация на [SimpleDrawingDemo.ino](https://github.com/makeabilitylab/arduino/blob/master/OLED/SimpleDrawingDemo/SimpleDrawingDemo.ino).
{: .fs-1 }

#### Дейност за създаване на прототип на рисуване на фигури

За вашите дневници за създаване на прототипи създайте своя собствена демонстрация за рисуване на фигури/текст. Направете снимка или, ако има анимация, запишете кратко видео или анимирано GIF. В дневниците си добавете линк към кода, вмъкнете снимките/видеата и отразявайте това, което сте научили.

### Дейност: нарисувайте подскачаща топка

Сега, след като се запознахме с API за рисуване и графичния пайплайн, нека научим малко за **анимацията**.

Ще нарисуваме проста подскачаща топка по екрана. Подскачащите или отразяващи се обекти са един от ключовите компоненти на много игри, включително [Pong](https://github.com/makeabilitylab/arduino/blob/master/OLED/Pong/Pong.ino), [Arkanoid](https://en.wikipedia.org/wiki/Arkanoid) и др.

За да създадем подскачаща топка, трябва да:

- Проследим **x,y местоположението** на топката през кадрите
- Да зададем **x,y скорост** в пиксели на кадър — т.е. колко се движи топката на кадър? За по-плавна анимация можем да проследяваме x,y скоростта във времето (*например* пиксели/секунда); това обаче е малко по-сложно (*например* изисква проследяване на времевите отметки в кода, изчисляване на времевите разлики *и т.н.*). За нашите цели проследяването на скоростта x,y в пиксели/кадър е напълно достатъчно.
- Проверявайте за **сблъсъци**, когато топката се сблъска с тавана, пода или стените на екрана. Когато се случи сблъсък, просто обърнете посоката на топката.
- ** Нарисувайте** кръга на даденото място x,y.

<!-- Повече за игровите цикли и времевите разлики:
- https://www.reddit.com/r/pcmasterrace/comments/29qcqr/an_explanation_of_game_loops_fps_and_delta_time/ciniknu?utm_source=share&utm_medium=web2x&context=3
- Забавянето трябва да е адаптивно, за да поддържа постоянна честота на кадрите: https://drewcampbell92.medium.com/understanding-delta-time-b53bf4781a03
- https://www.informit.com/articles/article.aspx?p=2928180&seqNum=6

Може би най-добрата статия, която съм чел:
- https://gameprogrammingpatterns.com/game-loop.html
- -->

#### Прототипиране на идеи с p5js

Ето [демонстрация на подскачаща топка](https://makeabilitylab.github.io/p5js/Animation/BallBounce2D/), която създадохме в [p5js](https://p5js.org/). Понякога е полезно да се създаде прототип на визуализация или идея за игра в бърза програмна среда като [p5js](https://p5js.org/) или [Processing](https://processing.org/), преди да се кодира в C++ за Arduino (а и е по-лесно да се отстраняват грешки в тези среди). Можете да редактирате и да си играете с тази демо версия в браузъра си [тук](https://editor.p5js.org/jonfroehlich/sketches/KpUirYrAk) с помощта на онлайн редактора p5js.

<video autoplay loop muted playsinline style="margin:0px">
<source src="assets/videos/BallBouncing_p5js.mp4" type="video/mp4" />
</video>
{: .mx-auto .align-center }

**Видео.** Видео на демото Ball Bounce, създадено в p5js. Можете да редактирате изходния код и да го изпълните на живо в онлайн редактора p5js [тук](https://editor.p5js.org/jonfroehlich/sketches/KpUirYrAk). Като алтернатива можете да [да видите изходния код](https://github.com/makeabilitylab/p5js/blob/master/Animation/BallBounce2D/sketch.js) в нашето [p5js GitHub репо](https://github.com/makeabilitylab/p5js).
{: .fs-1 }

#### C++ имплементация с Adafruit GFX

За C++ имплементацията с библиотеката Adafruit GFX и Arduino, ключовите части от кода са извлечени по-долу. Цялостната имплементация е доста подобна на [p5js версията](https://editor.p5js.org/jonfroehlich/sketches/KpUirYrAk). Уверете се, че сте прочели внимателно този код и сте го разбрали.

Отново, вместо да казваме "мили в час" или "пиксели в секунда", ние сме дефинирали скоростта като "пиксели на кадър" – тоест, колко пиксела се движи обектът на кадър. Ако зададем `_xSpeed` на 5 и `_ySpeed` на 0, тогава топката ще се движи 5 x пиксела на кадър (и просто ще отскача напред-назад от лявата страна на екрана към дясната и обратно).

{% highlight C++ %}
// Създаване на обект за показване
Adafruit_SSD1306 _display(128, 64, &Wire, 4);

// Глобални променливи на топката
const int _ballRadius = 5;
int _xBall = 0; // x местоположение на топката
int _yBall = 0; // y местоположение на топката
int _xSpeed = 0; // x скорост на топката (в пиксели на кадър)
int _ySpeed = 0; // y скорост на топката (в пиксели на кадър)

void setup() {
    // Инициализирайте дисплея
    _display.begin(SSD1306_SWITCHCAPVCC, 0x3D)

    // Получава случайно число между min и max - 1
    // https://www.arduino.cc/reference/en/language/functions/random-numbers/random/
    _xSpeed = random(1, 4);
    _ySpeed = random(1, 4);
}

void loop() {
    // Изчиства дисплея
    _display.clearDisplay();

    // Актуализира топката въз основа на скоростта и местоположението
    _xBall += _xSpeed;
    _yBall += _ySpeed;

    // Проверява за отскачане на топката. Първо проверява дали излиза от лявата или дясната страна на екрана
    if(_xBall - _ballRadius <= 0 || _xBall + _ballRadius >= _display.width()){
        _xSpeed = _xSpeed * -1; // обръща посоката по x
    }

    // Сега провери за отскачане от пода или тавана
    if(_yBall - _ballRadius <= 0 || _yBall + _ballRadius >= _display.height()){
        _ySpeed = _ySpeed * -1; // обърни посоката y
    }

    // Нарисувай кръг
    _display.drawCircle(_xBall, _yBall, _ballRadius, SSD1306_WHITE);

    // Рендиране на буфера на екрана
    _display.display();
}
{% endhighlight C++ %}

Можете да видите пълния код в GitHub като [BallBounce.ino](https://github.com/makeabilitylab/arduino/blob/master/OLED/BallBounce/BallBounce.ino). 

<!-- TODO: вмъкване на видео. -->

#### Отскачане на битова карта

Имаме и подобна демонстрация на "отскачане”, наречена [BitmapBounce.ino](https://github.com/makeabilitylab/arduino/blob/master/OLED/BitmapBounce/BitmapBounce.ino), която използва битова карта, а не графичен примитив. За да създадем байтния дъмп на битовата карта, използвахме този инструмент [image2cpp](http://javl.github.io/image2cpp/) върху това [лого на Makeability Lab](https://github.com/makeabilitylab/arduino/blob/master/OLED/BitmapBounce/logo_bw_no_text_600w.png).

<video autoplay loop muted playsinline style="margin:0px">
<source src="assets/videos/OLEDBouncingBitmap-IMG_6180-Optimized.mp4" type="video/mp4" />
</video>
**Видео.** Видео на [BitmapBounce.ino](https://github.com/makeabilitylab/arduino/blob/master/OLED/BitmapBounce/BitmapBounce.ino).
{: .fs-1 }

#### Дейност по създаване на дневник за прототипиране на анимации

За вашите дневници за прототипиране създайте персонализирана анимационна демонстрация, запишете кратко видео или анимиран GIF, добавете линк към кода и отразявайте това, което сте научили. Като прост пример променете обекта, който скача, от кръг на правоъгълник. Ако искате нещо по-предизвикателно, опитайте да скачате триъгълник по екрана и да използвате ъгъла на влизане и ъглите на триъгълника, за да изчислите правилно отражението (най-лесно е да направите това, като използвате [векторни изчисления](https://makeabilitylab.github.io/p5js/Vectors/BouncingBallsAndLineSegmentsImproved/)) . Или можете да използвате метода `drawLine`, за да анимирате дъжд, подобен на този [Purple Rain видеоклип](https://youtu.be/KkyIDI6rQJI) от [Coding Train](https://thecodingtrain.com/). Въпреки че това е направено за p5js, би било доста лесно да се преведе на Arduino и библиотеката Adafruit GFX.

### Дейност: интерактивна графика

Накрая, за нашата последна дейност, нека направим няколко **интерактивни прототипа**, т.е. графика, която реагира на цифров или аналогов вход. Интерактивността улавя истинската същност на физическото изчисление. И за [професор по HCI](https://jonfroehlich.github.io/) като мен, тук е мястото, където започва истинската радост!

#### Демонстрация 1: Настройка на размера на топката въз основа на аналогов вход

Ще започнем с промяна на размера на фигурата въз основа на вход от сензора. Макар че можете да използвате какъвто сензор пожелаете, за тази демонстрация ще използваме нашия старият и надежден [потенциометър](../arduino/potentiometers.md), свързан към `A0`.

##### OLED + потенциометър

Ето схемата. Същата като преди, но сме добавили 10K потенциометър.

![](assets/images/OLED_ArduinoLeonardo_POT_CircuitDiagram.png)
**Фигура** Основна OLED верига с [потенциометър](../arduino/potentiometers.md) вход на `A0`.
{: .fs-1 }

##### Кодът на OLED + потенциометър

Кодът е прост: прочетете аналоговия вход и го използвайте, за да зададете радиуса на кръга.

{% highlight C++ %}
void loop() {
    // При всеки цикъл ще искаме да изчистим дисплея, за да не записваме върху
    // предишно начертани данни
    _display.clearDisplay(); 

    // Прочетете стойността на аналоговия вход
    int sensorVal = analogRead(ANALOG_INPUT_PIN);

    // Максималният радиус е или ширината, или височината на дисплея, в зависимост от това коя е по-малка
    int maxRadius = min(_display.width(), _display.height());

    // Сега изчислете радиуса въз основа на стойността на сензора
    int radius = map(sensorVal, 0, MAX_ANALOG_INPUT, 0, maxRadius);

    // Центриране на кръга
    int xCircle = _display.width() / 2;
    int yCircle = _display.height() / 2;

    // Изчертаване на екрана
    _display.fillCircle(xCircle, yCircle, radius, SSD1306_WHITE);

    // Рендиране на графичния буфер на екрана
    _display.display(); 

    delay(50);
}
{% endhighlight C++ %}

Можете да видите пълния код в GitHub като [AnalogBallSize.ino](https://github.com/makeabilitylab/arduino/blob/master/OLED/AnalogBallSize/AnalogBallSize.ino).

<video autoplay loop muted playsinline style="margin:0px">
<source src="assets/videos/OLEDAnalogBallSize-IMG_6189-TrimmedAndOptimized.mp4" type="video/mp4" />
</video>
**Видео.** Видео на [AnalogBallSize.ino](https://github.com/makeabilitylab/arduino/blob/master/OLED/AnalogBallSize/AnalogBallSize.ino).
{: .fs-1 }

#### Демонстрация 2: Настройка на местоположението на топката въз основа на аналогов вход

Сега нека свържем **два** аналогови входа, за да контролираме местоположението x, y на кръга, а не размера. В този случай ще използваме два потенциометра. Схемата на свързване е показана по-долу.

![](assets/images/OLED_ArduinoLeonardo_2Pots_CircuitDiagram.png)
**Фигура** Схема на свързване и електрическа схема за два потенциометра и OLED дисплей.
{: .fs-1 }

Кодът е много подобен на [AnalogBallSize.ino](https://github.com/makeabilitylab/arduino/blob/master/OLED/AnalogBallSize/AnalogBallSize.ino). Но преобразуваме стойностите на `analogRead` в x и y координати: 

{% highlight C++ %}
void loop() {
    // При всеки цикъл ще искаме да изчистим дисплея, за да не записваме върху
    // предишно изчертани данни
    _display.clearDisplay();

    // Четем стойността на аналоговия вход
    int xSensorVal = analogRead(X_ANALOG_INPUT_PIN);
    delay(1); // дайте време на ADC
    int ySensorVal = analogRead(Y_ANALOG_INPUT_PIN);

    // Преобразувайте показанията на сензора в x, y пикселни местоположения
    int xLoc = map(xSensorVal, 0, MAX_ANALOG_INPUT, 0, _display.width());
    int yLoc = map(ySensorVal, 0, MAX_ANALOG_INPUT, 0, _display.height());

    // Нарисувайте го на екрана
    _display.fillCircle(xLoc, yLoc, BALL_RADIUS, SSD1306_WHITE);

    // Рендиране на графичния буфер на екрана
    _display.display(); 

    delay(50);
}
{% endhighlight C++ %}

Можете да видите пълния код в GitHub като [AnalogBallLocation.ino](https://github.com/makeabilitylab/arduino/blob/master/OLED/AnalogBallLocation/AnalogBallLocation.ino).

<video autoplay loop muted playsinline style="margin:0px">
<source src="assets/videos/OLEDMoveBallTwoPots-IMG_6190-TrimmedAndOptimized720p.mp4" type="video/mp4" />
</video>
**Видео** Демонстрация на [AnalogBallLocation.ino](https://github.com/makeabilitylab/arduino/blob/master/OLED/AnalogBallLocation/AnalogBallLocation.ino) с помощта на потенциометри на `A0` и `A1`.
{: .fs-1 }

#### Демонстрация 3: Основна аналогова графика в реално време

Една от най-известните демонстрации на [Arduino](https://www.arduino.cc/) + [Processing](https://processing.org/) е аналоговата графика на сензора в реално време ([link](https://www.arduino.cc/en/Tutorial/BuiltInExamples/Graph)): Arduino чете данните от сензора с помощта на `analogRead`, след което ги предава на компютъра с помощта на `Serial.println()`, където се анализират и графично представят с помощта на [Processing](https://processing.org/).

С OLED дисплея и библиотеката Adafruit GFX можем лесно да пресъздадем всичко това изцяло на Arduino!

Идеята е проста: прочетете стойността на сензора като `sensorVal`, начертайте вертикална линия в `xPos` с дължина, пропорционална на `sensorVal`, увеличете `xPos`, повторете. Когато `xPos >= _display.width()`, върнете `xPos` обратно на нула, изчистете дисплея и започнете целия процес отначало.

Забележително е, че този код се възползва от **селективното** извикване на `_display.clearDisplay()`. За разлика от другите примери, които сме споделили досега – които изчистват дисплея на всеки кадър – тук се възползваме от графиките, които се запазват при извикванията на `_display.display()`, за да "изградим" нашата графика във времето. Това означава, че рисуваме само **една** нова линия за всеки нов сензорен вход, която остава на екрана, докато `_xPos >= _display.width()`, в който момент извикваме `_display.clearDisplay()`.

{% highlight C++ %}
void loop() {

    // Чете аналоговата стойност на напрежението
    int analogVal = analogRead(ANALOG_INPUT_PIN);

    // Рисува линията за дадената стойност на сензора
    int lineHeight = map(analogVal, MIN_ANALOG_INPUT, MAX_ANALOG_INPUT, 0, _graphHeight);
    int yPos = _display.height() - lineHeight;

    // За чисто хоризонтални или вертикални линии има оптимизирани функции за рисуване на линии
    //, които избягват скъпи ъглови изчисления
    _display.drawFastVLine(_xPos++, yPos, lineHeight, SSD1306_WHITE);
    _display.display();

    // Ако x-позицията е извън дясната страна на екрана, изчистете дисплея
    // и започнете графиката отначало
    if (_xPos >= _display.width()) {
        _xPos = 0;
        _display.clearDisplay();
    }

    delay(10);
}
{% endhighlight C++ %}

Пълният изходен код е достъпен в нашия [OLED GitHub](https://github.com/makeabilitylab/arduino/tree/master/OLED) като [AnalogGraph.ino](https://github.com/makeabilitylab/arduino/blob/master/OLED/AnalogGraph/AnalogGraph.ino). Ето видео демонстрация:

<video autoplay loop muted playsinline style="margin:0px">
<source src="assets/videos/OLEDAnalogGraph_TrimmedAndOptimized720p.mp4" type="video/mp4" />
</video>
**Видео** Демонстрация на [AnalogGraph.ino](https://github.com/makeabilitylab/arduino/blob/master/OLED/AnalogGraph/AnalogGraph.ino) с използване на потенциометър за аналогов вход на `A0`. Показваме също така текущата измерена стойност на `A0` в горния ляв ъгъл и честотата на кадрите (fps) в горния десен ъгъл.
{: .fs-1 }

#### Демонстрация 4: Аналогова графика с превъртане в реално време

Малко подобрена, но по-сложна версия на аналоговата графика е **превъртащата** реализация. Вместо да изчистваме дисплея, когато `xPos >= _display.width()`, ние просто "превъртаме" съдържанието наляво. За ефективност на паметта и изчисленията, ние реализираме това с кръгов буфер, който е с размера на ширината на екрана ни (т.е. 64 стойности – по една за всеки x пиксел).

Разгледайте кода. Има ли смисъл? 

{% highlight C++ %}
int _circularBuffer[SCREEN_WIDTH]; //бърз начин за съхранение на стойности 
int _curWriteIndex = 0; // проследява къде се намираме в кръговия буфер

void loop() {
    // Изчистваме дисплея на всеки кадър. Рисуваме цялата графика на всеки кадър 
    // от _circularBuffer
    _display.clearDisplay ();

    // Четете и съхранявайте аналоговите данни в цикличен буфер
    int analogVal = analogRead(ANALOG_INPUT_PIN);
    Serial.println(analogVal);
    _circularBuffer[_curWriteIndex++] = analogVal;

    // Върнете индекса на цикличния буфер обратно на нула, когато достигне 
    // дясната страна на екрана
    if(_curWriteIndex >= _display.width()){
        _curWriteIndex = 0;
    }

    // Начертайте линейната графика въз основа на данните в _circularBuffer
    int xPos = 0;
    for (int i = _curWriteIndex; i < _display.width(); i++){
        int analogVal = _circularBuffer[i];
        drawLine(xPos, analogVal);
        xPos++;
    }

    for(int i = 0; i < _curWriteIndex; i++){
        int analogVal = _circularBuffer[i];
        drawLine(xPos, analogVal);
        xPos++;;
    }

    _display.display();

    delay(10);
}
{% endhighlight C++ %}

Пълният изходен код е достъпен в нашия [OLED GitHub](https://github.com/makeabilitylab/arduino/tree/master/OLED) като [AnalogGraphScrolling.ino](https://github.com/makeabilitylab/arduino/blob/master/OLED/AnalogGraphScrolling/AnalogGraphScrolling.ino). Ето видео демонстрация.
 

<video autoplay loop muted playsinline style="margin:0px">
<source src="assets/videos/OLED_ScrollingGraphDemo-IMG_6192-TrimmedAndOptimized720p.mp4" type="video/mp4" />
</video>
**Видео** Демонстрация на [AnalogGraphScrolling.ino](https://github.com/makeabilitylab/arduino/blob/master/OLED/AnalogGraphScrolling/AnalogGraphScrolling.ino) с използване на потенциометър за аналогов вход на `A0`. Показваме също така текущата стойност на `A0` в горния ляв ъгъл и честотата на кадрите (fps) в горния десен ъгъл.
{: .fs-1 }

Коя версия на графиката предпочитате? [AnalogGraph.ino](https://github.com/makeabilitylab/arduino/blob/master/OLED/AnalogGraph/AnalogGraph.ino) или [AnalogGraphScrolling.ino](https://github.com/makeabilitylab/arduino/blob/master/OLED/AnalogGraphScrolling/AnalogGraphScrolling.ino)? Ние лично предпочитаме втората!

#### Дейност за създаване на прототип на интерактивна графика

За вашите дневници за прототипиране, бързо създайте прототип на интерактивна OLED демонстрация, използвайки сензор по ваш избор, и проектирайте проста визуализация или отзивчива графика около този вход. В дневника си включете кратко описание с кратко видео (или анимиран GIF) и отразявайте това, което сте научили. Като една проста идея, за да ви дадем представа за това, което търсим тук, какво ще кажете да комбинирате анимация + интерактивност: какво ще стане, ако промените скоростта на топката в [BallBounce.ino] (https://github.com/makeabilitylab/arduino/blob/master/OLED/BallBounce/BallBounce.ino) въз основа на сензорния вход?

<!--
 
Описание на дейността:

- Анимация с топка
- Топка, която променя скоростта си в зависимост от аналоговия вход
- Преминаване към FSR

- Визуализация на аналоговия вход под формата на линейна графика
- Връзка към версия на аналоговата графика с възможност за превъртане

- Разширени OLED
- Къде говорим за използването на Makeability_Lab_Library и методите за рисуване?
- Няколко i2c устройства: accel + OLED
- Няколко OLED дисплея

- ВЪЗМОЖНО ЗА ИЗПЪЛНЕНИЕ: свързване на няколко OLED дисплея
- Можете да свържете няколко OLED дисплея. Но всеки от тях ще се нуждае от различен адрес. По подразбиране адресът е 0x3D (покажете снимка на гърба). Adafruit breakout board улеснява настройването на адреса на 0x3C, като просто свържете `SA0` с `GND`.
- Показване на отскачане на топка на два екрана? -->

## Ресурси

### OLED

- [Урок за OLED дисплей Arduino](https://lastminuteengineers.com/oled-display-arduino-tutorial/), Last Minute Engineers

- [Монохромни OLED разклонители](https://learn.adafruit.com/monochrome-oled-breakouts), Adafruit

- [Adafruit_GFX Library](https://learn.adafruit.com/adafruit-gfx-graphics-library/overview), Adafruit

- [SSD1306 Datasheet](https://cdn-shop.adafruit.com/datasheets/SSD1306.pdf), Solomon Systech

- [Бързо SSD1306 OLED рисуване с I2C Bit Banging](https://bitbanksoftware.blogspot.com/2018/05/fast-ssd1306-oled-drawing-with-i2c-bit.html), Larry Bank ([видео демонстрация](https://youtu.be/aQxOtyEr6eQ))

### Серийни комуникационни протоколи

- [I2C](https://learn.sparkfun.com/tutorials/i2c/all), Sparkfun.com

- [SPI](https://learn.sparkfun.com/tutorials/serial-peripheral-interface-spi), Sparkfun.com

## Следващ урок

В [следващия урок](vibromotor.md) ще научим за вибрационните мотори и как да ги използваме с Arduino.

<!-- В [следващия урок](resistors.md) ще разширим знанията си за [резистори](resistors.md) – специално проектирани електрически компоненти, които *устойчиви* на протичането на ток – преди да покажем как те са полезни с [LED диоди](leds.md). -->

<span class="fs-6">
[Следващо: Вибрационни мотори](vibromotor.md){: .btn .btn-outline }
<!-- [Следващо: Резистори](resistors.md){: .btn .btn-outline } -->
</span>
