from pgoapi.protos.pogoprotos.inventory.item.item_id_pb2 import ITEM_UNKNOWN, \
    ITEM_X_ATTACK, ITEM_X_DEFENSE, ITEM_X_MIRACLE, \
    ITEM_POKEMON_STORAGE_UPGRADE, ITEM_ITEM_STORAGE_UPGRADE


def parse_inventory_delta(inv_response):
    inventory_items = inv_response.get('inventory_delta', {}).get(
        'inventory_items', [])
    inventory = {}
    no_item_ids = (
        ITEM_UNKNOWN,
        #ITEM_TROY_DISK,
        ITEM_X_ATTACK,
        ITEM_X_DEFENSE,
        ITEM_X_MIRACLE,
        ITEM_POKEMON_STORAGE_UPGRADE,
        ITEM_ITEM_STORAGE_UPGRADE
    )
    for item in inventory_items:
        iid = item.get('inventory_item_data', {})
        if 'item' in iid and iid['item']['item_id'] not in no_item_ids:
            item_id = iid['item']['item_id']
            count = iid['item'].get('count', 0)
            inventory[item_id] = count
        elif 'egg_incubators' in iid and 'egg_incubator' in iid['egg_incubators']:
            for incubator in iid['egg_incubators']['egg_incubator']:
                item_id = incubator['item_id']
                inventory[item_id] = inventory.get(item_id, 0) + 1
    return inventory


def parse_player_stats(resp_get_inventory):
    inventory_items = resp_get_inventory.get('inventory_delta', {}).get(
        'inventory_items', [])
    for item in inventory_items:
        item_data = item.get('inventory_item_data', {})
        if 'player_stats' in item_data:
            return item_data['player_stats']
    return {}


def parse_caught_pokemon(catch_result):
    if ('CATCH_POKEMON' in catch_result):
        catch_pokemon = catch_result['CATCH_POKEMON']
        catch_status = catch_pokemon['status']
        if catch_status == 1:
            # Check inventory for caught Pokemon
            capture_id = catch_pokemon['captured_pokemon_id']
            iitems = catch_result['GET_INVENTORY']['inventory_delta'][
                'inventory_items']
            for item in iitems:
                iidata = item['inventory_item_data']
                if 'pokemon_data' in iidata and iidata['pokemon_data']['id'] == capture_id:
                    return iidata['pokemon_data']
    return None