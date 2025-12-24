import pandas as pd
import os
import re
import numpy as np

# 1. 설정
base_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(base_dir, "data")
input_file = "dataset_manual_cleaned.csv"  # 수동 정리한 파일

# 2. 데이터 로드
file_path = os.path.join(data_dir, input_file)
if not os.path.exists(file_path):
    print(f"오류: {input_file} 파일이 없습니다.")
    exit()

df = pd.read_csv(file_path)
print(f"수동 정제 데이터 개수: {len(df)}")

# 결측치 처리
df["title"] = df["title"].fillna("")
df["content"] = df["content"].fillna("")
df["source"] = df["source"].fillna("Unknown")

# 날짜순 정렬 (시계열 분할을 위해 필수)
df = df.sort_values(by="date").reset_index(drop=True)


# =======================================================
# [1단계] 고급 텍스트 전처리 (Cleaning)
# =======================================================
def advanced_clean(text):
    if not isinstance(text, str):
        return ""

    # 1. 학과 사무실 인사말 제거 (패턴 수정됨)
    text = re.sub(
        r"안녕하세요.*?Language\s*&?\s*AI.*?사무실입니다\.?",
        "",
        text,
        flags=re.IGNORECASE,
    )

    # 2. 전화번호 제거
    text = re.sub(r"\d{2,3}[.-]?\d{3,4}[.-]?\d{4}", "", text)

    # 3. 이메일 제거
    text = re.sub(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", "", text)

    # 4. URL 제거
    text = re.sub(r"http[s]?://\S+", "", text)

    # 5. 시스템 문구 제거
    text = re.sub(r"첨부파일\s*영역", "", text)
    text = re.sub(r"첨부파일\s*미리보기", "", text)

    # 6. 연도 4자리 숫자 제거
    text = re.sub(r"202\d", "", text)

    # 7. 공백 정리
    text = re.sub(r"\s+", " ", text).strip()

    return text


print(">>> 텍스트 전처리(Cleaning) 수행 중...")
df["content"] = df["content"].apply(advanced_clean)
df["title"] = df["title"].apply(advanced_clean)

# =======================================================
# [2단계] Stratified Time-Series Split (소스별 시계열 분할)
# =======================================================
train_list = []
val_list = []
test_list = []

sources = df["source"].unique()
print(f"\n>>> 소스별 시계열 분할 시작: {sources}")

for source in sources:
    # 해당 소스 데이터만 추출
    group = df[df["source"] == source].copy()

    # 날짜 정렬 (중요)
    group = group.sort_values(by="date").reset_index(drop=True)

    total_len = len(group)
    if total_len == 0:
        continue

    # 8:1:1 분할
    train_end = int(total_len * 0.8)
    val_end = int(total_len * 0.9)

    # 자르기
    t_train = group.iloc[:train_end]
    t_val = group.iloc[train_end:val_end]
    t_test = group.iloc[val_end:]

    train_list.append(t_train)
    val_list.append(t_val)
    test_list.append(t_test)

    print(
        f"[{source}] Total: {total_len} -> {len(t_train)} / {len(t_val)} / {len(t_test)}"
    )

# 병합
final_train = pd.concat(train_list, ignore_index=True)
final_val = pd.concat(val_list, ignore_index=True)
final_test = pd.concat(test_list, ignore_index=True)

# Train/Val은 셔플 (학습 효율 위해), Test는 시계열 순서 유지 (분석 위해)
final_train = final_train.sample(frac=1, random_state=42).reset_index(drop=True)
final_val = final_val.sample(frac=1, random_state=42).reset_index(drop=True)

print(f"\n>>> 최종 데이터셋 개수")
print(f"Train: {len(final_train)}")
print(f"Val  : {len(final_val)}")
print(f"Test : {len(final_test)}")

# =======================================================
# [3단계] 학습에 필요한 핵심 컬럼만 남김
# =======================================================
target_cols = ["label_relevance", "label_importance", "title", "content"]

final_train = final_train[target_cols]
final_val = final_val[target_cols]
final_test = final_test[target_cols]

final_train.to_csv(
    os.path.join(data_dir, "train.csv"), index=False, encoding="utf-8-sig"
)
final_val.to_csv(os.path.join(data_dir, "val.csv"), index=False, encoding="utf-8-sig")
final_test.to_csv(os.path.join(data_dir, "test.csv"), index=False, encoding="utf-8-sig")

print(">>> 모든 파일 저장 완료! (train.csv, val.csv, test.csv)")
