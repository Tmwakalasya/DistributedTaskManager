import grpc
from distributed_task_manager.protos import task_manager_pb2 as pb2
from distributed_task_manager.protos import task_manager_pb2_grpc as pb2_grpc


def create_task(stub):
    title = input("Enter task title: ")
    description = input("Enter task description: ")
    response = stub.CreateTask(pb2.CreateTaskRequest(title=title, description=description))
    print(f"Task created: {response}")


def get_task(stub):
    task_id = int(input("Enter task ID: "))
    response = stub.GetTask(pb2.GetTaskRequest(id=task_id))
    print(f"Task details: {response}")


def update_task(stub):
    task_id = int(input("Enter task ID: "))
    status = input("Enter new task status (PENDING, IN_PROGRESS, COMPLETED, CANCELED): ")
    status_enum = pb2.TaskStatus.Value(status)
    response = stub.UpdateTaskStatus(pb2.UpdateTaskStatusRequest(id=task_id, status=status_enum))
    print(f"Task updated: {response}")


def watch_task(stub):
    task_id = int(input("Enter task ID: "))
    print("Watching task updates (press Ctrl+C to stop)...")
    try:
        for update in stub.WatchTask(pb2.WatchTaskRequest(id=task_id)):
            print(f"Task update: {update}")
    except grpc.RpcError as e:
        print(f"WatchTask cancelled: {e}")


def main():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = pb2_grpc.TaskManagerStub(channel)
        while True:
            print("\nOptions:")
            print("1. Create Task")
            print("2. Get Task")
            print("3. Update Task")
            print("4. Watch Task")
            print("5. Exit")
            choice = input("Enter choice: ")
            if choice == '1':
                create_task(stub)
            elif choice == '2':
                get_task(stub)
            elif choice == '3':
                update_task(stub)
            elif choice == '4':
                watch_task(stub)
            elif choice == '5':
                print("Exiting...")
                break
            else:
                print("Invalid choice. Please try again.")


if __name__ == '__main__':
    main()
