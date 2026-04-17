"""
專題：針對社群不同類別（Technology / Sports / Finance / Politics /
      Health / Climate / Entertainment）評論，分析其情感分布與差異
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import chi2_contingency

sns.set_style("whitegrid")
plt.rcParams["figure.figsize"] = (10, 6)
plt.rcParams["font.sans-serif"] = ["Microsoft JhengHei", "PingFang TC", "Noto Sans CJK JP", "sans-serif"]  # 解決中文顯示問題
plt.rcParams["axes.unicode_minus"] = False  # 解決負號顯示問題

OUTPUT_DIR = "result"
os.makedirs(OUTPUT_DIR, exist_ok=True)

SENTIMENT_PALETTE = {"Positive": "#4CAF50", "Neutral": "#FFC107", "Negative": "#F44336"}
TOPIC_ORDER = [
    "Technology",
    "Sports",
    "Finance",
    "Politics",
    "Health",
    "Climate",
    "Entertainment",
]


def savefig(filename):
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, filename))
    plt.close()


def load_data():
    path = "archive/Social_Media_Sentiment_Analysis_AI_Trends_2026.csv"
    df = pd.read_csv(path, encoding="utf-8")
    df["posted_datetime"] = pd.to_datetime(df["posted_datetime"])
    df["topic_category"] = pd.Categorical(
        df["topic_category"], categories=TOPIC_ORDER, ordered=True
    )
    return df


# ── 1. 各主題情感分佈（計數） ────────────────────────────────────────────────
def topic_sentiment_count(df):
    ct = pd.crosstab(df["topic_category"], df["sentiment_label"])
    ct = ct.reindex(TOPIC_ORDER)[["Positive", "Neutral", "Negative"]]
    ct.plot(kind="bar", color=[SENTIMENT_PALETTE[c] for c in ct.columns])
    plt.title("各主題情感分佈（計數）Sentiment Count by Topic")
    plt.xlabel("Topic Category")
    plt.ylabel("Count")
    plt.xticks(rotation=30)
    plt.legend(title="Sentiment")
    savefig("1_topic_sentiment_count.png")


# ── 2. 各主題情感比例（堆疊）────────────────────────────────────────────────
def topic_sentiment_ratio(df):
    ct = (
        pd.crosstab(df["topic_category"], df["sentiment_label"], normalize="index")
        * 100
    )
    ct = ct.reindex(TOPIC_ORDER)[["Positive", "Neutral", "Negative"]]
    ct.plot(kind="barh", stacked=True, color=[SENTIMENT_PALETTE[c] for c in ct.columns])
    plt.title("各主題情感比例 Sentiment Ratio by Topic (%)")
    plt.xlabel("Percentage (%)")
    plt.legend(title="Sentiment", bbox_to_anchor=(1.05, 1), loc="upper left")
    savefig("2_topic_sentiment_ratio.png")


# ── 3. 各主題情感分數分佈（Boxplot）─────────────────────────────────────────
def topic_sentiment_score_box(df):
    sns.boxplot(
        x="topic_category",
        y="sentiment_score",
        hue="topic_category",
        data=df,
        order=TOPIC_ORDER,
        palette="Set2",
        legend=False,
    )
    plt.title("各主題情感分數分佈 Sentiment Score Distribution by Topic")
    plt.xlabel("Topic Category")
    plt.ylabel("Sentiment Score")
    plt.xticks(rotation=30)
    savefig("3_topic_sentiment_score_box.png")


# ── 4. 各主題情緒標籤分佈（Heatmap）─────────────────────────────────────────
def topic_emotion_heatmap(df):
    ct = pd.crosstab(df["topic_category"], df["emotion_label"], normalize="index") * 100
    ct = ct.reindex(TOPIC_ORDER)
    sns.heatmap(ct, annot=True, fmt=".1f", cmap="YlOrRd", linewidths=0.5)
    plt.title("各主題情緒分佈 Emotion Distribution by Topic (%)")
    plt.xlabel("Emotion")
    plt.ylabel("Topic Category")
    savefig("4_topic_emotion_heatmap.png")


# ── 5. 各主題 × 各平台情感差異 ──────────────────────────────────────────────
def topic_platform_sentiment(df):
    # Positive 比例作為指標
    pivot = (
        df[df["sentiment_label"] == "Positive"]
        .groupby(["topic_category", "platform"])
        .size()
        .div(df.groupby(["topic_category", "platform"]).size())
        .mul(100)
        .unstack("platform")
        .reindex(TOPIC_ORDER)
    )
    pivot.plot(kind="bar", colormap="tab10")
    plt.title("各主題各平台正面情感比例 Positive Sentiment % by Topic & Platform")
    plt.xlabel("Topic Category")
    plt.ylabel("Positive Sentiment (%)")
    plt.xticks(rotation=30)
    plt.legend(title="Platform", bbox_to_anchor=(1.05, 1), loc="upper left")
    savefig("5_topic_platform_sentiment.png")


# ── 6. 各主題毒性分數比較 ────────────────────────────────────────────────────
def topic_toxicity(df):
    sns.violinplot(
        x="topic_category",
        y="toxicity_score",
        hue="topic_category",
        data=df,
        order=TOPIC_ORDER,
        palette="Pastel1",
        inner="quartile",
        legend=False,
    )
    plt.title("各主題毒性分數分佈 Toxicity Score by Topic")
    plt.xlabel("Topic Category")
    plt.ylabel("Toxicity Score")
    plt.xticks(rotation=30)
    savefig("6_topic_toxicity.png")


# ── 7. 各主題互動分數比較 ────────────────────────────────────────────────────
def topic_engagement(df):
    avg = df.groupby("topic_category")["engagement_score"].mean().reindex(TOPIC_ORDER)
    sns.barplot(
        x=avg.index, y=avg.values, hue=avg.index, palette="Blues_d", legend=False
    )
    plt.title("各主題平均互動分數 Avg Engagement Score by Topic")
    plt.xlabel("Topic Category")
    plt.ylabel("Avg Engagement Score")
    plt.xticks(rotation=30)
    savefig("7_topic_engagement.png")


# ── 8. 各主題情感分數月趨勢 ──────────────────────────────────────────────────
def topic_sentiment_trend(df):
    monthly = (
        df.groupby(["topic_category", pd.Grouper(key="posted_datetime", freq="ME")])[
            "sentiment_score"
        ]
        .mean()
        .reset_index()
    )
    fig, ax = plt.subplots()
    for topic in TOPIC_ORDER:
        sub = monthly[monthly["topic_category"] == topic]
        ax.plot(sub["posted_datetime"], sub["sentiment_score"], marker="o", label=topic)
    ax.set_title("各主題情感分數月趨勢 Monthly Sentiment Score by Topic")
    ax.set_xlabel("Month")
    ax.set_ylabel("Avg Sentiment Score")
    ax.legend(title="Topic", bbox_to_anchor=(1.05, 1), loc="upper left")
    savefig("8_topic_sentiment_trend.png")


# ── 9. 卡方檢定：主題與情感是否有顯著關聯 ───────────────────────────────────
def chi2_topic_sentiment(df):
    ct = pd.crosstab(df["topic_category"], df["sentiment_label"])
    chi2, p, dof, _ = chi2_contingency(ct)
    print("\n[卡方檢定] topic_category vs sentiment_label")
    print(f"  Chi2 = {chi2:.2f}, p-value = {p:.4f}, dof = {dof}")
    if p < 0.05:
        print("  → 結論：不同主題的情感分佈有顯著差異 (p < 0.05)")
    else:
        print("  → 結論：不同主題的情感分佈無顯著差異 (p >= 0.05)")


def main():
    print("Loading data...")
    df = load_data()
    print(
        f"Rows: {len(df)} | Topics: {df['topic_category'].nunique()} | Platforms: {df['platform'].nunique()}"
    )

    steps = [
        ("1. 各主題情感分佈（計數）", topic_sentiment_count),
        ("2. 各主題情感比例（堆疊）", topic_sentiment_ratio),
        ("3. 各主題情感分數分佈（Boxplot）", topic_sentiment_score_box),
        ("4. 各主題情緒標籤分佈（Heatmap）", topic_emotion_heatmap),
        ("5. 各主題 × 各平台情感差異", topic_platform_sentiment),
        ("6. 各主題毒性分數比較", topic_toxicity),
        ("7. 各主題互動分數比較", topic_engagement),
        ("8. 各主題情感分數月趨勢", topic_sentiment_trend),
    ]

    for name, fn in steps:
        print(f"  繪製 {name}")
        fn(df)

    chi2_topic_sentiment(df)

    print(f"\nDone. Charts saved to '{OUTPUT_DIR}/'")


if __name__ == "__main__":
    main()
