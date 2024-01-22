class FixedPoint96:
    RESOLUTION = 96
    Q96 = 0x1000000000000000000000000


def _get_amount0_delta1(sqrt_ratio_ax96, sqrt_ratio_bx96, liquidity, round_up):
    if sqrt_ratio_ax96 > sqrt_ratio_bx96:
        sqrt_ratio_ax96, sqrt_ratio_bx96 = sqrt_ratio_bx96, sqrt_ratio_ax96
    numerator1 = liquidity << FixedPoint96.RESOLUTION
    numerator2 = sqrt_ratio_bx96 - sqrt_ratio_ax96
    if sqrt_ratio_ax96 < 0:
        return None
    else:
        if round_up:
            x = _mul_div_rounding_up(numerator1, numerator2, sqrt_ratio_bx96)
            return _div_rounding_up(x, sqrt_ratio_ax96)
        else:
            return (numerator1 * numerator2 / sqrt_ratio_bx96) / sqrt_ratio_ax96


def _get_amount1_delta1(sqrt_ratio_ax96, sqrt_ratio_bx96, liquidity, round_up):
    if sqrt_ratio_ax96 > sqrt_ratio_bx96:
        sqrt_ratio_ax96, sqrt_ratio_bx96 = sqrt_ratio_bx96, sqrt_ratio_ax96
    if round_up:
        x = _mul_div_rounding_up(liquidity, sqrt_ratio_bx96 - sqrt_ratio_ax96, FixedPoint96.Q96)
        return x
    else:
        return liquidity * (sqrt_ratio_bx96 - sqrt_ratio_ax96) / FixedPoint96.Q96


def _get_amount0_delta(sqrt_ratio_ax96, sqrt_ratio_bx96, liquidity):
    if liquidity < 0:
        return -_get_amount0_delta1(sqrt_ratio_ax96, sqrt_ratio_bx96, -liquidity, False)
    else:
        return _get_amount0_delta1(sqrt_ratio_ax96, sqrt_ratio_bx96, liquidity, True)


def _get_amount1_delta(sqrt_ratio_ax96, sqrt_ratio_bx96, liquidity):
    if liquidity < 0:
        return -_get_amount1_delta1(sqrt_ratio_ax96, sqrt_ratio_bx96, -liquidity, False)
    else:
        return _get_amount1_delta1(sqrt_ratio_ax96, sqrt_ratio_bx96, liquidity, True)


def get_token_amount_of_user(liquidity, sqrt_price_x96, tick, tick_lower, tick_upper):
    amount0, amount1 = 0, 0
    if liquidity != 0:
        if tick < tick_lower:
            amount0 = _get_amount0_delta(_get_sqrt_ratio_at_tick(tick_lower),
                                         _get_sqrt_ratio_at_tick(tick_upper), liquidity)
        elif tick < tick_upper:
            amount0 = _get_amount0_delta(sqrt_price_x96, _get_sqrt_ratio_at_tick(tick_upper), liquidity)
            amount1 = _get_amount1_delta(_get_sqrt_ratio_at_tick(tick_lower), sqrt_price_x96, liquidity)
        else:
            amount1 = _get_amount1_delta(_get_sqrt_ratio_at_tick(tick_lower),
                                         _get_sqrt_ratio_at_tick(tick_upper),
                                         liquidity)
    return amount0, amount1


def get_token_amount_of_pool(liquidity, tick_lower, tick_upper):
    amount0, amount1 = 0, 0
    if liquidity != 0:
        amount0 = _get_amount0_delta(_get_sqrt_ratio_at_tick(tick_lower),
                                     _get_sqrt_ratio_at_tick(tick_upper),
                                     liquidity)
        amount1 = _get_amount1_delta(_get_sqrt_ratio_at_tick(tick_lower),
                                     _get_sqrt_ratio_at_tick(tick_upper),
                                     liquidity)
    return amount0, amount1


def _div_rounding_up(x, y):
    return x // y + (x % y > 0)


def _mul_div_rounding_up(a, b, denominator):
    result = a * b / denominator
    if (a * b) % denominator > 0:
        if result < 2 ** 256 - 1:
            result += 1
        else:
            raise OverflowError("Result exceeds maximum uint256 value.")
    return result


def _get_sqrt_ratio_at_tick(tick):
    MAX_TICK = 887272
    abs_tick = abs(tick)
    if abs_tick > MAX_TICK:
        raise ValueError('T')

    ratio = 0xfffcb933bd6fad37aa2d162d1a594001 if abs_tick & 0x1 else 0x100000000000000000000000000000000
    ratio = (ratio * 0xfff97272373d413259a46990580e213a) >> 128 if abs_tick & 0x2 else ratio
    ratio = (ratio * 0xfff2e50f5f656932ef12357cf3c7fdcc) >> 128 if abs_tick & 0x4 else ratio
    ratio = (ratio * 0xffe5caca7e10e4e61c3624eaa0941cd0) >> 128 if abs_tick & 0x8 else ratio
    ratio = (ratio * 0xffcb9843d60f6159c9db58835c926644) >> 128 if abs_tick & 0x10 else ratio
    ratio = (ratio * 0xff973b41fa98c081472e6896dfb254c0) >> 128 if abs_tick & 0x20 else ratio
    ratio = (ratio * 0xff2ea16466c96a3843ec78b326b52861) >> 128 if abs_tick & 0x40 else ratio
    ratio = (ratio * 0xfe5dee046a99a2a811c461f1969c3053) >> 128 if abs_tick & 0x80 else ratio
    ratio = (ratio * 0xfcbe86c7900a88aedcffc83b479aa3a4) >> 128 if abs_tick & 0x100 else ratio
    ratio = (ratio * 0xf987a7253ac413176f2b074cf7815e54) >> 128 if abs_tick & 0x200 else ratio
    ratio = (ratio * 0xf3392b0822b70005940c7a398e4b70f3) >> 128 if abs_tick & 0x400 else ratio
    ratio = (ratio * 0xe7159475a2c29b7443b29c7fa6e889d9) >> 128 if abs_tick & 0x800 else ratio
    ratio = (ratio * 0xd097f3bdfd2022b8845ad8f792aa5825) >> 128 if abs_tick & 0x1000 else ratio
    ratio = (ratio * 0xa9f746462d870fdf8a65dc1f90e061e5) >> 128 if abs_tick & 0x2000 else ratio
    ratio = (ratio * 0x70d869a156d2a1b890bb3df62baf32f7) >> 128 if abs_tick & 0x4000 else ratio
    ratio = (ratio * 0x31be135f97d08fd981231505542fcfa6) >> 128 if abs_tick & 0x8000 else ratio
    ratio = (ratio * 0x9aa508b5b7a84e1c677de54f3e99bc9) >> 128 if abs_tick & 0x10000 else ratio
    ratio = (ratio * 0x5d6af8dedb81196699c329225ee604) >> 128 if abs_tick & 0x20000 else ratio
    ratio = (ratio * 0x2216e584f5fa1ea926041bedfe98) >> 128 if abs_tick & 0x40000 else ratio
    ratio = (ratio * 0x48a170391f7dc42444e8fa2) >> 128 if abs_tick & 0x80000 else ratio

    if tick > 0:
        ratio = (2 ** 256 - 1) // ratio

    sqrt_price_x96 = (ratio >> 32) + (0 if ratio % (1 << 32) == 0 else 1)
    return sqrt_price_x96
