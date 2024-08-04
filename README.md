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
