import polars as pl
import time
import pandas as pd
import os

df_pl = pl.read_parquet("social_media_data.parquet")
df_pl_users = pl.read_parquet("users.parquet")

threads = pl.thread_pool_size()
print(f"Polars threads: {threads}")

def query_A_polars():
    return df_pl.group_by('location').agg(pl.col('likes').mean()).height

def query_B_polars():
    return (
        df_pl
        .sort(["user_id", "timestamp"])
        .with_columns(
            pl.col("likes")
              .rolling_mean(window_size=3, min_samples=1)
              .over("user_id")
              .alias("avg_last_3")
        )
        .filter(pl.col("avg_last_3") > 5000)
        .height
    )


def query_C_polars():
    return df_pl.join(df_pl_users, on="user_id", how="inner").filter(pl.col("age") >= 25).height

queries = {
    "A polars": query_A_polars,
    "B polars": query_B_polars,
    "C polars": query_C_polars,
}


def measure_time(query):
    start = time.perf_counter()
    result = query()
    elapsed = time.perf_counter() - start
    return elapsed


def benchmark(queries):
    results = []
    for query_name, query_fn in queries.items():
        # warm-up
        query_fn()

        # benchmark
        t = measure_time(query_fn)

        results.append({
            "Threads": threads,
            "Query": query_name,
            "Time [s]": t,
        })

    return pd.DataFrame(results)

benchmark_results = benchmark(queries)
print(benchmark_results)
write_header = not os.path.exists("benchmark_polars.csv")
benchmark_results.to_csv("benchmark_polars.csv", mode="a", header=write_header, index=False)