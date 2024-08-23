from flask import Flask, jsonify, request, Response, render_template
from pymongo import MongoClient
import datetime, json
from bson import ObjectId

app = Flask(__name__)

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["almayadeen"]
collection = db["articles"]


@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")


# Route for getting top keywords
@app.route("/top_keywords", methods=["GET"])
def top_keywords():
    pipeline = [
        {"$unwind": "$keywords"},
        {"$group": {"_id": "$keywords", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 10},
    ]
    result = list(collection.aggregate(pipeline))
    json_result = json.dumps(result, ensure_ascii=False, indent=4)
    return Response(json_result, content_type="application/json; charset=utf-8"), 200


# Route for getting top authors
@app.route("/top_authors", methods=["GET"])
def top_authors():
    pipeline = [
        {"$group": {"_id": "$author", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 10},
    ]
    result = list(collection.aggregate(pipeline))
    json_result = json.dumps(result, ensure_ascii=False, indent=4)
    return Response(json_result, content_type="application/json; charset=utf-8"), 200


# Route for getting articles by publication date
@app.route("/articles_by_date", methods=["GET"])
def articles_by_date():
    pipeline = [
        {
            "$group": {
                "_id": {
                    "$dateToString": {
                        "format": "%Y-%m-%d",
                        "date": {"$toDate": "$published_time"},
                    }
                },
                "count": {"$sum": 1},
            }
        },
        {"$sort": {"count": -1}},
    ]
    result = list(collection.aggregate(pipeline))
    json_result = json.dumps(result, ensure_ascii=False, indent=4)
    return Response(json_result, content_type="application/json; charset=utf-8"), 200


# Route for getting articles by word count
@app.route("/articles_by_word_count", methods=["GET"])
def articles_by_word_count():
    pipeline = [
        {"$group": {"_id": "$word_count", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 10},
    ]
    result = list(collection.aggregate(pipeline))
    json_result = json.dumps(result, ensure_ascii=False, indent=4)
    return Response(json_result, content_type="application/json; charset=utf-8"), 200


# Route for getting articles by language
@app.route("/articles_by_language", methods=["GET"])
def articles_by_language():
    pipeline = [
        {"$group": {"_id": "$lang", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
    ]
    result = list(collection.aggregate(pipeline))
    json_result = json.dumps(result, ensure_ascii=False, indent=4)
    return Response(json_result, content_type="application/json; charset=utf-8"), 200


# Route for getting articles by classes
@app.route("/articles_by_classes", methods=["GET"])
def articles_by_classes():
    pipeline = [
        {"$group": {"_id": "$classes", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
    ]
    result = list(collection.aggregate(pipeline))
    json_result = json.dumps(result, ensure_ascii=False, indent=4)
    return Response(json_result, content_type="application/json; charset=utf-8"), 200


# Route for getting recent articles
@app.route("/recent_articles", methods=["GET"])
def recent_articles():
    pipeline = [{"$sort": {"published_time": -1}}, {"$limit": 10}]
    result = list(collection.aggregate(pipeline))

    for doc in result:
        if "_id" in doc and isinstance(doc["_id"], ObjectId):
            doc["_id"] = str(doc["_id"])

    json_result = json.dumps(result, ensure_ascii=False, indent=4)
    return Response(json_result, content_type="application/json; charset=utf-8"), 200


# Route for getting articles by keyword
@app.route("/articles_by_keyword/<keyword>", methods=["GET"])
def articles_by_keyword(keyword):
    pipeline = [{"$match": {"keywords": keyword}}, {"$project": {"_id": 0, "title": 1}}]
    result = list(collection.aggregate(pipeline))
    json_result = json.dumps(result, ensure_ascii=False, indent=4)
    return Response(json_result, content_type="application/json; charset=utf-8"), 200


# Route for getting articles by author
@app.route("/articles_by_author/<author_name>", methods=["GET"])
def articles_by_author(author_name):
    pipeline = [
        {"$match": {"author": author_name}},
        {"$project": {"_id": 0, "title": 1}},
    ]
    result = list(collection.aggregate(pipeline))
    json_result = json.dumps(result, ensure_ascii=False, indent=4)
    return Response(json_result, content_type="application/json; charset=utf-8"), 200


# Route for getting top classes
@app.route("/top_classes", methods=["GET"])
def top_classes():
    pipeline = [
        {"$unwind": "$classes"},
        {"$group": {"_id": "$classes", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 10},
    ]
    result = list(collection.aggregate(pipeline))
    json_result = json.dumps(result, ensure_ascii=False, indent=4)
    return Response(json_result, content_type="application/json; charset=utf-8"), 200


# Route for getting article details
@app.route("/article_details/<postid>", methods=["GET"])
def article_details(postid):
    pipeline = [
        {"$match": {"post_id": postid}},
        {"$project": {"_id": 0, "url": 1, "title": 1, "keywords": 1}},
    ]
    result = list(collection.aggregate(pipeline))
    json_result = json.dumps(result, ensure_ascii=False, indent=4)
    return Response(json_result, content_type="application/json; charset=utf-8"), 200


# Route for getting articles containing video
@app.route("/articles_with_video", methods=["GET"])
def articles_with_video():
    pipeline = [
        {"$match": {"video_duration": {"$ne": None}}},
        {"$project": {"_id": 0, "title": 1}},
    ]
    result = list(collection.aggregate(pipeline))
    json_result = json.dumps(result, ensure_ascii=False, indent=4)
    return Response(json_result, content_type="application/json; charset=utf-8"), 200


# Route for getting articles by publication year
@app.route("/articles_by_year/<year>", methods=["GET"])
def articles_by_year(year):
    pipeline = [
        {"$match": {"published_time": {"$regex": "^" + year}}},
        {"$group": {"_id": None, "count": {"$sum": 1}}},
        {"$project": {"_id": 0, "year": year, "count": 1}},
    ]
    result = list(collection.aggregate(pipeline))
    json_result = json.dumps(result, ensure_ascii=False, indent=4)
    return Response(json_result, content_type="application/json; charset=utf-8"), 200


# Route for getting longest articles
@app.route("/longest_articles", methods=["GET"])
def longest_articles():
    pipeline = [
        {
            "$project": {
                "_id": 0,
                "title": 1,
                "word_count": {"$toInt": {"$ifNull": ["$word_count", 0]}},
            }
        },
        {"$sort": {"word_count": -1}},
        {"$limit": 10},
    ]

    result = list(collection.aggregate(pipeline))
    json_result = json.dumps(result, ensure_ascii=False, indent=4)
    return Response(json_result, content_type="application/json; charset=utf-8"), 200


# Route for getting shortest articles
@app.route("/shortest_articles", methods=["GET"])
def shortest_articles():
    pipeline = [
        {
            "$project": {
                "_id": 0,
                "title": 1,
                "word_count": {"$toInt": {"$ifNull": ["$word_count", 0]}},
            }
        },
        {"$sort": {"word_count": 1}},
        {"$limit": 10},
    ]
    result = list(collection.aggregate(pipeline))
    json_result = json.dumps(result, ensure_ascii=False, indent=4)
    return Response(json_result, content_type="application/json; charset=utf-8"), 200


# Route for getting articles by keyword count
@app.route("/articles_by_keyword_count", methods=["GET"])
def articles_by_keyword_count():
    pipeline = [
        {"$project": {"_id": 0, "title": 1, "keyword_count": {"$size": "$keywords"}}},
        {"$group": {"_id": "$keyword_count", "count": {"$sum": 1}}},
        {"$addFields": {"keywords": "$_id"}},
        {"$project": {"_id": 0, "keywords": 1, "count": 1}},
        {"$sort": {"count": -1}},
    ]
    result = list(collection.aggregate(pipeline))
    json_result = json.dumps(result, ensure_ascii=False, indent=4)
    return Response(json_result, content_type="application/json; charset=utf-8"), 200


# Route for getting articles with thumbnail
@app.route("/articles_with_thumbnail", methods=["GET"])
def articles_with_thumbnail():
    pipeline = [
        {"$match": {"thumbnail": {"$ne": None}}},
        {"$project": {"_id": 0, "title": 1}},
    ]
    result = list(collection.aggregate(pipeline))
    json_result = json.dumps(result, ensure_ascii=False, indent=4)
    return Response(json_result, content_type="application/json; charset=utf-8"), 200


# Route for getting articles updated after publication
@app.route("/articles_updated_after_publication", methods=["GET"])
def articles_updated_after_publication():
    pipeline = [
        {"$match": {"last_updated": {"$gt": "$published_time"}}},
        {"$project": {"_id": 0, "title": 1}},
    ]
    result = list(collection.aggregate(pipeline))
    json_result = json.dumps(result, ensure_ascii=False, indent=4)
    return Response(json_result, content_type="application/json; charset=utf-8"), 200


@app.route("/articles_by_coverage/<coverage>", methods=["GET"])
def articles_by_coverage(coverage):
    pipeline = [
        {
            "$match": {
                "classes": {
                    "$elemMatch": {
                        "key": "class5",  # Key for coverage in your data
                        "value": coverage,
                    }
                }
            }
        },
        {"$project": {"_id": 0, "title": 1}},
    ]
    result = list(collection.aggregate(pipeline))
    json_result = json.dumps(result, ensure_ascii=False, indent=4)
    return Response(json_result, content_type="application/json; charset=utf-8"), 200


# Route for getting popular keywords in the last x days
@app.route("/popular_keywords_last_<int:x>_days", methods=["GET"])
def popular_keywords_last_X_days(x):
    # Ensure x is an integer and handle the case where it might not be
    try:
        days = int(x)
    except ValueError:
        return Response(
            json.dumps(
                {"error": "Invalid number of days"}, ensure_ascii=False, indent=4
            ),
            content_type="application/json; charset=utf-8",
            status=400,
        )

    pipeline = [
        {
            "$match": {
                "published_time": {
                    "$gte": datetime.datetime.now() - datetime.timedelta(days=days)
                }
            }
        },
        {"$unwind": "$keywords"},
        {"$group": {"_id": "$keywords", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 10},
    ]

    result = list(collection.aggregate(pipeline))
    json_result = json.dumps(result, ensure_ascii=False, indent=4)
    return Response(json_result, content_type="application/json; charset=utf-8"), 200


# Route for getting articles by published month
@app.route("/articles_by_month/<year>/<month>", methods=["GET"])
def articles_by_month(year, month):
    if len(month) == 1:
        month = "0" + month
    pipeline = [
        {"$match": {"published_time": {"$regex": "^" + year + "-" + month}}},
        {"$group": {"_id": None, "count": {"$sum": 1}}},
        {"$project": {"_id": 0, "month": month, "year": year, "count": 1}},
    ]
    result = list(collection.aggregate(pipeline))
    json_result = json.dumps(result, ensure_ascii=False, indent=4)
    return Response(json_result, content_type="application/json; charset=utf-8"), 200


# Route for getting articles by word count range
@app.route("/articles_by_word_count_range/<int:min>/<int:max>", methods=["GET"])
def articles_by_word_count_range(min, max):
    pipeline = [
        {"$addFields": {"word_count_int": {"$toInt": "$word_count"}}},
        {"$match": {"word_count_int": {"$gte": min, "$lte": max}}},
        {
            "$project": {
                "word_count_int": 0  # Exclude the word_count_int field from the output
            }
        },
        {"$sort": {"word_count": -1}},
    ]
    result = list(collection.aggregate(pipeline))
    for doc in result:
        doc["_id"] = str(doc["_id"])
    json_result = json.dumps(result, ensure_ascii=False, indent=4)
    return Response(json_result, content_type="application/json; charset=utf-8"), 200


# Route for getting articles with specific keyword count
@app.route("/articles_with_specific_keyword_count/<int:count>", methods=["GET"])
def articles_with_specific_keyword_count(count):
    pipeline = [
        {"$project": {"_id": 0, "title": 1, "keyword_count": {"$size": "$keywords"}}},
        {"$match": {"keyword_count": count}},
    ]
    result = list(collection.aggregate(pipeline))
    json_result = json.dumps(result, ensure_ascii=False, indent=4)
    return Response(json_result, content_type="application/json; charset=utf-8"), 200


# Route for getting articles by specific date
@app.route("/articles_by_specific_date/<date>", methods=["GET"])
def articles_by_specific_date(date):
    pipeline = [
        {"$match": {"published_time": {"$regex": "^" + date}}},
        {"$project": {"_id": 0, "title": 1}},
    ]
    result = list(collection.aggregate(pipeline))
    json_result = json.dumps(result, ensure_ascii=False, indent=4)
    return Response(json_result, content_type="application/json; charset=utf-8"), 200


# Route for getting articles containing specific text
@app.route("/articles_containing_text/<text>", methods=["GET"])
def articles_containing_text(text):
    pipeline = [
        {"$match": {"description": {"$regex": text, "$options": "i"}}},
        {"$project": {"_id": 0, "post_id": 1, "title": 1, "url": 1}},
    ]
    result = list(collection.aggregate(pipeline))
    json_result = json.dumps(result, ensure_ascii=False, indent=4)
    return Response(json_result, content_type="application/json; charset=utf-8"), 200


# Route for getting articles with more than N words
@app.route("/articles_with_more_than/<int:word_count>", methods=["GET"])
def articles_with_more_than(word_count):
    pipeline = [
        {"$match": {"word_count": {"$gt": word_count}}},
        {"$project": {"_id": 0, "title": 1, "word_count": 1}},
        {"$sort": {"word_count": -1}},
    ]
    result = list(collection.aggregate(pipeline))
    json_result = json.dumps(result, ensure_ascii=False, indent=4)
    return Response(json_result, content_type="application/json; charset=utf-8"), 200


# Route for getting articles grouped by coverage
@app.route("/articles_grouped_by_coverage", methods=["GET"])
def articles_grouped_by_coverage():
    pipeline = [
        {"$unwind": "$classes"},
        {"$group": {"_id": "$classes", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
    ]
    result = list(collection.aggregate(pipeline))
    json_result = json.dumps(result, ensure_ascii=False, indent=4)
    return Response(json_result, content_type="application/json; charset=utf-8"), 200


# Route for getting articles published in last x hours
@app.route("/articles_last_<int:x>_hours", methods=["GET"])
def articles_last_x_hours(x):
    pipeline = [
        {
            "$match": {
                "published_time": {
                    "$gte": datetime.datetime.now() - datetime.timedelta(hours=x)
                }
            }
        },
        {"$project": {"_id": 0, "title": 1, "published_time": 1, "post_id": 1}},
    ]
    result = list(collection.aggregate(pipeline))
    json_result = json.dumps(result, ensure_ascii=False, indent=4)
    return Response(json_result, content_type="application/json; charset=utf-8"), 200


# Route for getting articles by length of title
@app.route("/articles_by_title_length", methods=["GET"])
def articles_by_title_length():
    pipeline = [
        {
            "$project": {
                "_id": 0,
                "title": 1,
                "title_length": {"$size": {"$split": ["$title", " "]}},
            }
        },
        {"$group": {"_id": "$title_length", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
    ]
    result = list(collection.aggregate(pipeline))
    json_result = json.dumps(result, ensure_ascii=False, indent=4)
    return Response(json_result, content_type="application/json; charset=utf-8"), 200


# Route for getting most updated articles
@app.route("/most_updated_articles", methods=["GET"])
def most_updated_articles():
    pipeline = [
        {
            "$addFields": {
                "update_count": {
                    "$cond": {
                        "if": {"$ne": ["$published_time", "$last_updated"]},
                        "then": 1,
                        "else": 0,
                    }
                }
            }
        },
        {"$sort": {"update_count": -1, "last_updated": -1}},
        {
            "$project": {
                "_id": 0,
                "title": 1,
                "published_time": 1,
                "last_updated": 1,
                "update_count": 1,
            }
        },
    ]
    result = list(collection.aggregate(pipeline))
    json_result = json.dumps(result, ensure_ascii=False, indent=4)
    return Response(json_result, content_type="application/json; charset=utf-8"), 200


if __name__ == "__main__":
    app.run(debug=True)
