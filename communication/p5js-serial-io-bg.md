---
lang: bg
permalink: /communication/p5js-serial-io.html
page_id: communication-p5js-serial-io
layout: default
title: L4&#58; p5.js Сериен Вход/Изход
nav_order: 4
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

Добре, сега наистина започваме! Научихме за [серийната комуникация](serial-intro.md), след това как да използваме серийната комуникация в нашите браузъри ([web serial!](web-serial.md)), а след това как да направим това с [p5.js](p5js-serial.md). И вече създадохме няколко интересни демонстрации за доказателство на концепцията.

Нека използваме тези нарастващи знания и инерция, за да създадем малко по-сложни програми. Първо ще разгледаме случая с използването на p5.js за контрол на нещо в Arduino (`Компютър → Arduino`), след което ще въведем двупосочната комуникация (`Компютър ↔ Arduino`), при която компютърът и Arduino работят заедно, за да създадат цялостно интерактивно преживяване.

## DisplayShapeOut: p5.js към Arduino

За начало ще създадем проста демонстрационна програма p5.js, която рисува и променя размера на избрана фигура (кръг, триъгълник или правоъгълник) въз основа на x позицията на мишката и изпраща данните за тази фигура като текстово кодиран низ, разделен със запетая, през уеб сериален порт: ("shapeType, shapeSize”). От страна на Arduino ще анализираме този низ и ще нарисуваме текущата форма и размер на OLED. Тъй като размерът на платното p5.js и размерът на OLED екрана не съвпадат, ще използваме нормализирана стойност на размера между [0,1], където 0 е най-малкият размер, а 1 е максималният размер. Типът на формата се кодира като 0 за кръг, 1 за квадрат и 2 за правоъгълник.

Ето малка предварителен поглед върху това как ще изглежда крайният интерактивен опит.

<video autoplay loop muted playsinline style="margin:0px">
<source src="assets/videos/DisplayShapeIn.ino-DisplayShapeOut-Trimmed-Optimized.mp4" type="video/mp4" />
</video>
**Видео.** Демонстрация на приложението p5.js [DisplayShapeOut] (https://github.com/makeabilitylab/p5js/tree/master/WebSerial/p5js/DisplayShapeOut) и Arduino скица [DisplayShapeIn.ino](https://github.com/makeabilitylab/arduino/blob/master/Serial/DisplayShapeSerialIn/DisplayShapeSerialIn.ino). Приложението p5.js изпраща `shapeType` и `shapeSize` като текстов низ, разделен със запетая, към Arduino чрез уеб сериен порт. Програмата [DisplayShapeIn.ino](https://github.com/makeabilitylab/arduino/blob/master/Serial/DisplayShapeSerialIn/DisplayShapeSerialIn.ino) анализира този текст и изчертава фигура с подходящ размер на OLED. Не използвах обичайната си настройка за запис, защото OBS Studio + моята камера за документи имат забележимо забавяне. Можете да разглеждате, редактирате и играете с кода DisplayShapeOut в [онлайн редактора p5.js](https://editor.p5js.org/jonfroehlich/sketches/TfE1BjOX6) или от нашия GitHub ([страница на живо] (https://makeabilitylab.github.io/p5js/WebSerial/p5js/DisplayShapeOut/), [код](https://github.com/makeabilitylab/p5js/tree/master/WebSerial/p5js/DisplayShapeOut))
{: .fs-1 }

### Създаване на DisplayShapeOut в p5.js

Както и в [предходния урок](p5js-serial.md), ще започнем с [`SerialTemplate`](https://github.com/makeabilitylab/p5js/tree/master/WebSerial/p5js/SerialTemplate) . Ако използвате VSCode, копирайте [`SerialTemplate`](https://github.com/makeabilitylab/p5js/tree/master/WebSerial/p5js/SerialTemplate) и преименувайте папката на `DisplayShapeOut`. Ако използвате онлайн редактора p5.js, просто отворете този проект, [Serial Template](https://editor.p5js.org/jonfroehlich/sketches/vPfUvLze_C) и преименувайте проекта си на `DisplayShapeOut`.

#### Общ преглед на функционалността на DisplayShapeOut

Нека разгледаме някои от основните функции на DisplayShapeOut. Искаме потребителят да:

- **Избере текуща форма (кръг, триъгълник или правоъгълник)**. Ще направим това, като ги изброим поред чрез натискане на мишката

- **Промени размера на фигурата**. Ще направим това, като проследим x позицията на мишката и я съпоставим с размера

- **Изпрати данните за фигурата по сериен порт.** Всеки път, когато се промени текущата фигура или размер, трябва да изпратим актуализация по сериен порт. Ще направим това, като използваме [нашия уеб сериен клас](web-serial.md#our-web-serial-class)

#### Нарисувайте и променете динамично размера на фигурата

Ще изградим това стъпка по стъпка. Първо ще се фокусираме върху кода за рисуване на фигури в p5.js и след това ще добавим уеб сериен. Нека започнем с поддръжка на един тип фигура и добавяне на промяна на размера чрез позицията на мишката по ос x (подобно на [тази част от предишния ни урок](p5js-serial.md#make-circle-dynamically-sized)).

Добавете следните променливи от най-високо ниво:

{% highlight JavaScript %}
const MIN_SHAPE_SIZE = 10; // минимален размер на фигурата в пиксели
const MAX_SHAPE_MARGIN = 10; // когато фигурата е с максимален размер, маргинът до края на платното
let maxShapeSize = -1; // максималният размер на фигурата
let curShapeSize = 10; // текущият размер на фигурата
{% endhighlight JavaScript %}

Използваме префикса [`const`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/const), за да обозначим променливи само за четене, и [`let`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/let) за променливи с обхват на блок.

Сега инициализирайте `maxShapeSize` въз основа на ширината/височината на платното в `setup()`:

{% highlight JavaScript %}
function setup(){
...
maxShapeSize = min(width, height) - MAX_SHAPE_MARGIN;
...
}
{% endhighlight JavaScript %}

Актуализирайте функцията `draw()`, за да нарисувате формата (засега кръг).

{% highlight JavaScript %}
function draw() {
background(100);

fill(250);
noStroke();
const xCenter = width / 2;
const yCenter = height / 2;
circle(xCenter, yCenter, curShapeSize);
}
{% endhighlight JavaScript %}

Накрая, трябва да променим `curShapeSize` въз основа на x позицията на мишката:

{% highlight JavaScript %}
function mouseMoved(){
curShapeSize = map(mouseX, 0, width, MIN_SHAPE_SIZE, maxShapeSize);

// mouseMoved() се извиква дори когато мишката не е директно над платното
// затова се уверете, че сте ограничили само минималния и максималния размер. Ако не го направите
// кръгът може да стане по-голям, отколкото очаквате. Опитайте!
curShapeSize = constrain(curShapeSize, MIN_SHAPE_SIZE, maxShapeSize);
}
{% endhighlight JavaScript %}

Това е! Направихме първоначална интерактивна приложение за форми. Запазете работата си и я изпробвайте с [Live Server](https://marketplace.visualstudio.com/items?itemName=ritwickdey.LiveServer) на VSCode или просто натиснете бутона "play" в редактора p5.js.

Ето [демонстрация на живо](https://editor.p5js.org/jonfroehlich/sketches/qh-E0BRaR) от онлайн редактора p5.js. Преместете мишката върху платното по-долу, за да видите как размерът на кръга се променя пропорционално на x позицията на мишката.

<iframe width="736" height="400" scrolling="no" src="https://editor.p5js.org/jonfroehlich/embed/qh-E0BRaR"></iframe>
**Код.** Първоначалната структура на кода за интерактивно променяне на размера на фигурата въз основа на x позицията на мишката. Можете да видите, редактирате и експериментирате с кода [тук](https://editor.p5js.org/jonfroehlich/sketches/qh-E0BRaR).
{: .fs-1 }

#### Добавете поддръжка за няколко фигури

Сега нека добавим поддръжка за изобразяване на повече фигури: квадрат и триъгълник. Имаме нужда от променлива, за да проследяваме текущия тип фигура, и метод, с който потребителят да превключва между фигурите:

За да проследяваме текущия тип форма, ще използваме JavaScript [`Object`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object) — гъвкав, основен [тип данни в JavaScript](https://developer.mozilla.org/en-US/ docs/Web/JavaScript/Data_structures). Всичко, което не е [примитивен тип данни](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#data_and_structure_types) в JavaScript — *например* неща, които не са [String](https://developer.mozilla.org/en-US/ docs/Glossary/String), [Boolean](https://developer.mozilla.org/en-US/docs/Glossary/Boolean), [Number](https://developer.mozilla.org/en-US/docs/Glossary/Number), *и т.н.* — е JavaScript [`Object`](https://developer. mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object). В този случай просто ще третираме този обект като хранилище на ключове/стойности, така че нека го наречем `mapShapeTypeToShapeName`, където променливата показва "съпоставяне" на тип фигура (0, 1, 2) с име на фигура (кръг, квадрат, триъгълник). И ще проследяваме текущия тип форма чрез `curShapeType`.

{% highlight JavaScript %}
const mapShapeTypeToShapeName = {
0: "Circle",
1: "Square",
2: "Triangle"
};

let curShapeType = 0; // проследяване на текущия тип форма
{% endhighlight JavaScript %}

Така че `mapShapeTypeToShapeName` дефинира трите фигури и тяхната връзка ключ/стойност, а `curShapeType` проследява текущата фигура като 0 (за кръг), 1 (за квадрат) и 2 (за триъгълник).

За избор на типа на фигурата има много възможности – можем да нарисуваме малки иконични изображения на кръг, квадрат и триъгълник и да сменяме типа на фигурата, когато се кликне върху тях (като бутони). Но ще направим нещо още по-просто: ще увеличаваме `curShapeType` при всяко кликване с мишката.

{% highlight JavaScript %}
function mouseClicked() {
curShapeType++;
if(curShapeType >= Object.keys(mapShapeTypeToShapeName).length){
curShapeType = 0;
}

// Вашият шаблон може да има и този код в mouseClicked()
// Засега го коментирайте.
//if (!serial.isOpen()) {
// serial.connectAndOpen(null, serialOptions);
//}
}
{% endhighlight JavaScript %}

Накрая, трябва да актуализираме функцията `draw()`, за да нарисуваме трите типа фигури:
{% highlight JavaScript %}
function draw() {
background(100);
fill(250);
noStroke();
const xCenter = width / 2;
const yCenter = height / 2;
const halfShapeSize = curShapeSize / 2;

switch(curShapeType){
case 0: // изчертаване на кръг
circle(xCenter, yCenter, curShapeSize);
break;
case 1: // начертаване на квадрат
rectMode(CENTER); // Виж: https://p5js.org/reference/#/p5/rectMode
square(xCenter, yCenter, curShapeSize);
break;
case 2: // начертаване на триъгълник
let x1 = xCenter - halfShapeSize;
let y1 = yCenter + halfShapeSize;

let x2 = xCenter;
let y2 = yCenter - halfShapeSize;

let x3 = xCenter + halfShapeSize;
let y3 = y1;

triangle(x1, y1, x2, y2, x3, y3)
}
}
{% endhighlight JavaScript %}

За по-голяма удобство за потребителя, нека добавим и някои инструкции. В края на функцията draw() покажете текст, който гласи "Кликнете с мишката, за да промените формата":

{% highlight JavaScript %}
function draw() {
...

// Някои инструкции за потребителя
noStroke();
fill(255);
const tSize = 14; // размер на текста
const strInstructions = "Кликнете с мишката, за да промените формата";
textSize(tSize);
let tWidth = textWidth(strInstructions);
const xText = width / 2 - tWidth / 2;
text(strInstructions, xText, height - tSize + 6);
}
{% endhighlight JavaScript %}

Готово! Сега проверете работата си, като я заредите с Live Server или в онлайн редактора p5.js. Ето [жива демонстрация](https://editor.p5js.org/jonfroehlich/sketches/v3xWP3Np1):

<iframe width="736" height="400" scrolling="no" src="https://editor.p5js.org/jonfroehlich/embed/v3xWP3Np1"></iframe>
**Код.** Промяна на формите с кликване на мишката. Код [тук](https://editor.p5js.org/jonfroehlich/sketches/v3xWP3Np1).
{: .fs-1 }

#### Добавяне на уеб сериен изход

Накрая, последната стъпка е да изведем типа и размера на формата чрез уеб сериен изход. За да ограничим ненужните серийни записи, ще проследяваме последния тип и размер на формата и ще изпращаме нови данни само когато тези стойности се променят.

Първо, нека добавим серийна функция за запис, наречена `serialWriteShapeData(shapeType, shapeSize) `, която приема типа и размера на формата и ги извежда през уеб сериала като текстово кодирани данни.

{% highlight JavaScript %}
async function serialWriteShapeData(shapeType, shapeSize) {
if (serial.isOpen()) {
// Преобразувайте размера на формата в дроб между [0, 1] включително
let shapeSizeFraction = (shapeSize - MIN_SHAPE_SIZE) / (maxShapeSize - MIN_SHAPE_SIZE);

// Форматирайте текстовия низ, който да се изпрати през сериален порт. nf просто форматира плаващата запетая
// Вижте: https://p5js.org/reference/#/p5/nf
let strData = shapeType + ", " + nf(shapeSizeFraction, 1, 2);
serial.writeLine(strData);
}
}
{% endhighlight JavaScript %}

Забележително е, че преобразуваме размера на фигурата, който е в пиксели, в нормализирана стойност между [0, 1], наречена `shapeSizeFraction`—това е това, което ще предаваме по сериен порт и ще интерпретираме от страна на Arduino.

Сега нека актуализираме функцията `mouseClicked()`, за да се справим с отварянето и свързването с уеб сериала или, ако е установена връзка, да увеличим `curShapeType` и да изпратим новите данни през сериала, като извикаме новата ни функция `serialWriteShapeData()`.

{% highlight JavaScript %}
function mouseClicked() {
if (!serial.isOpen()) {
// Ако сериалната връзка не е отворена, започнете последователност за отваряне/свързване
serial.connectAndOpen(null, serialOptions);
}else{
// В противен случай увеличете типа на фигурата
curShapeType++;
if(curShapeType >= Object.keys(mapShapeTypeToShapeName).length){
curShapeType = 0;
}

// Тъй като типът на фигурата току-що се промени, запишете новите стойности в сериала
serialWriteShapeData(curShapeType, curShapeSize);
}
}
{% endhighlight JavaScript %}

Нека актуализираме и инструкциите за потребителя, за да знае, че кликването с мишката зависи от състоянието:

{% highlight JavaScript %}
function draw(){
...
// Някои инструкции за потребителя
noStroke();
fill(255);
const tSize = 14;
let strInstructions = "";
if(serial.isOpen()){
strInstructions = "Кликнете с мишката където и да е, за да промените формата";
}else{
strInstructions = "Кликнете където и да е, за да се свържете със сериала"
}
textSize (tSize);
let tWidth = textWidth(strInstructions);
const xText = width / 2 - tWidth / 2;
text(strInstructions, xText, height - tSize + 6);
}
{% endhighlight JavaScript %}

Накрая, трябва да актуализираме метода `mouseMoved()`, за да извикаме `serialWriteShapeData()` при нов размер на фигурата:

{% highlight JavaScript %}
function mouseMoved(){
let lastShapeSize = curShapeSize;
curShapeSize = map(mouseX, 0, width, MIN_SHAPE_SIZE, maxShapeSize);
curShapeSize = constrain(curShapeSize, MIN_SHAPE_SIZE, maxShapeSize);

if(lastShapeSize != curShapeSize){
serialWriteShapeData(curShapeType, curShapeSize);
}
}
{% endhighlight JavaScript %}

И готово с приложението p5.js! Можете да разглеждате, редактирате и експериментирате с кода в [онлайн редактора p5.js ](https://editor.p5js.org/jonfroehlich/sketches/TfE1BjOX6) или от нашия GitHub ([жива страница](https://makeabilitylab.github.io/p5js/WebSerial/p5js/ DisplayShapeOut/), [кода](https://github.com/makeabilitylab/p5js/tree/master/WebSerial/p5js/DisplayShapeOut)).

<!-- TODO: да обмислим десния клик за прекъсване на връзката? Тогава бихме могли да вградим всичко това в двупосочната серийна уеб страница? Но може да стане объркващо, ако имаме няколко примера на една страница -->

### Създаване на DisplayShapeIn в Arduino

Можем да проектираме много различни видове Arduino приложения, които четат `"shapeType, shapeSize"` от сериала и правят нещо интересно. Например, можем да използваме тази информация, за да зададем размера на ракетата и типа на топката (кръг, квадрат, триъгълник) в [Breakout игра](https://en.wikipedia.org/wiki/Breakout_(video_game)) на базата на OLED . За това Arduino приложение обаче нека просто възпроизведем визуалното преживяване на p5.js приложението. Това може да звучи трудно, но вие вече сте експерти по [OLED](../advancedio/oled.md) — можете да го направите!

Но откъде да започнем?

Ключът е да започнете просто и да изграждате приложението си стъпка по стъпка, тествайки постепенно всяка стъпка по пътя.

<!-- Когато пишете свои собствени приложения `Computer ↔ Arduino`, ще искате да проектирате двете приложения заедно. Трябва да решите как двете приложения ще комуникират по сериен порт – в този случай p5.s и Arduino – и формата на текстовите кодирани низове. Можете да започнете да реализирате проекта си или в p5.js, или в Arduino – и вероятно ще преминавате от едното към другото, докато създавате и двете. За нашия пример избрахме да започнем с p5.js ([DisplayShapeOut](https://github.com/makeabilitylab/p5js/tree/master/WebSerial/p5js/DisplayShapeOut)). Сега нека започнем да работим върху кода на Arduino. -->

#### Прост начален етап и стратегии за отстраняване на грешки

Нека започнем нашата Arduino приложение просто като отразяваме входящите данни обратно на сериен порт. Не забравяйте, че **не можете** да използвате [Serial Monitor](../arduino/serial-print.md) на Arduino IDE, след като вашето p5.js приложение се свърже с Arduino през сериен порт. Вижте съобщението за грешка на фигурата по-долу.

![](assets/images/OnlyOneProgramCanReadFromASerialPortAtATime_CannotOpenArduinoIDESerialMonitor.png)
**Фигура.** Тази фигура показва приложението p5.js [DisplayShapeOut](https://makeabilitylab.github.io/ p5js/WebSerial/p5js/DisplayShapeOut), която работи и е свързана с Arduino чрез уеб сериен порт. Вследствие на това не можем да отворим и използваме инструмента Serial Monitor (`Tools -> Serial Monitor`) на Arduino IDE, защото само една програма може да се свърже с сериен порт в даден момент. Когато опитаме, получаваме съобщение за грешка в конзолата на Arduino IDE (дясната картинка), което гласи: "Грешка при отваряне на сериен порт "COM5". (Портът е зает)".
{: .fs-1 }

Затова нека вместо това да програмираме приложението p5.js да чете входящите серийни данни и да ги отпечатва – уеб базиран Serial Monitor! За щастие, нашият p5.js [`SerialTemplate`](https:/ /github.com/makeabilitylab/p5js/tree/master/WebSerial/p5js/SerialTemplate) код вече прави това. В шаблона просто имаме:

{% highlight JavaScript %}
function onSerialDataReceived(eventSender, newData) {
console.log("onSerialDataReceived", newData);
pHtmlMsg.html("onSerialDataReceived: " + newData);
}
{% endhighlight JavaScript %}

Което отпечатва входящите данни, изпратени от Arduino към конзолата, и също така актуализира удобния HTML елемент `pHtmlMsg`, така че можете да видите информацията на вашата уеб страница (разбира се, можете да коментирате това).

Така че най-простият Arduino скиц, с който да започнете, може да бъде програма за "ехо обратно”, като:

{% highlight C++ %}
const long BAUD_RATE = 115200;
void setup() {
Serial.begin(BAUD_RATE);
}

void loop() {
// Проверява дали има входящи серийни данни
if(Serial.available() > 0){
// Отразява данните обратно на серийния порт (за целите на отстраняване на грешки)
Serial.print("Arduino Received: '");
Serial.print(rcvdSerialData);
Serial.println("'");
}
}
{% endhighlight C++ %}

**Код.** Проста програма за сериално ехо за Arduino ([EchoBackSerialIn.ino](https://github.com/makeabilitylab/arduino/blob/master/Serial/EchoBackSerialIn/EchoBackSerialIn.ino) в GitHub).
{: .fs-1 }

<!-- <script src="http://gist-it.appspot.com/https://github.com/makeabilitylab/arduino/blob/master/Serial/EchoBackSerialIn/EchoBackSerialIn.ino?footer=minimal"></script>

TODO: нужно видео -->

Тази техника с ехото е важен инструмент за отстраняване на грешки. Затова се уверете, че я разбирате! Можем да използваме и OLED дисплея, за да покажем резултатите от отстраняването на грешки, което така или иначе ни е необходимо за това приложение. Нека да го направим!

<!-- Друга полезна стратегия за отстраняване на грешки е да използваме нашите [OLED](../advancedio/oled.md) дисплеи за отстраняване на грешки. Можем да променяме тези отпечатъци за отстраняване на грешки, докато приложението ни напредва (и, разбира се, да ги премахнем, когато сме сигурни, че нещата работят по начина, по който искаме). -->

<!-- Нека добавим нашия OLED, който така или иначе ни е необходим за това приложение. -->

<!-- Важно е да разберете тази техника "echo” и факта, че вече не можете да използвате Serial Monitor за отстраняване на грешки (поне не по същия начин [като преди](../arduino/serial-print.md)), защото само една програма може да отвори и използва сериен порт едновременно (която ще бъде вашето p5.js приложение). -->

<!-- Друга стратегия за отстраняване на грешки е да използвате вашите [OLED](../advancedio/oled.md) дисплеи за отстраняване на грешки в изхода. OLED дисплеите всъщност са изключително полезни за показване на междинна информация за отстраняване на грешки, докато създавате и итерирате. Разбира се, можете да премахвате и променяте отпечатъците за отстраняване на грешки, докато приложението ви напредва.

Освен това може да е полезно просто да включите LED, за да проследите някакво състояние. Можете да направите това, без да свързвате LED, като използвате вградения LED на вашата платка (`LED_BUILTIN`). Така че, напишете `digitalWrite(LED_BUILTIN, HIGH)`, когато програмата ви влезе в някакво състояние, например.

Накрая, докато разработвате и двете приложения, може би най-важната стратегия е да модулирате и тествате, модулирате и тествате, модулирате и тествате. Изграждайте приложенията си на части и ги тествайте на всеки етап!

С това нека започнем да работим от страна на Arduino! -->

#### Проста OLED верига

Ще свържем OLED с I<sup>2</sup>C, както направихме в урока ни за [OLED](../advancedio/oled.md). За нашия урок ще използваме Arduino Leonardo, но някои от вас може да предпочетат да използват Adafruit Huzzah32 (ESP32). По-долу предоставяме и двете I<sup>2</sup>C свързвания.

##### Свързване на Arduino Leonardo

![](../advancedio/assets/images/ArduinoLeonardo_OLEDWiring_FritzingSchematics.png)
**Фигура** Свързването на Adafruit OLED дисплея с I<sup>2</sup>C изисква само четири кабела. За цветовете на кабелите използвах стандартната цветова кодировка STEMMA QT: синьо за данни (SDA), жълто за часовник (SCL), черно за заземяване (GND) и червено за захранване (5V). Имайте предвид, че I<sup>2</sup>C пиновете ще се различават в зависимост от вашата платка. Например, на Arduino Uno те са A4 (SDA) и A5 (SCL), а не цифрови пинове 2 (SDA) и 3 (SCL), както е при Leonardo.
{: .fs-1 }

##### Кабелното свързване на ESP32

![](../advancedio/assets/images/Huzzah32_OLEDWiring_FritzingSchematics.png)
**Фигура.** Схема на кабелното свързване за платка [Adafruit Huzzah32](../esp32/index.md) ESP32 с OLED. Обърнете внимание, че ESP32 има отпечатани SCL и SDA пинове в горния десен ъгъл.
{: .fs-1 }

#### Добавете OLED и отстранете printlns

Сега нека програмираме OLED да отпечата някои отстраняващи информация. Добавете следните декларации, необходими за OLED, в горната част:

{% highlight C++ %}
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

#define SCREEN_WIDTH 128 // Ширина на OLED дисплея, в пиксели
#define SCREEN_HEIGHT 64 // Височина на OLED дисплея, в пиксели

// Декларация за SSD1306 дисплей, свързан към I2C (SDA, SCL пинове)
#define OLED_RESET 4 // Пинов номер за ресет (или -1, ако се споделя пин за ресет на Arduino)
Adafruit_SSD1306 _display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);
{% endhighlight C++ %}

В `setup()`, инициализирайте OLED и отпечатайте съобщението "Waiting for serial...". Ще покажем и скоростта на предаване, която е полезна за справка, в случай че сте задали различна стойност в p5.js.

{% highlight C++ %}
const long BAUD_RATE = 115200;
void setup() {
Serial.begin(BAUD_RATE);

// SSD1306_SWITCHCAPVCC = генерира напрежение на дисплея от 3,3 V вътрешно
if(!_display.begin(SSD1306_SWITCHCAPVCC, 0x3D)) { // Адрес 0x3D за 128x64
Serial.println(F("SSD1306 allocation failed"));
for(;;); // Не продължавай, цикъл завинаги
}

_display.clearDisplay();
_display.setTextSize(1); // Нормална скала 1:1 пиксел
_display.setTextColor(SSD1306_WHITE); // Изчертаване на бял текст
_display.setCursor(0, 0); // Започнете от горния ляв ъгъл
_display.print("Изчакване на получаване на данни от сериен порт...");
_display.println("\n");
_display.print("Baud rate:");
_display.print(BAUD_RATE);
_display.print(" bps");
_display.display();
}
{% endhighlight C++ %}

Сега, в `loop()`, добавете отпечатваните от OLED отладки:

{% highlight C++ %}
void loop() {
// Проверете дали има входящи серийни данни
if(Serial.available() > 0){
// Ако сме тук, значи са получени серийни данни
// Прочетете данните от серийния порт, докато стигнете до разделителя на края на реда ("\n")
// Запишете всички тези данни в низ
String rcvdSerialData = Serial.readStringUntil("\n");
 

// Покажете данните на OLED за целите на отстраняването на грешки
_display.clearDisplay();
_display.setCursor(0, 0);
_display.setTextSize(1);
_display.println("RECEIVED:\n");
_display.setTextSize(3);
_display.println(rcvdSerialData);
_display.display();

// Отразяване на данните обратно на сериен порт (за целите на отстраняване на грешки)
Serial.print("Arduino Received: '");
Serial.print(rcvdSerialData);
Serial.println("'");
}
}
{% endhighlight C++ %}

Ето видео демонстрация на това, което имаме досега: пълното приложение DisplayShapeOut p5.js ([жива страница](https://makeabilitylab.github.io/p5js/WebSerial/p5js/DisplayShapeOut/), [код](https://github.com/makeabilitylab/p5js/tree/master/WebSerial/p5js/DisplayShapeOut)), работеща с междинна версия на [DisplayShapeSerialIn.ino](https://github.com/makeabilitylab/arduino/blob/master/Serial/ DisplayShapeSerialIn-Intermediate1/DisplayShapeSerialIn-Intermediate1.ino), която просто отразява обратно получените данни и показва някои отладки на OLED екрана.

<video autoplay loop muted playsinline style="margin:0px">
<source src="assets/videos/ DisplayShapeIn.ino-EchoBack-TrimmedAndOptimized.mp4" type="video/mp4" />
</video>
**Видео.** Тестване на C++ кода за отразяване за Arduino с приложението p5.js DisplayShapeOut ([жива страница](https://makeabilitylab.github.io/p5js/WebSerial/p5js/DisplayShapeOut/), [код](https://github.com/makeabilitylab/p5js/tree/master/WebSerial/p5js/DisplayShapeOut) ). Можете да видите тази междинна версия на DisplayShapeSerialIn.ino [тук](https://github.com/makeabilitylab/arduino/blob/master/Serial/DisplayShapeSerialIn-Intermediate1/DisplayShapeSerialIn-Intermediate1.ino).
{: .fs-1 }

#### Анализирайте серийните данни и актуализирайте OLED отладочния изход

Дотук всичко е наред!

Но сега всъщност трябва да **анализираме** входящите серийни текстови данни в полезни типизирани променливи. Нека да го направим и да актуализираме OLED-базирания ни дебъг изход. Отново, полезно е да конструираме програмата си стъпка по стъпка, като я тестваме по време на процеса.

Актуализирайте кода вътре в `if(Serial.available() > 0)` в `loop()`, за да включите анализиране. Има много възможни подходи за анализиране; обаче, ние ще се възползваме от Arduino [String](https://www.arduino.cc/reference/en/language/variables/data-types/stringobject/) и функции като [`indexOf()`](https://www.arduino.cc/reference/en/language/variables/data-types/string/functions/indexof) и [`substring()`] (https://www.arduino.cc/reference/en/language/variables/data-types/string/functions/substring), за да търсим запетаи и да анализираме данните си. Показахме подобна техника в урока [Въведение в сериалното](serial-intro.md#formatting-messages).

Засега ще покажем както суровите данни, получени по сериален начин, така и анализираните данни. След като се уверим, че всичко работи, ще премахнем този дебъг изход.

{% highlight C++ %}
String rcvdSerialData = Serial.readStringUntil("\n"); 

// Разделяне на низ, разделен със запетая
int indexOfComma = rcvdSerialData.indexOf(",");
if(indexOfComma != -1){
// Разделяне на типа на фигурата, който трябва да бъде 0 (кръг), 1 (квадрат), 2 (триъгълник)
String strShapeType = rcvdSerialData.substring(0, indexOfComma);
int shapeType = strShapeType.toInt();

// Разделяне на размера на формата, число между [0, 1]
String strShapeSize = rcvdSerialData.substring(indexOfComma + 1, rcvdSerialData.length());
float curShapeSizeFraction = strShapeSize.toFloat();

// Показване на данни за целите на отстраняване на грешки
_display.clearDisplay();
_display.setCursor(0, 0);
_display.println("RECEIVED:");
_display.println(rcvdSerialData);

// Показване на анализираните данни
_display.println("\nPARSED:");
_display.print("Shape Type: ");
_display.println(shapeType);
_display.print("Размер на формата: ");
_display.print(curShapeSizeFraction);
_display.display();
}
{% endhighlight C++ %}

Чудесно, сега нека качим това в Arduino и тестваме двете ни приложения дотук. Работи ли анализирането?

<video autoplay loop muted playsinline style="margin:0px">
<source src="assets/videos/DisplayShapeIn.ino-TestParsing-TrimmedAndOptimized.mp4" type="video/mp4" />
</video>
**Видео.* * Тестване на кода за C++ парсинг за Arduino с приложението p5.js DisplayShapeOut ([жива страница](https://makeabilitylab.github.io/p5js/WebSerial/p5js/DisplayShapeOut/), [код](https://github.com/makeabilitylab/p5js/tree/master/WebSerial/p5js/DisplayShapeOut) ). Можете да видите тази междинна версия на DisplayShapeSerialIn.ino [тук](https://github.com/makeabilitylab/arduino/blob/master/Serial/DisplayShapeSerialIn-Intermediate2/DisplayShapeSerialIn-Intermediate2.ino). 
{: .fs-1 }

#### Тестване на кода за анализиране чрез Serial Monitor

Нашата Arduino програма **не** знае откъде идват входящите данни от серийния порт. Те могат да идват от всякаква програма. Можем да използваме това в наша полза за тестване!

Нека затворим раздела p5.js в уеб браузъра си, за да се уверим, че е прекъсната връзката с Arduino. Сега отворете сериен монитор и въведете данни в него. При тестването е добре да въведете както правилно форматирани, така и неправилно форматирани данни. Не забравяйте да тествате и крайни случаи! Вижте видеото по-долу.

<video autoplay loop muted playsinline style="margin:0px">
<source src="assets/videos/DisplayShapeIn.ino-SerialMonitor-TrimmedOptimized1200w.mp4" type="video/mp4" />
</video>
**Видео.** Използване на [серийния монитор](../arduino/serial-print.md) на Arduino IDE за тестване на кода за анализиране. Използването на серийния монитор е лесен и удобен начин да тествате серийния вход и кода за анализиране на Arduino.
{: .fs-1 }

#### Напишете код за рисуване

Страхотно! Почти сме готови.

Нека преминем от четене и анализиране на сериен вход към писане на нашия код за рисуване на базата на OLED. Както споменахме по-рано, [Adafruit GFX drawing API](https://learn.adafruit.com/adafruit-gfx-graphics-library/graphics-primitives) не се различава значително от [p5js drawing API](https://p5js.org/reference/). Обърнете внимание на приликите по-долу!

Първо, нека представим някои типове и променливи, свързани с формите:

{% highlight C++ %}
// Нов енум за проследяване на типовете форми
enum ShapeType {
CIRCLE,
SQUARE,
TRIANGLE,
};

ShapeType _curShapeType = CIRCLE; // проследява текущия тип форма
float _curShapeSizeFraction = -1; // проследява текущата част от формата

const int MIN_SHAPE_SIZE = 4; // минимален размер на формата
int _maxShapeSize; // максимален размер на формата (зависи от ширината/височината на дисплея)
{% endhighlight C++ %}

Трябва също да инициализираме `_maxShapeSize` в `setup()`:

{% highlight C++ %}
void setup(){
...
_maxShapeSize = min(_display.width(), _display.height());
...
}
{% endhighlight C++ %}

Актуализирайте съответния код за анализиране, за да използвате новите глобални променливи `_curShapeType` и `_curShapeSizeFraction`. Добавете също така проверка на границите, за да се уверите, че фракцията на размера на фигурата е между [0, 1].

{% highlight C++ %}
...
if(indexOfComma != -1){
// Анализирайте типа на фигурата, който трябва да бъде 0 (кръг), 1 (квадрат), 2 (триъгълник)
String strShapeType = rcvdSerialData.substring(0, indexOfComma);
int shapeType = strShapeType.toInt();
_curShapeType = (ShapeType)shapeType;

// Разделяне на размера на формата, плаваща стойност между [0, 1]
String strShapeSize = rcvdSerialData.substring(indexOfComma + 1, rcvdSerialData.length());
_curShapeSizeFraction = strShapeSize.toFloat();

// Проверка на границите на размера на фигурата
if(_curShapeSizeFraction < 0){
_curShapeSizeFraction = 0;
}else if(_curShapeSizeFraction > 1){
_curShapeSizeFraction = 1;
}
}
...
{% endhighlight C++ %}

Сега нека добавим нашата функция `drawShape(ShapeType shapeType, float fractionSize)`, която рисува кръг, квадрат или триъгълник в зависимост от предадения `shapeType` с подходящ размер (`fractionSize`).

{% highlight C++ %}
void drawShape(ShapeType shapeType, float fractionSize){
_display.clearDisplay();

int shapeSize = MIN_SHAPE_SIZE + fractionSize * (_maxShapeSize - MIN_SHAPE_SIZE);
int halfShapeSize = shapeSize / 2;
int xCenter = _display.width() / 2;
int yCenter = _display.height() / 2;
 
int xLeft = xCenter - halfShapeSize;
int yTop = yCenter - halfShapeSize;

// Рендиране на подходящата форма
if(shapeType == CIRCLE){
_display.fillRoundRect(xLeft, yTop, shapeSize, shapeSize, halfShapeSize, SSD1306_WHITE);
}else if(shapeType == SQUARE) {
_display.fillRect(xLeft, yTop, shapeSize, shapeSize, SSD1306_WHITE);
}else if(shapeType == TRIANGLE){
int x1 = xCenter - halfShapeSize;
int y1 = yCenter + halfShapeSize;

int x2 = xCenter;
int y2 = yCenter - halfShapeSize;

int x3 = xCenter + halfShapeSize;
int y3 = y1;

_display.fillTriangle(x1, y1, x2, y2, x3, y3, SSD1306_WHITE);
}

_display.display();
}
{% endhighlight C++ %}

Накрая трябва да извикаме `drawShape()`, което ще направим в края на `loop()`:

{% highlight C++ %}
void loop() {
...

// ако няма пристигнали данни, частта от фигурата ще бъде < 0
if(_curShapeSizeFraction > 0){ 
drawShape(_curShapeType, _curShapeSizeFraction);
}
}
{% endhighlight C++ %}

Това е! Можете да видите пълната ни реализация в GitHub като [DisplayShapeSerialIn.ino](https://github.com/makeabilitylab/arduino/blob/master/Serial/DisplayShapeSerialIn/DisplayShapeSerialIn.ino).

### Пълна демонстрация от начало до край

Успяхме! Ето пълната демонстрация от начало до край.

<video autoplay loop muted playsinline style="margin:0px">
<source src="assets/videos/DisplaySerialIn-EndToEndDemo-TrimmedAndOptimized.mp4" type="video/mp4" />
</video>
**Видео.** Демонстрация на приложението p5.js [DisplayShapeOut](https://github.com/makeabilitylab/p5js/tree/master/WebSerial/p5js/DisplayShapeOut) и скица на Arduino [DisplayShapeIn.ino](https://github.com/makeabilitylab/arduino/blob/master/Serial/DisplayShapeSerialIn/DisplayShapeSerialIn.ino). Можете да разглеждате, редактирате и да си играете с кода на DisplayShapeOut в [онлайн редактора на p5.js](https://editor.p5js.org/jonfroehlich/sketches/ TfE1BjOX6) или от нашия GitHub ([жива страница](https://makeabilitylab.github.io/p5js/WebSerial/p5js/DisplayShapeOut/), [код](https://github.com/makeabilitylab/p5js/tree/master/WebSerial/p5js/DisplayShapeOut))
{: .fs-1 }

## DisplayShapeBidirectional: p5.js към Arduino и Arduino към p5.js

Горният пример демонстрира как да предавате данни от p5.js към Arduino чрез текстово кодирана серийна комуникация, но не изпраща никакви команди от Arduino към p5.js. Нека разширим кода си, за да комуникираме информация двупосочно (от p5.js към Arduino и от Arduino към p5.js)!

Отново, има много възможности, но нека не усложняваме нещата. Ще добавим два бутона от страна на Arduino, за да изберем **типа на фигурата** и **нов режим на рисуване** (запълване *vs.* контур). Можем също да променим тези променливи от страна на p5.js чрез кликване с мишката: ляв клик, за да променим типа на фигурата (същото като преди) и десен клик, за да променим режима на рисуване.

Ето един бърз поглед към това как ще изглеждат двете приложения:

<video autoplay loop muted playsinline style="margin:0px">
<source src="assets/videos/DisplayShapeBidirectional_ShortenedAndOptimized1200w.mp4" type="video/mp4" />
</video>
**Видео.** Кратка демонстрация от начало до край на приложението p5.js DisplayShapeBidirectional ([жива страница](http://makeabilitylab.github.io/p5js/WebSerial/p5js/DisplayShapeBidirectional), [код](https://github.com/makeabilitylab/ p5js/tree/master/WebSerial/p5js/DisplayShapeBidirectional)) и скицата на Arduino [DisplayShapeSerialBidirectional.ino](https://github.com/makeabilitylab/arduino/blob/master/Serial/DisplayShapeSerialBidirectional/DisplayShapeSerialBidirectional.ino).
{: .fs-1 }

Важно е да отбележим, че използваме **моментни бутони** за входа на Arduino, а не входни устройства или сензори, които поддържат физическо състояние като потенциометър, защото фиксираните физически състояния могат да се разсинхронизират с p5.js.

### Актуализиране на нашия p5.js код

За да започнете, направете копие на папката `DisplayShapeOut` p5.js и я преименувайте на нещо като `DisplayShapeBidirectional`. Сега нека добавим поддръжка за режима на рисуване, актуализираме нашето разчитане и модифицираме нашите инструкции към потребителя.

#### Добавяне на режим на рисуване с запълване/контур

За режима на рисуване с запълване *срещу* контур ще добавим допълнителна променлива за проследяване на състоянието, наречена `curShapeDrawMode`:

{% highlight JavaScript %}
let mapShapeDrawMode = {
0: "Fill",
1: "Outline",
};

let curShapeDrawMode = 0; // Запълване по подразбиране
{% endhighlight JavaScript %}

Режимът на рисуване може да се настрои или с **дясно кликване** с мишката, или от входящи данни от Arduino (от уеб сериала). Нека първо се заемем с първото (дясно кликване с мишката).

Според [документацията на p5.js](https://p5js.org/ reference/#/p5/mouseClicked), функцията `mouseClicked()` се извиква само когато левият бутон на мишката е натиснат и освободен. Следователно не можем да разчитаме на тази [`mouseClicked()`](https://p5js.org/reference/#/p5/mouseClicked) за промяна на режима на рисуване. Вместо това ще добавим проследяването на състоянието в [`mousePressed()`](https://p5js.org/reference/#/p5/mousePressed).

{% highlight JavaScript %}
function mousePressed () {
// Актуализирайте състоянията само ако сме свързани към сериен порт
if (serial.isOpen()) {
if (mouseButton == RIGHT) {
// Превключване между режим на запълване и режим на очертаване въз основа на десен клик
curShapeDrawMode++;
if (curShapeDrawMode >= Object.keys(mapShapeDrawMode).length) {
curShapeDrawMode = 0;
}
} else {
curShapeType++;
if (curShapeType >= Object.keys(mapShapeTypeToShapeName).length) {
curShapeType = 0;
}
}
serialWriteShapeData(curShapeType, curShapeSize, curShapeDrawMode);
}
}
{% endhighlight JavaScript %}

Обърнете внимание, че тук сме преместили и проследяването на `shapeType`.

#### Добавете нови инструкции за потребителя

В `draw()` актуализирайте инструкциите за потребителя, за да включите информация както за кликване с левия, така и за кликване с десния бутон на мишката:

{% highlight JavaScript %}
function draw(){
...

// Някои инструкции за потребителя
noStroke();
fill(255);
const tSize = 14;
let strInstructions = "";
if (serial.isOpen()) {
strInstructions = "Кликнете с левия бутон, за да промените формата. Кликнете с десния бутон, за да промените запълването/контура";
} else {
strInstructions = "Кликнете където и да е, за да се свържете със сериала"
}
textSize(tSize);
let tWidth = textWidth(strInstructions);
const xText = width / 2 - tWidth / 2;
text(strInstructions, xText, height - tSize + 6);
}
{% endhighlight JavaScript %}

#### Актуализирайте функцията serialWriteShapeData и извикващите я

Трябва също да актуализираме функцията `serialWriteShapeData()`, за да приема и записва три променливи: `shapeType`, `shapeSize` и `shapeDrawMode`, вместо две, както преди:

{% highlight JavaScript %}
async function serialWriteShapeData(shapeType, shapeSize, shapeDrawMode) {
if (serial.isOpen()) {
let shapeSizeFraction = (shapeSize - MIN_SHAPE_SIZE) / (maxShapeSize - MIN_SHAPE_SIZE);

// Настройка на strData с три променливи, разделени със запетая
let strData = shapeType + ", " + nf(shapeSizeFraction, 1, 2) + ", " + shapeDrawMode;

// Записване на данните в сериен порт
serial.writeLine(strData);
}
}
{% endhighlight JavaScript %}

И не забравяйте да актуализирате и извикването `serialWriteShapeData()` в `mouseMoved()`, за да използвате също три параметъра:

{% highlight JavaScript %}
function mouseMoved() { {
...
serialWriteShapeData(curShapeType, curShapeSize, curShapeDrawMode);
...
}
{% endhighlight JavaScript %}

#### Добавете код за анализиране на onSerialDataReceived

Накрая, трябва да добавим код, който анализира входящите серийни данни в `shapeType`, `shapeSize` и `shapeDrawMode`. За целта ще добавим нов аспект към нашия протокол за комуникация `Arduino → Компютър`. Да приемем, че всеки ред текст, предаден с префикс `#`, ще бъде игнориран и считан за отладочен изход. По този начин можем да продължим да използваме нашата p5. js уеб приложението за отстраняване на грешки в изхода, като същевременно продължаваме да анализираме полезна информация.

Припомнете си, че нашата уеб серийна библиотека има събитие, наречено `SerialEvents.DATA_RECEIVED`, за което се абонираме в `setup()` и свързваме метод, наречен `onSerialDataReceived(newData)`:

{% highlight JavaScript %}
function setup() {
...
serial.on(SerialEvents.DATA_RECEIVED, onSerialDataReceived);
...
}
{% endhighlight JavaScript %}

Сега нека актуализираме метода `onSerialDataReceived`!

{% highlight JavaScript %}
function onSerialDataReceived(eventSender, newData) {
//console.log("onSerialDataReceived", newData);
pHtmlMsg.html("onSerialDataReceived: " + newData);

// Проверете дали получените данни започват с "#". Ако е така, игнорирайте ги
// В противен случай, анализирайте ги! Игнорираме редовете, които започват с "#"
if (!newData.startsWith("#")) {
// Форматът на данните е ShapeType, ShapeDrawMode
const indexOfComma = newData.indexOf(",");
if (indexOfComma != -1) {
let strShapeType = newData.substring(0, indexOfComma).trim();
let strShapeDrawMode = newData.substring(indexOfComma + 1, newData.length).trim();
let newShapeType = parseInt(strShapeType);
let newShapeDrawMode = parseInt(strShapeDrawMode);

// Ако данните са валидни, задайте нов тип форма
if (newShapeType in mapShapeTypeToShapeName) {
curShapeType = newShapeType;
}

// ако режимът на рисуване на формата е валиден, задайте нов режим на рисуване
if (newShapeDrawMode in mapShapeDrawMode) {
curShapeDrawMode = newShapeDrawMode;
}
}
}
}
{% endhighlight JavaScript %}

И това е всичко! Ето пълната ни реализация като [DisplayShapeBidirectional](https://github.com/makeabilitylab/p5js/tree/master/WebSerial/p5js/ DisplayShapeBidirectional) в GitHub ([жива страница тук](http://makeabilitylab.github.io/p5js/WebSerial/p5js/DisplayShapeBidirectional)).

### Актуализиране на нашия Arduino код и верига

Сега преминаваме към Arduino. Да добавим два бутона към нашата Arduino верига: един бутон за преминаване през различните типове фигури и друг за преминаване през различните режими на рисуване. Ще ги свържем съответно към GPIO пинове 4 и 5 с вътрешни пул-ъп резистори.

![](assets/images/ArduinoLeonardo_OLED_TwoButtons.png)
**Фигура.** Веригата Arduino Leonardo с два бутона, свързани към пинове 4 и 5, използвайки вътрешните pull-up резистори на Arduino. По подразбиране те са в състояние `HIGH` и ще бъдат превключени в състояние `LOW` при натискане на бутона.
{: .fs-1 }

#### Добавяне на поддръжка на режим на рисуване

За кода, нека започнем с добавяне на поддръжка на режим на рисуване:

{% highlight C++ %}
enum DrawMode{
FILL,
OUTLINE,
NUM_DRAW_MODES
};

DrawMode _curDrawMode = FILL;
{% endhighlight C++ %}

И актуализирайте функцията `drawShape()`, за да приема три променливи и да рисува фигурите съответно (или **запълнени**, или като **контури**):

{% highlight C++ %}
void drawShape(ShapeType shapeType, float fractionSize, DrawMode curDrawMode){
_display.clearDisplay();

int shapeSize = MIN_SHAPE_SIZE + fractionSize * (_maxShapeSize - MIN_SHAPE_SIZE);
int halfShapeSize = shapeSize / 2;
int xCenter = _display.width() / 2;
int yCenter = _display.height() / 2;
int xLeft = xCenter - halfShapeSize;
int yTop = yCenter - halfShapeSize;

if(shapeType == CIRCLE){
if(curDrawMode == FILL){
_display.fillRoundRect(xLeft, yTop, shapeSize, shapeSize, halfShapeSize, SSD1306_WHITE);
}else{
_display.drawRoundRect(xLeft, yTop, shapeSize, shapeSize, halfShapeSize, SSD1306_WHITE);
}
}else if(shapeType == SQUARE){
if(curDrawMode == FILL){
_display.fillRect(xLeft, yTop, shapeSize, shapeSize, SSD1306_WHITE);
}else{
_display.drawRect(xLeft, yTop, shapeSize, shapeSize, SSD1306_WHITE);
}
}else if(shapeType == TRIANGLE){
int x1 = xCenter - halfShapeSize;
int y1 = yCenter + halfShapeSize;

int x2 = xCenter;
int y2 = yCenter - halfShapeSize;

int x3 = xCenter + halfShapeSize;
int y3 = y1;

if(curDrawMode == FILL){
_display.fillTriangle(x1, y1, x2, y2, x3, y3, SSD1306_WHITE);
}else{
_display.drawTriangle(x1, y1, x2, y2, x3, y3, SSD1306_WHITE);
}
}

_display.display();
}
{% endhighlight C++ %}

### Добавете поддръжка за бутони

Добавете нов метод, наречен `checkButtonPresses()`, който чете двата бутона, задава глобалните променливи `_curShapeType` и `_curDrawMode` съответно и ги изпраща по сериен порт.

{% highlight C++ %}
void checkButtonPresses(){
// Прочетете бутона за избор на форма (активен LOW)
int shapeSelectionButtonVal = digitalRead(SHAPE_SELECTION_BUTTON_PIN);
int lastShapeType = _curShapeType;
if(shapeSelectionButtonVal == LOW && shapeSelectionButtonVal != _lastShapeSelectionButtonVal){
// Увеличаване на типа на фигурата
_curShapeType = (ShapeType)((int)_curShapeType + 1);

// Върни обратно към CIRCLE, ако сме стигнали до NUM_SHAPE_TYPES
if(_curShapeType >= NUM_SHAPE_TYPES){
_curShapeType = CIRCLE;
}
}

// Прочети бутона за режим на рисуване на фигура val (активен LOW)
int shapeDrawModeButtonVal = digitalRead(SHAPE_DRAWMODE_BUTTON_PIN);
int lastDrawMode = _curDrawMode;
if(shapeDrawModeButtonVal == LOW && shapeDrawModeButtonVal != _lastDrawModeButtonVal){
// Увеличаване на режима на рисуване
_curDrawMode = (DrawMode)((int)_curDrawMode + 1);

// Върни обратно към FILL, ако сме стигнали до NUM_DRAW_MODES
if(_curDrawMode >= NUM_DRAW_MODES){
_curDrawMode = FILL;
}
}

// Изпрати нов тип форма и режим на рисуване на формата обратно през сериен порт
if(lastShapeType != _curShapeType || lastDrawMode != _curDrawMode){
Serial.print(_curShapeType);
Serial.print(", ");
Serial.println(_curDrawMode);
}

// Задайте стойностите на последния бутон (така че нищо да не се случи, ако потребителят просто задържи бутона натиснат)
_lastShapeSelectionButtonVal = shapeSelectionButtonVal;
_lastDrawModeButtonVal = shapeDrawModeButtonVal;
}
{% endhighlight C++ %}

Можем да тестваме новия бутон и кода за рисуване, независимо от сериен вход. Нека да го направим сега:

<video autoplay loop muted playsinline style="margin:0px">
<source src="assets/videos/DisplayShapeBidirectionalIntermediate-TrimmedAndOptimized.mp4" type="video/mp4" />
</video>
**Видео.** Тестване на междинна версия на нашия Arduino код (в GitHub [тук](https://github.com/makeabilitylab/arduino/blob/master/Serial/DisplayShapeSerialBidirectional-Intermediate1/DisplayShapeSerialBidirectional-Intermediate1.ino)).
{: .fs-1 }

### Актуализиране на кода за анализиране, за да поддържа режим на рисуване

Накрая, трябва да актуализираме кода за серийно анализиране, за да анализира три стойности, разделени със запетая, а не само две: `shapeType`, `shapeSizeFraction` и `drawMode`. Нека преместим целия този сериен код в собствена функция, наречена `checkAndParseSerial()`:

{% highlight C++ %}
void checkAndParseSerial() {
// Проверете дали има входящи серийни данни
if(Serial.available() > 0){
// Ако сме тук, значи са получени серийни данни
// Прочетете данните от серийния порт, докато стигнете до разделителя на края на реда ("\n")
// Запишете всички тези данни в низ
String rcvdSerialData = Serial.readStringUntil("\n");
 

// Разделяме низът, разделен със запетая
int startIndex = 0;
int endIndex = rcvdSerialData.indexOf(",");
if(endIndex != -1){
// Разделяме типа на фигурата, който трябва да е 0 (кръг), 1 (квадрат), 2 (триъгълник)
String strShapeType = rcvdSerialData.substring(startIndex, endIndex);
int shapeType = strShapeType.toInt();
_curShapeType = (ShapeType)shapeType;

// Разделяне на фракцията на размера на формата, число между [0, 1]
startIndex = endIndex + 1;
endIndex = rcvdSerialData.indexOf(",", startIndex);
String strShapeSize = rcvdSerialData.substring(startIndex, endIndex);
_curShapeSizeFraction = strShapeSize.toFloat();

if(_curShapeSizeFraction < 0){
_curShapeSizeFraction = 0;
}else if(_curShapeSizeFraction > 1){
_curShapeSizeFraction = 1;
}

// Разделяне на режима на рисуване 0 (запълване), 1 (контур)
startIndex = endIndex + 1;
endIndex = rcvdSerialData.length();
String strDrawMode = rcvdSerialData.substring(startIndex, endIndex);
int drawMode = strDrawMode.toInt();
_curDrawMode = (DrawMode)drawMode;
}

// Отразяване на данните обратно на сериен порт (за целите на отстраняване на грешки)
// Представяне на отстраняването на грешки с "#" като конвенция
Serial.print("# Arduino Received: "");
Serial.print(rcvdSerialData);
Serial.println(""");
}
}
{% endhighlight C++ %}

И сега пълният `loop()` изглежда така:

{% highlight C++ %}
void loop() {
checkAndParseSerial();
checkButtonPresses();

// Ако сме получили данни от сериен порт, тогава _curShapeSizeFraction вече
// няма да бъде -1
if(_curShapeSizeFraction >= 0){
drawShape(_curShapeType, _curShapeSizeFraction, _curDrawMode);
}
}
{% endhighlight C++ %}

Успяхме! По-долу предоставяме линкове към пълния код и видео демонстрация.

### Видео на DisplayShapeBidirectional

Ето видео демонстрация на DisplayShapeBidirectional ([жива страница](http://makeabilitylab.github.io/p5js/WebSerial/p5js/DisplayShapeBidirectional), [код](https://github.com/makeabilitylab/p5js/ tree/master/WebSerial/p5js/DisplayShapeBidirectional)) и скицата на Arduino [DisplayShapeSerialBidirectional.ino](https://github.com/makeabilitylab/arduino/blob/master/Serial/DisplayShapeSerialBidirectional/DisplayShapeSerialBidirectional.ino).

<video autoplay loop muted playsinline style="margin:0px">
<source src="assets/videos/DisplayShapeBidirectional_TrimmedAndOptimized900w.mp4" type="video/mp4" />
</video>
**Видео.** Демонстрация на приложението p5.js DisplayShapeBidirectional ([жива страница](http://makeabilitylab.github.io/p5js/WebSerial/p5js/DisplayShapeBidirectional), [код](https://github.com/makeabilitylab/p5js/tree/master/WebSerial/p5js/ DisplayShapeBidirectional)) и скицата на Arduino [DisplayShapeSerialBidirectional.ino](https://github.com/makeabilitylab/arduino/blob/master/Serial/DisplayShapeSerialBidirectional/DisplayShapeSerialBidirectional.ino).
{: .fs-1 }

## Дейност

За вашите дневници за прототипиране създайте проста двупосочна апликация в p5.js и Arduino. В идеалния случай тази апликация би съответствала на вашата идея за MP3, което ви позволява бързо да създадете прототип на концепцията. В дневника си опишете апликацията, добавете линк към кода (за p5.js и Arduino) и включете кратко видео.

<!-- разширете приложението p5.js DisplayShapeBidirectional ([жива страница](http://makeabilitylab.github.io/p5js/WebSerial/p5js/DisplayShapeBidirectional), [код](https://github.com/makeabilitylab/p5js/tree/master/WebSerial/p5js/ DisplayShapeBidirectional)) и скицата на Arduino [DisplayShapeSerialBidirectional.ino](https://github.com/makeabilitylab/arduino/blob/master/Serial/DisplayShapeSerialBidirectional/DisplayShapeSerialBidirectional.ino) -->

## Следващ урок

В [следващия урок](p5js-paint-io.md) ще съберем всичко заедно и ще създадем напълно функционално приложение за рисуване.

<span class="fs-6">
[Предишен: p5.js Serial In](p5js-serial.md){: .btn .btn-outline }
[Следващ: Пример за Paint I/O](p5js-paint-io.md){: .btn .btn-outline }
</span>

<!-- <span class="fs-6">
[Предишен: Въведение в Web Serial](web-serial.md){: .btn .btn-outline }
[Следващо: Serial I/O с p5.js](p5js-serial-io.md){: .btn .btn-outline }
</span> -->

<!-- Други идеи за p5js приложения:
- използвайте p5.js sound API и покажете звук в реално време
- анализирайте времето в Сиатъл и го покажете на OLED? -->

<!-- - Покажете как компютърът комуникира с Arduino
- Покажете проста двупосочна комуникация
- Направете проста програма за рисуване
-- Първо, два потенциометра като вход. Сега нека ги превключим на ускорение
-- След това можем да контролираме размера на четката с FSR
---- Когато не е натиснат, покажете като кръстосана линия или нещо подобно
-- Контролирайте "изчистването” на дисплея с бутон
-- Контролирайте цвета с цветен сензор

Друг пример:
- Един пример може да бъде използването на звуков вход p5.js, за да се направи FFT или просто OLED изход с величина -->
