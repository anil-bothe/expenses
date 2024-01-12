# Expense Task - Teachmint


### Steps for running this application. 
1. pip install -r requirements.txt

2. create .env file (add var; DEBUG, SECRET_KEY, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)

3. python manage migrate

4. [http://127.0.0.1:8000/api/v1/signup/] 

    body:  <code>{
        "email": "test1@user.com",
        "mobile": "9876543210",
        "name": "test1",
        "password": "test1"
    }</code>

    You will get token.

5. Use token for following APIs

6. Make post request on this endpoint: [http://127.0.0.1:8000/api/v1/expense/list/] with following payloads 

-  for type <b>EQUAL</b>
    <code>
    {
        "amount": 1000,
        "participants": [7, 8],
        "payer": 7,
        "split_type": "EXACT"
    }
    </code>

-  for type <b>EXACT</b>
    <code>
    {
        "amount": 1000,
        "participants": [7, 8],
        "payer": 7,
        "split_type": "EXACT",
        "shares": {
            "7": 200,
            "8": 800
        }
    }   
    </code>

-  for type <b>PERCENT</b>
    <code>
    {
        "amount": 1000,
        "participants": [7, 8],
        "payer": 7,
        "split_type": "PERCENT",
        "shares": {
            "7": 30, # <- percentage
            "8": 70
        }
    }   
    </code>

###### API:
1. create expense[POST request]: [http://127.0.0.1:8000/api/v1/expense/list/]
1. get single expense: [http://127.0.0.1:8000/api/v1/expense/:id/]
2. get balance with user [http://127.0.0.1:8000/api/v1/balance/] # (authenticated user balance get shown)
3. get balance with SIMPLIFY [http://127.0.0.1:8000/api/v1/balance/?simplify=true]

#### Please find screenshots in postman folder; :) 

<!-- # Features/Requirements:
1. User: Each user should have a userId, name, email, mobile number.
2. Expense: Could either be EQUAL, EXACT or PERCENT
3. Users can add any amount, select any type of expense and split with any of the
   available users.
4. The percent and amount provided could have decimals upto two decimal places.
5. In case of percent, you need to verify if the total sum of percentage shares is 100 or not.
6. In case of exact, you need to verify if the total sum of shares is equal to the total amount
   or not.
7. The application should have a capability to show expenses for a single user as well as
   balances for everyone.
8. When asked to show balances, the application should show balances of a user with all
   the users where there is a non-zero balance.
9. The amount should be rounded off to two decimal places. Say if User1 paid 100 and
   amount is split equally among 3 people. Assign 33.34 to first person and 33.33 to
   others.
10. There should be an option to simplify expenses. When simplify expenses is turned on
    (is true), the balances should get simplified. Ex: ‘User1 owes 250 to User2 and User2
    owes 200 to User3’ should simplify to ‘User1 owes 50 to User2 and 200 to User3’.
11. When a new expense is added, each participant in that expense should get an
    email telling them that they have been added to an expense, the total amount they
    owe for that expense. This email should be sent asynchronously (non-blocking)
    so that the API call doesn't get blocked.
    And create a scheduled job that will send an email every week to users. This
    email should contain the total amount of money they owe to each user.
12. Each expense can have up to 1000 participants and the maximum amount for an
    expense can go up to INR 1,00,00,000/- -->
