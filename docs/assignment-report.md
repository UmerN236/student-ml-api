# Advanced MLOps Exercise - Completion Report

**Student Name:** Muhammad Umer Naseer

**Roll Number:** 23i-0663

**MLOps Section:** A

**Application:** `student-ml-api`

**Repository:** <https://github.com/UmerN236/student-ml-api>

**Registry:** `ghcr.io/umern236/student-ml-api`

**Completed:** 6 September 2026

## 1. Project overview

For this assignment, I built a small Flask prediction API and set up the workflow around it as I would for a real team project. I developed the two application versions on separate feature branches, opened pull requests, ran automated checks, and merged only after CI passed. I then used Git tags to publish versioned Docker images to GitHub Container Registry (GHCR).

The table below gives a quick summary of the completed work and where the evidence can be found.

| Requirement | Implemented evidence |
|---|---|
| Application and at least four tests | `app.py`; eight passing tests in `tests/test_app.py` |
| Feature-branch development | `feature/prediction-api` and `feature/model-metadata` |
| Two professional PRs | [PR #1](https://github.com/UmerN236/student-ml-api/pull/1), [PR #2](https://github.com/UmerN236/student-ml-api/pull/2) |
| Failed and successful CI | [deliberate failure](https://github.com/UmerN236/student-ml-api/actions/runs/34041765056), [corrected success](https://github.com/UmerN236/student-ml-api/actions/runs/34041789935) |
| CI test and build-check only | `.github/workflows/ci.yml` |
| Tag-only release publishing | `.github/workflows/release.yml` |
| Successful releases | [v1.0.0 run](https://github.com/UmerN236/student-ml-api/actions/runs/34041836595), [v1.1.0 run](https://github.com/UmerN236/student-ml-api/actions/runs/34041965272) |
| Registry tags | `1.0.0`, `1.1.0`, `latest`, `6429225`, and `f6f1711` |
| Traceability | PR #2 -> merge `f6f1711...` -> tag `v1.1.0` -> image `1.1.0` -> digest `sha256:892843...` |
| Reproducibility and rollback | v1.0.0 deleted locally, pulled from GHCR, run, upgraded to v1.1.0, then rolled back without a rebuild |

## 2. Application and automated tests

The application has two endpoints. `GET /health` reports whether the service is running and shows the application and model versions. `POST /predict` accepts a number and returns twice that value. I also added validation so that missing values, text, null values, Boolean values, and non-finite numbers return HTTP 400 instead of causing an application error.

The current `/health` response is:

```json
{
  "application": "student-ml-api",
  "application_version": "1.1.0",
  "model_version": "model-1",
  "status": "healthy"
}
```

I wrote eight pytest cases covering:

1. health status and metadata;
2. integer prediction;
3. decimal prediction;
4. missing input;
5. invalid string input;
6. invalid null input;
7. invalid Boolean input; and
8. non-JSON input.

The final local test result was:

```text
........                                                                 [100%]
8 passed in 0.07s
```

Run locally with:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest -v
```

## 3. Git and pull-request workflow

### PR #1 - prediction API and v1.0.0

- URL: <https://github.com/UmerN236/student-ml-api/pull/1>
- Branch: `feature/prediction-api` -> `main`
- Meaningful commits include `feat: add prediction API and container image`, `test: add API tests and automation workflows`, and `fix: correct health endpoint test`.
- Merge commit: `6429225e39af874c0fc10c0d02593ce92e384271`
- Result: merged only after the required CI check passed.

### PR #2 - model metadata and v1.1.0

- URL: <https://github.com/UmerN236/student-ml-api/pull/2>
- Branch: `feature/model-metadata` -> `main`
- Commits: `feat: add model metadata to health endpoint` and `test: update health checks for model metadata`.
- Merge commit: `f6f1711c8a080c2ff18053f3cf9d98c7e5e8c2c5`
- Result: merged only after eight tests and the Docker build-check passed.

Both pull requests contain a clear summary, list of changes, testing details, Docker impact, and a completed checklist. I also added a review note before each merge.

### Merge strategy

I used **Squash and merge** for both feature pull requests. This keeps the history on `main` short and easy to read, while the full list of development commits is still available inside each pull request. The pull request number is included in the merge commit, so it is easy to move from the main history back to the original review.

## 4. Branch protection

The GitHub branch-protection rule for `main` has these settings:

- pull requests are required before merging;
- the `Test and Docker build` status check is required and must be current with `main` (`strict: true`);
- stale reviews are dismissed;
- conversations must be resolved;
- administrators are included, preventing an owner from bypassing the rule;
- force pushes and branch deletion are disabled.

This repository currently has one owner, so the required approval count is zero because GitHub does not allow an author to approve their own pull request. I recorded the review checks as comments on both pull requests. In a team repository, I would require at least one approval and use a CODEOWNERS file where appropriate.

## 5. CI workflow

The `ci.yml` workflow runs for pull requests targeting `main` and for pushes to feature branches. It checks out the code, installs Python 3.12 and the project dependencies, runs pytest, and builds the Docker image as a validation step. The workflow has read-only repository permissions and does not log in to GHCR or publish an image.

I kept CI and release publishing separate because a pull request is still work under review. Publishing an image for every PR would fill the registry with temporary images and could publish code that has not been approved. In this project, publishing happens only after the code is merged and a semantic version tag is pushed.

### Mandatory deliberate failure

1. Commit `3d2bc26` intentionally changed the expected health status from `healthy` to `wrong`.
2. [CI run 34041765056](https://github.com/UmerN236/student-ml-api/actions/runs/34041765056) failed in `Run unit tests`; Docker validation was correctly skipped.
3. Commit `31213d3` used the required message `fix: correct health endpoint test` and restored the assertion.
4. [CI run 34041789935](https://github.com/UmerN236/student-ml-api/actions/runs/34041789935) then passed pytest and Docker build validation.

PR #2 independently passed [CI run 34041923608](https://github.com/UmerN236/student-ml-api/actions/runs/34041923608).

## 6. Docker implementation and inspection

The Dockerfile uses the fixed base image `python:3.12.11-slim` instead of `latest`. The working directory is `/app`, dependencies are pinned, and pip uses `--no-cache-dir`. The requirements file is copied before the application code so that Docker can reuse the dependency layer when only the source code changes. Gunicorn listens on `0.0.0.0:5000`, and the application runs as the non-root user with UID 10001.

The `.dockerignore` file removes Git data, workflow files, Python cache files, virtual environments, environment files, temporary files, and documentation from the Docker build context.

Local inspection of the running v1.0.0 rollback container produced:

```text
CONTAINER=51b46608f0bd
IMAGE=ghcr.io/umern236/student-ml-api:1.0.0
IMAGE_ID=2d4522c756d4
PORTS=0.0.0.0:5051->5000/tcp
COMMAND="gunicorn --bind 0.0.0.0:5000 --workers 2 --access-logfile - app:app"
WORKDIR=/app
USER=10001
EXPOSED={"5000/tcp":{}}
```

Port 5051 was used on this Mac because host port 5000 is occupied by macOS AirPlay (`Server: AirTunes`). The container still exposes and listens on the assignment-required port 5000. On a host where port 5000 is free, use `-p 5000:5000` exactly as specified.

Equivalent inspection commands are:

```bash
docker images
docker ps
docker logs student-ml-api
docker inspect student-ml-api
docker exec -it student-ml-api sh
```

Inside the container, `pwd` returned `/app`, UID was `10001`, and files were `VERSION`, `app.py`, and `requirements.txt`.

## 7. Automated semantic releases and registry verification

The `release.yml` workflow runs only when a tag matching `v*.*.*` is pushed. It removes the leading `v`, checks that the remaining value follows semantic versioning, and compares it with the `VERSION` file. The release number is therefore derived automatically rather than being hard-coded in the workflow.

Before publishing, the workflow runs the tests again. It then signs in to GHCR using GitHub's temporary `GITHUB_TOKEN` and publishes the semantic version tag, `latest`, and a seven-character commit tag. No registry password is stored in the YAML file or Git history.

| Source | Image tags | Registry index digest |
|---|---|---|
| PR #1 merge `6429225...`, Git tag `v1.0.0` | `1.0.0`, `6429225` | `sha256:2d4522c756d483b242fdf3bfe3b0ca111f2dab2a5612d09771c072985af10c21` |
| PR #2 merge `f6f1711...`, Git tag `v1.1.0` | `1.1.0`, `f6f1711`, `latest` | `sha256:892843cbd96ca07a9274cb3d6c983c5d854f9d3a0b25f7bc2336f85488771a56` |

The matching digest confirms that `latest` and `1.1.0` currently refer to the same image. Version `1.0.0` still has its own digest and can be downloaded separately. The commit-based tag provides a direct link to the exact source revision, which is useful when investigating a deployment problem.

## 8. OCI image metadata

The Dockerfile and release workflow apply standard OCI labels. Inspection of the pulled 1.0.0 image showed:

```text
org.opencontainers.image.version=1.0.0
org.opencontainers.image.revision=6429225e39af874c0fc10c0d02593ce92e384271
org.opencontainers.image.source=https://github.com/UmerN236/student-ml-api
org.opencontainers.image.created=2026-09-06T20:17:17+05:00
```

These labels make it possible to identify the application version, exact Git commit, source repository, and build time directly from the image.

## 9. Artifact reproducibility and rollback

### Pull without rebuilding

The local v1.0.0 image was removed and restored from GHCR:

```bash
docker rmi student-ml-api:1.0.0
docker pull --platform linux/amd64 ghcr.io/umern236/student-ml-api:1.0.0
docker run -d --platform linux/amd64 --name student-ml-api \
  -p 5050:5000 ghcr.io/umern236/student-ml-api:1.0.0
```

The registry returned digest `sha256:2d4522...`. I did not rebuild the image. After starting the downloaded image, the health endpoint returned:

```json
{"application":"student-ml-api","status":"healthy","version":"1.0.0"}
```

GitHub's runner produced a linux/amd64 image, while my demonstration machine uses arm64. The first start therefore produced an `exec format error`. After enabling standard amd64 emulation with binfmt, the same downloaded image ran successfully without being rebuilt.

### Upgrade and rollback

The pulled v1.1.0 artifact returned:

```json
{"application":"student-ml-api","application_version":"1.1.0","model_version":"model-1","status":"healthy"}
```

To test rollback, I stopped version 1.1.0 and started the already downloaded 1.0.0 image. The original health response returned immediately. I did not change the source code, reinstall dependencies, or rebuild the image.

This approach is more reliable than running `git clone`, `pip install`, and `python app.py` during an incident. The container image already contains the tested code, Python runtime, dependencies, command, and filesystem. Recreating the service from source could install different dependencies or use a different runtime environment.

## 10. Complete v1.1.0 traceability chain

```text
Pull Request:       #2
PR URL:             https://github.com/UmerN236/student-ml-api/pull/2
Merge Commit:       f6f1711c8a080c2ff18053f3cf9d98c7e5e8c2c5
Git Tag:            v1.1.0
Docker Image:       ghcr.io/umern236/student-ml-api:1.1.0
Commit Image Tag:   ghcr.io/umern236/student-ml-api:f6f1711
Image Digest:       sha256:892843cbd96ca07a9274cb3d6c983c5d854f9d3a0b25f7bc2336f85488771a56
Release Run:        https://github.com/UmerN236/student-ml-api/actions/runs/34041965272
```

Both `1.1.0`, `f6f1711`, and `latest` resolved to this digest at verification time.

## 11. Docker layer-cache experiment

I ran three builds with the same build arguments so that only the file changes affected the cache:

1. Baseline built the current source.
2. After changing only `app.py`, `WORKDIR`, `COPY requirements.txt`, and `RUN pip install` were `CACHED`; only the application COPY and following user/ownership layer reran.
3. After restoring `app.py` and changing `requirements.txt`, `COPY requirements.txt` changed and `RUN pip install` downloaded and reinstalled the dependency set; all following layers reran.

Therefore this order is preferable:

```dockerfile
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py VERSION ./
```

Application files normally change more often than dependency files. By copying `requirements.txt` first, Docker can reuse the slower dependency-installation layer for normal source-code changes. If `COPY . .` came first, almost any file change would cause pip to run again.

## 12. Failure analysis

### Failure A - failed pytest (mandatory CI demonstration)

- **Symptom:** CI run 34041765056 failed; Docker validation did not run.
- **Root cause:** commit `3d2bc26` deliberately expected `status == "wrong"` while the API correctly returned `healthy`.
- **Evidence:** the failed run is linked in Section 5 and remains visible in PR #1 history.
- **Correction:** commit `31213d3` restored `healthy`; run 34041789935 passed.

### Failure B - wrong container port

- **Symptom:** `curl http://127.0.0.1:5051/health` returned an empty reply.
- **Root cause:** the deliberately faulty command used `-p 5051:5001`, but Gunicorn listens on container port 5000.
- **Evidence:** `docker port student-ml-api` showed `5001/tcp -> 0.0.0.0:5051`, while logs showed `Listening at: http://0.0.0.0:5000`.
- **Correction:** recreate with `-p 5051:5000`; `/health` returned HTTP 200 and the v1.0.0 payload.

### Additional environment diagnosis - missing dependency

- **Symptom:** the first clean-host pytest collection raised `ModuleNotFoundError: No module named 'flask'`.
- **Root cause:** pinned project dependencies had not yet been installed on the host.
- **Correction:** create `.venv`, run `pip install -r requirements.txt`, then run pytest; all eight tests passed.

## 13. Demonstration script

```bash
git clone https://github.com/UmerN236/student-ml-api.git
cd student-ml-api
git log --graph --decorate --oneline --all
gh pr view 1 --web
gh pr view 2 --web
gh run list

docker pull ghcr.io/umern236/student-ml-api:1.1.0
docker run -d --name student-ml-api -p 5000:5000 \
  ghcr.io/umern236/student-ml-api:1.1.0
curl http://localhost:5000/health

docker rm -f student-ml-api
docker pull ghcr.io/umern236/student-ml-api:1.0.0
docker run -d --name student-ml-api -p 5000:5000 \
  ghcr.io/umern236/student-ml-api:1.0.0
curl http://localhost:5000/health
```

Use an unused host port such as `5050:5000` if port 5000 is already reserved. On an arm64 host, include `--platform linux/amd64` and enable emulation because these release artifacts were built by GitHub's amd64 runner.

## 14. Viva answers

1. **Why avoid direct pushes to main?** They bypass peer review, automated gates, discussion, and a clear audit trail; one mistake can immediately destabilize the release branch.
2. **What is a PR for beyond merging?** It is the unit of review and collaboration: intent, diff, tests, CI results, risk, approvals, and discussion are recorded together.
3. **Why run CI before merge?** Defects are cheaper to fix before integration, and a required check prevents a known-bad revision entering the protected branch.
4. **Image versus container?** An image is an immutable runtime template; a container is a running or stopped instance with process and writable state.
5. **Why version images?** Version tags make deployments repeatable, comparable, auditable, and reversible.
6. **Why is `latest` insufficient?** It is mutable and does not identify which release or commit is running.
7. **Why promote the same artifact?** Rebuilding can change dependencies, base layers, timestamps, or tools. Promoting one digest preserves what was tested.
8. **Purpose of a registry?** It stores, secures, versions, and distributes container artifacts between build and runtime environments.
9. **CI versus release?** CI validates mutable candidate changes without publishing; release validates tagged approved source and publishes named artifacts.
10. **Why secrets for credentials?** Secrets prevent source/history exposure, allow rotation and access control, and can be scoped. This project uses the ephemeral GitHub token.
11. **How identify the producing commit?** Inspect the OCI revision label or commit-SHA image tag and verify it against the release tag/run.
12. **Why does layer ordering matter?** A changed layer invalidates every layer after it. Stable dependency steps before frequently changed source maximize cache reuse.
13. **How roll back 1.1.0?** Stop 1.1.0 and run the immutable registry artifact tagged 1.0.0 or, more strictly, its digest; do not rebuild.
14. **Git tag versus image tag?** The Git tag identifies the approved source commit; automation derives the corresponding image tag from it. The digest identifies the produced bytes.
15. **Independent app/model versions in MLOps?** Compatibility, feature schema, preprocessing, data lineage, monitoring baselines, staged rollout, and rollback must track both dimensions. One can change or regress without the other.

## 15. Conclusion

This assignment showed how the different parts of an MLOps workflow fit together. Git records changes to the source code, pull requests control how those changes reach `main`, and CI checks the application before merge. Docker packages the approved code into a repeatable artifact, while GHCR stores versioned images that can be traced to a commit and used again for deployment or rollback.
