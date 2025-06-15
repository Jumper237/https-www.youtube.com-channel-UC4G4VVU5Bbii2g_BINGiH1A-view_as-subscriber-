
import asyncio, httpx, json
from parsel import Selector

async def scrape_profile(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Accept-Language": "en-US,en;q=0.9"
    }
    async with httpx.AsyncClient(http2=True, headers=headers) as client:
        resp = await client.get(url)
        resp.raise_for_status()
        selector = Selector(resp.text)
        script = selector.xpath("//script[@id='__UNIVERSAL_DATA_FOR_REHYDRATION__']/text()").get()
        data = json.loads(script)
        user = data["__DEFAULT_SCOPE__"]["webapp.user-detail"]["userInfo"]
        stats = user["stats"]
        return {
            "uniqueId": user.get("uniqueId"),
            "nickname": user.get("nickname"),
            "bio": user.get("signature"),
            "followers": stats.get("followerCount"),
            "following": stats.get("followingCount"),
            "hearts": stats.get("heartCount"),
            "videoCount": stats.get("videoCount")
        }

async def main():
    url = "https://www.tiktok.com/@noor1171367491961"
    profile = await scrape_profile(url)
    print(json.dumps(profile, indent=2))

asyncio.run(main())
