import random

def calculate_statistics(data):
    total = sum(data)
    count = len(data)
    average = total / count if count else 0
    return total, average

def process_data(data):
    filtered_data = [x for x in data if x > 0]
    negative_data = [-x for x in data if x < 0]
    return filtered_data, negative_data

def main():
    raw_data = [random.randint(-10, 10) for _ in range(10)]
    positive_data, negative_data = process_data(raw_data)

    total_positive, avg_positive = calculate_statistics(positive_data)
    total_negative, avg_negative = calculate_statistics(negative_data)

    print(f"Raw data: {raw_data}")
    print(f"Positive data: {positive_data} (Total: {total_positive}, Average: {avg_positive})")
    print(f"Negative data: {negative_data} (Total: {total_negative}, Average: {avg_negative})")

    if avg_positive > avg_negative:
        print("Average of positive numbers is greater.")
    else:
        print("Average of negative numbers is greater or equal.")

    for i in range(5):
        print(f"Random data {i}: {random.choice(raw_data)}")

if __name__ == "__main__":
    main()