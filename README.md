# Instacart shopper challenge

## Goal
 To build a shopper registration web application to sign-up shoppers. This challenge is broken into two parts. The first part is implementing the public-facing site that a prospective Instacart Shopper would see when hearing about the opportunities that Instacart offers. The second is writing analytics to monitor the progress of shoppers through the hiring funnel.
You can either install the webapp by following method or check it online at https://frozen-shore-75994.herokuapp.com/shopper/

## Requirements
``` python  -- 2.7.9```
``` django  -- 1.11```
``` sqlite3 -- 2.6.0```
## Installation
* ``` git clone https://github.com/asmita0917/instacart_shopper_challenge.git ```
* ``` cd instacart_shopper_challenge/instaCart ```
* ``` python manage.py makemigrations ```
* ``` python manage.py migrate ```
If you want to seed database with random data then --
* ``` python manage.py populate_db <number of entries> ```
The number of entries is optional, and it defaults to 1000 if not present.
Then run the server --
* ```python manage.py runserver```
And go to url --
* ```http://127.0.0.1:8000/shopper/```

## APIs exposed by App
1. The web application exposes basic APIs for register, login, logout, editing an application. Following are those APIs --
* http://127.0.0.1:8000/shopper/register
* http://127.0.0.1:8000/shopper/login
* http://127.0.0.1:8000/shopper/logout
* http://127.0.0.1:8000/shopper/edit
   
2. We also expose an analytics api to monitor the progress of shoppers. This API returns the status of weekly shopper application grouped by workflow state count. This can be accessed by --
 * http://127.0.0.1:8000/shopper/funnel/?start_date=START_DATE&end_date=END_DATE
    The dates must follow the YYYY-MM-DD format. Eg -
* http://127.0.0.1:8000/shopper/funnel/?start_date=2010-10-01&end_date=2014-12-31

## Design Decisions
* I wrote a custom command to populate database with random inputs. It was difficult to generate unique random emails, and hence used generators. Even then during my testing I was getting duplicate entries after 60-70k entries, and hence added retry code.
* With 100,000 entries in database, funnel report generation was taking 0.256750106812 seconds. So I added django's default mem-cache which sped up things. I was able to retrieve same query in 0.00718402862549 seconds, approximately 35 times faster.
* The cache is using week as key, and hence only 54 entries per year is required. Currently cache is invalidated only on new user registration as there is no other way of altering an application state. Once such API is written, the cache needs to be invalidated from that API as well. With so much cache invalidation, the efficiency of using cache might diminish. Hence, instead of invalidating the entire cache, we can update the cache.
* Currently database is not designed keeping scale and analytics in mind. Efficient database design with indexing and partitioning would help. Also sqlite is good for development, for actual production use we should use MySQL or PostgreSQL on multiple nodes with load balancers.


## TODO
* Add authentication
* Add better error handling
* Improve front-end
* Add unit-tests

