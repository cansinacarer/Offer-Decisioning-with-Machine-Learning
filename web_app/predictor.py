import pandas as pd
import joblib
import os


# Load the pickled model
base_dir = os.path.dirname(__file__)  # Path to loader.py
pickled_model = os.path.join(base_dir, "model.pkl")
model = joblib.load(pickled_model)

# Available offers
offers = [
    {
        "offer_id": "9b98b8c7a33c4b65b9aebfe6a799e6d9",
        "offer_reward": 5,
        "offer_difficulty": 5,
        "offer_duration": 168,
        "channel_email": 1,
        "channel_mobile": 1,
        "channel_social": 0,
        "channel_web": 1,
        "offer_type_bogo": 1,
        "offer_type_discount": 0,
        "offer_type_informational": 0,
    },
    {
        "offer_id": "2906b810c7d4411798c6938adc9daaa5",
        "offer_reward": 2,
        "offer_difficulty": 10,
        "offer_duration": 168,
        "channel_email": 1,
        "channel_mobile": 1,
        "channel_social": 0,
        "channel_web": 1,
        "offer_type_bogo": 0,
        "offer_type_discount": 1,
        "offer_type_informational": 0,
    },
    {
        "offer_id": "f19421c1d4aa40978ebb69ca19b0e20d",
        "offer_reward": 5,
        "offer_difficulty": 5,
        "offer_duration": 120,
        "channel_email": 1,
        "channel_mobile": 1,
        "channel_social": 1,
        "channel_web": 1,
        "offer_type_bogo": 1,
        "offer_type_discount": 0,
        "offer_type_informational": 0,
    },
    {
        "offer_id": "0b1e1539f2cc45b7b9fa7c272da2e1d7",
        "offer_reward": 5,
        "offer_difficulty": 20,
        "offer_duration": 240,
        "channel_email": 1,
        "channel_mobile": 0,
        "channel_social": 0,
        "channel_web": 1,
        "offer_type_bogo": 0,
        "offer_type_discount": 1,
        "offer_type_informational": 0,
    },
    {
        "offer_id": "ae264e3637204a6fb9bb56bc8210ddfd",
        "offer_reward": 10,
        "offer_difficulty": 10,
        "offer_duration": 168,
        "channel_email": 1,
        "channel_mobile": 1,
        "channel_social": 1,
        "channel_web": 0,
        "offer_type_bogo": 1,
        "offer_type_discount": 0,
        "offer_type_informational": 0,
    },
    {
        "offer_id": "3f207df678b143eea3cee63160fa8bed",
        "offer_reward": 0,
        "offer_difficulty": 0,
        "offer_duration": 96,
        "channel_email": 1,
        "channel_mobile": 1,
        "channel_social": 0,
        "channel_web": 1,
        "offer_type_bogo": 0,
        "offer_type_discount": 0,
        "offer_type_informational": 1,
    },
    {
        "offer_id": "fafdcd668e3743c1bb461111dcafc2a4",
        "offer_reward": 2,
        "offer_difficulty": 10,
        "offer_duration": 240,
        "channel_email": 1,
        "channel_mobile": 1,
        "channel_social": 1,
        "channel_web": 1,
        "offer_type_bogo": 0,
        "offer_type_discount": 1,
        "offer_type_informational": 0,
    },
    {
        "offer_id": "4d5c57ea9a6940dd891ad53e9dbe8da0",
        "offer_reward": 10,
        "offer_difficulty": 10,
        "offer_duration": 120,
        "channel_email": 1,
        "channel_mobile": 1,
        "channel_social": 1,
        "channel_web": 1,
        "offer_type_bogo": 1,
        "offer_type_discount": 0,
        "offer_type_informational": 0,
    },
    {
        "offer_id": "2298d6c36e964ae4a3e7e9706d1fb8c2",
        "offer_reward": 3,
        "offer_difficulty": 7,
        "offer_duration": 168,
        "channel_email": 1,
        "channel_mobile": 1,
        "channel_social": 1,
        "channel_web": 1,
        "offer_type_bogo": 0,
        "offer_type_discount": 1,
        "offer_type_informational": 0,
    },
    {
        "offer_id": "5a8bc65990b245e5a138643cd4eb9837",
        "offer_reward": 0,
        "offer_difficulty": 0,
        "offer_duration": 72,
        "channel_email": 1,
        "channel_mobile": 1,
        "channel_social": 1,
        "channel_web": 0,
        "offer_type_bogo": 0,
        "offer_type_discount": 0,
        "offer_type_informational": 1,
    },
]

# Predict with the customer attributes received from the form
def predict_from_request(offer, request):

    # Merge the offer attributes with profile attributes
    offer.update(request)

    # Put the merged dictionary in a dataframe
    dfx = pd.DataFrame(offer, index=[0])

    # Reorder the columns of the dataframe to put binary variables for gender in the order the model expects
    dfx = dfx[
        [
            "offer_reward",
            "offer_difficulty",
            "offer_duration",
            "channel_email",
            "channel_mobile",
            "channel_social",
            "channel_web",
            "offer_type_bogo",
            "offer_type_discount",
            "offer_type_informational",
            "customer_age",
            "customer_income",
            "customer_profile_age",
            "customer_gender_M",
            "customer_gender_F",
            "customer_total_spending",
            "customer_total_no_offer_spending",
            "customer_total_offer_spending",
            "customer_days_without_offer",
            "customer_days_with_offer",
            "customer_average_no_offer_spending_rate",
            "customer_average_offer_spending_rate",
        ]
    ]

    # Final set of independent predictors
    x = dfx.to_numpy()

    # Prediction
    return model.predict(x)[0]
