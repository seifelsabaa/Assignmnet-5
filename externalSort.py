import os
import heapq

CHUNK_SIZE = 4 * 1024 * 1024  # 4 MB

def read_chunk(file, max_bytes):
    data = []
    size = 0
    while size < max_bytes:
        line = file.readline()
        if not line:
            break
        size += len(line)
        data.append(int(line.strip()))
    return data

def external_sort(input_file, output_file):
    print("Starting external sort...")

    temp_files = []

    with open(input_file, 'r') as f:
        while True:
            chunk = read_chunk(f, CHUNK_SIZE)
            if not chunk:
                break
            chunk.sort()
            name = f"run_{len(temp_files)}.txt"
            with open(name, 'w') as t:
                for num in chunk:
                    t.write(str(num) + "\n")
            temp_files.append(name)
            print(f"Created run file: {name}")

    print("Merging sorted chunks...")

    min_heap = []
    fps = []

    for name in temp_files:
        fp = open(name, 'r')
        fps.append(fp)
        line = fp.readline()
        if line:
            heapq.heappush(min_heap, (int(line), len(fps)-1))

    with open(output_file, 'w') as out:
        while min_heap:
            val, idx = heapq.heappop(min_heap)
            out.write(str(val) + "\n")
            nxt = fps[idx].readline()
            if nxt:
                heapq.heappush(min_heap, (int(nxt), idx))

    for fp in fps:
        fp.close()
    for name in temp_files:
        os.remove(name)

    print("Done! Output written to output.txt")


external_sort("input.txt", "output.txt")
