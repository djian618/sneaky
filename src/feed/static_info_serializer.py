import datetime
import csv

from du_response_parser import DuItem
from stockxsdk import StockxProduct

class StaticInfoSerializer():
    def __init__(self):
        return

    def extract_item_static_info(self, items):
        result = [items[i].get_static_info() for i in items]
        return result

    def dump_static_info_to_csv(self, items):
        static_items = self.extract_item_static_info(items)
        date_time = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        static_mapping_file = "du.mapping.{}.csv".format(date_time)
        with open(static_mapping_file, "w") as outfile:
            wr = csv.writer(outfile)
            wr.writerow(["style_id", "du_product_id", "du_title", "release_date", "gender"])
            for row in static_items:
                wr.writerow([row["style_id"], row["product_id"], row["title"], row["release_date"], row["gender"]])
        print("dumped static mapping to {}".format(static_mapping_file))

    def dump_stockx_static_info_to_csv(self, items):
        date_time = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        static_mapping_file = "stockx.mapping.{}.csv".format(date_time)
        with open(static_mapping_file, "w") as outfile:
            wr = csv.writer(outfile)
            wr.writerow(["style_id", "stockx_product_id", "stockx_title", "retail_price", "brand"])
            for row in items:
                wr.writerow([row.style_id, row.product_id, row.title, row.retail_price, row.brand])
        print("dumped static mapping to {}".format(static_mapping_file))

    def load_static_info_from_csv(self, filename):
        result = {}
        with open(filename, "r") as infile:
            rr = csv.reader(infile)
            count = 0
            for row in rr:
                count += 1
                if count == 1:
                    continue
                else:
                    style_id = row[0]
                    product_id = row[1]
                    title = row[2]
                    release_date = row[3]
                    gender = row[4]

                    item = DuItem(product_id, title, 0)
                    item.release_date = release_date
                    item.style_id = style_id
                    item.gender = row[4]
                    result[product_id] = item
        return result

    def load_stockx_static_info_from_csv(self, filename):
        result = {}
        with open(filename, "r") as infile:
            rr = csv.reader(infile)
            count = 0
            for row in rr:
                count += 1
                if count == 1:
                    continue
                else:
                    style_id = row[0]
                    product_id = row[1]
                    title = row[2]
                    price = row[3]
                    brand = row[4]

                    item = StockxProduct.from_csv_row(style_id, product_id, title, price, brand)
                    result[product_id] = item
        return result
