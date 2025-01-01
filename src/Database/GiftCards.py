from Database.MongoDB import client

# Create a schema for giftCards
giftCard_schema = {
    str: [
        {
            "gift_card_code": str,
            "price": int
        }
    ]
}

# Define the collections for giftCards
giftCards = client.permissions.giftCards


# Create a function to get the giftCard information from the database
def get_services_name():
    services_name_list = []
    for key, value in giftCards.find():
        services_name_list.append(value)

    return services_name_list


def save_service_name(service_name):
    giftCard_info_set = {
        service_name: [
            {
            }
        ]
    }

    if service_name not in get_services_name():
        giftCards.insert_one(giftCard_info_set)
        return "The service name has been saved"
    else:
        return "The Service name is already taken"


# Create a function to save the giftCard information to the database
def save_gift_card_name(service_name, gift_card_code, price):
    giftCard_info_set = {
        service_name: [
            {
                "gift_card_code": gift_card_code,
                "price": price
            }
        ]
    }

    if service_name not in get_services_name():
        giftCards.insert_one(giftCard_info_set)

    else:
        giftCard_info_update = {"$push": {
            service_name:
                {
                    "gift_card_code": gift_card_code,
                    "price": price
                }
        }
        }

        query_filter = str
        for x in giftCards.find({}, {"_id": 0}):
            for key, value in x.items():
                if key == service_name:
                    query_filter = value

        gift_card_list = []
        for x in query_filter:
            gift_card_list.append(x.get("gift_card_code"))

        if gift_card_code in gift_card_list:
            return "This gift Card is already exist"
        else:
            giftCards.update_one({service_name: query_filter}, giftCard_info_update)
            return "This gift Card has been added"
