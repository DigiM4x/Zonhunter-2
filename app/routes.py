from flask import Blueprint, render_template, request
import requests
import os
from app.models import Deal
from app import db

main = Blueprint('main', __name__)

@main.route('/', methods=['GET', 'POST'])
def index():
    deals = []
    if request.method == 'POST':
        discount = request.form.get('discount')
        free_shipping = request.form.get('free_shipping') == 'true'

        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {os.getenv("RAINFOREST_API_KEY")}'
        }

        params = {
            'type': 'search',
            'amazon_domain': 'amazon.com',
            'search_term': '',
            'filters[price_discount]': discount,
            'filters[prime_eligible]': free_shipping
        }

        response = requests.get('https://api.rainforestapi.com/request', headers=headers, params=params)
        data = response.json()
        deals = data.get('search_results', [])

        # Save deals to the database
        for deal in deals:
            new_deal = Deal(
                title=deal['title'],
                link=deal['link'],
                discount=deal['price']['discount'],
                free_shipping=free_shipping
            )
            db.session.add(new_deal)
        db.session.commit()

    # Retrieve all deals from the database
    deals = Deal.query.all()
    
    return render_template('index.html', deals=deals)
