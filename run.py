import json
from collections import defaultdict

# Known Rules
    # Any value is more specific than wildcard
    # A match on multiple criteria is more specific than a match on one
    # For a 'tie', publisher (most specific), duration (second specific), price (least)

# Purchase of importance logic:
    # 1) Publisher, Price, Duration
    # 2) Publisher, *, Duration
    # 3) Publisher, Price, *
    # 4) *, Price, Duration
    # 5) *, *, Duration
    # 6) *, Price, *
    # 7) *, *, *

def get_purchases():
    # Get list of purchases
    purchase_file = open('purchase_data.csv')
    purchases = []
    for line in purchase_file:
        each_part = line.split(',')
        purchases.append([i.replace('\n', '') for i in each_part])
    return purchases

def get_buckets():
    # Get list of buckets
    bucket_file = open('purchase_buckets.csv')
    buckets = []
    for line in bucket_file:
        each_part = line.split(',')
        buckets.append([i.replace('\n', '') for i in each_part])
    return buckets


def bucket_all_items(purchases, buckets):
    # Create empty dictionary to hold resulted buckets
    buckets_dict = defaultdict(list)
    # Create empty list to hold orders to prevent duplicate entries in duplicated buckets
    added_to_a_bucket = []

    for bucket in buckets:
        buckets_dict[bucket[0], bucket[1], bucket[2]] = []

    for purchase in purchases:
        # publisher = [2], price = [4], duration = [5]
        publisher = purchase[2]
        price = purchase[4]
        duration = purchase[5]
        bucket_to_find = publisher, price, duration
        # 1) Publisher, Price, Duration
        for k, v in buckets_dict.items():
            if bucket_to_find[0].lower() == k[0].lower() and bucket_to_find[1] == k[1] and bucket_to_find[2] == k[2]:
                if purchase not in added_to_a_bucket:
                    ','.join(purchase)
                    buckets_dict[k[0], k[1], k[2]].append(','.join(purchase))
                    added_to_a_bucket.append(purchase)
        else:
            # 2) Publisher, *, Duration
            bucket_to_find = publisher, '*', duration
            for k, v in buckets_dict.items():
                if bucket_to_find[0].lower() == k[0].lower() and bucket_to_find[1] == k[1] and bucket_to_find[2] == k[2]:
                    if purchase not in added_to_a_bucket:
                        buckets_dict[k[0], k[1], k[2]].append(','.join(purchase))
                        added_to_a_bucket.append(purchase)
            else:
                # 3) Publisher, Price, *
                bucket_to_find = publisher, price, '*'
                for k, v in buckets_dict.items():
                    if bucket_to_find[0].lower() == k[0].lower() and bucket_to_find[1] == k[1] and bucket_to_find[2] == k[2]:
                        if purchase not in added_to_a_bucket:
                            buckets_dict[k[0], k[1], k[2]].append(','.join(purchase))
                            added_to_a_bucket.append(purchase)
                else:
                    # 4) *, Price, Duration
                    bucket_to_find = '*', price, duration
                    for k, v in buckets_dict.items():
                        if bucket_to_find[0] == k[0] and bucket_to_find[1] == k[1] and bucket_to_find[2] == k[2]:
                            if purchase not in added_to_a_bucket:
                                buckets_dict[k[0], k[1], k[2]].append(','.join(purchase))
                                added_to_a_bucket.append(purchase)
                    else:
                        # 5) *, *, Duration
                        bucket_to_find = '*', '*', duration
                        for k, v in buckets_dict.items():
                            if bucket_to_find[0] == k[0] and bucket_to_find[1] == k[1] and bucket_to_find[2] == k[2]:
                                if purchase not in added_to_a_bucket:
                                    buckets_dict[k[0], k[1], k[2]].append(','.join(purchase))
                                    added_to_a_bucket.append(purchase)
                        else:
                            # 6) *, Price, *
                            bucket_to_find = '*', price, '*'
                            for k, v in buckets_dict.items():
                                if bucket_to_find[0] == k[0] and bucket_to_find[1] == k[1] and bucket_to_find[2] == k[2]:
                                    if purchase not in added_to_a_bucket:
                                        buckets_dict[k[0], k[1], k[2]].append(','.join(purchase))
                                        added_to_a_bucket.append(purchase)
                            else:
                                # 7) *, *, *
                                bucket_to_find = '*', '*', '*'
                                for k, v in buckets_dict.items():
                                    if bucket_to_find[0] == k[0] and bucket_to_find[1] == k[1] and bucket_to_find[2] == k[2]:
                                        if purchase not in added_to_a_bucket:
                                            buckets_dict[k[0], k[1], k[2]].append(','.join(purchase))
                                            added_to_a_bucket.append(purchase)
    return buckets_dict

def generate_file(buckets_dict):
    # Create final list of bucketed purchases
    output_of_buckets = []
    for key, value in buckets_dict.items():
        output_of_buckets.append({'bucket':key,'purchases':value})

    # Output a json file
    with open('json_results.json', 'w') as result_file:
        json.dump(output_of_buckets, result_file)

purchases = get_purchases()
buckets = get_buckets()
bucketed_purchases = bucket_all_items(purchases, buckets)
generate_file(bucketed_purchases)
