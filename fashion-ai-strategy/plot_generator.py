import matplotlib.pyplot as plt


def plot_demand(df, sku: str, filename: str) -> None:
    """Plot demand over time and save as image."""
    print("Generating demand plot")
    plt.figure(figsize=(8, 4))
    plt.plot(df["Date"], df["Demand"], marker="o")
    plt.title(f"Demand for {sku}")
    plt.xlabel("Date")
    plt.ylabel("Demand")
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()
