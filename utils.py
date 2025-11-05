"""
Utility functions for system information and runtime details.
Contains helper functions for gathering device, CPU, and model information.
"""

import streamlit as st
import torch
import platform
import multiprocessing
import psutil


def get_runtime_info() -> dict:
    info = {}
    
    is_cuda_available = torch is not None and torch.cuda.is_available()

    if is_cuda_available:
        info["device_info"] = get_gpu_info()
    else:
        info["device_info"] = get_cpu_info()

    if "pipe" in st.session_state:
        info["model_info"] = get_model_info()

    return info


def get_model_info() -> dict:
    model = st.session_state.pipe.model
    device_map = getattr(model, "hf_device_map", None)
    dtype = getattr(model, "dtype", None)

    return {
        "accelerate": device_map is not None,
        "device_map": device_map,
        "dtype": dtype if dtype else "Unknown",
        "model_params": f"{model.num_parameters()/1e6:.2f}M"
    }


def get_gpu_info() -> dict:
    props = torch.cuda.get_device_properties(0)

    return {
        "device": props.name,
        "compute": f"{props.major}.{props.minor}",
        "ram": f"{props.total_memory / 1e9:.2f}GB",
        "cores": props.multi_processor_count
    }


def get_cpu_info() -> dict:
    return {
        "device": platform.processor(),
        "ram": f"{psutil.virtual_memory().total / 1e9:.2f}GB",
        "cores": multiprocessing.cpu_count()
    }