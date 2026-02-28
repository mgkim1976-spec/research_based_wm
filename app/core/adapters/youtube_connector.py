import requests
import xml.etree.ElementTree as ET
from datetime import datetime
from app.models.resources import SmartMoneyVideo
from typing import List
import re

class SmartMoneyConnector:
    # We will use the RSS feed for the youtube channel.
    # To get the rss feed, we need the channel ID, not the handle.
    # @SmartMoney0 Channel ID: We will fetch it dynamically or hardcode it if known.
    # Let's dynamically find it or assume a known one for now. We can fetch the handle page to find it.
    
    YOUTUBE_HANDLE_URL = "https://www.youtube.com/@SmartMoney0"
    RSS_BASE_URL = "https://www.youtube.com/feeds/videos.xml?channel_id={}"
    
    def __init__(self):
        self.channel_id = None
        
    def _get_channel_id(self) -> str:
        if self.channel_id:
            return self.channel_id
            
        # Fetch channel page to extract channel_id
        res = requests.get(self.YOUTUBE_HANDLE_URL)
        res.raise_for_status()
        
        # Look for <meta itemprop="channelId" content="UC..."> or canonical URL
        match = re.search(r'<meta itemprop="channelId" content="([^"]+)">', res.text)
        if match:
            self.channel_id = match.group(1)
        else:
            match = re.search(r'"channelId":"([^"]+)"', res.text)
            if match:
                self.channel_id = match.group(1)
            else:
                raise ValueError("Could not find YouTube Channel ID from the handle URL.")
                
        return self.channel_id

    def fetch_recent_videos(self, limit: int = 10) -> List[SmartMoneyVideo]:
        """Fetches the most recent videos from SmartMoney YouTube channel via RSS."""
        channel_id = self._get_channel_id()
        rss_url = self.RSS_BASE_URL.format(channel_id)
        
        response = requests.get(rss_url)
        response.raise_for_status()
        
        root = ET.fromstring(response.content)
        
        # XML Namespaces used in YouTube RSS
        ns = {
            'atom': 'http://www.w3.org/2005/Atom',
            'yt': 'http://www.youtube.com/xml/schemas/2015',
            'media': 'http://search.yahoo.com/mrss/'
        }
        
        videos = []
        for entry in root.findall('atom:entry', ns)[:limit]:
            video_id = entry.find('yt:videoId', ns).text
            title = entry.find('atom:title', ns).text
            published_str = entry.find('atom:published', ns).text
            
            # 2026-02-27T10:00:00+00:00
            pub_date = datetime.fromisoformat(published_str.replace('Z', '+00:00'))
            
            link = entry.find('atom:link', ns).attrib['href']
            
            # Description is inside media:group -> media:description
            media_group = entry.find('media:group', ns)
            description = ""
            if media_group is not None:
                desc_elem = media_group.find('media:description', ns)
                if desc_elem is not None and desc_elem.text:
                    description = desc_elem.text
            
            # Simple heuristic for series name based on title
            series_name = "SmartMoney"
            if "EP." in title.upper() or "월스트리트파인더" in title:
                series_name = "Wall Street Finder"
            elif "시황" in title or "리뷰" in title:
                series_name = "Daily Market"
            
            video = SmartMoneyVideo(
                video_id=video_id,
                title=title,
                publish_date=pub_date,
                source_url=link,
                series_name=series_name,
                description=description
            )
            videos.append(video)
            
        return videos

if __name__ == "__main__":
    connector = SmartMoneyConnector()
    videos = connector.fetch_recent_videos(2)
    for v in videos:
        print(f"[{v.publish_date.strftime('%Y-%m-%d')}] {v.title} ({v.series_name})")
        print(f" URL: {v.source_url}")
