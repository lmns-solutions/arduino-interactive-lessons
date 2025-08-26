---
layout: default
title: Advanced I/O
nav_order: 3
has_toc: false # on by default
has_children: true
comments: true
usetocbot: true
lang: bg
---
# {{ page.title }}
{: .no_toc } ## Съдържание {: .no_toc .text-delta } 1. Съдържание {:toc} --- Добре дошли 👋 в третия модул от вашето приключение с физически изчисления: **Разширен вход/изход**. Не се плашете от префикса **разширен**. Съдържанието тук не е по-сложно от първите два модула, въпреки че надгражда върху тях: 1. [Въведение в електрониката](../electronics/index.md) 2. [Въведение в микроконтролерите, използващи Arduino](../arduino/index.md) Както обикновено, тези уроци са интерактивни – тоест, те предполагат, че следвате и изграждате **с нас**. Те са проектирани да бъдат завършвани **по ред**. Целият код за Arduino е с отворен код и се намира в това [GitHub хранилище](https://github.com/makeabilitylab/arduino). ## Изход ### [L1: OLED дисплеи](oled.md) В [този урок](oled.md) ще научите за органични светодиодни (OLED) дисплеи, основно графично програмиране и кратко въведение в два протокола за серийна комуникация, наречени [I <sup>2</sup> C](https://en.wikipedia.org/wiki/I%C2%B2C) (Inter-Integrated Circuit) и [SPI](https://en.wikipedia.org/wiki/Serial_Peripheral_Interface) (Serial Peripheral Interface). ### [L2: Вибромотори](vibromotor.md) В [този урок](vibromotor.md) ще научите за вибрационните двигатели (вибромотори), тяхната роля в хаптичната технология и как да ги свържете с микроконтролери. ## Вход ### [L1: Изглаждане на входни данни](smoothing-input.md) В [този урок](smoothing-input.md) ще научим как да изглаждаме входящите данни от сензори, използвайки основна цифрова обработка на сигнали. Ще разгледаме клас цифрови филтри, наречени алгоритми за изглаждане (известни още като **сигнални филтри**), защо са полезни и потенциалните компромиси при тяхното внедряване и употреба. <!-- ## Output:
### L1: Vibro motors
### L3: OLED Displays
### L3: Servo motors
### L4: RGB LED Neopixels and beyond

## Input
### L1: Smoothing Input
### L2: Microphones
### L4: accelerometer?
### Joystick?
### L3: Hall effect sensors
### L4: Ultrasonic distance sensor
### L5: Interrupts --><!-- ## Computer Communication
L1: Using Arduino as a keyboard or mouse 
L2: Using Serial and parsing with Processing or Python
L3: Web Serial
L4: Node.js -->
