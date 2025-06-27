import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt

class StockMlModel:
    """
    Predicts next-day stock movement using RSI, MACD, and Volume
    using Logistic Regression.
    """

    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()
        self.model = LogisticRegression(solver='liblinear', random_state=42)

    def engineer_features(self):
        """
        Engineer financial features (RSI, MACD) and construct the target column.

        Features:
        - RSI: Relative Strength Index over a 14-day window.
        - MACD: Difference between 12-day and 26-day EMA.
        - Volume: Already available in data.

        Target:
        - 1 if the next day's Close price is greater than today's, else 0.
        """
        # Compute RSI
        delta = self.df['Close'].diff()
        gain = delta.clip(lower=0)
        loss = -delta.clip(upper=0)
        avg_gain = gain.rolling(14).mean()
        avg_loss = loss.rolling(14).mean()
        rs = avg_gain / (avg_loss + 1e-10)
        self.df['RSI'] = 100 - (100 / (1 + rs))

        # Compute MACD
        exp1 = self.df['Close'].ewm(span=12, adjust=False).mean()
        exp2 = self.df['Close'].ewm(span=26, adjust=False).mean()
        self.df['MACD'] = exp1 - exp2

        # Confirm MACD is added
        if 'MACD' not in self.df.columns:
            raise ValueError("MACD was not added properly.")

        # Define Target
        self.df['Target'] = (self.df['Close'].shift(-1) > self.df['Close']).astype(int)

        print("Columns before dropna:", self.df.columns.tolist())
        self.df.dropna(inplace=True)
        print("Columns after dropna:", self.df.columns.tolist())

    def eda_summary(self):
        """
        Prints basic EDA summaries:
        - First few rows
        - Descriptive statistics
        - Target class distribution
        - Correlation between key features
        """
        print("\nHead of data:")
        print(self.df.head())

        print("\nSummary stats:")
        print(self.df.describe())

        print("\nClass distribution:")
        print(self.df['Target'].value_counts())

        print("\nCorrelation matrix:")
        print(self.df[['RSI', 'MACD', 'Volume', 'Target']].corr())

    def visualize_data(self):
        """
        Display EDA visualizations:
        - Histogram of RSI
        - Scatter plot of MACD vs RSI with target as hue
        """
        sns.histplot(self.df['RSI'], kde=True)
        plt.title("RSI Distribution")
        plt.show()

        sns.scatterplot(data=self.df, x='MACD', y='RSI', hue='Target')
        plt.title("MACD vs RSI with Target")
        plt.show()

    def train_and_evaluate(self):
        """
        Splits the data into training and test sets, trains a Logistic Regression model,
        and evaluates performance using accuracy, classification report, and confusion matrix.
        """
        features = ['RSI', 'MACD', 'Volume']
        missing = [f for f in features if f not in self.df.columns]
        if missing:
            raise ValueError(f"Missing features: {missing}")

        X = self.df[features]
        y = self.df['Target']

        # Train-test split
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Train model
        self.model.fit(X_train, y_train)

        # Predict
        predictions = self.model.predict(X_test)

        # Evaluation
        acc = accuracy_score(y_test, predictions)
        print(f"\nAccuracy: {acc * 100:.2f}%")

        print("\nClassification Report:")
        print(classification_report(y_test, predictions, zero_division=0))

        print("\nConfusion Matrix:")
        print(confusion_matrix(y_test, predictions))


# Example usage
if __name__ == "__main__":
    from data_fetcher import DataFetcherFactory

    print("\nFetching data for ML model...")
    fetcher = DataFetcherFactory.get_data_fetcher("alpha_vantage")
    df = fetcher.get_daily_data("RELIANCE.BSE", outputsize="full")

    if df.empty:
        print("No data found.")
    else:
        model = StockMlModel(df)
        model.engineer_features()
        model.eda_summary()
        # model.visualize_data()  # Uncomment to visualize
        model.train_and_evaluate()
