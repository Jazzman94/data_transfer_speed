import asyncio
import grpc
import stream_pb2
import stream_pb2_grpc

class AsyncStreamServicer(stream_pb2_grpc.StreamServiceServicer):
    async def ServerStream(self, request, context):
        for i in range(5):
            await asyncio.sleep(1)  # asynchronní čekání
            yield stream_pb2.Response(message=f"Async response {i} to {request.message}")
            
    async def ClientStream(self, request_iterator, context):
        messages = []
        async for request in request_iterator:
            messages.append(request.message)
        return stream_pb2.Response(message=f"Async received {len(messages)} messages")
        
    async def BidirectionalStream(self, request_iterator, context):
        async for request in request_iterator:
            await asyncio.sleep(0.5)
            yield stream_pb2.Response(message=f"Async echo: {request.message}")

# Spuštění asynchronního serveru
async def serve():
    server = grpc.aio.server()
    stream_pb2_grpc.add_StreamServiceServicer_to_server(AsyncStreamServicer(), server)
    server.add_insecure_port('[::]:50051')
    await server.start()
    await server.wait_for_termination()

if __name__ == '__main__':
    asyncio.run(serve())