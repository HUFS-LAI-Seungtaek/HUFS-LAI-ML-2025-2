# Markdown 사용법 가이드

Markdown은 간단한 문법으로 문서를 작성할 수 있는 마크업 언어입니다. GitHub을 포함한 많은 플랫폼에서 사용되며, 배우기 쉽고 읽기 편합니다.

---

## 목차
1. [제목 (Headings)](#1-제목-headings)
2. [강조 (Emphasis)](#2-강조-emphasis)
3. [리스트 (Lists)](#3-리스트-lists)
4. [링크 (Links)](#4-링크-links)
5. [이미지 (Images)](#5-이미지-images)
6. [코드 (Code)](#6-코드-code)
7. [표 (Tables)](#7-표-tables)
8. [인용구 (Blockquotes)](#8-인용구-blockquotes)
9. [수평선 (Horizontal Rule)](#9-수평선-horizontal-rule)
10. [체크리스트 (Task Lists)](#10-체크리스트-task-lists)

---

## 1. 제목 (Headings)

`#` 기호를 사용하여 제목을 만듭니다. `#`의 개수가 제목의 레벨을 결정합니다.

```markdown
# H1 제목 (가장 큰 제목)
## H2 제목
### H3 제목
#### H4 제목
##### H5 제목
###### H6 제목 (가장 작은 제목)
```

### 결과:

# H1 제목 (가장 큰 제목)
## H2 제목
### H3 제목

**팁**: 제목 레벨을 건너뛰지 말고 순차적으로 사용하세요 (예: H1 → H2 → H3)

---

## 2. 강조 (Emphasis)

텍스트를 강조하려면 `*` 또는 `_` 기호를 사용합니다.

```markdown
*이탤릭체* 또는 _이탤릭체_
**볼드체** 또는 __볼드체__
***볼드 + 이탤릭*** 또는 ___볼드 + 이탤릭___
~~취소선~~
```

### 결과:

*이탤릭체* 또는 _이탤릭체_
**볼드체** 또는 __볼드체__
***볼드 + 이탤릭*** 또는 ___볼드 + 이탤릭___
~~취소선~~

---

## 3. 리스트 (Lists)

### 3.1 순서 없는 리스트 (Unordered List)

`-`, `*`, `+` 기호를 사용합니다.

```markdown
- 항목 1
- 항목 2
  - 하위 항목 2-1
  - 하위 항목 2-2
- 항목 3
```

### 결과:

- 항목 1
- 항목 2
  - 하위 항목 2-1
  - 하위 항목 2-2
- 항목 3

### 3.2 순서 있는 리스트 (Ordered List)

숫자와 `.`을 사용합니다.

```markdown
1. 첫 번째 항목
2. 두 번째 항목
   1. 하위 항목 2-1
   2. 하위 항목 2-2
3. 세 번째 항목
```

### 결과:

1. 첫 번째 항목
2. 두 번째 항목
   1. 하위 항목 2-1
   2. 하위 항목 2-2
3. 세 번째 항목

---

## 4. 링크 (Links)

```markdown
[링크 텍스트](URL)
[Google](https://www.google.com)
[상대 경로 링크](./other-file.md)
```

### 결과:

[Google](https://www.google.com)

**팁**: 같은 레포지토리 내 파일을 링크할 때는 상대 경로를 사용하세요.

---

## 5. 이미지 (Images)

링크 문법 앞에 `!`를 추가합니다.

```markdown
![대체 텍스트](이미지 URL)
![예시 이미지](https://via.placeholder.com/150)
```

### 결과:

![예시 이미지](https://via.placeholder.com/150)

**팁**: GitHub에 이미지를 업로드하려면:
1. 이슈나 PR에서 이미지를 드래그 앤 드롭
2. 생성된 URL을 복사하여 사용

---

## 6. 코드 (Code)

### 6.1 인라인 코드 (Inline Code)

백틱(`` ` ``)으로 감쌉니다.

```markdown
`코드` 또는 `변수명`을 강조할 수 있습니다.
```

### 결과:

`코드` 또는 `변수명`을 강조할 수 있습니다.

### 6.2 코드 블록 (Code Block)

세 개의 백틱(` ``` `)으로 감싸고, 언어를 명시하면 문법 강조가 적용됩니다.

````markdown
```python
def hello_world():
    print("Hello, World!")
```
````

### 결과:

```python
def hello_world():
    print("Hello, World!")
```

**지원하는 언어**: `python`, `javascript`, `java`, `c`, `cpp`, `bash`, `json`, `markdown` 등

---

## 7. 표 (Tables)

파이프(`|`)와 하이픈(`-`)을 사용하여 표를 만듭니다.

```markdown
| 항목 | 설명 | 가격 |
|------|------|------|
| 사과 | 빨간 과일 | 1000원 |
| 바나나 | 노란 과일 | 1500원 |
```

### 결과:

| 항목 | 설명 | 가격 |
|------|------|------|
| 사과 | 빨간 과일 | 1000원 |
| 바나나 | 노란 과일 | 1500원 |

### 정렬 옵션:

```markdown
| 왼쪽 정렬 | 가운데 정렬 | 오른쪽 정렬 |
|:----------|:----------:|----------:|
| 텍스트 | 텍스트 | 텍스트 |
```

---

## 8. 인용구 (Blockquotes)

`>` 기호를 사용합니다.

```markdown
> 이것은 인용구입니다.
> 여러 줄로 작성할 수 있습니다.
>
> > 중첩된 인용구도 가능합니다.
```

### 결과:

> 이것은 인용구입니다.
> 여러 줄로 작성할 수 있습니다.
>
> > 중첩된 인용구도 가능합니다.

---

## 9. 수평선 (Horizontal Rule)

`---`, `***`, `___` 중 하나를 사용합니다.

```markdown
---
```

### 결과:

---

---

## 10. 체크리스트 (Task Lists)

GitHub에서 사용 가능한 체크리스트입니다.

```markdown
- [ ] 완료되지 않은 작업
- [x] 완료된 작업
- [ ] 또 다른 작업
```

### 결과:

- [ ] 완료되지 않은 작업
- [x] 완료된 작업
- [ ] 또 다른 작업

---

## 프로젝트 제안서 작성 팁

### 1. 구조화된 문서 작성

```markdown
# 프로젝트 제안서: AI 기반 번역 봇

## 1. 프로젝트 개요

### 1.1 프로젝트명
- 한글: AI 번역 봇
- 영문: AI Translation Bot

### 1.2 프로젝트 설명
LLM을 활용하여 고품질 번역을 제공하는 디스코드 봇입니다.
```

### 2. 코드와 파일명 강조

```markdown
`proposal.md` 파일을 작성하여 제출하세요.

사용할 라이브러리:
- `discord.py`: 디스코드 봇 개발
- `openai`: LLM API 호출
```

### 3. 리스트로 정보 정리

```markdown
## 핵심 기능
1. 실시간 번역
2. 다국어 지원
3. 번역 히스토리 저장

## 기술 스택
- **언어**: Python 3.10+
- **프레임워크**: Discord.py
- **API**: OpenAI GPT-4
```

### 4. 표로 비교/정리

```markdown
| 모델 | 속도 | 정확도 | 비용 |
|------|------|--------|------|
| GPT-4 | 보통 | 높음 | 높음 |
| GPT-3.5 | 빠름 | 중간 | 낮음 |
```

---

## 추가 리소스

### 공식 가이드
- [GitHub Markdown 가이드](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax)
- [Markdown Guide](https://www.markdownguide.org/)

### 연습 도구
- [Markdown Live Preview](https://markdownlivepreview.com/)
- [Dillinger](https://dillinger.io/)

### VS Code 확장
- Markdown All in One
- Markdown Preview Enhanced

---

## 자주 하는 실수

### 1. 제목 뒤 공백 없음
```markdown
❌ #제목
✅ # 제목
```

### 2. 리스트 들여쓰기
```markdown
❌
- 항목 1
  - 하위 항목 (들여쓰기가 부족함)

✅
- 항목 1
  - 하위 항목 (공백 2개)
```

### 3. 코드 블록 언어 명시
````markdown
❌
```
def hello():
    pass
```

✅
```python
def hello():
    pass
```
````

### 4. 표 형식 불일치
```markdown
❌
| 제목 1 | 제목 2
|------|------
| 내용 1 | 내용 2 |

✅
| 제목 1 | 제목 2 |
|--------|--------|
| 내용 1 | 내용 2 |
```

---

## 마무리

Markdown은 배우기 쉽지만 강력한 도구입니다. 이 가이드의 기본 문법만 익혀도 훌륭한 문서를 작성할 수 있습니다.

**꼭 기억하세요**:
- 제목은 계층 구조를 명확히
- 코드와 파일명은 백틱으로 강조
- 리스트로 정보를 정리
- 표로 비교 데이터 정리

Happy Writing! 📝
