# !/usr/bin/python
# -*- coding: utf-8 -*-
"""myds - A Data Science Package (https://github.com/augustomatheuss/myds)

Module ctl from myds for central limit theorem (CLT).
Copyright 2020 Augusto Damasceno

Redistribution and use in source and binary forms, with or without modification,
are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice,
this list of conditions and the following disclaimer.
2. Redistributions in binary form must reproduce the above copyright notice,
this list of conditions and the following disclaimer in the documentation
and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT,
INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE,
EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

__author__ = "Augusto Damasceno (augustodamasceno@protonmail.com)"
__version__ = "0.2"
__copyright__ = "Copyright (c) 2020 Augusto Damasceno"
__license__ = "2-Clause BSD License"

from scipy.stats import norm
import numpy as np


def sample_size_z(z, std, max_error):
    """
    Return the sample size required for the specified z-multiplier, standard deviation and maximum error.
    :param z: z-multiplier
    :param std: Standard deviation
    :param max_error: Maximum error
    :return: Required sample size
    """
    return pow(z, 2.0) * pow((std / max_error), 2.0)


def sample_size_conf(confidence, std, max_error):
    """
    Return the sample size required for the specified confidence level, standard deviation and maximum error.
    :param confidence: Confidence level
    :param std: Standard deviation
    :param max_error: Maximum error
    :return: Required sample size
    """
    # norm.interval(confidence) == (norm.ppf(((1.0-confidence)/2.0)), norm.ppf((1.0-(1.0-confidence)/2.0)))
    z = norm.interval(confidence)[1]
    return pow(z, 2.0) * pow((std / max_error), 2.0)


def get_error(sample_size, z, std):
    """
    Return the maximum error for the specified sample size, z-multiplier and standard deviation.
    :param sample_size: Sample size
    :param z: z-multiplier
    :param std: Standard deviation
    :return: Maximum error
    """
    return z * (std/np.sqrt(sample_size))


def get_error_conf(sample_size, confidence, std):
    """
    Return the maximum error for the specified sample size, confidence level and standard deviation.
    :param sample_size: Sample size
    :param confidence: Confidence level
    :param std: Standard deviation
    :return: Maximum error
    """
    # norm.interval(confidence) == (norm.ppf(((1.0-confidence)/2.0)), norm.ppf((1.0-(1.0-confidence)/2.0)))
    z = norm.interval(confidence)[1]
    return z * (std/np.sqrt(sample_size))


if __name__ == "__main__":
    """ If the module is called as script, plot the probability density function 
        and the cumulative distribution function.
        Modified from: https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.norm.html
    """
    from scipy.stats import norm
    import matplotlib.pyplot as plt
    import numpy as np

    print('Plotting the Probability Density Function'
          + '\n and the Cumulative Density Function')
    x = np.linspace(norm.ppf(0.001), norm.ppf(0.999), 100)
    plt.subplot(1, 2, 1)
    plt.plot(x, norm.pdf(x), 'r-', lw=5, alpha=0.6)
    plt.title("Probability Density Function")
    plt.xlabel("norm.ppf(0.001) <= x <= norm.ppf(0.999)")
    plt.ylabel("norm.pdf(x)")
    plt.subplot(1, 2, 2)
    plt.plot(x, norm.cdf(x), 'b-', lw=5, alpha=0.6)
    plt.title("Cumulative Density Function")
    plt.xlabel("norm.ppf(0.001) <= x <= norm.ppf(0.999)")
    plt.ylabel("norm.cdf(x)")
    plt.show()
