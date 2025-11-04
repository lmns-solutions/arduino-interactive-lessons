---
lang: bg
permalink: /advancedio/accel.html
page_id: advancedio-accel
layout: default
title: L2&#58; Акселерометри
nav_order: 2
# родител: Вход
# прародител: Разширени входно-изходни устройства
has_toc: true # (по подразбиране)
коментари: true
usemathjax: true
usetocbot: true
nav_exclude: true
---
# {{ page.title | replace_first:"L",'Урок '}}
{: .no_toc }

## Съдържание
{: .no_toc .text-delta }

1. Съдържание
{:toc}
---

## Общ преглед

- Прегледайте ускорителите и как работят. Видео за MEMs?
- Страхотно видео от engineerguy (кой друг!): https://youtu.be/KZVgKu6v808?t=52
- Обсъждане на ADXL335 (или ADXL345?) спрямо LIS3DH. Може би да се покажат примери за демоверсии и на двете?

- Таблица за нивелиране за калибриране:
- http://www.gcdataconcepts.com/calibration.html

### Възможни дейности

- Да се постави платка в режим на дълбок сън и да се събуди при засичане на движение.

## Ресурси

- [Adafruit LIS3DH Triple-Axis Accelerometer Breakout](https://learn.adafruit.com/adafruit-lis3dh-triple-axis-accelerometer-breakout), Adafruit Tutorial

- [LIS3DH избор на седмицата на Джон Едгар Парк](https://youtu.be/l1T3C-AZV0E), YouTube канал на Adafruit

- [LIS3DH технически данни](https://www.st.com/resource/en/datasheet/cd00274221.pdf), STMicroelectronics

### Как работят акселерометрите

- [Как работи акселерометърът](https://youtu.be/i2U49usFo10), Afrotechmods в YouTube

- [Акселерометри: Как смартфонът различава горе от долу](https://youtu.be/KZVgKu6v808), Engineer Guy в YouTube


## Интересни връзки:

<!-- - Полезна реализация на vector2D, създадена за Arduino: https://github.com/yazug/Arduino/blob/master/libraries/AP_Math/vector2.h 

- Ха, страхотно, някой е опитал да имплементира класа PVector на Shiffman в Arduino: https://github.com/stuthedew/AVector. Не изглежда много функционален. И мисля, че е трябвало да се използват шаблони
-->
