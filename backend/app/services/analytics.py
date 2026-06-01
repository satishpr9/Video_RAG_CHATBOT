def engagement_rate(
    likes,
    comments,
    views
):

    if not views:
        return "unavailable"

    return round(
        ((likes + comments) / views) * 100,
        2
    )