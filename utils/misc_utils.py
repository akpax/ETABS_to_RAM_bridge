import numpy as np
from icecream import ic
import pandas as pd


def find_rotation_matrix(src_vec, dest_vec):
    """
    Find the rotation matrix that aligns src_vec to dest_vec in 2D.
    :param src_vec: A 2d "source" vector
    :param dest_vec: A 2d "destination" vector
    :return: A transform matrix (2x2) which, when applied to src_vec, aligns it with dest_vec.
    """
    # Normalize the vectors
    a = src_vec / np.linalg.norm(src_vec)
    b = dest_vec / np.linalg.norm(dest_vec)

    # Compute the cosine and sine of the angle between src_vec and dest_vec
    cos_theta = np.dot(a, b)
    sin_theta = np.linalg.det(np.array([a, b]))

    # Construct the rotation matrix
    rotation_matrix = np.around(
        np.array([[cos_theta, -sin_theta], [sin_theta, cos_theta]])
    )
    print(rotation_matrix)
    return rotation_matrix


def matrix_rotation(x, y, rotation_matrix):
    input_vec = np.array([[x], [y]])
    rotated_vec = rotation_matrix @ input_vec
    return [num for num in rotated_vec.flat]


def delta_vec(x1: float, y1: float, x2: float, y2: float) -> list:
    """
    Finds resulting delta vector between 2 points
    """
    return x1 - x2, y1 - y2


def calibrate(src_pt1: list, src_pt2: list, out_pt1: list, out_pt2) -> tuple:
    """
    Find rotation matrix and translation delta to convert source points (src_pt)
    to output points (out_pt)
    """
    # TODO handle case where
    # use delta vectors bc if model is rotated we care about relative distances between points
    delta_vec_src = delta_vec(*src_pt1, *src_pt2)
    delta_vec_out = delta_vec(*out_pt1, *out_pt2)
    rotation_matrix = find_rotation_matrix(delta_vec_src, delta_vec_out)
    src_pt1_rot = matrix_rotation(*src_pt1, rotation_matrix)
    delta_translation = np.array(delta_vec(*out_pt1, *src_pt1_rot))
    return rotation_matrix, delta_translation


def convert_point_to_new_coord_system(x, y, rotation_matrix, delta_translation):
    return (matrix_rotation(x, y, rotation_matrix) + delta_translation).tolist()


if __name__ == "__main__":
    df = pd.read_csv(
        R"C:\Users\austin.paxton\OneDrive - Mar Structural Design\Documents\Python Projects\ETABs_to_RAM_bridge\validation_data\frames_df_results.csv"
    )
    print(df.head())
