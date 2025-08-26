---
layout: default
title: Intro to Electronics
nav_order: 1
has_children: true
has_toc: false # on by default
nav_exclude: false
lang: bg
---
# Електроника {: .no_toc } ## Съдържание {: .no_toc .text-delta } 1. Съдържание {:toc} --- <video autoplay loop muted playsinline style="margin:0px"><source src="assets/videos/FSR-TopDown9VCircuit-IMG_5683_Trimmed-Optimized.mp4" type="video/mp4" /></video> **Видео.** Видео демонстрация на резистор, чувствителен към сила (известен още като „сензор за налягане“), който променя съпротивлението си пропорционално на приложената сила. Това е само едно от многото неща, за които ще научите и ще изградите в тази поредица от уроци „Въведение в електрониката“. Вижте повече в [L8: Променливи резистори](variable-resistors.md). {: .fs-1 } Добре дошли 👋 на първата „стъпка“ във вашето пътешествие във физическите изчисления! В тази поредица от уроци ще научите за основите на електричеството – [напрежение, ток и съпротивление](electricity-basics.md) – и как тези елементи могат да се използват за изграждане на вериги, които включват светлини, въртят двигатели и извършват друга „работа“. Ще научите и за емпирично изведена зависимост, наречена [Закон на Ом](ohms-law.md), която свързва напрежението, тока и съпротивлението, както и методи за анализ на вериги, използващи закона на Ом. Накрая ще научите за три често срещани елемента в електрическите вериги (резистори, светодиоди, променливи резистори), как работят и как да ги използвате в електрически вериги. По време на обучението ще използвате инструменти за симулация като [CircuitJS](https://www.falstad.com/circuit/circuitjs.html) и [Tinkercad Circuits](https://www.tinkercad.com/), за да проектирате и оценявате електрически вериги, а след това реално да ги изграждате с помощта на физически компоненти. До края на този модул ще бъдете готови да започнете [Модул 2](../arduino/index.md) - нашата [Въведение в Arduino серията](../arduino/index.md) - където ще започнете да създавате с електроника, микроконтролери и програмиране! {: .note } Ако имате ограничени познания в областта на електрическите схеми и програмирането, може да разгледате и нашата поредица за [Създаване с Circuit Playground Express (CPX)](../cpx/), която използва чудесна платформа за прототипиране, наречена [CPX](https://www.adafruit.com/product/3333), заедно с език за визуално програмиране с плъзгане и пускане, наречен [MakeCode](https://makecode.adafruit.com/) (подобен на [Scratch](https://scratch.mit.edu/)). ## [Урок 1: Напрежение, ток и съпротивление](electricity-basics.md) Въвежда три ключови понятия за електричество, [ток, напрежение и съпротивление](electricity-basics.md), които формират основата на електрониката и електрическите схеми. ## [Урок 2: Схеми на електрически вериги](schematics.md) Въвежда визуален език за описание на електрически вериги, наречен [схеми на електрически вериги](schematics.md), които се използват в информационни листове за компоненти, CAD програми (*напр.* симулатори на електрически вериги, софтуер за оформление на печатни платки) и анализи на електрически вериги. Включва също така упражнение с помощта на [Fritzing](https://fritzing.org/) за изграждане на ваши собствени схеми. ## [Урок 3: Закон на Ом](ohms-law.md) Въвежда [закона на Ом](ohms-law.md), един от най-важните емпирични закони в електрическите вериги, който описва как токът, напрежението и съпротивлението са свързани помежду си. Включва също упражнение за изграждане и изследване на резистивни вериги в [CircuitJS](https://www.falstad.com/circuit/circuitjs.html). ## [Урок 4: Серийни срещу паралелни резистори](series-parallel.md) Представя [серийни и паралелни резистори](series-parallel.md), как да ги анализираме и защо са важни. Включва и упражнение за изграждане и изследване на конфигурации на серийни и паралелни резистори в [CircuitJS](https://www.falstad.com/circuit/circuitjs.html). ## [Урок 5: Резистори](resistors.md) Надграждайки върху уроци 1 - 4, нека се потопим по-задълбочено в [резистори](resistors.md) и да научим как работят резисторите, как са направени, как се характеризират по отношение на съпротивление $$R$$ и мощност $$P$$ и как да ги &quot;четем&quot;. ## [Урок 6: Светодиоди](leds.md) В [този урок](leds.md) ще ви представим един от най-разпространените електрически компоненти в света: [светодиоди](leds.md) или [LED](leds.md). Ще научите за първото си полупроводниково устройство, диодите, и как те са неомични и позволяват на тока да преминава само в една посока. След това ще ви представим специален вид диод, наречен LED, и ще покажем как да го използвате, как да изберете подходящ резистор за ограничаване на тока и защо са необходими резистори. Ще можете също така физически да сглобявате неща, ура! ## [Урок 7: Макетни платки](breadboards.md) В [този урок](breadboards.md) ще научим за много полезен инструмент за прототипиране на схеми, наречен breadboards, който улеснява бързото изграждане на схеми (и включването/изключването на компоненти и проводници). ## [Урок 8: Променливи резистори](variable-resistors.md) В [този урок](variable-resistors.md) ще научим за променливите резистори, определен вид променлив резистор, наречен потенциометър, а след това ще проектираме, симулираме и изградим някои светодиодни схеми, използвайки променливи резистори. Накрая дори ще направите свой собствен променлив резистор „Направи си сам“! <!-- ## [Lesson 9: Using a multimeter](multimeter.md)

TODO: or could integrate this somewhere else?   --><!-- # TODO
- Should we add voltage regulator? https://youtu.be/howQ05z4v7Q?
- Switches?
- Capacitors?
- Transistors?
- Rotary Encoders
- Diode
- Voltage Regulator
- Power
  - Batteries? https://learning.oreilly.com/library/view/hacking-electronics-an/9780071802369/ch05.html#ch5
- [NYU ITP's Physical Computing list of common electronic components](https://itp.nyu.edu/physcomp/labs/labs-electronics/components/)

# Possible sections
- [What is Electricity?](https://learn.sparkfun.com/tutorials/what-is-electricity)
- [Voltage, Current, Resistance, and Ohm’s Law](http://learn.sparkfun.com/tutorials/voltage-current-resistance-and-ohms-law)
- [What is a circuit?](http://learn.sparkfun.com/tutorials/what-is-a-circuit)
- [Metric Prefixes](https://learn.sparkfun.com/tutorials/metric-prefixes-and-si-units)
- [How to Use a Breadboard](https://learn.sparkfun.com/tutorials/how-to-use-a-breadboard)
- [How to Use a Multimeter](https://learn.sparkfun.com/tutorials/how-to-use-a-multimeter)
- [Connector Basics](https://learn.sparkfun.com/tutorials/connector-basics)
- [Polarity](https://learn.sparkfun.com/tutorials/polarity)
- [Series and Parallel Circuits](https://learn.sparkfun.com/tutorials/series-and-parallel-circuits)
- [AC vs DC current](https://learn.sparkfun.com/tutorials/alternating-current-ac-vs-direct-current-dc) --><!-- ## Old lesson plan

- L1: What is electricity: current, voltage, and resistance + online simulation activities
- Circuit schematics?
- LX: Common electronic components: resistors and LEDs
- L2: Ohm's Law + example circuit equations/solving + online simulation activities
- L3: Measuring current, voltage, and resistance using multimeters
- L4: Series vs. parallel resistance

- L4: How to use a breadboard + moving your prev circuit to breadboards
- LX: What are LEDs and resistors?
- L5: Series vs. Parallel Resistance, Voltage Dividers, and Ohm's Law
- LX: Building your first circuit: lighting up an LED, swapping out different resistances (maybe paper-based version)

Should I have a small lesson on what is a resistor and what is an LED (or perhaps I fold that into Lesson 2).

See also notes on phone. -->