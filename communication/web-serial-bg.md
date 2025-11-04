---
lang: bg
permalink: /communication/web-serial.html
page_id: communication-web-serial
layout: default
title: L2&#58; Уеб серийна комуникация
nav_order: 2
parent: Комуникация
has_toc: true # (включено по подразбиране)
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

В [предходния урок](serial-intro.md) се задълбочихме в асинхронната серийна комуникация, [серийната функционалност](https://www.arduino.cc/reference/en/language/functions/communication/serial/) на Arduino и как можем да пишем компютърни програми, като [serial_demo.py] (https://github.com/makeabilitylab/arduino/blob/master/Python/Serial/serial_demo.py), за двупосочна комуникация с Arduino.

В този урок ще приложим нашите нарастващи познания за сериалната комуникация в нов контекст: уеб! Сега може да ви се стори малко странно да използвате уеб браузър, за да комуникирате с локално свързано устройство. Но ако се замислите, всъщност правим това постоянно, когато използваме видео чат в уеб браузърите си: w3c [MediaDevices API](https://developer. mozilla.org/en-US/docs/Web/API/MediaDevices) предоставя регулиран достъп до медийни входни устройства като камери и микрофони.

По-скоро w3c специфицира API за сигурен достъп до USB устройства от уеб страници, наречен [WebUSB](https://wicg.github.io/webusb/ #security-and-privacy). Точно като [MediaDevices API](https://developer.mozilla.org/en-US/docs/Web/API/MediaDevices), сигурността и поверителността са от първостепенно значение. Уеб страниците, които искат достъп до локални USB устройства, трябва да поискат изрично разрешение от потребителя, което се обработва чрез уеб браузъра. Chrome добави поддръжка за WebUSB в края на 2017 г.

Въпреки това, WebUSB не включваше поддръжка за USB-към-серийни устройства като Arduino. Поради това беше предложен [Web Serial API](https://wicg.github.io/serial/), който беше пуснат в Chrome 89 (през март 2021 г.). Това е, което ще използваме в следващите няколко урока.

## Защо Web Serial?

Докато преди това сме преподавали серийна комуникация между компютър и Arduino с помощта на [Processing](https://processing.org/) и [Python](https://www.python.org/), използването на Web Serial ни позволява да комбинираме Arduino с творчески, бързо променящ се контекст: уеб. Web Serial ни позволява също да използваме всички чудесни уеб-базирани инструменти и API като [p5js](https://p5js.org/), [ml5js](https://ml5js.org/), [paper.js](http://paperjs.org/), [three.js](https://threejs.org/), [matter.js](https://brm.io/matter-js/) и други!

Разбира се, ако вашата Arduino платка има вграден WiFi, можете да комуникирате директно с уеб сървъри (както разглеждаме малко в [ESP32 IoT урок](../esp32/iot.md)); обаче, в този случай, ние приемаме, че имате или кабелна връзка чрез сериен порт през USB, или локална безжична връзка чрез сериен порт през Bluetooth.

Много от нещата, които правим с Web Serial, могат да бъдат преведени в WiFi контекст.
 

## Web Serial API

По думите на [François Beaufort](https://web.dev/serial/), Web Serial API:

> свързва уеб и физическия свят, като позволява на уебсайтовете да комуникират със сериенни устройства, като микроконтролери и 3D принтери
{: .fs-3 }

Web Serial вече се използва в уеб инструменти като [MakeCode на Microsoft](https://makecode.adafruit.com/), който ви позволява да програмирате микроконтролери чрез визуален език за програмиране с плъзгане и пускане, и [Arduino's Web Editor](https://create.arduino.cc/editor), който ви позволява да пишете код от браузъра, да съхранявате работата си в облака и да качвате скици директно от уеб.

### Поддържа ли уеб браузърът ми Web Serial?

Към момента на написването на тази статия (май 2021 г.) **Chrome** и **Edge** версии 89+ са единствените браузъри, които поддържат Web Serial, но скоро се очакват и други! За да проверите дали Web Serial API се поддържа, вижте [таблицата за съвместимост на браузърите](https://developer.mozilla.org/en-US/docs/Web/API/Serial#browser_compatibility) на Mozilla. Алтернативно, отворете конзолата на инструмента за разработчици в уеб браузъра си (в Windows, натиснете `ctrl-shift-i` в Chrome или Firefox; в Mac, натиснете `cmd-alt-i`).

{% highlight JavaScript %}
> "serial" в navigator
true
{% endhighlight JavaScript %}

Ако е true, браузърът поддържа функцията. Ако е false, браузърът не я поддържа.

### Как да използвате Web Serial API

[François Beaufort](https://web.dev/serial/) предоставя добър обзор на това как да използвате Web Serial API. Моля, прочетете [уебсайта им](https://web.dev/serial/) за подробна информация.

Но накратко. Web Serial API е асинхронен и базиран на събития. Това предотвратява блокирането на уебсайтовете, когато чакат вход от Web Serial.

#### Искане на разрешение за комуникация със сериен устройство

За да отворим сериен порт, първо трябва да поискаме порт. За сигурност, това повикване се управлява от браузъра и се появява диалогов прозорец, който пита потребителя да избере сериен порт и да даде разрешение на уебсайта. Кодът е базиран на [блога на François Beaufort](https://web.dev/serial/).

{% highlight JavaScript %}
// Показва на потребителя да избере сериен порт.
const port = await navigator.serial.requestPort();
{% endhighlight JavaScript %}

Ключовата дума [`await`](https://developer. mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/await) ключовата дума чака асинхронната функция `requestPort()` да се върне.

Подобно на [iPython](https://ipython.org/), една от невероятните характеристики на JavaScript е, че можем да го програмираме динамично в конзолата за разработчици и дори да взаимодействаме с променливите на текущия уебсайт, *и т.н.*

Така че можете да опитате горната команда сами. В конзолата на инструмента за разработчици на браузъра напишете:

{% highlight JavaScript %}
> await navigator.serial.requestPort();
{% endhighlight JavaScript %}

Ако Arduino е включен, трябва да видите нещо подобно на това:

![](assets/images/WebBrowserSerialDevicePermissionPrompt.png)
**Фигура.** Ако въведа `navigator.serial.requestPort()` в конзолата за разработчици на Chrome, като Arduino Leonardo е включен в USB порта на лаптопа ми, получавам показаното по-горе съобщение.
{: .fs-1 }

#### Отваряне на сериен порт

За да отворим сериен порт, извикваме `port.open(SerialOptions)`. [SerialOptions](https://reillyeon.github.io/serial/#dom-serialoptions) е речник с параметри за сериен порт, дефинирани като:

{% highlight JavaScript %}
речник SerialOptions {
required [EnforceRange] unsigned long baudRate;
[EnforceRange] octet dataBits = 8;
[EnforceRange] octet stopBits = 1;
ParityType parity = "none";
[EnforceRange] unsigned long bufferSize = 255;
FlowControlType flowControl = "none";
};
{% endhighlight JavaScript %}

Тези опции би трябвало да ви изглеждат познати. Имаме:
- `baudRate`: единствената **задължителна** опция, която трябва да бъде цяло число, като 9600 или 115200
- `dataBits`: броят на битовете данни на кадър (7 или 8).
- `stopBits`: броят на стоп битовете в края на кадъра (1 или 2).
- `parity`: режимът на четност (или "none", "even" или "odd").
- `bufferSize`: Размерът на буферите за четене и запис, които трябва да бъдат създадени (трябва да е по-малък от 16 MB).
- `flowControl`: Режимът на контрол на потока (или "none", или "hardware").

Така че, за да отворим порт с 9600 бода, ще напишем:

{% highlight JavaScript %}
// Покажете на потребителя да избере някой сериен порт.
const port = await navigator.serial.requestPort();

// Изчакайте сериен порт да се отвори.
await port.open( { baudRate: 9600 });
{% endhighlight JavaScript %}

#### Записване на данни

За да запишем двоични данни, използваме `getWriter()` и `write()`. Трябва да извикаме `releaseLock()`, за да може сериалният порт да бъде затворен по-късно.

{% highlight JavaScript %}
const writer = port.writable.getWriter();

// Записване на ASCII стойностите за думата "h”, "e”, "l”, "l”, "o”
// като бинарни данни
const data = new Uint8Array([104, 101, 108, 108, 111]);
await writer.write(data);

// Разрешаване на затварянето на сериен порт по-късно.
writer.releaseLock();
{% endhighlight JavaScript %}

За текстови данни използваме `TextEncoderStream`:

{% highlight JavaScript %}
const textEncoder = new TextEncoderStream();
const writableStreamClosed = textEncoder.readable.pipeTo(port.writable);

const writer = textEncoder.writable.getWriter();

await writer.write("hello");

// Позволете сериен порт да бъде затворен по-късно.
writer.releaseLock();
{% endhighlight JavaScript %}

#### Четене на данни

Четенето на данни е подобно. Използваме `getReader()` и методите `read()`. По-долу ще опишем решението за четене на текст. Можете да научите повече за четенето на двоични данни [тук](https://web.dev/serial/#read-port).

{% highlight JavaScript %}
const textDecoder = new TextDecoderStream();
const readableStreamClosed = port.readable.pipeTo(textDecoder.writable);
const reader = textDecoder.readable.getReader();

// Слушайте данните, идващи от серийното устройство.
while (true) {
const { value, done } = await reader.read();
if (done) {
// Позволете серийният порт да бъде затворен по-късно.
reader.releaseLock();
break;
}
// value е низ.
console.log(value);
}
{% endhighlight JavaScript %}

## Нашият клас Web Serial

За да улесним работата с Web Serial, написахме основен клас Web Serial JavaScript, наречен [`serial.js`](https://github.com/makeabilitylab/p5js/blob/master/_libraries/serial.js).

За да използвате нашия клас Web Serial, можете да клонирате нашето [p5js репо] (https://github.com/makeabilitylab/p5js) и да включите `serial.js` от `_libraries/serial.js` или да използвате услугата [jsDelivr](https://www.jsdelivr.com/), която превръща всяко GitHub репо в CDN и директно обслужва `serial.js` от нашето GitHub репо. 

За втория вариант, в `<head>` или `<body>` на вашия html файл, просто добавете:

{% highlight HTML %}
<script src="https://cdn.jsdelivr.net/gh/makeabilitylab/p5js/_libraries/serial.js"></script>
{% endhighlight HTML %}

Понастоящем [`serial.js`](https://github.com/makeabilitylab/p5js/blob/master/_libraries/serial.js) поддържа само четене/записване на текстови данни (а не бинарни данни), но това не би трябвало да ни засяга!

### Функции, базирани на събития

[`serial.js`](https://github.com/makeabilitylab/p5js/blob/master/_libraries/serial.js) използва архитектура, базирана на събития, с callback функции, което е често срещано в уеб и UI програмирането (виж: Mozilla's [Introduction to Events](https://developer.mozilla.org/en-US/docs/Learn/JavaScript/Building_blocks/Events)). Класът Serial има четири събития, които съответстват на отваряне на връзка, затваряне, получаване на данни и грешки.

{% highlight JavaScript %}
const SerialEvents = Object.freeze({
CONNECTION_OPENED: Symbol("Отворена нова връзка"),
CONNECTION_CLOSED: Symbol("Затворена връзка"),
DATA_RECEIVED: Symbol("Получени нови данни"),
ERROR_OCCURRED: Symbol("Възникнала грешка"),
});
{% endhighlight JavaScript %}

За да създадете нов Serial обект и да се абонирате за събитията, трябва да напишете:

{% highlight JavaScript %}
// Настройте Web Serial с помощта на serial.js
const serial = new Serial();

// Абонирайте се за събитията.
serial.on(SerialEvents.CONNECTION_OPENED, onSerialConnectionOpened) ;
serial.on(SerialEvents.CONNECTION_CLOSED, onSerialConnectionClosed);
serial.on(SerialEvents.DATA_RECEIVED, onSerialDataReceived);
serial.on(SerialEvents.ERROR_OCCURRED, onSerialErrorOccurred);

// Извиква се от Serial, когато възникне грешка
function onSerialErrorOccurred(eventSender, error) {
console.log("onSerialErrorOccurred", error);
}

// Извиква се от Serial, когато се отвори сериална връзка
function onSerialConnectionOpened(eventSender) {
console.log("onSerialConnectionOpened");
}

// Извиква се от Serial, когато се затвори връзка
function onSerialConnectionClosed(eventSender) {
console.log("onSerialConnectionClosed");
}

// Извиква се от Serial, когато се получат нови данни
function onSerialDataReceived(eventSender, newData) {
console.log("onSerialDataReceived", newData);
}
{% endhighlight JavaScript %}

Не е необходимо да се абонирате за *всички* събития – само за тези, които ви трябват. Абонирането за всички събития обаче ви предоставя повече информация, ако нещо се обърка.

### Отваряне на сериен порт

За да отворите сериен порт, извикайте `connect()`, последвано от `open()`. Сигнатурите на метода са:

{% highlight JavaScript %}
async connect(existingPort = null, portFilters = null)
async open(serialOptions = { baudRate: 9600 }) {
{% endhighlight JavaScript %}

Методът `connect()` приема два опционални параметра:

- `existingPort`: предварително създаден сериен порт (*например,* върнат от `navigator.serial.requestPort()`). Обикновено той е null
- `portFilters`: речник [SerialPortFilter](https://reillyeon.github.io/serial/#serialportfilter-dictionary). Обикновено той също е null.

Методът `open()` приема описания по-горе речник [SerialOptions](https://reillyeon.github.io/serial/#dom-serialoptions). Ако не се предаде параметър, речникът по подразбиране е `serialOptions = { baudRate: 9600 }`.

За удобство има два допълнителни метода `connectAndOpen()` и `autoConnectAndOpenPreviouslyApprovedPort()` — обикновено използваме тези:

{% highlight JavaScript %}
// Изисква одобрение от потребителя за свързване към сериен устройство и отваря порта към
// одобреното устройство
async connectAndOpen(portFilters = null, serialOptions = { baudRate: 9600 })

// Автоматично свързва и отваря предварително одобрения порт
// Ако има повече от един, взема най-горния порт в списъка с одобрени портове
async autoConnectAndOpenPreviouslyApprovedPort (serialOptions = { baudRate: 9600 })
{% endhighlight JavaScript %}

Методът `connectAndOpen()` просто комбинира двете функции `connect()` и `open()`. Функцията за автоматично свързване се възползва от кеширането на разрешенията на уеб браузъра – трябва да одобрите устройството само веднъж за всяка уеб страница.

## Да направим нещо

Ще започнем с изпълнението на същия Arduino код ([SimpleSerialIn.ino] (https://github.com/makeabilitylab/arduino/blob/master/Serial/SimpleSerialIn/SimpleSerialIn.ino)) със същата верига като в [предходния урок](serial-intro.md). Веригата:

![](assets/images/SimpleSerialIn_LEDCircuit.png)
**Фигура. ** Съответната верига за [SimpleSerialIn.ino](https://github.com/makeabilitylab/arduino/blob/master/Serial/SimpleSerialIn/SimpleSerialIn.ino). Изработена в Fritzing и PowerPoint.
{: .fs-1}

Сега нека създадем проста уеб страница, използвайки Web Serial, за да взаимодействаме с ([SimpleSerialIn.ino](https://github.com/ makeabilitylab/arduino/blob/master/Serial/SimpleSerialIn/SimpleSerialIn.ino)).

### Инструменти за уеб разработка

Препоръчваме разработването на уеб код в [Visual Studio Code (VSCode)](https://code.visualstudio.com/) с разширението [Live Server](https://marketplace.visualstudio.com/items?itemName=ritwickdey. LiveServer). Тъй като Web Serial изисква разрешение за устройството, трябва да стартирате уеб страницата си на сървър, вместо да отваряте `index.html` директно от операционната си система (с други думи, двойното кликване върху `index.html` в File Explorer или Finder няма да работи правилно).

За да инсталирате Live Server, отворете VSCode и кликнете върху `Extensions` в лявата странична лента (или натиснете `ctrl-shift-x`), след което потърсете [Live Server](https://marketplace.visualstudio.com/items?itemName=ritwickdey.LiveServer) в текстовото поле. Към момента на написването на тази статия разширението има почти 12 милиона инсталации.

За да използвате Live Server, отворете страница `.html` в VSCode. След това можете да кликнете с десния бутон върху файла и да изберете "Open with Live Server" (Отвори с Live Server) или да потърсите синия бутон "Go Live" (Стартирай на живо) в долния десен ъгъл на VSCode. Кликнете върху него и ето, вече стартирате уеб сървър, който обслужва уеб страницата! По подразбиране сървърът ще се презарежда при всяка промяна на html файла или някоя от неговите зависимости!

### Основна уеб страница със слайдер

Ще създадем проста уеб страница със слайдер, който предава стойност между 0 и 255 като текстово кодирана низове чрез Web Serial. Arduino получава текстовата стойност и я преобразува в `int`, след което записва това цяло число чрез `analogWrite` чрез един от пиновете с PWM.

Пълното изживяване на приложението трябва да изглежда така:

<video autoplay loop muted playsinline style="margin:0px">
<source src="assets/videos/SimpleSerialIn-JavaScript-SliderOut-Snippet720p.mp4" type="video/mp4" />
</video>
**Видео.** Изпълнение на демото SliderOut ([жива страница](https://makeabilitylab.github.io/p5js/WebSerial/Basic/SliderOut), [код](https://github.com/makeabilitylab/p5js/tree/master/WebSerial/Basic/SliderOut)) с [SimpleSerialIn.ino](https://github.com/makeabilitylab/arduino/blob/master/Serial/ SimpleSerialIn/SimpleSerialIn.ino) на Arduino Leonardo.
{: .fs-1 }

#### Създайте папка и начална страница index.html

За да започнете, създайте папка с име `SliderOut` и празен файл `index.html` в нея. След това в VSCode изберете `File->Open Folder` и изберете `SliderOut`. С отворена гледка `Explorer` в лявата странична лента на VSCode (`ctrl-shift-e`), кликнете два пъти върху файла `index.html`, за да го отворите. Сега VSCode трябва да изглежда по следния начин:

![](assets/images/VSCode_EmptyIndexHtmlFile.png)

В `index.html` копирайте/поставяйте тази проста, минималистична html страница:

{% highlight HTML %}
<!DOCTYPE html>
<html>
<head>
<title>Web Serial Demo</title>
</head>

<body>
Съдържанието ще бъде тук!
</body>
</html>
{% endhighlight HTML %}

Запазете файла (`ctrl-s`). Сега, за да се уверите, че всичко работи, стартирайте го чрез Live Server.

Има три начина да стартирате Live Server – всеки от тях ще работи! Можете да увеличите някоя от скрийншотите по-долу, като кликнете с десния бутон върху тях и изберете "Open Image in New Tab” (Отвори изображение в нов раздел).

| 1. Кликнете с десния бутон върху файла в Explorer View | 2. Кликнете с десния бутон върху файла в Editor | 3. Кликнете върху бутона "Go Live” |
| ----|----|----|
| ![](assets/images/VSCode_LaunchLiveServer1-RightClickOnIndexHtml.png) | ![](assets/images/VSCode_LaunchLiveServer2-RightClickonFileInEditor.png) | ![](assets/images/VSCode_LaunchLiveServer3-ClickOnGoLiveButton.png) |

След стартиране, вашият браузър по подразбиране ще се отвори към уеб сървър, работещ на `127.0.0.1` на порт 5500 (подразбиращи се настройки на Live Server). Уеб страницата трябва да изглежда така:

![](assets/images/LiveServerLaunched_WebSerialDemoBlankPage.png)

Сега нека добавим заглавие в блок `<h1>` и малко описателен текст:

{% highlight HTML %}
<!DOCTYPE html>
<html>
<head>
<title>Web Serial Demo</title>
</head>

<body>
<script src="https://cdn.jsdelivr.net/gh/makeabilitylab/p5js/_libraries/serial.js"></script>
<h1>Web Serial Demo</h1>
Тази демонстрация използва плъзгач, за да изпрати число между 0 и 255 на свързаното ви сериално устройство.
</body>
</html>
{% endhighlight HTML %}

Ако натиснете `ctrl-s`, уебсайтът трябва да се презареди автоматично, ако все още имате стартиран Live Server. Ако не е така, просто стартирайте отново уебстраницата с Live Server (и го оставете да работи, докато изграждаме).

![] (assets/images/WebSerialDemo_NowWithSimpleText.png)

#### Добавете бутон за свързване

Тъй като Web Serial изисква изрично разрешение от потребителя за свързване с локално сериално устройство, трябва да добавим "бутон за свързване". За да направим това, ще използваме HTML елемента [`<button>`](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/button) и ще зададем callback функция, наречена `onConnectButtonClick()` (можем да я наречем както искаме, но тя трябва да съвпада с последващата callback функция, която ще напишем).

{% highlight HTML %}
<!DOCTYPE html>
<html>
<head>
<title>Демонстрация на Web Serial</title>
</head>

<body>
<script src="https://cdn.jsdelivr.net/gh/makeabilitylab/p5js/_libraries/serial.js"></script>
<h1>Демонстрация на Web Serial</h1>
Тази демонстрация използва плъзгач, за да изпрати число между 0 и 255 на свързаното ви сериално устройство.

<p></p>
<button id="connect-button" onclick="onConnectButtonClick()">Свързване чрез сериен порт</button>

<script>
async function onConnectButtonClick() {
console.log("Натиснат бутон за свързване!")
}
</script>
</body>
</html>
{% endhighlight HTML %}

Презаредете уеб страницата и отворете конзолата за разработчици (която трябва да държите отворена почти винаги, когато разработвате уеб приложения). Кликнете върху бутона "Свързване чрез сериен порт" и трябва да видите съобщението "Натиснат бутон за свързване!" отпечатано в конзолата.

![](assets/images/WebSerialDemo_WithConnectButton.png)

#### Добавете и свържете serial.js

Сега трябва да добавим и свържем Web Serial, което ще направим чрез библиотеката [`serial.js`](https://github.com/makeabilitylab/p5js/blob/master/_libraries/serial.js). В HTML скриптовете могат да бъдат поставени в `<body>`, `<head>` или и в двете. Страниците се зареждат отгоре надолу. В този случай ще го поставим в горната част на `<body>`.

{% highlight HTML %}
<body>
<script src="https://cdn.jsdelivr.net/gh/makeabilitylab/p5js/_libraries/serial.js"></script>

...
{% endhighlight HTML %}

Сега трябва да създадем Serial обект и да добавим callback функциите. Добавете следното към блока `<script>` точно над `async function onConnectButtonClick()`:

{% highlight HTML %}
<script>
// Настройка на Web Serial с помощта на serial.js
const serial = new Serial();
serial.on(SerialEvents.CONNECTION_OPENED, onSerialConnectionOpened);
serial.on(SerialEvents.CONNECTION_CLOSED, onSerialConnectionClosed);
serial.on(SerialEvents.DATA_RECEIVED, onSerialDataReceived);
serial.on(SerialEvents.ERROR_OCCURRED, onSerialErrorOccurred);

function onSerialErrorOccurred(eventSender, error) {
console.log("onSerialErrorOccurred", error);
}

function onSerialConnectionOpened(eventSender) {
console.log("onSerialConnectionOpened", eventSender);
}

function onSerialConnectionClosed(eventSender) {
console.log("onSerialConnectionClosed", eventSender);
}

function onSerialDataReceived(eventSender, newData) {
console.log("onSerialDataReceived", newData);
}

async function onConnectButtonClick() {
console.log("Connect button clicked!");
}
</script>
{% endhighlight HTML %}

Въпреки че можете да запазите и презаредите уеб страницата в този момент, нищо забележимо няма да се случи, защото все още не сме свързали обекта `Serial` с бутона за свързване. Нека да го направим сега. Актуализирайте `onConnectButtonClick()`, за да се свържете и отворите сериен порт. 

{% highlight JavaScript %}
async function onConnectButtonClick() {
console.log("Натиснат бутон за свързване!");

if (navigator.serial) {
if (!serial.isOpen()) {
await serial.connectAndOpen();
} else {
console.log("Серийната връзка изглежда вече отворена");
}

} else {
alert("Web Serial API не изглежда поддържан от този уеб браузър.");
}
}
{% endhighlight JavaScript %}

Сега запазете и презаредете. С вашия Arduino включен към компютъра, опитайте да кликнете върху бутона "Свързване чрез сериен порт". След като кликнете върху бутона, уеб браузърът ще изброи всички налични серийни устройства и ще поиска разрешение от потребителя. Трябва да изглежда нещо като това:

<video autoplay loop muted playsinline style="margin:0px">
<source src="assets/videos/SliderOutScreenRecording_ButtonJustHookedUp-Optimized.mp4" type="video/mp4" />
</video>

#### Добавете и свържете плъзгач

Накрая, нека добавим и свържем интерактивен плъзгач, за да избираме и изпращаме стойности между 0 и 255 като текст през сериен порт. Плъзгачите се задават като [`<input type="range">`](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input/range) в HTML.

Под нашия `<button>` HTML в `<body>`, добавете плъзгача. Ще определим минимална, максимална и начална стойност, както и функция за обратно извикване, когато стойността на плъзгача се промени.

{% highlight HTML %}
<button id="connect-button" onclick="onConnectButtonClick()">Свързване чрез сериен порт</button>
<input id="slider" type="range" min="0" max="255" 
value="128" onchange="onSliderValueChanged(this, event)" />
{% endhighlight HTML %}

Сега, в блока `<script>`, добавете метода `onSliderValueChanged()`. В тази функция ще вземем новата стойност (`src.value`) и ще я предадем като низ чрез `serial.writeLine(src.value)`.

{% highlight JavaScript %}
async function onSliderValueChanged(src, event) {
console.log("Writing to serial: ", src.value.toString());
serial.writeLine(src.value);
}
{% endhighlight JavaScript %}

И това е всичко! Напълно работеща демонстрация на Web Serial, която трябва да изглежда нещо като това:

<video autoplay loop muted playsinline style="margin:0px">
<source src="assets/videos/SliderOutSuperBasic-Optimized.mp4" type="video/mp4" />
</video>
**Видео.** Дали просто залепих Arduino + breadboard на екрана на компютъра си, за да направя това видео? Да, точно така!
{: .fs-1 }

#### Полиране на интерфейса

Можем да направим няколко актуализации на потребителския интерфейс, за да го полираме. Първо, нека **скрием** бутона за свързване, след като успешно се свържем със сериала. За целта ще променим стила на показване на бутона на `none` във функцията `onSerialConnectionOpened()`:

{% highlight JavaScript %}
function onSerialConnectionOpened(eventSender) {
console.log("onSerialConnectionOpened", eventSender);
document.getElementById("connect-button").style.display = "none";
}
{% endhighlight JavaScript %}

Второ, нека покажем стойността на джаджата на плъзгача на уеб страницата. За целта трябва да добавим следното към HTML:

{% highlight HTML %}
<h1>Стойност на плъзгача: <span id="slider-value">0</span></h1>
{% endhighlight HTML %}

След това модифицирайте метода `onSliderValueChanged()`:

{% highlight JavaScript %}
async function onSliderValueChanged(src, event) {
console.log("Записване в сериен порт: ", src.value.toString());
serial.writeLine(src.value);

// Актуализирайте текста на стойността на плъзгача
document.getElementById("slider-value").textContent = src.value;
}
{% endhighlight JavaScript %}

Трябва също да инициализираме `slider-value` textContent при първоначалното зареждане на страницата, за да синхронизираме джаджата на плъзгача и текстовото представяне. Някъде в горната част на блока `<script>` добавете:

{% highlight JavaScript %}
// Получаване на текущата стойност на плъзгача и задаването й като текстово изходно съдържание на плъзгача
let sliderVal = document.getElementById("slider").value;
document.getElementById("slider-value").textContent = sliderVal;
{% endhighlight JavaScript %}

Накрая, нека обгърнем всички интерактивни контроли (с изключение на бутона за свързване) в техния собствен `<div>` с `id=interactive-controls` и да ги покажем само когато успешно се свържем със сериала. Така `<div>` започва скрит, което се задава с `style="display:none"`.

{% highlight HTML %}
<div id="interactive-controls" style="display:none">
<h1>Стойност на плъзгача: <span id="slider-value">0</span></h1>
<input id="slider" type="range" min="0" max="255" 
value="128" onchange="onSliderValueChanged(this, event)" />
</div>
{% endhighlight HTML %}

Сега променете програмно стила `interactive-controls` на `display:block`, когато се установи връзка:

{% highlight JavaScript %}
function onSerialConnectionOpened(eventSender) {
console.log("onSerialConnectionOpened", eventSender);
document.getElementById("connect-button").style.display = "none";
document.getElementById("interactive-controls").style.display = "block";
}
{% endhighlight JavaScript %}

<!-- TODO: добавете дебъг html-съобщенията? -->

#### Пълно видео демонстрация на слайдера

Ето пълно видео демонстрация на това как трябва да изглежда:

<video autoplay loop muted playsinline style="margin:0px">
<source src="assets/videos/SimpleSerialIn-JavaScript-SliderOut-TrimmedAndSpedUp720p.mp4" type="video/mp4" />
</video>
**Видео.** Изпълнение на демонстрацията на SliderOut ([жива страница](https://makeabilitylab.github.io/p5js/WebSerial/Basic/SliderOut), [код](https://github.com/makeabilitylab/p5js/tree/master/WebSerial/Basic/SliderOut)) с [SimpleSerialIn.ino](https://github.com/ makeabilitylab/arduino/blob/master/Serial/SimpleSerialIn/SimpleSerialIn.ino) на Arduino Leonardo.
{: .fs-1 }

### Проста двупосочна уеб страница с текст

За втория и последен пример ще създадем проста уеб страница, която изпраща и получава текстови данни чрез Web Serial. Докато пишете в предоставеното текстово поле, данните се предават незабавно по сериен порт и се показват на OLED дисплея, свързан с Arduino. Arduino отразява получените данни обратно към уеб приложението, което показва този текст в блока блока "Received from Arduino” (Получено от Arduino). Приложението изглежда така:

<video autoplay loop muted playsinline style="margin:0px">
<source src="assets/videos/DisplaySerialTextIn-QuickSnippet-Optimized.mp4" type="video/mp4" />
</video>
**Видео.** Изпълнение на демонстрацията DisplayText ([жива страница](https://makeabilitylab.github.io/p5js/WebSerial/Basic/DisplayText/) , [код](https://github.com/makeabilitylab/p5js/tree/master/WebSerial/Basic/DisplayText)) с [DisplayTextSerialIn.ino](https://github.com/makeabilitylab/arduino/blob/master/Serial/DisplayTextSerialIn/DisplayTextSerialIn.ino) на Arduino Leonardo.
{: .fs-1 }

За нашата верига и окабеляване ни е необходим само Arduino и [OLED дисплей](../advancedio/oled.md).
! [](assets/images/ArduinoLeonardo_OLEDDisplayWiring.png)

#### Създаване на нова папка и страница index.html

Както и преди, създайте нова папка (ние ще наречем нашата `DisplayText`) и файл `index.html` с начален HTML код.

{% highlight HTML %}
<!DOCTYPE html>
<html>
<head>
<title>Web Serial Demo</title>
<script src="https://cdn.jsdelivr.net/gh/makeabilitylab/p5js/_libraries/serial.js"></script>
</head>

<body>

</body>
</html>
{% endhighlight HTML %}

#### Добавете бутон за свързване и начален интерфейс

В тялото добавете бутон за свързване и начален интерфейс:

{% highlight HTML %}
<body>
<div id="main-content">
<button id="connect-button" onclick="onButtonConnectToSerialDevice()">
Свързване чрез сериен порт
</button>
<div id="text-interface">
<h3>Въведете текст:</h3>
<input placeholder="Въведете текст" name="input-text" />

<h3>Показване на текст:</h3>
<p id="output-text"></p>

<h3>Получено от Arduino:</h3>
<p id="received-text"></p>
</div>
</div>
</body>
{% endhighlight HTML %}

Запазете и отворете с Live Server. Трябва да изглежда така:

![](assets/images/DisplayTextWebPage_InitialUI.png)

#### Свържете бутона за свързване и сериен порт

Сега нека свържем бутона за свързване и добавим първоначалния код за Web Serial — и двете ще бъдат същите като преди. Добавете блок `<script>` в `<body>`:

{% highlight HTML %}
<script>
// Настройте Web Serial с помощта на serial.js
const serial = new Serial();
serial.on(SerialEvents.CONNECTION_OPENED, onSerialConnectionOpened);
serial.on(SerialEvents.CONNECTION_CLOSED, onSerialConnectionClosed);
serial.on(SerialEvents.DATA_RECEIVED, onSerialDataReceived);
serial.on(SerialEvents.ERROR_OCCURRED, onSerialErrorOccurred);

async function onButtonConnectToSerialDevice() {
console.log("onButtonConnectToSerialDevice");
if (!serial.isOpen()) {
await serial.connectAndOpen();
}
}

function onSerialErrorOccurred(eventSender, error) {
console.log("onSerialErrorOccurred", error);
}

function onSerialConnectionOpened(eventSender) {
console.log("onSerialConnectionOpened", eventSender);
}

function onSerialConnectionClosed(eventSender) {
console.log("onSerialConnectionClosed", eventSender);
}

function onSerialDataReceived(eventSender, newData) {
console.log("onSerialDataReceived", newData);
}

async function onConnectButtonClick() {
console.log("Натиснат бутон за свързване!");
}
</script>
{% endhighlight HTML %}

#### Свързване на слушател на събития към текстовото поле

В нашето уеб приложение може би сте забелязали, че нямаме бутон "Изпрати". Вместо това текстовите данни се изпращат веднага, когато потребителят въведе текст в текстовото поле. За да постигнем това, трябва да свържем слушател на събития към текстовото поле. Ще накараме слушателя на събития да извика нашата функция `updateOutputText(e)` при всяко ново въвеждане. Вътре в `updateOutputText` ще изпратим текстовите данни до Arduino чрез сериен порт и ще актуализираме `<p id="output-text"></p>` с изпратения текст.

Така че добавете следното в началото на нашия `<script>`:

{% highlight HTML %}
<script>
const inputText = document.querySelector("input");
const outputText = document.getElementById("output-text");

inputText.addEventListener("input", updateOutputText);

// Извиква се автоматично, когато текстовото поле за въвеждане се актуализира
function updateOutputText(e) {
outputText.textContent = e.target.value;
serialWriteTextData(e.target.value);
}

// Изпращане на текстови данни през сериен порт
async function serialWriteTextData(textData) {
if (serial.isOpen()) {
console.log("Записване в сериен порт: ", textData);
serial.writeLine(textData);
}
}
...
</script>
{% endhighlight HTML %}

#### Актуализирайте received-text с данни, получени от Arduino

Накрая, трябва да изслушаме данните, получени обратно от Arduino, и да актуализираме `<p id="received-text"></p>`. Добавете две допълнения към съществуващия скрипт:

{% highlight HTML %}
<script>
// Добавете това
const rcvdText = document.getElementById("received-text");

...

// И актуализирайте textContent на "received-text", когато се получат нови данни
function onSerialDataReceived(eventSender, newData) {
console.log("onSerialDataReceived", newData);
rcvdText.textContent = newData;
}
...
</script>
{% endhighlight HTML %}

В този момент трябва да можете да стартирате уеб приложението и да го свържете с Arduino. Опитайте го! Можем също да подобрим приложението с две актуализации на потребителския интерфейс.

#### Скриване на потребителския интерфейс, докато се установи серийна връзка

Когато се установи серийна връзка, ще скрием бутона за свързване и ще покажем интерфейса за въвеждане на текст:

{% highlight HTML %}
function onSerialConnectionOpened(eventSender) {
console.log("onSerialConnectionOpened");
document.getElementById("connect-button").style.display = "none";
document.getElementById("text-interface").style.display = "block";
}
{% endhighlight HTML %}

#### Добавете CSS

Ще подобрим и нашия потребителски интерфейс с някои основни CSS. В рамките на проекта `DisplayText` създайте папката `css` и CSS файла `styles.css` и въведете:

{% highlight CSS %}
#main-content {
margin: auto;
width: 800px;
border: 3px solid rgb(216, 216, 216);
padding: 10px;
}

input{
min-width: 400px;
}

#text-interface{
display: none;
}
{% endhighlight CSS %}

След това, в `index.html` добавете следното към `<head>`, за да свържете CSS.

{% highlight HTML %}
<head>
...
<link rel="stylesheet" href="css/styles.css">
...
</head>
{% endhighlight HTML %}

Успяхте! Сега играйте и експериментирайте!

#### Пълно видео демо на DisplayText

<video autoplay loop muted playsinline style="margin:0px">
<source src="assets/videos/DisplaySerialTextIn-FullSpedUp-Optimized.mp4" type="video/mp4" />
</video>
**Видео.** Пълна демонстрация на DisplayText ([жива страница](https://makeabilitylab.github.io/p5js/WebSerial/Basic/DisplayText/), [код](https://github.com/makeabilitylab/p5js/tree/master/WebSerial/Basic/DisplayText)) с [DisplayTextSerialIn.ino](https://github.com/makeabilitylab/arduino/blob/master/Serial/DisplayTextSerialIn/DisplayTextSerialIn.ino) на Arduino Leonardo.
{: .fs-1 }

## Дейност

За вашите дневници за прототипиране, модифицирайте или създайте своя собствена малка уеб приложение за комуникация с Arduino. Разбира се, можете също да напишете персонализиран Arduino код за получаване и анализиране на данни или за предаване на персонализирани данни. Заснемете видео, добавете линк към кода си и напишете кратко описание и размисли.

## Ресурси

- [Web Serial API Living Document](https://wicg.github.io/serial/), w3c Community Group Draft Report

- [Четене и записване на сериен порт от уеб](https://web.dev/serial/), François Beaufort

## Следващ урок

В [следващия урок](p5js-serial.md) ще покажем как да използвате [p5js](https://p5js.org/) с Web Serial. Ще бъде много забавно!

<span class="fs-6">
[Предишен: Въведение в Serial](serial-intro.md){: .btn .btn-outline }
[Следващ: Използване на p5js с Web Serial](p5js-serial.md){: .btn .btn-outline }
<!-- [Следващ: Използване на потенциометри](potentiometers.md){: .btn .btn-outline } -->
</span>
