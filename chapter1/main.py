import json
import math
from dotted.collection import DottedDict
import locale


def render_plain_text(data):
    result = f"청구 내역 (고객명: {data.customer})\n"

    for perf in data.performances:
        # 청구 내역을 출력한다.
        result += f' {perf.play.name}: {locale.currency(perf.amount / 100, grouping=True)} ({perf.audience}석)\n'

    result += f"총액: {locale.currency(data.total_amount / 100, grouping=True)}\n"
    result += f"적립 포인트': {data.total_volume_credits}점\n"

    return result


def statement():
    statement_data = DottedDict()

    def play_for(an_performance):
        return plays[an_performance.playID]

    def amount_for(an_performance):
        if an_performance.play.type == "tragedy":  # 비극
            result = 40000
            if an_performance.audience > 30:
                result += 1000 * (an_performance.audience - 30)
        elif an_performance.play.type == "comedy":  # 비극
            result = 30000
            if an_performance.audience > 20:
                result += 10000 + 500 * (an_performance.audience - 20)
            result += 300 * an_performance.audience
        else:
            raise Exception("알 수 없는 장르")
        return result

    def volume_credits_for(perf):
        result = 0
        result += max(perf.audience - 30, 0)
        if perf.play.type == "comedy":
            result += math.floor(perf.audience / 5)
        return result

    def total_volume_credits(data):
        result = 0
        for perf in data.performances:
            result += perf.volume_credits
        return result

    def total_amount(data):
        result = 0
        for perf in data.performances:
            result += amount_for(perf)
        return result

    def enrich_performance(an_performance):
        result = an_performance
        result.play = play_for(result)
        result.amount = amount_for(result)
        result.volume_credits = volume_credits_for(result)

        return result

    statement_data.customer = invoice.customer
    statement_data.performances = list(map(enrich_performance, invoice.performances))
    statement_data.total_amount = total_amount(statement_data)
    statement_data.total_volume_credits = total_volume_credits(statement_data)

    return render_plain_text(statement_data)


if __name__ == '__main__':
    locale.setlocale(locale.LC_ALL, 'en_US')

    with open('invoices.json') as json_file:
        invoice = DottedDict(json.load(json_file)[0])

    with open('plays.json') as json_file:
        plays = DottedDict(json.load(json_file))

    print(statement())