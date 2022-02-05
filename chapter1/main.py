import json
import math
from dotted.collection import DottedDict
import locale


def play_for(an_performance):
    return plays[an_performance.playID]


def amount_for(an_performance):
    if play_for(an_performance).type == "tragedy":  # 비극
        result = 40000
        if an_performance.audience > 30:
            result += 1000 * (an_performance.audience - 30)
    elif play_for(an_performance).type == "comedy":  # 비극
        result = 30000
        if an_performance.audience > 20:
            result += 10000 + 500 * (an_performance.audience - 20)
        result += 300 * an_performance.audience
    else:
        raise Exception("알 수 없는 장르")
    return result


def volume_credits_for(perf):
    volume_credits = 0
    volume_credits += max(perf.audience - 30, 0)
    if play_for(perf).type == "comedy":
        volume_credits += math.floor(perf.audience / 5)
    return volume_credits


def statement(invoice):
    total_amount, volume_credits = 0, 0
    result = f"청구 내역 (고객명: {invoice.customer})\n"

    for perf in invoice.performances:
        volume_credits += volume_credits_for(perf)

        # 청구 내역을 출력한다.
        result += f' {play_for(perf).name}: {locale.currency(amount_for(perf) / 100, grouping=True)} ({perf.audience}석)\n'
        total_amount += amount_for(perf)

    result += f"총액: {locale.currency(total_amount / 100, grouping=True)}\n"
    result += f"적립 포인트': {volume_credits}점\n"

    return result


if __name__ == '__main__':
    locale.setlocale(locale.LC_ALL, 'en_US')

    with open('invoices.json') as json_file:
        invoice = DottedDict(json.load(json_file)[0])

    with open('plays.json') as json_file:
        plays = DottedDict(json.load(json_file))

    print(statement(invoice))