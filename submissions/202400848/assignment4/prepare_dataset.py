import pandas as pd
import os

# 1. 데이터 경로 설정
base_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(base_dir, "data")

# 읽어올 파일 리스트
files = ["hufs_main.csv", "iel_notice.csv", "lai_notice.csv"]
dfs = []

print("=== 데이터 병합 및 중복 제거 시작 ===")

# 2. 파일 읽기
for f in files:
    path = os.path.join(data_dir, f)
    if os.path.exists(path):
        df = pd.read_csv(path)
        print(f"[{f}] 로드 됨: {len(df)}개")
        dfs.append(df)
    else:
        print(f"!! 파일 없음: {f}")

# 3. 하나로 합치기
if not dfs:
    print("데이터가 하나도 없습니다.")
    exit()

full_df = pd.concat(dfs, ignore_index=True)
print(f">> 전체 데이터 개수 (중복 포함): {len(full_df)}개")

# =======================================================
# [핵심] 중복 제거 (고정 공지 해결)
# =======================================================
# 제목(title)과 날짜(date)가 완전히 같으면 중복으로 간주하고 제거한다.
# keep='first': 중복된 것 중 맨 위에꺼 하나만 남기고 나머지는 버림.
full_df.drop_duplicates(subset=["title", "date"], keep="first", inplace=True)

# 혹시 링크(link)가 같은 것도 제거 (이중 안전장치)
full_df.drop_duplicates(subset=["link"], keep="first", inplace=True)

print(f">> 중복 제거 후 데이터 개수: {len(full_df)}개 (살아남은 데이터)")

# =======================================================
# 4. 라벨링용 빈 칸 만들기
# =======================================================
full_df["label_relevance"] = ""  # 0 or 1
full_df["label_importance"] = ""  # 0, 1, 2

# 컬럼 순서 예쁘게 정리
cols = [
    "label_relevance",
    "label_importance",
    "title",
    "content",
    "date",
    "link",
    "category",
    "source",
]
# 실제 데이터에 없는 컬럼이 있을 수 있으니 교집합만 선택
existing_cols = [c for c in cols if c in full_df.columns]
full_df = full_df[existing_cols]

# 5. 저장
save_path = os.path.join(data_dir, "dataset_for_labeling.csv")
full_df.to_csv(save_path, index=False, encoding="utf-8-sig")

print(f"\n완료! 라벨링용 파일이 생성되었습니다: {save_path}")
print("이제 이 파일을 열어서 중복 없이 깔끔한 데이터에 라벨링을 시작하세요.")
