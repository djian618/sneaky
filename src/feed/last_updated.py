#!/usr/bin/env python3

import csv
import os
import datetime
import time

class LastUpdatedSerializer():
    def __init__(self, last_updated_file, min_update_time=None):
        self.dst_file_path = last_updated_file
        self.last_updated = {}
        self.columns = ["du", "stockx", "flightclub"]
        self.min_update_time = float(min_update_time) if min_update_time is not None else 0
        if os.path.isfile(last_updated_file):
            self.load_last_updated()
    
    def load_last_updated(self):
        with open(self.dst_file_path) as infile:
            rr = csv.reader(infile)
            for row in rr:
                style_id = row[0]
                self.last_updated[style_id] = {}

                for i in range(len(self.columns)):
                    if i + 1 < len(row):
                        self.last_updated[style_id][self.columns[i]] = datetime.datetime.strptime(
                            row[i + 1], "%Y%m%d-%H%M%S")
    
    def update_last_updated(self, style_id, venue):
        if style_id not in self.last_updated:
            self.last_updated[style_id] = {}
        self.last_updated[style_id][venue] = datetime.datetime.now()
        return self.last_updated[style_id][venue]

    def should_update(self, style_id, venue):
        if not self.min_update_time:
            return True
        else:
            if style_id in self.last_updated and venue in self.last_updated[style_id]:
                now = datetime.datetime.now()
                last_update = time.time()
                last_update = self.last_updated[style_id][venue]
                return (now - last_update).total_seconds() > self.min_update_time
            else:
                return True

    def save_last_updated(self):
        with open(self.dst_file_path, "w") as outfile:
            wr = csv.writer(outfile)
            for style_id in self.last_updated:
                out_list = [style_id]
                for venue in self.last_updated[style_id]:
                    out_list.append(self.last_updated[style_id][venue].strftime("%Y%m%d-%H%M%S"))
                wr.writerow(out_list)


