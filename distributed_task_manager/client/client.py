import grpc
from distributed_task_manager.protos import task_manager_pb2 as pb2
from distributed_task_manager.protos import task_manager_pb2_grpc as pb2_grpc


def run():
    with grpc.insecure_channel('localhost:50051') as channel:

        stub = pb2_grpc.TaskManagerStub(channel)

        response = stub.CreateTask(pb2.CreateTaskRequest(title="Test Task", description="This is a test task."))

        print(f"Task created: {response}")


if __name__ == '__main__':
    run()
