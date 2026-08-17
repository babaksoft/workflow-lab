# Workflow Lab — Practical DockerHub + EC2 CD Playbook

This guide documents the final, working configuration used to publish Workflow Lab Docker images to DockerHub and manually deploy a selected image SHA to an AWS EC2 instance using GitHub Actions.

---

## 1. Create DockerHub repositories

### Task

Create separate DockerHub repositories for the API and Streamlit application images.

### Steps

Create:

```text
babaksoft/workflow-lab-api
babaksoft/workflow-lab-app
```

Create a DockerHub Personal Access Token (PAT) with permission to push images.

### GitHub configuration

Add:

* **Repository variable**

  * `DOCKERHUB_USERNAME` = `babaksoft`

* **Repository secret**

  * `DOCKERHUB_TOKEN` = DockerHub PAT

### Verification

From a local machine:

```powershell
docker login
```

Then verify that the DockerHub repositories are accessible from the account.

### Pitfalls

* Never commit the DockerHub PAT.
* Do not put credentials directly into workflow YAML.
* Keep API and UI images in separate repositories.

---

# 2. Prepare the EC2 server

### Task

Create a lightweight Ubuntu EC2 instance and prepare it as the deployment host.

### Required software

Install:

* Docker Engine
* Docker Compose plugin
* OpenSSH server/client
* Git, if required by the deployment setup

Verify:

```bash
docker --version
docker compose version
ssh -V
```

Add the deployment user to Docker's group:

```bash
sudo usermod -aG docker deploy
```

Log out and back in, then verify:

```bash
docker ps
```

### Deployment directory

Create:

```bash
sudo mkdir -p /opt/workflow-lab
sudo chown -R deploy:deploy /opt/workflow-lab
```

### Verification

```bash
ls -ld /opt/workflow-lab
docker ps
docker compose version
```

### Pitfalls

* The deployment user must be able to run Docker without `sudo`.
* Do not assume the EC2 public IP remains unchanged after stopping/starting the instance.
* Ensure the instance has enough EBS storage for Docker images and volumes.

---

# 3. Configure the EC2 security group

### Task

Allow the traffic required by the deployment and application.

For SSH deployment:

```text
TCP 22
Source: your permitted SSH source
```

For the application, expose only the ports intentionally required by the deployment/acceptance test.

The EC2 security group should be configured through the AWS console rather than through the application repository.

### Verification

From PowerShell:

```powershell
Test-NetConnection <EC2_HOST> -Port 22
```

From EC2:

```bash
docker ps
```

### Pitfalls

* Do not assume an application is externally reachable merely because its Docker port is published.
* Security-group rules and Docker port mappings are separate layers.
* Keep SSH access restricted where practical.

---

# 4. Prepare the production Compose configuration

### Task

Create a production-specific Compose file that pulls the published images rather than building them.

Use:

```text
docker-compose.prod.yml
```

The API and UI services reference the DockerHub repositories using `IMAGE_TAG`, for example:

```text
babaksoft/workflow-lab-api:${IMAGE_TAG}
babaksoft/workflow-lab-app:${IMAGE_TAG}
```

The production stack also contains:

* API
* Streamlit application
* Prometheus
* Grafana
* Phoenix

and the required persistent volumes/networks.

### Verification

On EC2:

```bash
docker compose -f docker-compose.prod.yml config
```

The command should complete without configuration errors.

### Pitfalls

* Production Compose should pull published images; it should not rebuild application images on EC2.
* Keep `IMAGE_TAG` externally configurable.
* Do not commit API credentials or other secrets to the Compose file.

---

# 5. Configure Docker Compose secrets

### Task

Pass cloud credentials securely to the API without committing them to Git.

The final configuration uses **environment-backed Compose secrets**.

Production Compose:

```yaml
secrets:
  openai_api_key:
    environment: OPENAI_API_KEY

  bedrock_api_key:
    environment: AWS_BEARER_TOKEN_BEDROCK
```

The API consumes them:

```yaml
api:
  secrets:
    - source: openai_api_key
      target: openai_api_key
      uid: "1000"
      gid: "1000"
      mode: 0400

    - source: bedrock_api_key
      target: bedrock_api_key
      uid: "1000"
      gid: "1000"
      mode: 0400
```

The application reads:

```text
/run/secrets/openai_api_key
/run/secrets/bedrock_api_key
```

and maps those values to the corresponding environment variables internally.

### Verification

After deployment:

```bash
docker exec workflow_api ls -l /run/secrets
```

The secret files should exist with restrictive permissions.

### Pitfalls

* Do not commit API keys.
* Do not put API keys directly in `docker-compose.prod.yml`.
* Do not use host secret files for this final configuration.

---

# 6. Configure GitHub Actions environments

### Task

Separate deployment-specific configuration from ordinary repository configuration.

Create a GitHub Environment:

```text
production
```

Add these **environment variables**:

```text
EC2_HOST
EC2_USER
```

For this project:

```text
EC2_USER=deploy
EC2_HOST=<current EC2 public DNS name>
```

Add these **environment secrets**:

```text
OPENAI_API_KEY
AWS_BEARER_TOKEN_BEDROCK
EC2_SSH_KEY_B64
```

`EC2_SSH_KEY_B64` contains the Base64 representation of the EC2 deployment private key.

### Create the Base64 SSH secret on Windows

From PowerShell:

```powershell
[Convert]::ToBase64String(
    [IO.File]::ReadAllBytes(".\workflow-lab-deploy.pem")
) | Set-Clipboard
```

Paste the resulting value into the GitHub secret:

```text
EC2_SSH_KEY_B64
```

### Verification

The GitHub Environment should contain:

```text
Variables:
  EC2_HOST
  EC2_USER

Secrets:
  OPENAI_API_KEY
  AWS_BEARER_TOKEN_BEDROCK
  EC2_SSH_KEY_B64
```

### Pitfalls

* `EC2_HOST` and `EC2_USER` are variables, not secrets.
* API credentials and the private SSH key are secrets.
* EC2's public DNS name can change after a stop/start unless an Elastic IP is used.

---

# 7. Configure CI image publishing

### Task

Extend the existing CI workflow so that a successful CI run publishes both Docker images.

The logical dependency is:

```text
quality ─┐
         ├──> publish
tests ───┘
```

The publish job must therefore wait for **both** quality and tests to succeed.

Images are tagged with the Git commit SHA, using the format:

```text
sha-<short-sha>
```

and also receive:

```text
latest
```

### Published images

```text
babaksoft/workflow-lab-api:sha-<short-sha>
babaksoft/workflow-lab-api:latest

babaksoft/workflow-lab-app:sha-<short-sha>
babaksoft/workflow-lab-app:latest
```

### Verification

After CI completes, check DockerHub and verify that both repositories contain the new SHA tag.

Locally:

```powershell
docker pull babaksoft/workflow-lab-api:sha-<short-sha>
docker pull babaksoft/workflow-lab-app:sha-<short-sha>
```

### Pitfalls

* Publish only after quality and tests pass.
* Prefer immutable SHA tags for deployment.
* Do not deploy `latest` when reproducibility matters.

---

# 8. Configure manual CD

### Task

Create a separate:

```text
.github/workflows/deploy.yml
```

The CD workflow is **manually triggered** with `workflow_dispatch`.

It accepts:

```text
image_tag
```

as a required input.

Example:

```text
sha-1b96eff
```

The final workflow does **not** automatically deploy after every CI run.

The overall pipeline is:

```text
CI
 ├── quality
 ├── tests
 └── publish → DockerHub

CD
 └── manual deployment → EC2
```

### Verification

In GitHub:

```text
Actions → CD → Run workflow
```

Enter the desired image SHA and start the workflow.

### Pitfalls

* Keep deployment manual for this portfolio environment.
* Never leave `IMAGE_TAG` empty.
* Deploy a specific SHA rather than relying on `latest`.

---

# 9. Authenticate the GitHub runner to EC2

### Task

Reconstruct the private SSH key safely on the GitHub runner.

The final workflow decodes the Base64 GitHub secret:

```bash
mkdir -p ~/.ssh

printf '%s' '${{ secrets.EC2_SSH_KEY_B64 }}' |
  base64 --decode > ~/.ssh/deploy.pem

chmod 600 ~/.ssh/deploy.pem
```

Validate it:

```bash
ssh-keygen -y -f ~/.ssh/deploy.pem > /dev/null
```

Register the EC2 host:

```bash
ssh-keyscan -H "$EC2_HOST" >> ~/.ssh/known_hosts
```

Connect:

```bash
ssh -i ~/.ssh/deploy.pem \
    "$EC2_USER@$EC2_HOST"
```

### Verification

The `ssh-keygen` command should complete successfully.

SSH should authenticate without requesting a password.

### Pitfalls

* Keep the PEM out of the repository.
* Base64 is encoding, not encryption; the GitHub Secret still provides the protection.
* Preserve the original private-key bytes when creating the Base64 secret.

---

# 10. Deploy the selected image

### Task

Have CD connect to EC2 and run Docker Compose with the selected SHA and cloud credentials.

The deployment supplies:

```text
IMAGE_TAG
OPENAI_API_KEY
AWS_BEARER_TOKEN_BEDROCK
```

to the Compose invocation.

The essential deployment operation is:

```bash
cd /opt/workflow-lab

IMAGE_TAG="$IMAGE_TAG" \
OPENAI_API_KEY="$OPENAI_API_KEY" \
AWS_BEARER_TOKEN_BEDROCK="$AWS_BEARER_TOKEN_BEDROCK" \
docker compose -f docker-compose.prod.yml pull

IMAGE_TAG="$IMAGE_TAG" \
OPENAI_API_KEY="$OPENAI_API_KEY" \
AWS_BEARER_TOKEN_BEDROCK="$AWS_BEARER_TOKEN_BEDROCK" \
docker compose -f docker-compose.prod.yml up -d
```

This causes Compose to:

1. Pull the selected API/UI images.
2. Create/update the containers.
3. Provide the credentials as Compose-managed secrets.
4. Start the production stack.

### Verification

On EC2:

```bash
docker ps
```

All expected containers should be running.

Check the API:

```bash
curl http://localhost:8000/api/v1/metrics
```

Check Compose configuration:

```bash
docker compose -f docker-compose.prod.yml config
```

### Pitfalls

* Pull before starting the new version.
* Deploy using the SHA supplied to the manual workflow.
* Do not put credentials into the image or Compose YAML.
* Don't confuse a successful container start with a successful application deployment.

---

# 11. Verify the complete deployment

### Task

Perform an end-to-end acceptance test after CD.

### API

From EC2:

```bash
curl http://localhost:8000/api/v1/metrics
```

From an HTTP client such as Insomnia, call the workflow endpoint.

### Streamlit

Open the deployed Streamlit application and execute the workflow.

Verify that the LLM response is displayed correctly.

### Prometheus

Open Prometheus and verify that the API target is:

```text
UP
```

### Grafana

Open Grafana and verify that the provisioned dashboard displays API/workflow metrics.

### Phoenix

Open Phoenix and verify that the deployed workflow produces:

* traces
* spans
* metrics
* prompts

### Container status

On EC2:

```bash
docker ps
```

### Logs

If something fails:

```bash
docker compose -f docker-compose.prod.yml logs api
docker compose -f docker-compose.prod.yml logs app
docker compose -f docker-compose.prod.yml logs phoenix
```

### Pitfalls

* Test the application, not just `docker ps`.
* Check API logs when the container repeatedly restarts.
* Verify observability independently from application response.
* Remember that EC2's public DNS name can change after stop/start.

---

# Final architecture

The completed experiment has this flow:

```text
Developer
   │
   ▼
Git push → master
   │
   ▼
GitHub Actions CI
   │
   ├── quality
   ├── tests
   │
   └── publish
          │
          ▼
      DockerHub
      ├── workflow-lab-api
      └── workflow-lab-app


Manual GitHub Actions CD
   │
   │ image_tag = sha-xxxxxxx
   │
   ├── GitHub Secrets
   │      ├── OPENAI_API_KEY
   │      ├── AWS_BEARER_TOKEN_BEDROCK
   │      └── EC2_SSH_KEY_B64
   │
   └── GitHub Environment variables
          ├── EC2_HOST
          └── EC2_USER
                 │
                 ▼
             SSH → EC2
                 │
                 ▼
       docker compose pull
                 │
                 ▼
       docker compose up -d
                 │
                 ▼
          Production stack
          ├── API
          ├── Streamlit
          ├── Prometheus
          ├── Grafana
          └── Phoenix
```

This is the final working configuration used for the first Workflow Lab production deployment.
