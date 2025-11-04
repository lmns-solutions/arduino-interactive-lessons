---
lang: bg
permalink: /signals/index.html
page_id: signals-index
layout: default
title: Сигнали
nav_order: 8
has_toc: true # включено по подразбиране
has_children: true
nav_exclude: false
---
# {{ page.title }}
{: .no_toc }

## Съдържание
{: .no_toc .text-delta }

1. Съдържание
{:toc}
---

<!-- TODO: напишете въведение за обработката на сигнали и преместете това в jupyter.md -->

![Снимка на Jupyter Notebook](assets/images/JupyterNotebook_Screenshot.png)

Снимка на Jupyter Notebook, показваща анализ и визуализация на 3-осев акселерометър за изчисляване на броя на стъпките.
{: .fs-1 }

Ще използваме [Jupyter Notebook](https://jupyter.org/index.html) за частта от курса, посветена на обработката на сигнали и машинно обучение. Jupyter Notebook е популярна платформа за наука за данни, предназначена за анализ, обработка, класифициране, моделиране и визуализация на данни. Макар Notebook да поддържа няколко езика (като R, Julia), ние ще използваме Python (по-конкретно Python 3). За тези, които са запознати с Python, Jupyter Notebook е изграден върху ядрото IPython, така че можете да използвате всички команди [magic](https://ipython.readthedocs.io/en/stable/interactive/magics.html) на IPython!

За анализ ще използваме [SciPy](https://www.scipy.org/) („Sigh Pie") екосистема от отворени библиотеки за математика, наука и инженерство. По-конкретно, [NumPy](https://numpy.org/), [SciPy](https://www.scipy.org/scipylib/index.html) и [matplotlib](https://matplotlib.org/). Може да се занимаваме и с [Pandas](https://pandas.pydata.org/) и [Seaborn](https://seaborn.pydata.org/). За машинно обучение ще използваме [sci-kit learn](https://scikit-learn.org/stable/). И не се притеснявайте, всички тези библиотеки ще бъдат управлявани и инсталирани за нас!

Точно както за Arduino, има множество чудесни уроци, форуми и видеоклипове за Jupyter Notebook и библиотеките SciPy. Можете да търсите онлайн и да споделяте с класа това, което откриете.

<!-- може би тук става дума за Google Colab? https://colab.research.google.com/notebooks/intro.ipynb -->

## Уроци

Тези уроци са предназначени да бъдат интерактивни. Трябва да модифицирате, изпълнявате, повтаряте и да си играете с клетките. Направете тези бележници свои!

Има три начина да разгледате уроците: **първо**, можете да кликнете върху експортираните HTML версии; те обаче не са интерактивни; **второ**, можете да клонирате нашето [Signals repo](https://github.com/makeabilitylab/signals) и да отворите `ipynb` файловете локално на вашия компютър (това е нашият препоръчителен подход):

```
git clone https://github.com/makeabilitylab/signals.git
```

**Трето и последно,** ако искате бърз и лесен начин да взаимодействате с бележниците, можете да използвате [Binder](https://mybinder.org/) или [Google Colab](https://colab.research.google.com/) — и двете облачни услуги зареждат динамично нашите бележници директно от GitHub, така че можете да играете, редактирате код и *т.н.* директно от браузъра си — само с едно кликване. Супер!

**Забележка:** Отново, за вашите реални задачи вероятно ще искате да изпълнявате бележниците си **локално**, защото ще искате да зареждате данни от диска. Можете да направите това и с Google Colab (просто ще трябва да прехвърлите данните си в облачната среда; вижте по-долу).

<!-- TODO: добавете първата бележка за използването на Jupyter Notebook -->
<!-- TODO: добавете H3, който да отделя малко тази информация -->
### Въведение в Jupyter Notebook, Python и SciPy

#### [Урок 0: Инсталиране на Jupyter Notebook и съвети](jupyter-notebook.md)

В [нашия първоначален урок](jupyter-notebook.md) ще научим как да инсталираме Jupyter Notebook, полезно разширение, което автоматично генерира съдържание, и ще разгледаме някои съвети.

#### Урок 1: Въведение в Jupyter Notebook

В интернет има много въвеждащи уроци и видеоклипове за Jupyter Notebook. Ще направим кратка демонстрация на Notebook в клас, но ако искате да научите повече, можете да се запознаете с този [урок на Datacamp](https://www.datacamp.com/community/tutorials/tutorial-jupyter-notebook) или този [урок на Dataquest](https://www.dataquest.io/blog/jupyter-notebook-tutorial/). Въпреки това, ще научите Notebook, докато преминавате през уроците по-долу и работите по задачите си.

<!-- MusicInformationRetrieval има добра страница с основи на Jupyter Notebook: https://musicinformationretrieval.com/get_good_at_ipython.html -->

#### [Урок 2: Въведение в Python](IntroToPython.html) ([ipynb](https://github.com/makeabilitylab/signals/blob/master/Tutorials/IntroToPython.ipynb))
 

Ако не сте запознати с Python – или дори ако сте – е добра идея да започнете с това (бързо) въведение в Python. То ще ви даде и представа за Jupyter Notebook. За да извлечете максимална полза от тези примерни Notebooks, трябва да модифицирате и изпълните клетките сами (и да добавите свои собствени клетки) . [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/makeabilitylab/signals/master?filepath=Tutorials%2FIntroToPython.ipynb) [![Отвори в Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/makeabilitylab/signals/blob/master/Tutorials/IntroToPython.ipynb).

#### [Урок 3: Въведение в NumPy](IntroToNumPy.html) ([ipynb](https://github.com/makeabilitylab/signals/blob/master/Tutorials/IntroToNumPy.ipynb))

Ще използваме [NumPy масиви](https://numpy.org/doc/stable/reference/arrays.html) като една от основните ни структури от данни. Използвайте този бележник, за да се запознаете с тях. Не е необходимо да станете експерти в тази област, но е полезно да разберете какво представляват `np.array` и как се използват и манипулират. [![Отвори в Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/makeabilitylab/signals/master?filepath=Tutorials%2FIntroToNumPy.ipynb) [![Отвори в Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/makeabilitylab/signals/blob/master/Tutorials/IntroToNumPy.ipynb)

#### [Урок 4: Въведение в Matplotlib](IntroToMatplotlib.html) ([ipynb](https://github.com/makeabilitylab/signals/blob/master/Tutorials/IntroToMatplotlib.ipynb))

За визуализиране на данните ни ще използваме [Matplotlib](https://matplotlib.org/) — невероятно мощна библиотека за визуализация с малко ексцентричен API (благодарение на Matlab). Отворете този бележник, научете как да създавате основни диаграми и опитайте да създадете свои собствени. [![Отвори в Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/makeabilitylab/signals/master?filepath=Tutorials%2FIntroToMatplotlib.ipynb) [![Отвори в Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/makeabilitylab/signals/blob/master/Tutorials/IntroToMatplotlib.ipynb)

### Сигнали

<!-- Не мога да накарам Binder да работи в следващите уроци, може би заради интервалите в имената на файловете? -->
<!-- Например: https://mybinder.org/v2/gh/makeabilitylab/signals/master?filepath=Tutorials%2FSignals%2520-%2520Comparing%2520Signals.ipynb не работи -->

#### [Урок 1: Квантизация и дискретизация](QuantizationAndSampling/index.html) ([ipynb](https://github.com/makeabilitylab/signals/blob/master/Tutorials/Signals%20-%20Quantization%20and%20Sampling.ipynb))

Представя двата основни фактора при дигитализирането на аналогов сигнал: **квантизация** и **дискретизация**. Описва и показва ефекта от различни нива на квантизация и честоти на дискретизация върху реални сигнали (аудио данни) и представя теоремата на Найкуист за дискретизация, алиасинг и някои честотни графики.
 

#### [Урок 2: Сравняване на сигнали (времева област)](ComparingSignals/index.html) ([ipynb](https://github.com/makeabilitylab/signals/blob/master/Tutorials/Signals%20-%20Comparing%20Signals.ipynb))

Въвежда техники за сравняване на сигнали във времевата област, включително евклидово разстояние, кръстосана корелация и динамично изкривяване на времето (DTW).

#### [Урок 3: Честотен анализ](FrequencyAnalysis/index.html) ([ipynb](https://github.com/makeabilitylab/signals/blob/master/Tutorials/Signals%20-%20Frequency%20Analysis.ipynb))

Въвежда честотния анализ, включително дискретни Фурие трансформации (DFT) и интуицията за това как работят, бързи Фурие трансформации и спектрални честотни графики, както и краткосрочни Фурие трансформации (STFT) и спектрограми.

### Упражнения

#### [Упражнение 1: Стъпка тракер](StepTracker/index.html) ([ipynb](https://github.com/makeabilitylab/signals/blob/master/Projects/StepTracker/StepTracker-Exercises.ipynb))

Въз основа на задачата ни от A2, нека анализираме някои примерни данни за стъпките от акселерометъра и да напишем алгоритъм в Jupyter Notebook, за да изведем стъпките. Notebook е идеално подходящ за тази задача: лесно е да визуализирате данни с [Matplotlib](https://matplotlib.org/), а [NumPy](https://numpy.org/) и [SciPy](https://www.scipy.org/scipylib/index.html) предлагат филтриране, отстраняване на тенденции и други полезни алгоритми за обработка на сигнали. Можете да опитате много идеи, да видите колко добре работят върху някои тестови данни и след това да приложите най-обещаващата си идея на ESP32. [![Отвори в Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/makeabilitylab/signals/blob/master/Projects/StepTracker/StepTracker-Exercises.ipynb).
 

#### [Упражнение 2: Разпознавател на жестове: Съвпадение на форми](gesturerec/shapebased/index.html) ([ipynb](https://github.com/makeabilitylab/signals/blob/master/Projects/GestureRecognizer/GestureRecognizer-ShapeBased.ipynb))

Нека създадем разпознавател на жестове, базиран на форми (или шаблони)! Този бележник предоставя структурите на данни и експерименталната рамка за писане и тестване на класификатори на жестове, базирани на форми.

#### [Упражнение 3: Разпознавател на жестове: Наблюдавано обучение](gesturerec/featurebased/index.html) ([ipynb](https://github.com/makeabilitylab/signals/blob/master/Projects/GestureRecognizer/GestureRecognizer-FeatureBased.ipynb))

Нека създадем разпознавател на жестове, базиран на характеристики (или модел), като използваме супервизирано обучение! Този бележник предоставя обща информация за това как да използвате супервизирано обучение и библиотеката Scikit-learn за класифициране на жестове.

#### [Упражнение 4: Разпознавател на жестове: автоматичен избор на характеристики и настройка на хиперпараметри](FeatureSelectionAndHyperparameterTuning/index.html) ([ipynb](https://github.com/makeabilitylab/signals/blob/master/Projects/GestureRecognizer/Feature%20Selection%20and%20Hyperparameter%20Tuning.ipynb))

В този бележник ще научите за автоматичния избор на характеристики и настройката на хиперпараметри.

<!-- ![](assets/images/JupyterNotebook_StepTrackerVisualization_Screenshot.png) -->

<!-- ## Вземане на проби

Обичам това видео на Монти Монтгомъри от Xiph за вземането на проби: https://youtu.be/FG9jemV1T7I, озаглавено: „Въведение в цифровите медии за маниаци от Кристофър „Монти" Монтгомъри и Xiph.org". Показва също влиянието на честотата на вземане на проби и квантизацията върху аудиото -->

<!-- Класификация на градските звуци: https://aqibsaeed.github.io/2016-09-03-urban-sound-classification-part-1/ -->
