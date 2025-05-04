import grpc
import os
import file_transfer_pb2
import file_transfer_pb2_grpc
import time

CHUNK_SIZE = 1024 * 1024  # 1MB

def load_chunks_into_memory(file_path):
    chunks = []
    filename = os.path.basename(file_path)
    with open(file_path, 'rb') as f:
        offset = 0
        while chunk := f.read(CHUNK_SIZE):
            chunks.append(file_transfer_pb2.FileChunk(
                content=chunk,
                filename=filename,
                offset=offset
            ))
            offset += len(chunk)
    return chunks

def run(file_path):
    file_size = os.path.getsize(file_path)
    chunks = load_chunks_into_memory(file_path)

    channel = grpc.insecure_channel('localhost:50051')
    stub = file_transfer_pb2_grpc.FileTransferStub(channel)

    start_time = time.time()
    response = stub.UploadFile(iter(chunks))
    end_time = time.time()

    elapsed_time = end_time - start_time
    print("Upload response:", response.message)
    print(f"File upload took {elapsed_time:.2f} seconds.")
    print(f"File size: {file_size / (1024 * 1024):.2f} MB")

if __name__ == '__main__':
    run("test_output/test_10000mb.bin")
