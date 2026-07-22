import sys
import platform
import subprocess

async def get_cpu_model():
    if sys.platform.startswith("linux"):
        try:
            with open("/proc/cpuinfo") as f:
                for line in f:
                    if "model name" in line:
                        return line.split(":", 1)[1].strip()
        except:
            pass

    # fallback for Windows / macOS / unknown
    return platform.uname().processor or "Unknown CPU"

async def get_hardware_model():
    if platform.system() == "Linux":
        paths = [
            "/sys/devices/virtual/dmi/id/product_name",
            "/sys/devices/virtual/dmi/id/product_version",
            "/sys/devices/virtual/dmi/id/board_name",
            "/sys/devices/virtual/dmi/id/sys_vendor",
        ]
        parts = []
        for p in paths:
            try:
                with open(p) as f:
                    parts.append(f.read().strip())
            except:
                pass
        return " ".join(parts).strip() or None

    if platform.system() == "Darwin":
        return subprocess.check_output(
            ["sysctl", "-n", "hw.model"]
        ).decode().strip()

    if platform.system() == "Windows":
        out = subprocess.check_output(
            ["wmic", "csproduct", "get", "name"]
        ).decode().strip().split("\n")
        return out[1].strip() if len(out) > 1 else None

    return None