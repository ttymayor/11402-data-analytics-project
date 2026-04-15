# 11402 Data Analytics Project

針對社群媒體不同主題類別（Technology、Sports、Finance、Politics、Health、Climate、Entertainment）的評論，分析其情感分布與差異。

資料集：`Social_Media_Sentiment_Analysis_AI_Trends_2026.csv`（2200 筆，來源：YouTube / Twitter / Reddit）

## 分析內容

| # | 圖表 | 說明 |
|---|------|------|
| 1 | 各主題情感分佈（計數） | 各類別評論量與正負情感數量 |
| 2 | 各主題情感比例（堆疊） | 哪個類別最正面／負面 |
| 3 | 情感分數 Boxplot | 各類別情感分數的集中與離散程度 |
| 4 | 情緒 × 主題 Heatmap | 各類別引發的情緒分佈 |
| 5 | 主題 × 平台正面比例 | 同一主題在不同平台的情感差異 |
| 6 | 毒性分數 Violinplot | 各類別討論的毒性程度分佈 |
| 7 | 平均互動分數 | 各類別引發互動的程度 |
| 8 | 情感分數月趨勢 | 各類別情感隨時間的變化 |

卡方檢定（topic × sentiment）結果另於終端機輸出。

## Setup

Install [uv](https://docs.astral.sh/uv/getting-started/installation/):

```bash
# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Install dependencies:

```bash
uv sync
```

## Run

基本分佈圖（情感、平台、情緒、主題、互動分數）：

```bash
uv run main.py
```

主題情感深度分析（專題核心）：

```bash
uv run data-analytics.py
```

圖表皆輸出至 `result/` 資料夾。
