import json
import re
"""
Methods for reading a txt file with 1 json object per line.
Matches 1 or more listings.txt lines to a single products.txt file
Outputs a data.txt file containing one product and its listings per line in a json object.
"""


def add_listing(listing, product_name, product_results):
    """ add listing to result set """
    if product_name not in product_results:
        product_results[product_name] = [listing]
    else:
        product_results[product_name].append(listing)


def build_regex(string):
    """ allow matching of products with different dividers by replacing special characters ex. W3-100 or W3_100
    ensure that the product isn't a substring of another products name ex. W3-100 shouldn't match W3-1000"""
    model_regex = re.sub('-|_| ', '[^a-zA-Z0-9]', string)
    model_regex2 = '(?:[^a-zA-Z0-9]|^)' + model_regex + '(?:[^a-zA-Z0-9]|$)'
    regex_model = re.compile(model_regex2)
    return regex_model


def print_results(product_objects, product_results):
    """ output # of products not found and their details"""
    missing = 0.0
    print("products not found: ")
    for product in product_objects:
        product_name = product['product_name']
        if product_name not in product_results:
            missing += 1
            print(product_name)
    print("missing % = " + str(100 * (missing / len(product_objects))))


def print_json_object_per_line(product_results):
    """ print out json to file in format specified (one json object per line)"""
    open('data.txt', 'w').write("%s" % "\n".join(json.dumps(dict([['product_name', product_name], ['listings', listings]]))
                                                 for product_name, listings in product_results.items()))


def open_txt_file(a_file):
    """ inputs a file with one json string per line. Outputs an array of json objects. """
    json_objects = []
    for line in a_file:
        json_object = json.loads(line)
        json_objects.append(json_object)
    a_file.close()
    return json_objects


def main():
    """ check if a product is found in all listings. Use a regular expression to match. If a match is found
    the product is added to the results along with the listing. Multiple listings can be attached to a product."""
    products_objects = open_txt_file(open('products.txt', encoding="utf8"))
    listings_objects = open_txt_file(open('listings.txt', encoding="utf8"))
    product_results = {}
    for i, product in enumerate(products_objects):
        if i % 100 == 0:
            print("Searched " + str(i) + " products...")

        product_name = product['product_name']
        model = product['model'].lower()
        manufacturer = product['manufacturer'].lower()

        # check if product has a family, if not we will ignore it
        has_family = True
        if 'family' not in product:
            has_family = False
        else:
            family = product['family'].lower()
            regex_family = build_regex(family)

        regex_model = build_regex(model)
        regex_manufacturer = build_regex(manufacturer)

        for listing in listings_objects:
            title = listing['title'].lower()
            if has_family:
                if len(regex_model.findall(title)) > 0 and len(regex_family.findall(title)) > 0 and \
                        len(regex_manufacturer.findall(title)) > 0:
                    add_listing(listing, product_name, product_results)
            else:
                if len(regex_model.findall(title)) > 0 and len(regex_manufacturer.findall(title)) > 0:
                    add_listing(listing, product_name, product_results)
    print_results(products_objects, product_results)
    print_json_object_per_line(product_results)
main()