# Major-Project
Code created from the MSc thesis Diffusion kurtosis imaging of the auditory nerve in unilateral and bilateral deaf patients: An automated processing and analysis pipeline (https://studenttheses.uu.nl/handle/20.500.12932/46434).

## Overview
This repository implements a *an automated processing and analysis pipeline to analyse dMRI data. The approach combines preprocessing steps, modeeling and tractography analysis of the auditory nerve.

---

## Method Summary
The pipeline operates on a diffusion MRI 4D data and T2 weighted images. The user can type in the UI about the steps they want to perform.

- Preprocessing steps include denoising, signal drift correction, eddy current correction, normalization, cropping and masking.
- Part of the preprocessing steps are being done in MATLAB by loading the backend fucntions of ExploreDTI toolbox.
- Tractogrpahy analysis including ROI creation based on cochlae masks, analysis and segmentation of the tracts.
