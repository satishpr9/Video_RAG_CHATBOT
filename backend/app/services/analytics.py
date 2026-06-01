def engagement_rate(
    likes,
    comments,
    views
):

    if not views:
        return None

    return round(
        ((likes + comments) / views) * 100,
        2
    )