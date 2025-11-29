import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
import os
import re
import urllib3

# SSL 경고 무시
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# =======================================================
# 1. 설정
# =======================================================
urls = {
    "공지(일반)": "https://www.hufs.ac.kr/hufs/11281/subview.do",
    "학사": "https://www.hufs.ac.kr/hufs/11282/subview.do",
    "장학": "https://www.hufs.ac.kr/hufs/11283/subview.do",
}

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Referer": "https://www.hufs.ac.kr/",
}


def clean_text(text):
    if not text:
        return ""
    text = re.sub(r"\s+", " ", str(text))
    return text.strip()


def crawl_hufs_list(category_name, base_url, pages=3):
    print(f"=== [{category_name}] 목록 수집 시작 ===")
    data_list = []

    for page in range(1, pages + 1):
        try:
            target_url = f"{base_url}?page={page}"
            # [핵심] verify=False, timeout, lxml 적용
            response = requests.get(
                target_url, headers=headers, verify=False, timeout=15
            )
            response.encoding = "utf-8"

            try:
                soup = BeautifulSoup(response.text, "lxml")
            except:
                soup = BeautifulSoup(response.text, "html.parser")

            rows = soup.select("table tbody tr")

            for row in rows:
                try:
                    title_tag = row.select_one(".td-subject span strong")
                    if not title_tag:
                        title_tag = row.select_one(".td-subject")

                    title = clean_text(title_tag.text) if title_tag else "제목 없음"

                    date_tag = row.select_one(".td-date")
                    date = clean_text(date_tag.text) if date_tag else "날짜 없음"

                    link_tag = row.select_one(".td-subject a")
                    link = link_tag["href"] if link_tag else ""
                    if link and not link.startswith("http"):
                        link = "https://www.hufs.ac.kr" + link

                    data_list.append(
                        {
                            "category": category_name,
                            "title": title,
                            "date": date,
                            "link": link,
                            "content": "",
                        }
                    )

                except Exception:
                    continue

            print(f"{page}페이지 완료... (누적 {len(data_list)}개)")
            time.sleep(random.uniform(1, 2))

        except Exception as e:
            print(f"에러 발생: {e}")

    return data_list


if __name__ == "__main__":
    all_data = []

    # 1. 목록 수집
    for name, url in urls.items():
        data = crawl_hufs_list(name, url, pages=52)
        all_data.extend(data)

    print(f"\n>>> 총 {len(all_data)}개의 목록 수집 완료. 본문 크롤링 시작...")

    # 2. 본문 수집
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
                print(f"{idx + 1}번째 본문 수집 중...")

            time.sleep(random.uniform(2, 3))

        except Exception as e:
            print(f"본문 에러: {e}")

    # 3. 저장
    df = pd.DataFrame(all_data)

    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(current_dir, "data")

    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    save_path = os.path.join(data_dir, "hufs_main.csv")

    df.to_csv(save_path, index=False, encoding="utf-8-sig")
    print(f"저장 완료: {save_path}")
