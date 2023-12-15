import urllib.request as url_request
import json
import requests


HYPIXEL_API = 'https://api.hypixel.net/v2'
COFLNET_API = 'https://sky.coflnet.com/api'

TAX = 0.01125


def get_bazaar_data():
    # Get the bazaar data from the hypixel API
    website = url_request.urlopen(HYPIXEL_API + '/skyblock/bazaar')
    content = website.read()

    data = json.loads(content)

    return data


def get_all_items():
    # Get all item datas from the Hypixel API
    website = url_request.urlopen(HYPIXEL_API + '/resources/skyblock/items')
    content = website.read()

    data = json.loads(content)

    return data


def get_sellable_items():
    # Get all items which can be sold to the npc
    item_data = get_all_items()

    all_items = item_data['items']

    sellable_items = {}

    for item in all_items:
        if 'npc_sell_price' in item:
            item_id = item['id']
            item_price = item['npc_sell_price']

            sellable_items[item_id] = item_price

    return sellable_items


def sort_and_output_results(data_list, print_output, show=3, custom_message=False, main_message_part='', show_profit_coins=False):
    # If the list is empty then return nothing and
    if len(data_list) == 0:
        if print_output:
            print('Empty list')
        return

    # This sorts the list using the first element of each list inside the list
    sorted_data = sorted(data_list, reverse=True)

    # If the output shouldn't be printed, then return the sorted list
    if not print_output:
        return sorted_data

    # Define the message
    if custom_message:
        general_message = main_message_part

    else:
        suffix = ' coins profit per item' if show_profit_coins else '% profit'

        general_message = f'{{place}}. Product for {main_message_part} is: {{item}} with {{profit}}{suffix}'  # Replace the not product specific values

    # Go through each wanted element
    for i in range(show):
        try:  # If the list is shorter than the number of wanted items
            # Calculate all output data for the element
            place_number = i + 1
            item_id = sorted_data[i][1]
            profit = round(sorted_data[i][0] * 10) / 10  # Round the profit number to one decimal place (Multiply with 10, round, divide by 10)

            # If the element's profit is greater than 0 then replace all the values in the message and print the message.
            if profit > 0:
                print(general_message.format(place=place_number, item=item_id, profit=profit))

            else:
                # This means the profit is small
                if i == 0:
                    print('No values found')

                break

        except IndexError:
            break


def get_bazaar_investment_and_return(product_data, instant):
    if instant:
        coins_invest = product_data['buy_summary'][0]['pricePerUnit']  # Coins to invest using buy order (which is the sell_summary price)
        coins_get = product_data['sell_summary'][0]['pricePerUnit'] * 0.98875  # This is multiplied with 0.98875 because there is 1.125 % tax which the seller gets subtracted from the actual price

    else:
        # Get the profit
        coins_invest = product_data['sell_summary'][0]['pricePerUnit']  # Coins to invest using buy order (which is the sell_summary price)
        coins_get = product_data['buy_summary'][0]['pricePerUnit'] * 0.98875  # This is multiplied with 0.98875 because there is 1.125 % tax which the seller gets subtracted from the actual price

    return coins_invest, coins_get


""""
The different money making methods
"""


# TODO Use the numberOfMovingWeek to show how fast the item should be bought and use "sellOrders" and "buyOrders" to show how popular this flip is
def bazaar_flipping(instant=False, show=3, show_profit_coins=False, print_output=True):
    bazaar_data = get_bazaar_data()
    all_bazaar_items = bazaar_data['products']

    profits_and_item_ids = []

    for item in all_bazaar_items.values():
        item_id = item['product_id']

        try:
            coins_invest, coins_get = get_bazaar_investment_and_return(item, instant)

            profit_coins = coins_get - coins_invest

            if show_profit_coins:
                profit = profit_coins

            else:
                profit_percentage = (profit_coins / coins_invest) * 100
                profit = profit_percentage

            if not item_id.startswith('ENCHANTMENT_'):
                # Add the items to the list. The list is sorted afterward.
                profits_and_item_ids.append([profit, item_id])

        except IndexError:
            pass

    message = f'bazaar flipping {"instant" if instant else "order"}'
    sort_and_output_results(profits_and_item_ids, print_output, show=show, main_message_part=message, show_profit_coins=show_profit_coins)


def bazaar_to_npc(instant=False, show=3, show_profit_coins=False, print_output=True):
    # Get the data
    sellable_items = get_sellable_items()

    # Analyze the bazaar data
    bazaar_data = get_bazaar_data()
    all_bazaar_items = bazaar_data['products']
    bazaar_item_ids = list(all_bazaar_items.keys())

    profits_and_item_ids = []

    # Go through
    for item_id in sellable_items.keys():
        if item_id in bazaar_item_ids:
            try:
                coins_invest, _ = get_bazaar_investment_and_return(all_bazaar_items[item_id], instant)

                coins_get = sellable_items[item_id]  # This doesn't need to be multiplied with 0.98875 because there is no tax on npc prices

                # Calculate and output the wanted profit
                profit_coins = coins_get - coins_invest

                if show_profit_coins:
                    profit = profit_coins

                else:
                    profit_percentage = (profit_coins / coins_invest) * 100
                    profit = profit_percentage

                if not item_id.startswith('PERFECT_'):
                    # Add the items to the list. The list is sorted afterward.
                    profits_and_item_ids.append([profit, item_id])

            except IndexError:
                pass

    message = f'bazaar {"instant" if instant else "order"} to npc'
    sort_and_output_results(profits_and_item_ids, print_output, show=show, main_message_part=message, show_profit_coins=show_profit_coins)


def bazaar_crafting_profit(coflnet=True, instant=False, show=3, show_profit_coins=False, print_output=True):
    bazaar_data = get_bazaar_data()
    all_bazaar_items = bazaar_data['products']

    profits_and_item_ids = []

    if coflnet:
        crafting_profit_data = requests.get(COFLNET_API + '/craft/profit').json()

        all_bazaar_item_ids = []

        for item in all_bazaar_items.values():
            item_id = item['product_id']

            all_bazaar_item_ids.append(item_id)

        for item in crafting_profit_data:
            item_id = item['itemId']

            if item_id in all_bazaar_item_ids:
                coins_get = item['sellPrice']
                coins_invest = item['craftCost']

                profit_coins = coins_get - coins_invest

                if show_profit_coins:
                    profit = profit_coins

                else:
                    profit_percentage = (profit_coins / coins_invest) * 100
                    profit = profit_percentage

                profits_and_item_ids.append([profit, item_id])

        message = f'bazaar crafting instant'
        sort_and_output_results(profits_and_item_ids, print_output, show=show, main_message_part=message, show_profit_coins=show_profit_coins)


def kat_profit(max_cost, show):
    kat_profit_data = requests.get(COFLNET_API + '/kat/profit').json()

    profits_and_pet_datas = []

    for pet_data in kat_profit_data:
        profit = pet_data['profit']

        pet_name = pet_data['originAuctionName']
        purchase_cost = pet_data['purchaseCost']
        target_rarity = pet_data['targetRarity']
        upgrade_cost = pet_data['upgradeCost'] + pet_data['materialCost']
        sell_cost = pet_data['median']

        total_cost = purchase_cost + upgrade_cost

        if total_cost <= max_cost:
            profits_and_pet_datas.append([profit, pet_name, purchase_cost, target_rarity, upgrade_cost, sell_cost])

    sorted_profits_and_pet_datas = sorted(profits_and_pet_datas, key=lambda x: x[0], reverse=True)

    for index, profit_and_pet_data in enumerate(sorted_profits_and_pet_datas[:show]):
        place = index + 1

        data = profit_and_pet_data

        print(f'{place}. {int(data[0])} coins profit by buying {data[1]} for {data[2]} coins and upgrade to {data[3]} for {int(data[4])} and selling it for {data[5]}')


if __name__ == '__main__':
    action = input('Kat Pet Sitting (k) / Bazaar flipping (f) / Bazaar to NPC (n) / Bazaar crafting (c): ').lower()

    selection_show = input('Show how many objects: ')
    try:
        selection_show = int(selection_show)
    except ValueError:
        selection_show = 20

    if action == 'k':
        selection_max_cost = input('Max cost: ')
        try:
            selection_max_cost = int(selection_max_cost)
        except ValueError:
            selection_max_cost = 10_000_000

        kat_profit(max_cost=selection_max_cost, show=selection_show)

    else:
        selection_instant = input('Instant: YES (y) / No (n): ').lower()
        if selection_instant == 'n':
            selection_instant = False
        else:
            selection_instant = True

        selection_profit_coins = input('Show profit in coins: YES (y) / No (n): ').lower()
        if selection_profit_coins == 'n':
            selection_profit_coins = False
        else:
            selection_profit_coins = True

        if action == 'f':
            bazaar_flipping(instant=selection_instant, show=selection_show, show_profit_coins=selection_profit_coins)
        elif action == 'n':
            bazaar_to_npc(instant=selection_instant, show=selection_show, show_profit_coins=selection_profit_coins)
        elif action == 'c':
            bazaar_crafting_profit(instant=selection_instant, show=selection_show, show_profit_coins=selection_profit_coins)
        else:
            print(f'Unrecognised action: {action}')
