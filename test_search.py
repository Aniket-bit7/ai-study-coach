from services.search_service import search_courses

results = search_courses(
    weak_areas=["Low Engagement"],
    difficulty="Easy",
    subject="Machine Learning",
    intent="resources"
)

for r in results:
    print("\n----------------------")
    print("TITLE:", r["title"])
    print("LINK:", r["link"])
    print("THUMBNAIL:", r["thumbnail"])