---
lang: bg
permalink: /cpx/sensor-instrument.html
page_id: cpx-sensor-instrument
layout: default
title: L4&#58; Инструмент за измерване на нивото на осветеност
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

В този урок ще надградим последния урок – [Button Piano](button-piano.md) – за да създадем интерактивен инструмент, който преобразува нивата на осветеност в звук и светлина. Звукът няма да е страхотен, но ще е забавен!

<!-- TODO обмислете добавянето на кратко видео с терменвок? -->

## Видео урок

<div class="iframe-container">
<iframe width="100%" src="https://www.youtube.com/embed/RlEPQqyQGEk" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>
</div>

**Видео.** Създаване на инструмент със светлинен сензор. Ето [пълният код](https://makecode.com/_drYKXH5UeV1r) и [линк към видеото в YouTube](https://youtu.be/RlEPQqyQGEk).
{: .fs-1 }

## Код

Ето окончателният [код](https://makecode.com/_2dVi02gquH6h). Кликнете с десния бутон върху кода по-долу и изберете "Отвори линка в нов раздел", за да го отворите в редактора MakeCode.

<div style="position:relative;height:calc(300px + 5em);width:100%;overflow:hidden;"><iframe style="position:absolute;top:0;left:0;width:100%;height:100%;" src="https://makecode.adafruit.com/---codeembed#pub:_2dVi02gquH6h" allowfullscreen="allowfullscreen" frameborder="0" sandbox="allow-scripts allow-same-origin"></iframe></div>

<!-- <div style="position:relative;height:0;padding-bottom:70%;overflow:hidden;"><iframe style="position:absolute;top:0;left:0;width:100%;height:100%;" src="https://makecode.adafruit.com/ #pub:_K9Xddy0gk1hY" frameborder="0" sandbox="allow-popups allow-forms allow-scripts allow-same-origin"></iframe></div>

<div style="position:relative;height:0;padding-bottom:100.0%;overflow:hidden;"><iframe style="position:absolute;top:0;left:0;width:100%;height:100%;" src="https://makecode.adafruit.com/---run?id=_K9Xddy0gk1hY" allowfullscreen="allowfullscreen" sandbox="allow-popups allow-forms allow-scripts allow-same-origin" frameborder="0"></iframe></div> -->

## Блокове

В този пример използваме следните блокове. Вижте ръководството [Adafruit MakeCode Reference](https://makecode.adafruit.com/reference).

### Изход

За изход използвахме блокове **[Light](https://makecode.adafruit.com/reference/light)**, **[Music](https://makecode.adafruit.com/reference/music)** и **[Console](https://makecode.adafruit.com/reference/console)**, по-специално:

- **[graph](https://makecode.adafruit.com/reference/light/graph)** превръща вградените NeoPixels в "барграф" в реално време
- **[ring tone](https://makecode.adafruit.com/reference/music/ring-tone)** възпроизвежда тон с дадена честота
- **[set volume](https://makecode.adafruit.com/reference/music/set-volume)** настройва силата на звука на изходния високоговорител
- **[stop all sounds](https://makecode.adafruit.com/reference/music/stop-all-sounds)** спира възпроизвеждането на всички звуци
- **[конзолен лог](https://makecode.adafruit.com/reference/console)** записва ред текст в конзолния изход

### Вход

За **[блокове за вход](https://makecode.adafruit.com/reference/input)** използвахме:

- **[ниво на осветеност](https://makecode.adafruit.com/reference/input/light-level)** измерва нивото на осветеност между 0 (тъмно) и 255 (светло)
- **превключвател надясно** е вярно, ако превключвателят е надясно; обаче не успях да намеря документация за този блок

### Логика

Използвахме и един [логически блок](https://makecode.adafruit.com/blocks/logic), за да проверим дали превключвателят е надясно и, ако е така, да възпроизведем звука. В противен случай да спрем всички звуци.

- **[if](https://makecode.adafruit.com/blocks/logic)** изпълнява код в зависимост от това дали дадено изявление е вярно

### Събитие

За да се уверим, че силата на звука е настроена правилно, я инициализираме на 255 (най-високата стойност), когато програмата стартира за първи път, използвайки блока [on start](https://makecode.adafruit.com/blocks/on-start)

- **[on start](https://makecode.adafruit.com/blocks/on-start)** се изпълнява веднъж и само веднъж, когато програмата стартира

## Дизайнерска дейност

{: .note }
Примерите, които включваме тук, са умишлено по-сложни, за да помогнат да се демонстрира мощността и потенциалът на MakeCode с CPX. Няма проблем, ако не разбирате нещо. Ще стигнем дотам!

Как бихте могли да използвате другите вградени сензори, за да създадете музика? Опитайте да си поиграете с [**ускорение** (движение)](https://makecode.adafruit.com/reference/input/acceleration), [**ниво на звука**](https://makecode.adafruit.com/reference/input/sound-level) и [**температура**](https://makecode.adafruit.com/reference/input/temperature) . Например, ние създадохме [пример за инструмент, базиран на акселерометър](https://makecode.com/_fbsJcbKMgJxv), който променя тона и силата на звука въз основа на ускорението по ос y и x, съответно. Не е необходимо да създавате нещо толкова сложно, но опитайте да експериментирате с различни сензори!

![Снимка на MakeCode, показваща инструмента с акселерометър](assets/images/MakeCode_AccelerometerInstrument.png)
**Фигура.** Инструмент, базиран на акселерометър, който променя тона и силата на звука въз основа на ускорението по ос y и x, съответно. Ето [пълния код](https://makecode.com/_fbsJcbKMgJxv).
{: .fs-1 }

Във връзка с това, как бихте могли да подобрите *начина*, по който звучи музиката? В [примера по-долу](https://makecode.com/_49zec62PC6eJ) ние съпоставяме нивото на осветеност с нотите в гамата C, като използваме предварително дефиниран масив от честоти (всяка честота се съпоставя с музикална нота в гамата C, която е индексирана въз основа на нивото на осветеност).

![Снимка на MakeCode, показваща инструмента с сензор за светлина, съответстващ на гамата До](assets/images/MakeCode_LightSensorInstrumentCScale.png)

**Фигура.** По-усъвършенстван инструмент с сензор за светлина, който преобразува нивата на светлината в ноти от гамата До. Ето [пълният код](https://makecode.com/_49zec62PC6eJ).
{: .fs-1 }

По същия начин, [ето версия](https://makecode.com/_RCK2f5KhHLby), която съпоставя x компонента на акселерометъра с ноти в музикалната гама C.

<!-- <div style="position:relative;height:calc(300px + 5em);width:100%;overflow:hidden;"><iframe style="position:absolute;top:0;left:0;width:100%;height:100%;" src="https://makecode.adafruit.com/---codeembed#pub:_bb6Musb9aVex" allowfullscreen="allowfullscreen" frameborder="0" sandbox="allow-scripts allow-same-origin"></iframe></div> -->

## Следващ урок

В [следващия урок](capacitive-touch) ще представим поредица от няколко части за използването на капацитивно сензиране за взаимодействие с предмети от ежедневието и други!

<span class="fs-6">
[Предишен: Пиано с бутони](button-piano.md){: .btn .btn-outline }
[Следващ: Капацитивно сензорно засичане](capacitive-touch.md){: .btn .btn-outline }
</span>
