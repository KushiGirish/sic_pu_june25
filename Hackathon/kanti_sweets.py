import pandas as pd, numpy as np, datetime, random, os, tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from collections import Counter
from itertools import combinations

def generate_kanti_sweets_data(num_records=10000):
    items = ["Mysore Pak", "Dharwad Peda", "Badam Milk", "Kaju Katli", "Laddoo (Boondi)",
             "Jalebi", "Samosa", "Gulab Jamun", "Rasgulla", "Milk Burfi", "Pista Roll",
             "Kesar Peda", "Sohan Papdi", "Chiroti", "Halwa (Assorted)"]
    branches = ["Jayanagar", "Malleswaram", "Indiranagar", "Koramangala", "Basavanagudi",
                "Vijayanagar", "RR Nagar", "HSR Layout", "Electronic City"]
    base_prices = {
        "Mysore Pak": 400, "Dharwad Peda": 450, "Badam Milk": 80, "Kaju Katli": 800,
        "Laddoo (Boondi)": 300, "Jalebi": 250, "Samosa": 30, "Gulab Jamun": 50,
        "Rasgulla": 55, "Milk Burfi": 380, "Pista Roll": 750, "Kesar Peda": 500,
        "Sohan Papdi": 280, "Chiroti": 150, "Halwa (Assorted)": 350
    }

    start, end = datetime.date.today() - datetime.timedelta(days=550), datetime.date.today()
    data = []
    for i in range(num_records):
        txn = f"TXN{100000 + i}"
        dt = start + datetime.timedelta(days=random.randint(0, (end - start).days))
        t = datetime.time(*(random.randint(a, b) for a, b in [(8,22), (0,59), (0,59)]))
        hour = t.hour
        period = "Morning" if 6 <= hour < 12 else "Afternoon" if 12 <= hour < 17 else "Evening" if 17 <= hour < 22 else "Night"
        selected_items = random.sample(items, random.choices([1,2,3], [70,20,10])[0])
        branch = random.choice(branches)

        for item in selected_items:
            cost = round(base_prices[item] * random.uniform(0.5, 3.0), 2)
            cost = cost if cost >= 20 else random.uniform(20, 100)
            data.append({"transaction_id": txn, "item_name": item, "date": dt.strftime("%Y-%m-%d"),
                         "time": t.strftime("%H:%M:%S"), "period": period, "purchase_cost": cost,
                         "branch_location": branch})
    return pd.DataFrame(data)

def display_table(tree, data, cols):
    tree.delete(*tree.get_children())
    tree["columns"], tree["show"] = cols, "headings"
    [tree.heading(c, text=c) or tree.column(c, width=200, anchor="center") for c in cols]
    [tree.insert("", "end", values=r) for r in data]

def plot_bar(data, title, xlabel, ylabel, color='skyblue'):
    plt.figure(figsize=(8, 5))
    data.plot(kind='bar', color=color)
    plt.title(title), plt.xlabel(xlabel), plt.ylabel(ylabel)
    plt.grid(axis='y'), plt.tight_layout(), plt.show()

def plot_hourly_sales(df, day):
    df['hour'] = pd.to_datetime(df['time']).dt.hour
    plot_bar(df.groupby('hour')['purchase_cost'].sum(), f"Hourly Sales on {day}", "Hour", "Sales (₹)")

def plot_sweet_sales_pie(df):
    s = df.groupby('item_name')['purchase_cost'].sum().sort_values(ascending=False).head(5)
    plt.figure(figsize=(6, 6))
    plt.pie(s, labels=s.index, autopct='%1.1f%%', startangle=140)
    plt.title("Top 5 Sweets by Sales"), plt.tight_layout(), plt.show()

def plot_period_sales_bar(df):
    plot_bar(df.groupby('period')['purchase_cost'].sum(), "Sales by Period", "Period", "Sales (₹)", color='orange')

def find_favorite_combos(df):
    grouped = df.groupby('transaction_id')['item_name'].apply(list)
    combos = [pair for items in grouped if len(items) > 1 for pair in combinations(sorted(items), 2)]
    return Counter(combos).most_common(5)

def perform_custom_daily_analysis(df, date_str, sweet, branch, tree):
    try:
        sel_day = pd.to_datetime(date_str).date()
    except ValueError:
        return messagebox.showerror("Invalid Date", "Use YYYY-MM-DD format.")
    
    df['date'] = pd.to_datetime(df['date'])
    day_df = df[df['date'].dt.date == sel_day]

    if branch != "All":
        day_df = day_df[day_df['branch_location'] == branch]
        if day_df.empty:
            return messagebox.showinfo("No Data", f"No transactions at '{branch}' on {sel_day}.")

    if day_df.empty:
        return messagebox.showinfo("No Data", f"No transactions for {sel_day}.")

    output = []
    total_sales = day_df['purchase_cost'].sum()
    avg_txn = day_df.groupby('transaction_id')['purchase_cost'].sum().mean()

    if sweet == "All":
        sales = day_df.groupby('item_name')['purchase_cost'].sum()
        top, least = sales.idxmax(), sales.idxmin()
        peak_hour = pd.to_datetime(day_df['time']).dt.hour
        peak_hour_val = day_df.groupby(peak_hour)['purchase_cost'].sum().idxmax()
        combo = find_favorite_combos(day_df)
        combo_text = f"{combo[0][0][0]} + {combo[0][0][1]}" if combo else "N/A"

        output = [
            ("Top Selling Sweet", "Highest revenue", f"{top} (₹{sales[top]:.2f})"),
            ("Least Selling Sweet", "Lowest revenue", f"{least} (₹{sales[least]:.2f})"),
            ("Peak Sale Hour", "Max sales hour", f"{peak_hour_val}:00"),
            ("Favorite Combo", "Most frequent pair", combo_text),
            ("Total Revenue", "All sales", f"₹{total_sales:.2f}"),
            ("Avg Transaction", "₹ per txn", f"₹{avg_txn:.2f}")
        ]

        display_table(tree, output, ["Category", "Description", "Value"])
        plot_hourly_sales(day_df, sel_day)
        plot_sweet_sales_pie(day_df)
        plot_period_sales_bar(day_df)
    else:
        s_df = day_df[day_df['item_name'] == sweet]
        if s_df.empty:
            return messagebox.showinfo("No Sweet Data", f"No sales of '{sweet}' on {sel_day}.")
        time_summary = s_df.groupby('period')['purchase_cost'].sum().reset_index()
        output = [(f"{sweet} - {row['period']}", "Sales", f"₹{row['purchase_cost']:.2f}") for _, row in time_summary.iterrows()]
        display_table(tree, output, ["Category", "Description", "Value"])
        plot_hourly_sales(s_df, sel_day)
        plot_period_sales_bar(s_df)

def run_gui():
    df = generate_kanti_sweets_data(15000)
    sweets = ["All"] + sorted(df['item_name'].unique().tolist())
    branches = ["All"] + sorted(df['branch_location'].unique().tolist())

    path = os.path.join(os.path.expanduser("~"), "Desktop", "kanti_sweets_transactions.csv")
    try: df.to_csv(path, index=False); print(f"Saved to {path}")
    except: df.to_csv("kanti_sweets_transactions.csv", index=False); print("Saved locally due to error.")

    root = tk.Tk(); root.title("Kanti Sweets Daily Analysis")
    ttk.Label(root, text="Enter date (YYYY-MM-DD):").pack(pady=5)
    date_entry = ttk.Entry(root, width=30); date_entry.pack(pady=5)

    ttk.Label(root, text="Select sweet (or 'All'):").pack(pady=5)
    sweet_var = tk.StringVar(); sweet_combo = ttk.Combobox(root, textvariable=sweet_var, values=sweets, width=30)
    sweet_combo.set("All"); sweet_combo.pack(pady=5)

    ttk.Label(root, text="Select branch (or 'All'):").pack(pady=5)
    branch_var = tk.StringVar(); branch_combo = ttk.Combobox(root, textvariable=branch_var, values=branches, width=30)
    branch_combo.set("All"); branch_combo.pack(pady=5)

    tree = ttk.Treeview(root); tree.pack(padx=10, pady=10, fill='x')
    ttk.Button(root, text="Analyze", command=lambda: perform_custom_daily_analysis(
        df, date_entry.get(), sweet_var.get(), branch_var.get(), tree)).pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    run_gui()
