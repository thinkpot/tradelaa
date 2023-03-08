from .models import Trades


def basic_dashboard(data):
    #Getting no. of target hits
    total_trades = Trades.objects.filter(is_target__isnull=False, is_sl__isnull=False)
    target_count = total_trades.filter(is_target=True).count()
    sl_count = total_trades.filter(is_sl=True).count()


    #Appending data to dict
    data['target_count'] = target_count
    data['sl_count'] = sl_count


    return data