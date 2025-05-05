import asyncio
import grpc
import stream_pb2
import stream_pb2_grpc

async def run_client():
    async with grpc.aio.insecure_channel('localhost:50051') as channel:
        stub = stream_pb2_grpc.StreamServiceStub(channel)
        
        # Server streaming
        print("Server streaming:")
        request = stream_pb2.Request(message="Hello server")
        async for response in stub.ServerStream(request):
            print(f"Received: {response.message}")
            
        # Client streaming
        print("\nClient streaming:")
        async def request_generator():
            for i in range(3):
                yield stream_pb2.Request(message=f"Message {i}")
                await asyncio.sleep(0.5)
                
        response = await stub.ClientStream(request_generator())
        print(f"Received: {response.message}")
        
        # Bidirectional streaming
        print("\nBidirectional streaming:")
        async def bidirectional_gen():
            for i in range(4):
                yield stream_pb2.Request(message=f"Bidirectional message {i}")
                await asyncio.sleep(1)
                
        responses = stub.BidirectionalStream(bidirectional_gen())
        async for response in responses:
            print(f"Received: {response.message}")

if __name__ == '__main__':
    asyncio.run(run_client())