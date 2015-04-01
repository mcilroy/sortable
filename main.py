import json
import re


# add listing to result set
def add_listing(listing, product_name, product_results):
    if product_name not in product_results:
        product_results[product_name] = [listing]
    else:
        product_results[product_name].append(listing)


# allow matching of products with W3-100 or W3_100 by replacing special characters
# ensure that the product isn't a substring of another products name ex. W3-100 shouldn't match W3-1000
def build_regex(string):
    model_regex = re.sub('-|_| ', '[^a-zA-Z0-9]', string)
    model_regex2 = '(?:[^a-zA-Z0-9]|^)' + model_regex + '(?:[^a-zA-Z0-9]|$)'
    regex_model = re.compile(model_regex2)
    return regex_model


# output # of products not found and their details
def print_results(product_data, product_results):
    missing = 0.0
    print("products not found: ")
    for product in product_data:
        product_name = product['product_name']
        if product_name not in product_results:
            missing += 1
            print(product_name)
    print("missing % = " + str(100 * (missing / len(product_data))))


# print out json to file
def print_json(product_results):
    with open('data.txt', 'w') as outfile:
        json.dump(product_results, outfile)


# check if a product is found in all listings. Use a regular expression to match. If a match is found
# the product is added to the results along with the listing. Multiple listings can be attached to a product.
def main():
    products_file = open('products.txt', encoding="utf8")
    listings_file = open('listings.txt', encoding="utf8")
    product_data = json.load(products_file)
    listings_data = json.load(listings_file)
    product_results = {}
    for i, product in enumerate(product_data):
        if i % 100 == 0:
            print("Searched " + str(i) + " products...")
        no_family = False
        product_name = product['product_name']
        model = product['model'].lower()
        manufacturer = product['manufacturer'].lower()
        try:
            family = product['family'].lower()
        except KeyError:
            no_family = True

        regex_model = build_regex(model)
        regex_manufacturer = build_regex(manufacturer)

        if not no_family:
            regex_family = build_regex(family)

        for listing in listings_data:
            title = listing['title'].lower()
            if not no_family:
                if len(regex_model.findall(title)) > 0 and len(regex_family.findall(title)) > 0 and \
                        len(regex_manufacturer.findall(title)) > 0:
                    add_listing(listing, product_name, product_results)
            else:
                if len(regex_model.findall(title)) > 0 and len(regex_manufacturer.findall(title)) > 0:
                    add_listing(listing, product_name, product_results)
    products_file.close()
    listings_file.close()
    print_results(product_data, product_results)
    print_json(product_results)
main()