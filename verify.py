import subprocess
import os
from multiprocessing import Pool, cpu_count
from tqdm import tqdm


TIMEOUT = 1000


def check_file(filepath: str):
    """Compile a single Lean file and return (filepath, error or None)."""
    try:
        result = subprocess.run(
            ["lake", "env", "lean", filepath],
            capture_output=True,
            text=True,
            timeout=TIMEOUT
        )
        if result.returncode != 0:
            return filepath, result.stdout.strip()
        return filepath, None
    except subprocess.TimeoutExpired:
        return filepath, f"Timeout: Compilation exceeded {TIMEOUT} seconds"


def check_files(workbook_dir="workbook", log_file="compile_errors.log"):
    # collect all lean files
    lean_files = []
    for root, _, files in os.walk(workbook_dir):
        for f in files:
            if f.endswith(".lean"):
                lean_files.append(os.path.join(root, f))

    print(f"Found {len(lean_files)} Lean files. Running in parallel...")

    errors = []
    # run in parallel with progress bar
    with Pool(cpu_count()) as pool:
        for filepath, err in tqdm(pool.imap_unordered(check_file, lean_files),
                                  total=len(lean_files),
                                  desc="Compiling"):
            if err:
                errors.append((filepath, err))

    # write results
    with open(log_file, "w") as lf:
        for filepath, err in errors:
            lf.write(f"{filepath}:\n")
            lf.write(err + "\n\n")

    # print summary
    print(f"\nSummary: {len(lean_files) - len(errors)} passed, {len(errors)} failed.")
    print(f"Details written to {log_file}")


if __name__ == "__main__":
    check_files()
