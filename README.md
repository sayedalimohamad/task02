# Week 02 - Data Storage in MongoDB and Flask API Development

# Almayadeen Articles Analysis

This project provides a Flask-based API to analyze and query a MongoDB database containing articles from Almayadeen. The API supports a variety of queries, including retrieving top keywords, top authors, articles by publication date, and more.

## Prerequisites

- Python 3.x
- MongoDB
- Flask
- pymongo

---

# API Endpoints

## Home Page

- **URL:** `/`
- **Method:** `GET`
- **Description:** Renders the home page.

## Top Keywords

- **URL:** `/top_keywords`
- **Method:** `GET`
- **Description:** Returns the top 10 keywords used in the articles.

## Top Authors

- **URL:** `/top_authors`
- **Method:** `GET`
- **Description:** Returns the top 10 authors based on the number of articles.

## Articles by Publication Date

- **URL:** `/articles_by_date`
- **Method:** `GET`
- **Description:** Returns the number of articles published on each date.

## Articles by Word Count

- **URL:** `/articles_by_word_count`
- **Method:** `GET`
- **Description:** Returns the number of articles based on word count.

## Articles by Language

- **URL:** `/articles_by_language`
- **Method:** `GET`
- **Description:** Returns the number of articles in each language.

## Articles by Classes

- **URL:** `/articles_by_classes`
- **Method:** `GET`
- **Description:** Returns the number of articles for each class.

## Recent Articles

- **URL:** `/recent_articles`
- **Method:** `GET`
- **Description:** Returns the 10 most recent articles.

## Articles by Keyword

- **URL:** `/articles_by_keyword/<keyword>`
- **Method:** `GET`
- **Description:** Returns articles that contain a specific keyword.

## Articles by Author

- **URL:** `/articles_by_author/<author_name>`
- **Method:** `GET`
- **Description:** Returns articles written by a specific author.

## Top Classes

- **URL:** `/top_classes`
- **Method:** `GET`
- **Description:** Returns the top 10 classes based on the number of articles.

## Article Details

- **URL:** `/article_details/<postid>`
- **Method:** `GET`
- **Description:** Returns details of a specific article based on its post ID.

## Articles Containing Video

- **URL:** `/articles_with_video`
- **Method:** `GET`
- **Description:** Returns articles that contain videos.

## Articles by Publication Year

- **URL:** `/articles_by_year/<year>`
- **Method:** `GET`
- **Description:** Returns the number of articles published in a specific year.

## Longest Articles

- **URL:** `/longest_articles`
- **Method:** `GET`
- **Description:** Returns the top 10 longest articles based on word count.

## Shortest Articles

- **URL:** `/shortest_articles`
- **Method:** `GET`
- **Description:** Returns the top 10 shortest articles based on word count.

## Articles by Keyword Count

- **URL:** `/articles_by_keyword_count`
- **Method:** `GET`
- **Description:** Returns the number of articles grouped by keyword count.

## Articles with Thumbnails

- **URL:** `/articles_with_thumbnail`
- **Method:** `GET`
- **Description:** Returns articles that have a thumbnail.

## Articles Updated After Publication

- **URL:** `/articles_updated_after_publication`
- **Method:** `GET`
- **Description:** Returns articles that have been updated after their initial publication.

## Articles by Coverage

- **URL:** `/articles_by_coverage/<coverage>`
- **Method:** `GET`
- **Description:** Returns articles based on specific coverage criteria.

## Popular Keywords in the Last X Days

- **URL:** `/popular_keywords_last_<int:x>_days`
- **Method:** `GET`
- **Description:** Returns the top 10 keywords used in the last `x` days.

## AND MORE ...
