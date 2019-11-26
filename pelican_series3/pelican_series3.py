# -*- coding: utf-8 -*-
"""
PELICAN 4.2.0 - SERIES v3
Arthur Dysart <https://github.com/arthurdysart>

FEATURES
- Enables Pelican articles to be classified under a SERIES label, independent of CATEGORY and TAG labels.
- Extends `pelican.content.Article` objects with `series.*` attributes available in JINJA2 templates.
- Creates `all_series` attribute exposing SERIES titles, and their articles, as JINJA2 template variables.

UPDATES
This plugin extends the functionality of its predecessors by:
    (1) Creating `all_series` parameter that collects all series and their constituent `article` objects,
    (2) Enabling new `SERIES__*` PELICANCONF settings to control series parsing and sorting behavior, and
    (3) reducing and optimizing loop iterations.

Copyright (c) 2019 Arthur Dysart. Inspired by the `series` plugin first developed by:
    - Leonardo Giordani <giordani.leonardo@gmail.com>
    - Boris Feld <lothiraldan@gmail.com>
"""


# REQUIRED MODULES
from collections import defaultdict
from pelican import signals


# MODULE DEFINITIONS
def apply_series(article_generator):
    """
    Parses and groups all articles under common SERIES label.
    Exposes `article.series.*` and `all_series` variables to JINJA2 article templates.

    :param article_generator: generator object containing `settings` and `articles` attributes
    :type article_generator: pelican.generators.ArticlesGenerator
    """
    # Import PELICANCONF settings
    is_date_sort = article_generator.settings.get("SERIES__IS_DATE_SORT", False)
    is_series_index_enabled = article_generator.settings.get("SERIES__IS_SERIES_INDEX_ENABLED", True)
    ignore_series_titles = article_generator.settings.get("SERIES__IGNORE_SERIES_TITLES", [])

    all_series = defaultdict(lambda: defaultdict(list))

    for article in article_generator.articles:
        # Collect all unique series and their articles (numbered and unnumbered)
        if article.metadata.get("series") not in {None, "", *ignore_series_titles}:
            # Found article with `series` attribute
            series_name = article.metadata["series"]

            if (is_series_index_enabled and
                article.metadata.get("series_index") not in {None, ""}):
                # Set sort key as `series_index` attribute
                all_series[series_name]["numbered"].append(article)

            else:
                # Set sort key as date attribute
                if is_date_sort is False:
                    # Set sort key as `modified` attribute (else `date` if invalid)
                    article.metadata["_series_sort_date"] = (article.modified
                                                             if article.modified not in (None, "")
                                                             else article.date)

                else:
                    # Set sort key as `date` attribute only
                    article.metadata["_series_sort_date"] = article.date

                all_series[series_name]["unnumbered"].append(article)

    collected_series = {}

    for series_name, unordered_articles in all_series.items():
        # Sort all series articles, then combine into single collection
        unordered_articles["numbered"].sort(key=lambda x: getattr(x, "metadata").get("series_index"),
                                            reverse=False)

        unordered_articles["unnumbered"].sort(key=lambda x: getattr(x, "metadata").get("_series_sort_date"),
                                              reverse=False)

        ordered_articles = unordered_articles["numbered"] + unordered_articles["unnumbered"]

        for num, article in enumerate(ordered_articles):
            # Set attributes for each `articles.series` object
            series_attributes = {"name": series_name,
                                 "index": num + 1,
                                 "all": ordered_articles,
                                 "all_previous": ordered_articles[:num],
                                 "all_next": ordered_articles[num+1:],
                                 "previous": ordered_articles[num-1] if num > 0 else None,
                                 "next": ordered_articles[num+1] if num + 1 < len(ordered_articles) else None}

            setattr(article, "series", series_attributes)

        # Collect all sorted articles organized by series name
        collected_series[series_name] = ordered_articles

    # Create `all_series` variable, then update context for JINJA2 templates
    setattr(article_generator, "all_series", collected_series)

    article_generator._update_context(["all_series"])


# MAIN MODULE
def register():
    signals.article_generator_finalized.connect(apply_series)

