---
lang: bg
permalink: /cpx/cpx-keyboard.html
page_id: cpx-cpx-keyboard
layout: default
title: L6&#58; CPX като клавиатура
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

В урок 6 от нашата серия CPX ще научим как да използваме CPX като програмируема клавиатура. Ще започнем с превръщането на бутоните A и B в клавиши на клавиатурата, а след това ще създадем все по-забавни и интересни клавиатури, включително клавиатура за управление на мултимедия (урок 6.2) и клавиатура на базата на акселерометър (урок 6.3).

{: .note }
Забележка: има известно припокриване на съдържанието с [Урок 5.3: Изработване на капацитивна клавиатура](capacitive-touch.md#lesson-53-making-a-capacitive-touch-keyboard), но искахме да започнем отначало и да продължим напред! Така че, би трябвало да можете да завършите тези уроци, дори ако не сте завършили Урок 5.3.

## Урок 6.1: Изработване на програмируема клавиатура

В този урок ще покажем как да използвате CPX като програмируема клавиатура

<div class="iframe-container">
<iframe width="100%" src="https://www.youtube.com/embed/2ehFfhHLcNQ" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>
</div>

### Урок 6.1 Код

Ето линк към MakeCode, който написахме в този урок:

- [Бутон А като пространство](https://makecode.com/_R01JeR0doWvL)
- [Лява/дясна стрелка + пространство](https://makecode.com/_UkEUewXxhH07)
- [Натискане и отпускане на клавиши](https://makecode.com/_02tfJu5xp785)

## Урок 6.2: CPX като контролер на медиен плейър

В този урок ще покажем как да използвате функционалността на медийните клавиши, за да контролирате Spotify и YouTube.

<div class="iframe-container">
<iframe width="100%" src="https://www.youtube.com/embed/0Uwvc497r2w" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>
</div>

### Урок 6.2 Код

Ето [MakeCode](https://makecode.com/_Ks7Ftj2jqHHW), който създадохме по време на този урок и който показва как да използвате натискането на мултимедийни клавиши за управление на Spotify и YouTube.

## Урок 6.3: Клавиатура с акселерометър

В този урок показваме как да преобразувате сигнала от акселерометъра в натискания на клавиши.

<div class="iframe-container">
<iframe width="100%" src="https://www.youtube.com/embed/6-ymgPJYrFw" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>
</div>

### Урок 6.3 Код

- [Основна програма за накланяне](https://makecode.com/_WJHbKkdeqEcx)
- [Тестер за накланяне в реално време](https://makecode.com/_VCPKbR341UyA)
- [Клавиатура с наклон](https://makecode.com/_M3m2PA76F6TL)
- [Подобрена клавиатура за накланяне](https://makecode.com/_atTA20HkMV3j)

Както обещахме, ето един различен подход ([линк към код](https://makecode.com/_e5kEupV4594H)) към клавиатурата за накланяне в реално време, която създадохме по-рано, но е различен от решението, което измислихме по време на видеото.

<!-- Идеи:
- Започнете с нещо много просто. Натиснете бутон "A", за да изпратите "Обичам да създавам!" или "Обичам да правя прототипи!".

- Обикновен контролер за игри. Изпратете "пробел". По-добре е да използвате тип тук.
- https://freeflappybird.org/

- След това създайте прост контролер и играйте игра, като изпращате команди за ляво и дясно на клавиатурата и пространствена клавиша?
- https://freegalaga.com/ <- използва лява, дясна пространствена клавиша
- https://www.retrogames.cc/arcade-games/galaga-namco.html
- https://tetris.com/play-tetris

- Пример за код: https://makecode.com/_UkEUewXxhH07

- Но след това подобрете, за да показвате натискане и отпускане на клавиша, така че да е по-непрекъснато
- https://freepong.org/
- https://www.retrogames.cc/arcade-games/galaga-namco.html
- Пример за код: https://makecode.com/_02tfJu5xp785

- Покажете команди за медии в Spotify: следваща песен, предишна песен, пространство за възпроизвеждане/пауза
- Разклатете, за да преминете към следващата песен
- https://open.spotify.com/playlist/5qTSCxoWreaB9ZTX5LFXSB#login

Сензори и команди от клавиатурата
- След това покажете как можем да използваме акселерометъра, за да играем тази игра
- Наклонете наляво, наклонете надясно, пространствена клавиша
- https://freegalaga.com/
- https://www.retrogames.cc/arcade-games/galaga-namco.html
- Пример за код: https://makecode.com/_PCHaak0Ki2cf
- По-сложно: https://makecode.com/_e5kEupV4594H

- След това покажете как да използвате сензор, за да изпращате команди като "силна звучност” за аплодисменти
- Може би покажете отново този праг
- Clappy Bird
- Хм, когато се опитам да използвам силата на звука, получавам CPX грешка :( -->

## Примери за проекти

Всички примери за проекти по-долу предоставят уроци с примерни MakeCode кодове.

- [Mouse Painter](https://learn.adafruit.com/mouse-painter-emulate-mice-with-makecode/overview), Джон Парк
- [Make it a Mouse](https://learn.adafruit.com/make-it-a-mouse), Anne Barela

## Следващ урок

В [следващия урок](cpx-mouse.md) ще разширим работата си, за да създадем персонализирана интерактивна мишка.

<span class="fs-6">
[Предишен: Капацитивно сензиране](capacitive-touch.md){: .btn .btn-outline }
[Следващ: CPX като мишка](cpx-mouse.md){: .btn .btn-outline }
</span>
