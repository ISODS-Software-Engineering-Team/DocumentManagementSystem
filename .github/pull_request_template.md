# What does this PR solve and how
## What is this PR about?
- clarify context and AC

## How to run it step by step
Step 1: Run application

Step 2: api request (using curl format)
```curl
curl --location 'http://127.0.0.1:8000/api/documents' \
--header 'Content-Type: application/json' \
--data '{
    "docs_id": "dvsd",
    "category_id": "sdfsd",
    "brief": "sdf",
    "content": "sdf",
    "media_file": "bcv",
    "author": "cvbc"
}'
```

# Implementation 

Add any implementation details
- design patterns used
- any new libs added
- algorithmic overview
- how is the error handling implemented
- observability of the code (monitoring/logging)

# Testing
- is it manual or automated
- how to test it manually
- any relevant screenshot

# Risk
- 

# Dependencies
- 

# PR Checklist
- [ ] Documentation
- [ ] Unit testing passed
- [ ] Code review and discussion
- [ ] Approve
- [ ] Merge
