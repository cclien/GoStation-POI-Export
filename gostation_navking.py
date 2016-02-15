#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""

    Creating NaviKing's favorites.db from GoStations list API

"""
import urllib, json
import sqlite3
import time
import sys

TABLE_NAME = "favListV0"
CATEGORY_NAME = "GoStationPOI"
DELETE_ROW_STMT = '''DELETE FROM %s WHERE category_name = "%s"''' % (TABLE_NAME, CATEGORY_NAME)
TEST_DB_STMT = "SELECT * FROM %s" % TABLE_NAME
LANG = "zh-TW"
QUOTE_SIGN = "\""
COMMON_FIELDS = {"create_time":int(time.time()), "poi_image_id":-1, "poi_image_name":"",\
                 "poi_photo_path":"", "category_name":CATEGORY_NAME, "phone_number":"",
                 "location":"", "buffer_string":"", "buffer_index":-1, "basic_option":13,
                 "extra_option":0, "use_frequency":0, "CRoad":0}
URL = "https://wapi.gogoro.com/tw/api/vm/list"

def get_lang(list_jsonstring):
    """ The API return multilanguages fields with following format:
        "City":"{\"List\":[{\"Value\":\"Taipei City\",\"Lang\":\"en-US\"},
                           {\"Value\":\"台北市\",\"Lang\":\"zh-TW\"}]}"
        Just grab the specified language we want """
    gogoro_list = json.loads(list_jsonstring)
    for item in gogoro_list['List']:
        if item['Lang'] == LANG:
            return item['Value']

    raise Exception("language %s not found" % LANG)

def prepare_row(data):
    """ Prepare DB row from API data """
    output = {}
    output['poi_name'] = get_lang(data['LocName'])
    output['lat'] = data['Latitude']
    output['lon'] = data['Longitude']
    output['region'] = "%s,%s" % (get_lang(data['City']), get_lang(data['District']))

    return output

def insert_sql(cur, data):
    """ insert the dict into the SQLite DB """
    columns = ','.join(data.keys())
    placeholders = ', '.join('?' * len(data))
    sql = 'INSERT INTO {} ({}) VALUES ({})'.format(TABLE_NAME, columns, placeholders)
    cur.execute(sql, data.values())

def main(argv):
    """ just main function here """

    if len(argv) < 2:
        print >> sys.stderr, "usage: %s [sqlite db filename]" % argv[0]
        return

    filename = argv[1]

    response = urllib.urlopen(URL)
    jsonbody = json.loads(response.read().decode('utf-8'))

    conn = sqlite3.connect(filename)
    cur = conn.cursor()

    try:
        cur.execute(TEST_DB_STMT)
    except sqlite3.OperationalError:
        print >> sys.stderr, "%s seems not like a working NavKing POI DB" % filename
        return

    cur.execute(DELETE_ROW_STMT)

    for data in jsonbody['data']:
        row = prepare_row(data)
        row.update(COMMON_FIELDS)
        insert_sql(cur, row)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    main(sys.argv)
