[![Testing with Pytest](https://github.com/yoona-ai/yoona-v1/actions/workflows/test.yaml/badge.svg)](https://github.com/yoona-ai/yoona-v1/actions/workflows/test.yaml)

[![Deployment status](https://github.com/yoona-ai/yoona-v1/actions/workflows/deployment.yaml/badge.svg)](https://github.com/yoona-ai/yoona-v1/actions/workflows/deployment.yaml)

# Yoona.ai V1 API

## Introduction

This is a SAAS (Software as a Service) API from Yoona.ai V1.
It is a RESTful API that uses JSON for serialization and HTTP for data exchange.
It is designed to be simple and easy to use.
API enables creating a separate workspace for each organization.
Organizations can invite as many users as they want to their workspace.
Users can create as many projects as they want in their workspace.
The core of the API is the ability to create fashion alternatives for a given image.
Given an image, the API will return a list of fashion alternatives for the image.
To aggregate the data, client can create a dataset and add images to it.
Dataset can be considered as a collection of images.
Which in the long term will be used to train the model to create better fashion alternatives.
