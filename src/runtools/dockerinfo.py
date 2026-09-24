#!/usr/bin/env python3
"""Shows an overview of Docker images, containers, volumes and build cache sorted by size."""

import argparse
import subprocess
import re
import sys


def parse_size_to_bytes(size_str: str) -> int:
    """Converts a text size (e.g. '1.5GB', '500MB', '2kB') to bytes."""
    size_str = size_str.strip()
    units = {
        "B":   1,
        "KB":  1_000,
        "MB":  1_000_000,
        "GB":  1_000_000_000,
        "TB":  1_000_000_000_000,
        "KIB": 1_024,
        "MIB": 1_048_576,
        "GIB": 1_073_741_824,
        "TIB": 1_099_511_627_776,
    }
    match = re.fullmatch(r"([\d.]+)\s*([A-Za-z]+)", size_str)
    if match:
        value = float(match.group(1))
        unit = match.group(2).upper()
        return int(value * units.get(unit, 1))
    # If the number has no unit, assume bytes
    try:
        return int(float(size_str))
    except ValueError:
        return 0


def format_size(size_bytes: int) -> str:
    """Formats bytes into a human-readable form."""
    for unit, threshold in [("TB", 1e12), ("GB", 1e9), ("MB", 1e6), ("KB", 1e3)]:
        if size_bytes >= threshold:
            return f"{size_bytes / threshold:.2f} {unit}"
    return f"{size_bytes} B"


def get_volumes_with_sizes() -> list[tuple[str, int, str]]:
    """
    Returns a list of (name, size_in_bytes, size_text) for all Docker volumes.
    Uses 'docker system df -v' to obtain the sizes.
    """
    try:
        result = subprocess.run(
            ["docker", "system", "df", "-v"],
            capture_output=True, text=True, check=True
        )
    except subprocess.CalledProcessError as e:
        print(f"Error running docker: {e.stderr}", file=sys.stderr)
        sys.exit(1)
    except FileNotFoundError:
        print("Docker is not installed or not available in PATH.", file=sys.stderr)
        sys.exit(1)

    volumes = []
    in_volumes_section = False
    header_found = False

    for line in result.stdout.splitlines():
        stripped = line.strip()

        # Detect the start of the volumes section
        if re.match(r"local volumes", stripped, re.IGNORECASE):
            in_volumes_section = True
            header_found = False
            continue

        if not in_volumes_section:
            continue

        # Skip the table header and note that we're past it
        if re.match(r"VOLUME\s+NAME", stripped, re.IGNORECASE):
            header_found = True
            continue

        # Skip a blank line before the header; after the header, end the section
        if stripped == "":
            if header_found:
                in_volumes_section = False
                header_found = False
            continue

        # Data rows (only after the header is found)
        if header_found:
            parts = stripped.split()
            if len(parts) >= 3:
                name = parts[0]
                size_str = parts[-1]
                size_bytes = parse_size_to_bytes(size_str)
                volumes.append((name, size_bytes, size_str))

    return volumes


def get_containers_with_sizes() -> list[tuple[str, int, int, str]]:
    """
    Returns a list of (name, own_size_bytes, virtual_size_bytes, status)
    for all Docker containers. Uses 'docker ps -a --size'.
    """
    try:
        result = subprocess.run(
            ["docker", "ps", "-a", "--size",
             "--format", "{{.Names}}\t{{.Size}}\t{{.Status}}"],
            capture_output=True, text=True, check=True
        )
    except subprocess.CalledProcessError as e:
        print(f"Error running docker: {e.stderr}", file=sys.stderr)
        sys.exit(1)
    except FileNotFoundError:
        print("Docker is not installed or not available in PATH.", file=sys.stderr)
        sys.exit(1)

    containers = []
    # SIZE format: "1.71GB (virtual 4.22GB)"
    size_pattern = re.compile(r"^([\d.]+\s*\S+)\s+\(virtual\s+([\d.]+\s*\S+)\)$", re.IGNORECASE)

    for line in result.stdout.splitlines():
        line = line.strip()
        if not line:
            continue
        parts = line.split("\t")
        if len(parts) < 3:
            continue
        name, size_str, status = parts[0], parts[1], parts[2]
        m = size_pattern.match(size_str.strip())
        if m:
            own_bytes = parse_size_to_bytes(m.group(1))
            virtual_bytes = parse_size_to_bytes(m.group(2))
        else:
            own_bytes = parse_size_to_bytes(size_str.strip())
            virtual_bytes = own_bytes
        containers.append((name, own_bytes, virtual_bytes, status))

    return containers


def get_networks_summary() -> tuple[list[tuple[str, str, str]], int]:
    """
    Returns (list of (name, driver, subnet), total_count_of_all_networks).
    Uses 'docker network ls' and 'docker network inspect'.
    """
    try:
        ls_result = subprocess.run(
            ["docker", "network", "ls", "--format", "{{.ID}}\t{{.Name}}\t{{.Driver}}"],
            capture_output=True, text=True, check=True
        )
    except subprocess.CalledProcessError as e:
        print(f"Error running docker: {e.stderr}", file=sys.stderr)
        sys.exit(1)
    except FileNotFoundError:
        print("Docker is not installed or not available in PATH.", file=sys.stderr)
        sys.exit(1)

    all_networks = []
    bridge_ids = []

    for line in ls_result.stdout.splitlines():
        parts = line.strip().split("\t")
        if len(parts) < 3:
            continue
        net_id, name, driver = parts[0], parts[1], parts[2]
        all_networks.append((name, driver))
        if driver == "bridge":
            bridge_ids.append(net_id)

    # For bridge networks, determine the subnet via inspect
    networks = []
    if bridge_ids:
        insp = subprocess.run(
            ["docker", "network", "inspect"] + bridge_ids +
            ["--format", "{{.Name}}\t{{.Driver}}\t{{range .IPAM.Config}}{{.Subnet}}{{end}}"],
            capture_output=True, text=True
        )
        for line in insp.stdout.splitlines():
            line = line.strip()
            if not line:
                continue
            parts = line.split("\t")
            name   = parts[0] if len(parts) > 0 else ""
            driver = parts[1] if len(parts) > 1 else "bridge"
            subnet = parts[2] if len(parts) > 2 else ""
            networks.append((name, driver, subnet))

    return networks, len(all_networks)


def get_images_with_sizes() -> list[tuple[str, int, int, int, str]]:
    """
    Returns a list of (name, unique_bytes, shared_bytes, virtual_bytes, containers)
    for all Docker images. unique_bytes = actual disk space used.
    Uses 'docker system df -v'.
    """
    try:
        result = subprocess.run(
            ["docker", "system", "df", "-v"],
            capture_output=True, text=True, check=True
        )
    except subprocess.CalledProcessError as e:
        print(f"Error running docker: {e.stderr}", file=sys.stderr)
        sys.exit(1)
    except FileNotFoundError:
        print("Docker is not installed or not available in PATH.", file=sys.stderr)
        sys.exit(1)

    images = []
    in_section = False
    header_found = False
    col: dict[str, int] = {}

    for line in result.stdout.splitlines():
        stripped = line.strip()

        if re.match(r"images space usage", stripped, re.IGNORECASE):
            in_section = True
            header_found = False
            continue

        if not in_section:
            continue

        if re.match(r"REPOSITORY", stripped, re.IGNORECASE):
            header_found = True
            # Column positions from the header — SIZE must come before SHARED SIZE
            col['shared'] = line.index('SHARED SIZE')
            col['unique'] = line.index('UNIQUE SIZE')
            col['containers'] = line.index('CONTAINERS')
            col['size'] = line.index('SIZE')   # first occurrence = standalone SIZE
            continue

        if stripped == "":
            if header_found:
                in_section = False
                header_found = False
            continue

        if header_found and col:
            repo_part  = line[:col['size']].strip()
            size_str   = line[col['size']:col['shared']].strip()
            shared_str = line[col['shared']:col['unique']].strip()
            unique_str = line[col['unique']:col['containers']].strip()
            containers_str = line[col['containers']:].strip()

            # repo_part = "REPO   TAG   IMAGE_ID   CREATED …"
            parts  = re.split(r'\s{2,}', repo_part)
            repo   = parts[0] if len(parts) > 0 else "<none>"
            tag    = parts[1] if len(parts) > 1 else "<none>"
            img_id = parts[2] if len(parts) > 2 else ""

            if repo == "<none>" and tag == "<none>":
                name = f"<none> ({img_id})"
            elif tag in ("<none>", ""):
                name = repo
            else:
                name = f"{repo}:{tag}"

            images.append((
                name,
                parse_size_to_bytes(unique_str),
                parse_size_to_bytes(shared_str),
                parse_size_to_bytes(size_str),
                containers_str,
            ))

    return images


def get_build_cache_summary() -> tuple[int, int, int]:
    """
    Returns (entry_count, total_bytes, reclaimable_bytes) for the build cache.
    Uses 'docker system df'.
    """
    try:
        result = subprocess.run(
            ["docker", "system", "df"],
            capture_output=True, text=True, check=True
        )
    except subprocess.CalledProcessError as e:
        print(f"Error running docker: {e.stderr}", file=sys.stderr)
        sys.exit(1)
    except FileNotFoundError:
        print("Docker is not installed or not available in PATH.", file=sys.stderr)
        sys.exit(1)

    for line in result.stdout.splitlines():
        if re.match(r"build cache", line.strip(), re.IGNORECASE):
            # "Build Cache   2753   0   71.37GB   70.33GB (98%)"
            parts = line.split()
            if len(parts) >= 6:
                try:
                    return (
                        int(parts[2]),
                        parse_size_to_bytes(parts[4]),
                        parse_size_to_bytes(parts[5]),
                    )
                except (ValueError, IndexError):
                    pass
    return (0, 0, 0)


def print_section(title: str, rows: list, col_name: int, columns: list[tuple[str, int, str]]):
    """Prints an aligned table section with the given columns."""
    # Build the header
    header_parts = [f"{'NAME':<{col_name}}"]
    for col_label, col_width, col_align in columns:
        if col_align == ">":
            header_parts.append(f"{col_label:>{col_width}}")
        else:
            header_parts.append(f"{col_label:<{col_width}}")
    header = "  ".join(header_parts)
    separator = "-" * len(header)

    print(f"\n{title}\n")
    print(header)
    print(separator)
    for row in rows:
        name = row[0]
        cells = [f"{name:<{col_name}}"]
        for i, (_, col_width, col_align) in enumerate(columns):
            val = row[i + 1]
            if col_align == ">":
                cells.append(f"{val:>{col_width}}")
            else:
                cells.append(f"{val:<{col_width}}")
        print("  ".join(cells))
    print(separator)


def main():
    argparse.ArgumentParser(description=__doc__).parse_args()

    # ── IMAGES ───────────────────────────────────────────────────────────────
    images = get_images_with_sizes()

    if not images:
        print("\nNo Docker images found.")
    else:
        images.sort(key=lambda x: x[1], reverse=True)
        col_name = max(max(len(img[0]) for img in images), 5)

        rows = [
            (name, format_size(unique), format_size(shared), format_size(virtual), containers)
            for name, unique, shared, virtual, containers in images
        ]
        print_section(
            "Docker images sorted by actual size on disk:",
            rows, col_name,
            [("UNIQUE", 12, ">"), ("SHARED", 12, ">"), ("VIRTUAL", 12, ">"), ("CONT.", 6, ">")],
        )
        total_unique = sum(img[1] for img in images)
        total_virtual = sum(img[3] for img in images)
        print(
            f"{'TOTAL':<{col_name}}  {format_size(total_unique):>12}  {'':>12}  {format_size(total_virtual):>12}"
        )
        print(f"\nNumber of images: {len(images)}")
        print("  UNIQUE  = layers unique to a given image (actual disk space used)")
        print("  SHARED  = layers shared with other images (stored on disk only once)")
        print("  VIRTUAL = total size including shared layers\n")

    # ── CONTAINERS ──────────────────────────────────────────────────────────
    containers = get_containers_with_sizes()

    if not containers:
        print("\nNo Docker containers found.")
    else:
        containers.sort(key=lambda x: x[1], reverse=True)
        col_name = max(max(len(c[0]) for c in containers), 5)

        rows = [
            (name, format_size(own), format_size(virt), status.split(" ")[0])
            for name, own, virt, status in containers
        ]
        print_section(
            "Docker containers sorted by size:",
            rows, col_name,
            [("OWN", 12, ">"), ("VIRTUAL", 12, ">"), ("STATUS", 10, "<")],
        )
        total_own = sum(c[1] for c in containers)
        total_virt = sum(c[2] for c in containers)
        print(
            f"{'TOTAL':<{col_name}}  {format_size(total_own):>12}  {format_size(total_virt):>12}"
        )
        print(f"\nNumber of containers: {len(containers)}")
        print("  OWN     = data written by the container on top of the base image")
        print("  VIRTUAL = own + shared base image\n")

    # ── VOLUMES ──────────────────────────────────────────────────────────────
    volumes = get_volumes_with_sizes()

    if not volumes:
        print("\nNo Docker volumes found.")
    else:
        volumes.sort(key=lambda x: x[1], reverse=True)
        col_name = max(max(len(v[0]) for v in volumes), 11)

        rows = [(name, format_size(size), raw) for name, size, raw in volumes]
        print_section(
            "Docker volumes sorted by size:",
            rows, col_name,
            [("SIZE", 12, ">"), ("RAW", 15, ">")],
        )
        total = sum(v[1] for v in volumes)
        print(f"{'TOTAL':<{col_name}}  {format_size(total):>12}")
        print(f"\nNumber of volumes: {len(volumes)}\n")

    # ── NETWORKS ─────────────────────────────────────────────────────────────
    bridge_networks, total_networks = get_networks_summary()

    # Default Docker limit: 16 networks from 172.16.0.0/12 + 16 from 192.168.0.0/16 = 32
    BRIDGE_POOL_LIMIT = 32
    bridge_used = len(bridge_networks)
    bridge_free = BRIDGE_POOL_LIMIT - bridge_used

    sep = "-" * 100
    print(sep)
    print(f"  Networks: total {total_networks}"
          f"  |  bridge: {bridge_used} used / {BRIDGE_POOL_LIMIT} available"
          f"  ({bridge_free} free)")
    if bridge_networks:
        col = max(len(n[0]) for n in bridge_networks)
        for name, _, subnet in sorted(bridge_networks, key=lambda x: x[2]):
            print(f"    {name:<{col}}  {subnet}")
    print("  Clean up unused:  docker network prune")
    print(sep)
    print()

    # ── BUILD CACHE ───────────────────────────────────────────────────────────
    entries, total_bytes, reclaimable_bytes = get_build_cache_summary()
    if entries > 0:
        pct = int(reclaimable_bytes / total_bytes * 100) if total_bytes else 0
        print("-" * 100)
        print(f"  Build cache: {format_size(total_bytes)}"
              f"  ({entries} entries,"
              f"  reclaimable: {format_size(reclaimable_bytes)} / {pct} %)")
        print("  Clean up:    docker builder prune")
        print("-" * 100)
    print()


if __name__ == "__main__":
    main()
