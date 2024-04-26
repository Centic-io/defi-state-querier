def get_fees(fee_growth_global_0, fee_growth_global_1, fee_growth_0_low, fee_growth_0_hi, fee_growth_inside_0,
             fee_growth_1_low, fee_growth_1_hi, fee_growth_inside_1, liquidity, decimals0, decimals1, tick_lower,
             tick_upper, tick_current):
    if tick_current >= tick_upper:
        tick_upper_fee_growth_above_0 = sub_in_256(fee_growth_global_0, fee_growth_0_hi)
        tick_upper_fee_growth_above_1 = sub_in_256(fee_growth_global_1, fee_growth_1_hi)
    else:
        tick_upper_fee_growth_above_0 = fee_growth_0_hi
        tick_upper_fee_growth_above_1 = fee_growth_1_hi
    if tick_current >= tick_lower:
        tick_lower_fee_growth_below_0 = fee_growth_0_low
        tick_lower_fee_growth_below_1 = fee_growth_1_low
    else:
        tick_lower_fee_growth_below_0 = sub_in_256(fee_growth_global_0, fee_growth_0_low)
        tick_lower_fee_growth_below_1 = sub_in_256(fee_growth_global_1, fee_growth_1_low)

    fr_t1_0 = sub_in_256(sub_in_256(fee_growth_global_0, tick_lower_fee_growth_below_0),
                         tick_upper_fee_growth_above_0)
    fr_t1_1 = sub_in_256(sub_in_256(fee_growth_global_1, tick_lower_fee_growth_below_1),
                         tick_upper_fee_growth_above_1)
    uncollect_fee_0 = liquidity * sub_in_256(fr_t1_0, fee_growth_inside_0) / 2 ** 128
    uncollect_fee_1 = liquidity * sub_in_256(fr_t1_1, fee_growth_inside_1) / 2 ** 128
    return uncollect_fee_0 / 10 ** decimals0, uncollect_fee_1 / 10 ** decimals1


def sub_in_256(a: int, b: int) -> int:
    """
    Performs subtraction on two 256-bit unsigned integers, handling overflow.
    """

    MAX_UINT256 = (1 << 256) - 1
    result = (a - b) % (MAX_UINT256 + 1)  # Handle overflow using modulo
    return result
