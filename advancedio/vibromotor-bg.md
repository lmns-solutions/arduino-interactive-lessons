---
lang: bg
permalink: /advancedio/vibromotor.html
page_id: advancedio-vibromotor
layout: default
title: L2&#58; Вибромотори
nav_order: 2
parent: Изход
grand_parent: Разширени входно-изходни устройства
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

Технологията на тактилните или тактилни актуатори предоставя обратна връзка на потребителя **чрез допир** чрез сила, движение или температура. В този урок ще научим за вибрационните мотори, които се използват често за предоставяне на тактилна обратна връзка в игрови контролери, мобилни телефони и смарт часовници.

![](assets/images/VibrationMotorExamplesInMobilePhonesAndWatches.png)
**Фигура.** Примери за *ексцентрични ротационни маси (ERM)* и *линейни резонансни актуатори (LRA)* в мобилни телефони и часовници. Изображения от [NFP Motors](https://youtu.be/k1iTLqAtd0U) и [Sosav](https://www.sosav.com/guides/mobiles/samsung/galaxy-s10/vibrator/)
{: .fs-1 }

## Вибромотори

<!-- https://www.fictiv.com/articles/intro-to-haptic-technology-vibration-motors -->

Има два обичайни типа вибрационни мотори: **ексцентрични ротационни мотори (ERM)**, които имат малка небалансирана маса, прикрепена към оста на DC мотора, която създава сила на изместване при въртене, и **линейни резонансни актуатори (LRA)**, които съдържат малка вътрешна маса, прикрепена към пружина, която вибрира в реципрочно линейно движение с приложен AC сигнал. ERM вибрират по две оси, докато LRA са едноосни вибратори. В този урок ще използваме ERM мотори. Видео откъсът по-долу от [Precision Microdrives](https://vimeo.com/132533086) показва как вибрират ERM и LRA.

<video autoplay loop muted playsinline style="margin:0px">
<source src="assets/videos/PrecisionMicrodrives_ERMvsLRAMotors_Optimized.mp4" type="video/mp4" />
</video>
**Видео.** [Видео](https://vimeo.com/132533086) от Precision Microdrives, показващо двата най-разпространени типа вибрационни мотори: мотори с ексцентрична въртяща се маса (ERM) и линейни резонансни актуатори (LRA). ERM моторите вибрират в две посоки поради центростремителната сила на небалансираната маса, прикрепена към оста на DC мотора. LRA са с дизайн, подобен на този на високоговорителите: 
{: .fs-1 }

**ERM** са конструирани с DC мотори и нецентрирана маса: те са евтини, осигуряват силна вибрация и са широко разпространени в играчки, контролери за игри, мобилни телефони и часовници; обаче, те имат сравнително дълго време за стартиране (~20-30 ms) и ограничена контролируемост. При ERM не можете да контролирате индивидуално честотата на вибрацията (*т.е.* колко бързо се върти масата) и амплитудата на тази вибрация – те са свързани помежду си. С увеличаването на приложеното DC напрежение честотата и амплитудата на вибрацията линейно се увеличават, което се възприема като обща интензивност на вибрацията. 

За разлика от ERM, **LRA** не се въртят. Те линейно движат маса (нагоре и надолу), прикрепена към пружина, използвайки [магнитна гласова бобина](https://en.wikipedia.org/wiki/Voice_coil). LRA изискват гладък синусоидален сигнал на напрежение (известен още като AC сигнал), задвижван при специфични резонансни честоти – обикновено 150-200Hz — който контролира честотата на движение на масата и, следователно, колебанието на вибрацията. Те стават все по-често срещани в смартфони, часовници и тракпад, за да имитират усещането от кликване. Например, по-новите Apple MacBook и iPhone разполагат с [Apple Taptic Engine](https://www.ifixit.com/News/16768/ apple-taptic-engine-haptic-feedback), който използва LRA технология. Макар LRA да са по-отзивчиви от ERM (~15-25 ms време за стартиране) , тяхната сила на вибрация е по-малка, а схемата на свързване е по-сложна. Освен това, тяхната честота на вибрация е най-силна при една единствена честота (резонансната честота).

Ако вибромоторът е напълно затворен в корпус, не можете да разберете дали е ERM или LRA, въпреки че технологиите са фундаментално различни. По-долу показваме формите "монета" (или "палачинка") на ERM и LRA.

! [](assets/images/PrecisionMicrodrives_ERMsAndLRAsCanLookSimilarBasedOnCase.png)
**Фигура.** В зависимост от корпуса и формата си, някои ERM и LRA могат да изглеждат подобни, въпреки че са фундаментално различни технологии. Те изискват различни драйверни вериги и методи на задействане (DC за ERM и AC за LRA). Изображения от [Precision Microdrives](https://www.precisionmicrodrives.com/).
{: .fs-1 }

<!-- Добър източник за сравнение между ERM и LRA: https://www.precisionmicrodrives.com/content/ab-028-vibration-motor-comparison-guide/ -->

### Ексцентрични ротационни маси (ERM)

Ексцентричните ротационни маси (ERM) имат небалансирана маса, прикрепена към оста им. Когато ERM моторът се върти, центростремителната сила на въртящата се маса причинява изместване. Чрез прикрепване на ERM към обект – като смартфон или гейм контролер – въртящата се неравномерна маса причинява разклащане на мотора и прикрепеното устройство. Колкото по-голям е обектът, толкова повече сила е необходима, за да се модулира вибрацията върху обекта.
 

<video autoplay loop muted playsinline style="margin:0px">
<source src="assets/videos/PrecisionMicrodrives_HowDoVibrationMotorsWork_ERM-OverviewOptimized.mp4" type="video/mp4" />
</video>
**Видео.** [Видео](https://vimeo.com/128603396) от [Precision Microdrives](https://www.precisionmicrodrives.com/vibration-motors/), което демонстрира как работят двигателите с ексцентрична въртяща се маса (ERM). Идеята е доста проста: прикрепете асиметрична или небалансирана маса към оста на DC мотора. Когато се върти, тежестта се измества, причинявайки вибрация.
{: .fs-1 }

#### Честота и амплитуда на вибрацията

Вибрацията има две основни характеристики: **честотата** на вибрацията, която е скоростта, с която се върти масата, и **амплитудата** на вибрацията, която е силата на вибрационната сила. При ERM двигателите *не можете* да променяте честотата и амплитудата на вибрациите независимо една от друга – и двете се увеличават линейно с приложеното напрежение.

DC моторите се въртят със скорост, пропорционална на приложеното напрежение. Измерваме "скоростта на въртене" в обороти в минута (RPM), но измерваме честотата на вибрациите в Hz (цикли в секунда). За да преобразуваме RPM в честота на вибрациите $$V_F$$ в Hz, просто разделяме на 60:
 

$$
V_F = \frac{RPM}{60}
$$

Силата на силата, генерирана от ERM мотора, е:

$$
F = m \cdot r \cdot ω^2
$$

Където $$F$$ е центростремителната сила в нютони (N), $$m$$ е масата на ексцентричната маса (в кг), $$r$$ е радиусът на ексцентричната маса (в метри), а $$ω$$ е ъгловата скорост в радиани/секунда (*т.е.* скоростта на мотора).

![](assets/images/ERMForceEquation.png)
**Фигура.** Силата на силата, генерирана от ERM мотора, е: $$F = m \cdot r \cdot ω^2$$ където $$F$$ е центростремителната сила в нютони (N), $$m$$ е масата на ексцентричната маса (в кг), $$r$$ е радиусът на ексцентричната маса (в метри) и $$ω$$ е ъгловата скорост в радиани/секунда. Изображение въз основа на [видео] (https://vimeo.com/128603396) от Precision Microdrives.
{: .fs-1 }

Когато е прикрепен към обект, амплитудата на вибрациите се влияе и от размера на този обект. Това би трябвало да е интуитивно ясно. Например, малкият ERM мотор в мобилния ви телефон (използван за сигнали и известия) няма да предизвика голямо изместване, когато е прикрепен към по-голям обект като лаптоп или офис бюро. Ако знаете размера на целевия обект, можете да използвате тази информация, за да определите размера и работните характеристики на вашия ERM мотор.

<video autoplay loop muted playsinline style="margin:0px" >
<source src="assets/videos/PrecisionMicrodrives_HowDoVibrationMotorsWork_ERM-VibrationAmplitudeOptimized.mp4" type="video/mp4" />
</video>
**Видео.** Амплитудата на вибрациите на ERM не е само функция на скоростта на двигателя и размера на ексцентричната маса, но и на размера на прикачения обект. По-голям обект изисква повече сила, за да вибрира. Забележете как изместването на вибрациите е по-голямо при по-малката прикачена маса в сравнение с по-голямата прикачена маса. Видео от [Precision Microdrives](https://www.precisionmicrodrives.com/vibration-motors/).
{: .fs-1 }

<!-- TODO: в бъдеще да се обсъдят други характеристики като време за стартиране, време за спиране и др. -->

#### Форма на ERM

Има различни форми на ERM – вижте фигурата по-долу – от основния цилиндричен "пейджър" мотор, който може да се монтира директно на PCB, до напълно капсулирани водоустойчиви версии, до популярните форми на монети или "палачинки". ERM с форма на монети са компактни, лесни за употреба и са снабдени със силно лепило за монтаж. Не се обърквайте: много LRA също се предлагат във форма на монета, но са с фундаментално различна технология.

![](assets/images/PrecisionMicrodrives_ERMMotorTypes.png)
**Фигура.** Примери за ERM мотори, включително цилиндрични (или пейджър) ERM и монети или палачинки ERM. Изображения от [Precision Microdrives](https://www.precisionmicrodrives.com/vibration-motors/vibration-motors-erms-and-lras/).
{: .fs-1 }

#### Примери за ERM двигатели

По-долу сме подчертали примери за ERM двигатели от популярен доставчик: [Precision Microdrives](https://www.precisionmicrodrives.com/). За всеки ERM мотор сме включили диаметъра и дължината на корпуса, радиуса и дължината на ексцентричната маса, работното напрежение и ток, както и скоростта на мотора и честотата на вибрациите при това напрежение/ток. Специално сме подбрали малки ERM мотори, които са често срещани в преносимите устройства, но те могат да бъдат и много по-големи.

Тъй като амплитудата на вибрациите зависи не само от скоростта на ERM мотора и размера на ексцентричната му маса, но и от размера на прикрепения целеви обект (*например* смартфон или часовник), в техническите спецификации на вибромоторите често се посочва "нормализирана амплитуда на вибрациите", която представлява производителността на ERM мотора при номиналното му напрежение, когато е прикрепен към фиксирана маса. В техническите спецификации на Precision Microdrive, например, се използва фиксирана маса от 100 g за изчисляване на нормализираната амплитуда на вибрациите за моторите.

| Модел | Диаметър на корпуса | Дължина на корпуса | Радиус на ексцентричното тегло | Дължина на ексцентричното тегло | Работно напрежение | Работен ток | Скорост на мотора | Честота на вибрациите | Нормализирана амплитуда |
|---|---|---|---|---|---|---|---|---|
| [![](assets/images/PrecisionMicrodrive_4x7mmERM_304-015.png)](https://www.precisionmicrodrives.com/product/ 304-015-4mm-vibration-motor-7mm-type) | 4,1 mm | 6,8 mm | 1,4 mm | 3 mm | 2,5 V | 25 mA | 11 000 об./мин | 183 Hz | 0,25 G |
| [![](assets/images/PrecisionMicrodrive_5mmVibrationMotor_304-005.002.png)](https://www.precisionmicrodrives.com/product/304-005 -002-5mm-vibration-motor-11mm-type) | 4,5 mm | 11 mm | 2 mm | 3 mm | 1,5 V | 17 mA | 9100 об./мин | 152 Hz | 0,4 G |
| [![](assets/images/PrecisionMicrodrive_8mmx3mm_308-100.png)](https://www.precisionmicrodrives.com/product/308-100-8mm-vibration-motor-3mm-type) | 8 mm | 3,4 mm | -- | -- | 3 V | 66 mA | 12 500 об./мин | 208 Hz | 1,13 G |
| [![](assets/images/PrecisionMicrodrive_10mmx2mm_310-118.001.png)](https://www.precisionmicrodrives.com/product/310-118-001-10mm-vibration-motor-2mm-type) | 10 mm | 2,1 mm | -- | -- | 3V | 60mA | 14 000 об./мин | 233 Hz | 1,1G |
| [![](assets/images/PrecisionMicrodrive_7mmx25mm_306-10H.png)](https://www.precisionmicrodrives.com/product/306-10h-7mm-vibration-motor-25mm-type) | 7 mm | 24,5 mm | -- | -- | 3V | 50mA | 13 800 об./мин | 230 Hz | 1,84G |
| [![](assets/images/PrecisionMicrodrive_9mmx25mm_307-103.png)](https://www.precisionmicrodrives.com/product/307-103-9mm-vibration-motor-25mm-type) | 8,7 mm | 25,1 mm | -- | -- | 3V | 100mA | 13 800 об./мин | 230 Hz | 7G |
| [![](assets/images/PrecisionMicrodrive_24x13mm_324-401.png)](https://www.precisionmicrodrives.com/ product/324-401-24mm-vibration-motor-13mm-type) | 24,3 mm | 12,5 mm | 9 mm | 4,8 mm | 12 V | 148 mA | 5500 об./мин | 92 Hz | 13G |
{: .vibro-table }

<!-- | [![](assets/images/PrecisionMicrodrive_4x6mm_304-10K.png)](https://www.precisionmicrodrives.com/product/304-10k-4mm-vibration-motor-6mm-type) | 4,4 mm | 6 mm | 1,7 mm | 2,8 mm | 2,7 V | 65 mA | 13 500 об./мин | 0,5 G | -->
<!-- | [![](assets/images/PrecisionMicrodrive_20x25mm_320-105.png)](https://www.precisionmicrodrives.com/product/320-105-20mm-vibration-motor-25mm-type) | 20,4 mm | 25 mm | 9 mm | 5,9 mm | 3 V | 413 mA | 6100 об./мин | 15,9 G | -->

<!-- - https://e2e.ti.com/blogs_/b/analogwire/posts/how-to-improve-the-startup-and-stop-behavior-of-erm-and-lra-actuators
- https://www.vibrationmotors.com/vibration-motor-product-guide/coin-vibration-motor/
-https://www.precisionmicrodrives.com/vibration-motors/ -->

#### ERM мотори с вибрация на монети

В нашите [учебни хардуерни комплекти](../index.md/#example-hardware-kits) често предлагаме ERM мотори във формата на монети. Тези мотори се наричат още pancake ERM или вибриращи мини моторни дискове. Coin ERM са компактни, самостоятелни и осигуряват силна вибрация. Благодарение на малкия си размер, лекотата на употреба и напълно затворения вибрационен механизъм, те са често срещани в мобилни телефони, преносими устройства (*например* контролери) и медицински приложения.

| Adafruit "Вибриращ мини-мотор диск" | Digikey ERM вибрационен мотор |
|-----|----|
| ![](assets/images/Adafruit_VibratingMiniMotorDisc.png) | ![](assets/images/SeeedTechnology_ERMVibrationMotor.png) |
| [Продукт #1201](https://www.adafruit.com/product/1201) 1,95 $ | [Продукт #316040001](https://www.digikey.com/en/products/detail/seeed-technology-co., -ltd/316040001/5487672) $1,20 |

Моторите с вибрация на монети са ERM и като цяло имат същите експлоатационни и функционални характеристики като цилиндричните си аналози, но конструкцията им е различна. Вижте видеото по-долу. Можете да прочетете за конструкцията им на уебсайта [Precision Microdrives](https://www.precisionmicrodrives.com/vibration-motors/coin-vibration-motors/).

<video autoplay loop muted playsinline style="margin:0px">
<source src="assets/videos/CoinVibromotor_HowAMobilePhoneVibrationMotorLooksAndWorks_TrimmedOptimized.mp4" type="video/mp4" />
</video>
**Видео.** Демонстрация на отворен монетен ERM от [Tech Vision](https://youtu.be/iwEGqBpYaqc). Има и друго [страхотно видео](https://youtu.be/lp7bwXXsVl8?t=537), в което Марти Джопсън разглежда монетен ERM под микроскоп.
{: .fs-1 }

<!-- - https://www.precisionmicrodrives.com/vibration-motors/coin-vibration-motors/
- https://nfpmotor.com/products-coin-vibration-motors.html
- https://www.androidpolice.com/2020/10/20/a-lot-more-goes-into-good-smartphone-haptics-than-youd-think/ -->

<!-- ### LRAs

Някои полезни връзки:

- https://www.vibrationmotors.com/vibration-motor-product-guide/linear-resonant-actuator/
- https://www.precisionmicrodrives.com/vibration-motors/linear-resonant-actuators-lras/
- https://www.nfpmotor.com/products-linear-resonant-actuators-lras.html

LRA са в iPhone от iPhone7: https://www.boreas.ca/blogs/piezo-haptics/last-decade-haptics-in-mobile-erm-to-lra-and-the-taptic-engine 

LRA Motors

| Модел | Диаметър на корпуса | Дължина на корпуса | Напрежение (RMS) | Работен ток | Честота на вибрациите | Амплитуда |
| ---|---|---|---|---|---|---|
| [![](assets/images/PrecisionMicrodrive_8mmLRA_C08-00A.png)](https://www.precisionmicrodrives.com/product/c08-00a-8mm-linear-resonant-actuator-3mm-type) | 8 mm | 2,6 mm | 1,2 V | 28 mA | 240 Hz | 0,7 G |
| [![](assets/images/ PrecisionMicrodrive_10mmLRA_C10-100.png)](https://www.precisionmicrodrives.com/product/c10-100-10mm-linear-resonant-actuator-4mm-type) | 10 mm | 3,7 mm | 2 V | 69 mA | 175 Hz | 1,5 G |
| [![](assets/images/PrecisionMicrodrive_6x12mm_C12-003.001.png)](https://www.precisionmicrodrives.com/product/c12-003 -001-6mm-linear-resonant-actuator-12mm-type) | 6 mm | 12 mm | 2 V | 111 mA | 204 Hz | 1,5 G |
{: .vibro-table } -->

<!-- | [![](assets/images/PrecisionMicrodrive_8mmLRA_C08-00A.003.png)](https://www.precisionmicrodrives.com/product/c08-00a-003-8mm-linear-resonant-actuator-3mm-type) | 8 mm | 2,6 mm | 1,2 V | 28 mA | 240 Hz | 0,7 G | -->

<!-- Наистина страхотна демонстрация на LRA: https://youtu.be/Nz3Z2XQZpJs?t=198 -->

<!-- Невероятно видео на LRA на Samsung S10 LRA: https://youtu.be/gOBhQRVmLsA -->

## Свързване на ERM мотори с Arduino

Въпреки че много онлайн уроци и YouTube видеоклипове показват ERM мотори, директно свързани към Arduino GPIO пинове, като се използват кабели, подобни на тези, с които свързваме [LED диоди](../arduino/led-blink.md) — това е неправилно и може да повреди вашия микроконтролер. Защо?

Припомнете си, че Arduino GPIO пиновете могат да доставят [максимум 40mA](https://www.arduino.cc/en/reference/board) на пин с безопасен непрекъснат ток от 20mA. Това е достатъчно, за да включите LED с резистори за ограничаване на тока, но не е достатъчно за по-високи токови натоварвания. В таблицата [по-горе](#example-erm-motors) повечето ERM мотори имат работни токове от 50mA или повече. Освен това, като електромеханични устройства, ERM изискват по-висок стартиращ ток, за да започнат движението на мотора от покой (поради инерцията). [Монетата ERM, продавана](https://www.adafruit.com/product/1201) от Adafruit, има работен ток от 75 mA и стартиращ ток до 120 mA.

И така, какво да направим? Трябва да използваме **транзистор**.

![](assets/images/Arduino_ERMMotorWirings_ThreeOptions.png)
**Фигура.** Три примера за свързване на ERM мотори към вашия Arduino. Неправилното свързване вляво свързва ERM директно с GPIO Pin 3 (използвайки подобно свързване, както при [LED-ите](../arduino/led-blink.md)) . Това е погрешно и може да повреди вашия Arduino. GPIO пиновете могат да доставят само до 40mA ток, но ERM моторът изисква 75mA с ток при стартиране до 120mA. Другите две свързвания използват транзистори като превключватели, за да свържат ERM моторите към 3.3V захранващи пинове, които са способни да доставят 150mA. Можете да кликнете -кликнете върху тази картинка и изберете "Open Image in a New Tab" (Отвори картинката в нов прозорец), за да я уголемите. Вижте също "[How to Build a Vibration Motor Circuit](http://www.learningaboutelectronics.com/Articles/Vibration-motor-circuit.php)" (Как да изградите верига за вибрационен мотор) от Learning about Electronics.
{: .fs-1 }

---

**ВНИМАНИЕ:**

Двата проводника на Adafruit coin ERM са изключително крехки и могат лесно да се счупят или да се откъснат от спойките си. Бъдете внимателни!

---


<!-- TODO: в бъдеще включете фигура, показваща как с обърнати червени и сини проводници просто се обръща посоката на мотора -->

### Транзистори

<!-- Изобретяването на транзистора през 1947 г. бележи началото на [компютърната революция] (https://en.wikipedia.org/wiki/History_of_computing_hardware_(1960s%E2%80%93present)#Third_generation), позволявайки на електрическите вериги бързо да се изключват (`0`) и включват (`1`), за да създават [логически вентили](https://en.wikipedia.org/wiki/Logic_gate), [акумулатори](https://en.wikipedia.org/wiki/Accumulator_(computing)) и други изчислителни елементи. Преди транзисторите компютрите използваха [вакуумни тръби](https://en.wikipedia.org/wiki/Vacuum_tube_computer), които бяха по-бавни, по-малко устойчиви, много по-големи и изискваха значително повече енергия.

TODO: вмъкване на снимка на различни транзистори -->

[Транзисторите](https://en.wikipedia.org/wiki/Transistor) са полупроводникови устройства, използвани за **усилване** или **превключване** на електронни сигнали. Те са основните компоненти на компютрите и се използват в почти всички съвременни електронни устройства, от смартфони до усилватели за слушалки. Транзисторите се предлагат в различни форми, размери и работни спецификации. Има два обичайни дизайна: [**BJT** ](https://en.wikipedia.org/wiki/Bipolar_junction_transistor) (биполярни транзистори), които ще използваме в този урок, и [**MOSFETS**](https://en.wikipedia.org/wiki/MOSFET) (метало-оксидни полупроводникови транзистори с полеви ефект), които са по-подходящи за по-високи токови натоварвания.

Има два основни "форматни фактора" или пакета за транзистори: [TO-92](https://en.wikipedia.org/wiki/TO-92) пакети и [TO-220](https://en.wikipedia.org/wiki/TO-220) пакети; вторите са по-често срещани за по-високи токови натоварвания поради вградените радиатори. Можете да намерите както BJT, така и MOSFET транзистори в двата типа пакети и сме включили примери за всеки от тях по-долу.

![](assets/images/ExampleBJTAndMOSFETTransistorsInDifferentPackaging.png)
**Фигура.** Има два основни "форматни фактора" или опаковки за транзистори: [TO-92](https://en.wikipedia.org/wiki/TO-92) опаковки и [TO-220](https://en.wikipedia.org/wiki/TO-220) опаковки. Можете да намерите както BJT, така и MOSFET транзистори в двата типа опаковки. Показано по-горе: [2N3904](https://www.sparkfun.com/datasheets/Components/2N3904.pdf) NPN BJT и [2N7000](https://www.onsemi.com/products/discretes-drivers/mosfets/2n7000) N-канален MOSFET с TO-92 опаковка и [TIP120] (https://components101.com/transistors/tip120-pinout-datasheet-equivalent) NPN BJT и [IRLB8721](https://cdn-shop.adafruit.com/datasheets/irlb8721pbf.pdf) N-канален MOSFET с TO-220 опаковка. Изображения от Wikipedia и съответните технически спецификации.
{: .fs-1 }

<!-- Интересна дискусия за BJT срещу Mosfet: https://electronics.stackexchange.com/a/527268 -->

Транзисторите са сложна тема, която заслужава отделен урок; обаче за нашите цели тук са важни две характеристики:

- Първо, транзисторите могат да работят като **електронно контролирани превключватели**. Можете да контролирате транзисторите с *малки* количества ток (за да ги включвате и изключвате), но сигналът, който контролират, може да бъде много *по-голям*. По този начин транзисторите се използват често за контролиране на високи токови натоварвания с микроконтролери като [RGB LED ленти](https://learn.adafruit.com/rgb-led-strips/usage) и [мотори](https://itp.nyu.edu/physcomp/labs/motors-and-transistors/).

<!-- На Arduino, не забравяйте, че нашите GPIO пинове могат да доставят само 40mA непрекъснат ток (максимум!) ; обаче, [RGB LED ленти](https://learn.adafruit.com/rgb-led-strips/usage) могат лесно да изискват 1A или повече, а дори и малки [DC хоби мотори](https://www.adafruit.com/product/711) използват между 70-250mA. Малкият плосък вибромотор, използван в този урок, има номинален ток от 75mA и стартиращ ток до ~120mA – и двата над максималния безопасен ток на нашите GPIO пинове на микроконтролера. -->

- Второ, тъй като транзисторите могат да **се включват и изключват бързо**, те могат да използват импулсно-широчинна модулация. Това означава, че вашият микроконтролер може да подава PWM сигнал към контролния вход на транзистора, който ще модулира същия PWM сигнал, но усилван, на изхода на транзистора. По този начин можем да използваме PWM чрез нашия транзистор, за да контролираме силата на вибрациите на нашия вибромотор.

<!-- ### BJT транзистор

Покажи -->

### Свързване на Adafruit ERM мотор с 2N2222 транзистор

В [техническото описание](https://cdn-shop.adafruit.com/product-files/1201/P1012_datasheet.pdf) на [вибриращия мини-мотор диск Adafruit](https://www.adafruit.com/product/1201) са посочени следните работни спецификации.

| Атрибут | Номинална стойност |
|------- ----|--------|
| Номинално работно напрежение | 3,0 V |
| Диапазон на напрежението | ~2,5-3,8 V |
| Номинален работен ток | 75 mA |
| Номинална скорост | 11 000 ± 3000 об./мин. |
| Номинална честота на вибрациите | 183 ± 50 Hz |
| Стартово напрежение | 2,3 V |
| Стартови ток | До ~120 mA |

Не забравяйте, че вибромоторът ERM е вид DC мотор, макар и много малък. Необходимо е да се подаде стартиращо напрежение и ток, за да се инициира въртенето от покой; тези стойности са по-високи от общото работно напрежение и ток. Въпреки че работното обхват на Adafruit ERM е 2,5-3,8 V, документацията на Adafruit посочва, че 2-5 V също са подходящи. Действително, ние също установихме, че това е така, като 5 V водят до по-силни вибрации (както се очаква). Въпреки това, за надлъжно използване, захранването с 3,3 V е по-разумно, като се има предвид техническата спецификация.

![](assets/images/Arduino_WiringUpERMMotorWithTransistor.png)
** Фигура**. Два примера за свързване с NPN BJT транзистор. Вляво използваме 3,3 V захранващ пин, а вдясно – 5 V захранващ пин. Ако разполагате с компонентите, трябва да добавите и обратна диода и кондензатор, както показахме по-рано. За да увеличите изображението, кликнете с десния бутон върху него и изберете "Отвори изображението в нов прозорец".
{: .fs-1 }

<!-- Как да подобрите времето за стартиране и спиране на ERM и LRA актуатори: https://e2e.ti.com/blogs_/b/analogwire/posts/how-to-improve-the-startup-and-stop-behavior-of-erm-and-lra-actuators -->

<!-- ![](assets/images/VibromotorTransistorCircuit_AbstractPictorialDiagramPlusCircuitDiagram.png) -->

По-конкретно, NPN биполярните транзистори, които използваме в нашите курсове, са [PN2222A](https://www.adafruit.com/ product/756) (и варианти като [2N2222A](https://components101.com/transistors/2n2222a-pinout-equivalent-datasheet)). Необходим ви е резистор, свързан последователно с пина за управление (базов пин) на транзистора. В този случай резистор от 1kΩ работи добре. 

Уверете се, че транзисторът е ориентиран правилно. Създадохме абстрактната диаграма по-долу, за да ви помогнем при сглобяването. В тази диаграма текстът върху транзистора е обърнат към нас, а изпъкналата част е обърната в обратна посока.

![](assets/images/Arduino_VibromotorTransistorCircuit_AbstractPictorialDiagramPlusCircuitDiagram.png)
**Фигура**. Допълнителна диаграма, която ще ви помогне да свържете тази верига на базата на транзистор. Обърнете специално внимание на ориентацията на транзистора. Текстът върху транзистора е обърнат към нас, а изпъкналата част е обърната в обратна посока. Идеята за диаграмата е базирана на [Learning About Electronics](http://www.learningaboutelectronics.com/Articles/Vibration-motor-circuit.php).
{: .fs-1 }

<!-- 1023 | 255 | 0,012 A | 75,55
900 | ~225 | 0,011 A | 65 mA
800 | 199 | 0,009A | 58 mA
700 | 174 | 0,008A | 52 mA
600 | 149 | 0,007 A | 45 mA
400 | 99 | 0,005 A | 32 mA
300 | 75 | 0,004 A | 25 mA
200 | 50 | 0,002 A | 15 mA
160 | 40 | 0,002A | 12 mA (изключено)
100 | 25 | 0,001A | 6,1 mA -->

<!-- TODO: Заснемете видео на експерименталната постановка.

- http://www.learningaboutelectronics.com/Articles/Vibration-motor-circuit.php
-https://www.precisionmicrodrives.com/content/how-to-drive-a-vibration-motor-with-arduino-and-genuino/
-http://www.ermicro.com/blog/?p=423
- Усилване на транзистора: https: //www.electronics-notes.com/articles/electronic_components/transistor/current-gain-hfe-beta.php
- [Дискретни драйверни вериги за вибрационни мотори](https://www.precisionmicrodrives.com/content/ab-001-discrete-driver-circuits-for-vibration-motors/), Precision Microdrives
- [Електрически техники за задвижване на вибрационни двигатели](https://www.precisionmicrodrives.com/content/ab-011-electrical-techniques-for-using-different-power-sources/), Precision Microdrives -->

<!-- Разговор за използването на диоди и кондензатори:
https://www.reddit.com/r/arduino/comments/a06hxr/why_do_motors_need_transistors_and_diodes/ -->

<!-- ### Tinkercad версия

<iframe width="725" height="453" src="https://www.tinkercad.com/embed/dlqdbv0SFV4?editbtn=1" frameborder="0" marginwidth="0" marginheight="0" scrolling="no"></iframe>

Въпреки че е по-неподредена, ние също [направихме версия](https://www.tinkercad.com/things/jGRVrL9C8Jv) с амперметри, за да проследяваме (1) тока през вибромотора и в емитера на транзистора, (2) тока в базовия пин на транзистора (контролния пин) и (3) тока, излизащ от емитера.

![](assets/images/VibromotorTransistorPotCircuit_WithAmmeters_Tinkercad.png)
**Фигура.** Преработихме оригиналната верига на вибромотора Tinkercad, за да включим амперметри ([линк](https://www.tinkercad.com/things/jGRVrL9C8Jv)).
{: .fs-1 } -->

<!-- ## Генериране на тактилни модели

Задача: учениците да създадат един или два тактилни модела. Може би да се планира прекъсване на таймера, за да се направи това?

Има ли Arduino библиотеки за това? -->

## Хаптични моторни драйвери

Когато хаптиката играе ключова роля във вашия проект, обмислете използването на [хаптичен моторен драйвер](https://learn.sparkfun.com/tutorials/haptic-motor-driver-hook-up-guide?_ga=2.87552344.1190007566. 1620233503-935977820.1612992862), който улеснява взаимодействието с вибрационни мотори и задвижването на сложни хаптични модели.

Например, Texas Instruments (TI) продава разнообразие от [хаптични моторни драйвери](https://www.ti.com/motor-drivers/actuator-drivers/overview.html). Популярният [TI DRV2605](https://www.ti.com/lit/ds/symlink/drv2605.pdf) предоставя [I<sup>2</sup>C](https://en.wikipedia.org/wiki/I%C2% B2C) интерфейс за управление на ERM и LRA мотори, генерира свои собствени импулсно-широчинно модулирани (PWM) вълни, което освобождава хост микроконтролера от тази отговорност, спестява хардуерни пинове и намалява сложността на кода (*например* настройка на прецизни таймерни прекъсвания за генериране на вълни) и включва интегрирана библиотека от 123 лицензирани хаптични модела, което намалява необходимостта от проектиране и внедряване на софтуер за създаване на персонализирани хаптични ефекти.

![](assets/images/TI_DRV205L_123LicensedHapticEffects.png)
**Фигура.** [TI DRV2605L](https://www.ti.com/lit/ds/symlink/drv2605l.pdf) включва предварително програмирана библиотека с над 100 хаптични вълнови ефекта, включително единични, двойни и тройни кликвания, предупреждения и преходи. Тези хаптични модели са лицензирани от Immersion Corporation. Вижте страница 63 от техническото описание на [TI DRV2605L](https://www.ti.com/lit/ds/symlink/drv2605l.pdf). Кликнете с десния бутон върху изображението и изберете "Отвори изображението в нов раздел", за да го увеличите.
{: .fs-1 }

Както [Adafruit](https://www.adafruit.com/product/2305), така и [SparkFun](https://www.sparkfun.com/products/14538) предлагат персонализирани разклонителни платки за свързване с IC [TI DRV2605](https://www.ti.com/lit/ds/symlink/drv2605.pdf).

| SparkFun Haptic Breakout Board за TI DRV2605L | Adafruit Haptic Breakout Board за TI DRV2605L |
| ![](assets/images/SparkFunHapticMotorDriver_DRV2605L.png) | ![](assets/images/AdafruitHapticMotorDriver_DRV2605L.png) |
| 8,50 $ от [SparkFun](https://www.sparkfun.com/products/14538) | 7,95 $ от [Adafruit](https://www.adafruit.com/product/2305) |

Можете също да закупите разклонителни платки с интегриран вибрационен мотор и хаптичен драйвер, като тази [SparkFun DA7280 Haptic Driver](https://www.sparkfun.com/products/17590) с Qwiic [I<sup>2</sup>C](https://en.wikipedia.org/wiki/I%C2%B2C) конектори.

За повече информация относно използването на хаптични моторни драйвери с Arduino, вижте [Ръководство за свързване на хаптичен моторен драйвер на SparkFun](https://learn.sparkfun.com/tutorials/haptic-motor-driver-hook-up-guide).

## Дейности по прототипиране

За вашия дневник за прототипиране, моля, изпълнете **трите** ERM моторни дейности, които започнахме в лекцията (вижте [слайдовете тук](https://docs.google.com/presentation/d/ 1bV08Yjvlf1CtBgx1nD3IamVHx6wtGVE_HgxQQnEf7P4/edit?usp=sharing)). Заснемете видео на вашите конструкции и включете линк към видеото и кода в дневника си. Опишете накратко какво сте направили и какво сте научили.

<!-- TODO: в бъдеще прегледайте всеки от тези уроци (поне предоставете схеми на свързване и няколко основни примера за код) -->

## Ресурси

### Ресурси за вибромотори

- [Най-добри практики за вибромотори от мобилни телефони](https://www.precisionmicrodrives.com/content/ab-008-vibration-motor-best-practices-from-mobile-cell-phones/), Precision Microdrives

- [Сравнителен наръчник за вибрационни мотори](https://www.precisionmicrodrives.com/content/ab-028-vibration-motor-comparison-guide/), Precision Microdrives

- [Разбиране на характеристиките на вибрационните мотори ERM](https://www.precisionmicrodrives.com/content/ab-004-understanding-erm-vibration-motor-characteristics/), Precision Microdrives

- [Как да изградим верига за вибрационен мотор](http://www.learningaboutelectronics.com/Articles/Vibration-motor-circuit.php), Обучение по електроника

### Използване на транзистори с Arduino

- [Как да управлявате вибрационен мотор с Arduino](https://www.precisionmicrodrives.com/content/how-to-drive-a-vibration-motor-with-arduino-and-genuino/), Precision Microdrives

- [Управление на RGB LED ленти с транзистори](https://learn.adafruit.com/rgb-led-strips/usage), Adafruit

- [Транзистори 101](https://learn.adafruit.com/transistors-101/overview), Adafruit

- [Използване на транзистор за управление на високи токови натоварвания с Arduino](https://itp.nyu.edu/physcomp/labs/motors-and-transistors/using-a-transistor-to-control-high-current-loads-with-an-arduino/), NYU ITP Physical Computing Course

- [Мотори и транзистори](https://itp.nyu.edu/physcomp/labs/motors-and-transistors/), курс по физическо компютърно инженерство на NYU ITP

### Видеоклипове

- [BJT като транзисторни превключватели](https://youtu.be/sRVvUkK0U80), AddOhms в YouTube

- [Транзистор (BJT) като превключвател](https://youtu.be/WRm2oUw4owE), GreatScott! в YouTube

- [MOSFET и транзистори с Arduino](https://youtu.be/IG5vw6P9iY4), DroneBot Workshop в YouTube
