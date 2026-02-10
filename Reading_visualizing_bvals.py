# -*- coding: utf-8 -*-
"""
Created on Mon Jun 19 13:07:02 2023

@author: Christos tsepas
"""
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from dipy.io import read_bvals_bvecs


def compute_and_plot_b_matrices(
    data_path: str | Path,
    output_txt: str | Path = "b_matrices.txt",
    plot: bool = True,
):
    """
    Compute b-matrices from .bval and .bvec files.
    Parameters
    ----------
    data_path : str or Path
        Path to either:
        - a directory containing one .bval and one .bvec file, OR
        - the base filename without extension
    output_txt : str or Path
        Output text file for b-matrices
    plot : bool
        Whether to generate a plot
    """

    data_path = Path(data_path)
    # Case 1: directory provided
    if data_path.is_dir():
        bval_files = list(data_path.glob("*.bval"))
        bvec_files = list(data_path.glob("*.bvec"))

        if len(bval_files) != 1 or len(bvec_files) != 1:
            raise ValueError("Directory must contain exactly one .bval and one .bvec file")

        fbvals = bval_files[0]
        fbvecs = bvec_files[0]

    # Case 2: base filename provided
    else:
        fbvals = data_path.with_suffix(".bval")
        fbvecs = data_path.with_suffix(".bvec")

        if not fbvals.exists() or not fbvecs.exists():
            raise FileNotFoundError("Could not find matching .bval / .bvec files")

    # Load b-values and b-vectors
    bvals, bvecs = read_bvals_bvecs(fbvals, fbvecs)

    # Compute b-matrices
    b_matrices = [
        bval * np.outer(bvec, bvec)
        for bval, bvec in zip(bvals, bvecs)
    ]

    # Write to file
    output_txt = Path(output_txt)
    with output_txt.open("w") as f:
        for i, b_matrix in enumerate(b_matrices):
            f.write(f"b-matrix {i + 1}:\n")
            np.savetxt(f, b_matrix, delimiter="\t", fmt="%.6f")
            f.write("\n")
    # Optional plotting
    if plot:
        fig = plt.figure()
        ax = fig.add_subplot(111, projection="3d")

        for b_matrix in b_matrices:
            ax.scatter(b_matrix[:, 0], b_matrix[:, 1], b_matrix[:, 2])
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_zlabel("Z")
        plt.show()

    return b_matrices





    

 
