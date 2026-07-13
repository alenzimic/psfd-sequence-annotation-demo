# PSFD Sequence Annotation Demo

This repository contains the front-end user interface for the Plant Stress Mechanism Map (PSMM) system. It connects to the locally running PSMM FastAPI server to allow users to search, annotate, and explore plant stress biological entities and their relationships.

## Features

- **Live Sequence Matching**: Connects to the PSMM backend (`http://localhost:8999`) to perform protein sequence searches.
- **Support for Multiple Search Engines**: Includes built-in support for searching via **ESM-C (Embed2Graph)** and **MMseqs2 (Seq2Graph)**.
- **Dynamic Relationship Extraction**: Extracts comprehensive knowledge graph relationships from the PSMM database for any given protein hit or user query.
- **Adjustable Parameters**: Users can set parameters like minimum similarity threshold for ESM-C and E-value for MMseqs2 directly from the UI.
- **Sequence Hit Stacking**: Stacks redundant hits from the same plant, presenting them cleanly in a horizontally scrollable carousel.
- **Rich Visualization**: Displays evidence-supported relations and hypotheses with context (tissues, species, pathways).

## Setup & Usage

To use this front-end interface, you must first have the PSMM backend server running.

1. Ensure the PSMM backend server is active (typically running on `http://localhost:8999`).
2. Serve this directory using any standard HTTP server. For example:
   ```bash
   # Using Python's built-in HTTP server
   python3 -m http.server 3001
   ```
3. Open your browser and navigate to the local address (e.g., `http://localhost:3001`).

## Configuration

This demo is currently configured to point to a local backend API at `http://localhost:8999`.

If you need to change the API URL, update the fetch requests in `assets/app.js`.

## Note on Legacy Code
Previous static data building scripts have been removed as this application now dynamically relies on the live PSMM API server rather than statically built JSON bundles.
