---
lang: bg
permalink: /arduino/force-sensitive-resistors.html
page_id: arduino-force-sensitive-resistors
layout: default
title: L5&#58; Резистори, чувствителни към сила
nav_order: 5
parent: Вход
grand_parent: Въведение в Arduino
has_toc: true # (по подразбиране)
comments: true
usemathjax: true
usetocbot: true
---
# {{ page.title | replace_first:"L",'Урок '}}
{: .no_toc }

## Съдържание
{: .no_toc .text-delta }

1. Съдържание
{:toc}
---

В този урок ще научите за резисторите, чувствителни към сила (FSR), и как да използвате FSR и двукраки променливи резистори по-общо с микроконтролери. Накрая ще изработим "чувствителен към сила” музикален инструмент – много подобен на този на джедаите!

Този урок се основава директно на предишния ([потенциометри](potentiometers.md)), така че непременно завършете първо него.

![Анимация, показваща FSR](/assets/movies/FSR_LEDCircuit_ArduinoForPower_WorkbenchWithAmmeter.gif)

**Фигура.** Анимацията показва как съпротивлението на FSR спада с прилаганото налягане (по-високо налягане, по-ниско съпротивление, по-ярък LED).
{: .fs-1 }

## Материали

Ще ни трябват следните материали:

| Breadboard | Arduino | FSR | Резистор | Пиезо зумер |
|:-----:|:-----:|:-----:|:-----:|:-----:|
| ![Бретборд]({{ site.baseurl }}/assets/images/Breadboard_Half.png) | ![Arduino Uno]({{ site.baseurl }}/assets/images/ArduinoUno_Fritzing.png) | ![FSR]({{ site.baseurl }}/assets/images/FSR_200h.png) | ![Изображение на резистор 10KOhm]({{ site.baseurl }}/assets/images/Resistor10K_Fritzing_100w.png) | ![Пиезо зумер]({{ site.baseurl }}/assets/images/PiezoBuzzer_100h.png) |
| Breadboard | Arduino Uno, Leonardo или подобен | [Резистор, чувствителен към сила](https://www.adafruit.com/product/166) | 10kΩ резистор | [Пиезо зумер](https://www.mouser.com/ProductDetail/810-PS1240P02BT) |

## Силочувствителни резистори (FSR)

Силочувствителните (или силочувствителни) резистори (FSR) са двукраки променливи резистори, чието съпротивление **намалява** с **увеличаването** на приложената сила.

FSR могат да се различават по размер, форма и чувствителност към сила. Има различни форми, включително квадратни и кръгли (които съдържат активната сензорна зона). В нашите хардуерни комплекти обикновено закупуваме и предоставяме популярния [Interlink FSR 402]({{ site.baseurl }}/assets/datasheets/ForceSensitiveResistor_InterlinkFSR402_2010-10-26-DataSheet-FSR402-Layout2.pdf) (или от [Sparkfun](https://www.sparkfun.com/products/9375), или от [Adafruit](https://www.adafruit.com/product/166)), който е продуктът в горния ляв ъгъл по-долу.

![Мрежа от примери за чувствителни към сила резистори от уебсайта на Sparkfun](assets/images/ForceSensitiveResistors_Examples_Sparkfun.png)
Цени и продукти от [Sparkfun.com](https://learn.sparkfun.com/tutorials/force-sensitive-resistor-hookup-guide/all)
{: .fs-1 }

### Приложения на FSR

Какво можем да правим с FSR?

В [FSR 402 datasheet]({{ site.baseurl }}/assets/datasheets/ForceSensitiveResistor_InterlinkFSR402_2010-10-26-DataSheet-FSR402-Layout2.pdf) са описани редица примери за приложения, включително:
- **Откриване на човешко взаимодействие.** Откриване дали докосването е случайно или умишлено чрез отчитане на силата (или друга обработка на сигнала)
- **Използване на сила за обратна връзка с потребителския интерфейс.** Откриване на силата на докосване на потребителя за създаване на по-интуитивен интерфейс
- **Повишаване на безопасността на инструментите.** Разграничаване на хващане от докосване като предпазна ключалка
- **Намиране на центъра на силата.** Използване на множество сензори за определяне на центъра на силата
- **Откриване на присъствие, позиция или движение** Откриване на човек/пациент в легло, стол или медицинско устройство
- **Откриване на запушване с течност.** Откриване на запушване или блокиране на тръба или помпа чрез измерване на обратното налягане

Макар че FSR реагират на сила, те не са прецизни измервателни инструменти като [товароизмервателни клетки](https://learn.sparkfun.com/tutorials/getting-started-with-load-cells) или [тензометрични датчици](https://learn.sparkfun.com/tutorials/getting-started-with-load-cells/strain-gauge-basics), така че използвайте тях, ако искате да измерите точно теглото, натоварването или деформацията.

<!-- TODO: в бъдеще включете статии от HCI и UbiComp с сензори за налягане -->

### Как работят FSR?

Как всъщност работят FSR? Конструкцията им е доста проста. Има три слоя: горният и долният слой са проводими, а средният слой осигурява "тънък въздушен слой", който разделя двата. Когато двата проводими слоя се притискат един към друг, се създават електрически пътища. Колкото по-силно натискате, толкова повече връзки се създават. И колкото повече връзки, толкова по-малко съпротивление. Вижте диаграмата на конструкцията на FSR от Interlink по-долу:

![Диаграма на конструкцията на FSR от Interlink, показваща три слоя: горният и долният слой са проводими, а средният слой е "въздушна междина", която ги разделя. ](assets/images/FSR_ConstructionDiagram_Interlink.png)
Диаграма от Interlink FSR [Ръководство за интеграция]({{ site.baseurl }}/assets/datasheets/ForceSensitiveResistor_Interlink_IntegrationGuide.pdf)
{: .fs-1 }

<!-- TODO: в бъдеще обмислете добавянето на втора диаграма, която показва как се създават връзките в "активната зона", когато горният слой се спуска? -->

### Графика на силата и съпротивлението на FSR

И така, каква точно е връзката между съпротивлението на FSR и приложената сила?

Графика на силата (g) спрямо съпротивлението (kΩ) на FSR 402 е показана по-долу (нанесена на логаритмична скала). Както може да се види от графиката, FSR има две фази на реакция: 

1. Начална "сила на скъсване" или "праг на включване", която драстично променя съпротивлението от >10MΩ до приблизително 10kΩ
2. След този праг съпротивлението на FSR става обратно пропорционално на приложената сила (следвайки характеристиката на обратната степенна зависимост).

В горния край на диапазона на сила (повече от 1000g), FSR се насища и не продължава да понижава съпротивлението.

![Графика на съпротивлението спрямо кривата на силата за Interlink FSR 402, показваща, че съпротивлението спада с прилаганото налягане](assets/images/ForceSensitiveResistor_ResistanceForceCurve_InterlinkFSR402.png)
Графика на силата (g) спрямо съпротивлението (kΩ), нанесена на логаритмична скала за Interlink FSR 402. Графика от [Interlink FSR Integration Guide]({{ site.baseurl }}/assets/datasheets/ForceSensitiveResistor_Interlink_IntegrationGuide.pdf).
{: .fs-1 }

За повече подробности вижте [FSR 402 datasheet]({{ site.baseurl }}/assets/datasheets/ForceSensitiveResistor_InterlinkFSR402_2010-10-26-DataSheet-FSR402-Layout2.pdf) и [Integration Guide] ({{ site.baseurl }}/assets/datasheets/ForceSensitiveResistor_Interlink_IntegrationGuide.pdf).

## Изработване на димер за LED с FSR

Да направим нещо!

За да започнем, точно както направихме с уроците за [бутоните](buttons.md) и [потенциометрите](potentiometers.md), ще направим проста LED верига без микроконтролер. Всъщност тази верига ще бъде точно същата като веригата с потенциометър "реостат" [тук] (potentiometers.md#build-the-potentiomer-based-led-dimmer) (но ще заменим реостата с FSR).

По-долу показваме две възможни схеми на свързване: първата (предпочитана) показва веригата FSR, захранвана от 9V батерия, докато втората показва захранване, получено от 5V и GND пиновете на Arduino. (Отново, ние предпочитаме първата, само за да подчертаем, че в този момент не използваме микроконтролери!

![Две схеми на свързване на FSR, свързан с LED](assets/images/FSR_WiringDiagram_NoArduino_Fritzing.png)
Две опции за свързване на FSR с помощта на breadboard. Както типичните резистори, FSR могат да бъдат включени във вашите вериги в двете посоки.
{: .fs-1 }

При окабеляването с 9V включваме резервен резистор, но при окабеляването с 5V (с Arduino) не го правим. Причината за това е, че както [FSR 402 datasheet]({{ site.baseurl }}/assets/datasheets/ForceSensitiveResistor_InterlinkFSR402_2010-10-26 -DataSheet-FSR402-Layout2.pdf) и нашият собствен емпиричен опит показват, че дори при значителна сила (около 1000 g според техническата спецификация), FSR все още има съпротивление от ~200 Ω-500 Ω. Така че, докато потенциометърът може да падне до 0 Ω при най-ниската настройка, FSR не го прави и следователно не се нуждае от резервен резистор.

За 9V окабеляване, ако приемем, че $$V_f=2V$$ на червения LED и най-ниското съпротивление на FSR от 200Ω, тогава $$I=\frac{9V-2V}{200Ω}=35mA$$, което надвишава максималния ток на LED. Затова добавихме резервен резистор 470Ω за сигурност. Така $$I=\frac{9V-2V}{200Ω + 470Ω}=10.4mA$$.

### Позициониране на FSR на платка

Двете контактни крачета са на разстояние 2,54 mm (0,1") едно от друго, така че трябва да се побират добре в платка. Точно като традиционен резистор, FSR може да се вмъкне в двете посоки.

![FSR близък план на двата контактни крака](assets/images/FSR_ContactLegs_Zoom_FromSparkfun.png)
Изображение от [Sparkfun.com](https://learn.sparkfun.com/tutorials/force-sensitive-resistor-hookup-guide/all#res).
{: .fs-1 }

Ако искате по-трайна връзка, вижте този [фантастичен наръчник](https://learn.sparkfun.com/tutorials/force-sensitive-resistor-hookup-guide/all#hardware-assembly) от Sparkfun за запояване на FSR (трудно) или използване на Amphenol FCI Clinchers (препоръчително):

![Изображение, показващо Amphenol CFI clincher конектори, инсталирани на крачетата на FSR] (assets/images/FSR_Clinchers_Sparkfun.png)
Изображение от [Sparkfun.com](https://learn.sparkfun.com/tutorials/force-sensitive-resistor-hookup-guide/all#hardware-assembly), показващо Amphenol CFI клипсови конектори, инсталирани на краката на FSR.
{: .fs-1 }

### Видео от работното място на завършената верига

След като направите веригата, забавлявайте се с FSR. Почувствайте неговата отзивчивост и колко силно трябва да натискате.

Ето видео от работното място на нашата завършена верига (това е същото видео като това в урока за [потенциометрите](potentiometers.md), така че има резервен резистор):

<iframe width="736" height="414" src="https://www.youtube.com/embed/YMCqDcnwMYo" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
Видео от работното място на веригата за димер на FSR LED
{: .fs-1 }

## Използване на FSR с микроконтролери
Добре, след като вече имате известен опит с FSR и разбирате как да ги използвате *без* микроконтролер, нека разгледаме как да ги използвате *с* микроконтролер.

Първо, както обикновено, ще ви покажем грешния начин за свързване на компонент към микроконтролер:

![Неправилна схема на свързване и схема на Arduino за FSR](assets/images/ArduinoUno_FSR_Incorrect_SchematicAndDiagram.png)

Защо това не работи?

Спомнете си от урока ни за [потенциометри](potentiometers.md), че микроконтролерите четат напрежение, а не ток. Трябва да настроим верига, която позволява на микроконтролера да "вижда" промените в напрежението.

<!-- направете и покажете анимация на потенциометъра, разделен на два резистора, и как това е същото, което трябва да направим за нашия FSR -->

Трябваше да направим същото и с [потенциометъра](potentiometers.md). Потенциометърът не би работил като аналогов вход, ако се използват само два крака. Трябваше да свържем и трите крака на потенциометъра.

За да използвате FSR – или какъвто и да е променлив резистор – с микроконтролер, трябва да добавите фиксиран резистор, за да образувате делител на напрежение, както е показано тук:

![Схема на свързване и схема на Arduino за FSR](assets/images/ArduinoUno_FSR_SchematicAndDiagram.png)

Този фиксиран резистор е като свързване на третия крак на потенциометъра. Той е подобен и на резисторите за изтегляне нагоре или надолу за нашите превключвателни вериги (и всъщност, когато FSR **не** е натиснат, той действа като отворен превключвател, защото съпротивлението му е много високо).

### Как да изберем фиксирания резистор

Но как да знаем каква стойност да изберем за този фиксиран резистор? Да погледнем в техническите спецификации!

В [Ръководството за интегриране на Interlink FSR]({{ site.baseurl }}/assets/datasheets/ForceSensitiveResistor_Interlink_IntegrationGuide.pdf) се предлага да изберете фиксирания резистор (наречен $$R_M$$) въз основа на конкретния контекст на употреба, за да максимизирате желания диапазон на чувствителност към сила и да ограничите тока.

Ръководството предоставя полезна графика на силата *срещу* $$V_{out}$$ с различни стойности на фиксирания резистор ($$R_M$$). Както може да се види от графиката, изборът на резистор 10kΩ за $$R_M$$ осигурява най-динамичния диапазон $$V_ {out}$$ за целия диапазон на силата на FSR. Обърнете внимание и на двуфазната зависимост с първоначален стръмен наклон, последван от по-плавно увеличение.

![Графика на силата на FSR спрямо Vout за различни стойности на фиксирания резистор от техническото описание на Interlink FSR](assets/images/Voltage-divider-circuit-Interlink-FSR-402-Makerguides.png)
Графика, първоначално от [Interlink FSR Integration Guide]({{ site.baseurl }}/assets/datasheets/ForceSensitiveResistor_Interlink_IntegrationGuide.pdf). Изображението по-горе е от [Makerguides](https://www.makerguides.com/fsr-arduino-tutorial).
{: .fs-1 }

Като цяло, за резистивен сензор като FSR, прочетете техническото описание (разбира се), но също така експериментирайте с сензора. Започнете с фиксиран резистор 10kΩ, напишете проста програма за Arduino, за да графично изобразите аналоговия вход в отговор на различни стимули (в този случай сила) и продължете оттам.

## Да направим нещо!

Ще започнем с проста верига за четене на FSR и пропорционално настройване на яркостта на вградения LED на Arduino. Ще графично изобразим входа на FSR, използвайки [Serial Plotter](https://randomnerdtutorials.com/arduino-serial-plotter-new-tool/) на Arduino IDE. След това ще завършим с "инструмента” Jedi-force "инструмент". За двете конструкции опитайте да направите веригата и да напишете кода, преди да погледнете нашите решения. Можете да го направите!

## LED фейдър на базата на FSR

### LED фейдър верига на базата на FSR

Нека направим проста FSR верига с фиксиран резистор (10kΩ) в положение pull-down. В тази конфигурация аналоговият вход A0 (VA0) ще се увеличава с нарастващата сила и ще започва от 0V, когато FSR не е натиснат.

![Схема на свързване на FSR за Arduino Uno с FSR крак 1 свързан към 5V и крак 2 свързан към фиксиран резистор 10kΩ в положението на пулдаун резистор](assets/images/ArduinoUno_FSR_FixedResistorInPullDown_SchematicAndDiagram.png)

### Код за LED фейд на базата на FSR

За нашия код за затъмняване на LED на базата на FSR ще прочетем стойността на FSR от делителя на напрежението, използвайки `analogRead`, и след това ще я използваме, за да настроим пропорционално яркостта на LED, използвайки `analogWrite`. Лесно, нали?

#### Преобразуване на обхвата на analogRead в обхват на analogWrite, използвайки map()

Има един малък проблем, а именно, че `analogRead` (на Uno и Leonardo) използва 10-битов ADC. По този начин стойността на `analogRead` варира от 0 до 1023; стойността на `analogWrite` обаче е 8 бита, което означава, че варира от 0 до 255. Затова трябва да направим просто преобразуване между двата диапазона: 0-1023 към 0-255.

Ако приемем, че и двата диапазона започват от нула (както е в този случай), преобразуването е просто: `int outputVal = (int)(inputVal/1023.0 * 255);`.
 

Ако вместо това не можем да приемем, че и двата диапазона започват от нула, по-общият алгоритъм за преобразуване е: `int outputVal = OUTPUT_MIN + (inputVal - INPUT_MIN)/(INPUT_MAX - INPUT_MIN) * (OUTPUT_MAX - OUTPUT_MIN);` Този тип преобразуване на диапазони е толкова често срещан, че Arduino (както и Processing и много други програмни библиотеки) имат вградена функция за него, наречена [`map`](https://www.arduino.cc/reference/en/language/functions/math/map/). Нарича се "map", защото искаме да преобразуваме число от един диапазон в друг. Ето цялата функция `map` от изходния код на Arduino:

{% highlight C %}
long map(long x, long in_min, long in_max, long out_min, long out_max) {
return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;
}
{% endhighlight C %}

Важно е да се отбележи, както става ясно от [документацията](https://www.arduino.cc/reference/en/language/functions/math/map/), че този вграден метод използва **целочислена** математика и затова няма да връща дроби (плаващи). Ако се нуждаете от по-прецизни преобразувания, имплементирайте своя собствена функция за съпоставяне (която също така предоставя възможност за имплементиране на нелинейни преобразувания като логаритмични съпоставяния). 

Добре, сега, след като изяснихме това, нека да напишем нашия код!

#### Пълен код за затъмняване на LED на базата на FSR

<!-- gist-it не работи, затова сега използваме emgithub -->
<!-- <script src="https://gist-it.appspot.com/https://github.com/makeabilitylab/arduino/blob/master/Basics/analogRead/ForceSensitiveResistorLED/ForceSensitiveResistorLED.ino?footer=minimal"></script> -->
<script src="https://emgithub.com/embed.js?target=https%3A%2F%2Fgithub.com%2Fmakeabilitylab%2Farduino%2Fblob%2Fmaster%2FBasics%2FanalogRead%2FForceSensitiveResistorLED%2FForceSensitiveResistorLED.ino&style=github&showCopy=on"></script>

Този [изходен код](https://github.com/makeabilitylab/arduino/blob/master/Basics/analogRead/ForceSensitiveResistorLED/ForceSensitiveResistorLED.ino) се намира в GitHub.
{: .fs-1 }

### Видео от работната маса със сериен плотер

Ето видео от работната маса със съответния запис на екрана на сериен плотер. Стойностите на FSR `analogRead` са в синьо, а стойностите на LED PWM `analogWrite` са в оранжево. Използваме вградения LED, така че промените в яркостта на LED може да са трудни за забелязване във видеото.

<iframe width="736" height="414" src="https://www.youtube.com/embed/MTpmVaVi92o" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

## Инструмент за силата на джедаите

За нашето последно творение ще направим инструмент за силата на джедаите: колкото по-силно натискате FSR, толкова по-висока е честотата, на която свирим на пиезо. Отново, опитайте се да го направите сами, без да гледате нашата схема или код.

### Схема на силата на джедаите

Просто добавете пиезо зумер и го свържете към GPIO пин.

![Схема на свързване на пиезо инструмента на базата на FSR](assets/images/ArduinoUno_FSRPiezoInstrument_BreadboardDiagram.png)

### Код за силата на Джедаите

В [нашия код](https://github.com/makeabilitylab/arduino/blob/master/Basics/analogRead/ForceSensitiveResistorPiezo/ForceSensitiveResistorPiezo.ino) възпроизвеждаме звук само когато FSR е натиснат (за да ограничим досадата). :)

<!-- gist-it не работи, затова сега използваме emgithub -->
<!-- <script src="https://gist-it.appspot.com/https://github.com/makeabilitylab/arduino/blob/master/Basics/analogRead/ForceSensitiveResistorPiezo/ForceSensitiveResistorPiezo.ino?footer=minimal"></script> -->
<script src="https://emgithub.com/embed.js?target=https%3A%2F%2Fgithub.com%2Fmakeabilitylab%2Farduino%2Fblob%2Fmaster%2FBasics%2FanalogRead%2FForceSensitiveResistorPiezo%2FForceSensitiveResistorPiezo.ino&style=github&showCopy=on"></script>

Този [изходен код](https://github.com/makeabilitylab/arduino/blob/master/Basics/analogRead/ForceSensitiveResistorPiezo/ForceSensitiveResistorPiezo.ino) се намира в GitHub.
{: .fs-1 }

### Видео на работната маса със сериен плотер

Ето нашето мнение по въпроса! Уверете се, че звукът ви е включен (или не), ако искате да чуете пиезо зумера! 

<iframe width="736" height="414" src="https://www.youtube.com/embed/OuEABPQV9_k" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

## Упражнения

За вашите дневници за прототипиране изберете едно от следните разширения и го реализирайте!

- Можете ли да подобрите инструмента на силата на джедаите, така че да звучи по-добре (е, толкова добре, колкото можем да направим пиезо с квадратни вълни да звучи). Какво ще кажете например да свирите само ноти от гамата?
- Добавете няколко LED диода, които да работят като "барграф” за стойността на FSR.
- Опитайте се да направите лоу-фай сензор за налягане, използвайки ежедневни материали, и го използвайте, за да направите нов инструмент за силата на Джедаите!
- Друга идея, за която можете да се сетите (която би трябвало да отнеме около 15-20 минути, за да се реализира!)

<!-- ### Направете свой собствен лоу-фай сензор за налягане. TODO: покажете супер прост лоу-фай сензор за налягане, направен от молив. Покажете версията с крокодилски клещи и версията с лента за скачане. -->

## Референции
- [Интерлинк FSR 402 технически спецификации]({{ site.baseurl }}/assets/datasheets/ForceSensitiveResistor_InterlinkFSR402_2010-10-26-DataSheet-FSR402-Layout2.pdf)
- [Ръководство за интегриране на Interlink FSR]({{ site.baseurl }}/assets/datasheets/ForceSensitiveResistor_Interlink_IntegrationGuide.pdf)
- [Урок за резистори, чувствителни към сила (FSR), с Arduino](https://www.makerguides.com/fsr-arduino-tutorial/), Makerguides.com
- [Резистори, чувствителни към сила (FSR)](http://www.openmusiclabs.com/learning/sensors/fsr/), Open Music Labs
- [Резистор, чувствителен към сила (FSR)](https://learn.adafruit.com/force-sensitive-resistor-fsr), Adafruit Learn
- [Ръководство за свързване на резистор, чувствителен към сила](https://learn.sparkfun.com/tutorials/force-sensitive-resistor-hookup-guide/all), Sparkfun Tutorials
