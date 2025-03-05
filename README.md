# Graph-Based Version Control

The aim of this project is build a version control system that uses Neo4j to track not just file changes, but also relationships between entitites in a graph database. This approach will allow us to create a powerful system for tracking knowledge evolution overtime.

## Current Project Goals

- Graph-Based Version Control System
  - Implement a commit history as a graph in Neo4j
  - Track file relationsghips, dependencies, and evolution over time
  - Support branching and merging of different graph states
- Content-Adressable Storage (CAS)
  - Store files using SHA-based immutable hashing
  - Ensure efficient deduplication by referincing existing content
  - Maintain a lighteweight, object-based storage format
- Versioned Graph Mutations
  - Track node and relaitonship changes across different commits
  - Support rollback to previous graph states
  - Implement stagging areas for proposed graph modifications
- Conflict Resolution & Merging
  - Implement three-way merging for graph conflicts
  - Explore CRDTs or Merkle Trees for distributed graph changes
  - Proide automated and manual conflict resolution tools
- Workflow Management & Collaboration
  - Support multi-user contributions with approval tracking
  - Maintain Change attribution (who modified what and when)
  - Enable staged commits and versioning approvals before changes go live
