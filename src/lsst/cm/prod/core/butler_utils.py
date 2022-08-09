# This file is part of cm_prod
#
# Developed for the LSST Data Management System.
# This product includes software developed by the LSST Project
# (https://www.lsst.org).
# See the COPYRIGHT file at the top-level directory of this distribution
# for details of code ownership.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from typing import Iterable

import numpy as np
from lsst.daf.butler import Butler


def get_sorted_array(itr: Iterable, field: str) -> np.ndarray:
    the_set = set()
    for x_ in itr:
        the_set.add(x_.dataId[field])
    the_array = np.array([x_ for x_ in the_set])
    return np.sort(the_array)


def build_data_queries(
    butler: Butler,
    dataset: str,
    field: str,
    min_queries: int = 1,
    max_step_size: int = 10000000,
) -> list[str]:

    itr = butler.registry.queryDatasets(dataset)
    sorted_field_values = get_sorted_array(itr, field)

    n_matched = sorted_field_values.size

    step_size = min(max_step_size, int(n_matched / min_queries))

    ret_list = []

    previous_idx = 0
    idx = 0

    while idx < n_matched:
        idx += step_size
        max_idx = min(idx, n_matched - 1)
        min_val = sorted_field_values[previous_idx]
        max_val = sorted_field_values[max_idx]
        ret_list.append(f"instrument = 'HSC' and ({min_val} <= {field}) and ({field} < {max_val})")
        previous_idx = idx

    return ret_list


if __name__ == "__main__":

    from lsst.daf.butler import Butler

    the_butler = Butler("/sdf/group/rubin/repo/main", collections=["HSC/raw/RC2"])

    data_queries_0 = build_data_queries(the_butler, "raw", "exposure")
    data_queries_1 = build_data_queries(the_butler, "raw", "exposure", 5)
    data_queries_2 = build_data_queries(the_butler, "raw", "exposure", 1, 20)
    data_queries_3 = build_data_queries(the_butler, "raw", "exposure", 5, 20)
