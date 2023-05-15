"""
簡易記帳系統

功能：
1. 顯示當前餘額
2. 新增收入（需要提供描述和金额與日期）
3. 新增支出（需要提供描述和金额與日期）
4. 依據時間區間顯示記帳紀錄

作者：Yen-Wei-Liang
"""




import tkinter as tk
import sqlite3

def update_balance():
    c.execute("SELECT SUM(amount) FROM transactions")
    result = c.fetchone()
    balance = result[0] if result[0] else 0.0
    balance_label.config(text=f"Balance: {balance}")

def add_income():
    """
    輸入收入金額和描述訊息，並加入資料庫內更新餘額。
    """
    amount = float(income_amount_entry.get())
    description = income_description_entry.get()
    date = income_date_entry.get()  
    c.execute("INSERT INTO transactions (date, amount, description) VALUES (?, ?, ?)", (date, amount, description))
    conn.commit()
    income_amount_entry.delete(0, tk.END)
    income_description_entry.delete(0, tk.END)
    income_date_entry.delete(0, tk.END)
    update_balance()

def add_expense():
    """
    輸入開銷金額和描述訊息，並加入資料庫內更新餘額。
    """
    amount = float(expense_amount_entry.get())
    description = expense_description_entry.get()
    date = expense_date_entry.get()  
    c.execute("INSERT INTO transactions (date, amount, description) VALUES (?, ?, ?)", (date, -amount, description))
    conn.commit()
    expense_amount_entry.delete(0, tk.END)
    expense_description_entry.delete(0, tk.END)
    expense_date_entry.delete(0, tk.END)
    update_balance()

def show_records():
    """
    輸入開始日期和結束日期取此時間範圍，查詢資料庫中在該範圍內的交易記錄，並在文本框中顯示這些記錄。
    """
    start_date = start_date_entry.get()
    end_date = end_date_entry.get()

    c.execute("SELECT * FROM transactions WHERE date BETWEEN ? AND ?", (start_date, end_date))
    result = c.fetchall()
    records_text.delete(1.0, tk.END)

    if result:
        for record in result:
            record_str = f"Date: {record[0]}\nType: {'Income' if record[1] > 0 else 'Expense'}\nDescription: {record[2]}\nAmount: {record[1]}\n\n"
            records_text.insert(tk.END, record_str)
    else:
        records_text.insert(tk.END, "No records found for the selected period.")

conn = sqlite3.connect('bookkeeping.db')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS transactions
             (date TEXT NOT NULL,
              amount REAL NOT NULL,
              description TEXT NOT NULL)''')

window = tk.Tk()
window.title("Simple Bookkeeping System")

balance_label = tk.Label(window, text="Balance: 0.0")
balance_label.pack()

income_frame = tk.Frame(window)
income_frame.pack(pady=10)

income_label = tk.Label(income_frame, text="Income:")
income_label.grid(row=0, column=0, sticky="W")
income_amount_entry = tk.Entry(income_frame)
income_amount_entry.grid(row=0, column=1)

income_description_label = tk.Label(income_frame, text="Description:")
income_description_label.grid(row=1, column=0, sticky="W")
income_description_entry = tk.Entry(income_frame)
income_description_entry.grid(row=1, column=1)

income_date_label = tk.Label(income_frame, text="Date (YYYY-MM-DD):")
income_date_label.grid(row=2, column=0, sticky="W")
income_date_entry = tk.Entry(income_frame)
income_date_entry.grid(row=2, column=1)

add_income_button = tk.Button(income_frame, text="Add Income", command=add_income)
add_income_button.grid(row=3, columnspan=2)

expense_frame = tk.Frame(window)
expense_frame.pack(pady=10)

expense_label = tk.Label(expense_frame, text="Expense:")
expense_label.grid(row=0, column=0, sticky="W")
expense_amount_entry = tk.Entry(expense_frame)
expense_amount_entry.grid(row=0, column=1)

expense_description_label = tk.Label(expense_frame, text="Description:")
expense_description_label.grid(row=1, column=0, sticky="W")
expense_description_entry = tk.Entry(expense_frame)
expense_description_entry.grid(row=1, column=1)

expense_date_label = tk.Label(expense_frame, text="Date (YYYY-MM-DD):")
expense_date_label.grid(row=2, column=0, sticky="W")
expense_date_entry = tk.Entry(expense_frame)
expense_date_entry.grid(row=2, column=1)

add_expense_button = tk.Button(expense_frame, text="Add Expense", command=add_expense)
add_expense_button.grid(row=3, columnspan=2)

date_frame = tk.Frame(window)
date_frame.pack(pady=10)

start_date_label = tk.Label(date_frame, text="Start Date (YYYY-MM-DD):")
start_date_label.grid(row=0, column=0, sticky="W")
start_date_entry = tk.Entry(date_frame)
start_date_entry.grid(row=0, column=1)

end_date_label = tk.Label(date_frame, text="End Date (YYYY-MM-DD):")
end_date_label.grid(row=1, column=0, sticky="W")
end_date_entry = tk.Entry(date_frame)
end_date_entry.grid(row=1, column=1)

show_records_button = tk.Button(date_frame, text="Show Records", command=show_records)
show_records_button.grid(row=2, columnspan=2)

records_text = tk.Text(window, height=6, width=30)
records_text.pack(pady=10)

update_balance()

window.mainloop()

conn.close()


