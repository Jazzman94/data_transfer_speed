import grpc
from concurrent import futures
import time
import stream_pb2
import stream_pb2_grpc

class StreamServicer(stream_pb2_grpc.StreamServiceServicer):
    def ServerStream(self, request, context):
        # Server streaming implementace
        for i in range(5):
            yield stream_pb2.Response(message=f"Response {i} to {request.message}")
            time.sleep(1)
            
    def ClientStream(self, request_iterator, context):
        # Client streaming implementace
        messages = []
        for request in request_iterator:
            messages.append(request.message)
        return stream_pb2.Response(message=f"Received {len(messages)} messages: {', '.join(messages)}")
        
    def BidirectionalStream(self, request_iterator, context):
        # Bidirectional streaming implementace
        for request in request_iterator:
            yield stream_pb2.Response(message=f"Echo: {request.message}")

# Spuštění serveru
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    stream_pb2_grpc.add_StreamServiceServicer_to_server(StreamServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()