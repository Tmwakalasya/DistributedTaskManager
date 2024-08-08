import unittest
from concurrent import futures
import grpc
from distributed_task_manager.protos import task_manager_pb2 as pb2
from distributed_task_manager.protos import task_manager_pb2_grpc as pb2_grpc
from distributed_task_manager.server.server import TaskManagerServicer
import time

class TaskManagerServicerTest(unittest.TestCase):
    # This sets up the server:
    def setUp(self):
        self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        self.port = '[::] 50051'
        self.server.add_insecure_port(self.port)
        self.server.start()
        time.sleep(1)
        # Set up the client:
        self.channel = grpc.insecure_channel('localhost: 50051')
        self.stub = pb2.grpc.TaskManagerStub(self.channel)

    def tearDown(self):
        self.channel.close()
        self.server.stop(None)

    def create_task(self, title, description):
        try:
            return self.stub.CreateTask(pb2.CreateTaskRequest(title=title, description=description))
        except grpc.RpcError as e:
            self.fail(f"CreateTask failed: {e}")

    def create_task_test(self):
        response = self.create_task("Test", "Test")
        self.assertEqual(response.title, "Test", "Unexpected title")
        self.assertEqual(response.description, "Test", "Unexpected description")
        self.assertEqual(response.status, pb2.TaskStatus.PENDING, "Unexpected status")

    def get_task_test(self):
        create_response = self.create_task("Test", "Test")
        response = self.stub.GetTask(pb2.GetTaskRequest(id=create_response.id))
        self.assertEqual(response.title, "Test", "Unexpected title")
        self.assertEqual(response.description, "Test", "Unexpected description")
        self.assertEqual(response.status, pb2.TaskStatus.PENDING, "Unexpected status")

    def update_task_test(self):
        create_response = self.create_task("Test", "Test")
        try:
            update_response = self.stub.UpdateTaskStatus(pb2.UpdateTaskStatusRequest(id=create_response.id, status=pb2.TaskStatus.COMPLETED))
            self.assertEqual(update_response.status, pb2.TaskStatus.COMPLETED, "Unexpected status")
        except grpc.RpcError as e:
            self.fail(f"UpdateTaskStatus failed: {e}")

    def watch_task_test(self):
        create_response = self.create_task("Test", "Test")
        try:
            watch_responses = self.stub.WatchTask(pb2.WatchTaskRequest(id=create_response.id))
            for response in watch_responses:
                self.assertEqual(response.id, create_response.id, "Unexpected task ID")
                self.assertEqual(response.title, "Test", "Unexpected title")
                self.assertEqual(response.description, "Test", "Unexpected description")
                break
        except grpc.RpcError as e:
            self.fail(f"WatchTask failed: {e}")

    @unittest.skip("Skipping this test for parallel execution")
    def test_update_non_existent_task(self):
        try:
            self.stub.UpdateTaskStatus(pb2.UpdateTaskStatusRequest(id=999, status=pb2.TaskStatus.COMPLETED))
            self.fail("UpdateTaskStatus should have failed for non-existent task")
        except grpc.RpcError as e:
            self.assertEqual(e.code(), grpc.StatusCode.NOT_FOUND, "Unexpected error code")

if __name__ == '__main__':
    unittest.main()