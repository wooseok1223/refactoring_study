import math
from functools import reduce
from dotted.collection import DottedDict


class PerformanceCalculator:
    def __init__(self, an_performance, an_play):
        self.performance = an_performance
        self.play = an_play

    def get_amount(self):
        raise Exception("서브 클래스에서 처리하도록 설계되었습니다.")

    def get_volume_credits(self):
        return max(self.performance.audience - 30, 0)


class TragedyCalculator(PerformanceCalculator):
    def __init__(self, an_performance, an_play):
        super().__init__(an_performance, an_play)

    def get_amount(self):
        result = 40000
        if self.performance.audience > 30:
            result += 1000 * (self.performance.audience - 30)
        return result


class ComedyCalculator(PerformanceCalculator):
    def __init__(self, an_performance, an_play):
        super().__init__(an_performance, an_play)

    def get_amount(self):
        result = 30000
        if self.performance.audience > 20:
            result += 10000 + 500 * (self.performance.audience - 20)
        result += 300 * self.performance.audience
        return result

    def get_volume_credits(self):
        return super().get_volume_credits() + math.floor(self.performance.audience / 5)


def create_performance_calculator(an_performance, an_play):
    if an_play.type == "tragedy":
        return TragedyCalculator(an_performance, an_play)
    elif an_play.type == "comedy":
        return ComedyCalculator(an_performance, an_play)
    return PerformanceCalculator(an_performance, an_play)


def create_statement_data(invoice, plays):
    statement_data = DottedDict()

    def play_for(an_performance):
        return plays[an_performance.playID]

    def total_volume_credits(data):
        return reduce(lambda total, p: total + p.volume_credits, data.performances, 0)

    def total_amount(data):
        return reduce(lambda total, p: total + p.amount, data.performances, 0)

    def enrich_performance(an_performance):
        calculator = create_performance_calculator(an_performance, play_for(an_performance))
        result = an_performance
        result.play = play_for(result)
        result.amount = calculator.get_amount()
        result.volume_credits = calculator.get_volume_credits()

        return result

    statement_data.customer = invoice.customer
    statement_data.performances = list(map(enrich_performance, invoice.performances))
    statement_data.total_amount = total_amount(statement_data)
    statement_data.total_volume_credits = total_volume_credits(statement_data)

    return statement_data
