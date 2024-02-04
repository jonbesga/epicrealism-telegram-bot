#!/bin/bash

IMAGE_NAME=$(awk -F= '/^name/{print $2}' pyproject.toml | tr -d '" ')
IMAGE_VERSION=$(awk -F= '/^version/{print $2}' pyproject.toml | tr -d '" ')
FULL_IMAGE_NAME=localhost:5000/${IMAGE_NAME}:${IMAGE_VERSION}
SHELL=/bin/bash

echo "Exporting new requirements.txt"
poetry export -f requirements.txt -o requirements.txt --without-hashes

echo "Building image ${IMAGE_NAME}:${IMAGE_VERSION}"
docker build . -t "${FULL_IMAGE_NAME}"

docker push "${FULL_IMAGE_NAME}"
