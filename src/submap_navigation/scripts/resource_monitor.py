#!/usr/bin/env python3
"""
System Resource Monitor
Measures CPU (overall + per-core peak), RAM, and Disk usage over a specified timeframe.
"""

import argparse
import sys
import time
import psutil


def monitor_resources(duration_sec: float, interval_sec: float = 1.0, disk_path: str = "/"):
    print(f"Monitoring started for {duration_sec}s (sampling every {interval_sec}s)...")
    print(f"Target disk partition: {disk_path}")
    print("Press Ctrl+C to stop early and calculate results.\n")

    # Prime psutil CPU counters (the first call returns 0.0 or inaccurate baseline)
    psutil.cpu_percent(percpu=True)
    psutil.cpu_percent(percpu=False)
    time.sleep(0.1)

    cpu_overall_samples = []
    per_core_samples = []  # list of lists: [[core0, core1, ...], [core0, core1, ...]]
    ram_percent_samples = []
    ram_used_mb_samples = []
    disk_percent_samples = []
    disk_used_gb_samples = []

    start_time = time.time()
    num_cores = psutil.cpu_count(logical=True)

    try:
        while True:
            elapsed = time.time() - start_time
            if duration_sec > 0 and elapsed >= duration_sec:
                break

            # Collect CPU metrics
            per_core = psutil.cpu_percent(interval=interval_sec, percpu=True)
            overall_cpu = sum(per_core) / len(per_core) if per_core else 0.0

            # Collect Memory metrics
            vmem = psutil.virtual_memory()

            # Collect Disk metrics
            dusage = psutil.disk_usage(disk_path)

            # Store metrics
            cpu_overall_samples.append(overall_cpu)
            per_core_samples.append(per_core)
            ram_percent_samples.append(vmem.percent)
            ram_used_mb_samples.append(vmem.used / (1024 ** 2))
            disk_percent_samples.append(dusage.percent)
            disk_used_gb_samples.append(dusage.used / (1024 ** 3))

            remaining = max(0.0, duration_sec - (time.time() - start_time)) if duration_sec > 0 else 0
            sys.stdout.write(
                f"\r[Sampling] Elapsed: {int(time.time() - start_time)}s / {int(duration_sec)}s | "
                f"CPU: {overall_cpu:5.1f}% | RAM: {vmem.percent:5.1f}% | Disk: {dusage.percent:5.1f}%"
            )
            sys.stdout.flush()

    except KeyboardInterrupt:
        print("\nMonitoring interrupted by user. Generating report...")

    print("\n" + "=" * 55)
    print("              RESOURCE MONITORING REPORT")
    print("=" * 55)

    if not cpu_overall_samples:
        print("No samples were collected.")
        return

    sample_count = len(cpu_overall_samples)
    actual_duration = time.time() - start_time
    print(f"Total Duration Monitored: {actual_duration:.1f} seconds ({sample_count} samples)")
    print("-" * 55)

    # 1. Overall CPU
    avg_overall_cpu = sum(cpu_overall_samples) / sample_count
    peak_overall_cpu = max(cpu_overall_samples)
    print(f"Overall CPU Usage:")
    print(f"  • Average Usage: {avg_overall_cpu:.2f}%")
    print(f"  • Peak Usage:    {peak_overall_cpu:.2f}%")

    # 2. Per-Core Peaks and Averages
    print(f"\nPer-Core CPU Breakdown ({num_cores} logical cores):")
    for core_idx in range(num_cores):
        core_values = [sample[core_idx] for sample in per_core_samples]
        core_peak = max(core_values)
        core_avg = sum(core_values) / len(core_values)
        print(f"  • Core {core_idx:2d} -> Peak: {core_peak:5.1f}% | Average: {core_avg:5.1f}%")

    # 3. RAM Usage
    avg_ram_pct = sum(ram_percent_samples) / sample_count
    peak_ram_pct = max(ram_percent_samples)
    avg_ram_mb = sum(ram_used_mb_samples) / sample_count
    peak_ram_mb = max(ram_used_mb_samples)
    total_ram_gb = psutil.virtual_memory().total / (1024 ** 3)

    print(f"\nRAM Usage (Total System RAM: {total_ram_gb:.2f} GB):")
    print(f"  • Average Usage: {avg_ram_pct:.2f}% ({avg_ram_mb:.1f} MB)")
    print(f"  • Peak Usage:    {peak_ram_pct:.2f}% ({peak_ram_mb:.1f} MB)")

    # 4. Disk Usage
    avg_disk_pct = sum(disk_percent_samples) / sample_count
    peak_disk_pct = max(disk_percent_samples)
    total_disk_gb = psutil.disk_usage(disk_path).total / (1024 ** 3)

    print(f"\nDisk Space Usage ('{disk_path}', Total: {total_disk_gb:.1f} GB):")
    print(f"  • Average Usage: {avg_disk_pct:.2f}%")
    print(f"  • Peak Usage:    {peak_disk_pct:.2f}%")
    print("=" * 55)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Profile system CPU, RAM, and Disk metrics over time.")
    parser.add_argument(
        "--duration",
        "-d",
        type=float,
        default=30.0,
        help="Monitoring window in seconds (default: 30.0s).",
    )
    parser.add_argument(
        "--interval",
        "-i",
        type=float,
        default=1.0,
        help="Sampling interval in seconds (default: 1.0s).",
    )
    parser.add_argument(
        "--path",
        "-p",
        type=str,
        default="/",
        help="Mount point or directory for disk usage tracking (default: '/').",
    )

    args = parser.parse_args()
    monitor_resources(duration_sec=args.duration, interval_sec=args.interval, disk_path=args.path)
