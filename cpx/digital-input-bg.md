---
lang: bg
permalink: /cpx/digital-input.html
page_id: cpx-digital-input
layout: default
title: L9&#58; Цифров вход
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

В урок 9 продължаваме да изследваме как да свързваме и използваме външни електронни устройства с нашия CPX. В урок 8 работихме с аналогов вход, който преобразува напрежението от 0 - 3,3V в 0 - 1023. В урок 9 ще работим с **цифров вход**, който преобразува входните сигнали на напрежение в ON (1) или OFF (0). Това е полезно за компоненти като бутони.

## Урок 8.1: Общ преглед на цифровия вход

В този урок ще научим какво е **цифров вход** и как да го използваме в Circuit Playground Express (CPX). Започваме по същия начин като в [уроците за аналоговия вход](analog-input.md): представяме 3.3V, GND и A1 CPX свързващите подложки и показваме как функцията **цифрово четене** реагира на различни входни напрежения (например 3.3V, GND).

<div class="iframe-container">
<iframe width="100%" src="https://www.youtube.com/embed/raIc-EuHfmc?si=-KCgO3ypF9kPKBVd" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>
</div>

## Урок 8.2: Свързване на бутони към CPX и защо са необходими пулдаун резистори?

В това видео представяме решение на проблема с "плаващите пинове” чрез използване на пулдаун резистори и свързваме първия си бутон към CPX.

<div class="iframe-container">
<iframe width="100%" src="https://www.youtube.com/embed/mFXvAfsiRx0?si=_6ks-_M8sWD0XlSQ" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>
</div>

{: .note }
Ако искате да пропуснете цялата теория за това защо се използват пул-даун резистори и просто да "следвате рецептата” за свързване на бутон, [прескочете до 13:54 във видеото ни](https://youtu.be/mFXvAfsiRx0?si=jWkx5H2zZZ5vhSaB&t=834). Можете да научите повече за "проблема с плаващия пин" и други теми в [Arduino L1: Използване на бутони](../arduino/buttons.md).

### Схеми на вериги

![](assets/images/CPX_ExternalPullDownAndPullUpResistors.png)

### Код

- [Пример за MakeCode за пулдаун резистор](https://makecode.com/_abT69mEadH6t). В пулдаун конфигурацията, стандартният вход към A1 се пулдаунва до 0V. След това, когато бутонът бъде натиснат, входът A1 преминава на 3,3V. Така че, ние включваме NeoPixels, когато A1 преминава на 3,3V (т.е. когато бутонът бъде натиснат).

- [Пример за MakeCode за Pull-up резистор](https://makecode.com/_FD0KHFLfDau7). В конфигурацията с pull-up, входът по подразбиране към A1 се изтегля нагоре до 3,3V. След това, когато бутонът бъде натиснат, входът A1 преминава на 0V. Така че, ние включваме NeoPixels, когато A1 преминава на 0V (т.е. когато бутонът бъде натиснат).

## Урок 8.3: Използване на вътрешни pull-up и pull-down резистори

В това видео представяме външни pull-up резистори и след това използваме вътрешни pull-up и pull-down резистори на CPX с MakeCode.

<div class="iframe-container">
<iframe width="100%" src="https://www.youtube.com/embed/JT4sQ72HJAM?si=ib8fGLSrsdvz5T-u" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>
</div>

### Схеми на вериги

![](assets/images/CPX_InternalPullUpResistorConfiguration.png)

![](assets/images/CPX_InternalPullDownResistorConfiguration.png)

## Урок 8.4: Свързване на аркадни бутони към CPX

В това видео показваме как да свържете аркадни бутони към CPX, които имат вградени LED диоди, които можем да включваме и изключваме. Ще покажем как да свържете аркадния бутон без и с вградения LED диод и по този начин ще научим малко за цифровото записване.

<div class="iframe-container">
<iframe width="100%" src="https://www.youtube.com/embed/nExLP211ZUA?si=5_z8wM0QDisPTTo8" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>
</div>

### Схеми

Използване на външен пулдаун резистор с аркадния бутон.

![](assets/images/CPX_ArcadeButtonExternalPullDown.png)

Използване на вътрешен пулдаун резистор с аркадния бутон (но без да се свързва вътрешният LED).

![](assets/images/CPX_ArcadeButtonInternalPullDown.png)

Свързване на вътрешен светодиод. Ето [пример за код](https://makecode.com/_0oVYVmYK5gYt), който включва вътрешния светодиод, когато бутонът е натиснат.

![](assets/images/CPX_ArcadeButtonInternalPullDown_WithInternalLED.png)

<!-- TODO: добавете схеми на вериги и линкове към код 
Публикувайте код за дебаунсинг
-->

### Код

- [Пример за код за аркаден бутон](https://makecode.com/_0oVYVmYK5gYt). Пример за код за аркаден бутон за вътрешна конфигурация на резистор, който включва NeoPixels при натискане на бутона и вътрешния LED на самия бутон (използвайки цифрово записване)

## Разширен код

* [Дебаунсинг на бутони в MakeCode](https://makecode.com/_ie5VHcgsXfEu). Забележка: Не съм открил нужда от дебаунсинг на бутони с MakeCode и CPX, но ако получавате неочаквани многократни натискания на бутон при използването му, опитайте това. За повече информация относно дебаунсинга, вижте нашия [Урок за дебаунсинг](../arduino/debouncing.md).

## Ресурси
Ето някои допълнителни ресурси:

* [MakeCode Pins](https://makecode.adafruit.com/reference/pins)
* [MakeCode's Digital Read Function](https://makecode.adafruit.com/reference/pins/digital-read)
* [Състояния на входа на MakeCode](https://makecode.adafruit.com/learnsystem/pins-tutorial/digital-input/input-states)
* [Adafruit MakeCode Learning: Digital Input](https://makecode.adafruit.com/learnsystem/digital-input)
* [Използване на цифров вход на CPX с Arduino C/C++](https://learn.adafruit.com/circuit-playground-digital-input/overview)


## Предишна лекция

<span class="fs-6">
[Предишна: Аналогов вход](analog-input.md){: .btn .btn-outline }
</span>
