# Workflow Lab: Open Issues

### Backlog

1. **Docker image garbage collection**

   * Safely prune old/unused API and UI images on EC2.
   * Prevent another EBS disk-full incident.

2. **Stable EC2 public IP**

   * Allocate an **Elastic IP** so `EC2_HOST` doesn't need updating after every stop/start.

3. **Production health endpoint**

   * Add a lightweight `/health` endpoint.
   * Use it as a post-deployment smoke test in CD instead of relying only on `docker ps`.
   * We explicitly deferred this until after the acceptance test.

4. **Automated post-deployment verification**

   * After `docker compose up -d`, have CD verify something like:

     * API container is healthy
     * `/health` returns 200
     * `/metrics` returns 200
     * optionally `/workflow` succeeds
   * This would turn "deployment succeeded" into "deployment actually works."

5. **Deployment rollback**

   * We currently deploy an explicitly selected SHA, which is good.
   * But there is no automated/easy rollback mechanism if a newly deployed image is broken.
   * A future issue could define a simple rollback procedure using the previous image SHA.

6. **EC2 lifecycle / cost management**

   * We deliberately chose a manually controlled deployment because you don't want an idle EC2 generating unnecessary compute charges.
   * A future improvement could automate **stop/start** or otherwise make the development/portfolio environment easier to shut down when unused.

7. **SSH deployment hardening**

   * We currently use SSH from GitHub Actions with an EC2 private key.
   * It works, but longer-term we could replace this with a more production-grade mechanism such as AWS Systems Manager.
   * I would mark this **low priority** for this portfolio project; we explicitly decided it wasn't worth the complexity now.

8. **Production secrets rotation**

   * We now have the correct GitHub Secrets → Compose secrets → `/run/secrets` path.
   * We haven't established a rotation procedure.
   * Not urgent, but worth documenting once the project becomes more than a portfolio deployment.

### Priority order

If we want this to remain a *lightweight* backlog:

**P1**

* Docker image pruning
* Elastic IP
* `/health` endpoint
* Post-deployment smoke test

**P2**

* Rollback procedure
* EC2 lifecycle/cost automation

**P3**

* SSH → SSM migration
* Secret rotation procedure
