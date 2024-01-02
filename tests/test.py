class FixedPoint96:

    RESOLUTION= 96
    Q96 = 0x1000000000000000000000000
def get_sqrt_ratio_at_tick(tick):
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
#
# def getAmount0Delta1(sqrtRatioAX96, sqrtRatioBX96, liquidity, roundUp):
#     if sqrtRatioAX96 > sqrtRatioBX96:
#         sqrtRatioAX96, sqrtRatioBX96 = sqrtRatioBX96, sqrtRatioAX96
#     numerator1 = liquidity << FixedPoint96.RESOLUTION
#     numerator2 = sqrtRatioBX96 - sqrtRatioAX96
#     if sqrtRatioAX96<0:
#         return None
#     else:
#         if roundUp:
#             x= mul_div_rounding_up(numerator1, numerator2, sqrtRatioBX96)
#             return div_rounding_up(x, sqrtRatioAX96)
#         else:
#             return mul_div(numerator1, numerator2, sqrtRatioBX96) / sqrtRatioAX96
#
# def getAmount1Delta1( sqrtRatioAX96, sqrtRatioBX96, liquidity, roundUp):
#     if sqrtRatioAX96 > sqrtRatioBX96:
#         sqrtRatioAX96, sqrtRatioBX96 = sqrtRatioBX96, sqrtRatioAX96
#     if roundUp:
#         x= mul_div_rounding_up(liquidity, sqrtRatioBX96 - sqrtRatioAX96, FixedPoint96.Q96)
#         return x
#     else:
#         return mul_div(liquidity, sqrtRatioBX96 - sqrtRatioAX96, FixedPoint96.Q96)
#
#
# def getAmount0Delta(sqrtRatioAX96,sqrtRatioBX96, liquidity):
#     if liquidity<0:
#         return getAmount0Delta1(sqrtRatioAX96, sqrtRatioBX96, -liquidity, False)
#     else:
#         return getAmount0Delta1(sqrtRatioAX96, sqrtRatioBX96, liquidity, True)
#
# def getAmount1Delta( sqrtRatioAX96,sqrtRatioBX96,liquidity):
#     if liquidity<0:
#         return -getAmount1Delta1(sqrtRatioAX96, sqrtRatioBX96, -liquidity, False)
#     else:
#         return getAmount1Delta1(sqrtRatioAX96, sqrtRatioBX96, liquidity, True)
#

def getAmount0Delta(sqrtRatioAX96, sqrtRatioBX96, liquidity, roundUp):
    if sqrtRatioAX96 > sqrtRatioBX96:
        sqrtRatioAX96, sqrtRatioBX96 = sqrtRatioBX96, sqrtRatioAX96

    numerator1 = liquidity * FixedPoint96.Q96
    numerator2 = sqrtRatioBX96 - sqrtRatioAX96

    if sqrtRatioAX96 <= 0:
        raise ValueError("sqrtRatioAX96 must be greater than 0")

    if roundUp:
        return div_rounding_up(mul_div_rounding_up(numerator1, numerator2, sqrtRatioBX96), sqrtRatioAX96)
    else:
        return mul_div(numerator1, numerator2, sqrtRatioBX96) // sqrtRatioAX96

def getAmount1Delta(sqrtRatioAX96, sqrtRatioBX96, liquidity, roundUp):
    if sqrtRatioAX96 > sqrtRatioBX96:
        sqrtRatioAX96, sqrtRatioBX96 = sqrtRatioBX96, sqrtRatioAX96

    if roundUp:
        return div_rounding_up(liquidity * (sqrtRatioBX96 - sqrtRatioAX96),  FixedPoint96.Q96)
    else:
        return mul_div(liquidity * (sqrtRatioBX96 - sqrtRatioAX96),  FixedPoint96.Q96,  FixedPoint96.Q96)

def getAmount0DeltaWithSign(sqrtRatioAX96, sqrtRatioBX96, liquidity):
    if liquidity < 0:
        return -getAmount0Delta(sqrtRatioAX96, sqrtRatioBX96, abs(liquidity), False)
    else:
        return getAmount0Delta(sqrtRatioAX96, sqrtRatioBX96, liquidity, True)

def getAmount1DeltaWithSign(sqrtRatioAX96, sqrtRatioBX96, liquidity):
    if liquidity < 0:
        return -getAmount1Delta(sqrtRatioAX96, sqrtRatioBX96, abs(liquidity), False)
    else:
        return getAmount1Delta(sqrtRatioAX96, sqrtRatioBX96, liquidity, True)
def div_rounding_up(x, y):
    return  x // y + (x % y > 0)

def mul_div(a, b, denominator):
    # 512-bit multiply [prod1 prod0] = a * b
    # Compute the product mod 2**256 and mod 2**256 - 1
    # then use the Chinese Remainder Theorem to reconstruct
    # the 512-bit result. The result is stored in two 256
    # variables such that product = prod1 * 2**256 + prod0
    prod0 = (a * b) % (2 ** 256)
    prod1 = (a * b // (2 ** 256 - 1)) % (2 ** 256)

    # Handle non-overflow cases, 256 by 256 division
    if prod1 == 0:
        if denominator == 0:
            raise ValueError("Denominator cannot be zero.")
        result = prod0 // denominator
        return result

    # Make sure the result is less than 2**256.
    # Also prevents denominator == 0
    if denominator <= prod1:
        raise ValueError("Denominator must be higher than prod1.")

    # 512 by 256 division.
    remainder = (a * b) % denominator
    prod1 -= remainder > prod0
    prod0 -= remainder

    # Factor powers of two out of denominator
    # Compute the largest power of two divisor of denominator.
    # Always >= 1.
    twos = -denominator & denominator
    # Divide denominator by power of two
    denominator //= twos

    # Divide [prod1 prod0] by the factors of two
    prod0 //= twos

    # Shift in bits from prod1 into prod0
    twos = (twos // 2) ^ (2 ** 256)
    prod0 |= prod1 * twos

    # Invert denominator mod 2**256
    # Compute the inverse by starting with a seed that is correct
    # for four bits.
    inv = pow(3 * denominator, 2, 2 ** 8)
    # Use Newton-Raphson iteration to improve the precision.
    inv *= 2 - denominator * inv  # inverse mod 2**8
    inv *= 2 - denominator * inv  # inverse mod 2**16
    inv *= 2 - denominator * inv  # inverse mod 2**32
    inv *= 2 - denominator * inv  # inverse mod 2**64
    inv *= 2 - denominator * inv  # inverse mod 2**128
    inv *= 2 - denominator * inv  # inverse mod 2**256

    # Because the division is now exact we can divide by multiplying
    # with the modular inverse of denominator.
    result = prod0 * inv
    return result


def mul_div_rounding_up(a, b, denominator):
    result = mul_div(a, b, denominator)
    if (a * b) % denominator > 0:
        if result < 2 ** 256 - 1:
            result += 1
        else:
            raise OverflowError("Result exceeds maximum uint256 value.")
    return result

def to_int256(value, bit_length=256):
    # Giá trị lớn nhất của int256
    max_int256 = 2**(bit_length - 1) - 1

    # Kiểm tra nếu giá trị là âm
    is_negative = value & (1 << (bit_length - 1))

    # Chuyển đổi giá trị sang int256 nếu là âm
    if is_negative:
        return -((~value + 1) & max_int256)
    else:
        return value
def get_amount0_amount1(liquidity, sqrtPriceX96, tick,tickLower,tickUpper ):
    amount0, amount1= 0,0
    if liquidity!=0:
        if tick< tickLower:
            amount0= getAmount0DeltaWithSign(get_sqrt_ratio_at_tick(tickLower),
                                     get_sqrt_ratio_at_tick(tickUpper),
                                     liquidity)
        elif tick< tickUpper:
            amount0= getAmount0DeltaWithSign(sqrtPriceX96, get_sqrt_ratio_at_tick(tickUpper), liquidity)
            amount1= getAmount1DeltaWithSign(get_sqrt_ratio_at_tick(tickLower), sqrtPriceX96, liquidity)
        else:
            amount1= getAmount1DeltaWithSign(get_sqrt_ratio_at_tick(tickLower),
                                     get_sqrt_ratio_at_tick(tickUpper),
                                     liquidity)
    return amount0, amount1


if __name__=="__main__":
    amount0, amount1=get_amount0_amount1(liquidity=19532091583577030936, sqrtPriceX96= 1889130429728103422674378119229, tick= 63433, tickLower=52200, tickUpper=66000)
    print(amount0, amount1)
    while amount0<0:

        amount0 =to_int256(amount0)
    print(amount0)