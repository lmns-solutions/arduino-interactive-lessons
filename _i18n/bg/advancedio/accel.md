---
layout: default
title: L2&#58; Accelerometers
nav_order: 2
# parent: Input
# grand_parent: Advanced I/O
has_toc: true # (on by default)
comments: true
usemathjax: true
usetocbot: true
nav_exclude: true
lang: bg
---
# {{ page.title | replace_first:'L','Lesson '}}
{: .no_toc } ## Съдържание {: .no_toc .text-delta } 1. Съдържание {:toc} --- ## План - Преглед на ускоренията и как работят. Видео за MEMS? - Страхотно видео от engineerguy (кой друг!): https://youtu.be/KZVgKu6v808?t=52 - Да поговорим за ADXL335 (или ADXL345?) спрямо LIS3DH. Може би да покажем примерни демонстрации и на двете? - Таблица за нивелиране за калибриране: - http://www.gcdataconcepts.com/calibration.html ### Възможности за активност - Платката да премине в дълбок сън и да се събуди, когато се засече движение. ## Ресурси - [Разклонение за триосен акселерометър Adafruit LIS3DH](https://learn.adafruit.com/adafruit-lis3dh-triple-axis-accelerometer-breakout), Урок за Adafruit - [Избор на седмицата за LIS3DH на Джон Едгар Парк](https://youtu.be/l1T3C-AZV0E), YouTube канал на Adafruit - [Технически данни за LIS3DH](https://www.st.com/resource/en/datasheet/cd00274221.pdf), STMicroelectronics ### Как работят акселерометрите - [Как работи акселерометърът](https://youtu.be/i2U49usFo10), Afrotechmods в YouTube - [Акселерометри: Как смартфонът различава нагоре от надолу](https://youtu.be/KZVgKu6v808), Engineer Guy в YouTube ## Интересни връзки: <!-- - Helpful vector2D implementation built for arduino: https://github.com/yazug/Arduino/blob/master/libraries/AP_Math/vector2.h 

- Ha, oh amazing, someone tried to implement the PVector class by Shiffman in Arduino: https://github.com/stuthedew/AVector. Does not look very feature complete. And should have used templates I think
-->