---
lang: bg
permalink: /cpx/button-piano.html
page_id: cpx-button-piano
layout: default
title: L3&#58; Button Piano
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

В този урок ще създадем първата си интерактивна CPX програма в MakeCode – просто пиано с бутони, което издава звуци, когато натискаме вградените бутони на CPX.

<!-- Бележки за урока:
* Въвеждане на понятието "бутон"
* Показване как MakeCode поддържа четири различни събития на бутоните: кликване, натискане, отпускане и др.
* Ако имате блок, който няма изрезка в горната част, това означава, че ще изпълни събитие, когато -->
<!-- Референция: https://youtu.be/NIKu0-Tgh2M (Урок по MakeCode) -->

## Видео урок

<div class="iframe-container">
<iframe width="100%" src="https://www.youtube.com/embed/wCSWP6PhNvY" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>
</div>

**Видео.** Създаване на пиано с бутони. Ето [пълният код](https://makecode.com/_EyqF3g3xb6Cy) и [линк към видеото в YouTube](https://youtu.be/wCSWP6PhNvY).
{: .fs-1 }

## Код

Ето окончателният [код](https://makecode.com/_EyqF3g3xb6Cy). Кликнете с десния бутон върху кода по-долу и изберете "Отвори линка в нов раздел", за да го отворите директно в редактора MakeCode.

<div style="position:relative;height:calc(300px + 5em);width:100%;overflow:hidden;"><iframe style="position:absolute;top:0;left:0;width:100%;height:100%;" src="https://makecode.adafruit.com/---codeembed#pub:_EsoWP4RwKXJK" allowfullscreen="allowfullscreen" frameborder="0" sandbox="allow-scripts allow-same-origin"></iframe></div>

## Блокове

В този пример използваме следните MakeCode блокове. Вижте ръководството [Adafruit MakeCode Reference](https://makecode.adafruit.com/reference).

### Изход

За изхода използвахме блокове **[Light](https://makecode.adafruit.com/reference/light)** и **[Music](https://makecode.adafruit.com/reference/music)**, по-специално:

- **[play tone](https://makecode.adafruit.com/reference/music/play-tone)** възпроизвежда тон на високоговорителя за определено време (задайте дължината на ритъма с [tempo](https://makecode.adafruit.com/reference/music/tempo))
- **[set all pixel color](https://makecode.adafruit.com/reference/light/set-all)** задава един цвят за всички NeoPixels
- **[set volume](https://makecode.adafruit.com/reference/music/set-volume)** задава силата на звука на изходния високоговорител

### Вход

За **[входни блокове](https://makecode.adafruit.com/reference/input)** използвахме:

- **[при натискане на бутона](https://makecode.adafruit.com/reference/input/button/on-event)** изпълнява сегмент от кода, когато бутонът бъде натиснат (или натиснат, отпуснат, *и т.н.*)

### Събитие

За да се уверим, че силата на звука е настроена правилно, я инициализираме на 255 (най-високата стойност), когато програмата стартира за първи път, използвайки блока [on start](https://makecode.adafruit.com/blocks/on-start)

- **[on start](https://makecode.adafruit.com/blocks/on-start)** се изпълнява веднъж и само веднъж, когато програмата стартира

## Следващ урок

В [следващия урок](sensor-instrument.md) ще създадем инструмент, реагиращ на светлина!

<span class="fs-6">
[Предишен: Как да използвате MakeCode](makecode.md){: .btn .btn-outline }
[Следващ: Инструмент, реагиращ на светлина](sensor-instrument.md){: .btn .btn-outline }
</span>
