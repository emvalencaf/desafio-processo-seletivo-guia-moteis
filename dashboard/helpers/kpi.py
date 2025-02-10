import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

import pandas as pd

def calculate_kpis(df: pd.DataFrame) -> dict:
    """
    Calculates the key performance indicators (KPIs) for the chatbot using Pandas.

    :param df: DataFrame containing the chatbot data with columns such as 
               session_id, satisfaction, input_tokens, output_tokens, 
               input_tokens_price, and output_tokens_price.
    :return: A dictionary containing the calculated KPIs: total_sessions, avg_satisfaction,
             total_input_tokens, total_output_tokens, avg_input_tokens, avg_output_tokens,
             and total_cost.
    """
    if df.empty:
        return {
            "total_sessions": 0,
            "avg_satisfaction": 0,
            "total_input_tokens": 0,
            "total_output_tokens": 0,
            "avg_input_tokens": 0,
            "avg_output_tokens": 0,
            "total_cost": 0
        }

    # Filling NaN values with 0 to avoid errors
    df = df.fillna(0)

    # Calculating KPIs
    total_sessions = df["session_id"].nunique()
    avg_satisfaction = df["satisfaction"].mean()
    total_input_tokens = df["input_tokens"].sum()
    total_output_tokens = df["output_tokens"].sum()

    # Calculating total cost based on price per million tokens
    total_cost_input = (df["input_tokens"] / 1_000_000 * df.get("input_tokens_price", 0)).sum()
    total_cost_output = (df["output_tokens"] / 1_000_000 * df.get("output_tokens_price", 0)).sum()

    total_cost = total_cost_input + total_cost_output

    avg_input_tokens = df["input_tokens"].mean()
    avg_output_tokens = df["output_tokens"].mean()

    return {
        "total_sessions": total_sessions,
        "avg_satisfaction": round(avg_satisfaction, 2),
        "total_input_tokens": total_input_tokens,
        "total_output_tokens": total_output_tokens,
        "avg_input_tokens": round(avg_input_tokens, 2),
        "avg_output_tokens": round(avg_output_tokens, 2),
        "total_cost": round(total_cost, 2),
    }

def tokens_trend(df: pd.DataFrame) -> plt.Figure:
    """
    Plots a graph showing the trend of token usage and total cost over time.

    :param df: DataFrame containing the token usage and cost data with columns 
               such as analysis_created_at, input_tokens, output_tokens, 
               input_tokens_price, and output_tokens_price.
    :return: A matplotlib figure object containing the plot.
    """
    df = df.sort_values("analysis_created_at")

    fig, ax = plt.subplots()
    sns.lineplot(x="analysis_created_at", y="input_tokens", data=df, marker="o", label="Input Tokens", ax=ax)
    sns.lineplot(x="analysis_created_at", y="output_tokens", data=df, marker="o", label="Output Tokens", ax=ax)
    sns.lineplot(x="analysis_created_at", y="input_tokens_price", data=df, marker="x", label="Input Cost (USD)", ax=ax)
    sns.lineplot(x="analysis_created_at", y="output_tokens_price", data=df, marker="x", label="Output Cost (USD)", ax=ax)
    
    ax.set_title("Token Usage and Total Cost Trend")
    ax.set_ylabel("Token Amount / Cost (USD)")
    ax.legend()
    return fig


def cost_distribution(df: pd.DataFrame) -> plt.Figure:
    """
    Plots the distribution of costs per session.

    :param df: DataFrame containing the session data with columns such as 
               session_id, input_tokens, output_tokens, input_tokens_price, 
               and output_tokens_price.
    :return: A matplotlib figure object containing the plot.
    """
    df = df.sort_values("session_id")

    fig, ax = plt.subplots()
    sns.lineplot(x="session_id", y="input_tokens", data=df, marker="o", label="Input Tokens", ax=ax)
    sns.lineplot(x="session_id", y="output_tokens", data=df, marker="o", label="Output Tokens", ax=ax)
    sns.lineplot(x="session_id", y="input_tokens_price", data=df, marker="x", label="Input Cost (USD)", ax=ax)
    sns.lineplot(x="session_id", y="output_tokens_price", data=df, marker="x", label="Output Cost (USD)", ax=ax)
    
    ax.set_title("Cost Distribution Per Session")
    ax.set_ylabel("Token Amount / Cost (USD)")
    ax.legend()
    return fig

