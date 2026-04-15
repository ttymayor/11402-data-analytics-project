import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_style("whitegrid")
plt.rcParams["figure.figsize"] = (8, 5)
plt.rcParams["font.sans-serif"] = ["Microsoft JhengHei"]


def main():
    path = "archive/Social_Media_Sentiment_Analysis_AI_Trends_2026.csv"
    print("Path to dataset files:", path)

    print("\n\n資料集資料載入")
    df = pd.read_csv(path, encoding="utf-8")
    print(df.head())

    print("\n\n缺失值 Missing Values")
    print(df.isnull().sum())

    os.makedirs("result", exist_ok=True)

    sns.countplot(x="sentiment_label", data=df)
    plt.title("情感分佈 Sentiment Distribution")
    plt.tight_layout()
    plt.savefig("result/sentiment_distribution.png")
    plt.close()

    sns.countplot(x="platform", data=df)
    plt.title("平台分佈 Platform Distribution")
    plt.tight_layout()
    plt.savefig("result/platform_distribution.png")
    plt.close()

    sns.countplot(x="emotion_label", data=df)
    plt.title("情緒分佈 Emotion Distribution")
    plt.tight_layout()
    plt.savefig("result/emotion_distribution.png")
    plt.close()

    sns.countplot(y="topic_category", data=df)
    plt.title("主題類別分佈 Topic Categories")
    plt.tight_layout()
    plt.savefig("result/topic_categories.png")
    plt.close()

    sns.histplot(df["engagement_score"], bins=30, kde=True)
    plt.title("互動分數分佈 Engagement Score Distribution")
    plt.tight_layout()
    plt.savefig("result/engagement_score_distribution.png")
    plt.close()


if __name__ == "__main__":
    main()
