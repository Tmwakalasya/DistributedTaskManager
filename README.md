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
