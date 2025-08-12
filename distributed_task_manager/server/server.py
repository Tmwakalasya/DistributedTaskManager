import grpc
from concurrent import futures
import time
import logging
import threading
from distributed_task_manager.protos import task_manager_pb2 as pb2
from distributed_task_manager.protos import task_manager_pb2_grpc as pb2_grpc

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')
logger = logging.getLogger(__name__)


class TaskManagerServicer(pb2_grpc.TaskManagerServicer):
    def __init__(self):
        self.tasks = {}
        self.next_id = 1
        self.lock = threading.Lock()

    def CreateTask(self, request, context):
        try:
            with self.lock:
                task_id = self.next_id
                self.next_id += 1
                timestamp = str(time.time())
                task = pb2.Task(
                    id=task_id,
                    title=request.title,
                    description=request.description,
                    status=pb2.TaskStatus.PENDING,
                    created_at=timestamp,
                    updated_at=timestamp,
                )
                self.tasks[task_id] = task

            logger.info(f"Creating Task with ID: {task_id}")
            logger.info(f"Request Title: {request.title}, Description: {request.description}")
            logger.info(f"Task Created: {task}")

            return pb2.CreateTaskResponse(
                id=task.id,
                title=task.title,
                description=task.description,
                status=task.status,
                created_at=task.created_at,
                updated_at=task.updated_at,
            )
        except Exception as e:
            logger.error(f"Exception occurred: {e}")
            context.abort(grpc.StatusCode.INTERNAL, "Failed to create task")

    def GetTask(self, request, context):
        try:
            with self.lock:
                task = self.tasks.get(request.id)
            if task is None:
                logger.error(f"Task with ID: {request.id} not found")
                context.abort(grpc.StatusCode.NOT_FOUND, "Task not found")
            return pb2.GetTaskResponse(
                id=task.id,
                title=task.title,
                description=task.description,
                status=task.status,
                created_at=task.created_at,
                updated_at=task.updated_at,
            )
        except Exception as e:
            logger.error(f"Exception occurred: {e}")
            context.abort(grpc.StatusCode.INTERNAL, "Failed to get task")

    def UpdateTaskStatus(self, request, context):
        try:
            with self.lock:
                task = self.tasks.get(request.id)
                if task is None:
                    logger.error(f"Task with ID: {request.id} not found")
                    context.abort(grpc.StatusCode.NOT_FOUND, "Task not found")
                task.status = request.status
                task.updated_at = str(time.time())
                updated_task = pb2.UpdateTaskStatusResponse(
                    id=task.id,
                    status=task.status,
                    updated_at=task.updated_at,
                )

            logger.info(f"Task Updated: {task}")

            return updated_task
        except Exception as e:
            logger.error(f"Exception occurred: {e}")
            context.abort(grpc.StatusCode.INTERNAL, "Failed to update task")

    def WatchTask(self, request, context):
        try:
            while True:
                with self.lock:
                    task = self.tasks.get(request.id)
                    if task is None:
                        logger.error(f"Task with ID: {request.id} not found")
                        context.abort(grpc.StatusCode.NOT_FOUND, "Task not found")
                    response = pb2.WatchTaskResponse(
                        id=task.id,
                        status=task.status,
                        created_at=task.created_at,
                        updated_at=task.updated_at,
                    )
                yield response
                time.sleep(5)  # Simulate periodic updates
        except grpc.RpcError as e:
            # Handle client disconnection
            logger.error(f"Client disconnected: {e}")
        except Exception as e:
            logger.error(f"Exception occurred: {e}")
            context.abort(grpc.StatusCode.INTERNAL, "Failed to watch task")


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pb2_grpc.add_TaskManagerServicer_to_server(TaskManagerServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    logger.info("Server started on port 50051")
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
