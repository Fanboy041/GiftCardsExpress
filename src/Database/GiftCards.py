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


def get_service_info(service_name):
    service_info_list = []
    for services_info in giftCards.find():
        for key, value in services_info.items():
            if key == service_name:
                service_info_list = value

    return service_info_list


def get_gift_cards(service_name):
    gift_cards_code_list = []
    gift_cards_list = get_service_info(service_name)
    for giftCardsCode in gift_cards_list:
        for key, value in giftCardsCode.items():
            if key == "gift_card_code":
                gift_cards_code_list.append(value)

    return gift_cards_code_list


def save_service_name(service_name):
    giftCard_info_set = {
        service_name: []
    }

    if service_name not in get_services_name():
        giftCards.insert_one(giftCard_info_set)
        return f"{service_name} service has been saved"
    else:
        return f"{service_name} service is already exist"


# Create a function to save the giftCard information to the database
def save_gift_card_name(service_name, gift_card_code, price):
    # giftCard_info_set = {
    #     service_name: [
    #         {
    #             "gift_card_code": gift_card_code,
    #             "price": price
    #         }
    #     ]
    # }

    if service_name not in get_services_name():
        return f"{service_name} was not found, please create a service name"
        # giftCards.insert_one(giftCard_info_set)

    else:

        giftCard_info_update = {"$push": {
            service_name:
                {
                    "gift_card_code": gift_card_code,
                    "price": price
                }
            }
        }
        print(get_gift_cards(service_name))
        print(gift_card_code)

        if gift_card_code not in get_gift_cards(service_name):
            #
            # query_filter = str
            # for x in giftCards.find({}, {"_id": 0}):
            #     for key, value in x.items():
            #         if key == service_name:
            #             query_filter = value

            # gift_card_list = []
            # for x in query_filter:
            #     gift_card_list.append(x.get("gift_card_code"))
            #
            giftCards.update_one({service_name: get_service_info(service_name)}, giftCard_info_update)
            return f"{service_name} gift card has been added"

        else:
            return f"{service_name}  gift card is already exist"
