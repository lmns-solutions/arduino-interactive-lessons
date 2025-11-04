---
lang: bg
permalink: /cpx/makecode.html
page_id: cpx-makecode
layout: default
title: L2&#58; Създаване с MakeCode
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

В този урок ще създадем първата си програма MakeCode+CPX, наречена Blinky, която ще възпроизвежда звуков ефект в началото и след това ще мига многократно. Докато я създаваме, ще научим за програмната среда MakeCode, симулатора и как да заредим програмата си на CPX.

## Програмна среда MakeCode

<video autoplay loop muted playsinline style="margin:0px">
<source src="assets/videos/Making_SimpleFastAnimationProgram_MakeCode_ScreenRecording.mp4" type="video/mp4" />
</video>
**Видео.** Бързо създаване на пълна програма с MakeCode: проста анимация на дъга. [Връзка към кода](https://makecode.com/_8uY3D8Fc8A5t).
{: .fs-1 }

MakeCode е визуален език за програмиране — подобен на [Scratch](https://scratch.mit.edu/) — създаден на базата на [Blockly](https://developers.google.com/blockly). Както показва видеото по-горе, за да програмирате CPX, просто плъзгате и пускате "парчета от пъзел". Наричаме тези парчета *блокове*. Като съчетавате блоковете, можете да създавате интерактивни програми!

<!-- Някои от вас може би са запознати с подобни езици като [Scratch](https://scratch.mit.edu/) или с интерфейсите за въведение в програмирането, използвани от [code.org](https://code.org/student/elementary). -->

### Интерфейсът на MakeCode

![](assets/images/MakeCode_ProgrammingInterface.png)
**Фигура.** Снимка на интерфейса на MakeCode с бележки, подчертаващи (1) работната среда за програмиране, (2) кутията с инструменти и (3) симулатора.
{: .fs-1 }

Редакторът MakeCode има три основни области на потребителския интерфейс: (1) работна среда за програмиране, (2) кутия с инструменти и (3) симулатор. Използвайте:

1. **Работното пространство за програмиране**, за да създадете програмата си чрез плъзгане и пускане на парчетата от пъзела
2. **Кутията с инструменти**, за да извадите парчетата от пъзела (известни още като блокове)
3. **Симулатора**, за да тествате програмата си, преди да я изтеглите на CPX

## Нашата първа програма: Blinky

Нека да създадем първата си програма: Blinky! За начало ще накараме Blinky да мига с всичките десет NeoPixel LED диода на CPX. След това ще добавим специален "стартов" звук, за да представим други програмируеми елементи.

<video autoplay loop muted playsinline style="margin:0px">
<source src="assets/videos/Making_Blinky_MakeCode_FinalLoop.mp4" type="video/mp4" />
</video>
**Видео.** Първоначалната програма Blinky: забележете как светлините на симулатора (NeoPixels) мигат в червено за 500 ms, след което гаснат за 500 ms и цикълът се повтаря.
{: .fs-1 }

Докато създавате програмата си, наблюдавайте как симулаторът вляво показва нейното поведение в реално време – забележете мигащите LED диоди във видеото по-горе. Когато правите промени в MakeCode, симулаторът автоматично ще се рестартира.

### Стъпка 1: Създаване на нов проект

За да започнете, отидете на [https://makecode.adafruit.com/](https://makecode.adafruit.com) и кликнете върху бутона "Нов проект".

![](assets/images/MakingBlinky_StartingANewProject.png)
**Фигура.** В [уебсайта на MakeCode](https://makecode.adafruit.com) кликнете върху бутона "Нов проект".
{: .fs-1 }

След като кликнете, трябва да видите интерфейса на редактора MakeCode с почти празна работна среда (вижте екранната снимка по-долу). Може да забележите, че MakeCode предварително попълва работната среда с блок [`forever`](https://makecode.adafruit.com/reference/loops/forever), който стартира автоматично и се изпълнява многократно в цикъл *forever.*

![](assets/images/MakingBlinky_TheForeverBlock.png)
**Фигура.** Блокът [`forever`](https://makecode.adafruit.com/reference/loops/forever) стартира автоматично и се изпълнява многократно в цикъл *forever. * Не забравяйте, че винаги можете да кликнете с десния бутон върху тези изображения и да изберете "Отвори изображението в нов раздел", за да ги видите в по-голям размер.
{: .fs-1 }

За Blinky ще поставим програмата си в този блок [`forever`](https://makecode.adafruit.com/reference/loops/forever), но това не винаги е необходимо (както ще видим в следващите уроци).

### Стъпка 2: Добавете блок за светлина

Сега нека добавим първия си блок: блок [`LIGHT`](https://makecode.adafruit.com/reference/light), за да включим светлините, т.е. 10-те NeoPixels. Има много различни възможности за блок [`LIGHT`](https://makecode.adafruit.com/reference/light), но засега нека използваме блока [`set all pixels to`](https://makecode.adafruit.com/reference/light/set-all), който ще настрои всички 10 NeoPixels на един и същи цвят.

От менюто [`LIGHT`](https://makecode.adafruit.com/reference/light) в инструменталната кутия, плъзнете и пуснете блока [`set all pixels to`](https://makecode.adafruit.com/reference/light/set-all) в работната област.
 

![](assets/images/MakingBlinky_TheFirstLightBlock.png)
**Фигура.** Плъзнете и пуснете блока [`set all pixels to`](https://makecode.adafruit.com/reference/light/set-all) от менюто [`LIGHT`](https://makecode.adafruit.com/reference/light).
{: .fs-1 }

Поставете блока [`задай всички пиксели на`](https://makecode.adafruit.com/reference/light/set-all) вътре в блока [`forever`](https://makecode.adafruit.com/reference/loops/forever) в работната среда. Програмата ви сега трябва да изглежда така:

![](assets/images/MakingBlinky_TheSetAllPixelsToBlock.png)
**Фигура.** Блокът [`задай всички пиксели на`](https://makecode.adafruit.com/reference/light/set-all) задава на всички 10 CPX светлини (NeoPixels) един и същ цвят. В този случай ще ги зададем на червено.
{: .fs-1 }

Забележете също как NeoPixels сега светят в червено в симулатора – страхотно!

### Стъпка 3: Добавете блок за пауза

За да накараме светлината да **мига**, трябва да добавим блок [`pause`](https://makecode.adafruit.com/reference/loops/pause), който е малко скрит в менюто на инструментариума [`LOOPS`](https://makecode.adafruit.com/blocks/loops). Кликнете върху бутона [`LOOPS`](https://makecode.adafruit.com/blocks/loops) в менюто и плъзнете и пуснете блока [`pause`](https://makecode.adafruit.com/reference/loops/pause) в работната област.

![](assets/images/MakingBlinky_AddingTheFirstPauseBlock.png)
**Фигура.** Плъзнете и пуснете блока [`pause`](https://makecode.adafruit.com/reference/loops/pause) от менюто на инструментариума [`LOOPS`](https://makecode.adafruit.com/blocks/loops).
{: .fs-1 }

Нека настроим червената светлина да остане включена за половин секунда (500 милисекунди), преди да преминем към следващото парче от пъзела.

![](assets/images/MakingBlinky_DescribingThePauseBlock.png)
**Фигура.** Блокът [`pause`](https://makecode.adafruit.com/reference/loops/pause) спира програмата ви за определено време. В този случай нека го настроим на половин секунда (500 ms), така че червената светлина да свети в продължение на 500 ms.
{: .fs-1 }

### Стъпка 4: Изключване на светлината

Накрая, за да завършим мигащия ефект, трябва да изключим светлините. Отново можем да използваме блока [`set all pixels to`](https://makecode.adafruit.com/reference/light/set-all).

![] (assets/images/MakingBlinky_AddingSecondLightBlock.png)
**Фигура.** За да изключим светлината, ни е необходим още един блок за светлина. Плъзнете и пуснете втори блок [`set all pixels to`](https://makecode.adafruit.com/reference/light/set-all) от менюто [`LIGHT`](https://makecode.adafruit.com/reference/light).
{: .fs-1 }

Този път ще настроим цвета на светлината на черно. В MakeCode настройването на светлините на черно е равносилно на изключването им. Можете да изберете друг цвят, ако желаете.

![](assets/images/MakingBlinky_SettingSecondLightBlockToBlack.png)
**Фигура.** За да промените цветовете на светлините в блока [`задаване на всички пиксели на`](https://makecode.adafruit.com/reference/light/set-all), кликнете върху овалното цветно поле и изберете цвят от изскачащото меню.
{: .fs-1 }

### Стъпка 5: Добавете финален блок за пауза
Както и преди, трябва да добавим блок [`pause`](https://makecode.adafruit.com/reference/loops/pause), който ще контролира колко дълго светлините ще са изключени, преди да се върнем в началото на програмата.

![](assets/images/MakingBlinky_AddingFinalPauseBlock.png)
**Фигура.** Плъзнете и пуснете блока [`pause`](https://makecode.adafruit.com/reference/loops/pause) от менюто на инструментариума [`LOOPS`](https://makecode.adafruit.com/blocks/loops).
{: .fs-1 }

Крайната ни програма трябва да изглежда така. Тъй като кодът ни се намира в блок [`forever`](https://makecode.adafruit.com/reference/loops/forever), той ще се повтаря вечно, създавайки безкрайно мигане на червени светлини.

![](assets/images/MakingBlinky_LoopingBackToTheBeginning.png)
**Фигура.** Тъй като кодът ни се намира в блок [`forever`](https://makecode.adafruit.com/reference/loops/forever), той ще се повтаря вечно, създавайки безкрайно мигане на червени светлини.
{: .fs-1 }

### Видео за създаването на Blinky

Ето пълно видео с инструкции за създаването на Blinky от начало до край в MakeCode само за 30 секунди. Това наистина демонстрира колко бързо можем да създадем прототип на електронни поведения с MakeCode+CPX.

<video autoplay loop muted playsinline style="margin:0px">
<source src="assets/videos/Making_Blinky_MakeCode_ScreenRecording.mp4" type="video/mp4" />
</video>
**Видео.** Пълно видео с инструкции за изграждане на Blinky от начало до край само за 30 секунди. Можете да спрете видеото или да го отворите в нов прозорец за пълен екран (кликнете с десния бутон върху видеото и изберете "Отвори видео в нов прозорец").
{: .fs-1 }

## Добавяне на звук към Blinky

Преди да изтеглите Blinky на физическата CPX платка, нека добавим още едно нещо: "стартиращ" звук, който се възпроизвежда при първоначалното включване (или ресет) на CPX.

<video autoplay loop muted playsinline style="margin:0px">
<source src="assets/videos/Making_BlinkyWithPowerUp_ScreenRecording.mp4" type="video/mp4" />
</video>
**Видео.** Добавяне на звук при стартиране към Blinky. Сега, когато Blinky се включи, ще възпроизведе звук.
{: .fs-1 }

### Стъпка 1: Добавете блок "при стартиране"

В допълнение към блока [`forever`](https://makecode.adafruit.com/reference/loops/forever), който се изпълнява многократно, MakeCode има и блок [`on start`](https://makecode.adafruit.com/blocks/on-start), който се изпълнява при първото стартиране на програмата. Това е идеалното място за поставяне на кода за "звук при стартиране"!

Отворете менюто на инструментариума [`LOOPS`](https://makecode.adafruit.com/blocks/loops) и плъзнете и пуснете блока [`on start`](https://makecode.adafruit.com/blocks/on-start) в работното си пространство.

![](assets/images/MakingBlinkyWithSound_AddingInOnStart.png)
**Фигура.** Плъзнете и пуснете блока [`on start`](https://makecode.adafruit.com/blocks/on-start) от менюто на инструментариума [`LOOPS`](https://makecode.adafruit.com/blocks/loops).
{: .fs-1 }

Сега вашата програма Blinky трябва да изглежда така. Аз произволно поставих блока [`on start`](https://makecode.adafruit.com/blocks/on-start) до блока [`forever`] (https://makecode.adafruit.com/blocks/on-start) блок – можете да го поставите където пожелаете. Независимо от позицията му в редактора, блокът [`on start`](https://makecode.adafruit.com/blocks/on-start) винаги ще се изпълнява преди блока [`forever`](https://makecode.adafruit.com/blocks/on-start).

![](assets/images/MakingBlinkyWithSound_OnStartDescription.png)
**Фигура.** Блокът [`on start`](https://makecode.adafruit.com/blocks/on-start) се изпълнява автоматично при първото стартиране на програмата.
{: .fs-1 }

### Стъпка 2: Добавяне на звук

Дотук сме програмирали само един тип изход, [светлина](https://makecode.adafruit.com/reference/light), но има и звук! За звука можем да използваме менюто [`MUSIC`](https://makecode.adafruit.com/reference/music) от инструментариума.

Нека използваме блока [`play sound`](https://makecode.adafruit.com/reference/music/play-sound), който възпроизвежда предварително програмиран звук като "power up" или "jump up" (тези звуци може да ви са познати, тъй като някои от тях са от Super Mario!).

![](assets/images/MakingBlinkyWithSound_TheMusicMenu.png)
**Фигура.** Плъзнете и пуснете блока [`play sound`](https://makecode.adafruit.com/reference/music/play-sound) от менюто на инструментите [`MUSIC`](https://makecode.adafruit.com/reference/music).
{: .fs-1 }

Можете да изберете която и да е опция за звук. Ние ще използваме "power up". Веднага след като добавите този блок, трябва да чуете звука в симулатора (ако звукът ви е включен и имате високоговорители/слушалки).

![](assets/images/MakingBlinkyWithSound_ThePlaySoundBlock.png)
**Фигура.** Блокът [`play sound`](https://makecode.adafruit.com/reference/music/play-sound) възпроизвежда избрания звук.
{: .fs-1 }

### Стъпка 3: Крайната програма

Успяхте! Крайната програма трябва да изглежда така:

![](assets/images/MakingBlinkyWithSound_TheFinalProgram.png)
**Фигура.** Крайната програма ["Blinky with Sound"](https://makecode.com/_2iL2xkVKa7Dh) в MakeCode. Можете да редактирате и да си играете с нашия код [тук](https://makecode.com/_2iL2xkVKa7Dh) — ние променихме цвета от червен на син.
{: .fs-1 }

## Прехвърляне на програмата ни към CPX

Досега използвахме симулатора, за да тестваме и стартираме Blinky. Но истинската сила и удоволствие от физическото програмиране и CPX е работата с *физически материали.* Затова трябва да прехвърлим Blinky от лаптопа ви към CPX.

<!-- След като CPX е програмиран, можете да го откачите от компютъра си и да го захранвате с батерия. Вашата MakeCode програма "живее" в CPX! -->

Има два начина за прехвърляне на MakeCode програми към CPX:
 

1. **Ръчно изтегляне.** Чрез ръчно изтегляне на програмата и копирането й в CPX (сякаш CPX е USB флашка).
2. **Директно изтегляне.** Чрез използване на експериментална WebUSB функция за директно изтегляне на програмата ви в CPX. Когато работи, това се усеща като много плавно. Въпреки това, тъй като тази функция е експериментална, тя е малко нестабилна, което може да доведе до разочарование.

По-долу ще разгледаме и двата начина. Препоръчваме поне да опитате подхода с "пряко изтегляне" и да се върнете към ръчното изтегляне, когато той не работи.

### Ръчно изтегляне

<video autoplay loop muted playsinline style="margin:0px">
<source src="assets/videos/CopyingProgramToCPXFromMac_NoSound.mp4" type="video/mp4" />
</video>
**Видео.** Изтегляне на програма MakeCode и прехвърляне към CPX с помощта на Mac.
{: .fs-1 }

Ръчното изтегляне на програмата MakeCode към CPX е процес от 4 стъпки:

1. **Изтегляне.** Кликнете върху розовия бутон "Изтегляне", който ще изтегли файл `.uf2` във вашата папка за изтегляния;
2. **Свържете CPX.** Свържете CPX към вашия лаптоп/компютър с помощта на USB микро кабел.
3. **Преведете CPX в състояние, подходящо за програмиране.** Кликнете върху бутона "Reset" (Нулиране) на CPX. CPX трябва да светне в зелено и да монтира нова папка "thumb drive" (флашка), наречена CPLAYBOOT; 
4. **Преместете файла .uf2 в CPLAYBOOT** Плъзнете и пуснете изтегления файл `.uf2` в CPLAYBOOT. Когато файлът приключи копирането, CPX ще се рестартира автоматично и ще започне да изпълнява програмата ви, което също ще прекъсне връзката на CPX с лаптопа/компютъра ви.

![](assets/images/ThreeStepProcessForManuallyProgrammingCPX.png)

**Фигура.** След като кликнете върху розовия бутон "Изтегли" в MakeCode, интерфейсът на MakeCode показва този триетапен подкана за прехвърляне на изтегления файл `.uf2` към CPX.
{: .fs-1 }

Ще ви покажем как да направите това както за Windows, така и за Mac.

#### Ръчно изтегляне с Mac

<video playsinline controls style="margin:0px">
<source src="assets/videos/CopyingProgramToCPXFromMac.mp4" type="video/mp4" />
</video>
**Видео.** Изтегляне на програма MakeCode и прехвърляне към CPX с Mac.
{: .fs-1 }

#### Ръчно изтегляне с Windows

<iframe width="736" height="414" src="https://www.youtube.com/embed/Y_jkUylGe4E" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

**Видео.** Ръчно изтегляне и прехвърляне на програмата MakeCode на CPX с Windows ([YouTube link](https://youtu.be/Y_jkUylGe4E))
{: .fs-1 }

### Директно изтегляне с WebUSB

В това видео ще ви покажем как да изтеглите директно програмата си MakeCode на CPX с помощта на WebUSB. Това е много по-идеален и безпроблемен начин за програмиране на MakeCode, но не винаги работи надеждно. Трябва да използвате уеб браузърите Chrome или Microsoft Edge и трябва да работи както за Mac, така и за Windows.

<iframe width="736" height="414" src="https://www.youtube.com/embed/7FjYEJhVeLY" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

**Видео.** Директно изтегляне на програмата MakeCode на CPX чрез WebUSB ([YouTube link](https://youtu.be/7FjYEJhVeLY))
{: .fs-1 }

## Споделяне на програмата MakeCode

Ако искате да споделите програмата си с други, кликнете върху бутона "Сподели" в лентата за навигация и копирайте/поставяйте предоставения URL адрес. Вижте видеото по-долу.

<video loop muted playsinline style="margin:0px" controls>
<source src="assets/videos/MakeCode_SharingYourProject2.mp4" type="video/mp4" />
</video>
**Видео.** За да споделите програмата си MakeCode с други, кликнете върху бутона "Сподели" в лентата за навигация и копирайте/поставяйте URL адреса. [Връзка към кода](https://makecode.com/_JdPfj8VrmWV3).
{: .fs-1 }

## Дизайнерска дейност

Успяхме! Успешно създадохме първата си програма в MakeCode, я стартирахме в симулатора и след това я изтеглихме на нашия CPX хардуер. Научихме също как да добавяме звук и да споделяме програмата си с други хора.

За дизайнерското предизвикателство в този урок опитайте да видите колко различни начини има да създадете интересни светлинни модели с MakeCode, като използвате команди като show animation, photon и други! По-долу сме включили един прост пример, но можете да направите много повече!

<video autoplay loop muted playsinline style="margin:0px">
<source src="assets/videos/MakeCode_SimpleNeoPixelFun_Optimized.mp4" type="video/mp4" />
</video>
**Видео.** Много проста площадка с различни NeoPixel анимации, вградени в MakeCode [линк към кода](https://makecode.com/_AxFigA8KX82K). Използваме и команди за извеждане на конзолата, за да ни помогнат да се позоваваме на различните анимации.
{: .fs-1 }

## Следващ урок

В [следващия урок](button-piano.md) ще създадем първата си интерактивна програма: пиано с бутони!

<span class="fs-6">
[Предишен: Въведение в CPX](cpx.md){: .btn .btn-outline }
[Следващ: Пиано с бутони](button-piano.md){: .btn .btn-outline }
</span>

<!-- TODO:
- Добавете запазване и споделяне на проекти
- Добавете дизайнерско предизвикателство за използване на повече светлини? Покажете пример за празнични светлини от децата
- Добавете идеята, че след като изтеглите програмата си, тя се изпълнява на CPX
- -->
