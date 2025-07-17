import pandas as pd
import numpy as np
import datetime
import random
import os
import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from collections import Counter
from itertools import combinations

# ========================= Data Generation =========================
def generate_kanti_sweets_data(num_records=10000):
    item_names = [
        "Mysore Pak", "Dharwad Peda", "Badam Milk", "Kaju Katli", "Laddoo (Boondi)",
        "Jalebi", "Samosa", "Gulab Jamun", "Rasgulla", "Milk Burfi",
        "Pista Roll", "Kesar Peda", "Sohan Papdi", "Chiroti", "Halwa (Assorted)"]

    branch_locations = [
        "Jayanagar", "Malleswaram", "Indiranagar", "Koramangala",
        "Basavanagudi", "Vijayanagar", "RR Nagar", "HSR Layout", "Electronic City"]

    item_base_prices = {
        "Mysore Pak": 400, "Dharwad Peda": 450, "Badam Milk": 80, "Kaju Katli": 800,
        "Laddoo (Boondi)": 300, "Jalebi": 250, "Samosa": 30, "Gulab Jamun": 50,
        "Rasgulla": 55, "Milk Burfi": 380, "Pista Roll": 750, "Kesar Peda": 500,
        "Sohan Papdi": 280, "Chiroti": 150, "Halwa (Assorted)": 350
    }

    end_date = datetime.date.today()
    start_date = end_date - datetime.timedelta(days=int(365 * 1.5))

    data = []
    for i in range(num_records):
        transaction_id = f"TXN{100000 + i}"
        days_diff = (end_date - start_date).days
        random_date = start_date + datetime.timedelta(days=random.randint(0, days_diff))
        hour = random.randint(8, 22)
        minute = random.randint(0, 59)
        second = random.randint(0, 59)
        random_time = datetime.time(hour, minute, second)

        if 6 <= hour < 12:
            period = "Morning"
        elif 12 <= hour < 17:
            period = "Afternoon"
        elif 17 <= hour < 22:
            period = "Evening"
        else:
            period = "Night"

        num_items = random.choices([1, 2, 3], weights=[70, 20, 10])[0]
        selected_items = random.sample(item_names, num_items)

        branch = random.choice(branch_locations)

        for item in selected_items:
            base_cost = item_base_prices.get(item, 300)
            purchase_cost = round(base_cost * random.uniform(0.5, 3.0), 2)
            if purchase_cost < 20:
                purchase_cost = random.uniform(20, 100)

            data.append({
                "transaction_id": transaction_id,
                "item_name": item,
                "date": random_date.strftime("%Y-%m-%d"),
                "time": random_time.strftime("%H:%M:%S"),
                "period": period,
                "purchase_cost": purchase_cost,
                "branch_location": branch
            })

    df = pd.DataFrame(data)
    return df

# ========================= GUI Analysis =========================
def display_table(tree, data, columns):
    tree.delete(*tree.get_children())
    tree["columns"] = columns
    tree["show"] = "headings"

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=200, anchor="center")

    for row in data:
        tree.insert("", "end", values=row)


def plot_hourly_sales(df, selected_day):
    df['hour'] = pd.to_datetime(df['time'], format='%H:%M:%S').dt.hour
    hourly_sales = df.groupby('hour')['purchase_cost'].sum()

    plt.figure(figsize=(8, 5))
    hourly_sales.plot(kind='bar', color='skyblue')
    plt.title(f"Hourly Sales Distribution on {selected_day}")
    plt.xlabel("Hour of Day")
    plt.ylabel("Total Sales (₹)")
    plt.grid(axis='y')
    plt.tight_layout()
    plt.show()


def plot_sweet_sales_pie(df):
    sweet_sales = df.groupby('item_name')['purchase_cost'].sum()
    top_sweets = sweet_sales.sort_values(ascending=False).head(5)
    plt.figure(figsize=(6, 6))
    plt.pie(top_sweets, labels=top_sweets.index, autopct='%1.1f%%', startangle=140)
    plt.title("Top 5 Sweets by Sales Share")
    plt.tight_layout()
    plt.show()


def plot_period_sales_bar(df):
    period_sales = df.groupby('period')['purchase_cost'].sum()
    plt.figure(figsize=(6, 4))
    period_sales.plot(kind='bar', color='orange')
    plt.title("Sales by Period")
    plt.xlabel("Period")
    plt.ylabel("Total Sales (₹)")
    plt.tight_layout()
    plt.show()


def find_favorite_combos(df):
    grouped = df.groupby('transaction_id')['item_name'].apply(list)
    combos = []
    for items in grouped:
        if len(items) > 1:
            combos += list(combinations(sorted(items), 2))
    most_common = Counter(combos).most_common(5)
    return most_common


def perform_custom_daily_analysis(df, selected_date, selected_sweet, tree_widget):
    try:
        selected_day = pd.to_datetime(selected_date).date()
    except ValueError:
        messagebox.showerror("Invalid Date", "Please enter a valid date in YYYY-MM-DD format.")
        return

    df['date'] = pd.to_datetime(df['date'])
    df['day'] = df['date'].dt.date
    day_df = df[df['day'] == selected_day]

    if day_df.empty:
        messagebox.showinfo("No Data", f"No transactions found for {selected_day}.")
        return

    output_data = []
    total_sales = day_df['purchase_cost'].sum()
    avg_transaction = day_df.groupby('transaction_id')['purchase_cost'].sum().mean()

    if selected_sweet == "All":
        top_sweet = day_df.groupby('item_name')['purchase_cost'].sum().idxmax()
        top_amount = day_df.groupby('item_name')['purchase_cost'].sum().max()

        least_sweet = day_df.groupby('item_name')['purchase_cost'].sum().idxmin()
        least_amount = day_df.groupby('item_name')['purchase_cost'].sum().min()

        peak_hour = pd.to_datetime(day_df['time'], format='%H:%M:%S').dt.hour
        peak_hour_sale = day_df.groupby(peak_hour)['purchase_cost'].sum()
        peak_hour_result = peak_hour_sale.idxmax()

        favorite_combo = find_favorite_combos(day_df)
        fav_combo_text = f"{favorite_combo[0][0][0]} + {favorite_combo[0][0][1]}"

        output_data = [
            ("Top Selling Sweet", "Highest revenue sweet", f"{top_sweet} (₹{top_amount:.2f})"),
            ("Least Selling Sweet", "Lowest revenue sweet", f"{least_sweet} (₹{least_amount:.2f})"),
            ("Peak Sale Hour", "Hour with max sales", f"{peak_hour_result}:00"),
            ("Favorite Combo", "Most common sweet pair", fav_combo_text),
            ("Total Revenue", "Total of the day", f"₹{total_sales:.2f}"),
            ("Average Transaction", "Avg ₹ per transaction", f"₹{avg_transaction:.2f}")
        ]

        display_table(tree_widget, output_data, ["Category", "Description", "Value"])
        plot_hourly_sales(day_df, selected_day)
        plot_sweet_sales_pie(day_df)
        plot_period_sales_bar(day_df)

    else:
        sweet_df = day_df[day_df['item_name'] == selected_sweet]
        if sweet_df.empty:
            messagebox.showinfo("No Sweet Data", f"No transactions for '{selected_sweet}' on {selected_day}.")
            return

        time_summary = sweet_df.groupby('period')['purchase_cost'].sum().reset_index()
        for _, row in time_summary.iterrows():
            output_data.append((f"{selected_sweet} - {row['period']}", "Sales in ₹", f"₹{row['purchase_cost']:.2f}"))

        display_table(tree_widget, output_data, ["Category", "Description", "Value"])
        plot_hourly_sales(sweet_df, selected_day)
        plot_period_sales_bar(sweet_df)

# ========================= Main GUI =========================
def run_gui():
    df = generate_kanti_sweets_data(num_records=15000)
    unique_sweets = sorted(df['item_name'].unique().tolist())
    unique_sweets.insert(0, "All")

    # Save to Desktop
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    file_name = "kanti_sweets_transactions.csv"
    full_path = os.path.join(desktop_path, file_name)

    try:
        df.to_csv(full_path, index=False)
        print(f"Successfully saved '{file_name}' to: {full_path}")
    except Exception as e:
        df.to_csv(file_name, index=False)
        print(f"Error saving file: {e}. Saved to current directory as '{file_name}'")

    root = tk.Tk()
    root.title("Kanti Sweets Daily Sweet Analysis Menu")

    ttk.Label(root, text="Enter date (YYYY-MM-DD):").pack(pady=5)
    date_entry = ttk.Entry(root, width=30)
    date_entry.pack(pady=5)

    ttk.Label(root, text="Select sweet (or choose 'All'):").pack(pady=5)
    sweet_var = tk.StringVar()
    sweet_combo = ttk.Combobox(root, textvariable=sweet_var, values=unique_sweets, width=30)
    sweet_combo.set("All")
    sweet_combo.pack(pady=5)

    tree = ttk.Treeview(root)
    tree.pack(padx=10, pady=10, fill='x')

    analyze_btn = ttk.Button(
        root,
        text="Analyze Sweet Sales on Date",
        command=lambda: perform_custom_daily_analysis(df, date_entry.get(), sweet_var.get(), tree)
    )
    analyze_btn.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    run_gui()
