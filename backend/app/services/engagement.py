def calculate_engagement(metadata):

    views = metadata.get("views", 0)
    likes = metadata.get("likes", 0)
    comments = metadata.get("comments", 0)

    if views == 0:
        return 0

    return round(
        ((likes + comments) / views) * 100,
        2
    )