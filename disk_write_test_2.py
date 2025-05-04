import time
import os
import statistics

def write_file(file_path, size_mb):
    block_size = 1024 * 1024  # 1 MB
    total_blocks = size_mb

    with open(file_path, 'wb') as f:
        for _ in range(total_blocks):
            f.write(os.urandom(block_size))  # random data

def read_file(file_path):
    block_size = 1024 * 1024  # 1 MB

    with open(file_path, 'rb') as f:
        while f.read(block_size):
            pass

def timed_run(func, *args):
    start = time.time()
    func(*args)
    return time.time() - start

def run_tests(file_path, size_mb, repeats=3):
    print(f"\n📁 Size: {size_mb} MB | 📄 File: {file_path} | 🔁 Repeats: {repeats}")

    write_times = []
    read_times = []

    for i in range(repeats):
        print(f"  ➤ Iteration {i+1}/{repeats}...")

        # Write
        wt = timed_run(write_file, file_path, size_mb)
        write_times.append(wt)

        # Read
        rt = timed_run(read_file, file_path)
        read_times.append(rt)

        os.remove(file_path)  # clean up for next iteration

    # Statistics
    def summarize(name, values):
        avg = statistics.mean(values)
        minimum = min(values)
        maximum = max(values)
        print(f"📊 {name} - Avg: {avg:.2f}s | Min: {minimum:.2f}s | Max: {maximum:.2f}s")

    summarize("Write", write_times)
    summarize("Read", read_times)

if __name__ == "__main__":
    sizes = [10, 50, 100, 500, 1000, 5000, 10000]  # in MB (you can remove 10000 if space is limited)
    repeats = 7
    output_dir = "test_output"
    os.makedirs(output_dir, exist_ok=True)

    for size in sizes:
        file_path = os.path.join(output_dir, f"test_{size}mb.bin")
        run_tests(file_path, size, repeats)
