# Supercomputer Execution Guide

## Overview

This repository contains the training code for the Whisper Sinhala model. The code has been verified on Google Colab but requires adaptation for the cluster environment.

## Note to the Operator

The enclosed codebase has been successfully tested and verified in a Google Colab environment. However, I am aware that adapting it for the supercomputer will require several configuration adjustments, particularly regarding file system paths. The Google Drive mounts and local path references in `run_training.py` and `training_args.json` will need to be remapped to the cluster’s specific Scratch directory.

Regarding the workflow, please note:

- **Data Preparation:** The `prepare_data` script is designed to run prior to training to ensure data is properly localized.
- **Checkpointing:** I have implemented checkpointing logic (via `save_steps` and `resume_from_checkpoint`) to safeguard against time-limit interruptions.
- **Authentication:** If the model weights need to be re-downloaded on the node, please ensure a valid `HF_TOKEN` is set in the environment.

Since I lack familiarity with the cluster's specific scheduling environment, I have not included the necessary scheduler/job scripts (e.g., Slurm). Please feel free to alter the code or hyperparameters as you see fit to optimize performance.

I sincerely apologize for any inefficiencies or errors in the implementation and am incredibly grateful for your time and expertise in helping me execute this run.
