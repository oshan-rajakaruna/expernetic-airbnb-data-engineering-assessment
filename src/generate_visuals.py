from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt


ANALYSIS_DIR = Path("outputs/tables/analysis")
FIGURES_DIR = Path("outputs/figures")
FIGURES_DIR.mkdir(parents=True, exist_ok=True)


def save_bar_chart(df, x_col, y_col, title, xlabel, ylabel, filename, rotate_x=True):
    plt.figure(figsize=(10, 6))
    plt.bar(df[x_col].astype(str), df[y_col])
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

    if rotate_x:
        plt.xticks(rotation=45, ha="right")

    plt.tight_layout()
    output_path = FIGURES_DIR / filename
    plt.savefig(output_path, dpi=300)
    plt.close()

    print(f"Saved: {output_path}")


def main():
    room_type = pd.read_csv(ANALYSIS_DIR / "02_room_type_summary.csv")
    top_price_neighbourhoods = pd.read_csv(ANALYSIS_DIR / "03_top_neighbourhoods_by_price.csv")
    neighbourhood_supply = pd.read_csv(ANALYSIS_DIR / "04_neighbourhood_supply_availability.csv")
    review_activity = pd.read_csv(ANALYSIS_DIR / "07_review_activity_by_neighbourhood.csv")
    revenue_proxy = pd.read_csv(ANALYSIS_DIR / "08_revenue_proxy_by_neighbourhood.csv")

    save_bar_chart(
        df=room_type,
        x_col="room_type",
        y_col="listing_count",
        title="Listing Count by Room Type",
        xlabel="Room Type",
        ylabel="Number of Listings",
        filename="01_listing_count_by_room_type.png",
    )

    save_bar_chart(
        df=room_type,
        x_col="room_type",
        y_col="avg_price",
        title="Average Price by Room Type",
        xlabel="Room Type",
        ylabel="Average Price",
        filename="02_average_price_by_room_type.png",
    )

    save_bar_chart(
        df=top_price_neighbourhoods,
        x_col="neighbourhood",
        y_col="avg_price",
        title="Top 10 Neighbourhoods by Average Price",
        xlabel="Neighbourhood",
        ylabel="Average Price",
        filename="03_top_neighbourhoods_by_average_price.png",
    )

    top_supply = neighbourhood_supply.sort_values(
        "listing_count", ascending=False
    ).head(10)

    save_bar_chart(
        df=top_supply,
        x_col="neighbourhood",
        y_col="listing_count",
        title="Top 10 Neighbourhoods by Listing Supply",
        xlabel="Neighbourhood",
        ylabel="Number of Listings",
        filename="04_top_neighbourhoods_by_listing_supply.png",
    )

    save_bar_chart(
        df=review_activity,
        x_col="neighbourhood",
        y_col="total_reviews",
        title="Top 10 Neighbourhoods by Review Activity",
        xlabel="Neighbourhood",
        ylabel="Total Reviews",
        filename="05_review_activity_by_neighbourhood.png",
    )

    save_bar_chart(
        df=revenue_proxy,
        x_col="neighbourhood",
        y_col="estimated_revenue_proxy",
        title="Top 10 Neighbourhoods by Estimated Revenue Proxy",
        xlabel="Neighbourhood",
        ylabel="Estimated Revenue Proxy",
        filename="06_revenue_proxy_by_neighbourhood.png",
    )

    print("\nVisualization generation complete.")


if __name__ == "__main__":
    main()