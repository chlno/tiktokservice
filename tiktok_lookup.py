import aiohttp

from bs4 import BeautifulSoup

class tiktokservice:
    def __init__(self, bot) -> bool:
        self.bot = bot

    async def tik(self, username):
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://www.tiktok.com/@{username}") as r:
                if r.status != 200:
                    return None
                content = await r.text()
                soup = BeautifulSoup(content, "html.parser")

                full_title = soup.find("meta", property="og:title")
                if not full_title:
                    return None

                user = full_title["content"].split("(@")
                if len(user) < 2:
                    return None

                description = soup.find("meta", property="og:description")
                if not description:
                    return None

                start = description["content"].find("Followers. ")
                end = description["content"].find(".Watch", start + len("Followers. "))
                if start != -1 and end != -1:
                    desc = description["content"][start + len("Followers. "):end].strip()
                else:
                    desc = "No bio"

                avatar_url = soup.find("meta", property="og:image")
                if not avatar_url:
                    return None

                avatar_url = avatar_url["content"]
                verified = bool(soup.find("circle", {"fill": "#20D5EC"}))
                likes = soup.find(title="Likes")
                followers = soup.find(title="Followers")
                following = soup.find(title="Following")

                likes = likes.text if likes else "N/A"
                followers = followers.text if followers else "N/A"
                following = following.text if following else "N/A"

                profile = {
                    'name': user[1].split(")")[0],
                    'display': user[0].strip(),
                    'description': desc,
                    'url': f"https://www.tiktok.com/@{username}",
                    'likes': likes,
                    'followers': followers, 
                    'following': following,  
                    'avatar': avatar_url,
                    'verified': verified
                }
                return profile
