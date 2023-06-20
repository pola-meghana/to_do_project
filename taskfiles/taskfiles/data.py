import csv
import random
import random
from datetime import datetime, timedelta

def generate_random_date(start_date, end_date):
    # Convert start_date and end_date strings to datetime objects
    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d")
    
    # Calculate the difference between start_date and end_date
    delta = end_date - start_date
    
    # Generate a random number of days within the date range
    random_days = random.randrange(delta.days + 1)
    
    # Add the random number of days to the start_date
    random_date = start_date + timedelta(days=random_days)
    
    return random_date.strftime("%Y-%m-%d")



sNO = []
customerId = []
category = ["Shopping","Travel","Food","Groceries","Utility Bills","Investments"]
modeOfPayments = ["Credit Card","Debit Card","Net Banking","UPI","Cash","Wallet"]
amountSpent = []
date = []

f=open('data_for_database.csv',mode='w')
writer=csv.writer(f)
writer.writerow(['S.NO','Customer Id','Category','Mode of Payment','Amount Spent','Date'])
for i in range(1000):
    x=random.uniform(1600,20000)
    y=round(x,4)
    random_date = generate_random_date("2023-01-01", "2023-12-31")

    writer.writerow([i+1,random.randint(7000,8010),random.choice(category),random.choice(modeOfPayments),y,random_date])
f.close()



# writer.writerow([i['name'],i['age'],i['job_title'],i['dept_name'],i['salary']])
# print(random.uniform(10.5, 75.5))
# y = round(x, 2)