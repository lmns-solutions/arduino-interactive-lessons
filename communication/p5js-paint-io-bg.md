---
lang: bg
permalink: /communication/p5js-paint-io.html
page_id: communication-p5js-paint-io
layout: default
title: L5&#58; Пример за PaintIO
nav_order: 5
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

В последните няколко урока научихме за [серийната комуникация](serial-intro.md), [уеб серийната комуникация](web-serial.md) и използването на серийната комуникация за създаване на [p5.js](https://p5js.org/) + Arduino приложения ([първи урок](p5js-serial.md), [втори урок](p5js-serial-io.md)). В този урок ще надградим нашите знания и съществуващия код, за да създадем пълно приложение p5.js + Arduino, което ще наречем ** PaintIO**. PaintIO включва персонализиран контролер "четка” с OLED дисплей, който контролира и комуникира двупосочно с персонализирано приложение за рисуване в p5.js.

<video autoplay loop muted playsinline style="margin:0px">
<source src="assets/videos/PaintIO2-JustAHeart-TrimmedAndOptimized.mp4" type="video/mp4" />
</video>
**Видео.** Кратка демонстрация на един контролер PaintIO, използващ 3-осев акселерометър LIS3DH за настройка на местоположението на четката, скоростта на четката за настройка на цвета, резистор, чувствителен към сила, за настройка на размера на четката, и три бутона за промяна на формата на четката, запълване *vs. * контура и за изчистване на рисунката. Контролерът също така показва текущите свойства на четката, като размер, форма и местоположение на OLED. Кодът на Arduino е в нашия GitHub като [PaintIOAccel.ino](https://github.com/makeabilitylab/arduino/blob/master/Serial/PaintIOAccel/PaintIOAccel.ino). Приложението p5.js е тук: [жива страница](https://makeabilitylab.github.io/p5js/WebSerial/p5js/PaintIO), [код](https://github.com/makeabilitylab/p5js/tree/master/WebSerial/p5js/PaintIO).
{: .fs-1 }

Приложението за рисуване е чудесен пример за физическо програмиране и ни помага да обобщим наученото досега, защото:
- Има много **различни свойства на боята, които могат да се контролират**, като размер на четката, скорост, цвят, форма
- Можем да **изследваме** и **играем** с различни видове **сензори** и **хардуер** **вход**, за да контролираме тези свойства
- Рисуването е **открито творческо** и **богато занимание** – има много малко правила! А нашата персонализирана хардуерна четка може да повлияе директно на *начина*, по който боядисваме и *какво* боядисваме. От гледна точка на дизайна на взаимодействието, това е вълнуващо и забавно!
- Накрая, както вече видяхме, създаването на приложение за рисуване в p5.js е **доста лесно** (и забавно)! Но как можем да го направим още по-интересно с Arduino и персонализиран вход?

Преди това създадохме това [просто приложение за рисуване](https://editor.p5js.org/jonfroehlich/embed/MSGdVYUle) само с около 20 реда код (Впечатляващо! Демонстрира силата на p5.js). В това приложение размерът на четката се променя пропорционално според скоростта на мишката, цветът се съпоставя с x координатите на мишката и можете да кликнете с мишката, за да превключвате между запълване *и* контур. Играйте с него по-долу!

<iframe width="736" height="400" scrolling="no" src="https://editor.p5js.org/jonfroehlich/embed/MSGdVYUle"></iframe>
**Код.** Проста програма за рисуване p5.js с около 20 реда код. Можете да я видите, редактирате и играете с нея [тук](https://editor.p5js.org/jonfroehlich/sketches/MSGdVYUle) чрез онлайн редактора p5.js. В този урок ще разширим този пример, за да включим [уеб сериал](web-serial.md) и персонализиран контролер "четка".
{: .fs-1 }

В този урок ще надградим този пример, но с персонализиран контролер "четка” и различни взаимодействия за настройка на свойствата на четката. Ще научите как да модулирате и бавно да изграждате p5.js + Arduino приложение, как да рисувате, използвайки [offscreen buffers](https://p5js.org/reference/#/p5/createGraphics), как да използвате [keyboard](https://p5js.org/reference/# /p5/keyPressed) за взаимодействие и как да мислите и проектирате протоколи за комуникация на ниво приложение между p5.js и Arduino.

## Изисквания за дизайна на PaintIO

Първо, нека определим някои изисквания за дизайна на PaintIO. Приложението трябва:

- Да има **двупосочна комуникация** между Arduino и p5.js приложението. Докато Arduino трябва да служи като основен вход за рисуване, ние трябва да можем да променяме настройките в p5.js, което трябва да се отрази незабавно на контролера

- Като минимум, контролерът на четката, базиран на Arduino, трябва да контролира **x,y местоположението**, **размера**, **формата** и **режима на запълване** (запълване срещу контур) на четката. Тези свойства трябва да ви звучат познати – ще надграждаме директно върху предишните ни уроци!

- Контролерът на четката трябва да включва и **OLED**, за да предоставя обратна връзка на художника ни за четката. Ние се интересуваме от взаимодействието между два екрана и основни/вторични дисплеи, както Nintendo експериментира с [Wii U](https://en.wikipedia.org/wiki/Wii_U).

### Серийна комуникация

Нека уточним как ще отговорим на тези изисквания, използвайки серийна комуникация.

#### От Arduino към p5.js

От Arduino към p5.js ще предаваме низ, разделен със запетая, като: `xPosFrac, yPosFrac, sizeFrac, brushType, brushFillMode`, където:
- `xPosFrac` е число с плаваща запетая между [0, 1] включително, представляващо x позицията на четката
- `yPosFrac` е число с плаваща запетая между [0, 1] включително, представляващо y позицията на четката
- `sizeFrac` е число между [0, 1] включително, представляващо размера на четката
- `brushType` е или 0, 1, 2, съответстващо на CIRCLE, SQUARE, TRIANGLE
- `brushFillMode` е или 0, 1, съответстващо на FILL, OUTLINE

Ще "отразяваме” получените данни за целите на отстраняването на грешки. Ще поставяме пред тези отражения префикс `#`, както направихме в [предходния урок](p5js-serial-io.md#add-onserialdatareceived-parsing-code), за да покажем на приложението p5.js, че тези редове са за отстраняване на грешки. 

#### От p5.js към Arduino

Тъй като приложението ни ще бъде двупосочно, ще обменяме информация и от p5.js към Arduino. За целта ще използваме примера [DisplayShapeBidirectionl](p5js-serial-io.md#displayshapebidirectional -p5js-to-arduino-and-arduino-to-p5js) от предишния урок и ще предаваме низ, разделен със запетая, от `brushType, brushFillMode`, където отново:
- `brushType` е 0, 1, 2, съответстващо на CIRCLE, SQUARE, TRIANGLE
- `brushFillMode` е или 0, 1, съответстващо на FILL, OUTLINE

## PaintIO 1: Първоначално приложение p5.js

Както обикновено, нека започнем с основен прототип и да го разширяваме. Първо, нека направим основно приложение за рисуване p5.js без никаква зависимост от Arduino.

### Копирайте SerialTemplate и създайте начална структура на PaintIO

Започнете с копиране на [`SerialTemplate`](https://github.com/makeabilitylab/p5js/tree/master/WebSerial/p5js/SerialTemplate). Ако използвате VSCode, копирайте [`SerialTemplate`](https://github.com/makeabilitylab/p5js/tree/master/WebSerial/p5js/SerialTemplate) и преименувайте папката на `PaintIO`. Ако използвате онлайн редактора p5.js, просто отворете този проект, [Serial Template](https://editor.p5js.org/jonfroehlich/sketches/vPfUvLze_C), и преименувайте проекта си на `PaintIO`.

В `sketch.js` превъртете надолу и премахнете следното. Ще използваме различен подход за свързване към сериен порт.

{% highlight JavaScript %}
function mouseClicked() {
if (!serial.isOpen()) {
serial.connectAndOpen(null, serialOptions);
}
}
{% endhighlight JavaScript %}

Също така коментирайте тази линия код в `setup()`, която се опитва да се свърже автоматично с предварително одобрени серийни устройства:

{% highlight JavaScript %}
// serial.autoConnectAndOpenPreviouslyApprovedPort(serialOptions);
{% endhighlight JavaScript %}

Засега искаме да игнорираме всичко, свързано със сериен порт.

### Добавете и инициализирайте променливи за рисуване

За кода за рисуване ще използваме подобни променливи и код за рисуване от [DisplayShapeBidirectional](https://github.com/makeabilitylab/p5js/tree/master/WebSerial/p5js/DisplayShapeBidirectional) в [предходния урок](p5js-serial-io. md#displayshapebidirectional-p5js-to-arduino-and-arduino-to-p5js). Но ще го създадем наново.

Добавете следните глобални променливи, които включват текущите `brushType`, `brushSize`, `brushFillMode`, `brushColor` и местоположението на четката (`brushX`, `brushY`). Освен това, вместо да рисуваме директно върху платното, ще използваме графичен буфер извън екрана, наречен `offscreenGfxBuffer` — така че декларирайте и него. Ще говорим повече за това по-нататък. 

{% highlight JavaScript %}
let mapBrushTypeToShapeName = {
0: "Circle",
1: "Square",
2: "Triangle"
};

let mapBrushFillMode = {
0: "Fill",
1: "Outline",
};

const MAX_BRUSH_SIZE = 150; // максималният размер на четката

let brushType = 0; // Circle като подразбиращо се
let brushFillMode = 0; // Fill като подразбиращо се
let brushSize = 50; // Начален размер на четката
let brushX = 0; // Текущо местоположение на четката по ос Х (в пикселни координати)
let brushY = 0; // текущо местоположение на четката по ос Y (в пикселни координати)
let brushColor; // текущ цвят на четката

let lastBrushX = 0; // последно местоположение на четката по ос X (подобно на pmouseX, но за четката)
let lastBrushY = 0; // последно местоположение на четката по ос Y (подобно на pmouseY, но за четката)

let showInstructions = true; // Ако е true, показва инструкциите на приложението на екрана

// Ще рисуваме в графичен буфер извън екрана
// Виж: https://p5js.org/reference/#/p5/createGraphics
let offscreenGfxBuffer;
{% endhighlight JavaScript %}

Тъй като не можем да използваме никакви конструкции или функции на p5.js, докато не бъде извикана `setup()`, трябва да инициализираме `brushColor` и `offscreenGfxBuffer` в `setup()`. Ако се опитаме да ги инициализираме при декларацията, онлайн редакторът на p5.js е достатъчно умен, за да забележи това и да ни подскаже за проблема:

```
🌸 p5.js казва: Има грешка, защото "color” не е дефинирано в текущия обхват (на ред 116 в about:srcdoc [about:srcdoc:116:18]).

Ако сте го дефинирали в кода си, трябва да проверите обхвата, правописа и регистъра (JavaScript е чувствителен към регистър). За повече информация:
https://p5js.org/examples/data-variable-scope.html
https://developer.mozilla.org/docs/Web/JavaScript/Reference/Errors/Not_Defined#What_went_wrong
 
Опитахте ли да използвате функцията color() на p5.js? Ако да, може да искате да я преместите във функцията setup() на скицата си.

За повече подробности вижте: https://github.com/processing/p5.js/wiki/p5.js-overview#why-cant-i-assign-variables-using-p5-functions-and-variables-before-setup
 
```

![](assets/images/p5jsOnlineEditor_TryingToUseP5jsFunctionsBeforeSetup.png)
**Фигура.* * Не можете да използвате никакви функции или класове на p5.js, преди да бъде извикана `setup()`. Ако го направите, вероятно ще получите грешка като горната, където се опитахме да използваме [`color()`](https://p5js.org/reference/#/p5/color) по време на декларация на глобална променлива. Конкретната грешка гласи: " Опитахте ли да използвате функцията color() на p5.js? Ако да, може да искате да я преместите във функцията setup() на вашия скиц. За повече подробности вижте [p5.js wiki](https://github.com/processing/p5.js/wiki/p5.js-overview# why-cant-i-assign-variables-using-p5-functions-and-variables-before-setup)"
{: .fs-1 }

Затова, вместо това, инициализирайте ги в `setup()`:

{% highlight JavaScript %}
function setup() {
...
// Инициализирайте цвета на четката до ~бял с ~20% непрозрачност (50/255 е 19,6%)
brushColor = color(250, 250, 250, 50);

// Вместо да съхраняваме отделни мазки + свойства на боята в
// структура от данни, просто рисуваме веднага в буфер извън екрана
// и след това показваме този буфер извън екрана при всяко извикване на рисуване
// Вижте: https://p5js.org/reference/#/p5/createGraphics
offscreenGfxBuffer = createGraphics(width, height);
offscreenGfxBuffer.background(100);
}
{% endhighlight JavaScript %}

Функцията [`createGraphics()`](https://p5js.org/reference/#/p5/createGraphics) ни позволява да създадем нов буфер за графики извън екрана. Функцията връща нов обект [p5.Renderer](https://p5js.org/reference/#/p5.Renderer), който има същия API за рисуване като основния p5.js. Така че, ако искаме да зададем фона на буфера извън екрана, ще напишем `offscreenGfxBuffer.background(100);`. Ако искаме да нарисуваме червен кръг с координати `10, 10` и диаметър 50 на буфера извън екрана, ще напишем: 

{% highlight JavaScript %}
offscreenGfxBuffer.fill(255, 0, 0); // задаване на цвета на запълване в графичния контекст извън екрана на червено
offscreenGfxBuffer.circle(10, 10, 50); // рисуване на кръга в буфера извън екрана.
{% endhighlight JavaScript %}

И така нататък. Можем да направим буфера извън екрана с всякакъв размер, но в този случай искаме той да е със същия размер като платното ни, затова предаваме `ширината` и `височината` на платното в извикването `createGraphics()`.

### Добавете код за рисуване

В метода `draw()` ще нарисуваме четката върху буфера извън екрана и след това ще нарисуваме този буфер върху платното.

{% highlight JavaScript %}
function draw() {
// Нарисувайте текущия щрих на четката на дадената позиция x, y
// Но не рисуваме върху платното, а върху offscreenGfxBuffer
drawBrushStroke(mouseX, mouseY);

// Нарисувайте буфера извън екрана върху екрана
image(offscreenGfxBuffer, 0, 0);
}
{% endhighlight JavaScript %}

Очевидно е, че трябва да добавим и метода `drawBrushStroke()`, който би трябвало да ви е познат и разбираем от [предишните уроци](p5js-serial-io.md). Единствената разлика е, че рисуваме върху буферния обект извън екрана `offscreenGfxBuffer`. 

{% highlight JavaScript %}
function drawBrushStroke(xBrush, yBrush){
// задаване на настройките за запълване и контур на четката
if (brushFillMode == 0) { // brushFillMode 0 е запълване
offscreenGfxBuffer.fill(brushColor);
offscreenGfxBuffer.noStroke();
} else { // brushFillMode 0 е контур
offscreenGfxBuffer.stroke(brushColor);
offscreenGfxBuffer.noFill();
}

// нарисувай конкретната форма на четката в зависимост от brushType
let xCenter = xBrush;
let yCenter = yBrush;
let halfShapeSize = brushSize / 2;
switch (brushType) {
case 0: // нарисувай кръг
offscreenGfxBuffer.circle(xCenter, yCenter, brushSize);
break;
случай 1: // нарисувай квадрат
// Нарисувай правоъгълник въз основа на координатите на центъра
offscreenGfxBuffer.rectMode(CENTER);
offscreenGfxBuffer.square(xCenter, yCenter, brushSize);
break;
случай 2: // нарисувай триъгълник
let x1 = xCenter - halfShapeSize;
let y1 = yCenter + halfShapeSize;

let x2 = xCenter;
let y2 = yCenter - halfShapeSize;

let x3 = xCenter + halfShapeSize;
let y3 = y1;

offscreenGfxBuffer.triangle(x1, y1, x2, y2, x3, y3)
}
}
{% endhighlight JavaScript %}

### Защо да използваме буфер извън екрана?

Но **защо** използваме буфер извън екрана? Заради простотата и скоростта на рендиране!

Накратко, използването на буфер извън екрана ни позволява да рендерираме отделни щрихи само веднъж и все пак да рисуваме върху тях, като инструкции на екрана, курсор с кръстосани линии и *т.н.*

<!-- Ще поставим цялото рендериране, свързано с "рисуването”, в буфера извън екрана и все пак ще можем да рисуваме върху него, като инструкции на екрана, курсор с кръстосани линии и *т.н.* -->

Често се използват извън екранни графични (или кадърни) буфери в кода за игри и визуализация, защото ни позволяват да рисуваме изчислително сложни обекти веднъж – в буфер – и след това просто да рендерираме този буфер, когато имаме нужда от този обект отново. Един пример е този [визуализатор на звук] (https://editor.p5js.org/jonfroehlich/sketches/d2euV09i) изчислява в реално време звуковата обработка на входящите данни от микрофона и рисува различни визуализации в реално време, включително превъртащи се вълнови форми и спектрограми – и двете рендерират звуковите данни за даден буфер със звукови проби веднъж и само веднъж в графичен буфер извън екрана и след това просто добавят нови графики към този буфер с течение на времето.

В нашия случай бихме могли да създадем структура от данни – да речем клас `PaintStroke`, който приема позиция x, y, цвят на четката и всички други свойства, свързани с четката – за да съхраняваме отделни мазки в масив. За всяка нова операция с боя (*т.е.* всеки нов нарисуван кръг, квадрат или триъгълник) бихме създали съответния обект `PaintStroke` и бихме го съхранили в този масив. След това, при всяко ново извикване на `draw()`, бихме итерирали през тези обекти `PaintStroke` и бихме изпълнили съответните p5. js. С нарастването на броя на щрихите обаче скоростта на рендиране ще намалее! А е неефективно да прерисуваме едно и също щрих отново и отново. Затова вместо това рисуваме всяка операция с боя веднъж и само веднъж в буфера извън екрана!

Имайте предвид, че проследяването и съхраняването на обекти `PaintStroke` **не** е взаимно изключващо се с използването на буфер извън екрана за рендиране. Все пак можем да направим това, за да поддържаме операции като отмяна/повторение, промяна на предишни щрихи и т.н. (а ако го направим, операцията отмяна/повторение ще ни накара да преминаваме през всички `PaintStrokes` и да ги прерисуваме).

<!-- Можем също да имаме много едновременни графични буфери извън екрана и след това да използваме различни алгоритми за смесване, за да ги комбинираме. -->

<!-- 

Това е просто лесен подход за нас да "съхраняваме” всички операции по рисуване, които потребителят е извършил до момента. Като алтернатива можем да създадем структура от данни – например клас `PaintStroke`, който приема позиция x, y, цвят на четката и всички други свойства, свързани с четката – за да съхраняваме отделните щрихи в масив. За всяка нова операция по рисуване (*т.е.* всеки нов нарисуван кръг, квадрат или триъгълник) ще създаваме съответния обект `PaintStroke` и ще го съхраняваме в този масив. След това, при всяко ново извикване на `draw()`, бихме итерирали през тези `PaintStroke` обекти и бихме изпълнили съответните p5.js операции по рисуване. Този обектно-ориентиран подход има много предимства: можете да поддържате отмяна/повторение (чрез премахване на части от масива), можете да "променяте" предишни щрихи и т.н. Всъщност, със сигурност можете да комбинирате и двата подхода – те не се изключват взаимно. -->

### Добавете инструкции на екрана

Тъй като използваме този графичен буфер извън екрана, е лесно да нарисуваме "слой" върху рисунката на потребителя с други графики – в този случай инструкции за потребителя. Важно е, че за разлика от щрихите, ние **не** рисуваме тези инструкции в буфера извън екрана, а директно върху платното.

{% highlight JavaScript %}
function drawInstructions(){
// Някои инструкции за потребителя
noStroke();
fill(255);
let tSize = 10;

textSize(tSize);
let yText = 2;
let yBuffer = 1;
let xText = 3;
text("KEYBOARD COMMANDS", xText, yText + tSize);
yText += tSize + yBuffer;
text(""i" : Show/hide instructions", xText, yText + tSize);

yText += tSize + yBuffer;
text(""l" : Изчисти екрана", xText, yText + tSize);

yText += tSize + yBuffer;
let strBrushType = ""b" : Задай тип четка (" + mapBrushTypeToShapeName[brushType] + ")";
text(strBrushType, xText, yText + tSize);

yText += tSize + yBuffer;
let strToggleFillMode = ""f" : Превключване на режим на запълване (" + mapBrushFillMode[brushFillMode] + ")";
text(strToggleFillMode, xText, yText + tSize);
}
{% endhighlight JavaScript %}

Нека се върнем към нашата функция `draw()` и добавим извикването на `drawInstructions()`, но само ако `showInstructions` е активирано. И обърнете внимание, че това извикване на `drawInstructions()` трябва да се случи след изчертаването на буфера извън екрана на екрана. По този начин то ще бъде "насложено” отгоре.

{% highlight JavaScript %}
function draw() {
// Нарисувайте текущия щрих на четката на дадената позиция x, y
// Но ние не рисуваме върху платното, а върху offscreenGfxBuffer
drawBrushStroke(mouseX, mouseY);

// Нарисувайте буфера извън екрана на екрана
image(offscreenGfxBuffer, 0, 0);

// Проверяваме дали трябва да нарисуваме инструкциите
if(showInstructions){
drawInstructions();
}
}
{% endhighlight JavaScript %}

### Свързване на команди от клавиатурата

Ако внимателно прочетете инструкциите по-горе, може би сте забелязали, че ще слушаме определени клавиши от клавиатурата, за да контролираме различни свойства и поведения на нашата програма PaintIO. Ще използваме следните клавишни комбинации:

- Клавишът **i** ще показва/скрива инструкциите
- Клавишът **l** (малка буква L) ще изчиства екрана
- Клавишът **b** ще преминава през формите на четката (КРЪГ, КВАДРАТ, ТРИЪГЪЛНИК)
- Клавишът **f** ще преминава през типовете на режим на запълване (ЗАПЪЛВАНЕ, КОНТУР)

Ще имплементираме поддръжка на клавиатурата чрез метода [`keyPressed()`](https://p5js.org/reference/#/p5/keyPressed), който се извиква веднъж при всяко натискане на клавиш.

{% highlight JavaScript %}
function keyPressed() {
let lastFillMode = brushFillMode;
let lastBrushType = brushType;
print("keyPressed", key);
if(key == "f"){
brushFillMode++;
if (brushFillMode >= Object.keys(mapBrushFillMode).length) {
brushFillMode = 0;
}
}else if(key == "b"){
brushType++;
if (brushType >= Object.keys(mapBrushTypeToShapeName).length) {
brushType = 0;
}
}else if(key == "i"){
showInstructions = !showInstructions;
}else if(key == "l"){
// За да изчистите екрана, просто "нарисувайте” върху съществуващия
// графичен буфер с празен фон
offscreenGfxBuffer.background(100);
}
}
{% endhighlight JavaScript %}

За да изчистите екрана, обърнете внимание как просто презаписваме текущия графичен буфер с едноцветен фон с даден цвят (в този случай сиво 100): извикването `offscreenGfxBuffer.background(100)`.

### Напълно функционално приложение за рисуване в сиво

Ето какво имаме досега. Приложение за рисуване в сиво, което има фиксиран размер на четката, но няколко типа четки (кръг, квадрат, триъгълник) — избираеми с клавиша `b` — и типове запълване (запълване, контур) — избираеми с клавиша `f`. Можете също да изчистите екрана с клавиша `l` и да покажете/скриете инструкциите с `i`. Опитайте го по-долу или отворете кода в онлайн редактора p5.js [тук](https://editor.p5js.org/jonfroehlich/sketches/bl5o1BeZd), за да видите, редактирате и експериментирате с кода сами!

<iframe width="736" height="400" scrolling="no" src="https://editor.p5js.org/jonfroehlich/embed/bl5o1BeZd"></iframe>
**Код.* * Трябва да кликнете върху сивото платно, за да му дадете "фокус", за да могат да работят клавишните команди. Можете да разглеждате, редактирате и експериментирате с кода в [онлайн редактора p5.js](https://editor.p5js.org/jonfroehlich/sketches/bl5o1BeZd).
{: .fs-1 }

## PaintIO 2: Добавяне на Arduino

Направихме първоначална апликация за рисуване с мишка в p5.js (ура!), но тя не поддържа нашия персонализиран контролер "четка" и всъщност ние дори не сме създали или обсъдили този контролер (буу!).

Продължавайки с темата за простота и постепенно изграждане: нека създадем първоначален контролер "четка”, който предоставя само данни за местоположението на четката **x, y** (нормализирани като плаващи числа между [0, 1]). Първоначално контролерът ще бъде само за въвеждане на данни, т.е. той комуникира еднопосочно през сериен порт от Arduino към приложението p5.js.

Трябва да актуализираме приложението p5.js, за да поддържа сериен порт и да анализира входящите данни от нашия контролера "четка" и да проектираме и изградим споменатия контролер "четка" в Arduino. Да започваме!

<video autoplay loop muted playsinline style="margin:0px">
<source src="assets/videos/PaintIO-Grayscale-TwoPots-SayHi-Optimized.mp4" type="video/mp4" />
</video>
**Видео.** Ето един кратък поглед върху първоначалното приложение p5.js + Arduino, което ще разработим по-нататък в този урок. Да, опитвам се да напиша "Hi!”. Прилича на етч-а-скеч. :) Тази версия на кода p5.js е достъпна като [Paint I/O 2 - Web Serial](https://editor.p5js.org/ jonfroehlich/sketches/NxUaI2hnT), а кодът на Arduino е [XYAnalogOut.ino](https://github.com/makeabilitylab/arduino/blob/master/Serial/XYAnalogOut/XYAnalogOut.ino) в GitHub.
{: .fs-1 }

### Актуализиране на PaintIO от страна на p5.js за поддръжка на сериен

За да актуализираме приложението p5.js PaintIO за поддръжка на уеб сериен, трябва да изпълним четири стъпки:

- Добавете **серийна връзка** и **отворена** последователност
- Актуализирайте **инструкциите на екрана**, за да обясните как да се свържете със серийния порт (чрез натискане на клавиша `o`)
- Добавете **код за анализиране **, който анализира входящите данни от контролера на четката
- **Актуализирайте кода за рисуване **, за да използвате анализираното x,y местоположение на четката от серийните данни

#### Добавете последователност за серийно свързване и отваряне

В предишните уроци записвахме кликванията с мишката, за да инициираме серийни връзки. Тук ще използваме клавиатурата, по-конкретно клавиша `o`. Нека актуализираме функцията `keyPressed()`, за да търси клавиша `o` и след това да извика `serial.connectAndOpen()`.

{% highlight JavaScript %}
function keyPressed(){
...
}else if(key == "o"){
if (!serial.isOpen()) {
serial.connectAndOpen(null, serialOptions);
}
}
}
{% endhighlight JavaScript %}

#### Актуализирайте инструкциите на екрана

И добавете съответните инструкции:

{% highlight JavaScript %}
function drawInstructions(){
...
yText += tSize + yBuffer;
let strConnectToSerial = ""o" : Open serial (";
if(serial.isOpen()){
strConnectToSerial += "свързан";
}else{
strConnectToSerial += "несвързан";
}
strConnectToSerial += ")";
text(strConnectToSerial, xText, yText + tSize);
...
}
{% endhighlight JavaScript %}

#### Анализиране на серийни данни

Актуализирайте функцията `onSerialDataReceived()`, за да анализирате входящите данни и да зададете променливите `brushX` и `brushY`, които съдържат координатите x,y на четката в пиксели, както и `lastBrushX` и `lastBrushY`, които проследяват предишните местоположения x,y (подобно на [`pmouseX`](https://p5js.org/ reference/#/p5/pmouseX) и [`pmouseY`](https://p5js.org/reference/#/p5/pmouseY)):

{% highlight JavaScript %}
function onSerialDataReceived(eventSender, newData) {
//console.log("onSerialDataReceived", newData);
pHtmlMsg.html("onSerialDataReceived: " + newData);

if(!newData.startsWith("#")){
let startIndex = 0;
let endIndex = newData.indexOf(",");
if(endIndex != -1){
// Анализирайте местоположението x (нормализирано между 0 и 1)
let strBrushXFraction = newData.substring(startIndex, endIndex).trim();
let xFraction = parseFloat(strBrushXFraction);

// Анализирайте местоположението y (нормализирано между 0 и 1)
startIndex = endIndex + 1;
endIndex = newData.indexOf(",", startIndex);
let strBrushYFraction = newData.substring (startIndex, endIndex).trim();
let yFraction = parseFloat(strBrushYFraction);

// Задаване на съответните глобални променливи за местоположението на четката x,y в пиксели
lastBrushX = brushX;
lastBrushY = brushY;

brushX = xFraction * width;
brushY = yFraction * height;
}
}
}
{% endhighlight JavaScript %}

#### Актуализирайте кода за рисуване, за да използвате четката x,y

В момента рисуваме само четката в текущата позиция `mouseX` и `mouseY`. Сега нека нарисуваме четката и в текущата позиция `brushX` и `brushY`, които са зададени от Arduino-базирания контролер на четката. 

Внимателният читател ще забележи, че сега извикваме `drawBrushStroke()` **два пъти**: веднъж за вход от мишката и веднъж за вход от нашия контролер на базата на Arduino. Да, това е вярно. Но двуръчното взаимодействие с два контролера има дълга история в HCI (вижте [Mother of All Demos](https://youtu.be/yJDv-zdhzMY?t=2115) на Engelbart от 1968 г.) и отваря много плодотворни възможности за взаимодействие! По-късно ще направим мишката като четка, която може да се превключва. 

{% highlight JavaScript %}
function draw() {

// Нарисувай текущия щрих на четката в дадената позиция x, y на мишката
drawBrushStroke(mouseX, mouseY);

// Проверява дали сериалният порт е отворен. Ако е, използва данните brushX, brushY
if(serial.isOpen()){
// Рисува текущия щрих на четката в текущата позиция x,y на четката (от сериалния порт)
drawBrushStroke(brushX, brushY);
}

// Рисува буфера извън екрана на екрана
image(offscreenGfxBuffer, 0, 0);

// Проверете дали трябва да нарисуваме инструкциите
if(showInstructions){
drawInstructions();
}
}
{% endhighlight JavaScript %}

И това е всичко. Пълният код е достъпен в онлайн редактора p5.js като [Paint I/O 2 - Web Serial](https://editor.p5js.org/jonfroehlich/sketches/NxUaI2hnT).

### Изграждане на контролера за четката

Сега, след като завършихме първоначалната PaintIO приложение с поддръжка на сериен вход, е време да изградим персонализиран контролер за четката, базиран на Arduino. Припомнете си, че в началото просто ще предаваме информация за местоположението на четката x,y от Arduino към p5.js. Можем да използваме всеки аналогов сензор, който искаме за това, но за по-голяма простота ще започнем с нашия удобен и надежден [потенциометър](../ arduino/potentiometers.md).

#### Първоначалната схема на контролера за четката

![](assets/images/ArduinoLeonardo_2Pots_WithBreadboard.png)
**Фигура.** Първоначалният контролер за четката с два потенциометра, които контролират съответно x- и y-положението на четката.
{: .fs-1 }

#### Първоначален код на контролера за четката

Кодът на Arduino е прост: чете от двата аналогови входни пина, нормализира тези отчитания между [0, 1] (включително) и ги предава по сериен порт като низ, разделен със запетая.

{% highlight C++ %}
const int X_ANALOG_INPUT_PIN = A0;
const int Y_ANALOG_INPUT_PIN = A1;

// На Arduino Uno/Leonardo има 10-битов ADC, така че
// максималната аналогова стойност е 1023. На други микроконтролери, като ESP32,
// има 12-битов ADC, така че максималната аналогова стойност е 4095
const int MAX_ANALOG_VAL = 1023;
 

const long BAUD_RATE = 115200;
void setup() {
Serial.begin(BAUD_RATE);
}

void loop() {
// Прочетете аналоговите стойности
int xAnalogVal = analogRead(X_ANALOG_INPUT_PIN);
int yAnalogVal = analogRead(Y_ANALOG_INPUT_PIN);

// Изчисляване на нормализирано x,y местоположение
_x = xAnalogVal / (float)MAX_ANALOG_VAL;
_y = yAnalogVal / (float)MAX_ANALOG_VAL;

// Предаване през сериен порт като низ, разделен със запетая
Serial.print(_x, 4);
Serial.print(", ");
Serial.println(_y, 4);

забавяне(10);
}
{% endhighlight C++ %}

**Код.** Този код е достъпен в нашия GitHub като [XYAnalogOut.ino](https://github.com/makeabilitylab/arduino/blob/master/Serial/XYAnalogOut/XYAnalogOut.ino) . Можете да видите и варианта на базата на OLED като [XYAnalogOutOLED.ino](https://github.com/makeabilitylab/arduino/blob/master/Serial/XYAnalogOutOLED/XYAnalogOutOLED.ino).
{: .fs-1 }

### Тествайте и играйте с първоначалното приложение от край до край!

Успяхме! Сега е време да го тестваме и да си поиграем с него.

<video autoplay loop muted playsinline style="margin:0px">
<source src="assets/videos/PaintIO-Grayscale-TwoPots-KeyboardCommands-Optimized.mp4" type="video/mp4" />
</video>
**Видео.* * Първоначално приложение PaintIO p5.js + Arduino. Използваме двата потенциометра, за да зададем x,y местоположението на четката (размерът на четката е фиксиран) и клавиатурата на лаптопа, за да превключваме между типовете четки (клавиш `b`) и режимите на запълване (клавиш `f`). Кодът p5.js е достъпен като [Paint I/O 2 - Web Serial](https://editor. p5js.org/jonfroehlich/sketches/NxUaI2hnT), а кодът на Arduino е [XYAnalogOut.ino](https://github.com/makeabilitylab/arduino/blob/master/Serial/XYAnalogOut/XYAnalogOut.ino) в GitHub.
{: .fs-1 }

### Актуализиране на Arduino контролера с OLED

Тъй като ни интересува проучването на взаимодействието между два екрана, нека добавим [OLED](../advancedio/oled.md) към контролера на четката – по този начин художникът може да получава информация в реално време за четката на самия контролер. Засега ще показваме само местоположението на четката. Но ще добавим повече информация с развитието на приложението ни.

#### Основен контролер за четка с OLED

![](assets/images/ArduinoLeonardo_TwoPots_WithOLED.png)
**Фигура.** Същата верига с два потенциометра като преди, но с OLED дисплей.
{: .fs-1 }

#### Актуализирайте кода, за да покажете местоположението x,y на четката на OLED

Сега нека актуализираме кода на Arduino, за да покажем местоположението x,y на четката на OLED. Това ще се окаже полезно, когато добавим динамични размери на четката и четката ни е малка в приложението p5.js. Пълният код е в GitHub като [XYAnalogOutOLED.ino](https://github.com/ makeabilitylab/arduino/blob/master/Serial/XYAnalogOutOLED/XYAnalogOutOLED.ino); обаче, съответната част е просто:

{% highlight C++ %}
void loop(){
...

// Изчислете нормализираното x,y местоположение
_x = xAnalogVal / (float)MAX_ANALOG_VAL;
_y = yAnalogValal2 / (float)MAX_ANALOG_VAL;

// Задаване на ново местоположение на кръга въз основа на ускорението
int xBall = _radius + _x * _display.width() - 2 * _radius;
int yBall = _radius + _y * _display.height() - 2 * _radius;

// Показване на това нормализирано местоположение на екрана
_display.setCursor(0, 0);
_display.println("Нормализирани x,y:");
_display.print("X: ");
_display.println(_x, 4);
_display.print("Y: ");
_display.print(_y, 4);

_display.fillCircle(xBall, yBall, _radius, SSD1306_WHITE);

// Рендиране на буфера на екрана
_display.display();

...
}
{% endhighlight C++ %}

**Код.** Пълният код се намира в GitHub като [XYAnalogOutOLED.ino](https://github.com/makeabilitylab/arduino/blob/master/Serial/XYAnalogOutOLED/XYAnalogOutOLED.ino).
{: .fs-1 }

### Видео демонстрация на първоначалното приложение PaintIO

<video autoplay loop muted playsinline style="margin:0px">
<source src="assets/videos/PaintIO-Grayscale-TwoPots-Optimized.mp4" type="video/mp4" />
</video>
**Видео.** Тук използваме същия p5.js код като преди ([Paint I/O 2 - Web Serial](https://editor.p5js.org/jonfroehlich/sketches/NxUaI2hnT)), но с актуализирана Arduino верига (с OLED) и код за показване на позицията на четката. Забележете как, докато движим четката чрез двата потенциометра, позицията на четката се показва и на OLED. Също така отпечатваме нормализираната x,y позиция на OLED за отстраняване на грешки. Arduino кодът е в GitHub като [XYAnalogOutOLED.ino](https://github.com/makeabilitylab/arduino/blob/master/Serial/XYAnalogOutOLED/XYAnalogOutOLED.ino).
{: .fs-1 }

<!-- Поддържа и двуръчно взаимодействие:

TODO: вмъкване на видео. -->

<!-- TODO: възможно е също да се покаже SharpIR сензорът като вход за четката? -->

## PaintIO 3: Добавяне на двупосочност

Сега, когато имаме основна приложение за рисуване от край до край с персонализиран контролер за вход, нека добавим някои допълнителни творчески функции за рисуване, което ще изисква актуализиране както на p5.js, така и на Arduino приложенията:

- **Двупосочна комуникация:** Позволете на художника да зададе типа на четката и режима на запълване както в p5.js, така и в контролера за рисуване.
- **Поддръжка на четири входящи свойства на четката**: От Arduino към p5.js ще получим низ, разделен със запетая, за местоположението, размера, типа и режима на запълване на четката: `xPosFrac, yPosFrac, sizeFrac, brushType, brushFillMode`.
- **Поддръжка на сигнал за изчистване на екрана**: Искаме художникът да може да задейства изчистване на екрана с помощта на четката.
- **Показване на свойствата на четката на OLED:** В момента показваме само представяне на местоположението на четката на OLED. Нека подобрим това, за да показваме и друга информация за четката, като тип, размер и режим на запълване.
- **Цвят:** Можем също да получим ясна информация за цвета от Arduino. Засега обаче нека просто зададем цвета въз основа на размера на четката.

Разбира се, можете да добавите още функции, като персонализиран хардуер за въвеждане, за да контролирате цвета на четката, непрозрачността на четката, дебелината на контурите *и т.н.* Не се колебайте да го направите! Но засега ще се съсредоточим върху горните точки.

Ето един малък поглед!

<video autoplay loop muted playsinline style="margin:0px">
<source src="assets/videos/PaintIO-FullPotController-PaintingWithShapes-1200w.mp4" type="video/mp4" />
</video>
**Видео.** Ето един поглед към приложението p5.js [Paint I/O 3 - Bidirectional with Color](https://editor.p5js.org/jonfroehlich/sketches/GOvMjQr6y) с Arduino скица [PaintIO.ino](https://github.com/makeabilitylab/arduino/blob/master/Serial/PaintIO/PaintIO.ino) .
{: .fs-1 }

### Актуализиране на приложението p5.js

Както бе отбелязано по-горе, нашето приложение p5.js PaintIO вече трябва да поддържа четири входящи свойства на четката: `xPosFrac, yPosFrac, sizeFrac, brushType, brushFillMode`, които са описани [подробно тук](p5js-paint-io.md#from-arduino-to-p5js) . Освен това, когато потребителят натисне клавиша `b` (за да промени типа на четката) или клавиша `f` (за да промени режима на запълване), искаме да предадем тази информация обратно на Arduino, така че нашият контролер на четката и OLED екранът да останат синхронизирани.

#### Анализиране на допълнителни свойства на четката и изчистване на екрана

Нека започнем с актуализиране на кода за анализиране, за да поддържаме четирите входящи свойства на четката и командата "изчистване на екрана”. За последната, нека приемем, че входящият сериен текст, който започва с "cls”, задейства изчистване на екрана. Трябва да проверим това в допълнение към редовете, които започват с "#”, които показват редове за отстраняване на грешки.

Актуализирайте функцията `onSerialDataReceived()`:

{% highlight JavaScript %}
function onSerialDataReceived(eventSender, newData) {
pHtmlMsg.html("onSerialDataReceived: " + newData);

if(!newData.startsWith("#")){ // игнорирайте отстраняването на грешки
if(newData.toLowerCase().startsWith("cls")){ // проверете за изчистване на екрана
offscreenGfxBuffer.background(100);
}else{
parseBrushData(newData); // в противен случай анализирайте данните за четката
}
}
}
{% endhighlight JavaScript %}

След това добавете функцията `parseBrushData()`, за да анализирате `xPosFrac` като float между [0, 1], `yPosFrac` като float между [0, 1], `sizeFrac` като float между [0, 1], `brushType` като 0, 1, 2, съответстващо на CIRCLE, SQUARE, TRIANGLE, и `brushFillMode`, съответстващо на FILL *vs.* OUTLINE.

{% highlight JavaScript %}
function parseBrushData(newData){
// Форматът е xPosFrac, yPosFrac, sizeFrac, brushType, brushFillMode
let startIndex = 0;
let endIndex = newData.indexOf(",");
if(endIndex != -1){
let strBrushXFraction = newData.substring(startIndex, endIndex).trim();
let xFraction = parseFloat(strBrushXFraction);

startIndex = endIndex + 1;
endIndex = newData.indexOf(",", startIndex);
let strBrushYFraction = newData.substring(startIndex, endIndex).trim();
let yFraction = parseFloat(strBrushYFraction);

startIndex = endIndex + 1;
endIndex = newData.indexOf(",", startIndex);
let strBrushSizeFraction = newData.substring(startIndex, endIndex).trim();
let brushSizeFraction = parseFloat(strBrushSizeFraction);

startIndex = endIndex + 1;
endIndex = newData.indexOf(",", startIndex);
let strBrushType = newData.substring(startIndex, endIndex).trim();
let newBrushType = parseInt(strBrushType);

startIndex = endIndex + 1;
//endIndex = newData.indexOf(",", startIndex);
endIndex = newData.length;
let strBrushDrawMode = newData.substring(startIndex, endIndex).trim();
let newBrushDrawMode = parseInt(strBrushDrawMode);

// Ако данните са валидни, задайте нов тип форма
if (newBrushType in mapBrushTypeToShapeName) {
brushType = newBrushType;
}

// ако режимът на рисуване на фигурата е валиден, задайте нов режим на рисуване
if (newBrushDrawMode in mapBrushFillMode) {
brushFillMode = newBrushDrawMode;
}

lastBrushX = brushX;
lastBrushY = brushY;

brushX = xFraction * width;
brushY = yFraction * height;

brushSize = MAX_BRUSH_SIZE * brushSizeFraction;
}
}
{% endhighlight JavaScript %}

#### Предаване на типа четка и режим на запълване

Поддържаме промяна на типа четка и режим на запълване както чрез команди от клавиатурата, така и чрез контролера на четката. Следователно трябва да синхронизираме двете приложения (p5.js и Arduino). По този начин, когато използваме клавиатурата, за да променим типа на четката или режима на запълване, трябва да предадем тази информация по сериен порт към контролера на четката.

Добавете метод, наречен `serialWriteShapeData`, който е подобен на този, който имахме в [предходния урок](p5js-serial-io.md) за двупосочна серийна комуникация.

{% highlight JavaScript %}
async function serialWriteShapeData(shapeType, shapeDrawMode) {
if (serial.isOpen()) {
let strData = shapeType + "," + shapeDrawMode;
serial.writeLine(strData);
}
}
{% endhighlight JavaScript %}

След това извикайте тази функция от `keyPressed()`, когато е необходимо:

{% highlight JavaScript %}
function keyPressed() {
...
if(lastFillMode != brushFillMode || lastBrushType != brushType){
serialWriteShapeData(brushType, brushFillMode);
}
}
{% endhighlight JavaScript %}

#### Добавяне на цвят

Сега нека добавим малко цвят. Малко по-късно ще разгледаме няколко различни цветови карти. Засега нека просто съпоставим оттенъка с размера на четката. Най-лесният начин да контролираме оттенъка е да превключим `colorMode` от стандартния RGB на [HSB](https://en.wikipedia.org/wiki/HSL_and_HSV) (или понякога наричан HSB, за оттенък, насищане, стойност). Можем да направим това чрез функцията [`colorMode(HSB)`](https://p5js.org/reference/#/p5/colorMode), която ни позволява да зададем максимална стойност за оттенък (H), насищане (S), яркост (B) и алфа (A). По подразбиране този диапазон е съответно 360, 100, 100, 1 за HSB и 255, 255, 255, 255 за RGBA. За по-голяма простота ще направим максималната стойност 1 за HSBA. За повече информация за HSB и неговите предимства прочетете тази [статия в Уикипедия] (https://en.wikipedia.org/wiki/HSL_and_HSV).

Но накратко, ние използваме HSB, за да контролираме по-лесно оттенъка.

В `setup()` добавете следното:

{% highlight JavaScript %}
function setup(){
...
// Задайте цветовия режим на HSB с всяка стойност в диапазона от 0 до 1
colorMode(HSB, 1, 1, 1, 1)

// Задайте началния цвят на четката
brushColor = color(1, 0, 1, 0.18);
...
}
{% endhighlight JavaScript %}

След това, в draw, динамично задайте оттенъка въз основа на размера на четката:
{% highlight JavaScript %}
function draw() {

// Задайте цвета на четката
let hue = map(brushSize, 0, MAX_BRUSH_SIZE, 0, 1);
brushColor = color(hue, 0.7, 1, 0.2);

...
}
{% endhighlight JavaScript %}

Това е всичко. Можете да разгледате, редактирате и да си поиграете с тази нова версия на приложението PaintIO [тук](https://editor.p5js.org/jonfroehlich/sketches/GOvMjQr6y).

### Актуализиране на контролера на четката

Сега трябва да актуализираме контролера на четката, за да:
- Контролираме местоположението, размера, типа и режима на запълване на четката
- Показваме информация за четката на OLED

#### Актуализиране на веригата на четката

За самите хардуерни контроли отново можем да използваме всичко, което искаме! За да опростим нещата в този пример, ще използваме:
- Както и преди, потенциометри на A0 и A1 за контрол на местоположението на четката по x и y, съответно
- Потенциометър на A2 за контрол на размера на четката
- Три бутона за промяна на формата на четката, режима на запълване и за изчистване на екрана

![](assets/images/PaintIO_ArduinoLeonardo_ThreePotsThreeButtons.png)
**Фигура.** Схема на свързване за пълния контролер на четката с три потенциометра на A0, A1 и A2 за контрол на местоположението (x, y) и размера на четката, съответно, и три бутона за промяна на формата на четката, режима на запълване и изчистване на екрана. Изображение, създадено в Fritzing и PowerPoint.
{: .fs-1 }

#### Актуализиране на кода на четката

За кода трябва да актуализираме контролера на четката, за да:

- Чете A0, A1 и A2 за местоположението x, y и размера на четката и да нормализира стойностите до [0, 1]
- Чете GPIO пинове 4, 5, 6, за да итерира формата на четката и режима на запълване и да изчисти екрана
- Предава тези стойности през сериен порт
- Четене на серийния входен поток и анализиране на формата на четката и режима на запълване
- Изчертаване на информация, свързана с четката, на OLED, включително местоположението и размера на четката

Вместо да разглеждаме този код парче по парче, просто ще го свържем с GitHub като [PaintIO.ino](https://github.com/makeabilitylab/arduino/blob/master/Serial/PaintIO/PaintIO.ino). Самият код е по същество кулминация на последните няколко урока по сериен порт, така че трябва да е относително лесен (макар и малко дълъг). Не се колебайте да задавате въпроси!

<!-- TODO: да се обмисли предоставянето на увеличен изглед на OLED екрана тук? -->

### Видео демонстрация на двупосочен PaintIO

И кратко видео, което демонстрира как всичко работи заедно!

<video autoplay loop muted playsinline style="margin:0px">
<source src="assets/videos/PaintIO-FullPotController-PaintingWithPotAndMouseSimultaneously2-StaticShapes-Optimized.mp4" type="video/mp4" />
</video>
**Видео.** Видео демонстрация на приложението p5.js [Paint I/O 3 - Bidirectional with Color](https://editor.p5js.org/jonfroehlich/sketches/GOvMjQr6y) с Arduino скица [PaintIO.ino](https://github.com/makeabilitylab/arduino/blob/master/Serial/PaintIO/PaintIO.ino).
 
{: .fs-1 }

## PaintIO 4: Окончателно приложение PaintIO

Направихме няколко малки актуализации на PaintIO, за да създадем окончателен прототип на приложението, който включва поддръжка за:
- Включване и изключване на мишката като четка чрез натискане на клавиша `m`
- Превключване на четката на базата на Arduino чрез натискане на клавиша `s`
- И настройка на различни цветови режими чрез натискане на клавиша `c`, включително оцветяване според размера на четката, скоростта на четката, местоположението на четката и местоположението на мишката.
- Добавяне на курсор на екрана в p5.js за местоположението на четката

Окончателното приложение е в GitHub (p5.js [жива страница](https://makeabilitylab.github.io/p5js/WebSerial/p5js/ PaintIO), [код](https://github.com/makeabilitylab/p5js/tree/master/WebSerial/p5js/PaintIO)) и скица на Arduino ([PaintIOAccel.ino](https://github.com/makeabilitylab/arduino/blob/master/Serial/PaintIOAccel/PaintIOAccel.ino)).

### Контролер за четка, базиран на акселерометър

Също така проектирахме много по-плавен и интересен контролер за четка, използвайки 3-осев акселерометър за контрол на x,y местоположението на четката и [резистор, чувствителен към сила](../arduino/force-sensitive-resistors.md) за контрол на размера на четката. Преминахме към ESP32, защото библиотеките на OLED + LIS3DH акселерометъра заемаха повече памет, отколкото имаше на разположение Leonardo. 

Илюстративните и схематични диаграми на окабеляването са показани по-долу.

![](assets/images/PaintIO_ESP32_AccelAndFSR_PictorialDiagram.png)
**Фигура.** Илюстративна диаграма на контролера за четка, базиран на акселерометър, с ESP32. Изработена с Fritzing.
{: .fs-1 }

И схематичната:

![](assets/images/PaintIO_ESP32_AccelAndFSR_SchematicDiagram.png)
**Фигура.** Схематична диаграма на контролера за четка, базиран на акселерометър, с ESP32. Изработена с Fritzing.
{: .fs-1 }

### Видео демонстрация на PaintIO 4

Ето един кратък поглед върху това как използвам този нов контролер, последван от YouTube видео с обзор на цялото приложение PaintIO и опита с контролера.

<video autoplay loop muted playsinline style="margin:0px">
<source src="assets/videos/PaintIO-HelloPlusTrianglePainting-Optimized.mp4" type="video/mp4" />
</video>
**Видео.** Кратко видео демонстрация на нашия нов Arduino контролер, базиран на акселерометър (наречен [PaintIOAccel.ino](https://github.com/makeabilitylab/arduino/blob/master/Serial/PaintIOAccel/PaintIOAccel.ino)) и приложението PaintIO p5.js ([жива страница] (https://makeabilitylab.github.io/p5js/WebSerial/p5js/PaintIO), [код](https://github.com/makeabilitylab/p5js/tree/master/WebSerial/p5js/PaintIO)).
{: .fs-1 }

В YouTube видеото по-долу представяме пълна демонстрация на PaintIO с контролер за четка, базиран на акселерометър:

<iframe width="736" height="414" src="https://www.youtube.com/embed/oTuMkisug2A" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
**Видео.** Пълна видео демонстрация в [YouTube](https://youtu.be/oTuMkisug2A).
{: .fs-1 }

### Други идеи

Можете (и трябва) да проектирате и свой собствен контролер за четка! Помислете как да съпоставите различните свойства на четката със сензорите:
- Задайте размера или цвета на четката въз основа на входния сигнал от микрофона – по-силните звуци съответстват на по-големи размери на четката или различни нюанси. Сега можете да свирите, да викате и да пеете, за да рисувате!
- Задайте цвета на четката, като използвате сензор за цвят като [този от Adafruit](https://www.adafruit.com/product/1334)
- Позволете на художника да "рисува върху" съществуваща картина или видео поток (подобно на [това](https://youtu.be/QfpFX4NBhJw))
- Как да създадете нова форма на четка, която подпомага художника, допълва вградените сензори и се побира по-добре в ръцете му

<!-- ### Видео демонстрация на двупосочен Paint I/O -->


<!-- ![](assets/images/PaintIO_Image1.png)

![](assets/images/PaintIO_Image2.png) -->

<!-- Размерът на четката може да се настройва според температурата, звука и др. -->

## Някои примерни изображения

![](assets/images/PaintIO_Image1.png)

![](assets/images/PaintIO_Image3-Accel.png)

![](assets/images/PaintIO_Image4-Accel2.png)

<!-- - Импресионист?
- Импресионист на живо?

- Ако използваме версията с цветен сензор, можем да се свържем с един от любимите ни примери: I/O Brush от Ishii и Ryokai.
- Да използваме джойстик за въвеждане, вместо два потенциометра? -->

## Следващ урок

В [следващия урок](ml5js-serial.md) ще представим рамките за машинно обучение (ML) и ще използваме една от тях, наречена [ml5.js](https://ml5js.org/), за да създадем интерактивни приложения, базирани на ML, с Arduino.

<span class="fs-6">
[Предишен: p5.js Serial I/O](p5js-serial-io.md){: .btn .btn-outline }
[Следващ: ml5.js Serial](ml5js-serial.md){: .btn .btn-outline }
</span>
