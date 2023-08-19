from django.shortcuts import render
from django.views.generic import TemplateView
from rest_framework.views import APIView
from django.http import JsonResponse
from rest_framework.status import HTTP_200_OK
from optionprice import Option
from .helpers import black_scholes_dexter


class OptionCalculator(TemplateView):
    template_name = 'tools/option_calculator.html'


class APIOptionCalculator(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data

        kind = 'call'
        price_initial = data.get('underlying_price_input', 0)
        price_strike = data.get('strike_price_input', 0)
        dividend_yield = data.get('dividend_yield_input', 0)
        volatility = data.get('volatility_input', 0)
        interest_rate_input = data.get('interest_rate_input', 0)
        time_span = data.get('day_exp_input', 0)
        start_date = data.get('start_date')
        end_date = data.get('end_date')

        S0 = int(price_initial)
        X = int(price_strike)
        q = int(dividend_yield)
        σ = int(volatility)
        t = int(time_span)
        r = int(interest_rate_input)
        call_theta, put_theta, call_premium, put_premium, call_delta, put_delta, gamma, vega, call_rho, put_rho = black_scholes_dexter(
            S0, X, t, σ=σ, r=r, q=q, td=365)

        payload = {
            'call_theta':call_theta,
            'put_theta':put_theta,
            'call_premium':call_premium,
            'put_premium':put_premium,
            'call_delta':call_delta,
            'put_delta':put_delta,
            'gamma':gamma,
            'vega':vega,
            'call_rho':call_rho,
            'put_rho':put_rho
        }

        return JsonResponse({
            "type": "success",
            "data": payload
        }, status=HTTP_200_OK)