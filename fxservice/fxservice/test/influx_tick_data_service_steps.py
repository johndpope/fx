#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pytest_bdd import given, then, scenario, parsers

from fxservice.fxservice.tick_data_service.influx_tick_data_service import *


@scenario('influx_tick_data_service.feature', 'Tạo service với db mới thì dữ liệu là mặc định')
def test_publish34():
    pass


@scenario('influx_tick_data_service.feature', 'Tạo service với db mới và thêm dữ liệu thì thêm đúng')
def test_publish1():
    pass


@given("Tạo service test với db mới")
def tao_service():
    return InfluxTickDataService('localhost', 8086, 'root', 'root', 'test_bdd')


@then(parsers.parse("Kiểm tra count bằng {count:d}"))
def kiem_tra(tao_service, count):
    assert tao_service.get_count() == int(count)


@then("Kiểm tra lasted bar khác None")
def kiem_tra_none(tao_service):
    assert tao_service.get_lasted_bar() is not None


@then("Kiểm tra lasted bar bằng None")
def kiem_tra_none(tao_service):
    assert tao_service.get_lasted_bar() is None


@given("Thêm 1 tick")
def kiem_tra_none(tao_service):
    tao_service.push_data({'candles': [{'volume': 3, 'time': '2000-01-01T00:00:00Z', 'bid': {
        'o': 1, 'h': 3, 'l': 0, 'c': 2
    }}]})
