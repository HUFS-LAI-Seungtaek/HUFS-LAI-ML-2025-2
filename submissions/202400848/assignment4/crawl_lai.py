import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
import os
import re
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

BASE_URL = "https://langai.hufs.ac.kr"
TARGETS = [
    {
        "name": "LAI_공지",
        "url": "https://langai.hufs.ac.kr/langai/m05_s01.do",
        "pages": 23,
    },
    {
        "name": "LAI_소식",
        "url": "https://langai.hufs.ac.kr/langai/m05_s02.do",
        "pages": 1,
    },
]

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}


def clean_text(text):
    if not text:
        return ""
    text = re.sub(r"\s+", " ", str(text))
    return text.strip()


def crawl_lai_full():
    all_data = []

    for target in TARGETS:
        print(f"\n=== [{target['name']}] 목록 수집 시작 ===")
        for page in range(1, target["pages"] + 1):
            try:
                params = {"page": page}
                response = requests.get(
                    target["url"],
                    headers=headers,
                    params=params,
                    verify=False,
                    timeout=15,
                )
                response.encoding = "utf-8"

                try:
                    soup = BeautifulSoup(response.text, "lxml")
                except:
                    soup = BeautifulSoup(response.text, "html.parser")

                rows = soup.select("table tbody tr")

                for row in rows:
                    try:
                        title_td = row.select_one("td.td-subject")
                        if not title_td:
                            tds = row.select("td")
                            if len(tds) > 1:
                                title_td = tds[1]

                        if not title_td:
                            continue

                        title = clean_text(title_td.text)
                        link_tag = title_td.select_one("a")
                        link = link_tag["href"] if link_tag else ""
                        if link and not link.startswith("http"):
                            link = BASE_URL + link

                        tds = row.select("td")
                        date_td = row.select_one("td.td-date")
                        date_raw = (
                            date_td.text.strip()
                            if date_td
                            else (tds[3].text.strip() if len(tds) >= 4 else "날짜없음")
                        )
                        date = clean_text(date_raw)

                        all_data.append(
                            {
                                "source": target["name"],
                                "title": title,
                                "date": date,
                                "link": link,
                                "content": "",
                            }
                        )
                    except:
                        continue

                print(f"{page}페이지 완료... (누적 {len(all_data)}개)")
                time.sleep(random.uniform(1, 2))
            except Exception as e:
                print(f"접속 에러: {e}")

    print("\n=== 본문 상세 크롤링 시작 ===")
    for idx, item in enumerate(all_data):
        link = item["link"]
        if not link:
            continue
        try:
            response = requests.get(link, headers=headers, verify=False, timeout=15)
            response.encoding = "utf-8"

            try:
                soup = BeautifulSoup(response.text, "lxml")
            except:
                soup = BeautifulSoup(response.text, "html.parser")

            content_tag = soup.select_one("div.view-con")
            if not content_tag:
                content_tag = soup.select_one(".td-content")

            if content_tag:
                content = clean_text(content_tag.text)
            else:
                content = "본문 추출 실패"

            item["content"] = content
            if (idx + 1) % 10 == 0:
                print(f"{idx + 1}번째 본문 처리 중...")
            time.sleep(random.uniform(2, 3))
        except:
            continue

    return pd.DataFrame(all_data)


if __name__ == "__main__":
    df = crawl_lai_full()

    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(current_dir, "data")

    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    save_path = os.path.join(data_dir, "lai_notice.csv")

    df.to_csv(save_path, index=False, encoding="utf-8-sig")
    print(f"저장 완료: {save_path}")
