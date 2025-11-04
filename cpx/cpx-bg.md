---
lang: bg
permalink: /cpx/cpx.html
page_id: cpx-cpx
layout: default
title: L1&#58; Въведение в CPX
parent: Платката Circuit Playground Express
has_toc: true # (по подразбиране)
comments: true
nav_exclude: false
usetocbot: true
---
# {{ page.title | replace_first:"L",'Урок '}}
{: .no_toc }

## Съдържание
{: .no_toc .text-delta }

1. Съдържание
{:toc}
---

![Ръка, държаща платка Circuit Express Playground](assets/images/CircuitExpressPlaygroundHandModelShot_Adafruit_Edited.png)
**Фигура.** Circuit Express Playground. Изображение от [Adafruit](https://www.adafruit.com/product/3333).
{: .fs-1 }
 

Circuit Playground Express (CPX) е въвеждаща платка за физическо компютърно програмиране, създадена от [Adafruit](https://adafruit.com). Това е чудесна платформа за електронно прототипиране, подходяща за изучаване на *електроника* и *програмиране* и за създаване на творчески проекти за физическо компютърно програмиране (*например,* [вижте примери тук](https://learn.adafruit.com/category/circuit-playground)).

В сравнение с [Arduino](../arduino/index.md), предимствата на CPX за начинаещи производители са две:

1. Първо, CPX може да се програмира с **лесен за използване визуален език за програмиране с плъзгане и пускане**, наречен [MakeCode](https://makecode.adafruit.com/), разработен от [Microsoft](https://www.microsoft.com/en-us/makecode), който е подобен на [Scratch](https://scratch.mit.edu/). С натрупването на опит и знания учениците и създателите могат да преминат към по-напреднали езици за програмиране, като [CircuitPython](https://learn.adafruit.com/adafruit-circuit-playground-express/what-is-circuitpython) (Python) или [Arduino](https://learn.adafruit.com/adafruit-circuit-playground-express/arduino) (C/C++).

2. Второ, CPX включва разнообразни **вградени входове и изходи**, така че не е необходимо да закупувате или свързвате външни компоненти (или дори да използвате [бредборд](../electronics/breadboards.md)). Вградените **входове** включват [акселерометър LIS3DH] (https://learn.adafruit.com/adafruit-lis3dh-triple-axis-accelerometer-breakout), сензор за ниво на осветеност (фототранзистор), няколко бутона, микрофон, а **изходите** включват [неопикселни LED-ове](https://learn.adafruit.com/neopixels-with-makecode), високоговорител и инфрачервени приемници/предаватели.

За да контекстуализираме потенциала на CPX още повече, можем да използваме трите критерия за оценка на творческите конструкторски комплекти, които Мичъл Резник и Брайън Силвърман очертават в своята фантастична статия IDC'05 ["Някои размисли върху проектирането на конструкторски комплекти за деца"](https://doi.org/10.1145/1109540.1109556). Творческите конструкторски комплекти трябва да имат:

1. **Ниски подове** – комплектите трябва да са достъпни и лесни за използване от начинаещи;
2. **Високи тавани** – комплектите трябва да растат заедно с вас, докато учите и натрупвате опит, като ви позволяват да създавате все по-сложни проекти;
3. и **Широки стени** – комплектите трябва да поддържат широка гама от дизайни и проекти.
 

Ние вярваме, че CPX отговаря на всеки от тези критерии, което го прави мощна платформа за прототипиране и обучение. Например, в Университета на Вашингтон CPX се използва в нашата [MHCI+D програма](https://mhcid.washington.edu/), както и в някои въвеждащи курсове по електротехника — доста широк спектър от контексти!

## Хардуер
<!-- ![Анотирана версия на Circuit Playground Express, показваща местоположението на всички компоненти](assets/images/CircuitExpressHardwareOverview_AnnotationsByJonFroehlich.png)
**Фигура.** Общ преглед на хардуера на Circuit Express Playground (CPX), включително вградени входове и изходи. Вижте по-долу за по-големи версии.
{: .fs-1 } -->

<!-- ![](assets/images/BuiltInCPXInput_AnnotationsByJonFroehlich.png.png)

![Анотирана версия на Circuit Playground Express, показваща местоположението на всички компоненти](assets/images/CircuitPlaygroundExpress_AnnotatedImage_Adafruit.png)
*Фигура.* Анотирана версия на CPX, показваща местоположението на всички основни компоненти. Изображение от [Adafruit](https://learn.adafruit.com/adafruit-circuit-playground-express/guided-tour). -->

Едно от основните предимства на хардуера CPX – в сравнение с обикновените Arduino платки като Uno – е, че той е пълен с невероятни входни/изходни (IO) компоненти. Adafruit предоставя подробна ["разходка"](https://learn.adafruit.com/adafruit-circuit-playground-express/guided-tour), но накратко, платка включва пет типа входни компоненти, включително движение, температура, светлина, звук и бутони, както и два типа изходни компоненти (LED, звук).

{: .note }
Няма проблем, ако не разбирате цялата терминология, използвана по-долу. Всъщност, ако това е първият път, когато се занимавате с електроника, очакваме, че всичко това е ново за вас. Все пак си струва да прегледате разделите по-долу, за да се запознаете с възможностите на CPX, преди да започнем да го сглобяваме!

### Вграден вход

<video autoplay loop muted playsinline style="margin:0px">
<source src="assets/videos/CPX_PaintingWithCPXAccelerometerAsAMouse.mp4" type="video/mp4" />
</video>

**Видео.** CPX има много забавни и интересни вградени сензори, включително акселерометър, температурен, светлинен, звуков и други. В горното видео показвам как да използвате вградения акселерометър (сензор за движение), за да създадете "мишка за движение” с CPX. Вижте [L7.2: Мишка с акселерометър](cpx-mouse.md#lesson-72-accelerometer-mouse) за повече информация! 
{: .fs-1 }

По-конкретно, CPX включва следните вградени входове/сензори:

- 1 x сензор за движение (триосен акселерометър LIS3DH с откриване на докосване, откриване на свободно падане)
- 1 x сензор за температура (термистор)
- 1 x сензор за светлина (фототранзистор). Може да действа и като сензор за цвят и сензор за пулс.
- 1 x сензор за звук (MEMS микрофон)
- 2 x бутона, обозначени с A и B
- 1 x плъзгащ превключвател

![Анотирана диаграма, показваща местоположението на вградените сензори за движение, температура, светлина, звук, заедно с бутоните и плъзгащия превключвател](assets/images/BuiltInCPXInput_AnnotationsByJonFroehlich.png)

**Фигура.** Анотирана картина на вградените сензори/вход на CPX.
{: .fs-1 .align-center}

### Вграден изход

В допълнение към вградения вход, CPX има и вградени LED диоди и високоговорител за изход на светлина и звук. По-конкретно:

- 10 x мини [NeoPixels](https://learn.adafruit.com/neopixels-with-makecode), всеки от които може да показва всеки цвят
- 1 x мини високоговорител с усилвател клас D (7,5 mm магнитен високоговорител/зумер)
- Зелен светодиод "ON", за да знаете, че е включен
- Червен светодиод "#13" за основно мигане

![Анотирана диаграма, показваща местоположението на вградените неопиксели и високоговорител](assets/images/BuiltInCPXOutput_AnnotationsByJonFroehlich.png)

**Фигура.** Анотирана изображение на вградения изход на CPX.
{: .fs-1 .align-center}



<!-- ### I/O

- Инфрачервен (IR) приемник и предавател: може да приема и предава всички кодове за дистанционно управление, както и да изпраща съобщения между Circuit Playground Expresses. Може да действа и като сензор за близост.
- 8 x входни/изходни пина, подходящи за крокодилски клеми
- Включва I2C, UART, 8 пина, които могат да правят аналогови входове, множество PWM изходи -->

## Вход/изход (I/O)

В допълнение към вградените компоненти, CPX има 14 свързващи подложки, които поддържат интерфейс с външни входове/изходи (I/O), включително бутони, LED и други. Можете да използвате различни стратегии за свързване, от шиене с проводима нишка до увиване на проводници и дори малки метални винтове, но най-често използваното свързване е с клещи тип "алигатор". 

<!-- TODO: вмъкване на снимка или анимиран филм на CPX с клещи тип "алигатор" -->

<!-- ![Диаграма на изводите на CPX, подчертаваща 14-те клещи](assets/images/CPX_14AlligatorClips_ByJonFroehlich.png) -->

![Диаграма на изводите на CPX, подчертаваща 14-те алигаторни подложки](assets/images/CPX_14AlligatorClipsAnnotated_ByJonFroehlich.png)

**Фигура.** Изображение с анотации на 14-те алигаторни подложки на CPX за захранване и GPIO.
{: .fs-1 .align-center}

### Входно-изходни (I/O) контакти

CPX има осем универсални I/O пина (GPIO) за свързване с външни електронни компоненти. Всички I/O контакти могат да се използват като цифрови I/O, аналогови входове и PWM. 

{: .warning }
Всеки пад може да осигури до ~20mA ток, така че **не свързвайте директно мотор** или друг компонент с висока мощност. Ако не знаете какво означава това, няма проблем! Винаги можете да попитате екипа за инструкции дали даден компонент е безопасен за използване!

![Диаграма на пиновете на CPX, подчертаваща CPX GPIO контактите](assets/images/CPX_GPIOPadsAnnotated_ByJonFroehlich.png)

<!-- TODO: обмислете добавянето на кратко .mp4, показващо сензора за налягане + CPX светлини и второ .mp4, показващо NeoPixel свързване. -->

За повече информация вижте [Ръководството за пиновете на CPX на Adafruit](https://learn.adafruit.com/adafruit-circuit-playground-express/pinouts#each-pin-2906289).

### Аналогов вход
<video autoplay loop muted playsinline style="margin:0px">
<source src="assets/videos/CPX_AnalogInput_PotentiometerOverview_Optimized.mp4" type="video/mp4" />
</video>

**Видео.** Пинковете A1-A7 на CPX могат да се използват за аналогов вход за отчитане на напрежения между 0-3,3 V, които CPX преобразува в число между 0-1023. Тук използвам [потенциометър](../electronics/variable-resistors.md#potentiometers), който динамично променя съпротивлението си (и разделя нивата на напрежение) в зависимост от позицията на копчето. Научете повече за аналоговия вход в [L8: Аналогов вход](analog-input.md)!
{: .fs-1 }

CPX има шест пина, които могат да четат аналогов вход (A1-A7). Аналоговите входни пинове четат нива на напрежение, които варират между 0V (GND) и 3.3V. CPX преобразува тези напрежения в число между 0-1023, използвайки т.нар. аналогово-цифров преобразувател (ADC). Официалните документи на CPX посочват ADC като 12 бита (0-4096), но ние установихме, че на практика той е по подразбиране 10 бита. Така че аналоговият сигнал се преобразува от 0 до 1023.

По-долу е показана схемата на изводите на CPX, на която са отбелязани аналоговите входни изводи (A1-A7):

![Схема на изводите на CPX, на която са отбелязани аналоговите входни изводи](assets/images/CPX_AnalogInputPads_ByJonFroehlich.png)

Повече за аналоговия вход ще научите в [L8: Аналогов вход](analog-input.md)!

### Капацитивни сензорни панели

<video autoplay loop muted playsinline style="margin:0px">
<source src="assets/videos/CPX_CapacitiveSensing_SodaCanProximityDetector_MakeCode_Optimized.mp4" type="video/mp4" />
</video>
**Видео.** Пинът A1-A7 на CPX може да се използва за капацитивно докосване. Тук показвам как можем да използваме кутия от сода, за да направим прост детектор за близост на ръка. [Научете повече тук!](capacitive-touch.md)
{: .fs-1 }

От осемте GPIO пина **седем** могат да се използват за капацитивно докосване (пинове A1-A7). Ще научите повече за капацитивното докосване в [Урок 5](capacitive-touch.md)!

![Диаграма на пиновете на CPX, подчертаваща капацитивните сензорни панели](assets/images/CPX_CapacitiveTouchPadsAnnotated_ByJonFroehlich.png)

### Панели за захранване

Както е описано в [ръководството за Adafruit CPX](https://learn.adafruit.com/adafruit-circuit-playground-express/pinouts#power-pads-2906283), има шест панела за захранване, разположени на равни разстояния по периферията на CPX. По-конкретно, има:

- 3 x **GND** панела, които са свързани помежду си
- 2 x **3.3V out** подложки
- 1 x **USB/battery Vout** подложка, която е специална захранваща подложка. Този пин ще доставя или USB захранване (5V), или LiPoly захранване (3.7V). Ако и двете са свързани, CPX доставя по-високото напрежение. Този изход не е свързан с вградения регулатор, така че може да доставя до 500mA непрекъснато и 1A пиково напрежение, преди да се задейства вътрешният предпазител (ако предпазителят се задейства, просто изчакайте минута и той автоматично ще се нулира)

![Диаграма на пиновете на CPX, подчертаваща захранващите падове с клещи](assets/images/CPX_PowerPadsAnnotated_ByJonFroehlich.png)

**Фигура.** Изображение с бележки на GND и Vout захранващите падове на CPX.
{: .fs-1 .align-center}

### Микроконтролер CPX

CPX разполага и с мощен вграден микроконтролер – процесор ATSAMD21 ARM Cortex M0 – работещ при 3,3 V и 48 MHz. За сравнение, Arduino Uno се захранва от много по-стар и по-бавен микроконтролер: ATmega328P при 5 V и 16 MHz.

## Използване на CPX като вход за компютър

<video playsinline style="margin:0px" controls>
<source src="assets/videos/CPX_BananaPiano_OptimizedTrimmed.mp4" type="video/mp4" />
</video>
**Видео.** CPX може да се използва като контролер за вход към вашия компютър. Можете да си направите своя собствена клавиатура, мишка, джойстик и много други! Този пример е взет от [Урок 5.3: Изработване на капацитивна клавиатура](capacitive-touch.md#lesson-53-making-a-capacitive-touch-keyboard).
{: .fs-1 }

Подобно на Arduino Leonardo, CPX може да действа като клавиатура, мишка, джойстик, MIDI или просто сериен порт. Така че можете лесно да създадете персонализиран вход за вашия компютър – страхотно!

Можете да научите повече за това в:

- [Урок 5.3: Изработване на капацитивна клавиатура](capacitive-touch.md#lesson-53-making-a-capacitive-touch-keyboard)
- [Урок 6: Използване на CPX като клавиатура](cpx-keyboard.md)
- [Урок 7: Използване на CPX като мишка] (cpx-mouse.md)

## Програмиране

Допълнително предимство на CPX в сравнение с традиционния Arduino е, че може да се програмира по различни начини.

За начинаещи с ограничени познания по програмиране или за тези, които просто харесват визуалните езици за програмиране, можете да използвате **[MakeCode](https://learn.adafruit.com/adafruit-circuit-playground-express/makecode)**. По-напредналите потребители могат да изберат Python чрез **[CircuitPython](https://learn.adafruit.com/adafruit-circuit-playground-express/what-is-circuitpython)** или C/C++ чрез **[Arduino IDE](https://learn.adafruit.com/adafruit-circuit-playground-express/arduino)**.

### MakeCode

MakeCode на Microsoft е проектиран да предоставя визуален интерфейс с функция "дръпни и пусни” за програмиране на проекти за физически изчисления. Този визуален стил на програмиране, наречен "блоково програмиране”, е популяризиран от [Scratch](https://scratch.mit.edu/) и е подобен на него. Видеото по-долу показва как да програмирате CPX просто чрез "дръпни и пусни” на "парченца от пъзел” (блокове).

Удивително е, че можете да тествате програмата си и да видите как се държи с "виртуален" CPX директно в MakeCode. Виждате ли CPX в лявата странична лента? Този CPX е симулатор, който показва как ще работи кода ви, когато в крайна сметка бъде зареден на самия CPX хардуер!

<!--
Това е старото видео на Adafruit, което имахме тук
<video class="img img-responsive lazy" preload="auto" muted="muted" loop="loop" autoplay="autoplay" playsinline="" poster="https://cdn-learn.adafruit.com/assets/assets/000/048/088/medium800thumb/makecodedragdemo.jpg? 1510260958">
<source src="https://cdn-learn.adafruit.com/assets/assets/000/048/088/large1024mp4/makecodedragdemo.mp4?1510260958">
<source src="https://cdn-learn.adafruit.com/assets/assets/000/048/088/large1024webm/makecodedragdemo.webm?1510260958" type="video/webm; codecs=vp8,vorbis">
<source src="https://cdn-learn.adafruit.com/assets/assets/000/048/088/large1024ogv/makecodedragdemo.ogv?1510260958" type="video/ogg; codecs=theora,vorbis">
Вашият браузър не поддържа видео тага.
</video> -->

<video autoplay loop muted playsinline style="margin:0px">
<source src="assets/videos/Making_Blinky_MakeCode_Annotated.mp4" type="video/mp4" />
</video>
**Видео.** Бързо създаване на пълна програма с MakeCode, наречена "Blinky". Ще включим всички NeoPixels (като ги настроим на червено), след това ще ги спрем, ще ги изключим (като ги настроим на черно) и ще повторим "завинаги". [Връзка към кода](https://makecode.com/_JdPfj8VrmWV3).
{: .fs-1 }

## Ресурси за обучение

<!-- ![Снимка на уебсайта MakeCode, където можете да намерите връзки към проекти](assets/images/MakeCode_Screenshot_Tutorials.png)
**Фигура** Снимка на [уебсайта Adafruit MakeCode](https://makecode.adafruit.com/), който съдържа връзки към уроци и примерни проекти.
{: .fs-1 } -->

За да научите повече, Adafruit и MakeCode са публикували серия от добре обмислени и лесни за разбиране уроци:
- Въведение ["Какво е MakeCode и как се използва"](https://learn.adafruit.com/makecode)

- Можете да намерите [уроци стъпка по стъпка за MakeCode + CPX](https://makecode.adafruit.com/) в самия редактор MakeCode. Хубавото тук е, че редакторът MakeCode ви води през всяка стъпка. Страхотно!

- Можете също да получите достъп до горните уроци като [традиционни, линейни стъпка по стъпка ръководства тук](https://makecode. adafruit.com/tutorials).

- [Peli de Halleux](https://learn.adafruit.com/users/pelikhan) от Microsoft е създал няколко ръководства за CPX+MakeCode на уебсайта на Adafruit, включително едно за [NeoPixels](https://learn.adafruit.com/neopixels-with-makecode) и друго за [CPX Sensors](https://learn. adafruit.com/sensors-in-makecode).

- Adafruit публикува и индивидуални "курсове", включително [Използване на CPX Pins](https://makecode.adafruit.com/learnsystem/pins-tutorial), [Логична лаборатория](https://makecode.adafruit.com/learnsystem/logic-lab) и [Курс за създатели](https://makecode.adafruit.com/courses/maker).

- Накрая, ако искате да се запознаете по-подробно с някои от отделните хардуерни компоненти на CPX, [Shawn Hymel](https://shawnhymel.com/), Adafruit и MakeCode се обединиха, за да създадат серия от видео уроци, наречена [Behind the MakeCode Hardware](https://makecode.adafruit.com/ behind-the-makecode-hardware), включваща теми като:
- [Neopixels](https://youtu.be/Bo0cM2qmuAE). Вижте също урокът на Halleux [NeoPixels with MakeCode](https://learn.adafruit.com/neopixels-with-makecode).
- [Високоговорител](https://youtu.be/JjJ-KGwKh_4). Вижте също урокът [Make it Sound](https://learn.adafruit.com/make-it-sound?view=all#music-and-sound-in-makecode).
- [Акселерометър](https://youtu.be/2HzNKz-QlV0)
- [Светлинен сензор](https://youtu.be/9LrWQ68lO20)
- [Инфрачервен сензор](https://youtu.be/0EMuaMClfos)
- [Микрофон](https://youtu.be/g5894PVYOF4)

### Примерни проекти

- Adafruit публикува [примерни проекти MakeCode+CPX](https://learn.adafruit.com/category/makecode) заедно с уроци.

## Следващ урок

В [следващия урок](makecode.md) ще създадем първата си програма MakeCode+CPX, наречена Blinky. Докато я създаваме, ще научим за програмната среда MakeCode, симулатора и как да заредим програмата си на CPX.

<span class="fs-6">
[Следващо: Програмиране на CPX с MakeCode](makecode.md){: .btn .btn-outline }
</span>

## Отражения върху образованието

Като човек, който работи и преподава физическо програмиране от почти десетилетие, MakeCode преодолява няколко бариери за начинаещите (в приблизителен ред по важност):

- Първо, интерфейсът, базиран на блокове, с функция "дръпни и пусни”, е много по-достъпен за начинаещи програмисти, отколкото IDE на Arduino и средата C/C++. MakeCode генерира **реален** JavaScript код въз основа на вашата блок програма, така че можете да преминавате между двете.
- Второ, **обработка на събития**. Ключово предизвикателство с Arduino за начинаещите е обработката на събития (например, когато се натисне бутон, направи това), особено когато програмите съдържат много цикли (което може да направи системата да изглежда неотзивчива, вижте тази [дискусия](https://makeabilitylab.github.io/physcomp/arduino/led-fade.html#improved-fading-approach-limiting-delays)).
- Трето, има вградена **симулационна среда**, която ви позволява веднага да видите как ще работи кодът ви, преди да го качите на физическото си CPX устройство
- И накрая, това е **уеб-базиран редактор**. Няма нищо за инсталиране и можете да програмирате CPX от уеб браузъра си. И след като сте заредили редактора, той остава в кеша на браузъра ви (така че работи офлайн).
