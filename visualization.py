import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from models_stacking import train_models


def main():
    models, X_test, y_test, dates, idx_test, _ = train_models()

    test_dates = dates.iloc[idx_test].values
    sort_idx = np.argsort(test_dates)
    test_dates_sorted = test_dates[sort_idx]
    actual_sorted = y_test.values[sort_idx]

    fig, ax = plt.subplots(figsize=(12, 5))

    ax.plot(test_dates_sorted, actual_sorted, label="Actual", linewidth=2)

    for name, model in models.items():
        preds = model.predict(X_test)[sort_idx]
        ax.plot(test_dates_sorted, preds, label=name, linestyle="--")

    ax.set_title("Actual vs Predicted Day Change % (Test Set)")
    ax.set_xlabel("Date")
    ax.set_ylabel("Day Change %")
    ax.legend()
    ax.grid(True)

    plt.xticks(rotation=35, ha="right")
    plt.tight_layout()
    plt.savefig("sp500_predictions.png", dpi=150)

if __name__ == "__main__":
    main()