import json
import os
import sys

from dotted.collection import DottedDict
import locale

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from chapter1.create_statement_data import create_statement_data


def render_plain_text(data):
    result = f"청구 내역 (고객명: {data.customer})\n"

    for perf in data.performances:
        # 청구 내역을 출력한다.
        result += f' {perf.play.name}: {locale.currency(perf.amount / 100, grouping=True)} ({perf.audience}석)\n'

    result += f"총액: {locale.currency(data.total_amount / 100, grouping=True)}\n"
    result += f"적립 포인트': {data.total_volume_credits}점\n"

    return result


def statement():
    return render_plain_text(create_statement_data(invoice, plays))


if __name__ == '__main__':
    locale.setlocale(locale.LC_ALL, 'en_US')

    with open('invoices.json') as json_file:
        invoice = DottedDict(json.load(json_file)[0])

    with open('plays.json') as json_file:
        plays = DottedDict(json.load(json_file))

    print(statement())
