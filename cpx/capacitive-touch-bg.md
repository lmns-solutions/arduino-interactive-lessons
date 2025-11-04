---
lang: bg
permalink: /cpx/capacitive-touch.html
page_id: cpx-capacitive-touch
layout: default
title: L5&#58; Капацитивен сензорен екран
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

В урок 5 от нашата серия CPX ще научим как да използваме капацитивното сензорно докосване. Това е серия от няколко части, която започва с въведение в капацитивното сензорно докосване.

## Урок 5.1: Въведение в капацитивното сензорно докосване на CPX

В този урок първо ще представим концепцията за капацитивното сензорно докосване, преди да построим просто капацитивно сензорно "пиано". След това ще покажем как да визуализираме суровите стойности на капацитета и праговите стойности на капацитивното докосване, които се използват за задействане на капацитивни събития. На трето място, ще разгледаме как да използваме както автоматична, така и ръчна калибрация, за да променим прага на капацитивното докосване, преди да създадем капацитивно-отзивчив инструмент (подобен на [Урок 4: Светло-отзивчив инструмент](sensor-instrument.md)). 

<div class="iframe-container">
<iframe width="100%" src="https://www.youtube.com/embed/HKwtXrTdocE" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>
</div>

### Урок 5.1 Код

Ето линк към програмите, които създадохме в урок 5.1.

- [Код за графично представяне на капацитета A1](https://makecode.com/_EWVVviTtzWC5)
- [Код за графично представяне на капацитета A1, прага на допир и прекалибриране](https://makecode.com/_XKm2wUYgWcw9)
- [Код за инструмент с капацитивен отговор (близост!)](https://makecode.com/_8pAMay1XXg6W)

## Урок 5.2: Капацитивно сензиране с предмети от ежедневието

Въз основа на 5.1 ще създадем прототип на интерактивно пиано от ежедневни предмети като портокал, банан и кутия сода с CPX, MakeCode и капацитивно сензорно докосване. Отново ще покажем колко е важно да се измерват капацитетните стойности на докосване на различни предмети и да се използва автоматична или ръчна калибрация за конфигуриране на праговете на капацитетно докосване.

<div class="iframe-container">
<iframe width="100%" src="https://www.youtube.com/embed/_eMAbP7ATOU" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>
</div>

### Урок 5.2 Код

Ето линк към програмите, които създадохме в урок 5.2.

- [Код за капацитивно-сензорно пиано](https://makecode.com/_X18RPxJte8EU)

## Урок 5.3: Изработване на капацитивна сензорна клавиатура

Въз основа на 5.2 ще използваме капацитивно докосване, за да създадем персонализирана клавиатура и да възпроизвеждаме музика и видео игри с плодове, монети и кутии от сода. По същество ще накараме лаптопа ви да мисли, че CPX е клавиатура, и ще се забавляваме, като използваме различни предмети като клавиши!

<div class="iframe-container">
<iframe width="100%" src="https://www.youtube.com/embed/DrqrGA9OtvE" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>
</div>

### Урок 5.3 Код

Ето линк към програмите, които създадохме в урок 5.3.

- [Код за капацитивна сензорна клавиатура](https://makecode.com/_cfwTFgTK1AAy)

## Урок 5.4: Изработване на Lo-fi капацитивен сензорен контролер за Nintendo

Въз основа на 5.3 ще използваме капацитивно сензорно засичане, за да изработим персонализиран Lo-fi контролер за Nintendo NES от картон, медна лента и алуминиево фолио и да играем Super Mario Bros.

<div class="iframe-container">
<iframe width="100%" src="https://www.youtube.com/embed/2HasGGKsyI0" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>
</div>

### Урок 5.4 Код

Ето линк към програмите, които създадохме в урок 5.4.

- [Код за геймпад с капацитивен сензор](https://makecode.com/_2q5bAx9ch5am)

<!-- Идеи за урок 5.5 и след него:
- Направете "Саймън казва" с сензорни панели и звук. Вижте: https://learn.adafruit.com/simon-game-clone-with-circuitplayground-express-and-circuitpython 
-
- -->

<!-- Поток:
Не забравяйте, че A0 не може да се използва за капацитивен сензор
- Започнете с крайния резултат. Капацитивно сензорно плодово пиано (бележка: може да се редактира)

- След това много просто с капацитивно докосване на A1. Не забравяйте, че A0 не може да се използва за капацитивно докосване. Покажете диаграмата.
- Изградете докосване на A1. Покажете конзолата, когато пръстът ви докосне панела.
- След това изградете сензорни панели A1 - A3
- Но най-вълнуващата част е, когато се свържем с други проводими обекти. Да опитаме с 
- Ето код за просто капацитивно докосване на A1, който показва и прага. Този праг е много важен
,
 тъй като той задейства събитието на докосване. https://makecode.com/_EWVVviTtzWC5
- Как работи това? Когато програмата ви стартира за първи път, тя извиква калибрационна последователност за сензорните панели, която определя прага на капацитет, необходим за задействане на докосване. Нека да разгледаме
- След това го изградете на всички сензорни панели от A1 до A3
- Сега идва забавната част. Можем да свържем външни обекти, които са проводими. "Свързването на обект с сензорен пин може да го превърне в сензор за докосване. Когато някой обект е свързан с пин, той променя капацитета, който се измерва за пина. Когато програмата ви стартира, тя калибрира измерването на капацитета за повърхността на пина и всеки обект, свързан с него. Това й позволява да открива правилно докосването ви." https://makecode.adafruit.com/learnsystem/pins-tutorial/touch-input/sensor-objects

- След това покажете как да направите жест с навеждане, който променя тона? -->

<!-- Капацитивната сензорна технология работи чрез измерване на промяната в капацитета (способността на дадена система да съхранява електрически заряд) в рамките на проекционното си поле поради наличието на проводим обект. Вижте: https://www.rspinc.com/blog/contract-manufacturing/what-is-a-capacitive-touch-sensor-how-are-they-used/ -->

<!-- От Уикипедия:
"Капацитивното сензиране (понякога капацитно сензиране) е метод за електрическо сензиране, който може да открива и измерва всичко, което е проводимо или има диелектрична константа (която е мярка за способността на дадено вещество да съхранява енергия), различна от тази на въздуха. ...

Много видове сензори използват капацитивно сензиране, включително сензори за откриване и измерване на близост, налягане, влажност.

Вие сте заобиколени от капацитивно сензиране – така работят и съвременните сензорни екрани и сензорни панели." -->

<!-- Adafruit Touch Sensor Docs: https://makecode.adafruit.com/reference/input/button/touch-sensors 
Adafruit Capacitive lesson: https://learn.adafruit.com/make-it-sense/makecode-6-->

## Референции

<!-- https://makecode.adafruit.com/learnsystem/pins-tutorial/devices/capacitors -->

- [Капацитивен сензорен вход на CPX](https://makecode.adafruit.com/learnsystem/pins-tutorial/touch-input), Adafruit MakeCode Documentation

- [Калибриране на капацитивната чувствителност](https://makecode.adafruit.com/learnsystem/pins-tutorial/touch-input/calibrate-sensitivity), документация на Adafruit MakeCode

- [Създаване на сензорни обекти](https://makecode.adafruit.com/learnsystem/pins-tutorial/touch-input/sensor-objects), документация на Adafruit MakeCode

## Как работят капацитивните и резистивните сензори

Ако искате да научите повече за това как работят капацитивните и резистивните сензорни екрани, вижте по-долу:

- [Капацитивни сензорни екрани](https://youtu.be/BR4wNq6WGkg), Tufts Final Project 2015
- [Използване на резистивен сензорен екран](https://www.youtube.com/watch?v=_GT_sgbKQrc), DroneBot Workshop
- [Как да добавите капацитивно сензиране към всеки Arduino проект](https://www.digikey.com/en/maker/blogs/2021/how-to-add-capacitive-sensing-to-any-arduino-project), Maker.io

<!-- ## Предишна лекция

<span class="fs-6">
[Предишен: Инструмент, реагиращ на светлина](sensor-instrument.md){: .btn .btn-outline }
</span> -->

## Следващ урок

В [следващия урок](cpx-keyboard.md) ще разгледаме отново използването на CPX като програмируема клавиатура и ще задълбочим разбирането си.

<span class="fs-6">
[Предишен: Инструмент, реагиращ на светлина](sensor-instrument.md){: .btn .btn-outline }
[Следващ: CPX като клавиатура](cpx-keyboard.md){: .btn .btn-outline }
</span>
