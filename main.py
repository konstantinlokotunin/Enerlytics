from src.extract import extract_data
from src.transform import transform_data
from src.visualization import visualize_data


def main():
    df = extract_data()
    df = transform_data(df)
    visualize_data(df)

if __name__ == "__main__":
    main()