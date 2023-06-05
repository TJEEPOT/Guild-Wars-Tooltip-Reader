# disambiguation.json #
A dict of all disambiguation pages found so far on the wiki. 
The key for each entry are the item names from in-game formatted for use on the wiki ("Great Axe" is formatted to "Great_Axe" and "3 Piles of Glittering Dust" is formatted to "Pile_of_Glittering_Dust", for example). 
The value for each entry is a list of pages on the wiki which that disambiguation page linked to.

## Structure Example ##
{
    "Water_Staff":
        ["Water_Staff_(Canthan)", "Water_Staff_(core)", "Water_Staff_(Tyrian)"],
    "Elonian_Daggers":
        ["Elonian_Daggers_(common)", "Elonian_Daggers_(uncommon)", "Elonian_Daggers_(rare)"]
}

# salvage.json # 
A dict of all items returned from the Guild Wars Wiki along with the information scraped from those pages. 
The key for each entry is the item name formatted for use on the wiki (see above for examples).
The value for each entry is a dict of the information found on the given page. There are no guaranteed keys within this dict, so all should be checked before reading (and writing). Current valid keys are:
- "common_mats": a list of dicts representing the common materials the parent item salvages into. Each dict can contain the keys: 
    - "item_name": the name of the item the parent item salvages into 
    - "avg_count": an integer representing the average number of the above material that the parent item salvages into. If 0, this data hasn't been added yet.
- "rare_mats": as above, a list of dicts for each rare material the parent item salvages into. Keys within each dict are:
    - "item_name": the name of the item the parent item salvages into 
    - "avg_count": an integer representing the average number of the above material that the parent item salvages into. If 0, this data hasn't been added yet.
- "nicholas_date": an ISO 8601 date of the Monday when this item is next accepted by Nicholas the Traveler (as of the date the information was scraped). 959 days

## Structure Example ##
{
    "Water_Staff_(Core)":{
        "common_mats":[
            {"item_name":"Iron Ingot", "avg_count":6}, 
            {"item_name":"Pile of Glittering Dust", "avg_count":4}, 
            {"item_name":"Wood Plank", "avg_count":6}
        ],
        "rare_mats":[
            {"item_name":"Steel Ingots", "avg_count":1}
        ]
    }
    "Sandblasted_Lodestone":{
        "common_mats":[
            {"item_name":"Granite Slabs", "avg_count":7}
        ]
        "nicholas_date":"2023-06-05"
    }
}

# materials.json #
A dict of all salvage materials that can be bought and sold to a vendor.
The key is the name of a single stack of a material, not edited for wiki use.
The value is a dict of information about that material. Current valid keys are:
- "type": either "common" or "rare", corresponding to the rarity of the material (blue or purple)
- "buy": integer representing the gold price a vendor will buy this material for (1 platinum = 1000g). This price is for 10x common materials, and 1x rare.
- "sell": integer representing the gold price a vendor will sell this material for. Same rules as with "buy".

## Structure Example ##
{
    "Iron Ingot":{"type":"common", "buy":150, "sell":50},
    "Steel Ingot":{"type":"rare", "buy":1200, "sell":700}
}