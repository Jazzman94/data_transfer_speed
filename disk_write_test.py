import time
import os

def write_test(file_path, size_mb):
    block_size = 1024 * 1024  # 1 MB
    total_blocks = size_mb

    print(f"\nZapisování {size_mb} MB do: {file_path}")

    start_time = time.time()
    with open(file_path, 'wb') as f:
        for _ in range(total_blocks):
            f.write(os.urandom(block_size))  # náhodná data (simuluje reálný zápis)
    end_time = time.time()

    duration = end_time - start_time
    speed = size_mb / duration

    print(f"⏱️ Trvání: {duration:.2f} s | 📈 Rychlost: {speed:.2f} MB/s")

if __name__ == "__main__":
    sizes = [10, 100, 1000, 10000]  # v MB
    output_dir = "test_output"
    os.makedirs(output_dir, exist_ok=True)

    for size in sizes:
        file_path = os.path.join(output_dir, f"test_{size}mb.bin")
        write_test(file_path, size)
