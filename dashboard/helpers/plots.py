import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud


def generate_wordcloud(series: pd.Series) -> plt.Figure:
    """
    Generates a word cloud from a Pandas Series.

    :param series: A Pandas Series containing the text data to generate the word cloud.
    :return: A matplotlib figure object containing the word cloud plot.
    """
    text = " ".join(series.dropna().astype(str))
    
    wordcloud = WordCloud(width=800, height=400, background_color="white").generate(text)
    
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wordcloud, interpolation="bilinear")
    ax.axis("off")
    
    return fig

def satisfaction_trend(df: pd.DataFrame) -> plt.Figure:
    """
    Plots a graph showing the trend of satisfaction over time.

    :param df: DataFrame containing the satisfaction data with columns such as
               session_created_at and satisfaction.
    :return: A matplotlib figure object containing the plot.
    """
    df = df.sort_values("session_created_at")

    fig, ax = plt.subplots()
    sns.lineplot(x="session_created_at", y="satisfaction", data=df, marker="o", ax=ax)
    ax.set_title("Satisfaction Trend")
    
    return fig