from app.services.analytics import engagement_rate

rate = engagement_rate(
    likes=1000,
    comments=200,
    views=10000
)

print(rate)