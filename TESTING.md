# Testing Guide for AI Coders

## Overview

This document outlines the standard procedure for testing code in this repository. The goal is to have a consistent and reproducible testing process that is well-documented and easy for other AI coders to follow.

The core philosophy is that each feature or agent should be self-contained in its own directory, which includes the code, the tests, and the documentation for the test results.

## Standard Procedure

Here is the step-by-step guide for testing a new feature or agent:

### 1. Create a Dedicated Directory

For each new feature or agent, create a new directory in the root of the repository. The directory name should be descriptive of the feature or agent.

For example, if you are creating a new agent called `data_processing_agent`, you would create a directory named `data_processing_agent`.

### 2. Add Necessary Files

Inside the feature's directory, you should have the following files:

*   `feature_name.py`: The core logic for the feature or agent.
*   `feature_name_test.py` or `feature_name_example.py`: The script for testing the feature or running an example. This script should be runnable from the command line.
*   `feature_name_results.md`: A markdown file that documents the results of the test.

### 3. Write and Run Tests

The test script should be written to be executed from the command line. When running the test, you should redirect the output to a file. This captured output will be used to update the results documentation.

For example:

```bash
python feature_name/feature_name_test.py > feature_name/test_results.txt
```

### 4. Update Documentation

After running the test, you should update the `feature_name_results.md` file with the content of the `test_results.txt` file. This ensures that the documentation is always up-to-date with the latest test results.

You can use the following command to copy the content of the `test_results.txt` file to the `feature_name_results.md` file:

```bash
cat feature_name/test_results.txt > feature_name/feature_name_results.md
```

### 5. Clean Up

After updating the documentation, you can remove the `test_results.txt` file.

## Example: `base_agent`

Here is a walkthrough of the steps that were taken to test the `base_agent` and update its documentation.

### 1. Directory Structure

The `base_agent` feature is contained in the `base_agent` directory, which has the following structure:

```
base_agent/
├── base_agent.py
├── base_agent_example.py
└── improved-base-agent.md
```

*   `base_agent.py`: The core logic for the base agent.
*   `base_agent_example.py`: The benchmark script for the base agent.
*   `improved-base-agent.md`: The documentation for the benchmark results.

### 2. Running the Benchmark

The benchmark was run using the following command, which redirected the output to a file named `benchmark_results.txt`:

```bash
python base_agent/base_agent_example.py > benchmark_results.txt
```

### 3. Updating the Documentation

The `improved-base-agent.md` file was updated with the content of the `benchmark_results.txt` file using the following command:

```bash
cat benchmark_results.txt > base_agent/improved-base-agent.md
```

### 4. Cleaning Up

The `benchmark_results.txt` file was removed after updating the documentation.

By following this procedure, we can ensure that all features and agents in this repository are well-tested and that the test results are properly documented.
