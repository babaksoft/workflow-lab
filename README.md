
![Python Version from PEP 621 TOML](https://img.shields.io/python/required-version-toml?tomlFilePath=https://github.com/babaksoft/workflow-lab/raw/refs/heads/master/pyproject.toml)
![Static Badge](https://img.shields.io/badge/framework-LlamaIndex-orange)
![Static Badge](https://img.shields.io/badge/category-GenAI-orange)
![GitHub License](https://img.shields.io/github/license/babaksoft/workflow-lab)
![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/babaksoft/workflow-lab/build.yml)

# Workflow Lab

An experimental platform for building, evaluating, and observing **LLM-powered workflows** with a production-oriented architecture.

The project focuses on **Agentic Workflows / LLM orchestration**, while deliberately keeping infrastructure modular, lightweight, and provider-agnostic.

## Main Objective

**Workflow Lab is a hands-on laboratory for designing, evaluating, observing, and deploying LLM-powered workflows with a production-oriented Python architecture.**

## Current Stack

* **Python 3.12+**
* **LlamaIndex Workflows**
* **FastAPI** — API layer
* **Streamlit** — lightweight UI
* **OpenAI, Amazon Bedrock, Ollama** — LLM providers
* **OpenInference + Arize Phoenix** — LLM observability
* **Prometheus** — application metrics
* **Grafana** — metrics visualization
* **Docker / Docker Compose** — containerization
* **Docker Hub** — container registry
* **GitHub Actions** — CI/CD
* **pytest / mypy / Ruff / Black / isort** — quality and testing
* **Alembic / SQLAlchemy** — persistence foundation

## Architecture

```text
                         ┌──────────────────┐
                         │    Streamlit     │
                         │       UI         │
                         └────────┬─────────┘
                                  │ HTTP
                                  ▼
                         ┌──────────────────┐
                         │     FastAPI      │
                         │       API        │
                         └────────┬─────────┘
                                  │
                         ┌────────▼─────────┐
                         │    Workflows     │
                         │                  │
                         │ GeneratorJudge   │
                         │ MathFlow         │
                         └────────┬─────────┘
                                  │
                         ┌────────▼─────────┐
                         │  LLM Providers   │
                         │                  │
                         │ OpenAI           │
                         │ Bedrock          │
                         │ Ollama           │
                         └──────────────────┘

        ┌─────────────────┐       ┌─────────────────┐
        │    Prometheus   │──────▶│     Grafana     │
        └────────┬────────┘       └─────────────────┘
                 │
                 │ metrics
                 ▼
             FastAPI

        ┌─────────────────────────────────────────┐
        │              Arize Phoenix              │
        │     OpenTelemetry / OpenInference       │
        └────────────────────▲────────────────────┘
                             │
                         LLM traces
```

## Implemented Features

### Workflow Engine

The project uses **LlamaIndex Workflows** as the orchestration layer.

A deterministic `MathFlow` was initially implemented as the minimal baseline. The first LLM-based workflow is now `GeneratorJudgeFlow`, which:

1. Uses an LLM to generate an answer under strict constraints.
2. Passes the generated answer to a second LLM call.
3. Uses the second call as a judge.
4. Produces structured rubric scores and justifications.

Workflow data flow follows LlamaIndex Workflows' `Event` model, and workflows are validated before execution.

### LLM Provider Abstraction

A provider abstraction was introduced to keep workflow code independent of individual LLM integrations.

Currently supported:

* OpenAI
* Amazon Bedrock
* Ollama

Provider adapters expose a common generation interface and are selected through a provider factory.

This allows the same workflow to run against different LLM backends without changing workflow code.

### API

FastAPI exposes the workflow execution API under:

```text
/api/v1
```

The API includes:

* Workflow execution endpoint
* Prometheus metrics endpoint
* HTTP-level metrics middleware
* Workflow-level metrics
* Application logging
* Health/operational infrastructure

LLM execution is deliberately kept behind the workflow/provider boundary rather than embedded in the API layer.

### Streamlit UI

The Streamlit application acts as a deliberately thin client.

It communicates with the FastAPI service over HTTP rather than directly invoking workflows or LLM providers.

This keeps the UI independently replaceable and prevents application-specific dependencies from leaking into the API architecture.

### Observability

Two complementary observability layers are implemented.

**Application metrics**

Prometheus collects metrics such as:

* HTTP request counts
* HTTP request latency
* HTTP errors
* workflow execution counts
* workflow errors

Grafana provides dashboards for visualizing these metrics.

**LLM observability**

Arize Phoenix is integrated through:

* OpenTelemetry
* OpenInference
* LlamaIndex instrumentation

Phoenix successfully captures workflow and LLM traces including information such as:

* prompts
* model/provider
* completion output
* prompt/completion/total token counts
* latency
* model invocation parameters
* provider-specific metadata
* cost information where available

The integration has been verified against:

* OpenAI
* Ollama
* Amazon Bedrock

The experiment demonstrated that Phoenix provides substantially richer visibility into LLM execution than application-level metrics alone.

### Containerization

The complete application stack runs through Docker Compose.

Current services include:

* API
* Streamlit app
* Prometheus
* Grafana
* Phoenix

The API and UI use optimized multi-stage Docker builds with:

* cache-friendly dependency layers
* `constraints.txt`
* non-root runtime users
* `.dockerignore`
* BuildKit layer caching
* separated UI dependencies

Persistent Docker volumes are configured for:

* Prometheus
* Grafana
* Phoenix

Sensitive LLM credentials are supplied through Docker secrets rather than committed configuration.

### CI

GitHub Actions continuously validates the project using the project's quality and test suite.

The CI pipeline includes static analysis, formatting/linting and automated tests.

### Continuous Delivery

A GitHub Actions CD workflow has now been implemented.

After successful CI on `master`, the workflow:

1. Checks out the exact successful commit.
2. Builds the API Docker image.
3. Builds the Streamlit Docker image.
4. Uses BuildKit/GitHub Actions caching.
5. Publishes both images to Docker Hub.
6. Creates immutable commit-specific SHA tags.
7. Also updates the `latest` tags.

Published artifacts:

```text
workflow-lab-api:<sha>
workflow-lab-api:latest

workflow-lab-app:<sha>
workflow-lab-app:latest
```

The published API image has been independently smoke-tested by pulling/running the Docker Hub artifact and successfully executing a real LLM-backed workflow.

## Current Deployment Pipeline

```text
Developer
    │
    ▼
  master
    │
    ▼
GitHub Actions CI
    │
    │ success
    ▼
GitHub Actions CD
    │
    ├── Build API
    ├── Build UI
    ├── BuildKit cache
    └── Push images
          │
          ▼
      Docker Hub
```

## Testing Strategy

The project currently uses multiple testing levels:

* Unit tests for individual components
* Workflow tests
* API contract tests
* Provider smoke tests
* Docker/Compose verification
* Manual UI verification
* Observability verification
* Prometheus/Grafana verification
* Published-container smoke testing

A particularly important architectural decision is that API tests can substitute the production workflow with a deterministic `MathFlow`, avoiding real LLM calls and external API dependencies in the normal test suite.

## Current Milestone Status

**Infrastructure milestone: COMPLETE ✅**

The project currently has:

* ✅ LlamaIndex Workflow orchestration
* ✅ Multi-provider LLM abstraction
* ✅ FastAPI API
* ✅ Streamlit UI
* ✅ Prometheus metrics
* ✅ Grafana dashboards
* ✅ Phoenix LLM observability
* ✅ Docker Compose environment
* ✅ Persistent monitoring/observability storage
* ✅ Docker secrets
* ✅ CI
* ✅ Docker Hub publishing
* ✅ Continuous Delivery Phase 1

### Next Direction

The infrastructure foundation is now sufficiently mature to shift the project's focus toward **real LLM workflows, evaluation, and experimentation**.

Potential next areas include:

* richer agentic workflows
* structured workflow outputs
* workflow evaluation
* experiment/run tracking
* token/cost analysis
* retrieval-augmented workflows
* more sophisticated observability
* remote deployment
