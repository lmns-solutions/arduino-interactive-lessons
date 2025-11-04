---
lang: bg
permalink: /communication/p5js-serial.html
page_id: communication-p5js-serial
layout: default
title: L3&#58; p5.js Сериен Вход
nav_order: 3
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

Едва сега започваме да разкриваме възможностите, които предлага комбинацията от Arduino и компютри. В този урок (и в следващия) ще използваме творчески инструмент за кодиране, наречен [p5.js](https://p5js.org/), за да демонстрираме този потенциал. Очаква ни много забавно!

## Processing и p5.js

![](assets/images/ProcessingSketches_CollatzVariations.png)
**Фигура.** Вариации на хипотезата на Колац от потребител [/u/ideology_boi](https://www.reddit.com/r/processing/comments/dy5z5h/collatz_variations/) в Reddit. Кодирано в ~200 реда в Processing ([линк към кода](https://dailygenerative.art.blog/2019/11/17/reflections/)). Вдъхновено от видеото с разходка в Coding Train ["Предположението на Колац" ](https://www.youtube.com/watch?v=EYLWxwo1Ed8).
{: .fs-1 }

p5.js се базира на [Processing](https://processing.org/), който е създаден от [Casey Reas](https://en.wikipedia.org/wiki/Casey_Reas) и [Ben Frey](https://en.wikipedia.org/wiki/Ben_Fry) в MIT през 2001 г., за да предостави достъпен инструмент за програмиране за комбиниране на изкуство и технология. От уебсайта на Processing:

> От 2001 г. Processing насърчава софтуерната грамотност в областта на визуалните изкуства и визуалната грамотност в областта на технологиите. Десетки хиляди студенти, художници, дизайнери, изследователи и любители използват Processing за обучение и създаване на прототипи.
{: .fs-3 }

Processing включва както IDE, така и библиотека на базата на Java, за да позволи на дизайнери, художници, производители и инженери да *скицират с код*. Processing създава безопасна, достъпна и лесна за използване среда за кодиране, в която да се създават прототипи, експериментира и играе. Представете си Processing като творческо платно за програмисти!

Processing опростява графичното програмиране и абстрахира сложността. Всъщност, когато пишете код в Processing, дори не е нужно да знаете, че използвате Java! Това дизайнерско решение може да ви се стори познато! Всъщност, рамката на Arduino също абстрахира сложността и често начинаещите дори не знаят, че пишат `C/C++`. Това не е случайно: Arduino IDE и парадигмата на програмиране се базират на Processing!

![](assets/images/ProcessingVsArduino.png)
**Фигура.** Arduino IDE се базира на Processing ([източник](https://www.arduino.cc/en/guide/introduction)). Кликнете с десния бутон върху изображението и изберете "Отвори изображението в нов раздел", за да го увеличите.
{: .fs-1 }

Създаването на интерактивни графики и визуализации в Processing изисква само няколко реда код. Например, тук сме създали малка програма за рисуване с около 10 реда.

<video autoplay loop muted playsinline style="margin:0px">
<source src="assets/videos/ProcessingSimpleDrawingDemo-Optimized.mp4" type="video/mp4" />
</video>
**Видео.** Десетредна програма за рисуване, написана в [Processing](https://processing.org/).
{: .fs-1 }

Трудно е да се преувеличи влиянието, което Processing е оказал върху дигиталните артисти, творческите програмисти и дори образованието по компютърни науки. Processing се използва както от професионалисти, така и от любители и е създал творби, включени в музикални клипове (*например* [Radiohead's House of Cards](http://www.aaronkoblin.com/work/rh/index.html)), изложени в художествени галерии и включени в филми, телевизия и други медии. Processing е с отворен код и има етика на споделяне на работа и учене от другите. Вижте [Reddit Processing community](https: //www.reddit.com/r/processing/). Прочетете повече за мисията на Processing в [Processing Foundation](https://processingfoundation.org/).

<iframe width="736" height="414" src="https://www.youtube.com/embed/8nTFjVm9sTQ" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

**Видео.** Музикалният клип към песента House of Cards на Radiohead е кодиран в Processing. Вижте статията на Аарон Коблин [тук](http://www.aaronkoblin.com/work/rh/index.html). Разгледайте всички творби на Коблин [тук](http://www.aaronkoblin.com/) и се вдъхновете!
{: .fs-1 }

<!-- Космическа симулация в 35 реда код: https://www.reddit.com/r/processing/comments/dswnx6/a_galaxy_in_35_lines_of_code/
https://www.reddit.com/r/processing/comments/gye5sd/platonic_waves_octahedron/
https://www.reddit.com/ r/processing/comments/e12eg3/waves/
https://www.reddit.com/r/processing/comments/du2ewt/tree_generator/
-->

### p5.js

През 2008 г. [John Resig](https://en.wikipedia.org/wiki/John_Resig) (създателят на jQuery) пренесе Processing в JavaScript, което позволи на създателите да използват Processing без Java плъгин ([Wikipedia](https://en.wikipedia.org/wiki/Processing_(programming_language)#Processing.js)). Въпреки че прехвърлянето бе успешно в началото и бе прието от образователни програми като [Khan Academy](https://www.khanacademy.org/), то може би се случи малко прекалено рано в историята на HTML+JavaScript.

През 2013 г. Лорен Маккарти (медиен артист + професор в UCLA) създаде [p5.js](https://p5js.org/), която сега е официално поддържаната библиотека на базата на JavaScript за Processing и се визуализира в елемента [Canvas](https://developer.mozilla.org/en-US/docs/Web/API/Canvas_API). Подобно на първоначалната мисия на Processing, p5.js е:

> JavaScript библиотека за творческо кодиране, с фокус върху това да направи кодирането достъпно и включващо за артисти, дизайнери, преподаватели, начинаещи и всеки друг! p5.js е безплатна и с отворен код, защото вярваме, че софтуерът и инструментите за неговото изучаване трябва да бъдат достъпни за всеки.
{: .fs-3 }

Въпреки че p5.js е написан на JavaScript, а не на Java — два езика, които са с подобни имена, но нямат абсолютно [никаква връзка](https://en.wikipedia.org/wiki/JavaScript#Java)) — реализацията на p5.js има почти идентичен API. Така че е много лесно да преведете съществуващ Processing код в p5.js (и да научите p5.js като цяло, ако знаете Processing). Подобно на Processing, p5.js абстрахира голяма част от сложността на писането в JavaScript и ви позволява да се съсредоточите изцяло върху интерактивни графики и визуализации. Ето една проста програма в p5.js — забелязвате ли приликите?

![](assets/images/p5jsOnlineEditor.png)

А ето и същата програма за черно-бяло рисуване, която написахме в Processing по-горе, но сега написана в p5.js:

<video autoplay loop muted playsinline style="margin:0px">
<source src="assets/videos/p5jsSimpleDrawingDemo-Optimized.mp4" type="video/mp4" />
</video>
**Видео.** Десетредна програма за рисуване, написана в [p5.js](https://editor.p5js.org/jonfroehlich/sketches/fja8NHOKO). Преглеждайте, редактирайте и играйте с кода чрез [онлайн редактора](https://editor.p5js.org/jonfroehlich/sketches/fja8NHOKO).
{: .fs-1 }

p5.js разполага и с удобен и невероятно готин [онлайн редактор](https://editor.p5js.org/), който улеснява не само бързото писане, тестване и итерация на кода, но и споделянето му с други. В редактора просто отидете на `Файл -> Сподели` и изберете една от опциите.

![](assets/images/p5jsSharingSketch.png)
**Фигура.** Опции за споделяне в [онлайн редактора](https://editor.p5js.org/) на p5.js.
{: .fs-1 }

Така че не само можете да [видите нашия код](https://editor.p5js.org/jonfroehlich/sketches/fja8NHOKO) и да го редактирате директно – не се притеснявайте, това няма да повлияе на оригиналния код — но можете и да вградите кода в другите си HTML страници. Например, тук сме вградили скицата по-долу! Задръжте мишката, за да промените "четката" на чисто черно.

<iframe width="736" height="380" scrolling="no" src="https:// editor.p5js.org/jonfroehlich/embed/fja8NHOKO"></iframe>
**Код**. Жива вградена версия на нашата проста програма за черно-бяло рисуване в p5.js. Прегледайте, редактирайте и играйте с кода [тук](https://editor.p5js.org/jonfroehlich/sketches/fja8NHOKO).
{: .fs-1 }

Подобно на Processing, основната концепция е да *скицирате с код* – да играете, да експериментирате, да повтаряте, да създавате бързо прототипи на идеи. Намирам го за много интелектуално освобождаващо.

<!- - ### Примери за p5.js -->

<!-- Circle of rings: https://codepen.io/Mamboleoo/pen/JjGZBqL -->

### Примери за p5.js, написани в онлайн редактора

Ето някои примери, които сме написали директно в редактора на p5.js. Можете да кликнете върху тези връзки, за да видите, редактирате и изпълните кода. Имайте предвид, че много от тези примери са написани, докато ние самите все още се учехме да работим с p5.js (и, разбира се, нашето обучение никога не свършва!).

- [Визуализации на звук] (https://editor.p5js.org/jonfroehlich/sketches/d2euV09i)
- [Генератор на пейзажи с Дядо Коледа](https://editor.p5js.org/jonfroehlich/sketches/KFDQe5sbQ)
- [Игра "Cookie Monster"](https://editor.p5js.org/jonfroehlich/sketches/oUIeXC9sS)
- [Основна игра със слайдер и скролер](https://editor.p5js.org/jonfroehlich/sketches/JwvvVJlNi)
- [Игра "Falling Star FFT"](https://editor. p5js.org/jonfroehlich/sketches/UvFAcoUgu)
- [Flappy Bird](https://editor.p5js.org/jonfroehlich/sketches/shtF6XFeY)

## Обучение на p5.js

След като овладеете [OLED дисплея](../advancedio/oled.md) и графичното рендиране, p5.js ще ви се стори познат, но и безкрайно по-изразителен и достъпен. [Processing](https://processing.org/) (за Java) и [p5.js](https://p5js.org/) (за JavaScript) са някои от любимите ни програмни среди и нямаме търпение да споделим p5.js с вас!

В интернет има някои **страхотни** ресурси за изучаване на p5.js. Затова, вместо да ги повтаряме, просто ще ги споделим с вас!

- [Въведение в p5.js](https://medium.com/comsystoreply/introduction-to-p5-js-9a7da09f20aa) на Йоханес Прайс, отлично въведение в p5.js, редактора за кодиране, основното графично рендиране и интерактивността.

- Официалното ръководство за p5.js [Първи стъпки](https://p5js.org/get-started/), което е подобно на част от съдържанието на Preis, но все пак си заслужава да се разгледа.

- Множеството официални [примери за p5.js](https://p5js.org/examples/)

- [Programming with p5.js](https://thecodingtrain.com/beginners/p5.js/) на Coding Train от Даниел Шифман, който вероятно създава най-добрите, най-интересни, забавни и достъпни видеоклипове за творческо кодиране.

- Създателят на p5.js, Лорен Маккарти, написа книга, озаглавена [Първи стъпки с p5.js: създаване на интерактивни графики в JavaScript и Processing](https://alliance-primo.hosted.exlibrisgroup.com/permalink/f/kjtuig/CP71274969160001451), която е достъпна като електронна книга чрез библиотеката на UW.

Ще разгледаме части от p5.js и в лекциите, и в следващите няколко урока, но предполагаме, че сте прочели поне [Introduction to p5.js] (https://medium.com/comsystoreply/introduction-to-p5-js-9a7da09f20aa) и официалното ръководство за p5.js [Първи стъпки](https://p5js.org/get-started/).

## Разработване на p5.js

Можете да разработвате проекти с p5.js или в [онлайн редактора](https://editor.p5js.org/), или във вашата любима среда за уеб разработка. Ако ще разработвате локално, силно препоръчваме [VS Code] (https://code.visualstudio.com). Често преминаваме от [онлайн редактора](https://editor.p5js.org/) — за да скицираме или лесно да споделяме бързи идеи — към VSCode за по-големи или по-сложни проекти.
 

#### Настройка на p5.js в VSCode

В [предходния урок](web-serial.md) използвахме [Visual Studio Code (VS Code)](https://code.visualstudio.com/). Надяваме се, че вече сте изтеглили [VSCode](https://code.visualstudio.com/) и сте инсталирали разширението [Live Server](https://marketplace.visualstudio.com/items? itemName=ritwickdey.LiveServer). Ако не сте, следвайте [тези инструкции](web-serial.md#web-dev-tools) и го направете сега!

##### Използване на разширение p5.js VSCode

Най-лесният начин да настроите VSCode за p5.js е да инсталирате разширение като [p5.vcode](https://marketplace.visualstudio.com/items?itemName=samplavigne.p5-vscode) от Sam Lavigne. Това разширение:
- Автоматично създава празна папка с необходимите HTML/ CSS/JavaScript файлове. За да създадете нов проект, отворете VSCode Command Palette с `ctrl-shift-p` на Windows или `cmd-shift-p` на Mac и напишете `Create p5.js Project`, след което изберете нова празна папка, в която да поставите проекта си.
- Свързва автодопълването и документацията за ключовите думи и функции на p5.js, използвайки TypeScript дефиниции
- Предоставя локална версия на p5. js библиотеки, за да можете вие и вашият проект да работите офлайн
- Идва в комплект с други полезни разширения като Live Server, за да стартирате и тествате лесно проекти с уеб сървър.

Ако сте начинаещ в VSCode или уеб разработката, препоръчваме ви това решение!

<video autoplay loop muted playsinline style="margin:0px">
<source src="assets/videos/VSCodeAutocompleteForP5JS-TrimmedAndOptimized.mp4" type="video/mp4" />
</video>
**Видео.** Времето, прекарано в настройка на VSCode за p5.js, си заслужава инвестицията. Както показва видеото, получавате автодопълване, вградена документация и др. Можете да направите това с разширението [p5.vcode](https://marketplace.visualstudio.com/items?itemName=samplavigne.p5-vscode) или чрез ръчна настройка, описана по-долу.
{: .fs-1 }

##### Ръчна настройка на VSCode за p5.js

Въпреки че съм използвал горното разширение, обикновено конфигурирам VSCode ръчно за уеб разработка. Няма нищо магично в p5.js. Това е просто JavaScript библиотека!

Основната трудност е в опита да накарате VSCode да поддържа автодопълване за ключови думи и функции на p5.js. p5.js е написан на ванилов JavaScript, а не на [TypeScript](https://www.typescriptlang.org/) — и няма официална версия на файловете с дефиниции на p5.js TypeScript ([прочетете повече тук](https://stackoverflow.com/questions/ 54581512/make-vscode-understand-p5js)), което прави така, че [Intellisense](https://code.visualstudio.com/docs/editor/intellisense) на VSCode (*например,* автодопълване на код, изскачащи дефиниции на функции) не работи.

За щастие, има някои [страхотни блог постове ] (https://breaksome.tech/p5js-editor-how-to-set-up-visual-studio-code/) за това как да го накарате да работи.

## p5.js, Web Serial и Arduino

Добре, да започнем да създаваме неща! Ще започнем с Arduino, който изпраща данни към p5.js чрез сериен порт (`Arduino → Компютър`).

<!-- TODO: направи схема на веригата -->

### Стартов шаблон за код

За да улесним създаването на уеб приложения с p5.js и уеб сериала, създадохме основен шаблон за p5.js сериала. Можете да го видите и дублирате чрез [онлайн редактора на p5.js](https://editor. p5js.org/jonfroehlich/sketches/vPfUvLze_C) или от нашето GitHub хранилище (като [SerialTemplate](https://github.com/makeabilitylab/p5js/tree/master/WebSerial/p5js/SerialTemplate)).

---
**ВАЖНО:**

Трябва да се уверите, че скоростта на предаване в JavaScript програмата и в Arduino програмата съвпадат. За JavaScript можем да я настроим с опцията `let serialOptions = { baudRate: 115200 };`. За Arduino го правим с `Serial.begin(baudRate)`, както е описано в нашия [урок "Въведение в Serial"](serial-intro.md).

---

### Приложение за размер на кръг

Добре, нека създадем просто уеб приложение `Arduino → Computer` p5.js, което чете едно число с плаваща запетая между [0, 1] (като данни, кодирани като текст) и рисува кръг с подходящ размер. За тази демонстрация ще използваме програмата AnalogOut.ino на Arduino и уеб приложението CircleSizeIn (жива страница, код). Пълното приложение ще изглежда така:

<video autoplay loop muted playsinline style="margin:0px">
<source src="assets/videos/AnalogInputOut.ino-CircleSizeIn-POT-TrimmedAndOptimized.mp4" type="video/mp4" />
</video>
**Видео.** Демонстрация на приложението p5.js CircleSizeIn ([жива страница](http://makeabilitylab.github.io/p5js/WebSerial/p5js/CircleSizeInDemo), [код](https://github.com/makeabilitylab/p5js/tree/master/WebSerial/p5js/CircleSizeInDemo)), която получава сериен вход от прикачения Arduino, работещ с [AnalogOut.ino](https://github.com/makeabilitylab/arduino/blob/master/Serial/AnalogOut/ AnalogOut.ino). Използваме потенциометър на Pin A0 като аналогов вход. Забележка: в това видео използваме малко по-различен Arduino скиц, наречен [AnalogOutOLED.ino](https://github.com/makeabilitylab/arduino/blob/master/Serial/AnalogOutOLED/AnalogOutOLED.ino), за да демонстрираме както Arduino изхода, така и p5.js интерактивността.
{: .fs-1 }

Да започнем да създаваме!

#### Кодът на Arduino: AnalogOut.ino

Програмата на Arduino е проста: чете аналогова стойност и я предава чрез сериен порт.

По-конкретно, ще използваме [`analogRead` ](https://www.arduino.cc/reference/en/language/functions/analog-io/analogread/) на Pin A0 и ще го преобразуваме в дробна стойност между [0, 1] (включително) — този процес на "нормализиране” на сензорния вход просто улеснява споделянето на данни между програмите. За да нормализираме между [0, 1], просто трябва да разделим `analogVal` на максималния аналогов вход (който е 1023 на Arduino Uno и Leonardo поради 10-битовите ADC и 4095 на микроконтролери като ESP32, които имат 12-битови ADC). Ще зададем и скоростта на предаване на 115200.

Така цялата програма изглежда така:

{% highlight C %}
const int DELAY_MS = 5;

const int ANALOG_INPUT_PIN = A0;
const int MAX_ANALOG_INPUT = 1023;

int _lastAnalogVal = -1;

void setup() {
Serial.begin(115200); // задайте скоростта на предаване на 115200
}

void loop() {

// Получете новата аналогова стойност
int analogVal = analogRead(ANALOG_INPUT_PIN);

// Ако аналоговата стойност се е променила, изпрати нова през сериен порт
if(_lastAnalogVal != analogVal){
float sizeFrac = analogVal / (float)MAX_ANALOG_INPUT;
Serial.println(sizeFrac, 4); // 4 десетични знака точност
}

_lastAnalogVal = analogVal;
delay(DELAY_MS);
}
{% endhighlight C %}

**Код.** Пълният код е [AnalogOut.ino](https://github.com/makeabilitylab/arduino/blob/master/Serial/AnalogOut/AnalogOut.ino) в нашия GitHub.
{: .fs-1 }

Всичко това би трябвало да е ясно. Няма нищо ново тук. Правим това още от най-ранните уроци [Въведение в Arduino](../arduino/index.md).

#### Кодът p5.js: CircleSizeIn

Ще изградим първоначалното p5.js приложение стъпка по стъпка. Можете да изберете да го направите в [p5.js онлайн редактор](https://editor.p5js.org/) или в VSCode. Нашите инструкции ще бъдат за VSCode.
 

##### Настройка на първоначалния шаблон p5.js

Започнете с изцяло нов празен проект с файлове `index.html`, `css\style.css` и `sketch.js`. Ние ги поставяме в папка, наречена `CircleSizeIn`, но това зависи от вас.

Ако имате инсталиран [p5.vcode](https://marketplace.visualstudio.com/ items?itemName=samplavigne.p5-vscode), можете просто да създадете нов проект, като натиснете `ctrl-shift-p` в Windows или `cmd-shift-p` в Mac в VSCode и напишете `Create p5.js Project`, след което изберете нова празна папка (например `CircleSizeIn`), в която да поставите проекта си. Ако направите това, не забравяйте да добавите `serial. js` към `<body>` или `<head>` в `index.html`:

{% highlight HTML %}
<script src="https://cdn.jsdelivr.net/gh/makeabilitylab/p5js/_libraries/serial.js"></script>
{% endhighlight HTML %}

Или можете да създадете необходимите файлове ръчно.

Index.html трябва да изглежда така:

{% highlight HTML %}
<!DOCTYPE html>
<html>

<head>
<script src="https://cdnjs.cloudflare.com/ajax/libs/p5.js/1.3.1/p5.js"></script>
<link rel="stylesheet" type="text/css" href="css\style.css">
<meta charset="utf-8">
</head>

<body>
<script src="https://cdn.jsdelivr.net/gh/makeabilitylab/p5js/_libraries/serial.js"></script>
<script src="sketch.js"></script>
</body>

</html>
{% endhighlight HTML %}

Файлът `css\style.css`:

{% highlight CSS %}
html, body {
margin: 0;
padding: 0;
}

canvas {
display: block;
}
{% endhighlight CSS %}

И файлът `sketch.js`:

{% highlight JavaScript %}
function setup() {
createCanvas(400, 400);
}

function draw() {
background(100);
}
{% endhighlight JavaScript %}

Сега запазете и заредете страницата с Live Server. Тя трябва да изглежда така:

![](assets/images/CircleSizeDemoBlankCanvas.png)
**Фигура.** Първоначален шаблон за уеб разработка с p5.js и web serial.
{: .fs-1 }

Ако страницата ви не се зарежда или не изглежда така, разгледайте нашия празен шаблон тук ([live page](https://makeabilitylab.github.io/p5js/WebSerial/p5js/BlankTemplate/), [code](https://github.com/makeabilitylab/p5js/tree/master/WebSerial/p5js/BlankTemplate)).

##### Нарисувайте кръг

Нека актуализираме нашия `sketch.js`, за да нарисуваме бял кръг с диаметър 30 в центъра на платното. Ще използваме функцията [`fill()`](https://p5js.org/reference/#/p5/fill), за да зададем цвета на запълване, и ще изключим очертаването с [`noStroke()`](https://p5js.org/reference/#/p5/noStroke).

{% highlight JavaScript %}
function setup() {
createCanvas(400, 400);
}

function draw() {
background(100);

noStroke(); // изключване на контура
fill(250); // бял кръг

// Получаване на x,y центъра на рисунката Canvas
let xCenter = width / 2;
let yCenter = height / 2;
let circleDiameter = 50;
circle(xCenter, yCenter, circleDiameter);
}
{% endhighlight JavaScript %}

Трябва да изглежда така:

![](assets/images/CircleSizeDemo-StaticCircleInTheMiddle.png)

Или ето [жива демонстрация](https:// editor.p5js.org/jonfroehlich/sketches/aPoybLEdC) от онлайн редактора p5.js.

<iframe width="736" height="380" scrolling="no" src="https://editor.p5js.org/jonfroehlich/embed/aPoybLEdC"></iframe>

##### Направете кръга с динамичен размер

Сега нека направим тази скица интерактивна! Ще зададем размера на кръга въз основа на x позицията на мишката. По-късно ще модифицираме този код, за да използваме **входящи серийни данни** вместо мишката, но е добре да модулираме кода по този начин и да направим първоначалната интерактивност да работи.

{% highlight JavaScript %}
function draw() {
background(100);

noStroke(); // изключване на контура
fill(250); // бял кръг

// Получаване на x,y центъра на рисунката Canvas
let xCenter = width / 2;
let yCenter = height / 2;

// Задаване на диаметъра въз основа на позицията на мишката по ос Х
const maxDiameter = min(width, height);
let shapeFraction = mouseX / width;
let circleDiameter = maxDiameter * shapeFraction;
circle(xCenter, yCenter, circleDiameter);
}
{% endhighlight JavaScript %}

Трябва да изглежда нещо като това:

<video autoplay loop muted playsinline style="margin:0px">
<source src="assets/videos/CircleSizeIn-MouseX.mp4" type="video/mp4" />
</video>

Или ето [жива демонстрация](https://editor.p5js.org/jonfroehlich/sketches/HqhM0dc1B) от онлайн редактора p5.js.

<iframe width="736" height="380" scrolling="no" src="https://editor.p5js.org/jonfroehlich/embed/HqhM0dc1B"></iframe>

##### Добавете уеб сериен обект и функции за обратно извикване

Сега можем да добавим сериална функционалност. Това е много подобно на предишното, но ще добавим кода към `sketch.js`, а не като вграден скрипт в HTML `<body>` на индекса.

Първо, добавете три глобални променливи в началото на `sketch.js`:

{% highlight JavaScript %}
let shapeFraction = 0; // проследява новата форма на фракцията от сериала
let serial; // сериалният обект
let pHtmlMsg; // използва се за показване на съобщения чрез html (по избор)
{% endhighlight JavaScript %}

След това създайте Serial обекта в `setup()`, настройте callback функциите и опитайте да се свържете автоматично с предварително одобрени портове. Така `setup()` трябва да изглежда така:

{% highlight JavaScript %}
function setup() {
createCanvas(400, 400);

// Настройте Web Serial с помощта на serial.js
serial = new Serial();
serial.on(SerialEvents.CONNECTION_OPENED, onSerialConnectionOpened);
serial.on(SerialEvents.CONNECTION_CLOSED, onSerialConnectionClosed);
serial.on(SerialEvents.DATA_RECEIVED, onSerialDataReceived);
serial.on(SerialEvents.ERROR_OCCURRED, onSerialErrorOccurred);

// Ако имаме предварително одобрени портове, опитайте да се свържете с тях
serial.autoConnectAndOpenPreviouslyApprovedPort(serialOptions);

// Добавете малък елемент <p>, за да предоставяте съобщения. Това е по избор
pHtmlMsg = createP("Кликнете където и да е на тази страница, за да отворите диалоговия прозорец за сериална връзка");
}
{% endhighlight JavaScript %}

Трето, добавете тези callback функции:

{% highlight JavaScript %}
function onSerialErrorOccurred(eventSender, error) {
console.log("onSerialErrorOccurred", error);
pHtmlMsg.html(error);
}

function onSerialConnectionOpened(eventSender) {
console.log("onSerialConnectionOpened");
pHtmlMsg.html("Серийната връзка е отворена успешно");
}

function onSerialConnectionClosed(eventSender) {
console.log("onSerialConnectionClosed");
pHtmlMsg.html("onSerialConnectionClosed");
}

function onSerialDataReceived(eventSender, newData) {
console.log("onSerialDataReceived", newData);
pHtmlMsg.html("onSerialDataReceived: " + newData);
}
{% endhighlight JavaScript %}

Накрая добавете функцията `mouseClicked()`, за да се свържете със сериалния порт:

{% highlight JavaScript %}
function mouseClicked() {
if (!serial.isOpen()) {
serial.connectAndOpen(null, serialOptions);
}
}
{% endhighlight JavaScript %}

Сега запазете и стартирайте. Страницата трябва да изглежда почти същата, с изключение на добавения нов елемент `<p>` в долната част, който гласи "Кликнете където и да е на тази страница, за да отворите диалоговия прозорец за сериен порт".

![](assets/images/CircleSizeDemo-JustHookedUpSerialButDidNotParseContentYet.png)

##### Анализиране на входящи уеб серийни данни

Накрая, трябва да анализираме входящите серийни данни от `onSerialDataReceived()` и да ги съхраним в променливата `shapeFraction`, след което леко да актуализираме функцията `draw()`, за да използваме тази `shapeFraction`.

Ето актуализацията на `onSerialDataReceived()` 

{% highlight JavaScript %}
function onSerialDataReceived(eventSender, newData) {
console.log("onSerialDataReceived", newData);
pHtmlMsg.html("onSerialDataReceived: " + newData);

// Анализирайте входящата стойност като float
shapeFraction = parseFloat(newData);
}
{% endhighlight JavaScript %}

За нашата рутина `draw()` можем просто да коментираме реда `let shapeFraction = mouseX / width;`, защото `shapeFraction` вече се задава от `onSerialDataReceived()`:

{% highlight JavaScript %}
function draw() {
background(100);

noStroke(); // изключване на контура
fill(250); // бял кръг

// Получаване на x,y центъра на рисунката Canvas
let xCenter = width / 2;
let yCenter = height / 2;

// Задайте диаметъра въз основа на позицията на мишката по ос x
const maxDiameter = min(width, height);
// let shapeFraction = mouseX / width;
let circleDiameter = maxDiameter * shapeFraction;
circle(xCenter, yCenter, circleDiameter);
}
{% endhighlight JavaScript %}

И това е всичко! Успяхме! Можете да видите, редактирате и стартирате CircleSizeIn в онлайн редактора на p5.js [тук](https://editor.p5js.org/jonfroehlich/sketches/5Knw4tN1d) или чрез GitHub ([жива страница](http://makeabilitylab.github.io/p5js/WebSerial/p5js/CircleSizeInDemo) , [код](https://github.com/makeabilitylab/p5js/tree/master/WebSerial/p5js/CircleSizeInDemo)).

#### Видео демонстрация на CircleIn

Ето видео демонстрация:

<video autoplay loop muted playsinline style="margin:0px">
<source src="assets/videos/AnalogInputOut.ino-CircleSizeIn-POT-TrimmedAndOptimized.mp4" type="video/mp4" />
</video>
**Видео.** Демонстрация на приложението p5.js CircleSizeIn ([жива страница](http://makeabilitylab.github.io/p5js/WebSerial/p5js/CircleSizeInDemo) , [код](https://github.com/makeabilitylab/p5js/tree/master/WebSerial/p5js/CircleSizeInDemo)), която получава сериен вход от свързания Arduino, работещ с [AnalogOut.ino](https://github.com/makeabilitylab/arduino/blob/master/Serial/AnalogOut/AnalogOut. ino). Използваме потенциометър на Pin A0 като аналогов вход. Забележка: в това видео използваме малко по-различен Arduino скиц, наречен [AnalogOutOLED.ino](https://github.com/makeabilitylab/arduino/blob/master/Serial/AnalogOutOLED/AnalogOutOLED.ino), за да демонстрираме както Arduino изхода, така и p5.js интерактивността.
{: .fs-1 }

#### Други сензори като вход

И, разбира се, можем да свържем всеки сензор, който искаме, като вход. По-долу показваме демонстрации на [резистор, чувствителен към сила](../arduino/force-sensitive-resistors.md) и инфрачервен сензор за разстояние.

<!-- TODO: изготвяне на схеми на вериги за всеки -->
##### CircleSizeIn с FSR

Демонстрация на CircleSizeIn ([жива страница](http://makeabilitylab.github.io/p5js/WebSerial/p5js/CircleSizeInDemo), [код] (https://github.com/makeabilitylab/p5js/tree/master/WebSerial/p5js/CircleSizeInDemo)) с [резистор, чувствителен към сила](../arduino/force-sensitive-resistors.md). Arduino все още работи с [AnalogOut.ino](https://github.com/makeabilitylab/arduino/blob/master/Serial/AnalogOut/AnalogOut.ino).

<video autoplay loop muted playsinline style="margin:0px">
<source src="assets/videos/AnalogOut-CircleSizeIn-FSR-Trimmed2-Optimized.mp4" type="video/mp4" />
</video>
**Видео.** Демонстрация на приложението p5.js CircleSizeIn ([жива страница](http://makeabilitylab.github.io/p5js/WebSerial/p5js/CircleSizeInDemo), [код](https://github.com/makeabilitylab/p5js/tree/master/WebSerial/p5js/CircleSizeInDemo)), с [резистор, чувствителен към сила -чувствителен резистор (FSR)](../arduino/potentiometers.md) на Pin A0 и Arduino, работещ с [AnalogOut.ino](https://github.com/makeabilitylab/arduino/blob/master/Serial/AnalogOut/AnalogOut.ino). Използваме FSR на Pin A0 като аналогов вход. Забележка: в това видео използваме малко по-различен Arduino скиц, наречен [AnalogOutOLED.ino](https://github.com/makeabilitylab/arduino/blob/master/Serial/AnalogOutOLED/AnalogOutOLED.ino), за да демонстрираме както Arduino изхода, така и p5.js интерактивността.
{: .fs-1 }

##### CircleSizeIn с IR сензор за разстояние

А тук е демонстрация на CircleSizeIn ([жива страница](http://makeabilitylab.github.io/p5js/WebSerial/p5js/CircleSizeInDemo), [код](https://github.com/makeabilitylab/p5js/tree/master/WebSerial/p5js/ CircleSizeInDemo)) с [Sharp GP2Y0A21YK](https://www.sparkfun.com/ products/242) инфрачервен сензор за разстояние, който има аналогов изход, вариращ от 3,1 V при 10 cm до 0,4 V при 80 cm. Тъй като IR сензорът е шумен, не използвахме [AnalogOut.ino](https://github.com/makeabilitylab/arduino/blob/master/Serial/AnalogOut/AnalogOut.ino). Вместо това написахме специална програма, наречена [SharpIRDistanceOut.ino](https://github.com/makeabilitylab/arduino/blob/master/Serial/SharpIRDistanceOut/SharpIRDistanceOut.ino), която използва [филтър за пълзяща средна стойност](../advancedio/smoothing-input.md), за да изглади входните данни (с цената на малко забавяне на входните данни). 

<video autoplay loop muted playsinline style="margin:0px">
<source src="assets/videos/SharpIRDistance-CircleSizeIn-Trimmed-Optimized.mp4" type="video/mp4" />
</video>
**Видео.** Демонстрация на CircleSizeIn ([жива страница](http://makeabilitylab.github.io/p5js/WebSerial/p5js/CircleSizeInDemo), [код](https://github.com/makeabilitylab/p5js/tree/master/WebSerial/p5js/CircleSizeInDemo)) с [Sharp GP2Y0A21YK](https://www.sparkfun.com/products/242) инфрачервен сензор за разстояние, който има аналогов изход, вариращ от 3,1 V при 10 cm до 0,4 V при 80 cm. За видеото използвахме леко модифицирана версия на [SharpIRDistanceOut.ino](https://github.com/makeabilitylab/arduino/blob/master/Serial/SharpIRDistanceOut/SharpIRDistanceOut.ino), която също извежда информация към свързан OLED, наречен [SharpIRDistanceOutOLED.ino] (https://github.com/makeabilitylab/arduino/blob/master/Serial/SharpIRDistanceOutOLED/SharpIRDistanceOutOLED.ino)
{: .fs-1 }

### Опростен график в реално време

След като въведем данните в p5.js, можем да правим *всичко*, което пожелаем: да използваме въведените данни, за да променяме цветовете, да играем игра, да създаваме визуализации *и т.н.*

Спомнете си, че в [урока за OLED](../advancedio/oled.md) създадохме [аналогова графика в реално време](../advancedio/oled.md#demo-4-real-time-scrolling-analog-graph). По време на този урок аз споменах как тази графика възпроизвежда [известен пример за обработка](https://www.arduino.cc/en/Tutorial/BuiltInExamples/Graph), но е самостоятелна на Arduino. Сега можем да създадем този пример за обработка в p5.js!

От страна на Arduino можем да използваме същия Arduino код ([AnalogOut.ino](https://github.com/makeabilitylab/arduino/blob/master/Serial/AnalogOut/AnalogOut.ino)) като преди – което е логично, тъй като програмата Arduino просто чете аналогови данни и ги предава чрез сериен порт; обаче, очевидно трябва да напишем ново p5.js приложение. Нека я наречем `GraphIn`.

#### Написване на GraphIn в p5.js

Можем да започнем със същия сериен шаблон p5.js като преди: просто копирайте [`SerialTemplate`](https://github.com/makeabilitylab/p5js/tree/master/WebSerial/p5js/SerialTemplate) и преименувайте папката на `GraphIn`. Сега да започнем да пишем код!

Нашият p5.js код всъщност ще изглежда много подобен на версията за Arduino ([AnalogGraph.ino](https://github.com/makeabilitylab/arduino/blob/master/OLED/AnalogGraph/AnalogGraph.ino)), което говори за добрата работа, която екипът на Adafruit е свършил при писането на библиотеката си [GFX graphics] (https://learn.adafruit.com/adafruit-gfx-graphics-library/overview) библиотека.

Ще използваме опашка, за да съхраняваме временно данните, идващи от сериала, след което ще четем и изпразваме тази опашка в нашата функция `draw()`. За всяка нова стойност от сериала ще начертаем представителна линия на все по-нарастваща x-пикселна позиция (`xPos`). Тъй като това *не* е имплементация на превъртане, ние нулираме `xPos`, когато достигнем ширината на платното и започваме отначало.

Пълният код е ~50 реда

{% highlight JavaScript %}
let serial; // обектът Serial
let serialOptions = { baudRate: 115200 };
let queue = []
let xPos = 0;

function setup() {
createCanvas(750, 420);

// Настройка на Web Serial с помощта на serial.js
serial = new Serial();
serial.on(SerialEvents.DATA_RECEIVED, onSerialDataReceived);

// Ако имаме предварително одобрени портове, опитайте да се свържете с тях
serial.autoConnectAndOpenPreviouslyApprovedPort(serialOptions);

// Добавете малък елемент <p>, за да предоставяте съобщения. Това е по избор
pHtmlMsg = createP("Кликнете където и да е на тази страница, за да отворите диалоговия прозорец за серийна връзка");

background(50);
}

function draw() {

while(queue.length > 0){
// Вземете най-старата стойност от опашката (първо влязло, първо излязло)
// JavaScript не е многонишков, така че не е необходимо да заключваме опашката
// преди четене/модифициране.
let val = queue.shift();
let yPixelPos = height - val * height;

// Подобряване на цвета чрез динамично задаване на цвета на линията
// въз основа на текущата стойност на сензора
let redColor = val * 255;
stroke(redColor, 34, 255); //задаване на цвета
line(xPos, height, xPos, yPixelPos);

xPos++;
}

if(xPos >= width){
xPos = 0;
background(50);
}
}

function onSerialDataReceived(eventSender, newData) {
pHtmlMsg.html("onSerialDataReceived: " + newData);

// JavaScript не е многонишков, така че не е необходимо да заключваме опашката
// преди да добавим нови елементи
queue.push(parseFloat(newData));
}

function mouseClicked() {
if (!serial.isOpen()) {
serial.connectAndOpen(null, serialOptions);
}
}
{% endhighlight JavaScript %}

Това е! Доста впечатляващо, нали?! Можете да видите нашата реализация като [жива страница](https://makeabilitylab.github.io/p5js/WebSerial/p5js/GraphIn/) или [в GitHub](https://github.com/makeabilitylab/p5js/tree/master/WebSerial/p5js/GraphIn).

##### Видео демонстрация на GraphIn

Ето две видео демонстрации: едната с потенциометър, а другата с инфрачервен сензор за разстояние Sharp.

<video autoplay loop muted playsinline style="margin:0px">
<source src="assets/videos/AnalogOut.ino-GraphIn-POT-Trimmed-Optimized.mp4" type="video/mp4" />
</video>
**Видео.** Демонстрация на GraphIn ([жива страница](https://makeabilitylab.github.io/p5js/WebSerial/p5js/GraphIn/), [код](https://github.com/makeabilitylab/p5js/tree/master/WebSerial/p5js/GraphIn)) с потенциометър, свързан към Pin A0. Arduino работи с [AnalogOutOLED.ino] (https://github.com/makeabilitylab/arduino/blob/master/Serial/AnalogOutOLED/AnalogOutOLED.ino), но и нещо по-просто като [AnalogOut.ino](https://github.com/makeabilitylab/arduino/blob/master/Serial/AnalogOut/AnalogOut.ino) би работило!
{: .fs-1 }

А ето и демонстрация с инфрачервения сензор за разстояние Sharp.

<video autoplay loop muted playsinline style="margin:0px">
<source src="assets/videos/SharpIRDistanceOutOLED-GraphIn-Trimmed-Optimized.mp4" type="video/mp4" />
</video>
**Видео.** Демонстрация на GraphIn ([жива страница](https://makeabilitylab.github.io/p5js/WebSerial/p5js/GraphIn/), [код](https://github.com/makeabilitylab/p5js/tree/master/WebSerial/p5js/GraphIn)) с [Sharp GP2Y0A21YK](https://www.sparkfun.com/products/242) инфрачервен сензор за разстояние. Както и преди, използвахме леко модифицирана версия на [SharpIRDistanceOut.ino](https://github.com/makeabilitylab/arduino/blob/master/Serial/SharpIRDistanceOut/SharpIRDistanceOut.ino), която също извежда информация към свързан OLED, наречен [SharpIRDistanceOutOLED.ino] (https://github.com/makeabilitylab/arduino/blob/master/Serial/SharpIRDistanceOutOLED/SharpIRDistanceOutOLED.ino)
{: .fs-1 }

## Дейност

За вашите дневници за прототипиране създайте проста p5.js приложение, което чете една или повече серийни стойности, ги анализира по подходящ начин и прави нещо интересно. Приложението ви не трябва да е сложно, но искаме да проучите p5.js API и да демонстрирате вашите проучвания чрез код. Ако е необходимо, моля, напишете и съпътстваща Arduino програма (но винаги можете да използвате една от нашите, като [AnalogOut.ino](https://github.com/makeabilitylab/arduino/blob/master/Serial/AnalogOut/AnalogOut.ino) или [AnalogOutOLED.ino] (https://github.com/makeabilitylab/arduino/blob/master/Serial/AnalogOutOLED/AnalogOutOLED.ino)). В дневниците си включете кратко видео, линкове към кода и кратко отражение на наученото.

## Следващ урок

В [следващия урок](p5js-serial-io.md) ще покажем по-сложни примери, в които Arduino и p5.js комуникират двупосочно (компютър ↔ Arduino). Ще бъде забавно!

<span class="fs-6">
[Предишен: Въведение в уеб сериала](web-serial.md){: .btn .btn-outline }
[Следващ: Сериен I/O с p5.js](p5js-serial-io.md){: .btn .btn-outline }
</span>

<!-- TODO: да се обмисли показването на едно от по-ранните ни p5.js видеоклипове, които направихме за HCID с контролер? -->

<!-- - p5.js демота (направих три: едно само за изход, едно само за вход, едно двупосочно).

Просто демо за размер на топка

- ExplodingImage?

За вход може да се покаже: FSR и след това SharpIR (има SharpIRDistanceOut и SharpIRDistanceOutOLED)

Демонстрация на EtchaSketch
- Може да се използва цветен сензор, за да се оцвети четката в etchasketch
- Също така натиск, за да се промени размерът на четката. Може да са необходими три ръце за това

-- Не само с потенциометри, но и с FSR, може би сензор SharpIR?
-- След това да се покаже друга версия с красиви цветове и по-големи размери на топката? Подобно на версията, която имам в YouTube.

AccelBallDemo
- как да се направи това двупосочно?
- може би да се рисува на екрана (като редактор на нива) и да се превежда на OLED?

- И всъщност, accel може да бъде и вход за etch-a-sketch

-->
