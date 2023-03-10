import pandas as pd
from flask import Flask, render_template, request
from wtforms import (
    Form,
    validators,
    IntegerField,
    StringField,
    FloatField,
)
import predictor

app = Flask(__name__)


class CustomerAttributesForm(Form):
    customer_age = IntegerField(
        "Customer Age",
        [validators.NumberRange(min=0, max=120), validators.InputRequired()],
    )
    customer_income = IntegerField(
        "Customer Income",
        [validators.NumberRange(min=0, max=10000000), validators.InputRequired()],
    )
    customer_profile_age = IntegerField(
        "Customer Profile Age",
        [validators.NumberRange(min=0, max=36500), validators.InputRequired()],
    )
    customer_gender = StringField("Gender")
    customer_total_spending = IntegerField(
        "Customer Total Spending",
        [validators.NumberRange(min=0, max=1000000), validators.InputRequired()],
    )
    customer_total_no_offer_spending = IntegerField(
        "Customer Total No Offer Spending",
        [validators.NumberRange(min=0, max=1000000), validators.InputRequired()],
    )
    customer_total_offer_spending = IntegerField(
        "Customer Total Offer Spending",
        [validators.NumberRange(min=0, max=1000000), validators.InputRequired()],
    )
    customer_days_without_offer = IntegerField(
        "Customer Days Without Offer",
        [validators.NumberRange(min=0, max=30), validators.InputRequired()],
    )
    customer_days_with_offer = IntegerField(
        "Customer Days With Offer",
        [validators.NumberRange(min=0, max=30), validators.InputRequired()],
    )
    customer_average_no_offer_spending_rate = FloatField(
        "Customer Average No Offer Spending Rate",
        [validators.NumberRange(min=0, max=1000), validators.InputRequired()],
    )
    customer_average_offer_spending_rate = FloatField(
        "Customer Average Offer Spending Rate",
        [validators.NumberRange(min=0, max=1000), validators.InputRequired()],
    )


@app.route("/", methods=["get", "post"])
def index():
    form = CustomerAttributesForm(request.form)

    if request.method == "POST" and form.validate():
        # Read the form inputs
        customer_fields = request.form.to_dict()

        # Convert html select options to model's binary variables
        customer_fields["customer_gender_M"] = (
            1 if customer_fields["customer_gender"] == "male" else 0
        )
        customer_fields["customer_gender_F"] = (
            1 if customer_fields["customer_gender"] == "female" else 0
        )

        # Remove the old gender variable that came from html select
        customer_fields.pop("customer_gender")

        # Save predictions to a temporary copy of the offers list
        try:
            del temp_offers
        except:
            pass
        temp_offers = predictor.offers
        offer_influence = []
        for offer in temp_offers:
            offer_influence.append(
                predictor.predict_from_request(offer, customer_fields)
            )

        # Add the result to the dictionary that builds the offers table
        for i, offer in enumerate(temp_offers):
            offer["offer_influence"] = offer_influence[i]

        index_of_best_offer = offer_influence.index(max(offer_influence))
        best_offer = temp_offers[index_of_best_offer]["offer_id"]

        message = (
            "success",
            f"Based on predicted offer influences, the best offer for a customer with the given attributes is {best_offer}.<br />Please scroll to the right end side of the table below to see the predicted offer influences that would result if the offer in that row is presented to that customer.",
        )
        return render_template(
            "index.html", offers=temp_offers, message=message, form=form
        )

    message = (
        "primary",
        "Based on the customer attributes you input, this program will predict the influences of the offers listed in the table below and return the best of these offers for the customer with the attributes above.",
    )
    return render_template(
        "index.html", offers=predictor.offers, message=message, form=form
    )


def main():
    app.run(host="0.0.0.0", debug=True)


if __name__ == "__main__":
    main()
