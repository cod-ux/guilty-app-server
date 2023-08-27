#for creating client
import plaid
from plaid.api import plaid_api as Connect
from flask import Flask
import json
import datetime
import calendar

#parameters of link request obj
from plaid.model.products import Products 
from plaid.model.country_code import CountryCode 
from plaid.model.link_token_create_request_user import LinkTokenCreateRequestUser 

#to create exchange request
from plaid.model.item_public_token_exchange_request import ItemPublicTokenExchangeRequest as exc_request 

from plaid.model.item_webhook_update_request import ItemWebhookUpdateRequest
from plaid.model.transactions_refresh_request import TransactionsRefreshRequest
from plaid.model.accounts_balance_get_request import AccountsBalanceGetRequest


public_token = 'public-development-98f5f9a7-e038-4e79-8f2d-046a545c173e'
#access_token = "access-development-bfe6171e-82dc-44cb-a02e-780b738d17b1" 

# fields to populate: account_balance, tab, day_add
# additional fields used: monthly_budget, start_date
# output: day_balance, runway



def get_real_balance(access_token):
    configuration = plaid.Configuration(
    host = plaid.Environment.Development,
    api_key = {
        'clientId': '6377de812443a60012a4c1db',
        'secret': 'e978853789ea98468172615b7a807e',
    }
    )

    api_config = plaid.ApiClient(configuration)
    client = Connect.PlaidApi(api_config)

    request = AccountsBalanceGetRequest(access_token=access_token)
    response = client.accounts_balance_get(request)
    accounts = response['accounts']
    return accounts[-1].to_dict()['balances']['available']

