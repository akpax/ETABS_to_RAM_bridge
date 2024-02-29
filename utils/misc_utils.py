import numpy as np


def rotation_matrix_from_2d_vectors(vec1, vec2):
    """
    Find the rotation matrix that aligns vec1 to vec2 in 2D.
    :param vec1: A 2d "source" vector
    :param vec2: A 2d "destination" vector
    :return: A transform matrix (2x2) which, when applied to vec1, aligns it with vec2.
    """
    # Normalize the vectors
    a = vec1 / np.linalg.norm(vec1)
    b = vec2 / np.linalg.norm(vec2)

    # Compute the cosine and sine of the angle between vec1 and vec2
    cos_theta = np.dot(a, b)
    sin_theta = np.linalg.det(np.array([a, b]))

    # Construct the rotation matrix
    rotation_matrix = np.around(
        np.array([[cos_theta, -sin_theta], [sin_theta, cos_theta]])
    )

    return rotation_matrix


vec1 = [0, 1]
vec2 = [-1, 0]

rot_mat = rotation_matrix_from_2d_vectors(vec1, vec2)

print(rot_mat)
print(type(rot_mat))
