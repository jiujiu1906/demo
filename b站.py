
import requests
import re
import json
import subprocess
import os

# 尝试导入moviepy，如果失败则使用ffmpeg作为备选方案
try:
    from moviepy.editor import VideoFileClip, AudioFileClip
    USE_MOVIEPY = True
except ImportError:
    try:
        from moviepy import VideoFileClip, AudioFileClip
        USE_MOVIEPY = True
    except ImportError:
        USE_MOVIEPY = False
        print("警告: moviepy未安装，将尝试使用ffmpeg进行视频音频合并")

base_url = "https://www.bilibili.com/video/BV1KR8Cz8EfP/"
params = {
    "spm_id_from": "333.337.search-card.all.click",
    "vd_source": "64932cc25623f234f6e48e94b7b4dfec"
}

headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "cache-control": "max-age=0",
    "priority": "u=0, i",
    "referer": "https://search.bilibili.com/all?keyword=%E7%94%9C%E5%A6%B9&from_source=webtop_search&spm_id_from=333.40138&search_source=3",
    "sec-ch-ua": "\"Chromium\";v=\"148\", \"Microsoft Edge\";v=\"148\", \"Not/A)Brand\";v=\"99\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "same-origin",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36 Edg/148.0.0.0"
}

cookies = {
    "buvid3": "720D573E-69DB-C5C5-47EA-083FF5C6FBD432497infoc",
    "b_nut": "1759071032",
    "_uuid": "1EB488C1-9C53-2E92-DD97-773CBFCA3CD1033280infoc",
    "buvid_fp": "713cb1a5d4ec7c87181e171b68824c63",
    "enable_web_push": "DISABLE",
    "home_feed_column": "5",
    "buvid4": "ACEB418D-D02D-1434-B2ED-F31236B8431835658-025092822-JAwKGlV5GxqvAqhf61CjTBBpB284DLHlsMsukP6VrYxzc2XBAtBshbOJHSXKkwo6",
    "browser_resolution": "1707-846",
    "SESSDATA": "03e1e33f%2C1794379708%2Ce7fe4%2A52CjA0_qP5ZDAf2mseWGzJo-sICbI2efbbdqj7PVaP5YbQq6-hgLdGGMNHjwOqgsRtWjQSVlZvS2tYQWZsdzZMY1J1YldzQ3BXRno5NllUSDEzeW9tVkdicWszQ0RhYTZqUXdTVWF0aHhOQ1IwMm9yMi1rdnRpWXJYV2tkMUdadHRjTzcwcDV5a1ZBIIEC",
    "bili_jct": "0ba46ce5275b19bd86fe07932b809c28",
    "DedeUserID": "3706989999819155",
    "DedeUserID__ckMd5": "4ec421cf5eb3ca73",
    "theme-tip-show": "SHOWED",
    "bp_t_offset_3706989999819155": "1202544946859474944",
    "theme-avatar-tip-show": "SHOWED",
    "CURRENT_QUALITY": "0",
    "rpdid": "0zbfAGOKo7|MtcGiVUR|44q|3w1WnMmd",
    "bili_ticket": "eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NzkwODcwNDEsImlhdCI6MTc3ODgyNzc4MSwicGx0IjotMX0.hAbgaEHq45iHhXjxaHFv46de6deBXc7iueUHHr8kH1Y",
    "bili_ticket_expires": "1779086981",
    "bsource": "search_bing",
    "bmg_af_switch": "1",
    "bmg_src_def_domain": "i1.hdslb.com",
    "sid": "8gierb56",
    "CURRENT_FNVAL": "2000",
    "b_lsid": "6743D459_19E31191ADE"
}

response = requests.get(
    base_url,
    params=params,
    headers=headers,
    cookies=cookies
)

str_data = response.content.decode("utf-8")
# print(str_data)
pattern = re.findall(r'<script>window\.__playinfo__=(.*?)</script>', str_data)[0]
# 视频 数据
video_data = json.loads(pattern)["data"]["dash"]["video"][0]["baseUrl"]
# 音频
audio_url = json.loads(pattern)["data"]["dash"]["audio"][0]["baseUrl"]
# print(video_data)
# print(audio_url)
# 获取视频数据
video_content = requests.get(url=video_data, headers=headers, cookies=cookies).content
# 获取音频数据
audio_content = requests.get(url=audio_url, headers=headers, cookies=cookies).content
# 保存 数据
with open("audio.wav", "wb") as audio:
    audio.write(audio_content)
with open("video.mp4", "wb") as video:
    video.write(video_content)

print("视频和音频文件已下载完成")

# 视频音频合并
if USE_MOVIEPY:
    try:
        # 合并视频和音频
        video_clip = VideoFileClip("video.mp4")
        audio_clip = AudioFileClip("audio.wav")

        # 将音频添加到视频中 (兼容新旧版本moviepy)
        try:
            # 新版moviepy (2.x) 使用 with_audio
            final_clip = video_clip.with_audio(audio_clip)
        except AttributeError:
            # 旧版moviepy (1.x) 使用 set_audio
            final_clip = video_clip.set_audio(audio_clip)

        # 输出合并后的视频文件
        final_clip.write_videofile("output.mp4", codec='libx264', audio_codec='aac')

        # 关闭剪辑对象以释放资源
        video_clip.close()
        audio_clip.close()
        final_clip.close()

        print("视频和音频已成功合并为 output.mp4 (使用moviepy)")



