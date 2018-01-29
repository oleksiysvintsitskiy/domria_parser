## Description
This is a [dom.ria.ua](https://dom.ria.com/) parser which parses selected state and gives **.xls** output about all realtors and individuals selling realties in selected state in the next format:
* name
* type (realtor or not)
* agency (if realtor)
* term (how long user has been working with dom.ria)
* offers (how many offers user has made)
* state
* city
* phone numbers
Works in 10 threads by default (THREADS_NUM variable in main.py).

## Usage
Enter id of state in **state_id.txt** file and run **main.py**.
