import requests
import json
import sqlite3
import sys

class GameData:
    def __init__(self):
        self._db               = GameData._create_db()
        self._populate_db()
        self._q_equip_w_skill  = GameData._read_sql_file("./sql/query/equip_with_skill.sql")[0]
        self._q_equip_w_set_b  = GameData._read_sql_file("./sql/query/equip_with_set_bonus.sql")[0]
        self._q_equip_w_type   = GameData._read_sql_file("./sql/query/equip_with_type.sql")[0]
        self._q_skill_to_set_b = GameData._read_sql_file("./sql/query/skill_to_set_bonus.sql")[0]
        self._q_all_skill      = GameData._read_sql_file("./sql/query/all_skill.sql")[0]
        self._q_all_set_b      = GameData._read_sql_file("./sql/query/all_set_bonus.sql")[0]


    def __del__(self):
        self._db.close()


    def equipment_with_skill(self, skill):
        return self._exec_sql_str(self._q_equip_w_skill, (skill, ))


    def equipment_with_set_bonus(self, bonus):
        return self._exec_sql_str(self._q_equip_w_set_b, (bonus, ))


    def equipment_with_type(self, e_type):
        return self._exec_sql_str(self._q_equip_w_type, (e_type, ))


    def skill_to_set_bonus(self):
        return self._exec_sql_str(self._q_skill_to_set_b)


    def skills(self):
        return self._exec_sql_str(self._q_all_skill)


    def set_bonuses(self):
        return self._exec_sql_str(self._q_all_set_b)


    def _populate_db(self):
        self._exec_sql_str("PRAGMA foreign_keys = ON")
        for s in GameData._read_sql_file("./sql/create.sql"):
            self._exec_sql_str(s)

        armor_url = "https://mhw-db.com/armor/sets"
        armor_par = { "q":"{\"rank\": \"master\"}" }
        charm_url = "https://mhw-db.com/charms"
        deco_url  = "https://mhw-db.com/decorations"
        skill_url = "https://mhw-db.com/skills"
        armor     = GameData._request_data(armor_url, params=armor_par)
        charm     = GameData._request_data(charm_url)
        deco      = GameData._request_data(deco_url)
        skill     = GameData._request_data(skill_url)

        for s in skill:
            insert = ()
            insert += (s["id"], )
            insert += (s["name"], )
            self._exec_sql_str('INSERT OR IGNORE INTO Skill \
                                VALUES (' + ','.join('?' * len(insert)) + ')', insert)
            for r in s["ranks"]:
                insert = ()
                insert += (r["id"], )
                insert += (r["level"], )
                insert += (s["id"], )
                self._exec_sql_str('INSERT OR IGNORE INTO SkillLevel \
                                    VALUES (' + ','.join('?' * len(insert)) + ')', insert)

        for a_set in armor:
            if not a_set["bonus"]:
                continue
            insert = ()
            insert += (a_set["bonus"]["id"], )
            insert += (a_set["bonus"]["name"], )
            self._exec_sql_str('INSERT OR IGNORE INTO SetBonus \
                                VALUES (' + ','.join('?' * len(insert)) + ')', insert)
            for r in a_set["bonus"]["ranks"]:
                insert = ()
                insert += (a_set["bonus"]["id"], )
                insert += (r["skill"]["id"], )
                insert += (r["pieces"], )
                self._exec_sql_str('INSERT OR IGNORE INTO BonusRank \
                                    VALUES (' + ','.join('?' * len(insert)) + ')', insert)

        for a_set in armor:
            for p in a_set["pieces"]:
                insert = ()
                insert += (p["id"], )
                insert += (p["name"], )
                insert += (p["type"], )
                insert += (p["skills"][0]["id"] if len(p["skills"]) >= 1 else None, )
                insert += (p["skills"][1]["id"] if len(p["skills"]) >= 2 else None, )
                insert += (a_set["bonus"]["id"] if a_set["bonus"] else None, )
                insert += (p["slots"][0]["rank"] if len(p["slots"]) >= 1 else None, )
                insert += (p["slots"][1]["rank"] if len(p["slots"]) >= 2 else None, )
                insert += (p["slots"][2]["rank"] if len(p["slots"]) >= 3 else None, )
                self._exec_sql_str('INSERT OR IGNORE INTO Equipment \
                                    VALUES (' + ','.join('?' * len(insert)) + ')', insert)

        for c in charm:
            r = c["ranks"][-1]
            insert = ()
            insert += (c["id"], )
            insert += (c["name"], )
            insert += ("charm", )
            insert += (r["skills"][0]["id"], )
            insert += (r["skills"][1]["id"] if len(r["skills"]) >= 2 else None, )
            for i in list(range(0,4)): insert += (None, )
            self._exec_sql_str('INSERT OR IGNORE INTO Equipment \
                                VALUES (' + ','.join('?' * len(insert)) + ')', insert)

        for d in deco:
            insert = ()
            insert += (d["id"], )
            insert += (d["name"].replace('\\',''), )
            insert += (d["slot"], )
            insert += (d["skills"][0]["id"], )
            insert += (d["skills"][1]["id"] if len(d["skills"]) >= 2 else None, )
            self._exec_sql_str('INSERT OR IGNORE INTO Decoration \
                                VALUES (' + ','.join('?' * len(insert)) + ')', insert)


    def _exec_sql_str(self, str, vars=None):
        cursor = self._db.cursor()
        ret = None
        try:
            if vars:
                ret = cursor.execute(str, vars).fetchall()
            else:
                ret = cursor.execute(str).fetchall()
        except sqlite3.Error as e:
            print(e)
            # sys.exit(e)
        cursor.close()
        self._db.commit()
        return ret


    @staticmethod
    def _read_sql_file(file):
        fd     = open(file, 'r')
        sql    = fd.read()
        fd.close()
        return sql.split(';')


    @staticmethod
    def _create_db():
        conn = None
        try:
            conn = sqlite3.connect('mhw.sqlite')
        except sqlite3.Error as e:
            sys.exit(e)
        return conn


    @staticmethod
    def _request_data(url, params=None):
        return requests.get(url, params=params).json()
