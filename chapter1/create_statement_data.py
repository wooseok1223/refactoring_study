import math
from functools import reduce
from dotted.collection import DottedDict


def create_statement_data(invoice, plays):
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
        return reduce(lambda total, p: total + p.volume_credits, data.performances, 0)

    def total_amount(data):
        return reduce(lambda total, p: total + p.amount, data.performances, 0)

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

    return statement_data
