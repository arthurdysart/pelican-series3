# Pelican: series3
[Arthur Dysart](https://github.com/arthurdysart)

Enable Pelican articles to be grouped in ["series."](https://www.google.com/search?q=define+book+series). New JINJA2
template variables `all_series` and `article.series.*` contain details on constituent articles. Control article order
and appearance in series via Pelican settings `SERIES__*`.

Built for [Pelican 4.2.0](https://docs.getpelican.com/en/stable/changelog.html#id1) and
[Python 3.6+](https://www.python.org/downloads/release/python-360/).

## Quick start
Update or create the following variables in `pelicanconf.py`:
```python3
# ~/my_pelican_proj/pelicanconf.py

PATH = "content"
PLUGIN_PATHS = ["pelican-plugins"]
PLUGINS = ["series3"]

SERIES__IS_DATE_SORT = True
SERIES__IS_SERIES_INDEX_ENABLED = True
SERIES__IGNORE_SERIES_TITLES = [""]
```

Create new article with metadata parameters `series` (required) and `series_index` (optional):
```markdown
# ~/my_pelican_proj/content/articles/hello_world.md

title: Hello World
date: 2019-01-01
slug: hello-world
series: my-first-articles
series_index: 1

This is my first article. Hello World!
```

Create new JINJA2 HTML template:
```jinja2
# ~/my_pelican_proj/theme/templates/index.html

{# Access `all_series` attribute #}
{% if all_series %}
    <p>All series in blog:</p>
    <ol>
        {% for series, items in all_series %}
        <li {% if series == article.series %}class="active"{% endif %}>
            Series "{{ series }}":
            <ol>
                {% for item in items %}
                <li {% if item == article %}class="active"{% endif %}>
                    <a href="{{ SITEURL }}/{{ item.url }}">{{ item.title }}</a>
                </li>
                {% endfor %}
            </ol>
        </li>
        {% endfor %}
    </ol>
{% endif %}

{# Access `article.series.*` attributes #}
{% if article.series %}
    <p>This post is Part {{ article.series.index }} of the "{{ article.series.name }}" series:</p>
    <ol class="parts">
        {% for item in article.series.all %}
            <li {% if item == article %}class="active"{% endif %}>
                <a href="{{ SITEURL }}/{{ item.url }}">{{ item.title }}</a>
            </li>
        {% endfor %}
    </ol>
{% endif %}
```

Accessible JINJA2 template variables:

| JINJA2 variable             | Evaluation                                       | Description                                                              |
|-----------------------------|--------------------------------------------------|--------------------------------------------------------------------------|
| all_series                  | [("first-series", [Obj-1, ..., Obj-N]), ...]     | Grouped `pelican.content.Article` objects according to series name.      |
| article.series.name         | "first-series"                                   | Series name set in article metadata.                                     |
| article.series.index        | 3                                                | Index of current article. May change during sorting!                     |
| article.series.all          | [Obj-1, ..., Obj-N]                              | Ordered list of articles in series (inclusive).                          |
| article.series.all_previous | [Obj-1, Obj-2]                                   | Ordered list of articles published before current article (exclusive).   |
| article.series.all_next     | [Obj-4, ..., Obj-N]                              | Ordered list of articles published after current article (exclusive).    |
| article.series.previous     | Obj-2                                            | Last article in series (identical to `article.series.all_previous[-1]`). |
| article.series.next         | Obj-4                                            | Next article in the series (identical to `article.series.all_next[0]`).  |


## Description

### Features
This plugin inherits features from its predecessors
["series".](https://github.com/getpelican/pelican-plugins/tree/master/series) such as priority index ordering and
`article.series.*` JINJA variables. New additional features include:

- Enables Pelican articles to be classified under a SERIES label, independent of CATEGORY and TAG labels.
- Extends `pelican.content.Article` objects with `series.*` attributes available in JINJA2 templates.
- Creates `all_series` attribute exposing SERIES titles, and their articles, as JINJA2 template variables.

### Updates
This plugin extends the functionality of its predecessors by:
1. Creating `all_series` parameter that collects all series and their constituent `article` objects,
2. Enabling new `SERIES__*` PELICANCONF settings to control series parsing and sorting behavior, and
3. reducing and optimizing loop iterations.

## Installation
See the [official Pelican documentation](https://docs.getpelican.com/en/stable/) and the
[Pelican Plugins documentation](https://github.com/getpelican/pelican-plugins#pelican-plugins)
for more details on using plugins.

1. Install Pelican and setup new project:
    ```bash
    python3 -m venv ~/venv
    source ~/venv/bin/activate
    pip3 install --upgrade pelican
    mkdir ~/my_pelican_proj && cd ~/my_pelican_proj
    pelican-quickstart
    ```

2. Copy repository:
    ```bash
    git clone \
        --recursive \
        --single-branch --branch=master \
        https://github.com/getpelican/pelican-plugins \
        ~/pelican-plugins
    ```

3. Update `pelicanconf.py` and create Pelican assets. See [Quickstart](#quick-start) section.

4. Generate Pelican static site and view output:
    ```bash
    pelican ~/my_pelican_proj/content \
        && pelican --listen
    
    python3 -m webbrowser http://127.0.0.1:8000/
    ```

## Contributors
Inspired by the ["series"](https://github.com/getpelican/pelican-plugins/tree/master/series) plugin first developed by:
- Leonardo Giordani <giordani.leonardo@gmail.com>
- Boris Feld <lothiraldan@gmail.com>
