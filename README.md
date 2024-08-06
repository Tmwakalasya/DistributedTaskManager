TaskManager

TaskManager is a distributed task management system that uses gRPC for communication. It allows users to create, update, retrieve, and watch tasks. This project demonstrates the implementation of a gRPC server with in-memory storage for tasks and a client to interact with the server.

Project Description

TaskManager provides the following functionalities:

	•	CreateTask: Create a new task with a title and description.
	•	GetTask: Retrieve the details of an existing task using its ID.
	•	UpdateTask: Update the status of an existing task.
	•	WatchTask: Stream updates for a specific task.

Features

	•	gRPC Communication: Uses gRPC for efficient and robust client-server communication.
	•	In-Memory Storage: Tasks are stored in memory for simplicity.
	•	Error Handling: Comprehensive error handling for all RPC methods.
	•	Logging: Logs significant events and errors for traceability.

Setup

Prerequisites

	•	Python 3.7 or higher
	•	gRPC and gRPC tools for Python
Installing Dependencies

	1.	Clone the repository:
 		git clone https://github.com/Tmwakalasya/DistributedTaskManager.git
		cd DistributedTaskManager
	2.	Create and activate a virtual environment (optional but recommended):
 		python -m venv venv
		source venv/bin/activate  # On Windows use `venv\Scripts\activate`
  	3.	Install the required dependencies:
   		pip install grpcio grpcio-tools
Compiling Protobuf Files

Make sure the .proto files are compiled into Python code. If they are not already compiled, you can do so with:
	python -m grpc_tools.protoc -I=. --python_out=. --grpc_python_out=. distributed_task_manager/protos/task_manager.proto

Usage

Running the Server

Start the gRPC server:
	python server.py
You should see a log message indicating that the server has started:
	INFO:Server started on port 50051
 Running the Client

You can create a simple client to interact with the server. Below is an example client script:
	import grpc
	from distributed_task_manager.protos import task_manager_pb2 as pb2
	from distributed_task_manager.protos import task_manager_pb2_grpc as pb2_grpc

	def run():
    	# Create a channel to the server
    	with grpc.insecure_channel('localhost:50051') as channel:
        # Create a stub (client)
        stub = pb2_grpc.TaskManagerStub(channel)
        
        # Create a new task
        response = stub.CreateTask(pb2.CreateTaskRequest(title="Test Task", description="This is a test task."))
        print(f"Task created: {response}")

        # Retrieve the task
        task = stub.GetTask(pb2.GetTaskRequest(id=response.id))
        print(f"Retrieved Task: {task}")

        # Update the task status
        updated_task = stub.UpdateTask(pb2.UpdateTaskRequest(id=task.id, status=pb2.TaskStatus.COMPLETED))
        print(f"Updated Task: {updated_task}")

        # Watch the task (This will keep running, you may want to run it separately)
        # for update in stub.WatchTask(pb2.WatchTaskRequest(id=task.id)):
        #     print(f"Task update: {update}")

	if __name__ == '__main__':
    		run()
Methods

CreateTask

Create a new task with a title and description.

	•	Request: CreateTaskRequest
	•	title: The title of the task.
	•	description: The description of the task.
	•	Response: CreateTaskResponse
	•	id: The unique ID of the created task.
	•	title: The title of the task.
	•	description: The description of the task.
	•	status: The status of the task.
	•	created_at: The creation timestamp.
	•	updated_at: The update timestamp.

GetTask

Retrieve the details of an existing task using its ID.

	•	Request: GetTaskRequest
	•	id: The unique ID of the task.
	•	Response: GetTaskResponse
	•	id: The unique ID of the task.
	•	title: The title of the task.
	•	description: The description of the task.
	•	status: The status of the task.
	•	created_at: The creation timestamp.
	•	updated_at: The update timestamp.

UpdateTask

Update the status of an existing task.

	•	Request: UpdateTaskRequest
	•	id: The unique ID of the task.
	•	status: The new status of the task.
	•	Response: UpdateTaskResponse
	•	id: The unique ID of the task.
	•	status: The updated status of the task.
	•	updated_at: The update timestamp.

WatchTask

Stream updates for a specific task.

	•	Request: WatchTaskRequest
	•	id: The unique ID of the task.
	•	Response: WatchTaskResponse (streaming)
	•	id: The unique ID of the task.
	•	status: The status of the task.
	•	created_at: The creation timestamp.
	•	updated_at: The update timestamp.

Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

	1.	Fork the repository.
	2.	Create your feature branch (git checkout -b feature/AmazingFeature).
	3.	Commit your changes (git commit -m 'Add some AmazingFeature').
	4.	Push to the branch (git push origin feature/AmazingFeature).
	5.	Open a Pull Request.

