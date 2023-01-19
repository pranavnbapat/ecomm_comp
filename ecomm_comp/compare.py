import sys
import core_functions as cf


def scrape_data(brand_name=None):
    if not brand_name:
        print("Please provide a brand name")
        return

    print("Scraping from amazon.nl and bol.com started...\n")

    product_names_list = []
    product_prices_list = []
    product_link_list = []
    product_source_list = []
    product_timestamp_list = []

    amazon_product_names_list, amazon_product_prices_list, amazon_product_link_list, amazon_product_source_list, \
        amazon_timestamp_list = cf.scrape_amazon(brand_name)

    product_names_list.append(amazon_product_names_list)
    product_prices_list.append(amazon_product_prices_list)
    product_link_list.append(amazon_product_link_list)
    product_source_list.append(amazon_product_source_list)
    product_timestamp_list.append(amazon_timestamp_list)

    bol_product_names_list, bol_product_prices_list, bol_product_link_list, bol_product_source_list, \
        bol_timestamp_list = cf.scrape_bol(brand_name)

    product_names_list.append(bol_product_names_list)
    product_prices_list.append(bol_product_prices_list)
    product_link_list.append(bol_product_link_list)
    product_source_list.append(bol_product_source_list)
    product_timestamp_list.append(bol_timestamp_list)

    cf.save_data(product_names_list, product_prices_list, product_link_list, product_source_list,
                 product_timestamp_list, brand_name)


if __name__ == "__main__":
    brand = ["apple"]

    # Getting data
    for b in brand:
        scrape_data(brand_name=b)
