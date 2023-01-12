# Starbucks Offer Analysis

## Project Motivation

Once every few days, Starbucks sends out an offer to users of the mobile app. An offer can be merely an advertisement for a drink or an actual offer such as a discount or BOGO (buy one get one free). Some users might not receive any offer during certain weeks. There are three types of offers that can be sent: buy-one-get-one (BOGO), discount, and informational. In a BOGO offer, a user needs to spend a certain amount to get a reward equal to that threshold amount. In a discount, a user gains a reward equal to a fraction of the amount spent. In an informational offer, there is no reward, but neither is there a requisite amount that the user is expected to spend. Offers can be delivered via multiple channels.

## Problem Statement

We are given three data files which contain simulated data that mimics customer behavior on the Starbucks rewards mobile app. Our task is to use the data to identify which groups of people are most responsive to each type of offer, and how best to present each type of offer.

## Methodology

In order to decide which offer should be presented to which customer, we need to know which offer was presented to which customer during the experiment period and what the result was; so that we can predict the offer that would influence a customer's spending behavior the most.

We call each case a distinct offer is presented to a customer a "presented offer". We have aggregated the events with profile and offer attributes for each offer presented to each customer as below; so that the relationships between them can be investigated.

### Metrics

We define offer influence as the difference between the amount a customer spends during an offer and the baseline amount they spend in periods with no offer viewed. We called the metric for measuring this behavior difference `offer_influence`. It is calculated as the difference between the following two variables we derived from the event logs provided in the `transcript.json`:

-   `offer_spending_rate`: The daily average spending amount of a customer during the period after they have seen a given offer. This quantity is unique for each presented offer.
-   `average_no_offer_spending_rate`: The daily average spending amount of a customer across all days when they do have an valid offer or they have not seen the active offer they have. This quantity is unique for each customer.

We hypothesize that the amount of the influence each offer has on spending amount is a function of the customer profile attributes and offer attributes. We will try different regression algorithms to find this function and calculate the influence of future offers for a given set of customer and offer attributes.

We consider the average daily amount a customer spends without having seen any offers as the baseline. When the customer is presented with an offer, we consider them "influenced" only during the period between when they have viewed that offer until that offer expires.

## Data Preprocesing

The provided json files looked as below after initial reading with pandas:

![input_data](https://github.com/cansinacarer/Offer-Decisioning-with-Machine-Learning/blob/main/img/input_data.jpg?raw=true)

In the resulting dataset, each row also contains information derived from the event logs about the presented offer including when it is presented, when it is viewed, when it is expired, daily average amount the customer spent after viewing the offer, and how that compares to other periods.

Below is a transposed sample from this dataset

![offer-instance-clean](https://github.com/cansinacarer/Offer-Decisioning-with-Machine-Learning/blob/main/img/offer-instance-clean.jpg?raw=true)

## Modeling

We have used offer attributes and customer profile attributes shown in the image above as independent variables and the offer influence as the dependent variable. The algorithms we have tested and their performances are shown below.


## Model Implementation: Web Application

A continuous deployment pipeline is set up to always have the version of the web application seen in this repository be running at this address:
[https://offer-decisioning-starbucks.montreal.cansin.net/](https://offer-decisioning-starbucks.montreal.cansin.net/).

## Conclusion

## Other Notes

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
