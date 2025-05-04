import grpc
from concurrent import futures
import time

import file_transfer_pb2
import file_transfer_pb2_grpc

class FileTransferServicer(file_transfer_pb2_grpc.FileTransferServicer):
    def UploadFile(self, request_iterator, context):
        print("[SERVER] Receiving file...")

        start_time = time.time()
        total_bytes = 0
        chunk_count = 0

        try:
            for chunk in request_iterator:
                total_bytes += len(chunk.content)
                chunk_count += 1

            end_time = time.time()
            elapsed = end_time - start_time

            print("[SERVER] Upload finished")
            print(f"[SERVER] Chunks received: {chunk_count}")
            print(f"[SERVER] Total size: {total_bytes / (1024 * 1024):.2f} MB")
            print(f"[SERVER] Duration: {elapsed:.2f} seconds")
            print(f"[SERVER] Avg speed: {total_bytes / (1024 * 1024) / elapsed:.2f} MB/s")

            return file_transfer_pb2.UploadStatus(success=True, message="Upload received (not saved).")

        except Exception as e:
            print(f"[SERVER] Error during upload: {e}")
            return file_transfer_pb2.UploadStatus(success=False, message="Server error during upload.")

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    file_transfer_pb2_grpc.add_FileTransferServicer_to_server(FileTransferServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("[SERVER] gRPC server listening on port 50051...")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
