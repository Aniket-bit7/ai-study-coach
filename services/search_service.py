from serpapi import GoogleSearch
from agent.config import SERPAPI_KEY


def search_courses(weak_areas, difficulty, subject, intent=None):
    recommendations = []

    # Query
    if intent == "resources":
        query = f"{subject} tutorial video"
    else:
        query = f"{subject} course tutorial"

    params = {
        "q": query,
        "engine": "google",
        "api_key": SERPAPI_KEY
    }

    search = GoogleSearch(params)
    results = search.get_dict()

    print("🔍 RAW RESULTS:", results)

    # 1. PRIORITY → VIDEOS (BEST PART)
    videos = results.get("inline_videos", [])

    for vid in videos[:5]:
        recommendations.append({
            "title": vid.get("title"),
            "link": vid.get("link"),
            "thumbnail": vid.get("thumbnail"),
            "type": "video"
        })

    # 2. FALLBACK → COURSES / WEBSITES
    if not recommendations:
        for result in results.get("organic_results", [])[:5]:
            recommendations.append({
                "title": result.get("title"),
                "link": result.get("link"),
                "thumbnail": result.get("thumbnail"),
                "type": "course"
            })

    return recommendations