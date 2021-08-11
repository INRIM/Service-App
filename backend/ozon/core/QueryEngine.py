# Copyright INRIM (https://www.inrim.eu)
# See LICENSE file for full licensing details.
import sys
import os
import logging
import ujson
from .BaseClass import PluginBase
from fastapi.exceptions import HTTPException
from datetime import datetime, date, time
from .DateEngine import DateEngine
import re


class JsonDatetime(datetime):
    def __json__(self):
        return '"%s"' % self.isoformat()


datetime = JsonDatetime

logger = logging.getLogger(__name__)


class QueryEngine(PluginBase):
    plugins = []

    def __init_subclass__(cls, **kwargs):
        cls.plugins.append(cls())


class QueryEngineBase(QueryEngine):
    @classmethod
    def create(cls, session):
        self = QueryEngineBase()
        self.init(session)
        return self

    def init(self, session):
        self.session = session
        self.date_datetime_mask = '%Y-%m-%dT%H:%M:%S'
        self.dte = DateEngine(SERVER_DTTIME_MASK='%Y-%m-%dT%H:%M:%S')
        # for dt --> 2021-08-11T17:22:04
        self.isodate_regex = re.compile('(\d{4}-\d{2}-\d{2})[A-Z]+(\d{2}:\d{2}:\d{2})')
        self.autodate_parser = {
            "year": lambda y=0: self.dte.year_range(year=y),
            "month": lambda y=0, m=0, me=0: self.dte.month_range(year=y, month=m, monthe=me),
            "today": lambda d=0: self.dte.today(days=d),
            "now": lambda: self.dte.now
        }
        # for dt --> 2021-08-11T17:22:04.51+01:00
        # self.isodate_regex = re.compile('(\d{4}-\d{2}-\d{2})[A-Z]+(\d{2}:\d{2}:\d{2}).([0-9+-:]+)')

    def get_today_first_last(self):
        return {}

    def get_now(self):
        return {}

    def _check_update_date(self, obj_val):
        if not isinstance(obj_val, str):
            return obj_val
        if self.isodate_regex.match(obj_val):
            # val = datetime.strptime(obj_val, self.date_datetime_mask)
            val = self.dte.strdatetime_server_to_datetime(obj_val)
            logger.info(f" render {obj_val} -> {val}")
            return val
        else:
            return obj_val

    def _check_update_user(self, obj_val):
        if not isinstance(obj_val, str):
            return obj_val
        if "_user_" in obj_val:
            # logger.info(f" render {obj_val}")
            x = obj_val.replace("_user_", "")
            return getattr(self.session, x)  # self.session.get(x, "")
        else:
            return obj_val

    def get_query_date(self, strcode):
        pass

    def _check_update_auto_date(self, obj_val):
        """
        :param obj_val: possible config
            date_year  --> return range current year
            date_year-2020  --> return range for year 2020
            date_month  --> return range current year and current month
            date_month-1-0  --> return range current year for January
            date_month-1-3  --> return range current year frm 1st January  and 31st March
            date_month-1-3-2020  --> return range frm 1st January  and 31st March 2020
            date_today --> return date today at 00:00:00 (TZ)
            date_today_1 --> return date tommorrow at 00:00:00 (TZ)
            date_today_n_1 --> return  n means negative date yesterday at 00:00:00 (TZ)
            date_now --> return date today at this tick time (TZ)
        :return: date range or date objects
        """
        if not isinstance(obj_val, str):
            return obj_val
        if "_date_" in obj_val:
            # logger.info(f" render {obj_val}")
            x = obj_val.replace("_date_", "")
            return getattr(self.session, x)  # self.session.get(x, "")
        else:
            return obj_val

    def update(self, data):
        if isinstance(data, dict):
            for k, v in data.copy().items():
                if isinstance(v, dict):  # For DICT
                    data[k] = self.update(v)
                elif isinstance(v, list):  # For LIST
                    data[k] = [self.update(i) for i in v]
                else:  # Update Key-Value
                    data[k] = self.update(v)
                    # logger.info(f"updated data[k] {data}")
        else:
            data = self._check_update_date(data)
            data = self._check_update_user(data)
            return data
        return data.copy()

    def scan_find_key(self, data, key):
        res = []
        if isinstance(data, dict):
            for k, v in data.items():
                res.append(k == key)
                if isinstance(v, dict):  # For DICT
                    res.append(self.scan_find_key(v, key))
                elif isinstance(v, list):  # For LIST
                    for i in v:
                        res.append(self.scan_find_key(i, key))
        return res[:]

    def flatten(self, l):
        for item in l:
            try:
                yield from self.flatten(item)
            except TypeError:
                yield item

    def check_key(self, data, key):
        # logger.info("check key")
        res_l = self.scan_find_key(data, key)
        res_flat = list(self.flatten(res_l))
        try:
            i = res_flat.index(True)
            return True
        except ValueError:
            return False

    def default_query(self, model, query: dict, parent="", model_type="") -> dict:
        # model_schema = model.schema()
        # fields = {k: model_schema['properties'][k]['type'] for k, v in model_schema['properties'].items()}
        if not self.check_key(query, "deleted"):
            query.update({"deleted": 0})

        if not self.check_key(query, "active"):
            query.update({"active": True})

        if not self.check_key(query, "parent") and parent:
            query.update({"parent": {"$eq": parent}})

        if not self.check_key(query, "type") and model_type:
            query.update({"type": {"$eq": model_type}})

        q = self.update(query)
        logger.info(f"result query: {q}")
        return q
