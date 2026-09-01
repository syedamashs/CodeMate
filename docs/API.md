# CodeMate API Documentation

## Overview

CodeMate provides a REST API for code analysis and evaluation.

## Endpoints

### Health Check

```
GET /api/health
```

**Response:**
```json
{
  "status": "ok",
  "model_provider": "demo"
}
```

### Analyze Code

```
POST /api/analyze
```

**Request:**
```json
{
  "code": "def hello():\n    print('Hello')",
  "language": "Python",
  "error_message": "Optional error context"
}
```

**Response:**
```json
{
  "result": "Analysis result",
  "latency": 0.234,
  "mode": "demo"
}
```

**Error Responses:**
- `400`: Missing or invalid code
- `413`: Code exceeds size limit
- `503`: Model provider error

### Evaluate Models

```
POST /api/evaluate
```

**Request:**
```json
{
  "dataset": "MBPP",
  "samples": 10
}
```

**Response:**
```json
{
  "dataset": "MBPP",
  "samples": 10,
  "accuracy": "N/A"
}
```

## Error Handling

All errors follow this format:
```json
{
  "error": "Error description",
  "mode": "demo"
}
```

## Authentication

Currently no authentication required. Add API key support for production use.
