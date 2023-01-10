import pandas as pd
from flask import Flask
from flask import render_template, request

import predictor


app = Flask(__name__)


@app.route("/", methods=["get", "post"])
def index():
    if request.method == "POST":
        # Save predictions to a temporary copy of the offers list
        temp_offers = predictor.offers
        offer_influence = []
        for offer in temp_offers:
            offer_influence.append(
                predictor.predict_from_request(offer, request.form.to_dict())
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
        return render_template("index.html", offers=temp_offers, message=message)

    message = (
        "primary",
        "Based on the customer attributes you input, this program will predict the influences of the offers listed in the table below and return the best of these offers for the customer with the attributes above.",
    )
    return render_template("index.html", offers=predictor.offers, message=message)


def main():
    app.run(host="0.0.0.0", debug=True)


if __name__ == "__main__":
    main()
