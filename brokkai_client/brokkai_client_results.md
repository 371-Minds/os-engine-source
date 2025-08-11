--- Analysis for Agent 1: Simple Function ---
{
  "semantic_analysis": {
    "language": "python",
    "libraries": [],
    "functions": [
      {
        "name": "hello_world",
        "signature": "def hello_world(...)",
        "dependencies": []
      }
    ],
    "classes": []
  },
  "confidence_score": 0.95
}
\n
--- Analysis for Agent 2: Class with a Method ---
{
  "semantic_analysis": {
    "language": "python",
    "libraries": [],
    "functions": [
      {
        "name": "greet",
        "signature": "def greet(...)",
        "dependencies": []
      }
    ],
    "classes": [
      {
        "name": "Greeter",
        "methods": []
      }
    ]
  },
  "confidence_score": 0.95
}
\n
--- Analysis for Agent 3: Script with Imports ---
{
  "semantic_analysis": {
    "language": "python",
    "libraries": [
      "os",
      "sys"
    ],
    "functions": [
      {
        "name": "list_directory",
        "signature": "def list_directory(...)",
        "dependencies": []
      }
    ],
    "classes": []
  },
  "confidence_score": 0.95
}
\n
--- Analysis for Agent 4: Complex Class ---
{
  "semantic_analysis": {
    "language": "python",
    "libraries": [
      "logging"
    ],
    "functions": [
      {
        "name": "__init__",
        "signature": "def __init__(...)",
        "dependencies": []
      },
      {
        "name": "process",
        "signature": "def process(...)",
        "dependencies": []
      }
    ],
    "classes": [
      {
        "name": "DataProcessor",
        "methods": []
      }
    ]
  },
  "confidence_score": 0.95
}
\n
