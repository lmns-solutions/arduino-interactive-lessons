---
lang: bg
permalink: /communication/handpose-serial.html
page_id: communication-handpose-serial
layout: default
title: L7&#58; Сериен интерфейс за позиция на ръката
nav_order: 7
parent: Комуникация
has_toc: true # (по подразбиране)
comments: true
usemathjax: true
usetocbot: true
---
# { { page.title }}
{: .no_toc }

## Съдържание
{: .no_toc .text-delta }

1. Съдържание
{:toc}
---

В [предходния урок](ml5js-serial.md) представихме комбинирането на Arduino с библиотеки за машинно обучение (ML) като [ml5.js](https://ml5js.org/), уеб-базирана ML библиотека, изградена върху [Google TensorFlow](https://www.tensorflow.org/js) . По-конкретно, създадохме [p5.js приложение](https://makeabilitylab.github.io/p5js/WebSerial/ml5js/NoseTracker/), което подаваше поток от уеб камера в реално време към [ml5's PoseNet](https://learn.ml5js.org/#/reference/posenet), за да идентифицира и класифицира части от човешкото тяло (ключови точки) и изпраща идентифицираните ключови точки към нашия Arduino, за да създаде нови интерактивни преживявания.

В този урок ще представим нов ml5 модел, наречен [Handpose](https://learn.ml5js.org/#/reference/handpose), който точно проследява ръката и 20 ключови точки на пръстите в 3 измерения, и ще го използваме за управление на серво мотор. Този урок ще ви помогне да задълбочите разбирането си за използването на [ml5](https://ml5js.org/), как да модулирате и изградите ml5+Arduino приложение стъпка по стъпка, и се надяваме да ви вдъхнови да помислите как можем да комбинираме ML в реално време с Arduino.

<!-- който е пренесен от [модела TensorFlow Handpose на Google](https://github.com/tensorflow/tfjs-models/tree/master/handpose), -->

<video autoplay loop muted playsinline style="margin:0px">
<source src="assets/videos/HandPose_Optimized_1200w.mp4" type="video/mp4" />
</video>
**Видео.** Кратка демонстрация на [ml5's Handpose](https://learn.ml5js.org/ #/reference/handpose), както е имплементирана в нашето приложение за пример, наречено [HandWaveDetector](https://makeabilitylab.github.io/p5js/ml5js/HandPose/HandWaveDetector) ([code](https://github.com/makeabilitylab/p5js/tree/master/ml5js/HandPose/HandWaveDetector)).
{: .fs-1 }

## Поза на ръката

През март 2020 г. [екипът на Google TensorFlow.js](https://blog.tensorflow.org/2020/03/face-and-hand-tracking-in-browser-with-mediapipe-and-tensorflowjs.html) пусна два невероятни пакета за проследяване на лица и ръце в уеб среда, озаглавени [FaceMesh](https:// www.npmjs.com/package/@tensorflow-models/facemesh) (сега [face-landmarks-detection](https://github.com/tensorflow/tfjs-models/tree/master/face-landmarks-detection)) и [HandPose](https://github.com/tensorflow/tfjs-models/tree/master/handpose) . Скоро след това един потребител направи [заявка за нова функция](https://github.com/ml5js/ml5-library/issues/823) за поддръжка на тези нови пакети с ml5. До ноември 2020 г. тя беше имплементирана в ml5 от [Bomani Oseni McClendon](https://github.com/bomanimc) като част от [ml5.js Fellows Program](https:/ /medium.com/processing-foundation/announcing-our-2020-ml5-js-fellows-45f8f6ff378d)).

<video autoplay loop muted playsinline style="margin:0px">
<source src="assets/videos/HandPoseFaceMesh_Optimized.mp4" type="video/mp4" />
</video>
**Видео.** Демонстрация на [FaceMesh](https://github.com/tensorflow/tfjs-models/tree/master/face-landmarks-detection) и [HandPose] на TensorFlow.js (https://github.com/tensorflow/tfjs-models/tree/master/handpose) на TensorFlow.js, които са достъпни в ml5 като [Facemesh](https://learn.ml5js.org/#/reference/facemesh) и [Handpose](https://learn.ml5js.org/#/reference/handpose). Видео от [блога на TensorFlow.js](https://blog.tensorflow.org/2020/03/face-and-hand-tracking-in-browser-with-mediapipe-and-tensorflowjs.html).
{: .fs-1 }

В този урок ще се фокусираме върху [HandPose](https://learn.ml5js.org/#/reference/handpose), а не върху [FaceMesh](https://learn.ml5js.org/#/reference/facemesh) (въпреки че и двете са налични в ml5) . Можете да използвате [TensorFlow.js implementation](https://github.com/tensorflow/tfjs-models/tree/master/handpose), [Google's MediaPipe version](https://google.github.io/mediapipe/solutions/hands) или [ml5's version](https://learn.ml5js.org/#/ reference/handpose). И трите реализации използват един и същ предварително обучен ML модел. За този урок ще използваме [HandPose на ml5](https://learn.ml5js.org/#/reference/handpose). Ето няколко примера за демонстрации на трите реализации, които се изпълняват във вашия уеб браузър:

- [Демонстрация на проследяване на ръцете на Google MediaPipe](https://codepen.io/mediapipe/pen/RwGWYJw)
- [Демонстрационно приложение на Google MediaPipe: Hand Defrosting](https://codepen.io/mediapipe/pen/bGweWyR)
- [Демонстрация на HandPose на Google TensorFlow](https://storage.googleapis.com/tfjs-models/demos/handtrack/index.html)
- [Демонстрация на ml5 HandPose в уеб редактора p5.js](https://editor.p5js.org/ml5/sketches/Handpose_Webcam)

### Модел HandPose

През 2019 г. изследователите Маргарет Мичъл, Тимнит Гебру и колегите им публикуваха статия, озаглавена [*Model Cards for Model Reporting*](https:// arxiv.org/pdf/1810.03993.pdf), в която призоваха API-та, базирани на ML, да предоставят прозрачна информация за *начина*, по който е обучен основният ML модел в API, и очакваните контексти на употреба. Статията започва с важна мотивация, която подчертава как ML започва да прониква във всеки аспект от живота с сериозни последствия:

> Обучените модели за машинно обучение се използват все по-често за изпълнение на задачи с голямо въздействие в области като правоприлагане, медицина, образование и заетост. За да се изяснят предвидените случаи на употреба на моделите за машинно обучение и да се сведе до минимум тяхното използване в контексти, за които не са подходящи, препоръчваме пуснатите модели да бъдат придружени от документация, в която подробно се описват техните характеристики на работа.
{: .fs-4 }

След това те предлагат рамка, наречена „моделни карти“, за стандартизиране на начина, по който компаниите докладват за ML моделите:

> В тази статия предлагаме рамка, която наричаме **моделни карти**, за да насърчим такова прозрачно отчитане на моделите. Моделните карти са кратки документи, придружаващи обучените модели за машинно обучение, които предоставят сравнителна оценка в различни условия, като например различни културни, демографски или фенотипни групи (*например* раса, географско местоположение, пол, тип кожа по Fitzpatrick [[15](https://pubmed.ncbi.nlm.nih.gov/ 3377516/)]) и интерсекционални групи (*например* възраст и раса или пол и тип кожа по Фицпатрик), които са свързани с предвидените области на приложение. Моделните карти разкриват също контекста, в който моделите са предназначени да се използват, подробности за процедурите за оценка на ефективността и друга свързана информация.
{: .fs-4 }

Тази статия и съответните изследователи, които са я написали, са оказали значително влияние върху ML общността. Като доказателство за това, много от Google ML API и моделите вече предоставят „моделни карти“. Ето моделната карта за [HandPose](https://drive.google.com/file/d/1sv4sSb9BSNVZhLzxXJ0jBv9DqD-4jnAz/view) ([местна копия](../assets/datasheets/GoogleTensorFlow_ModelCard_HandPose.pdf))—забележително е, че не успях да намеря такава за [PoseNet](https://github.com/tensorflow/tfjs-models/tree/master/posenet).

По-долу обобщаваме няколко важни бележки за модела HandPose.

#### Спецификации на модела

HandPose се състои от два леки модела, детектор на дланта и модел на ориентири на ръката, за да открива и класифицира ключови точки на ръката. Моделът въвежда изображение или видео кадър, променя размера на въведеното до 256x256 за разпознаване и извежда:
- ограничаваща кутия на дланта,
- 21 триизмерни ориентира на ръката (ключови точки) и
 
- обща оценка на достоверността за откриването на ръката 

21-те ключови точки включват по четири за `палеца`, `показалеца`, `средния пръст`, `безименния пръст` и `малкия пръст`, плюс още една за `основата на дланта`:

![](assets/images/HandPose_Keypoints_FromGoogleMediaPipe.png)
**Фигура.** Ключовите точки на HandPose от [екипа на MediaPipe](https://google.github.io/mediapipe/solutions/hands).
{: .fs-1 }

Действителните индекси на ключовите точки от TensorFlow имплементацията, която ml5 използва:

{% highlight TypeScript %}
export const MESH_ANNOTATIONS: {[key: string]: number[]} = {
thumb: [1, 2, 3, 4],
indexFinger: [5, 6, 7, 8],
middleFinger: [9, 10, 11, 12],
ringFinger: [13, 14, 15, 16],
pinky: [17, 18, 19, 20],
palmBase: [0]
};
{% endhighlight TypeScript %}

**Код.** Източник от [keypoints.ts](https://github.com/tensorflow/tfjs-models/blob/master/handpose/src/keypoints.ts) в [репозиторията на моделите на TensorFlow] (https://github.com/tensorflow/tfjs-models).
{: .fs-1 }

Според [екипа на TensorFlow](https://github.com/tensorflow/tfjs-models/tree/master/handpose), HandPose е подходящ за извличане на заключения в реално време на различни устройства, като постига 40 FPS на MacBook Pro 2018, 35 FPS на iPhone11 и 6 FPS на Pixel3.

#### Ограничения на модела и етични съображения

По отношение на ограниченията и етичните съображения, [картата на модела HandPose](https://drive.google.com/file/d/1sv4sSb9BSNVZhLzxXJ0jBv9DqD-4jnAz/view) уточнява, че моделите HandPose са обучени на ограничен набор от данни и не са подходящи за преброяване на ръцете в тълпа, откриване на ръце с ръкавици или затъмнения, или откриване на ръце, които са далеч от камерата (повече от ~2 метра).

Освен това, моделната карта ясно посочва, че моделът HandPose не е предназначен за вземане на решения, които са от жизненоважно значение, и че ефективността му варира в зависимост от цвета на кожата, пола, възрастта и условията на околната среда (*например* слаба осветеност).

Важно е да се отбележи, че подобно на [PoseNet](https://learn.ml5js.org/#/reference/posenet), който използвахме в [предходния урок] (ml5js-serial.md), **открива** ключови точки на позата на тялото, но **не** се опитва да **разпознае** *кой* е на изображението, HandPose също извършва откриване, но не се опитва да разпознае (т.е. *кой* е собственикът на откритата ръка). В компютърното зрение има важна разлика между *откриване* и *разпознаване*. Всички откривания се извършват локално в уеб браузъра на потребителя (а не в облака).

<!-- Моделът HandPose открива ръце в изображение или видео поток и връща двадесет и един триизмерни ориентира (ключови точки), които локализират характеристики във всяка ръка. По-конкретно, -->

## ml5 HandPose

Моделът ml5 HandPose работи по подобен начин като версиите [TensorFlow.js](https://github.com/tensorflow/tfjs-models/tree/master/handpose) и [ MediaPipe](https://google.github.io/mediapipe/solutions/hands); обаче моделът ml5 поддържа само **една** ръка едновременно.

## # Структурата на данните на HandPose

Точно както при [PoseNet](ml5js-serial.md#the-posenet-data-structure), API-тата на TensorFlow и ml5 HandPose използват една и съща структура на данните. Моделът връща масив от обекти, описващи всяка открита ръка (понастоящем винаги една в случая на ml5). Всеки обект „ръка“ включва четири елемента:
- `handInViewConfidence`, което е увереността на модела, че ръката действително съществува
- `boundingBox`, което предоставя позициите `topLeft` x,y и `bottomRight` x,y на откритата ръка
- масив `landmarks`, който включва 3D (x,y,z) координатите на всяка ориентир (ключова точка) на ръката
- масив `annotations`, който предоставя същите 3D координати като `landmarks`, но семантично групирани в `thumb`, `indexFinger`, `middleFinger`, `ringFinger`, `pinky` и `palmBase`

Структурата на масива изглежда така:

{% highlight JavaScript %}
[
{
handInViewConfidence: 1, // Вероятността за наличие на ръка.
boundingBox: { // Ограждащата кутия около ръката.
topLeft: [162.91, -17.42],
bottomRight: [548.56, 368.23],
},
landmarks: [ // 3D координатите на всяка отбележка на ръката.
[472.52, 298.59, 0.00],
[412.80, 315.64, -6.18],
...
],
annotations: { // Семантични групировки на координатите на `landmarks`.
палец: [
[412.80, 315.64, -6.18]
[350.02, 298.38, -7.14],
...
],
...
}
}
]
{% endhighlight JavaScript %}

За да стане по-ясно, ето екранна снимка от инструментите за разработчици на Chrome, показваща масива `predictions` (който, отново, винаги ще бъде с размер 1, защото ml5 понастоящем е ограничен до откриване на една ръка едновременно). В екранната снимка съм разширил масива, за да покажа споменатата по-горе структура на високо ниво на `handInViewConfidence`, `boundingBox`, `landmarks` и `annotations`.

![](assets/images/HandPose_ChromeDevToolsScreenshot.png)
* *Фигура.** Тази фигура показва екранна снимка на масива „predictions“ на HandPose и основните обекти, както се показват в инструментите за разработчици на Chrome. Кликнете с десния бутон и изберете „Отвори изображение в нов раздел“, за да го увеличите. Приложението, което се изпълнява тук, е нашето [HandPoseDemo](https://makeabilitylab.github.io/p5js/ ml5js/HandPose/HandPoseDemo/). Можете също да разгледате модела интерактивно: стартирайте [HandPoseDemo](https://makeabilitylab.github.io/p5js/ml5js/HandPose/HandPoseDemo/), отворете `sketch.js` в Източници, поставете точка на прекъсване на функцията `onNewHandPosePrediction()` и добавете масива `predictions` към списъка `Watch`. Разглеждане на структури от данни като тази може да ви помогне да разберете по-добре и е чудесна стратегия за уеб разработка.
{: .fs-1 }

### Пример p5.js + ml5. js HandPose demo

За да демонстрираме ml5.js HandPose API и как да преминем през структурата на данните, създадохме проста приложение, наречено [HandPoseDemo](https://makeabilitylab.github.io/p5js/ml5js/HandPose/HandPoseDemo/), което визуализира:

- `boundingBox`, върнат от API, заедно с „по-тясна“ версия, която изчисляваме ръчно въз основа на ключови точки
- резултата `handInViewConfidence`, който изчертаваме над „стегнатия“ ограничаващ правоъгълник
- 21-те `landmarks` (ключови точки) за `thumb`, `indexFinger`, `middleFinger`, `ringFinger`, `pinky` и `palmBase` заедно с текстови етикети

Тази структура на данни е подобна, но не идентична с [PoseNet](ml5js-serial.md#the-posenet-data-structure) – една от основните разлики е, че за разлика от PoseNet, отделните ключови точки не включват конкретни оценки за достоверност. Ето кратко видео демонстрация.

<video autoplay loop muted playsinline style="margin:0px">
<source src="assets/videos/HandPoseDemo-GrayBackdrop_TrimmedAndOptimized.mp4" type="video/mp4" />
</video>
**Видео.** [HandPoseDemo](https://makeabilitylab.github.io/p5js/ml5js/HandPose/HandPoseDemo/) ([код](https://github.com/makeabilitylab/p5js/tree/master/ml5js/HandPose/HandPoseDemo) в GitHub). Можете също да разглеждате, редактирате и играете с кода в [уеб редактора p5.js](https://editor.p5js.org/jonfroehlich/sketches/Nn4pXTpbu).
{: .fs-1 }

Пуснахме HandPoseDemo в уеб редактора p5.js ([линк](https://editor.p5js.org/jonfroehlich/sketches/Nn4pXTpbu) ). Препоръчваме ви да разгледате кода, да го редактирате и да си поиграете с него. Демонстрацията е достъпна и в GitHub ([страница на живо](https://makeabilitylab.github.io/p5js/ml5js/HandPose/HandPoseDemo), [код](https://github.com/makeabilitylab/p5js/tree/master/ml5js/HandPose/HandPoseDemo)).

## Създаване на ml5 HandPose + Arduino приложение: HandWaver

За да подчертаем потенциала на ML в реално време и Arduino, ще създадем прост „роботизиран“ махач с ръка. Ще използваме HandPose API на ml5, за да усетим ръката на потребителя, която след това ще контролира серво мотор, вграден в фигура, изработена от картон. Вижте краткото представяне по-долу.

<video autoplay loop muted playsinline style="margin:0px">
<source src="assets/videos/HenryBodySerial_HenryStanding_TrimmedAndOptimized.mp4" type="video/mp4" />
</video>
**Видео.** Кратка демонстрация на „Хенри, човекът с лентата“, който беше проектиран и изработен от дете от детска градина, дете от предучилищна възраст и мен. Фронтендът, базиран на JavaScript, е изграден с приложението p5+ml5, наречено [HandWaver] (https://github.com/makeabilitylab/p5js/tree/master/WebSerial/ml5js/HandWaver) и Arduino скицата [ServoSerialIn.ino](https://github.com/makeabilitylab/arduino/blob/master/Serial/ServoSerialIn/ServoSerialIn.ino). (Действителният Arduino sketch, който се изпълнява тук, е леко модифицирана версия, наречена [ServoPotWithSerialInOLED.ino](https://github.com/makeabilitylab/arduino/blob/master/Serial/ServoPotWithSerialInOLED/ServoPotWithSerialInOLED.ino))
{: .fs-1 }

### Изграждане на уеб приложението

Ще започнем с изграждането на уеб приложението в [p5.js](https://p5js.org/) и [ml5](https://ml5js.org/) . Както обикновено, ще започнем с [шаблона за уеб сериен интерфейс](https://github.com/makeabilitylab/p5js/tree/master/WebSerial/p5js/SerialTemplate), тъй като ще комуникираме между ml5 и Arduino чрез уеб сериен интерфейс:

- Ако използвате VSCode, копирайте [`SerialTemplate`](https://github.com/makeabilitylab/p5js/tree/master/WebSerial/p5js/SerialTemplate) и преименувайте папката на `HandWaver`.
- Ако използвате онлайн редактора p5.js, просто отворете [Serial Template](https://editor.p5js.org/jonfroehlich/sketches/vPfUvLze_C) и преименувайте проекта си на `HandWaver`.

### # Добавете и инициализирайте HandPose на ml5

Библиотеката ml5 като цяло има за цел да създаде последователност в своите API. По този начин API-то HandPose на ml5 би трябвало да ви е познато, ако сте следвали предишния ни [урок за PoseNet](ml5js-serial.md). Подобно на [PoseNet](https://learn.ml5js.org/#/reference/posenet), конструкторът `ml5.handpose` приема три опционални аргумента `video`, `options` и `callback` (обозначени с префикса `?`):

{% highlight JavaScript %}
const handpose = ml5.handpose(?video, ?options, ?callback);
{% endhighlight JavaScript %}

- `video`: Незадължителен [HTMLVideoElement](https://developer.mozilla.org/en-US/docs/Web/API/HTMLVideoElement), който можем да получим в p5.js просто чрез извикване на [`createCapture(VIDEO)`](https://p5js.org/reference/#/p5/createCapture).

- `options`: Незадължителен обект от свойствата за конфигуриране на PoseNet. Вижте по-долу.

- `callback`: Незадължителна препратка към callback функция, която се извиква, когато моделът се зареди.

Конфигурационните `options` са изброени по-долу (с показани стойности по подразбиране). Можете и трябва да експериментирате с тези опции в зависимост от нуждите на вашето приложение.

{% highlight JavaScript %}
const options = {
flipHorizontal: false, // булева стойност за това дали видеото трябва да се обърне, по подразбиране е false
maxContinuousChecks: Infinity, // Колко кадри да минат, без да се изпълнява детекторът на ограничаващия правоъгълник 
detectionConfidence: 0.8, // [0, 1] праг за отхвърляне на прогноза
scoreThreshold: 0.75, // [0, 1] праг за премахване на дублирани откривания чрез „немаксимално потискане“
 
iouThreshold: 0.3, // [0, 1] праг за определяне дали кутиите се припокриват при немаксимално потискане
}
{% endhighlight JavaScript %}

Вижте също: [документацията на TensorFlow тук](https://github.com/tensorflow/tfjs-models/tree/master/handpose#parameters-for-handposeload).

За да инициализираме и създадем обект `ml5.handpose`, пишем:

{% highlight JavaScript %}
let handPoseModel; // съхранява модела, върнат от конструктора ml5.handpose
let video; // видео потока createCapture
let curHandPose = null; // текущата поза на ръката (ml5 поддържа само една по едно време)
let isHandPoseModelInitialized = false; // дали моделът на позата на ръката е инициализиран

function setup() {
createCanvas(640, 480);
video = createCapture(VIDEO);
video.hide();
handPoseModel = ml5.handpose(video, onHandPoseModelReady);
}

function onHandPoseModelReady() {
console.log(„HandPose model ready!“);
isHandPoseModelInitialized = true;
}
{% endhighlight JavaScript %}

Отново, това би трябвало да ви е познато! Дотук е доста подобно на нашия [урок за PoseNet](ml5js-serial.md#initialize-ml5s-posenet).

#### Абонирайте се за новото събитие HandPose

Също като [PoseNet](https://learn.ml5js.org/#/reference/posenet), можем да се абонираме за „ново събитие за поза” чрез функцията `on`, като предаваме името на събитието `predict`:

{% highlight JavaScript %}
handpose.on(„predict“, callback);
{% endhighlight JavaScript %}

Така че, нашият пълен код за инициализация + абонамент за HandPose е:

{% highlight JavaScript %}
let handPoseModel;
let video;
let curHandPose = null;
let isHandPoseModelInitialized = false;

function setup() {
createCanvas(640, 480);
video = createCapture(VIDEO);
video.hide();
handPoseModel = ml5.handpose(video, onHandPoseModelReady);
handPoseModel.on(„predict“, onNewHandPosePrediction);
}

function onHandPoseModelReady() {
console.log(„HandPose model ready!“);
isHandPoseModelInitialized = true;
}

function onNewHandPosePrediction(predictions) {
if (predictions && predictions.length > 0) {
curHandPose = predictions[0];
console.log(curHandPose);
} else {
curHandPose = null;
}
}
{% endhighlight JavaScript %}

Можете да видите, да си играете и да редактирате [този код](https://editor.p5js.org/jonfroehlich/sketches/7q-M3hpvr) в онлайн редактора p5.js. Но все още няма много неща там!

#### Добавете код за рисуване

Сега идва забавната част! Да добавим код за рисуване, за да визуализираме три неща:
- **21 ключови точки на HandPose** като кръгове (в нова функция, наречена `drawHand()`), 
- **ограничаваща кутия** с обща оценка на достоверността на ръката (в функция, наречена `drawBoundingBox()`), и 
- **удобен текст**, който да информира потребителя за инициализирането на модела („Чакане за зареждане на модела... .").

Първо, нека актуализираме функцията `draw()`, за да покаже удобен текст, докато моделът все още се зарежда, и да извика функциите за рисуване на ключовите точки на ръката и ограничаващия правоъгълник (ако ръката е била открита):

{% highlight JavaScript %}
function draw() {
image(video, 0, 0, width, height);

if(!isHandPoseModelInitialized){ // ако моделът на ръката все още не е инициализиран, покажете текста „зареждане на модела“
background(100);
push();
textSize(32);
textAlign(CENTER);
fill(255);
noStroke();
text(„Изчакване на зареждането на модела HandPose...“, width/2, height/2);
pop();
}

if(curHandPose){ // нарисувай ръка, ако е открита
drawHand(curHandPose);
drawBoundingBox(curHandPose);
}
}
{% endhighlight JavaScript %}

Трябва да изглежда нещо като това:

![](assets/images/WaitingForHandPoseModelToLoadScreenshot.png)
**Фигура.** Показване на текста „Изчакване на зареждането на модела HandPose...“ в [редактора p5.js](https://editor.p5js.org/jonfroehlich/sketches/YVRlHlR0I).
{: .fs-1 }

Сега да добавим функцията `drawHand(handPose)`. Ще преминем през всички 21 ориентира (ключови точки) и ще нарисуваме зелен кръг на тяхната x,y позиция (съхранена в индекс 0 и 1 на `landmark` съответно).

{% highlight JavaScript %}
function drawHand(handPose) {

// Начертаване на ключови точки. Въпреки че всяка ключова точка предоставя 3D точка (x, y, z), ние чертаем само точките x и y.
for (let j = 0; j < handPose.landmarks.length; j += 1) {
const landmark = handPose.landmarks[j];
fill(0, 255, 0, 200); // зелено с известна непрозрачност
noStroke();
circle(landmark[0], landmark[1], 10); // landmark[0] е x позиция, landmark[1] е y позиция
}
}
{% endhighlight JavaScript %}

Сега ръката ви трябва да има зелени кръгове, начертани върху ориентирите, както е показано тук:

![](assets/images/HandPoseKeypointsDrawninGreen.png)
**Фигура.** Начертаване на ключовите точки върху ръката. Снимка от [p5.js editor](https://editor.p5js.org/jonfroehlich/sketches/YVRlHlR0I).
{: .fs-1 }

Накрая, нека добавим функция `drawBoundingBox(handPose)`, която изобразява правоъгълник за обекта HandPose `boundingBox` заедно с неговата оценка `handInViewConfidence`:

{% highlight JavaScript %}
function drawBoundingBox(handPose){
// Нарисувай ограничаваща кутия за позата на ръката
const bb = handPose.boundingBox;
const bbWidth = bb.bottomRight[0] - bb.topLeft[0];
const bbHeight = bb.bottomRight[1] - bb.topLeft[1];
noFill();
stroke(„red“);
rect(bb.topLeft[0], bb.topLeft[1], bbWidth, bbHeight);

// Начертайте увереност
fill(„red“);
noStroke();
textAlign(LEFT, BOTTOM);
textSize(20);
text(nfc(handPose.handInViewConfidence, 2), bb.topLeft[0], bb.topLeft[1]);
}
{% endhighlight JavaScript %}

Ето екранна снимка с ключовите точки, ограничаващата кутия и увереността:

![](assets/images/HandposeKeypointsBoundingBoxAndConfidence.png)
**Фигура.** Изчертаване на ключовите точки, ограничаващата кутия и оценката за увереност на ръката. Снимка на екрана от [p5.js editor](https://editor.p5js.org/jonfroehlich/sketches/YVRlHlR0I).
{: .fs-1 }

Можете да разглеждате, редактирате и експериментирате с [този код](https://editor.p5js.org/jonfroehlich/sketches/YVRlHlR0I) в онлайн редактора p5.js.

#### Добавяне на уеб сериен код

За последната стъпка ще добавим код за предаване на нормализираната x позиция [0, 1] на `palmBase` чрез уеб сериен код. За да избегнем претоварване на уеб сериен код с данни, ще ограничим скоростта на предаване до ~20Hz (едно предаване на всеки 50ms). Накрая, нека добавим и код за рисуване, за да покажем информацията за `palmBase` на екрана (полезно за отстраняване на грешки!).
 

Първо, добавете глобална променлива:
{% highlight JavaScript %}
let palmXNormalized = 0;
let timestampLastTransmit = 0;
const MIN_TIME_BETWEEN_TRANSMISSIONS_MS = 50; // 50 ms е ~20 Hz
{% endhighlight JavaScript %}

След това актуализирайте функцията `onNewHandPosePrediction`, за да изчислите и предадете `palmXNormalized`:

{% highlight JavaScript %}
function onNewHandPosePrediction(predictions) {
if (predictions && predictions.length > 0) {
curHandPose = predictions[0];
// Вземете x-позицията на дланта и я нормализирайте до [0, 1]
const palmBase = curHandPose.landmarks[0];
const palmBaseX = palmBase[0]; // x е в palmBase[0], y е в palmBase[1]
palmXNormalized = palmBaseX / width; // нормализирайте x, като го разделите на ширината на платното

if(serial.isOpen()){
const outputData = nf(palmXNormalized, 1, 4);
 
const timeSinceLastTransmitMs = millis() - timestampLastTransmit;
if(timeSinceLastTransmitMs > MIN_TIME_BETWEEN_TRANSMISSIONS_MS){
serial.writeLine(outputData);
timestampLastTransmit = millis();
}else{
console.log(„Не изпрати „“ + outputData + „“ защото времето от последната трансмисия е “ 
+ timeSinceLastTransmitMs + „ms“);
}
}
} else {
curHandPose = null;
}
}
{% endhighlight JavaScript %}

Накрая, актуализирайте функцията `draw()`, за да нарисувате информацията за `palmBase` на екрана:

{% highlight JavaScript %}
function draw() {
...
if(curHandPose){
...
// нарисувайте информацията за дланта
noFill();
stroke(255);
const palmBase = curHandPose.landmarks[0];
circle(palmBase[0], palmBase[1], kpSize); // изчертаване на кръг около ключовата точка на дланта
noStroke();
fill(255);
text(nf(palmXNormalized, 1, 4), palmBase[0] + kpSize, palmBase[1] + textSize() / 2);
}
}
{% endhighlight JavaScript %}

И това е всичко! Тъй като нашият [`SerialTemplate`](https:// github.com/makeabilitylab/p5js/tree/master/WebSerial/p5js/SerialTemplate) вече поддържа свързване към сериен уред чрез кликване върху платното (по подразбиране) и/или автоматично свързване към предварително одобрени уеб серийни уреди, всичко е готово. Можете да добавите свой собствен код за свързване (*например ,* специфичен „бутон за свързване” за уеб сериен). Пълният код е [тук](https://editor.p5js.org/jonfroehlich/sketches/vMbPOkdzu).

![](assets/images/ScreenshotOfHandWaverFullRunningInP5OnlineEditor.png)
**Фигура. ** Снимка на екрана на HandWaver, работещ в [p5.js онлайн редактор](https://editor.p5js.org/jonfroehlich/sketches/vMbPOkdzu) . Кодът е и в GitHub ([жива страница](https://makeabilitylab.github.io/p5js/WebSerial/ml5js/HandWaver/), [код](https://github.com/makeabilitylab/p5js/tree/master/WebSerial/ml5js/HandWaver)).
{: .fs-1 }

Сега преминаваме към Arduino!

### Изграждане на Arduino

Ще изградим Arduino стъпка по стъпка. Има пет основни стъпки:

- Създаване на първоначална верига на серво мотор и тестова програма за Arduino
- Създаване на проста p5.js + тестова програма за серво с уеб сериен порт
- Създаване на интересна lo-fi форма за нашия вграден серво мотор
- Тестване на формата и веригата на серво мотора
- Създаване на цялостна система HandPose + Arduino

#### Първоначална верига на сервомотора и тестова програма за Arduino

Като кратко въведение в сервомоторите, моля, прочетете този [урок на Adafruit](https://learn.adafruit.com/adafruit-arduino-lesson-14-servo-motors) от Simon Monk. Въз основа на този урок ще създадем основна верига, която позволява на потребителя да контролира позицията на сервомотора с потенциометър. По-конкретно, ще прочетем стойността на потенциометъра на пин `A0`, използвайки [`analogRead ()`](https://www.arduino.cc/reference/en/language/functions/analog-io/analogread/), ще я преобразуваме в ъгъл между 0 и 180 и след това ще запишем ъгъла в сервомотора.

![](assets/images/BasicServoPlusPotCircuit_ArduinoLeonardo.png)
**Фигура.** Основна верига на сервомотор с пин за серво импулс, свързан към пин 9 на Arduino, и потенциометър, свързан към пин `A0`. Диаграмата е изготвена в Fritzing и PowerPoint.
{: .fs-1 }

Пълният код е:

{% highlight C++ %}
#include <Servo.h>

const int POTENTIOMETER_INPUT_PIN = A0;
const int SERVO_OUTPUT_PIN = 9;
const int MAX_ANALOG_VAL = 1023;
Servo _servo; 

void setup() 
{
_servo.attach(SERVO_OUTPUT_PIN);
}
 

void loop() 
{
// Прочитане на стойността на потенциометъра
int potVal = analogRead(POTENTIOMETER_INPUT_PIN);

// Серво моторът може да се движи между 0 и 180 градуса
int servoAngle = map(potVal, 0, MAX_ANALOG_VAL, 0, 180);

// Задаване на ъгъла на серво
_servo.write(servoAngle); 
}
{% endhighlight C++ %}

**Код.** Този код се намира в GitHub като [ServoPot.ino](https://github.com/makeabilitylab/arduino/blob/master/Basics/servo/ServoPot/ServoPot.ino).
{: .fs-1 }

Ето видео демонстрация, показваща леко модифицирана Arduino верига и скица (наречена [ServoPotOLED.ino](https://github.com/makeabilitylab/arduino/blob/master/Basics/servo/ServoPotOLED/ ServoPotOLED.ino)). Единствената разлика е, че OLED версията извежда текущия ъгъл на сервомеханизма на OLED дисплея.

<video autoplay loop muted playsinline style="margin:0px">
<source src="assets/videos/ServoMotorWithStick_TrimmedAndOptimized.mp4" type="video/mp4" />
</video>
**Видео.** Демонстрация на серво веригата с потенциометър. Видеото показва [ServoPotOLED.ino](https://github.com/makeabilitylab/arduino/blob/master/Basics/servo/ServoPotOLED/ServoPotOLED.ino), което е функционално еквивалентно на кода по-горе ([ServoPot.ino](https://github.com/makeabilitylab/arduino/blob/master/Basics/servo/ServoPot/ServoPot.ino)), но включва OLED поддръжка. Тук OLED дисплеят показва текущия ъгъл на сервомотора.
{: .fs-1 }

#### Актуализирайте кода, за да приема серийни входни данни

Нека актуализираме кода си, за да зададем ъгъла на сервомотора въз основа на **сериен вход**, а не на потенциометъра. Ще напишем малко по-гъвкав код за анализиране от обичайния. В този случай ще приемаме или редове, разделени с интервали, от целочислени стойности в диапазона от 0 до 180 включително, или плаващи стойности в диапазона от 0 до 1 включително. Ще определим дали сериен предавател е изпратил целочислена *vs.* плаваща стойност, като търсим десетична запетая в низ.

Пълен код:

{% highlight C++ %}
#include <Servo.h>

const int SERVO_OUTPUT_PIN = 9;
const int MAX_ANALOG_VAL = 1023;
const int MIN_SERVO_ANGLE = 0;
const int MAX_SERVO_ANGLE = 180;

Servo _servo; 
int _serialServoAngle = -1;

void setup() 
{ 
Serial.begin(115200);
_servo.attach(SERVO_OUTPUT_PIN);
 
}

void loop()
{
// Проверява дали има серийни данни, ако има, ги чете
if(Serial.available() > 0){
// Чете данните от серийния порт, докато стигне до крайния разделител („\n“)
// Запазва всички тези данни в низ
String rcvdSerialData = Serial.readStringUntil(„\n“);
 

// Приемаме цели числа между 0 и 180 или числа с плаваща запетая. Числата с плаваща запетая трябва да имат точка, за да бъдат разпознати
int indexOfDecimal = rcvdSerialData.indexOf(„.“);
if(indexOfDecimal != -1){
float serialServoAngleF = rcvdSerialData.toFloat();
_serialServoAngle = MIN_SERVO_ANGLE + (int)(serialServoAngleF * (MAX_SERVO_ANGLE - MIN_SERVO_ANGLE));
}else{
_serialServoAngle = rcvdSerialData.toInt();
}

_serialServoAngle = constrain(_serialServoAngle, MIN_SERVO_ANGLE, MAX_SERVO_ANGLE);

// Отразяване на данните
Serial.print(„# Arduino Received: „“);
Serial.print(rcvdSerialData);
Serial.print(„“ Converted to: “);
Serial.println(_serialServoAngle);

// Задаване на нов ъгъл на серво
_servo.write(_serialServoAngle);
}
}
{% endhighlight C++ %}

**Код.** Пълният код е тук [ServoSerialIn.ino](https://github.com/makeabilitylab/arduino/blob/master/Serial/ServoSerialIn/ServoSerialIn.ino).
{: .fs-1 }

<video autoplay loop muted playsinline style="margin:0px">
<source src="assets/videos/ServoSerialInOLED-Pot-TrimmedAndOptimized.mp4" type="video/mp4" />
</video>
**Видео.** Демонстрация на управление на серво мотор от сериен вход. Това видео използва леко модифициран скиц с OLED поддръжка, наречен [ServoSerialInOLED.ino] (https://github.com/makeabilitylab/arduino/blob/master/Serial/ServoSerialInOLED/ServoSerialInOLED.ino), но функционално е еквивалентен на [ServoSerialIn.ino](https://github.com/makeabilitylab/arduino/blob/master/Serial/ServoSerialIn/ServoSerialIn.ino).
{: .fs-1 }

Също така създадохме малко по-усъвършенствана версия, която позволява на потребителя да избира дали да използва потенциометъра или сериен вход за управление на сервомотора: [ServoPotWithSerialIn.ino](https://github.com/makeabilitylab/arduino/blob/master/Serial/ServoPotWithSerialIn/ServoPotWithSerialIn.ino) и [ServoPotWithSerialInOLED.ino](https://github.com/makeabilitylab/arduino/blob/master/Serial/ServoPotWithSerialInOLED/ServoPotWithSerialInOLED.ino). Можете да превключвате между потенциометър *и* сериен вход с помощта на бутона.

<video autoplay loop muted playsinline style="margin:0px">
<source src="assets/videos/ServoPotWithSerialInOLED-SerialMonitor_TrimmedAndOptimized.mp4" type="video/mp4" />
</video>
**Видео.** Демонстрация на [ServoPotWithSerialInOLED.ino](https://github.com/makeabilitylab/arduino/blob/master/Serial/ServoPotWithSerialInOLED/ServoPotWithSerialInOLED.ino). Можете да използвате бутона, за да превключвате между два режима на вход за управление на сервомотора: потенциометър и сериен вход. Във видеото обърнете внимание как натискаме бутона, за да превключим между управление чрез потенциометър и серийно управление. За второто изпращаме нови стойности чрез Serial Monitor. Също така създадохме версия на кода без OLED, наречена [ServoPotWithSerialIn.ino](https://github.com/makeabilitylab/arduino/blob/master/Serial/ServoPotWithSerialIn/ServoPotWithSerialIn.ino).
{: .fs-1 }

#### Сега добавете основното приложение за тестване p5.js

За да тестваме по-лесно скицата ни за Arduino с [p5](https://p5js.org/)), нека създадем просто уеб приложение за сериен контрол, за да управляваме сервомеханизма чрез уеб браузъра. В този случай ще прочетем позицията `x` на мишката, ще я нормализираме до [0, 1] и ще я предадем по сериен контрол. Ако това работи, тогава последната стъпка ще бъде да интегрираме приложението HandWaver, което би трябвало да е лесно.

Започнете, като направите копие на [`SerialTemplate`](https://github.com/makeabilitylab/p5js/tree/master/WebSerial/p5js/SerialTemplate), ако използвате VSCode, или [Serial Template](https://editor.p5js.org/jonfroehlich/sketches/vPfUvLze_C), ако използвате p5.js. Преименувайте проекта си на нещо като `XMouseSerialOut` – но името, разбира се, е по ваш избор.

Сега трябва да реализираме три неща:
- **Да усетим и нормализираме** позицията на мишката `x`. Това е лесно, винаги можем да вземем текущата позиция на мишката `x`, използвайки глобалната променлива `mouseX` в p5.js, а функцията `mouseMoved()` се извиква всеки път, когато мишката на потребителя се движи
- **Да предадем** нормализираната позиция `x` през уеб сериала
- **Да нарисуваме** информацията за мишката x върху платното. Това е по избор, но е полезно.

##### Усещане, нормализиране и предаване на позицията на мишката по ос x

Функцията p5.js [`mouseMoved()`](https://p5js.org/reference/#/p5/mouseMoved) се извиква всеки път, когато мишката се движи (стига бутонът на мишката да не е натиснат). Нека поставим кода, свързан с мишката, там.

Първо, създайте две глобални променливи за проследяване на мишката:

{% highlight JavaScript %}
let xMouseConstrained = 0;
let xMouseNormalized = 0;
{% endhighlight JavaScript %}

Сега имплементирайте функцията `mouseMoved()`:

{% highlight JavaScript %}
function mouseMoved(){
xMouseConstrained = constrain(mouseX, 0, width); // получаване на текущата позиция на мишката по x
xMouseNormalized = xMouseConstrained / width; // нормализирайте позицията по x

if(serial.isOpen()){
serial.writeLine(nf(xMouseNormalized, 0, 4)); // запишете нормализираната стойност, ако сериалният порт е свързан/отворен
}
}
{% endhighlight JavaScript %}

##### Добавете код за изчертаване на позицията на мишката по x

Накрая добавете код за рисуване, за да се покаже сива линия за текущата позиция на мишката по ос x и голям текст за нормализираната стойност:

{% highlight JavaScript %}
function draw() {
background(100);

// начертайте вертикална линия в позиция x
noFill();
stroke(150);
line(xMouseConstrained, 0, xMouseConstrained, height);

// начертаване на нормализирана стойност x
textSize(80);
fill(255);
noStroke();

textAlign(CENTER, CENTER);
text(nf(xMouseNormalized, 0, 4), width / 2, height / 2);
}
{% endhighlight JavaScript %}

Можете да разглеждате, редактирате и да си играете с приложението [XMouseSerialOut](https://makeabilitylab.github.io/p5js/WebSerial/p5js/XMouseSerialOut/) в [уеб редактора p5.js](https://editor.p5js.org/jonfroehlich/sketches/iwbGN0wkj) или в GitHub ( [жива страница](https://makeabilitylab.github.io/p5js/WebSerial/p5js/XMouseSerialOut/), [код](https://github.com/makeabilitylab/p5js/tree/master/WebSerial/p5js/XMouseSerialOut)).

<video autoplay loop muted playsinline style="margin:0px">
<source src="assets/videos/XMouseP5jsAppWithServoSerial_TrimmedAndOptimized.mp4" type="video/mp4" />
</video>
**Видео.** Демонстрация на малко тестово приложение p5.js, наречено [XMouseSerialOut](https://makeabilitylab.github.io/p5js/WebSerial/p5js/XMouseSerialOut/) ([code](https://github.com/makeabilitylab/p5js/tree/master/WebSerial/p5js/XMouseSerialOut)), което извежда нормализирана позиция `x` на мишката към сериен порт. Кодът, който се изпълнява на Arduino, е [ServoPotWithSerialInOLED.ino](https://github.com/makeabilitylab/arduino/blob/master/Serial/ServoPotWithSerialInOLED/ServoPotWithSerialInOLED.ino), но много други програми в нашето GitHub хранилище биха работили по същия начин, като например [ServoSerialIn](https://github.com/makeabilitylab/arduino/tree/master/Serial/ServoSerialIn).
{: .fs-1 }

#### Тест с приложението HandWaver p5.js

Ако простата уеб приложение p5.js x-position работи с вашия Arduino скиц, тогава приложението HandWaver също трябва да работи. Затова се върнете към кода на HandWaver – ето нашата версия на [уеб редактора p5.js](https://editor. p5js.org/jonfroehlich/sketches/vMbPOkdzu) и в GitHub ([жива страница](https://makeabilitylab.github.io/p5js/WebSerial/ml5js/HandWaver), [код](https://github.com/makeabilitylab/p5js/tree/master/WebSerial/ml5js/HandWaver)). На Arduino можете да изпълните някой от следните описани по-горе серийни серво кодове или да напишете свой собствен:

- [ServoSerialIn.ino](https://github.com/makeabilitylab/arduino/blob/master/Serial/ServoSerialIn/ServoSerialIn.ino) или OLED версията, наречена [ServoSerialInOLED.ino] (https://github.com/makeabilitylab/arduino/blob/master/Serial/ServoSerialInOLED/ServoSerialInOLED.ino), които приемат цяло число между 0 и 180 или число с плаваща запетая между 0 и 1 и задават съответната позиция на сервомеханизма.
- [ServoPotWithSerialIn.ino](https://github.com/makeabilitylab/arduino/blob/master/Serial/ServoPotWithSerialIn/ServoPotWithSerialIn.ino) или OLED версията, наречена [ServoPotWithSerialInOLED.ino] (https://github.com/makeabilitylab/arduino/blob/master/Serial/ServoPotWithSerialInOLED/ServoPotWithSerialInOLED.ino), които работят по подобен начин като предишните програми за Arduino, но позволяват на потребителя да превключва между управление с потенциометър и серийно управление на сервомеханизма чрез бутон.

<video autoplay loop muted playsinline style="margin:0px">
<source src="assets/videos/ServoPotWithSerialInOLED-HandWaver_TrimmedAndOptimized.mp4" type="video/mp4" />
</video>
**Видео.* * Демонстрация на [HandWaver](https://editor.p5js.org/jonfroehlich/sketches/vMbPOkdzu) с [ServoPotWithSerialInOLED.ino](https://github.com/makeabilitylab/arduino/blob/master/Serial/ServoPotWithSerialInOLED/ServoPotWithSerialInOLED.ino).
{: .fs-1 }

#### Създаване на интересна форма

Сега, още една забавна и творческа част: трябва да създадем интересна форма за серво мотора. Не забравяйте, че серво моторът ще се движи в отговор на x позицията на ръката ви. Така че можете да:

- Създадете Дарт Вейдър, размахващ светлинен меч
- Създадете модел на Статуята на свободата, която движи факлата си
- Създадете картонен ЛеБрон Джеймс, който движи ръката си, за да блокира Андре Игуодала във финала на НБА през 2016 г. ([видео](https://youtu.be/-zd62MxKXp8)). Сега известен просто като „[Блокажът.](https://en.wikipedia.org/wiki/The_Block_(basketball))“
- Да създадете картонена кралица на Англия, която ви маха с ръка
- ... вашите идеи тук! ...

В този случай работих с дете от детска градина и предучилищна възраст, за да създадем планинска сцена от хартия и фигурка, която наричаме „Хенри, човекът с тиксото“.

![](assets/images/HenryTheTapeManConstruction.png)
**Фигура.** Създаване на „Хенри, човекът с тиксото“ с цветна хартия, картон, лепило и много тиксо!
{: .fs-1 }

След това изчислихме подходящото място за поставяне на сервомотора за ръката на Хенри и изрязахме вдлъбнатина и отвор в картона:

![](assets/images/HenryTheTapeMan-InsertingTheServoMotor.png)
**Фигура.** Поставяне на сервомотора в картонената основа.
{: .fs-1 }

Прикрепихме временна „ръка“, за да тестваме конструкцията с потенциометъра и [HandWaver](https://makeabilitylab.github.io/p5js/WebSerial/ml5js/HandWaver).

<video autoplay loop muted playsinline style="margin:0px">
<source src="assets/videos/Henry_NoBody_TestingArmWithPot_Optimized.mp4" type="video/mp4" />
</video>
**Видео.** Тестване на сервомотора, вграден в картона, с потенциометъра – Arduino работи с [ServoPotWithSerialInOLED.ino](https://github.com/makeabilitylab/arduino/blob/master/Serial/ServoPotWithSerialInOLED/ServoPotWithSerialInOLED.ino).
{: .fs-1 }

Сега тестване с [HandWaver](https://makeabilitylab.github.io/p5js/WebSerial/ml5js/HandWaver):

<video autoplay loop muted playsinline style="margin:0px">
<source src="assets/videos/Henry_NoBody_TestingArmWithHandWaver_Optimized.mp4" type="video/mp4" />
</video>
**Видео.** Тестване на сервомотора, вграден в картона, с приложението [HandWaver](https://makeabilitylab.github.io/p5js/WebSerial/ml5js/HandWaver). Arduino работи с [ServoPotWithSerialInOLED.ino](https://github.com/makeabilitylab/arduino/blob/master/Serial/ServoPotWithSerialInOLED/ServoPotWithSerialInOLED.ino).
{: .fs-1 }

От тези тестове установихме, че добър диапазон на движение за ръката на Хенри е 40 - 85 градуса, така че актуализирахме скицата на Arduino:

{% highlight C++ %}
const int MIN_SERVO_ANGLE = 40;
const int MAX_SERVO_ANGLE = 85;
{% endhighlight C++ %}

<!-- TODO: след това направихме стойка -->

### Окончателна конструкция

И ето крайната конструкция, на която работи приложението p5+ml5 HandWaver—налично в [уеб редактора p5.js](https://editor.p5js.org/jonfroehlich/sketches/vMbPOkdzu) или в GitHub ([жива страница](https://makeabilitylab.github.io/p5js/WebSerial/ml5js/HandWaver), [код](https://github.com/makeabilitylab/p5js/tree/master/WebSerial/ml5js/HandWaver)) . На Arduino изпълняваме [ServoPotWithSerialInOLED.ino](https://github.com/makeabilitylab/arduino/blob/master/Serial/ServoPotWithSerialInOLED/ServoPotWithSerialInOLED.ino), но нещо толкова просто като [ServoSerialIn.ino](https://github.com/makeabilitylab/arduino/blob/master/Serial/ServoSerialIn/ServoSerialIn.ino) би работило (ако нямате OLED или не се налага/не искате да превключвате между потенциометъра и серийния вход, за да контролирате сервото).

<video autoplay loop muted playsinline style="margin:0px">
<source src="assets/videos/Henry_FullHandWaver_Optimized.mp4" type="video/mp4" />
</video>
**Видео.** Демонстрация на [HandWaver](https://editor.p5js.org/jonfroehlich/sketches/vMbPOkdzu) с [ServoPotWithSerialInOLED.ino](https://github.com/makeabilitylab/arduino/blob/master/Serial/ServoPotWithSerialInOLED/ServoPotWithSerialInOLED.ino) .
{: .fs-1 }

<!-- TODO: създаване на HandPoseDemo 3D? -->

<!-- TODO: с две ръце може да се контролират два различни серво мотора и да се направи дуел между картонен Дарт Вейдър и картонен Люк -->

## Референции

- [ml5 HandPose](https://learn.ml5js.org/#/reference/handpose), ml5

- [TensorFlow HandPose](https://github.com/tensorflow/tfjs-models/tree/master/handpose), Google TensorFlow

- [Обучение на детектор за ръце като OpenPose в TensorFlow](https://ortegatron.medium.com/training-a-hand-detector-like-the-openpose-one-in-tensorflow-45c5177d6679), Marcelo Ortega в Medium

- [Проследяване на ръце в реално време на устройството с MediaPipe](https://ai.googleblog.com/2019/08/on-device-real-time-hand-tracking-with.html), Валентин Базаревски и Фан Жанг, блог на Google AI

- [Проследяване на лицето и ръцете в браузъра с MediaPipe и TensorFlow.js](https://blog.tensorflow.org/2020/03/face-and-hand-tracking-in-browser-with-mediapipe-and-tensorflowjs.html), Ан Юан и Андрей Вакунов, блог на TensorFlow
