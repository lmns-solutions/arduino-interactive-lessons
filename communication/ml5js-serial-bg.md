---
lang: bg
permalink: /communication/ml5js-serial.html
page_id: communication-ml5js-serial
layout: default
title: L6&#58; ml5.js Серийна комуникация
nav_order: 6
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

В този урок ще разширим знанията си за [web serial](web-serial.md) и [p5.js](p5js-serial.md), като включим рамка за машинно обучение (ML), наречена [ml5.js](https://ml5js.org/) . Въпреки че интегрирането на машинно обучение в нашите проекти може да *изглежда* плашещо, точно както p5.js улеснява играта и експериментирането с интерактивна графика в JavaScript, така и [ml5.js](https://ml5js.org/) улеснява играта и експериментирането с машинно обучение. Това е наистина удивително!

Например, само с няколко реда JavaScript код и някои леки модификации на нашия [FlappyBird.ino](https://github.com/makeabilitylab/arduino/blob/master/OLED/FlappyBird/FlappyBird.ino) Arduino скиц (актуализиран до [FlappyBirdSerialIn.ino](https://github.com/makeabilitylab/arduino/blob/master/Serial/FlappyBirdSerialIn/FlappyBirdSerialIn.ino)), можем да играем FlappyBird с носа си, използвайки поток от уеб камера в реално време и [библиотеката PoseNet на ml5](https://learn.ml5js.org/#/reference/posenet).

<video autoplay loop muted playsinline style="margin:0px">
<source src="assets/videos/FlappyBirdNoseTracker_Short_1000w.mp4" type="video/mp4" />
</video>
**Видео.* * Играя Flappy Bird на Arduino Leonardo, като използвам носа си с p5.js, [ml5.js](https://ml5js.org/) и [web serial](web-serial.md). Приложението p5.js се нарича Nose Tracker ([p5.js онлайн редактор](https://editor.p5js.org/jonfroehlich/sketches/QgPPEU5o2), GitHub [жива страница](https://makeabilitylab.github.io/p5js/WebSerial/ml5js/NoseTracker), GitHub [код](https://github.com/makeabilitylab/p5js/tree/master/WebSerial/ml5js/NoseTracker)). Скицата на Arduino е [FlappyBirdSerialIn.ino](https://github.com/makeabilitylab/arduino/blob/master/Serial/FlappyBirdSerialIn/FlappyBirdSerialIn.ino).
{: .fs-1 }

В този урок ще покажем как да направите това и още много други неща. Но първо нека започнем с малко информация за рамките за машинно обучение, преди да се впуснем в [ml5.js](https://ml5js.org/) и ml5+Arduino по-конкретно.

## Фреймворки за машинно обучение

<video autoplay loop muted playsinline style="margin:0px">
<source src="assets/videos/RealTimeGestureRecognizer-EditedAndOptimized.mp4" type="video/mp4" />
</video>
**Видео.** В нашия магистърски курс по *Уbiquitous Computing* (Универсално компютърно изчисление) студентите създават разпознавател на жестове в реално време "от нулата", като използват акселерометър LIS3DH, Arduino и Python. Използваме платформата за машинно обучение [scikit-learn](https://scikit-learn.org/stable/). Пълно [YouTube видео](https://youtu.be/nnTyqCwYVbA).
{: .fs-1 }

В нашия магистърски курс по компютърни науки и инженерство на тема *Убиквити компютинг* преподаваме ~4-седмичен модул по филтриране, интерпретиране и класифициране на данни от сензори. Студентите изучават и изпитват пълния процес на класифициране: събиране на данни, писане на код за обработка и визуализация на тези данни, идентифициране и извличане на уникални характеристики за класифициране и писане на код за класифициране на тези характеристики. Например, студентите създават персонализирани [ускорителни сензори за проследяване на стъпките] (https://makeabilitylab.github.io/physcomp/signals/StepTracker/index.html) и [3D-разпознаватели на жестове](https://youtu.be/nnTyqCwYVbA) с помощта на Arduino и Python. Вижте видеото по-горе.

<!-- TODO: вмъкнете диаграма на този процес -->

За да стигнем дотам, разглеждаме теми в [цифровата обработка на сигнали](https://makeabilitylab.github.io/physcomp/signals/) и [класификацията на сигнали](https://makeabilitylab.github.io/physcomp/signals/classification.html), включително [кръстосана корелация](https://makeabilitylab.github.io/physcomp/signals/ ComparingSignals/index.html), [динамично изкривяване на времето](https://makeabilitylab.github.io/physcomp/signals/ComparingSignals/index.html) и [честотен анализ](https://makeabilitylab.github.io/physcomp/signals/FrequencyAnalysis/index.html), преди да се впуснем в [класификация на базата на хеуристика](https:// makeabilitylab.github.io/physcomp/signals/step-tracker.html), [съвпадение на шаблони](https://makeabilitylab.github.io/physcomp/signals/gesturerec/shapebased/index.html) и супервизирано обучение (*например* [поддържащи векторни машини] (https://makeabilitylab.github.io/physcomp/signals/gesturerec/featurebased/index.html)). Самите тези теми са обширни, плътни и заслужават свои собствени курсове – всъщност инженерните факултети обикновено предлагат множество курсове по DSP и машинно обучение. Макар че нашият магистърски курс предлага бърз преглед с приложна перспектива, все още съществуват значителни бариери за достъп, като например запознаване с математическите символи, техническата номенклатура и изучаване на съответните инструментариуми/библиотеки.

Например, в нашия 4-седмичен модул използваме [Python3](https://www.python.org/downloads/), [Jupyter Notebook](https://jupyter.org/) и редица изключително мощни, но не особено достъпни рамки за обработка на сигнали и машинно обучение, включително [NumPy](https://numpy.org/) , [SciPy](https://www.scipy.org/), [pandas](https://pandas.pydata.org/), [sci-kit learn](https://scikit-learn.org/stable/) и [matplotlib](https://matplotlib.org/). Уф! Макар че тези рамки предоставят изчерпателни библиотеки за обработка, класифициране и визуализиране на данни – и улесняват значително анализа и изграждането на ML системи – те имат сравнително високи изисквания за достъп. Както подчертава [Даниел Шифман](https://medium.com/ml5js/ml5-friendly-open-source-machine-learning-library-for-the-web-e802b5da3b2) в своето въведение към [ml5](https://ml5js.org/):

> Фреймворките за машинно обучение обикновено са предназначени за хора с напреднали познания по математически анализ, линейна алгебра, статистика, наука за данните и няколко години опит в програмирането на езици като Python или C++. Въпреки че това е важно за изследването и разработването на нови модели и архитектури за машинно обучение, започването от тази точка може да отблъсне новодошлите с друг опит. Вместо да мислят творчески за това как да използват машинно обучението като артистична платформа, начинаещите могат да се почувстват претоварени от фините различия между скалари, вектори, матрици, операции, входни слоеве, изходни слоеве и др.
{: .fs-4 }

Ами ако не се налага (или не искаме) да обучаваме свои класификатори или да се занимаваме задълбочено с анализ на сигнали? Ами ако просто искаме да си играем и да експериментираме с предварително обучени модели и/или най-съвременни техники за класификация, за да създадем нови интерактивни преживявания? За щастие, има много нови възможности!

### Прави машинно обучението достъпно

От самото си създаване изследователите работят, за да направят машинното обучение по-достъпно за творци като музиканти, художници, дизайнери и хобисти. Например, през 2009 г. Fiebrink и колегите му създадоха *[Wekinator](https://ualresearchonline.arts.ac.uk/id/eprint/16687/1/FiebrinkTruemanCook_NIME2009.pdf)*, за да позволят на "*музиканти, композитори и дизайнери на нови инструменти да обучават и модифицират интерактивно много стандартни алгоритми за машинно обучение в реално време.*” Шест години по-рано Джери Фейлс и Дан Олсен-младши представиха [*Crayons*](http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.14.8362&rep=rep1&type=pdf) – интерактивен модел за машинно обучение, който позволяваше на потребителите да обучават, класифицират и коригират класификации на базата на пиксели чрез скициране (виж фигурата по-долу).

![](assets/images/CrayonsScreenShot_ByJerrFailsAndDanOlsenJr.png)
**Фигура.** Интерактивният процес на машинно обучение на Crayons за автоматично сегментиране на пикселни "петна" в изображенията. Потребителите бързо скицират върху пикселите, които искат да включат или изключат от класификацията – в този случай сегментиране на човешка ръка – и веднага виждат отговора на ML модела (подчертани пиксели) и след това правят корекции. Вижте пълното [видео демонстрация тук](https://youtu.be/GtW-7YsiQdI).
{: .fs-1 }

С усъвършенстването на техниките за машинно обучение се усъвършенстват и библиотеките, които ги правят по-достъпни, включително [Teachable Machine на Google](https://teachablemachine.withgoogle.com/), [Runway ML](https://runwayml.com/) и [ml5.js](https://ml5js.org/) – всички те работят в уеб браузъра и с JavaScript!

Като доказателство за тези инструментариуми, машинно обучението все повече се превръща в още един *материал за прототипиране*. По същия начин, по който създаваме прототипи с код, електроника и занаяти, можем да създаваме прототипи и с ML, откривайки нови възможности за изчислителна креативност и нови приложения! Въпреки че е много мощен, ML може да бъде и опасен и да се използва за злонамерени цели – [правителствата използват лицево разпознаване](https://epic.org/state-policy/facialrecognition/#:~:text=Facial%20recognition%20can%20be%20used,%2C%20misuse% 2C%20и%20мисионно%20отклонение), за да наблюдават без съгласие, модели, които насърчават [системни расови или полови предразсъдъци](http://proceedings.mlr.press/v81/buolamwini18a/buolamwini18a.pdf), и/или технолози, които преувеличават способностите на ML, излагайки на опасност крайните потребители и евентуално [водейки до смърт](https://www.washingtonpost.com/technology/2021/05/14/tesla-california-autopilot-crash/). Затова нека подходим към тези ML рамки с предпазливост – те са несъвършени и вероятностни. Както гласи [принципът на Питър Паркър] (https://en.wikipedia.org/wiki/With_great_power_comes_great_responsibility):

> Голямата сила носи голяма отговорност

Въпреки че този урок няма да се задълбочава в ML, нашата надежда е, че той ще ви послужи като достъпен път за задълбочаване на разбирането ви за това как работи ML, значението на данните и обучението на модели, както и социално-техническите последици от създаването на технологии, зависещи от ML. Например, ще използваме библиотеката ml5 PoseNet за разпознаване на човешки тела – колко добре мислите, че този модел работи при различни типове тела, възрасти и цветове на кожата? Отговорът ще се основава на *тренировъчния набор* за невронния мрежов модел. Ако обучителният набор се състои предимно от изображения на високи, слаби, бели мъже на средна възраст, облечени в делови ежедневни дрехи, при идеални условия на осветление и с едноцветен фон, е малко вероятно PoseNet да работи добре при други демографски групи, типове тела, цветове на кожата и среди. Важно е постоянно да мислим за това как се обучават нашите ML системи, откъде идват данните и колко добре ще работят ML системите в различни контексти.

### Приятелско машинно обучение в интернет: ml5.js

<video autoplay loop muted playsinline style="margin:0px">
<source src="assets/videos/PoseNet_TensorFlow-Optimized.mp4" type="video/mp4" />
</video>
**Видео.** [PoseNet](https://learn.ml5js.org/# /reference/posenet) е модел за машинно обучение за оценка на позата в реално време, базиран на [TensorFlow](https://medium.com/tensorflow/real-time-human-pose-estimation-in-the-browser-with-tensorflow-js-7dd0bc881cd5).
{: .fs-1 }

В този урок ще използваме [ml5.js](https://www.tensorflow.org/js/), който предоставя лесна за използване библиотека около [TensorFlow.js](https://www.tensorflow.org/js/) на Google и е проектиран да работи добре с [p5.js](https://p5js.org/) (оттук и "5" в името!). 

![](assets/images/ml5js_DiagramRelationToTensorFlow.png)
{: .mx-auto .align-center }

**Фигура.** ml5.js е изграден върху [TensorFlow.js](https://www.tensorflow.org/js/) на Google. Той използва модели, слоеве и API за данни на TensorFlow, но ги абстрахира в програмистки интерфейс, подходящ за начинаещи. Диаграма от курса "Машинно обучение за уеб" на Yining Shi в ITP, NYU ([link](https://docs.google.com/ presentation/d/1s0iT382Pl1DMGKb5xhk7_V3DlW1QQHfHs4snNoS_sIU/edit#slide=id.g953c8caacd_0_2))
{: .fs-1 }

Както се посочва в [страницата "За ml5"](https://ml5js.org/about/):

> ml5 не се занимава само с разработването на софтуер за машинно обучение, а и с това да направи машинно обучение достъпно за широка аудитория от артисти, творчески програмисти и студенти. Библиотеката предоставя достъп до алгоритми и модели за машинно обучение в браузъра, като се основава на TensorFlow.js без други външни зависимости
{: .fs-4 }

Можете да прочетете повече за историята на ml5 [тук](https://medium.com/ml5js/ml5-friendly-open-source-machine-learning-library-for-the-web-e802b5da3b2). ml5.js е с отворен код в [GitHub](https://github.com/ml5js/ml5-library).

### Първи стъпки с ml5.js

За да започнете с [ml5.js](https://ml5js.org/), препоръчваме да прочетете официалната страница на ml5.js ["Първи стъпки"](https://learn.ml5js.org/# /) и да гледате някои от сериите на Даниел Шифман Coding Train YouTube за ["Начално ръководство за машинно обучение с ml5.js"](https://www.youtube.com/playlist?list=PLRqwX-V7Uu6YPSwT06y_AEYTqIwbeam3y), което включва чудесни видеоклипове за [класифициране на изображения](https:// www.youtube.com/watch?v=yNkAuWz5lnY&list=PLRqwX-V7Uu6YPSwT06y_AEYTqIwbeam3y&index=3) , [откриване на обекти](https://www.youtube.com/watch?v=QEzRxnuaZCk&list=PLRqwX-V7Uu6YPSwT06y_AEYTqIwbeam3y&index=5&t=211s), [класификация на звуци] (https://www.youtube.com/watch?v=cO4UP2dX944&list=PLRqwX-V7Uu6YPSwT06y_AEYTqIwbeam3y&index=19&t=766s) , [класификация на драсканици](https://www.youtube.com/watch?v=ABN_DWnM5GQ&list=PLRqwX-V7Uu6YPSwT06y_AEYTqIwbeam3y&index=30) и още много други! Шифман също така ви показва как да обучавате свои собствени модели, включително за играта Snake, базирана на JavaScript ([линк](https://www.youtube.com/watch?v=kwcillcWOg0&list=PLRqwX-V7Uu6YPSwT06y_AEYTqIwbeam3y&index=13&t=66s)), или да [класифицирате свои собствени звуци] (https://www.youtube.com/watch?v=TOrVsLklltM&list=PLRqwX-V7Uu6YPSwT06y_AEYTqIwbeam3y&index=20). Първото видео от [серията Coding Train ml5js](https://www.youtube.com/playlist? list=PLRqwX-V7Uu6YPSwT06y_AEYTqIwbeam3y) е по-долу.

<iframe width="736" height="414" src="https://www.youtube.com/embed/jmznx0Q1fP0" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
**Видео.** Първото видео от YouTube поредицата на Шифман "Coding Train" на тема "Ръководство за начинаещи в машинно обучение с ml5.js" ](https://www.youtube.com/playlist?list=PLRqwX-V7Uu6YPSwT06y_AEYTqIwbeam3y). Препоръчваме всички [видеоклипове от Coding Train](https://www.youtube.com/channel/UCvjgXvBlbQiydffZU7m1_aw)!
{: .fs-1 }

### Защо не вградено машинно обучение?

![](assets/images/SoundWatch_FourArchitecturesDiagram.png)
**Фигура.* * Има много възможности за архитектурата на вградени/IoT ML системи в зависимост от изискванията за мощност, изчислителна мощност и латентност. В нашата [статия ASSETS'20](https://makeabilitylab.cs.washington.edu/media/publications/Jain_SoundwatchExploringSmartwatchBasedDeepLearningApproachesToSupportSoundAwarenessForDeafAndHardOfHearingUsers_ASSETS2020.pdf) за [SoundWatch] (https://makeabilitylab.cs.washington.edu/project/soundwatch/), например, разглеждаме четири различни ML архитектури: *watch-only*, *watch+phone*, *watch+phone+cloud* и *watch+cloud*.
{: .fs-1 }

Тъй като това е курс по физическо програмиране, човек може с право да попита: защо да не се преподава *вградено* машинно обучение, при което ML моделът работи локално на Arduino или IoT устройство, а не на компютър или в облака. Това е чудесен въпрос с многостранен отговор:

- Първо, когато започваме да изучаваме ML – дори в приложното му значение – смятаме, че настолният компютър предоставя по-достъпна среда за учене. Инструментите са по-усъвършенствани, по-лесно е да се визуализират и разберат данните и ML моделът, и е по-лесно да се отстраняват грешки и да се повтарят операциите. 
- Въпреки че новите ML рамки като [TensorFlow Lite](https://www.tensorflow.org/lite) са проектирани специално за мобилни устройства и устройства с ниски ресурси, общността все още е малка и съответно има малко примери. И отново, пускането на модел директно на Arduino увеличава сложността на обучението, тестването и итерацията. Трябва да започнем просто и да се разрастваме навън!
- Накрая, дори "умните" IoT или носими устройства, които използват машинно обучение, често разчитат на API-та, базирани в облака, за класификация. Самото устройство може да преобработва данните или да извлича характеристики за облака, но пълният класификатор работи извън устройството. Например, нашата система [SoundWatch](https:// makeabilitylab.cs.washington.edu/project/soundwatch/) класифицира и визуализира звуци в реално време на смарт часовник за хора, които са глухи или с увреден слух. В нашата [статия ASSETS'20] (https://makeabilitylab.cs.washington.edu/media/publications/Jain_SoundwatchExploringSmartwatchBasedDeepLearningApproachesToSupportSoundAwarenessForDeafAndHardOfHearingUsers_ASSETS2020.pdf) разглеждаме четири различни архитектури за класификация: *само часовник*, *часовник+телефон*, *часовник+телефон+облак* и *часовник+облак*. Има много възможности за архитектурата на вградени/IoT ML системи в зависимост от изискванията за мощност, изчислителна мощност и латентност.

В този урок **няма** да класифицираме сензорни потоци от Arduino, а по-скоро ще класифицираме данни от уеб камера с ml5.js и ще предаваме получената информация към Arduino чрез [уеб сериен порт](web-serial.md).

<!-- TODO: защо да не пуснем класификатори на микроконтролера?
Вижте: https://experiments.withgoogle.com/tfmicrochallenge -->

<!-- Pacman уеб камера контролер: https://storage.googleapis.com/tfjs-examples/webcam-transfer-learning/dist/index.html -->

<!-- TODO: в бъдеще да се доразвие секцията за библиотеката ml5.js и да се предоставят скрийншотове и др.
### Библиотека ml5.js

Библиотеката [ml5.js](https://learn.ml5js.org/#/reference/index) предоставя класификация на изображения, звук и текст. Моля, вижте страницата "Референции" за подробности. По-долу ще разгледаме няколко често срещани модела.

#### Изображение

## Други библиотеки -->

<!-- - face-api.js https://github.com/justadudewhohacks/face-api.js -->

## Разпознаване на човешки пози с PoseNet

В този първи урок ще използваме p5.js, за да заснемем поток от уеб камера в реално време, и ml5.js, за да разпознаем обекти в този поток – по-специално човешкото тяло и ключови части от него.

Разпознаването на части от човешкото тяло в изображения/видео е вид проблем на компютърното зрение, наречен "оценка на позата". Важно е да се отбележи, че оценката на позата **не** разпознава *кой* е на изображението или видеото, а просто идентифицира дали има хора и, ако има, предоставя данни за частите на тялото им (*например* позицията `x,y` на глезена или носа). Това отдавна е предизвикателна задача за компютърното зрение. Предишните разработки често разчитаха на специализирани камери, като [Microsoft Kinect](https://www.microsoft.com/en-us/research/project/human-pose-estimation-for-kinect/), за да заснемат и идентифицират човешките пози.

През май 2018 г. Google Creative Lab [обяви](https://medium.com/tensorflow/real-time-human-pose-estimation-in-the-browser-with-tensorflow-js-7dd0bc881cd5) PoseNet, базирана на TensorFlow.js система за оценка на човешките пози в реално време за уеб браузъра. Това беше невероятно постижение: сега всеки, който има уеб браузър и уеб камера, може да използва и/или създава приложения, базирани на пози. TensorFlow.js работи локално в браузъра, използвайки предварително обучени данни. По този начин всички данни за разпознаване и пози са локални – никои от тях не се изпращат в облака (освен ако приложение, създадено на базата на PoseNet, не предава тази информация).

Откъде идват данните за обучение? Според [тази статия](https://medium.com/ml5js/ml5-friendly-open-source-machine-learning-library-for-the-web-e802b5da3b2), моделите за откриване на поза са обучени с помощта на [Cambridge Landmarks](http://mi.eng. cam.ac.uk/projects/relocalisation/) и [7-Scenes Datasets](https://www.microsoft.com/en-us/research/project/rgb-d-dataset-7-scenes/). Не е ясно колко добре се генерализират; обаче, PoseNet работи добре за нас в продължение на ~2 години преподаване (с може би ~100 студенти).

#### PoseNet модели

PoseNet всъщност има два различни обучени модела: единичен оценител на позата, когато се нуждаете (или очаквате) само една човешка фигура в кадър, и детектор на множествена поза за откриване на няколко души. Макар единичният модел да е по-бърз, ако има вероятност в кадъра да има няколко души, използвайте модела за множествена поза. В противен случай моделът за единична поза може да смеси части от телата на различни хора (*например* лявата лакътна става на човек 1 е част от човек 2).

<!-- Пример:
https://storage.googleapis.com/tfjs-models/demos/posenet/camera.html -->

#### Структурата на данните на PoseNet
![](assets/images/PoseNet_PosesAndKeypoints_FromMediumArticle.png)
**Фигура.** Общ преглед на данните на PoseNet. Изображения от "[Оценка на позата на човека в реално време в браузъра с TensorFlow.js](https://medium.com/tensorflow/real-time-human-pose-estimation-in-the-browser-with-tensorflow-js-7dd0bc881cd5)".
{: .fs-1 }

Както [TensorFlow.js PoseNet](https://github.com/tensorflow/tfjs-models/tree/master/posenet), така и [ml5.js wrapper ](https://learn.ml5js.org/#/reference/posenet) използват една и съща структура на данните за позата. PoseNet връща масив от обекти – по един обект за всеки човек, открит в кадър. За всеки човек получаваме: 
1. обект `pose`, който включва обща оценка на достоверността и масив от 17 ключови точки, и
 
2. обект "скелет", който включва същите данни за ключови точки, но с информация за свързаността на ставите (*например* "дясната лакътна става" и "дясното рамо" са свързани). 

Всяка ключова точка има "позиция" (позицията на ключовата точка в пиксели по ос x и y), "оценка" на достоверност (в диапазона от 0 до 1) и име на "част". Както показва фигурата по-горе, има общо [17 ключови точки](https://github.com/tensorflow/tfjs-models/tree/master/posenet#keypoints): "нос", "ляво око", "дясно око", "ляво ухо", "дясно ухо", "ляво рамо", "дясно рамо", "ляв лакът", "десен лакът", "лява китка", "дясна китка", "ляво бедро", "дясно бедро", "ляво коляно", "дясно коляно", "лява глезена", "дясна глезена". Вижте изображението по-горе.

Структурата на масива изглежда така:

{% highlight JavaScript %}
[
{
pose: {
score: { confidence },
keypoints: [{ position: { x, y }, score, part }, { position: { x, y }, score, part }, ...],
leftAngle: { x, y, confidence },
leftEar: { x, y, confidence },
ляв лакът: { x, y, увереност },
...
},
скелет: [
[{ част, позиция: { x, y }, резултат }, { част, позиция: { x, y }, резултат }],
[{ част, позиция: { x, y }, резултат }, { част, позиция: { x, y }, резултат }],
...
],
},
{
резултат: { увереност },
поза: {
ключови точки: [{ позиция: { x, y }, резултат, част }, { позиция: { x, y }, резултат, част }, ...],
ляв ъгъл: { x, y, увереност },
ляво ухо: { x, y, увереност },
ляв лакът: { x, y, увереност },
...
},
скелет: [
{ част, позиция: { x, y }, резултат }, { част, позиция: { x, y }, резултат }, ...
],
},
...
];
{% endhighlight JavaScript %}

За да стане по-ясно, ето екранна снимка на нашето приложение [Skeleton](https://makeabilitylab.github.io/p5js/ml5js/PoseNet/Skeleton/) с инструментите за разработчици на Chrome, показваща поза и скелет.

![](assets/images/PoseNet_DataStructure_ChromeDevTools.png)
* *Фигура.** Проверка на структурата на данните на PoseNet за една разпозната поза. Кликнете с десния бутон и изберете "Отвори изображение в нов раздел", за да го увеличите. Ако искате да направите същото, отворете приложението ни [Skeleton](https://makeabilitylab.github.io/p5js/ml5js/PoseNet/Skeleton/) в уеб браузъра си (*например* Chrome или FireFox). След това отворете инструментите за разработка (ctrl-shift-i в Windows, cmd-option-i в Mac). Кликнете върху раздела "Източници" и след това поставете точка на прекъсване при извикването на функцията "drawPose()" във функцията "draw()". Накрая добавете променливата "currentPoses" към "Watch" в дебъгера.
{: .fs-1 }

### Пример за p5.js + ml5.js PoseNet демо

За да демонстрираме [ml5.js PoseNet API](https://learn.ml5js.org/# /reference/posenet), създадохме проста приложение, наречено [Skeleton](https://makeabilitylab.github.io/p5js/ml5js/PoseNet/Skeleton/), което изобразява:
- ограничаваща кутия около всеки открит човек, показваща "резултат" за увереност
- всички 17 ключови точки с позиция `x,y` и специфични за ключовите точки `резултати` за увереност
- данните за `скелета` за всяка поза.

Ето видео демонстрация:

<video autoplay loop muted playsinline style="margin:0px">
<source src="assets/videos/PoseNet_SkeletonDemo_Optimized.mp4" type="video/mp4" />
</video>
**Видео.** Това видео демонстрира ml5 PoseNet API чрез приложението [Skeleton](https://makeabilitylab.github.io/p5js/ ml5js/PoseNet/Skeleton/). Ние изчертаваме всяка от 17-те разпознати ключови точки заедно с позицията x, y и оценките за достоверност. Кодът е достъпен в GitHub [тук](https://github.com/makeabilitylab/p5js/tree/master/ml5js/PoseNet/Skeleton) .
{: .fs-1 }

Препоръчваме да отворите [версията в онлайн редактора на p5.js](https://editor.p5js.org/jonfroehlich/sketches/mX-kqe-MS) и да експериментирате с кода. Можете ли да промените цвета на ключовите точки, да удебелите скелета или да филтрирате (да не рисувате) ключови точки с ниски оценки за достоверност? Можете също да видите приложението на GitHub ([жива страница](https://github.com/makeabilitylab/p5js/tree/master/ml5js/PoseNet/Skeleton), [код](https://github.com/makeabilitylab/p5js/tree/master/ml5js/PoseNet/Skeleton)).

Добре, сега сме готови да започнем да създаваме заедно приложение ml5.js + Arduino!

## Създаване на първото ни приложение ml5.js + Arduino: NoseTracker

За първото ни упражнение ще създадем проста, но забавна играчка: проследяване на носа на човек с помощта на [ml5.js' PoseNet](https://learn.ml5js.org/#/reference/posenet), за да се движи обект по OLED дисплея на Arduino. Тъй като това е част от нашата [web serial](web-serial.md) серия, ще предаваме информация от нашето JavaScript приложение към Arduino чрез серийна комуникация.

Ето кратък предварителен преглед. Обърнете специално внимание на OLED дисплея, който показва икона на лице въз основа на позицията на носа ми в кадъра на уеб камерата!

<video autoplay loop muted playsinline style="margin:0px">
<source src="assets/videos/NoseTracker_TrimmedAndOptimized.mp4" type="video/mp4" />
</video>
**Видео.** Това кратко демо показва нашето приложение p5.js + Arduino, което използва PoseNet на ml5, за да проследява носа и очите на потребителя в реално време с поток от уеб камера. Тези данни се използват, за да се нарисува карикатурно наслагване върху позициите на носа и очите, за да предаде нормализирана x,y позиция на носа към Arduino чрез уеб сериен порт и да нарисува емоджи-подобно лице на x,y позицията на OLED дисплея. Приложението p5.js е свободно базирано на това видео на Coding Train "[Час на кодиране с p5.js и PoseNet](https://youtu.be/EA3-k9mnLHs)”. Пълният код е достъпен в [p5.js онлайн редактор](https://editor.p5js.org/jonfroehlich/sketches/QgPPEU5o2) или в GitHub ([жива страница](https://makeabilitylab.github.io/p5js/WebSerial/ml5js/NoseTracker/), [код](https://github.com/makeabilitylab/p5js/ tree/master/WebSerial/ml5js/NoseTracker)). Кодът за Arduino е в GitHub като [NoseTrackerSerialIn.ino](https://github.com/makeabilitylab/arduino/blob/master/Serial/NoseTrackerSerialIn/NoseTrackerSerialIn.ino).
{: .fs-1 }

### Изграждане на уеб приложението

Първо, нека започнем с изграждането на p5.js + ml5.js NoseTracker. Както и в предишните уроци, започнете с копиране на [`SerialTemplate`](https:// github.com/makeabilitylab/p5js/tree/master/WebSerial/p5js/SerialTemplate). Ако използвате VSCode, копирайте [`SerialTemplate`](https://github.com/makeabilitylab/p5js/tree/master/WebSerial/p5js/SerialTemplate) и преименувайте папката на `NoseTracker`. Ако използвате онлайн редактора p5.js, просто отворете [Serial Template](https://editor.p5js.org/jonfroehlich/sketches/vPfUvLze_C) и преименувайте проекта си на `NoseTracker`.

#### Добавете и инициализирайте PoseNet на ml5

Сега нека добавим PoseNet на ml5.js. Обектът `ml5.poseNet` има [два основни конструктора](https://learn.ml5js.org/#/reference/posenet?id=initialize) – единият използва живо `видео` излъчване, например от уеб камера, а другият не. И двата конструктора използват множество *опционални* аргументи (показани с префикса "?" в списъка с параметри на функцията):

{% highlight JavaScript %}
// Инициализирайте с видео, опции и callback
const poseNet = ml5.poseNet(?video, ?options, ?callback);

// Инициализирайте БЕЗ видео. Тук са само опциите и callback
const poseNet = ml5.poseNet(?callback, ?options);
{% endhighlight JavaScript %}

Параметрите са:
* `video`: Опционален [HTMLVideoElement](https://developer.mozilla.org/en-US/docs/Web/API/HTMLVideoElement). Това е лесно да се получи в p5.js, просто извикваме [`createCapture(VIDEO)`](https://p5js.org/reference/#/p5/createCapture). Не се притеснявайте, по-долу ще покажем пример.

* `options`: Незадължителен обект от свойствата на конфигурацията на PoseNet. Вижте по-долу.

* `callback`: Опционална препратка към callback функция, която се извиква, когато моделът се зареди.

Обектът *options* е форматиран както следва. Ако не се предаде обект options, се използват дадените по-долу стойности по подразбиране. За повече информация за значението на тези свойства, моля, вижте [ml5.js PoseNet properties reference](https://learn.ml5js.org/ #/reference/posenet?id=properties)e или тази [статия за TensorFlow PoseNet](https://medium.com/tensorflow/real-time-human-pose-estimation-in-the-browser-with-tensorflow-js-7dd0bc881cd5) (превъртете до раздела "Част 2а: Оценка на позата на едно лице").

{% highlight JavaScript %}
{
architecture: "MobileNetV1",
imageScaleFactor: 0.3,
outputStride: 16,
flipHorizontal: false,
minConfidence: 0.5,
maxPoseDetections: 5,
scoreThreshold: 0.5,
nmsRadius: 20,
detectionType: "multiple",
inputResolution: 513,
multiplier: 0.75,
quantBytes: 2,
};
{% endhighlight JavaScript %}

За да инициализираме ml5 PoseNet с видео потока от уеб камерата, пишем:

{% highlight JavaScript %}
let video;
let poseNet;
function setup(){
createCanvas(640, 480);
video = createCapture (VIDEO);
poseNet = ml5.poseNet(video);
}
{% endhighlight JavaScript %}

Ако искаме да знаем кога е инициализиран моделът PoseNet, можем да предадем опционална препратка към callback функция:
{% highlight JavaScript %}
function setup(){
...
poseNet = ml5.poseNet(video, onPoseNetModelReady);
}

function onPoseNetModelReady() {
print("Моделът PoseNet е готов...");
}
{% endhighlight JavaScript %}

Можем също да предоставим опции за конфигуриране – например, да зададем оценка за единична поза или минимална степен на увереност за поза от 0,3:

{% highlight JavaScript %}
function setup(){
...
const poseNetOptions = { detectionType: "single", minConfidence: 0.3 };
poseNet = ml5.poseNet(video, poseNetOptions, onPoseNetModelReady);
}
{% endhighlight JavaScript %}

#### Абонирайте се за новото събитие за поза

Точно както нашата [web serial](web-serial.md) библиотека ([serial.js](https://github.com/makeabilitylab/p5js/blob/master/_libraries/serial.js)) използва архитектура, базирана на събития, така и ml5.js. Припомнете си, че с serial.js можем да се абонираме за четири различни събития, съответстващи на отворена връзка, затворена връзка, получени данни и възникнала грешка. Ако имате нужда от освежаване на паметта, вижте [тази секция](web-serial.md#event-based-functions) от нашия [урок за уеб сериала](web-serial.md).

{% highlight JavaScript %}
// Настройка на уеб сериала с помощта на serial.js
const serial = new Serial();

// Абонирайте се за събитията
serial.on(SerialEvents.CONNECTION_OPENED, onSerialConnectionOpened);
serial.on(SerialEvents.CONNECTION_CLOSED, onSerialConnectionClosed);
serial.on(SerialEvents.DATA_RECEIVED, onSerialDataReceived);
serial.on(SerialEvents.ERROR_OCCURRED, onSerialErrorOccurred);
{% endhighlight JavaScript %}

Библиотеката ml5 PoseNet е подобна, но има само едно събитие за абонамент, наречено "pose". Абонираме се, като предоставяме име на събитието и препратка към функция за обратно извикване:

{% highlight JavaScript %}
poseNet.on("pose", onPoseDetected);
{% endhighlight JavaScript %}

По този начин пълният код за инициализиране на ml5 PoseNet с абонамент за събитието "pose" е:

{% highlight JavaScript %}
let video;
let poseNet;
function setup() {
createCanvas(640, 480);
video = createCapture(VIDEO);
video.hide(); // скриване на необработеното видео (можете да коментирате в/извън, за да видите ефекта)
poseNet = ml5.poseNet(video, onPoseNetModelReady); //извикайте onPoseNetModelReady, когато е готово
poseNet.on("pose", onPoseDetected); // извикайте onPoseDetected, когато се открие поза
}

function onPoseNetModelReady() {
print("Моделът PoseNet е готов...");
}

function onPoseDetected(poses) {
print("Засечени са нови пози!");
if (poses){
print("Намерихме " + poses.length + " човека");
}
}
{% endhighlight JavaScript %}

Можете да видите, да си играете и да редактирате [този код](https://editor.p5js.org/jonfroehlich/sketches/TMafCYmKE) в онлайн редактора p5.js.

#### Нарисувайте ключова точка на носа

Сега да се забавляваме! Да нарисуваме червен "нос" на ключовата точка `nose`.

Първо, променете метода `onPoseDetected(poses)`, за да съхраните масив от текущи пози:

{% highlight JavaScript %}
function onPoseDetected(poses) {
print("On new poses detected!");
if(poses){
print("We found " + poses.length + " humans");
}
currentPoses = poses;
}
{% endhighlight JavaScript %}

Сега, във функцията `draw()`, нека нарисуваме носа в ключовата точка `nose`.

{% highlight JavaScript %}
function draw() {
background(100);

image(video, 0, 0); // нарисувайте видеото на екрана в 0,0
if(currentPoses){
for(let human of currentPoses){ // преминавайте през всеки човек
fill("red"); // червен нос
noStroke();

// Нарисувайте кръг за ключовата точка на носа
circle(human.pose.nose.x, human.pose.nose.y, 40);
}
}
}
{% endhighlight JavaScript %}

Ето видео демонстрация с връзки към [примерния код](https://editor.p5js.org/jonfroehlich/sketches/khxRw8FI3) на това, до което сме стигнали досега:

<video autoplay loop muted playsinline style="margin:0px">
<source src="assets/videos/NoseTracker2-Nose_2x_Optimized.mp4" type="video/mp4" />
</video>
**Видео.** Видео демонстрация на използването на ml5 за проследяване и рисуване върху ключови точки на части от тялото. Базирано на Coding Train "[Hour of Code with p5.js and PoseNet](https://youtu.be/EA3-k9mnLHs)” от Даниел Шифман. Можете да изпълните и редактирате този код директно в браузъра си, използвайки онлайн редактора p5.js ([линк](https://editor.p5js.org/jonfroehlich/sketches/khxRw8FI3)).
{: .fs-1 }

Можете да разгледате, да си поиграете и да редактирате [този код](https://editor.p5js.org/jonfroehlich/sketches/khxRw8FI3) в онлайн редактора p5.js.

#### Превърнете се в кукла

За да направим това малко по-забавно, можем да се [превърнем в кукли](https://en.wikipedia.org/wiki/The_Muppets), като добавим очи. Това е като създаването на основен филтър за лице в Snapchat или Instagram! Ще модулираме кода си, като създадем функциите `drawNose` и `drawEye`.

{% highlight JavaScript %}
function draw() {
image(video, 0, 0); // изчертайте видеото на екрана на 0,0
if(currentPoses){
for(let human of currentPoses){ // преминавайте през всеки човек
drawNose(human.pose.nose.x, human.pose.nose.y);
drawEye(human.pose.leftEye.x, human.pose.leftEye.y);
drawEye(human.pose.rightEye.x, human.pose.rightEye.y);
}
}
}

function drawNose(x, y) {
fill("red"); // червен нос
noStroke();
circle(x, y, 35);
}

function drawEye(x, y) {
noStroke();

fill(255); // бяло на окото (склерата)
const eyeWidth = 40;
const pupilWidth = 15;
ellipse(x, y, eyeWidth);

fill(0); // черни зеници
ellipse(x, y, pupilWidth);
}
{% endhighlight JavaScript %}

И още едно видео демо, за да покажем какво сме създали досега! Забележете как PoseNet разпознава *снимки* на хора, както и реални, физически хора в потока от уеб камерата (но не и снимки на тюлени!).

<video autoplay loop muted playsinline style="margin:0px">
<source src="assets/videos/NoseTracker3-EyesAndNoseWithBook-Optimized.mp4" type="video/mp4" />
</video>
**Видео.** Видео демонстрация на превръщането на себе си в Елмо с помощта на ml5 PoseNet. За да демонстрирам разпознавателя на много пози, използвах корица на книга с човешко лице (по това време нямаше никой около мен, който да ми помогне с демонстрацията! . Видеото показва и как корицата на книга с тюлен не се разпознава. Можете да изпълните и редактирате този код директно в браузъра си, използвайки онлайн редактора p5.js ([link](https://editor.p5js.org/jonfroehlich/sketches/ZsvOFxZ0d)).
{: .fs-1 }

Можете да видите, да си играете и да редактирате [този код](https://editor.p5js.org/jonfroehlich/sketches/ZsvOFxZ0d) в онлайн редактора p5.js.

#### Добавете код за уеб сериен номер

Накрая, нека добавим код за предаване на местоположението на носа през уеб сериен номер. Както направихме в предишните уроци, вместо да предаваме суровите x,y пикселни местоположения, ще предаваме нормализирана версия между [0, 1] включително за x и y. Модифицирайте функцията `onPoseDetected(poses)`, както следва:

{% highlight JavaScript %}
function onPoseDetected(poses) {
print("On new poses detected!");

if(poses){
let strHuman = " human";
if(poses.length > 1){
strHuman += "s";
}
text("We found " + poses.length + strHuman);

// Ако сериалът е отворен, предайте нормализираното местоположение на носа
if(serial.isOpen()){
const human = poses[0];

// Вземете позицията на носа и я нормализирайте като x,y част от екрана, за да я предадете през сериала
let noseXNormalized = human.pose.nose.x / width;
let noseYNormalized = human.pose.nose.y / height;

let outputData = nf(noseXNormalized, 1, 4) + ", " + nf(noseYNormalized, 1, 4)
serial.writeLine(outputData);
}
}
currentPoses = poses;
}
{% endhighlight JavaScript %}

#### Свързване с уеб сериен устройство

Нашият шаблон код, [`SerialTemplate`](https://github.com/makeabilitylab/p5js/tree/master/WebSerial/p5js/SerialTemplate), предоставя два различни механизма за свързване — и двата са вече кодирани, така че не е необходимо да правите нищо тук. Но за да припомним, двата различни подхода за свързване са:

Първо, ако никога преди не сте се свързвали с конкретно уеб сериен устройство, можете да кликнете върху платното, където ще ви посрещне диалогов прозорец за свързване:

{% highlight JavaScript %}
function mouseClicked() {
if (!serial.isOpen()) {
serial.connectAndOpen(null, serialOptions);
}
}
{% endhighlight JavaScript %}

Второ, ако вече сте одобрили уеб сериалното устройство, то ще се свърже автоматично, веднага щом стартирате приложението. Това се прави в `setup()`:

{% highlight JavaScript %}
serial.autoConnectAndOpenPreviouslyApprovedPort(serialOptions);
{% endhighlight JavaScript %}

Разбира се, можете да създадете свой собствен интерфейс за свързване с уеб серийни устройства, но това е, което предлага шаблонът!

#### Приключихме с JavaScript приложението

Това е всичко за p5.js приложението. Пълният код е достъпен в [p5.js онлайн редактор](https://editor.p5js.org/jonfroehlich/sketches/QgPPEU5o2) или в GitHub ([жива страница](https://makeabilitylab.github.io/p5js/WebSerial/ml5js/NoseTracker/), [код](https://github.com/makeabilitylab/p5js/tree/master/WebSerial/ml5js/NoseTracker)).

### Изграждане на Arduino

Има много творчески възможности за това как Arduino може да използва данните от PoseNet. Засега ще нарисуваме икона на лице на OLED дисплея на входящата x,y позиция.

#### OLED веригата

Веригата е подобна на много от тези, които сме изградили за нашите [уроци по уеб сериен интерфейс](p5js-serial-io.md#a-simple-oled-circuit). Просто свържете OLED с I<sup>2</sup>C връзки.

| Arduino Leonardo свързване | Huzzah32 (ESP32) свързване |
|-------------- -----------|-------------------------|
| ![](assets/images/ArduinoLeonardo_OLEDDisplayWiring.png) | ![](../advancedio/assets/images/Huzzah32_OLEDWiring_FritzingSchematics.png) |

**Фигура.** Два примера за свързване на OLED дисплея, които описваме подробно в [урока за OLED](../advancedio/oled.md). Можете да кликнете с десния бутон върху изображенията и да изберете "Отвори изображенията в нов раздел", за да ги уголемите.
{: .fs-1 }

#### Кодът за Arduino

Кодът на NoseTracker Arduino е подобен на [предишните уроци](p5js-serial-io.md#parse-serial-data-and-update-oled-debug-output). Просто трябва да:
- **Анализираме входящите серийни данни** в x,y плаващи точки.
- **Преобразуваме нормализираните x,y** позиции в OLED пикселни позиции
- **Нарисуваме лице** на позициите на пикселите x,y
- **Върнем данните** към нашето p5.js приложение за целите на отстраняване на грешки 

За лицето, вместо да го нарисуваме, използвайки примитивни форми (*например,* [`drawCircle`](oled.md#drawing-shapes) извиквания), ще използваме вградената икона за лице от стандартния набор от шрифтове (който е индекс на символ `2`):

{% highlight C++ %}
_display.drawChar(x, y, (unsigned char)2, SSD1306_WHITE, SSD1306_BLACK, CHAR_SIZE);
{% endhighlight C++ %}

! [](assets/images/FaceCharacter2_DefaultFontSet_OLED.png)
**Фигура.** Близък план на иконата на лицето, която ще използваме от стандартния набор от символи.
{: .fs-1 }

##### Анализиране на входящите серийни данни
Първо, декларирайте някои глобални променливи, свързани с рисуването на лица.

{% highlight C++ %}
const int CHAR_SIZE = 3; // задайте размер на шрифта 3
const int DEFAULT_CHAR_WIDTH = 5; // шрифтът по подразбиране е с ширина 5 пиксела при размер 1
const int DEFAULT_CHAR_HEIGHT = 8; // шрифтът по подразбиране е с ширина 8 пиксела при размер 1

int _charWidth = DEFAULT_CHAR_WIDTH * CHAR_SIZE; // изчислете ширината на символа при размер на символа
int _charHeight = DEFAULT_CHAR_HEIGHT * CHAR_SIZE; // изчислете височината на символа при размер на символа

float _faceX = 0; // нормализирана x позиция на лицето
float _faceY = 0; // нормализирайте y позицията на лицето
{% endhighlight C++ %}

Сега, в `loop()` потърсете входящи серийни данни. Ако има серийни данни, прочетете ги и ги анализирайте в x,y floats.

{% highlight C++ %}
void loop() {
// Проверете дали има входящи серийни данни
if(Serial.available() > 0){
// Прочетете данните от сериен порт, докато стигнете до разделителя на края на реда ("\n")
String rcvdSerialData = Serial.readStringUntil("\n"); 

// Разделете низът, разделен със запетая
int indexOfComma = rcvdSerialData.indexOf(",");

if(indexOfComma != -1) {
String strXLocation = rcvdSerialData.substring(0, indexOfComma);
_faceX = strXLocation.toFloat();

String strYLocation = rcvdSerialData.substring(indexOfComma + 1, rcvdSerialData.length());
_faceY = strYLocation.toFloat();
}
 

// Отразяване на данните обратно на сериен порт (за целите на отстраняване на грешки)
Serial.print("# Arduino Received: "");
Serial.print(rcvdSerialData);
Serial.println(""");
}

_display.clearDisplay();
drawFace(_faceX, _faceY); // изчертаване на лицето
_display.display();
delay(DELAY_MS);
}
{% endhighlight C++ %}

##### Рисуване на лицето

Всъщност можем да нарисуваме каквото пожелаем на получената x,y позиция – анимиран спрайт, фигура, *и т.н.*. В този пример просто ще нарисуваме лице.

{% highlight C++ %}
void drawFace(float xFrac, float yFrac){
int x = xFrac * (_display.width() - _charWidth);
int y = yFrac * (_display.height() - _charHeight);

_display.drawChar(x, y, (unsigned char)2, SSD1306_WHITE, SSD1306_BLACK, CHAR_SIZE);
}
{% endhighlight C++ %}

И това е всичко, пълният код е достъпен в GitHub като [NoseTrackerSerialIn.ino](https://github.com/makeabilitylab/arduino/blob/master/Serial/NoseTrackerSerialIn/NoseTrackerSerialIn.ino).

### Видео демонстрация на NoseTracker

Ето по-дълго видео с демонстрация на пълното приложение p5.js + Arduino NoseTracker:

<video autoplay loop muted playsinline style="margin:0px">
<source src="assets/videos/NoseTrackerFullDemo-Optimized.mp4" type="video/mp4" />
</video>
**Видео.** Пълният код е достъпен в [p5.js онлайн редактор](https://editor.p5js.org/jonfroehlich/sketches/QgPPEU5o2) или в GitHub ([жива страница](https://makeabilitylab.github.io/p5js/WebSerial/ml5js/NoseTracker/), [код](https://github.com/makeabilitylab/p5js/tree/master/WebSerial/ml5js/NoseTracker)). Кодът за Arduino е в GitHub като [NoseTrackerSerialIn.ino](https://github.com/makeabilitylab/arduino/blob/master/Serial/NoseTrackerSerialIn/NoseTrackerSerialIn.ino). Можете да игнорирате двата моментно-действащи бутона на платка за прототипи – тук не ги използваме.
{: .fs-1 }

## Представяне на FlappyNose

Използвайки същия p5+ml5 код, NoseTracker ([жива страница](https://makeabilitylab.github.io/p5js/WebSerial/ml5js/NoseTracker/) , [код](https://github.com/makeabilitylab/p5js/tree/master/WebSerial/ml5js/NoseTracker)), можем да създадем много интересни физически изчислителни преживявания. Като един пример, можем да модифицираме кода [FlappyBird.ino](https://github.com/makeabilitylab/arduino/blob/master/OLED/FlappyBird/FlappyBird.ino), който представихме в нашия [OLED урок](../advancedio/oled.md), за да използваме **сериен вход** вместо **цифров вход** (натискане на бутон) за контрол на махането. Ще наречем тази нова версия: FlappyNose! :)

В този случай ще нарисуваме екран с меню, което пита потребителя да избере контрола за "махането" – сериен или бутон. Ако се избере сериен, скицата на Arduino очаква текстово кодирана, разделена със запетая линия от x,y позиции – точно като тази, която предава страницата [NoseTracker](https://makeabilitylab. github.io/p5js/WebSerial/ml5js/NoseTracker/) предава – обаче, в играта използваме само позицията y, за да зададем позицията на "птицата". Вижте видеото по-долу.

<iframe width="736" height="414" src="https://www.youtube.com/embed/AktNXq-cflw" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
**Видео.** Пълна демонстрация на "FlappyNose". Гледайте как постигам висок резултат от 33 точки след няколко опита. :) Приложението p5.js е достъпно в [онлайн редактора p5.js](https://editor.p5js.org/jonfroehlich/sketches/QgPPEU5o2) или в GitHub ([жива страница](https://makeabilitylab.github.io/p5js/WebSerial/ml5js/NoseTracker), [код](https://github.com/makeabilitylab/p5js/tree/master/WebSerial/ml5js/NoseTracker)). Скицата на Arduino е [FlappyBirdSerialIn.ino](https://github.com/makeabilitylab/arduino/blob/master/Serial/FlappyBirdSerialIn/FlappyBirdSerialIn.ino).
{: .fs-1 }


<!-- TODO: Можете да си представите модифициране на това приложение, за да контролирате игра.

Очертание:
- Покажи Елмо
- Покажи проследяване на лицето на Елмо + Arduino
- Адаптирай код за flappy bird
- Покажи цялото тяло на OLED? Може би с обърнат дисплей? -->


<!-- Physcomp + ml:
- https://experiments.withgoogle.com/objectifier-spatial-programming
- https://experiments.withgoogle.com/tfmicrochallenge -->

## Ресурси

- [Машинно обучение за уеб](https://github.com/yining1023/machine-learning-for-the-web), курс на Yining Shi в ITP, NYU

- [Начално ръководство за машинно обучение с ml5.js](https://www.youtube.com/playlist?list=PLRqwX-V7Uu6YPSwT06y_AEYTqIwbeam3y), YouTube поредицата Coding Train на Даниел Шифман
