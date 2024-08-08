import unittest
from concurrent import futures
import grpc
import time
from distributed_task_manager.protos import task_manager_pb2 as pb2
from distributed_task_manager.protos import task_manager_pb2_grpc as pb2_grpc
from distributed_task_manager.server.server import TaskManagerServicer


class TaskManagerTest(unittest.TestCase):

    def setUp(self):
        # Set up gRPC server
        self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        pb2_grpc.add_TaskManagerServicer_to_server(TaskManagerServicer(), self.server)
        self.port = '[::]:50051'
        self.server.add_insecure_port(self.port)
        self.server.start()
        time.sleep(1)  # Give the server time to start

        # Set up gRPC client
        self.channel = grpc.insecure_channel('localhost:50051')
        self.stub = pb2_grpc.TaskManagerStub(self.channel)

    def tearDown(self):
        self.channel.close()
        self.server.stop(None)
