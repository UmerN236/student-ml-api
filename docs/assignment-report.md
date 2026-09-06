# Advanced MLOps Exercise - Completion Report

**Application:** `student-ml-api`  
**Repository:** <https://github.com/UmerN236/student-ml-api>  
**Registry:** `ghcr.io/umern236/student-ml-api`  
**Completed:** 6 September 2026

## 1. Outcome and requirement map

The repository implements a Flask prediction API, eight automated tests, pull-request CI, a production-oriented Docker image, protected-branch development, semantic Git releases, automated GHCR publication, artifact recovery, rollback, OCI metadata, commit tags, cache analysis, and failure diagnosis.

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

## 2. Application and tests

The `/predict` endpoint doubles a finite numeric input. It rejects missing JSON/fields, strings, nulls, booleans, and non-finite numbers with HTTP 400. The current `/health` response is:

```json
{
  "application": "student-ml-api",
  "application_version": "1.1.0",
  "model_version": "model-1",
  "status": "healthy"
}
```

The eight pytest cases cover:

1. health status and metadata;
2. integer prediction;
3. decimal prediction;
4. missing input;
5. invalid string input;
6. invalid null input;
7. invalid Boolean input; and
8. non-JSON input.

Final local result:

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

Both PR descriptions include Summary, Changes, Testing Performed, Docker Impact, and a completed readiness checklist. A review record was added to each PR.

### Merge strategy

Both feature PRs used **Squash and merge**. This keeps `main` release-focused and easy to revert while each PR retains the detailed feature/test/failure history and discussion. The PR number is included in each squash commit subject, preserving navigation from `main` back to the review record.

## 4. Branch protection

The GitHub branch-protection rule for `main` has these settings:

- pull requests are required before merging;
- the `Test and Docker build` status check is required and must be current with `main` (`strict: true`);
- stale reviews are dismissed;
- conversations must be resolved;
- administrators are included, preventing an owner from bypassing the rule;
- force pushes and branch deletion are disabled.

The repository has one owner account, so the approving-review count is zero; GitHub does not permit a PR author to approve their own PR. Review records on both PRs document the manual review performed. In a team repository this should be raised to at least one approval, ideally with CODEOWNERS.

## 5. CI workflow

`ci.yml` runs on pull requests targeting `main` and on feature-branch pushes. Its single required job performs checkout, Python 3.12 setup, pinned dependency installation, pytest, and a Docker build. It has read-only repository permissions, uses concurrency cancellation, and never authenticates to or pushes into a registry.

The CI/release split is a security and lifecycle boundary. A PR is untrusted, mutable candidate source. Publishing every PR would create noisy, unreviewed images, consume registry storage, risk tag races, and unnecessarily expose write credentials. Releases are produced only from approved source identified by an immutable semantic tag.

### Mandatory deliberate failure

1. Commit `3d2bc26` intentionally changed the expected health status from `healthy` to `wrong`.
2. [CI run 34041765056](https://github.com/UmerN236/student-ml-api/actions/runs/34041765056) failed in `Run unit tests`; Docker validation was correctly skipped.
3. Commit `31213d3` used the required message `fix: correct health endpoint test` and restored the assertion.
4. [CI run 34041789935](https://github.com/UmerN236/student-ml-api/actions/runs/34041789935) then passed pytest and Docker build validation.

PR #2 independently passed [CI run 34041923608](https://github.com/UmerN236/student-ml-api/actions/runs/34041923608).

## 6. Docker implementation and inspection

The Dockerfile uses the explicit base `python:3.12.11-slim`, `/app` as `WORKDIR`, pinned dependencies, `pip --no-cache-dir`, cache-aware COPY ordering, port 5000, Gunicorn bound to `0.0.0.0`, and a non-root UID 10001. `.dockerignore` excludes Git metadata, workflows, bytecode, caches, virtual environments, secrets, temporary evidence, documentation, and Markdown files.

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

`release.yml` runs only for tags matching `v*.*.*`. It removes the leading `v` at runtime, validates semantic-version syntax, and fails if the derived value differs from `VERSION`. Nothing in the workflow hard-codes `1.0.0` or `1.1.0`.

The workflow tests before publishing, authenticates to GHCR with the ephemeral `GITHUB_TOKEN`, and publishes semantic, `latest`, and seven-character commit-SHA tags. No registry password exists in YAML or repository history.

| Source | Image tags | Registry index digest |
|---|---|---|
| PR #1 merge `6429225...`, Git tag `v1.0.0` | `1.0.0`, `6429225` | `sha256:2d4522c756d483b242fdf3bfe3b0ca111f2dab2a5612d09771c072985af10c21` |
| PR #2 merge `f6f1711...`, Git tag `v1.1.0` | `1.1.0`, `f6f1711`, `latest` | `sha256:892843cbd96ca07a9274cb3d6c983c5d854f9d3a0b25f7bc2336f85488771a56` |

The matching digest proves `latest` currently points to the same artifact as `1.1.0`. Version `1.0.0` remains independently retrievable. A commit tag is useful during incident response because it maps a running artifact directly to one source snapshot even when semantic or floating tags are unavailable or move.

## 8. OCI image metadata

The Dockerfile and release workflow apply standard OCI labels. Inspection of the pulled 1.0.0 image showed:

```text
org.opencontainers.image.version=1.0.0
org.opencontainers.image.revision=6429225e39af874c0fc10c0d02593ce92e384271
org.opencontainers.image.source=https://github.com/UmerN236/student-ml-api
org.opencontainers.image.created=2026-09-06T20:17:17+05:00
```

This metadata connects the binary artifact to its version, exact Git commit, repository, and build time.

## 9. Artifact reproducibility and rollback

### Pull without rebuilding

The local v1.0.0 image was removed and restored from GHCR:

```bash
docker rmi student-ml-api:1.0.0
docker pull --platform linux/amd64 ghcr.io/umern236/student-ml-api:1.0.0
docker run -d --platform linux/amd64 --name student-ml-api \
  -p 5050:5000 ghcr.io/umern236/student-ml-api:1.0.0
```

The registry returned digest `sha256:2d4522...`; no `docker build` occurred. The downloaded image returned:

```json
{"application":"student-ml-api","status":"healthy","version":"1.0.0"}
```

The GitHub runner produced a linux/amd64 image. On the arm64 demonstration machine, the first start correctly diagnosed `exec format error`; installing the standard binfmt amd64 emulator allowed the exact same pulled bytes to run, still without rebuilding.

### Upgrade and rollback

The pulled v1.1.0 artifact returned:

```json
{"application":"student-ml-api","application_version":"1.1.0","model_version":"model-1","status":"healthy"}
```

Rollback removed that container and started the already-pulled immutable `1.0.0` registry tag. Its old health contract immediately returned again. No source change, clone, dependency resolution, or image build occurred.

This is safer than `git clone; pip install; python app.py` because the image freezes the application, interpreter, dependencies, runtime command, filesystem, and metadata as one verified artifact. A source-based rollback can resolve newer dependencies, use a different interpreter or OS, omit configuration, and take longer during an incident.

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

Three builds used identical build arguments to isolate file changes:

1. Baseline built the current source.
2. After changing only `app.py`, `WORKDIR`, `COPY requirements.txt`, and `RUN pip install` were `CACHED`; only the application COPY and following user/ownership layer reran.
3. After restoring `app.py` and changing `requirements.txt`, `COPY requirements.txt` changed and `RUN pip install` downloaded and reinstalled the dependency set; all following layers reran.

Therefore this order is preferable:

```dockerfile
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py VERSION ./
```

Application files change much more often than dependencies. Separating the stable dependency manifest preserves the expensive installation layer for ordinary code edits. `COPY . .` before installation invalidates that layer for nearly every source or documentation edit.

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

## 15. Core principle

Git records how source evolves. Pull requests govern entry to the protected branch. CI verifies candidate changes. Docker packages approved code and runtime dependencies as an artifact. GHCR stores immutable, versioned artifacts that can be traced, deployed consistently, and rolled back without rebuilding.
