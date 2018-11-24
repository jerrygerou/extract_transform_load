import json
from collections import defaultdict
from itertools import chain


# Any value is more specific than wildcard
# A match on multiple criteria is more specific than a match on one
# For a 'tie', publisher (most specific), duration (second specific)


# Order of importance logic:
    # 1) Publisher, Price, Duration
    # 2) Publisher, *, Duration
    # 3) Publisher, Price, *
    # 4) *, *, Duration
    # 5) *, Price, Duration
    # 6) *, *, *

def get_orders():
    order_file = open('purchase_data.csv')
    orders = []
    for line in order_file:
        each_part = line.split(',')
        orders.append([i.replace('\n', '') for i in each_part])
    return orders

def get_buckets():
    bucket_file = open('purchase_buckets.csv')
    buckets = []
    for line in bucket_file:
        each_part = line.split(',')
        buckets.append([i.replace('\n', '') for i in each_part])
    return buckets


def bucket_all_items(orders, buckets):
    buckets_dict = defaultdict(list)
    added_to_a_bucket = []

    for bucket in buckets:
        buckets_dict[bucket[0], bucket[1], bucket[2]] = []

    for order in orders:
        # publisher = [2], price = [4], duration = [5]
        publisher = order[2]
        price = order[4]
        duration = order[5]
        key_to_find = publisher, price, duration
        # 1) Publisher, Price, Duration
        for k, v in buckets_dict.items():
            if key_to_find[0].lower() == k[0].lower() and key_to_find[1] == k[1] and key_to_find[2] == k[2]:
                if order not in added_to_a_bucket:
                    ','.join(order)
                    buckets_dict[k[0], k[1], k[2]].append(','.join(order))
                    added_to_a_bucket.append(order)
        else:
            # 2) Publisher, *, Duration
            key_to_find = publisher, '*', duration
            for k, v in buckets_dict.items():
                if key_to_find[0].lower() == k[0].lower() and key_to_find[1] == k[1] and key_to_find[2] == k[2]:
                    if order not in added_to_a_bucket:
                        buckets_dict[k[0], k[1], k[2]].append(','.join(order))
                        added_to_a_bucket.append(order)
            else:
                # 3) Publisher, Price, *
                key_to_find = publisher, price, '*'
                for k, v in buckets_dict.items():
                    if key_to_find[0].lower() == k[0].lower() and key_to_find[1] == k[1] and key_to_find[2] == k[2]:
                        if order not in added_to_a_bucket:
                            buckets_dict[k[0], k[1], k[2]].append(','.join(order))
                            added_to_a_bucket.append(order)
                else:
                    # 4) *, *, Duration
                    key_to_find = '*', '*', duration
                    for k, v in buckets_dict.items():
                        if key_to_find[0] == k[0] and key_to_find[1] == k[1] and key_to_find[2] == k[2]:
                            if order not in added_to_a_bucket:
                                buckets_dict[k[0], k[1], k[2]].append(','.join(order))
                                added_to_a_bucket.append(order)
                    else:
                        # 5) *, Price, Duration
                        key_to_find = '*', price, duration
                        for k, v in buckets_dict.items():
                            if key_to_find[0] == k[0] and key_to_find[1] == k[1] and key_to_find[2] == k[2]:
                                if order not in added_to_a_bucket:
                                    buckets_dict[k[0], k[1], k[2]].append(','.join(order))
                                    added_to_a_bucket.append(order)
                            else:
                                # 6) *, *, *
                                key_to_find = '*', '*', '*'
                                for k, v in buckets_dict.items():
                                    if key_to_find[0] == k[0] and key_to_find[1] == k[1] and key_to_find[2] == k[2]:
                                        if order not in added_to_a_bucket:
                                            buckets_dict[k[0], k[1], k[2]].append(','.join(order))
                                            added_to_a_bucket.append(order)

    # Create final list of bucketed purchases
    output_of_buckets = []
    for key, value in buckets_dict.items():
        output_of_buckets.append({'bucket':key,'purchases':value})

    # Output a json file with correct separators
    with open('result.json', 'w') as result_file:
        json.dump(output_of_buckets, result_file)

orders = get_orders()
buckets = get_buckets()
bucket_all_items(orders, buckets)
