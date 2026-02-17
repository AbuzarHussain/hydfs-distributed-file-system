# HyDFS: Hybrid Distributed File System

## Description

HyDFS is a hybrid between HDFS (Hadoop Distributed File System) and Cassandra, built for CS 428 (Distributed Systems) at UIUC. The project implements a fault-tolerant, scalable distributed file storage system (HyDFS) and robust membership protocols (Gossip and Ping/Ack) to maintain node communication and data consistency across a cluster of nodes.

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/AbuzarHussain/hydfs-distributed-file-system.git
   cd hydfs-distributed-file-system
   ```
2. **Build the project:**
   - Ensure you have Java 11+ and Maven installed.
   - Run:
     ```bash
     mvn clean package
     ```
3. **Prepare directories:**
   - Create required directories for file storage:
     ```bash
     mkdir -p hdfs inputs output
     ```

## Usage

1. **Start a node:**
   - Run the main class for your node, specifying configuration as needed.
   - Example:
     ```bash
     java -jar target/hydfs-distributed-file-system.jar --nodeId=<NODE_ID> --config=config.yaml
     ```
   - In case that doesnt work (replace XX with the current IP and introducer node IP respectively):
     ```bash
     mvn exec:java -Dexec.mainClass="com.uiuc.systems.Main" -Dexec.args="fa25-cs425-76XX.cs.illinois.edu fa25-cs425-76XX.cs.illinois.edu gossip nosuspect"
     ```


2. **File operations:**
   - Use the CLI or provided scripts to create, append, and retrieve files in the distributed system.
   - Example commands:
     - Create a file:
       ```bash
       java -jar target/hydfs-distributed-file-system.jar create <local_file> <hdfs_file>
       ```
     - Append to a file:
       ```bash
       java -jar target/hydfs-distributed-file-system.jar append <local_file> <hdfs_file>
       ```
     - Retrieve a file:
       ```bash
       java -jar target/hydfs-distributed-file-system.jar get <hdfs_file> <local_file>
       ```

## Example Workflow

1. **Start multiple nodes** on different machines or ports.
2. **Create a file** in the distributed system:
   ```bash
   java -jar target/hydfs-distributed-file-system.jar create inputs/example.txt distributed_example.txt
   ```
3. **Append data** to the file:
   ```bash
   java -jar target/hydfs-distributed-file-system.jar append inputs/append.txt distributed_example.txt
   ```
4. **Retrieve the file** from HyDFS:
   ```bash
   java -jar target/hydfs-distributed-file-system.jar get distributed_example.txt output/local_copy.txt
   ```
5. **Observe logs** to see membership protocol messages and replica synchronization.

## Testing

1. **Unit tests:** Run with Maven:
   ```bash
   mvn test
   ```
2. **Integration tests:** Simulate node failures, file operations, and membership changes by running multiple instances and observing system behavior.
3. **Manual testing:** Use the CLI to create, append, and get files, and verify data consistency across nodes.

## Roadmap

- [x] Implement HyDFS file operations (create, append, get, merge)
- [x] Gossip-based membership protocol
- [x] Ping/Ack membership protocol with suspicion mechanism
- [x] Dynamic replica rebalancing and re-replication
- [x] Command-line management tools
- [x] Enhanced monitoring and logging

## Project Status

**Completed** 
