import requests
import pywaves as pw
import time
from config import asset_to_parameters

def convert_to_traditional_units(asset_factor, balance_waves_units):
    return balance_waves_units / asset_factor

def convert_to_waves_units(asset_factor, balance_traditional_units):
    return balance_traditional_units * asset_factor

def get_asset_balance_waves_units(address, asset_id, node_url):
    asset_balance_waves_units = requests.get(f'{node_url}/assets/balance/{address}/{asset_id}').json()['balance']
    return asset_balance_waves_units

def get_lp_asset_balance_waves_units(owner_address_str, asset_address_str, node_url):
    asset_value = requests.get(f'{node_url}/addresses/data/{asset_address_str}/{owner_address_str}_aTokenBalance').json()['value']
    return asset_value

def convert_asset_lp_to_asset(lp_factor, asset_lp):
    return lp_factor * asset_lp

node_url = 'https://nodes.wavesnodes.com'
pw.setNode(node=node_url, chain='mainnet')

my_address_str = 'YOUR_ADDRESS'
my_address = pw.Address(privateKey='YOUR_PRIVATE_KEY') 

WAVES_CONVERSION_CST = 10 ** 8
WAVES_FEE_SC = int(0.005 * WAVES_CONVERSION_CST)


asset_name = 'USDC' #switch to "USDT" to withdraw USDT
asset_factor = asset_to_parameters[asset_name]["asset_factor"]  #10 ** 6 for USDC/USDT and 10 ** 8 for waves and btc
lp_factor = asset_to_parameters[asset_name]["lp_factor"]
vires_dapp_address_str = asset_to_parameters[asset_name]["dapp_address_str"] 
vires_asset_address_str =  asset_to_parameters[asset_name]["asset_address_str"] 
asset_id =  asset_to_parameters[asset_name]["asset_id"]
asset_lp_id = asset_to_parameters[asset_name]["asset_lp_id"]
min_amount_to_withdraw_traditional_units = 30

def job():
    asset_balance_on_vires_waves_units = convert_asset_lp_to_asset(lp_factor, get_lp_asset_balance_waves_units(my_address_str,\
                                                                            vires_asset_address_str , node_url) )
    asset_balance_withdrawn_waves_units = my_address.balance(assetId=asset_id, confirmations=0)
    vires_asset_balance_waves_units = get_asset_balance_waves_units(vires_asset_address_str, asset_id, node_url)
    

    asset_balance_to_withdraw_waves_units = min(vires_asset_balance_waves_units, asset_balance_on_vires_waves_units)
    asset_balance_to_withdraw_traditional_units = convert_to_traditional_units(asset_factor, asset_balance_to_withdraw_waves_units)

   
    print("waves balance: ", my_address.balance() / WAVES_CONVERSION_CST)
    print("asset name: ", asset_name)
    print("asset balance withdrawn: ", convert_to_traditional_units(asset_factor, asset_balance_withdrawn_waves_units))
    print("asset balance still to withdraw: ",  convert_to_traditional_units(asset_factor, asset_balance_on_vires_waves_units))
    print("dapp asset balance available: ", convert_to_traditional_units(asset_factor, vires_asset_balance_waves_units))
    print(f"amount of {asset_name} we can withdraw: ",  asset_balance_to_withdraw_traditional_units)
    print()
   
    if asset_balance_to_withdraw_traditional_units > min_amount_to_withdraw_traditional_units:
        tx = my_address.invokeScript(vires_dapp_address_str, 'withdraw',
                                     params=[{"type": "string", "value": asset_id},\
                                             {"type": "integer", "value": int(asset_balance_to_withdraw_waves_units)}],\
                                     payments=[{"amount": WAVES_FEE_SC, "assetId": None}])
        print(tx)

while True:
    try:
        job()
        time.sleep(0.01)
    except:
        continue

