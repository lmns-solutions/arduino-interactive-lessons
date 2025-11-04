---
lang: bg
permalink: /website-dev.html
page_id: website-dev
layout: default
title: Бележки за разработката на уебсайта
has_toc: false # включено по подразбиране
nav_exclude: true
usemathjax: true
usetocbot: true
---

# {{ page.title | replace_first:"L",'Урок '}}
{: .no_toc }

## Съдържание
{: .no_toc .text-delta }

1. Съдържание
{:toc}
---

## Стартиране на уебсайта
Ако разполагате с необходимите библиотеки и софтуерна инфраструктура (например Jekyll) — вижте нашето [ръководство за настройка на уебсайта тук](website-install.md) — можете да отворите терминала в VSCode и да въведете:

```
> bundle exec jekyll serve 
```

## VS Code
Използвам [VS Code](https://code.visualstudio.com/) с някои популярни разширения за маркиране, за да разработвам уебсайта.

### Разширения
Имам инсталирани следните разширения за VS Code:
- Code Spell Check 1.8.0 (1,1 млн. изтегляния)
- Markdown All in One 2.7.0 (1,2 млн. изтегляния)
- markdownlint 0.34.0 (1,5 млн. изтегляния)
- Paste Image 1.0.4 (45 000): Позволява на потребителя да поставя изображения от клипборда с помощта на `alt-cmd-v` (Mac) и `ctrl-alt-v` (Windows)

## Вграждане на markdown съдържание в страница

Включване на други markdown страници: https://stackoverflow.com/a/41966993/388117.

<!-- {знак процент include_relative tutorials/index.md знак процент} -->

## Подчертаване на код
<!-- Подчертаване на фрагмент от код: https://jekyllrb.com/docs/liquid/tags/#code-snippet-highlighting -->

### Използване на функцията `highlight` на Jekyll
Това е тест.
{% highlight C %}
void loop() {
digitalWrite(led, HIGH); // включване на LED (HIGH е нивото на напрежението)
delay(1000); // изчакване за една секунда
digitalWrite(led, LOW); // изключване на LED чрез понижаване на напрежението
delay(1000); // изчакване за една секунда
}
{% endhighlight C %}

### Използване на отметките на Markdown

```
void loop() {
digitalWrite(led, HIGH); // включване на LED (HIGH е нивото на напрежението)
delay(1000); // изчакване за секунда
digitalWrite(led, LOW); // изключване на LED чрез намаляване на напрежението до LOW
delay(1000); // изчакване за секунда
}
```

### Използване на `gist-it.appspot.com` за вграждане на код директно от GitHub
<!-- <script src="http://gist-it.appspot.com/http://github.com/$file"></script> -->
Това е страхотно! Може да вгражда код директно! Ако работи, трябва да вгради кода [Blink.ino](https://github.com/jonfroehlich/arduino/blob/master/Basics/digitalWrite/Blink/Blink.ino) директно по-долу.

<script src="http://gist-it.appspot.com/https://github.com/jonfroehlich/arduino/blob/master/Basics/digitalWrite/Blink/Blink.ino?footer=minimal"></script>

Актуализация: [gist-it.appspot.com](https://gist-it.appspot.com/) изглежда не работи.

![](assets/images/gist-it.appspot.com-down.png)

### Използване на `emgithub.com` за вграждане на код директно от GitHub
Като алтернатива, тъй като изглежда, че [gist-it.appspot.com](https://gist-it.appspot.com/) не работи, можем да използваме [emgithub.com](https://emgithub.com/)

<script src="https://emgithub.com/embed.js?target=https%3A%2F%2Fgithub.com%2Fjonfroehlich%2Farduino%2Fblob%2Fmaster%2FBasics%2FdigitalWrite%2FBlink%2FBlink.ino& style=github&showBorder=on&showLineNumbers=on&showFileMeta=on&showCopy=on"></script>

Същото нещо без специални добавки, с изключение на бутона за копиране:

<script src="https://emgithub.com/embed.js?target=https%3A%2F%2Fgithub.com%2Fjonfroehlich%2Farduino%2Fblob%2Fmaster%2FBasics%2FdigitalWrite%2FBlink%2FBlink.ino&style=github&showCopy=on"></script>

Същото, но без граници, номера на редове, метаданни на файла и бутон за копиране:

<script src="https://emgithub.com/embed.js?target=https%3A%2F%2Fgithub.com%2Fjonfroehlich%2Farduino%2Fblob%2Fmaster%2FBasics%2FdigitalWrite%2FBlink%2FBlink.ino&style=github"></script>

## Стил на таблиците

| Колона 1 | Колона 2 |
| --------------------------------------- | ------------------------------------- |
| `border-bottom-right-radius` | Определя формата на долния десен ъгъл |

За да зададем размера на таблицата, можем да използваме вградени span елементи.

| <span style="display: inline-block; width:500px">текст</span> | описание |
| --------------------------------------- | ------------------------------------- |
| `border-bottom-right-radius` | Определя формата на долния десен ъгъл |


## Направете бележка (Call Out Box)
Има различни начини за създаване на "поле за бележки” в Markdown.

### Вариант 1: Две хоризонтални линии
Най-простият и универсален начин, препоръчан в тази [публикация в Stack Overflow](https://stackoverflow.com/a/41449789/388117), е да начертаете две хоризонтални линии около съдържанието, както е показано тук:

---

**ЗАБЕЛЕЖКА**

Това работи с почти всички варианти на Markdown (празният ред по-долу е важен). Това е от [линк](https://stackoverflow.com/a/41449789/388117).

---

### Вариант 2: Използвайте цитати

> **_ЗАБЕЛЕЖКА:_** Можете да опитате и формат на цитат от [линк](https://stackoverflow.com/a/43120795/388117).

### Вариант 3: Използвайте табулатори
Тази версия използва табулатори:

Започнете на нов ред
Натиснете два пъти табулатора, въведете съдържанието
Вашето съдържание трябва да се появи в кутия. Въпреки това, изглежда, че сега не поддържа Markdown. Например, **това** трябва да е с удебелен шрифт. Въпреки това, все още мога да използвам html, нали? Например, <b>това</b> е с удебелен шрифт? Или може би не! Така че, може би това се третира като блок код или нещо подобно...

Тази версия използва отметки (вместо табулатори), но трябва да се визуализира по същия начин:
```
Използвайте отметки
```

### Вариант 4: Персонализиран CSS
Но ако искаме да направим нещо по-сложно, ще ни е необходим персонализиран CSS. Например, много ми харесват каретата с пояснения на страницата на Бозер за преподаване в Бъркли [IoT49](https://people.eecs.berkeley.edu/~boser/courses/49_sp_2019/N_gpio.html):

![Снимка на полетата с пояснения от уебсайта на Бозер](assets/images/BoserIoT49Webpage.png)

За да се получи правилно, обаче, ще са необходими някои експерименти и персонализиран CSS.

## Как да добавите персонализиран CSS към Markdown
Добавянето на персонализиран CSS към Markdown е сравнително лесно.

### Модифициране на custom.css
Първо, добавете персонализирания CSS към `assets\css\custom.css`. Нека добавим следния нов CSS клас, наречен `.test-css`:

```css
.test-css{
font-size: 14 pt;
font-family: "Courier New", Courier, monospace;
}
```

### Използване на персонализиран CSS
Сега нека използваме този нов CSS клас, за да оформим нашия Markdown.

Този параграф вече използва стила `.test-css`. Прави това, като използваме тази синтаксис `{: .test-css}` под елемента, който искаме да оформим.
{: .test-css}

Така Markdown изглежда по следния начин:

```
Този параграф сега използва стила `.test-css`. Прави това, като използваме тази синтаксис `{: .test-css}` под елемента, който искаме да оформим.
{: .test-css}
```

## LaTeX

### Добавяне на поддръжка за LaTeX
След няколко експеримента успях да накарам LaTeX да работи, използвайки **отдалечен** Jekyll шаблон и GitHub Pages. Стъпки:
1. До голяма степен следвах съветите от тази [блог публикация](https://alan97.github.io/random/mathjax/)
2. Тъй като в момента използвам `remote_theme: pmarsceill/just-the-docs`, бях малко объркан как да направя локални промени в конфигурацията, тъй като повечето онлайн блогове и публикации във форуми говорят за редактиране на съдържанието в папката `_includes`; обаче, аз не разполагах с такава в моята локална среда за разработка. И така, какво да правя?
3. Ръчно създадох папка `_includes` с име на файл `head_custom.html` и сложих в нея:

{% highlight html %}{% raw %}
{% if page.usemathjax %}
<script type="text/javascript" async
src="https://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-MML-AM_CHTML">
</script>
{% endif %}
{% endraw %}{% endhighlight %}

### Използване на LaTeX на страници с markdown
На страниците, на които искате да използвате LaTeX, добавете `usemathjax: true` към съдържанието на заглавката

Ето едно тестово уравнение в LaTeX. Ако работи, то трябва да се визуализира правилно.

$$\frac{\partial f(y)} {\partial x} = \frac{\partial f}{\partial y} \times \frac{\partial y}{\partial x}$$

Тъй като съм вечен LaTeX новак, намерих този онлайн [WYSIWYG LaTeX математически редактор](https://www.mathcha.io/editor). За дискусия относно други WYSIWYG редактори, вижте [тази публикация в Stack Overflow](https://tex.stackexchange.com/questions/57068/wysiwyg-latex-editor-for-maths). 

## Disqus

Опитах се да накарам Disqus да работи с Jekyll, като следвах официалните им инструкции, но *просто* не се получи и нямах достатъчно време да се опитам да отстраня проблема/отстраня грешката. В конзолата на инструмента за разработчици на Chrome продължаваше да се появява безполезна грешка:

```
Uncaught SyntaxError: Unexpected end of input led-on.html:1
```

А в FireFox:

```
SyntaxError: липсва } след тялото на функцията led-on.html:1:754
бележка: { отворен на ред 1, колона 287 led-on.html:1:287
```

Но реших да опитам още веднъж и се натъкнах на [публикация в блог](https://disqus.com/home/discussion/channel-discussdisqus/why_does_the_disqus_not_work_in_jekyll/), която съдържаше решението "Универсалният код”, който Disqus ви кара да вградите в уебсайта си, включва коментари `// single line` и `/* multi-line */`. Когато Jekyll създава уебсайта, обаче, той поставя целия произведен html код на един ред (т.е. не го форматира), така че едноредните коментари нарушават кода. Ето кодът, който **не работи**.

{% highlight HTML %}
<div id="disqus_thread"></div>
<script>
/**
* ПРЕПОРЪЧИТЕЛНИ КОНФИГУРАЦИОННИ ПРОМЕНЛИВИ: РЕДАКТИРАЙТЕ И ОТМЕНЕТЕ КОМЕНТАРИТЕ В СЕКЦИЯТА ПО-ДОЛУ, ЗА ДА ВЪВЕДЕТЕ ДИНАМИЧНИ 
* СТОЙНОСТИ ОТ ВАШАТА ПЛАТФОРМА ИЛИ CMS.
* НАУЧЕТЕ ЗАЩО Е ВАЖНО ДА ОПРЕДЕЛИТЕ ТЕЗИ ПРОМЕНЛИВИ: 
* https://disqus.com/admin/universalcode/#configuration-variables */

var disqus_config = function () {
this.page.url = document.location.href; // Заменете PAGE_URL с каноничната URL променлива на вашата страница
this.page.identifier = document.location.pathname; // Заменете PAGE_IDENTIFIER с уникалната идентификационна променлива на вашата страница
};

(function () { // НЕ РЕДАКТИРАЙТЕ ПОД ТАЗИ ЛИНИЯ
var d = document,
s = d.createElement("script");
s.src = "https://physical-computing.disqus.com/embed.js";
s.setAttribute("data-timestamp", +new Date());
(d.head || d.body).appendChild(s);
}) ();
</script>
<noscript>Моля, активирайте JavaScript, за да видите <a href="https://disqus.com/?ref_noscript">коментарите, поддържани от
Disqus.</a></noscript>
</div>
{% endhighlight HTML %}

А ето и кода, който **работи**, като едноредните коментари са заменени с многоредни коментари:

{% highlight HTML %}
<div id="disqus_thread"></div>
<script>
/**
* ПРЕПОРЪЧИТЕЛНИ КОНФИГУРАЦИОННИ ПРОМЕНЛИВИ: РЕДАКТИРАЙТЕ И ОТМЕНЕТЕ КОМЕНТАРИТЕ В СЕКЦИЯТА ПО-ДОЛУ, ЗА ДА ВЪВЕДЕТЕ ДИНАМИЧНИ 
* СТОЙНОСТИ ОТ ВАШАТА ПЛАТФОРМА ИЛИ CMS.
* НАУЧЕТЕ ЗАЩО Е ВАЖНО ДА ОПРЕДЕЛИТЕ ТЕЗИ ПРОМЕНЛИВИ:
* https://disqus.com/admin/universalcode/#configuration-variables */

var disqus_config = function () {
this.page.url = document.location.href; /* Заменете PAGE_URL с каноничната URL променлива на вашата страница */
this.page.identifier = document.location.pathname; /* Заменете PAGE_IDENTIFIER с уникалната идентификационна променлива на вашата страница */
};

(function () { /* НЕ РЕДАКТИРАЙТЕ ПОД ТАЗИ ЛИНИЯ */
var d = document,
s = d.createElement("script");
s.src = "https://physical-computing.disqus.com/embed.js";
s.setAttribute("data-timestamp", +new Date());
(d.head || d.body).appendChild(s);
})();
</script>
<noscript>Моля, активирайте JavaScript, за да видите <a href="https://disqus.com/?ref_noscript">коментарите, поддържани от
Disqus.</a></noscript>
</div>
{% endhighlight HTML %}

## Инструменти

### Създаване на анимирани GIF файлове
За да създавам анимирани GIF файлове, използвам [https://ezgif.com/](https://ezgif.com/).

#### Шаблони
- Minimal Mistakes
- "Just the Docs". Вероятно любимият ми шаблон, който съм оценявал досега.
