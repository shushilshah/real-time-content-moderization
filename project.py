import os

BASE_DIR = "real_time_moderation"

# Folder structure
structure = {
    "apps/api/routes": ["moderation.py", "health.py", "metrics.py"],
    "apps/api/schemas": ["request.py", "response.py"],
    "apps/api/dependencies": ["auth.py"],
    "apps/api/middleware": ["logging.py", "rate_limit.py"],
    "apps/api": ["main.py"],

    "apps/worker": ["consumer.py", "producer.py", "tasks.py"],

    "apps/dashboard/components": ["charts.py", "tables.py"],
    "apps/dashboard": ["app.py", "utils.py"],

    "core": ["config.py", "logger.py", "security.py", "constants.py"],

    "models/inference": ["predictor.py", "preprocess.py", "postprocess.py"],
    "models/training": ["train.py", "evaluate.py", "dataset.py"],
    "models/artifacts/tokenizer": [],
    "models/artifacts": ["model.pt", "config.json"],

    "services": ["moderation_service.py", "decision_engine.py", "feedback_service.py"],

    "streaming": ["kafka_config.py", "topics.py", "schemas.py"],

    "database/crud": ["moderation_log.py", "user.py"],
    "database/migrations": [],
    "database": ["db.py", "models.py"],

    "cache": ["redis_client.py", "rate_limiter.py"],

    "utils": ["text_cleaner.py", "validators.py", "helpers.py"],

    "tests": ["test_api.py", "test_model.py", "test_pipeline.py", "conftest.py"],

    "scripts": ["start_kafka.sh", "load_test.py", "seed_data.py"],

    "configs": ["app.yaml", "kafka.yaml", "model.yaml", "logging.yaml"],

    "infra/docker": ["Dockerfile.api", "Dockerfile.worker", "Dockerfile.dashboard"],
    "infra/kubernetes": [
        "api-deployment.yaml",
        "worker-deployment.yaml",
        "kafka.yaml",
        "redis.yaml",
    ],
    "infra": ["docker-compose.yml"],
}

# Root-level files
root_files = [
    ".env",
    ".env.example",
    "requirements.txt",
    "pyproject.toml",
    "README.md",
    "Makefile",
    ".gitignore",
]


def create_file(path):
    """Create file with minimal starter content"""
    if not os.path.exists(path):
        with open(path, "w") as f:
            if path.endswith(".py"):
                f.write("# Auto-generated file\n")
            elif path.endswith(".md"):
                f.write("# Real-Time Content Moderation\n")
            elif path.endswith(".txt"):
                f.write("")
            elif path.endswith(".yaml") or path.endswith(".yml"):
                f.write("# configuration\n")
            elif path.endswith(".sh"):
                f.write("#!/bin/bash\n")
            else:
                f.write("")


def create_structure():
    for folder, files in structure.items():
        folder_path = os.path.join(BASE_DIR, folder)
        os.makedirs(folder_path, exist_ok=True)

        for file in files:
            file_path = os.path.join(folder_path, file)
            create_file(file_path)

    # Create root files
    for file in root_files:
        file_path = os.path.join(BASE_DIR, file)
        create_file(file_path)


def main():
    os.makedirs(BASE_DIR, exist_ok=True)
    create_structure()
    print(f"✅ Project structure created at: {BASE_DIR}")


if __name__ == "__main__":
    main()