def extract_metadata(info):

    return {
        "title": info.get("title"),
        "creator": info.get("uploader"),
        "views": info.get("view_count", 0),
        "likes": info.get("like_count", 0),
        "comments": info.get("comment_count", 0),
        "duration": info.get("duration", 0),
        "upload_date": info.get("upload_date"),
        "hashtags": info.get("tags", [])
    }