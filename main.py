import pandas as pd
import csv
from datetime import datetime
from data_entry import get_date, get_amount, get_description, get_category
import matplotlib.pyplot as plt


class CSV:
  CSV_FILE = 'data.csv'
  COLUMNS = ['date', 'amount', 'description', 'category']
  FORMAT = '%d-%m-%Y'
  @classmethod
  def init_csv(cls):
    try:
      pd.read_csv(cls.CSV_FILE)
    except FileNotFoundError:
      df = pd.DataFrame(columns=cls.COLUMNS)
      df.to_csv(cls.CSV_FILE, index=False)

  @classmethod
  def add_entry(cls, date, amount, description, category):
    new_entry ={
      'date': date,
      'amount': amount,
      'description': description,
      'category': category
    }
    with open(cls.CSV_FILE, 'a', newline='') as f:
      writer = csv.DictWriter(f, fieldnames=cls.COLUMNS)
      writer.writerow(new_entry)
      print('Entry added successfully!')

  @classmethod
  def get_transactions(cls, start_date = '01-01-1900', end_date = '31-12-2100'):
    df = pd.read_csv(cls.CSV_FILE)
    df["date"] = pd.to_datetime(df['date'], format=cls.FORMAT)
    start_date = pd.to_datetime(start_date, format=cls.FORMAT)
    end_date = pd.to_datetime(end_date, format=cls.FORMAT)

    mask = (df['date'] >= start_date) & (df['date'] <= end_date)
    filtered_df = df.loc[mask] if start_date and end_date else df
    if filtered_df.empty:
      print('No transactions found for the given date range.')
      return pd.DataFrame(columns=cls.COLUMNS)
    else:
      print(f"Transactions from {start_date.strftime(cls.FORMAT)} to {end_date.strftime(cls.FORMAT)}:")
      print(filtered_df.to_string(index=False, formatters={'date': lambda x: x.strftime(cls.FORMAT)}))
      total_income = filtered_df[filtered_df['category'] == 'Income']['amount'].sum()
      total_expense = filtered_df[filtered_df['category'] == 'Expense']['amount'].sum()
      print("\n Summary:")
      print(f"Total Income: {total_income:.2f}")
      print(f"Total Expense: {total_expense:.2f}")
      print(f"Net Income: {total_income - total_expense:.2f}")
      return filtered_df

def add():
  date = get_date('Enter the date of the transaction (dd-mm-yyyy): ', allow_default=True)
  amount = get_amount()
  description = get_description()
  category = get_category()
  CSV.add_entry(date, amount, description, category)

def plot_transactions(df):
  df.set_index('date', inplace=True)
  incomw_df = df[df['category'] == 'Income'].resample('D').sum().reindex(df.index, fill_value=0)
  expense_df = df[df['category'] == 'Expense'].resample('D').sum().reindex(df.index, fill_value=0)
  plt.figure(figsize=(10, 5))
  plt.plot(incomw_df.index, incomw_df['amount'], label='Income', color='green')
  plt.plot(expense_df.index, expense_df['amount'], label='Expense', color='red')
  plt.xlabel('Date')
  plt.ylabel('Amount')
  plt.title('Income and Expense Over Time')
  plt.legend()
  plt.grid()
  plt.show()

def main():
  CSV.init_csv()
  while True:
    print("\nMenu:")
    print("1. Add a transaction")
    print("2. View transactions")
    print("3. Exit")
    choice = input("Enter your choice: ")
    if choice == '1':
      add()
    elif choice == '2':
      start_date = get_date('Enter the start date (dd-mm-yyyy): ', allow_default=True)
      end_date = get_date('Enter the end date (dd-mm-yyyy): ', allow_default=True)
      df = CSV.get_transactions(start_date, end_date)
      if input("Do you want to plot the transactions? (y/n): ").lower() == 'y':
        plot_transactions(df)
    elif choice == '3':
      print("Exiting the program.")
      break
    else:
      print("Invalid choice. Please try again.")
if __name__ == "__main__":
  main()