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
BASE_URL = "https://iel.hufs.ac.kr"
TARGETS = [
    {"name": "IEL_공지", "url": "https://iel.hufs.ac.kr/iel/m05_s01.do", "pages": 23},
    {"name": "IEL_자유", "url": "https://iel.hufs.ac.kr/iel/m05_s03.do", "pages": 8},
]

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}


def clean_text(text):
    """
    줄바꿈, 탭 등 모든 공백을 스페이스 하나로 치환하여 한 줄로 만듦
    """
    if not text:
        return ""
    # \s+ 는 줄바꿈, 탭, 공백 등을 모두 포함함
    text = re.sub(r"\s+", " ", str(text))
    return text.strip()


def crawl_iel_full():
    all_data = []

    # ---------------------------------------------------
    # 단계 1: 목록(List) 수집
    # ---------------------------------------------------
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
                response.encoding = "utf-8"  # 인코딩 고정

                soup = BeautifulSoup(response.text, "lxml")  # lxml 파서 사용
                rows = soup.select("table.board-table tbody tr")

                for row in rows:
                    try:
                        title_td = row.select_one("td.td-subject")
                        if not title_td:
                            tds = row.select("td")
                            if len(tds) > 1:
                                title_td = tds[1]

                        if not title_td:
                            continue

                        # [핵심 수정] 제목에도 clean_text 적용!
                        title = clean_text(title_td.text)

                        link_tag = title_td.select_one("a")
                        link = link_tag["href"] if link_tag else ""
                        if link and not link.startswith("http"):
                            link = BASE_URL + link

                        tds = row.select("td")
                        date_raw = tds[3].text.strip() if len(tds) > 3 else "날짜없음"

                        # [핵심 수정] 날짜에도 clean_text 적용
                        date = clean_text(date_raw)

                        all_data.append(
                            {
                                "source": target["name"],
                                "title": title,
                                "date": date,
                                "link": link,
                                "content": "",  # 본문은 아래에서 채움
                            }
                        )
                    except:
                        continue

                print(f"{page}페이지 완료... (누적 {len(all_data)}개)")
                time.sleep(random.uniform(1, 2))

            except Exception as e:
                print(f"페이지 접속 에러: {e}")

    # ---------------------------------------------------
    # 단계 2: 본문(Content) 상세 수집
    # ---------------------------------------------------
    print("\n=== 본문 상세 크롤링 시작 ===")

    for idx, item in enumerate(all_data):
        link = item["link"]
        if not link:
            continue
        try:
            response = requests.get(link, headers=headers, verify=False, timeout=15)
            response.encoding = "utf-8"

            soup = BeautifulSoup(response.text, "lxml")

            content_tag = soup.select_one("div.view-con")
            if not content_tag:
                content_tag = soup.select_one(".td-content")

            if content_tag:
                # [기존 유지] 본문 clean_text 적용
                content = clean_text(content_tag.text)
            else:
                content = "본문 추출 실패"

            item["content"] = content

            if (idx + 1) % 10 == 0:
                print(f"{idx + 1}번째 본문 처리 중...")
            time.sleep(random.uniform(2, 3))

        except Exception as e:
            # print(f"본문 에러: {e}")
            item["content"] = "에러"
            continue

    return pd.DataFrame(all_data)


if __name__ == "__main__":
    df = crawl_iel_full()

    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(current_dir, "data")

    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    save_path = os.path.join(data_dir, "iel_notice.csv")

    df.to_csv(save_path, index=False, encoding="utf-8-sig")
    print(f"저장 완료: {save_path}")
