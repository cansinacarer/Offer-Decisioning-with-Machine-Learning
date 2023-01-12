# Starbucks Offer Analysis

## Project Motivation

Once every few days, Starbucks sends out an offer to users of the mobile app. An offer can be merely an advertisement for a drink or an actual offer such as a discount or BOGO (buy one get one free). Some users might not receive any offer during certain weeks. There are three types of offers that can be sent: buy-one-get-one (BOGO), discount, and informational. In a BOGO offer, a user needs to spend a certain amount to get a reward equal to that threshold amount. In a discount, a user gains a reward equal to a fraction of the amount spent. In an informational offer, there is no reward, but neither is there a requisite amount that the user is expected to spend. Offers can be delivered via multiple channels.

## Problem Statement

We are given three data files which contain simulated data that mimics customer behavior on the Starbucks rewards mobile app. Our task is to use the data to identify which customer which receive which offer.

## Methodology

In order to decide which offer should be presented to which customer, we need to know which offer was presented to which customer during the experiment period and what the result was.

We call each case a distinct offer is presented to a customer a "presented offer". We have aggregated the events with profile and offer attributes for each offer presented to each customer as below; so that the relationships between them can be investigated.

We created a machine learning model that predicts the influence of a given offer on the spending behavior of a given customer, based on the offer and customer attributes. Then, we implemented this model in a web application so that when a user enters customer attributes, the application predicts influence of each offer for that customer and recommends the best one.

### Metrics

We define offer influence as the difference between the amount a customer spends during an offer and the baseline amount they spend in periods with no offer viewed. We called the metric for measuring this behavior difference `offer_influence`. It is calculated as the difference between the following two variables we derived from the event logs provided in the `transcript.json`:

-   `offer_spending_rate`: The daily average spending amount of a customer during the period after they have seen a given offer. This quantity is unique for each presented offer.
-   `average_no_offer_spending_rate`: The daily average spending amount of a customer across all days when they do have an valid offer or they have not seen the active offer they have. This quantity is unique for each customer.

We hypothesize that the amount of the influence each offer has on spending amount is a function of the customer profile attributes and offer attributes. We will try different regression algorithms to find this function and calculate the influence of future offers for a given set of customer and offer attributes.

We consider the average daily amount a customer spends without having seen any offers as the baseline. When the customer is presented with an offer, we consider them "influenced" only during the period between when they have viewed that offer until that offer expires.

## Data Preprocesing

The provided json files looked as below when first read with pandas:

| reward | channels                     | difficulty | duration | offer_type    | id                               |
| :----- | :--------------------------- | :--------- | :------- | :------------ | :------------------------------- |
| 10     | [email, mobile, social]      | 10         | 7        | bogo          | ae264e3637204a6fb9bb56bc8210ddfd |
| 10     | [web, email, mobile, social] | 10         | 5        | bogo          | 4d5c57ea9a6940dd891ad53e9dbe8da0 |
| 0      | [web, email, mobile]         | 0          | 4        | informational | 3f207df678b143eea3cee63160fa8bed |
| 5      | [web, email, mobile]         | 5          | 7        | bogo          | 9b98b8c7a33c4b65b9aebfe6a799e6d9 |
| 5      | [web, email]                 | 20         | 10       | discount      | 0b1e1539f2cc45b7b9fa7c272da2e1d7 |

| gender | age | id                               | became_member_on | income |
| :----- | :-- | :------------------------------- | :--------------- | :----- |
| M      | 44  | 1a6441a8ccd74a81a388841d357b8c0d | 20180108         | 67000  |
| M      | 62  | 81e459ab24434db99f657b928338c88c | 20171111         | 91000  |
| F      | 61  | fbb3c6ad80b04d3a94c666a2f08f2a2e | 20170916         | 96000  |
| F      | 85  | 19446b361caa43de84c2aed517457a47 | 20160927         | 103000 |
| O      | 42  | 8ead309bb7254edbab114c8837cd54b2 | 20170926         | 63000  |

| person                           | event          | value                                            | time |
| :------------------------------- | :------------- | :----------------------------------------------- | :--- |
| e69130c406cf4e3fbb0168b535309b96 | offer received | {'offer id': '9b98b8c7a33c4b65b9aebfe6a799e6d9'} | 0    |
| 23bc15e276d247669fd7d1c08a8fb678 | offer viewed   | {'offer id': 'f19421c1d4aa40978ebb69ca19b0e20d'} | 144  |
| bafc2350ece84692b0db74a6130a213c | transaction    | {'amount': 4.17}                                 | 234  |
| f2b3ad312ea343f483ea8a3db41b3a47 | transaction    | {'amount': 0.85}                                 | 666  |
| 7ffb3bc618ad453b9bce311ec88e481d | offer viewed   | {'offer id': 'fafdcd668e3743c1bb461111dcafc2a4'} | 366  |

In the resulting dataset, each row also contains information derived from the event logs about the presented offer including when it is presented, when it is viewed, when it is expired, daily average amount the customer spent after viewing the offer, and how that compares to other periods.

### Data Preprocesing Result
Below is a transposed sample from the aggregated dataset with variables derived from the tables above.

![offer-instance-clean](https://github.com/cansinacarer/Offer-Decisioning-with-Machine-Learning/blob/main/img/presented-offers-clean.jpg?raw=true)

## Modeling

We have used offer attributes and customer profile attributes shown in the image above as independent variables and the offer influence as the dependent variable. The algorithms we have tested and their performances are shown below.

|                                        | Mean Absolute Error (MAE) | Mean Squared Error (MSE) | Root Mean Square Error (RMSE) | Explained Variance (R^2 Score) |
| :------------------------------------- | :------------------------ | :----------------------- | :---------------------------- | :----------------------------- |
| CatBoost Regressor                     | 3.186                     | 55.833                   | 1.785                         | 0.407                          |
| Bayesian Ridge Regression              | 3.186                     | 55.833                   | 1.785                         | 0.407                          |
| Linear Regression                      | 3.187                     | 55.840                   | 1.785                         | 0.407                          |
| Elastic Net Regression                 | 3.230                     | 56.228                   | 1.797                         | 0.403                          |
| Gradient Boosting Regressor            | 3.243                     | 63.045                   | 1.801                         | 0.331                          |
| Light GBM Regressor                    | 3.293                     | 71.057                   | 1.815                         | 0.246                          |
| Random Forest Regressor                | 3.711                     | 78.179                   | 1.926                         | 0.170                          |
| MLP Regressor                          | 5.645                     | 78.726                   | 2.376                         | 0.165                          |
| XGBoost Regressor                      | 3.423                     | 87.035                   | 1.850                         | 0.076                          |
| Support Vector Regressor               | 4.371                     | 93.839                   | 2.091                         | 0.004                          |
| Decision Tree Regressor                | 4.670                     | 150.574                  | 2.161                         | -0.598                         |
| Stochastic Gradient Descent Regression | 4.26E+17                  | 2.00E+35                 | 652480033.3                   | -2.12E+33                      |

We have chosen CatBoost Regressor as it performed the best against all of our metrics. Based on the Mean Absolute Error of this model, it will be able to predict the `offer_influence` with an average of $3.18 error for any given set of profile attributes and offer attributes.

### Model Implementation: Web Application

We have implemented the selected model in an offer decisioning web application. This application allows the user to input a customer profile details and the application shows the user the offer that has the highest predicted influence for that profile.

This application is deployed at [https://offer-decisioning-starbucks.montreal.cansin.net](https://offer-decisioning-starbucks.montreal.cansin.net). You can see the code for this application in the `web-application` directory of this repository.

The deployed application is runs the latest version from this repository using a continuous deployment pipeline.

## Other Notes

- Please see the notebook file for the steps of this analysis and the conclusions.

- This project is submitted in partial fulfillment of the Data Scientist Nanodegree Program from Udacity.

### Running the Web Application and the Notebook

If you want to test it locally, navigate into the web-application folder, create and activate a virtual environment, install dependencies from `requirements.txt`, then run `run.py` and open to the URL shown in the terminal in a browser.

While running the notebook, make sure you have the virtual environment selected as the kernel.

### Data Dictionary

#### profile.json

Rewards program users (17000 users x 5 fields)

-   gender: (categorical) M, F, O, or null
-   age: (numeric) missing value encoded as 118
-   id: (string/hash)
-   became_member_on: (date) format YYYYMMDD
-   income: (numeric)

#### portfolio.json

Offers sent during 30-day test period (10 offers x 6 fields)

-   reward: (numeric) money awarded for the amount spent
-   channels: (list) web, email, mobile, social
-   difficulty: (numeric) money required to be spent to receive reward
-   duration: (numeric) time for offer to be open, in days
-   offer_type: (string) bogo, discount, informational
-   id: (string/hash)

#### transcript.json

Event log (306648 events x 4 fields)

-   person: (string/hash)
-   event: (string) offer received, offer viewed, transaction, offer completed
-   value: (dictionary) different values depending on event type
-   offer id: (string/hash) not associated with any "transaction"
-   amount: (numeric) money spent in "transaction"
-   reward: (numeric) money gained from "offer completed"
-   time: (numeric) hours after start of test
