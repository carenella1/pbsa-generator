from pathlib import Path
import shutil
import os
import stat

BASE_DIR = Path(__file__).resolve().parent.parent
BUILD_DIR = BASE_DIR / "output" / "builds"


def remove_readonly(func, path, excinfo):
    os.chmod(path, stat.S_IWRITE)
    func(path)


def cleanup():

    if not BUILD_DIR.exists():
        print("Build directory does not exist.")
        return

    deleted = False

    for folder in BUILD_DIR.iterdir():

        if folder.is_dir():

            try:
                shutil.rmtree(folder, onerror=remove_readonly)
                print(f"Deleted: {folder.name}")
                deleted = True

            except Exception as e:
                print(f"Failed to delete {folder.name}: {e}")

    if not deleted:
        print("No builds to delete.")

    print("Cleanup complete.")


if __name__ == "__main__":
    cleanup()