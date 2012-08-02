import numpy as np
import math

chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_'
chars_to_indices = dict([(chars[i],i) for i in xrange(64)])

# This constant is 2^17, the value that represents the sign in an 18-bit two's
# complement encoding. The minimum integer that can be represented in such an
# encoding is -SIGN_BIT, and the maximum is SIGN_BIT - 1.
SIGN_BIT = 131072

def twosComplementEncode(number):
    """
    Given a number, return a three-character string representing
    (the integer part of) it, as 18-bit two's complement.

    See documentation in pack64_specs.txt.
    """
    number = int(number)
    assert -SIGN_BIT <= number < (SIGN_BIT - 1), "Integer out of range: %d" % number
    if number < 0:
        number += SIGN_BIT * 2
    
    # using // for forward-compatible integer division
    first = number // 4096
    without_firstval = number - 4096 * first
    second = without_firstval // 64
    third = without_firstval - 64*second
    return chars[first] + chars[second] + chars[third]

def twosComplementDecode(string):
    """
    Given a three-character string (encoded from twosComplementEncode),
    return the integer it represents.
    See documentation in pack64_specs.txt.
    """
    number = 4096 * chars_to_indices[string[0]] + \
               64 * chars_to_indices[string[1]] + \
                    chars_to_indices[string[2]]
    if number > 131071:
        number -= 262144
    return number

def pack64(vector):
    """
    Return a string encoding of the given numpy array.
    See documentation in pack64_specs.txt.
    """
    vector = np.asarray(vector)
    highest = max(np.abs(vector))
    if np.isinf(highest) or np.isnan(highest):
        raise ValueError, 'Vector contains an invalid value.'
    if not highest:
        lowest_unused_power = -40
    else:
        lowest_unused_power = int(math.floor(math.log(highest, 2))) + 1
        if lowest_unused_power > 40:
            raise OverflowError
    exponent = max(lowest_unused_power-17, -40)
    increment = 2**exponent
    first = exponent + 40
    newvector = vector / float(increment)
    encoded = [twosComplementEncode(value) for value in newvector]
    return chars[first] + ''.join(encoded)

def unpack64(string):
    """
    Decode the given string (encoded from pack64) into a np array.
    See documentation in pack64_specs.txt.
    """
    increment = 2**(chars_to_indices[string[0]] - 40)
    numbers = np.array([chars_to_indices[s] for s in string[1:]])
    highplace = numbers[::3]
    midplace = numbers[1::3]
    lowplace = numbers[2::3]
    values = 4096*highplace + 64*midplace + lowplace
    signs = (values >= SIGN_BIT)
    values -= 2 * signs * SIGN_BIT
    return np.array(values) * increment

