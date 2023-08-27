import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import pld
import datetime
import pytz

cred = credentials.Certificate('credentials.json')
firebase_admin.initialize_app(cred)

db = firestore.client()

users_ref = db.collection('users')

#function to add a collection called account to a user document given a document id
def create_new_user(user_id):
    user_ref = users_ref.document(user_id)
    #create a new collection called account with three fields - monthly budget, tab, start date (datetimeobject)
    user_ref.collection('account').document('account_data').set({
        'monthly_budget': 0,
        'tab': 0,
        'start_date': None,
        'access_token': ""
    })

def get_access_token(uid):
    return users_ref.document(uid).collection('account').document('account_data').get().to_dict()['access_token']

def read_ac(uid):
    return users_ref.document(uid).collection('account').document('account_data').get().to_dict()

def write_ac(uid, field_name, update_value):
    users_ref.document(uid).collection('account').document('account_data').update({str(field_name): update_value})

def refresh_account(uid):
    #output required: day balance & runway
    #first output: day balance
    #check whether a document field called account_balance exists
    access_token = users_ref.document(uid).collection('account').document('account_data').get().to_dict()['access_token']

    if not 'account_balance' in users_ref.document(uid).collection('account').document('account_data').get().to_dict():
        #if not, create missing fields for new user
        users_ref.document(uid).collection('account').document('account_data').update({
            'account_balance': pld.get_real_balance(access_token),
            'added_savings': 0
        })
    
    #calculate money spent from last time
    spent = read_ac(uid=uid)['account_balance'] - pld.get_real_balance(get_access_token(uid=uid))
    
    #write tab
    tab = read_ac(uid=uid)['tab']
    tab += spent
    write_ac(uid=uid, field_name='tab', update_value=tab)

    #calculate ideal spend: date_limit + added savings
    #calculate days_running, the number of the day it is from the beginning of the start date from account_data plus 1 day
    start_date = read_ac(uid=uid)['start_date']
    days_running = (datetime.datetime.now(pytz.UTC) - start_date).days + 1 

    #calculate daily limit, which is monthly budget divided by 30
    daily_limit = read_ac(uid=uid)['monthly_budget'] / 30
    #calculate ideal spend, which is daily limit multiplied by days running
    ideal_spend = daily_limit * days_running + read_ac(uid=uid)['added_savings']

    #calculate day balance, which is ideal spend minus tab
    day_balance = ideal_spend - tab

    #write day balance
    write_ac(uid=uid, field_name='day_balance', update_value=day_balance)




refresh_account('42xGhEiG9Fe0YZ2DAOBoFHTDEYF2')