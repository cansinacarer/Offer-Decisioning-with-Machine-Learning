# Starbucks Offer Analysis

## Background

**Project Overview:** Once every few days, Starbucks sends out an offer to users of the mobile app. An offer can be merely an advertisement for a drink or an actual offer such as a discount or BOGO (buy one get one free). Some users might not receive any offer during certain weeks. There are three types of offers that can be sent: buy-one-get-one (BOGO), discount, and informational. In a BOGO offer, a user needs to spend a certain amount to get a reward equal to that threshold amount. In a discount, a user gains a reward equal to a fraction of the amount spent. In an informational offer, there is no reward, but neither is there a requisite amount that the user is expected to spend. Offers can be delivered via multiple channels.

**Problem Statement**: We are given three data files which contain simulated data that mimics customer behavior on the Starbucks rewards mobile app. Our task is to use the data to identify which groups of people are most responsive to each type of offer, and how best to present each type of offer.

**Metrics**: In order to decide which offer should be presented to which customer, we need to know the offer that would influence a particular customer's spending behavior the most. Our metric in measuring this behavior difference will be `offer_influence`. This is calculated as the difference between the following two variables we derived from the event logs provided in the `transcript.json`:

-   `offer_spending_rate`: The daily average spending of a customer between when they viewed and offer and when that offer is expired.
-   `offer_spending_rate`: The daily average spending of a customer across all days when they have an valid offer and they had previously viewed it.

We hypothesize that the amount of this influence each offer has on spending amount is a function of the customer profile attributes and offer attributes.

    WHAT STATISTICAL METRICS USED TO MEASURE THE MODEL PERFORMANCE? Accuracy score and/or F-score?

## Data Preprocesing

The provided json files looked as below after initial reading with pandas:

![input_data](https://github.com/cansinacarer/API-Endpoint-Test/blob/main/img/input_data.jpg?raw=true)

We call each case a distinct offer is presented to a customer an "instance" of that offer. Part 1 of this analysis contains the data wrangling steps that aggregate the events with profile and offer attributes for each offer presented to each customer as below; so that the relationships between them can be investigated.

In the resulting dataset, each row also contains information derived from the event logs about the offer instance including when it is presented, when it is viewed, when it is expired, daily average amount the customer spent after viewing the offer, and how that compares to other periods.

Below is a transposed sample from this dataset

![offer-instance-clean](https://github.com/cansinacarer/API-Endpoint-Test/blob/main/img/offer-instance-clean.jpg?raw=true)

## Data Dictionary

### profile.json

Rewards program users (17000 users x 5 fields)

-   gender: (categorical) M, F, O, or null
-   age: (numeric) missing value encoded as 118
-   id: (string/hash)
-   became_member_on: (date) format YYYYMMDD
-   income: (numeric)

### portfolio.json

Offers sent during 30-day test period (10 offers x 6 fields)

-   reward: (numeric) money awarded for the amount spent
-   channels: (list) web, email, mobile, social
-   difficulty: (numeric) money required to be spent to receive reward
-   duration: (numeric) time for offer to be open, in days
-   offer_type: (string) bogo, discount, informational
-   id: (string/hash)

### transcript.json

Event log (306648 events x 4 fields)

-   person: (string/hash)
-   event: (string) offer received, offer viewed, transaction, offer completed
-   value: (dictionary) different values depending on event type
-   offer id: (string/hash) not associated with any "transaction"
-   amount: (numeric) money spent in "transaction"
-   reward: (numeric) money gained from "offer completed"
-   time: (numeric) hours after start of test
