import json
import os
from datetime import datetime

# File to store user BMI history
DATA_FILE = "bmi_history.json"

# BMI categories
def bmi_category(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif 18.5 <= bmi < 24.9:
        return "Normal weight"
    elif 25 <= bmi < 29.9:
        return "Overweight"
    else:
        return "Obese"

# Calculate BMI
def calculate_bmi(weight, height):
    return round(weight / (height ** 2), 2)

# Save BMI record to JSON
def save_bmi(user_name, bmi, category):
    record = {
        "date": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "bmi": bmi,
        "category": category
    }
    data = {}
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
    if user_name in data:
        data[user_name].append(record)
    else:
        data[user_name] = [record]
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

# Show BMI history with ASCII graph
def show_history(user_name):
    if not os.path.exists(DATA_FILE):
        print("No history found.")
        return
    with open(DATA_FILE, "r") as f:
        data = json.load(f)
    if user_name not in data:
        print("No history for this user.")
        return

    print(f"\nBMI History for {user_name}:")
    for entry in data[user_name]:
        print(f"{entry['date']}: BMI = {entry['bmi']} ({entry['category']})")
    print("\nBMI Trend Graph:")
    for entry in data[user_name]:
        bar = "#" * int(entry['bmi'])
        print(f"{entry['date'][:10]} | {bar} ({entry['bmi']})")

# Main program
def main():
    print("=== Advanced Terminal BMI Calculator ===\n")
    user_name = input("Enter your name: ").strip()
    while True:
        try:
            weight = float(input("Enter weight (kg): "))
            height = float(input("Enter height (cm): ")) / 100  # Convert cm to meters
            if weight <= 0 or height <= 0:
                print("Weight and height must be positive numbers. Try again.")
                continue
        except ValueError:
            print("Invalid input. Enter numeric values only.")
            continue

        bmi = calculate_bmi(weight, height)
        category = bmi_category(bmi)
        print(f"\n{user_name}, your BMI is {bmi} ({category})")

        # Save BMI record
        save_bmi(user_name, bmi, category)

        # Show history
        show_history(user_name)

        cont = input("\nDo you want to calculate BMI again? (yes/no): ").strip().lower()
        if cont != "yes":
            print("Goodbye!")
            break

if __name__ == "__main__":
    main()
