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


def render_html(data):
    result = f"<h1>청구 내역 (고객명: ${data.customer})</h1>\n'"
    result += "<table>\n"
    result += "<tr><th>연극</th><th>좌석 수</th><th>금액</th></tr>"
    for perf in data.performances:
        result += f"<tr><td>${perf.play.name}</td><td>(${perf.audience}석)</td>"
        result += f"<td>${locale.currency(perf.amount, grouping=True)} </td></tr>\n"
    result += "</table>\n"
    result += f"<p>총액: <em>${locale.currency(data.total_amount, grouping=True)}</em></p>\n"
    result += f"<p>적립 포인트: <em>${data.total_volume_credits}점</em></p>\n"

    return result


def html_statement():
    return render_html(create_statement_data(invoice, plays))


def statement():
    return render_plain_text(create_statement_data(invoice, plays))


if __name__ == '__main__':
    locale.setlocale(locale.LC_ALL, 'en_US')

    with open('invoices.json') as json_file:
        invoice = DottedDict(json.load(json_file)[0])

    with open('plays.json') as json_file:
        plays = DottedDict(json.load(json_file))

    print(statement())
    print(html_statement())
