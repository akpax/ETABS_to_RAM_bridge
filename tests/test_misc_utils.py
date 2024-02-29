import pytest
import numpy as np
from math import sqrt

from ..utils.misc_utils import *


# pytest.mark.parameterize confused by np array (double counted params)
# this is next best option
class Test_find_rotation_matrix:
    def test_find_rotation_matrix_case1(self):
        # test 90 deg counter-clockwise rotation
        assert np.allclose(
            find_rotation_matrix([0, 1], [-1, 0]), np.array([[0, -1], [1, 0]])
        )

    def test_find_rotation_matrix_case2(self):
        # test 90 deg clockwise rotation
        assert np.allclose(
            find_rotation_matrix([0, 1], [1, 0]), np.array([[0, 1], [-1, 0]])
        )

    def test_find_rotation_matrix_case3(self):
        # test 90 deg counter-clockwise rotation w/ different src_vec
        assert np.allclose(
            find_rotation_matrix([1, 0], [0, 1]), np.array([[0, -1], [1, 0]])
        )

    def test_find_rotation_matrix_case4(self):
        # test 90 deg clockwise rotation w/ different src_vec
        assert np.allclose(
            find_rotation_matrix([0, -1], [-1, 0]), np.array([[0, 1], [-1, 0]])
        )

    def test_find_rotation_matrix_45deg(self):
        # 45 degree counter clock rotation
        assert np.allclose(
            find_rotation_matrix([1, 0], [1, 1]),
            np.array([[1, -1], [1, 1]]),
        )

    def test_find_rotation_matrix_same_vec(self):
        # test same src_vec and dest_vec case
        assert np.allclose(
            find_rotation_matrix([-1, -1], [-1, -1]), np.array([[1, 0], [0, 1]])
        )

    def test_find_rotation_matrix_same_vec_diff_magnitude(self):
        # test same src_vec and dest_vec directions with different
        # src_vec and dest_vec magnitudes
        assert np.allclose(
            find_rotation_matrix([2, 2], [1, 1]), np.array([[1, 0], [0, 1]])
        )


def test_delta_vec():
    vec1 = [1, 2]
    vec2 = [-1, 4]
    assert delta_vec(*vec1, *vec2) == (2, -2)


def test_calibrate_rotation_and_translation():
    """
    test calibrate function n scenario where rotation and transation of points is required
    """
    src_pt1 = [-1, 0]
    src_pt2 = [1, 0]
    out_pt1 = [1, 1]
    out_pt2 = [1, 3]
    rotation_matrix, delta_translation = calibrate(src_pt1, src_pt2, out_pt1, out_pt2)
    assert np.allclose(rotation_matrix, np.array([[0, -1], [1, 0]]))
    assert np.allclose(delta_translation, np.array([1, 2]))


def test_convert_point_to_new_coord_system():
    """
    test in scenario where rotation and transation of points is required
    """
    rotation_matrix = np.array([[0, -1], [1, 0]])
    delta_translation = np.array([1, 2])
    src_pt1 = [-1, 0]
    out_pt1 = [1, 1]
    assert np.allclose(
        convert_point_to_new_coord_system(*src_pt1, rotation_matrix, delta_translation),
        out_pt1,
    )
