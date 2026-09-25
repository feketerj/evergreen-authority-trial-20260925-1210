# Frozen platform-mechanics protocol

## Scope and authority

This trial uses a disposable **public** GitHub repository containing only synthetic text. The account `feketerj` owns both repository configuration and the proposed PR. No second authenticated reviewer is available. Therefore a passing check or ruleset is only platform-mechanics evidence; it cannot clear `SCIENTIFIC_REVIEW_PENDING`, prove independent method use, or authorize process/production promotion.

## Before execution

Record this protocol's commit, the base workflow/script commit, repository ID, active ruleset JSON, PR number and every exact head SHA. Keep the base verifier fixed during the challenge. The `pull_request_target` workflow runs the base verifier and posts `trial/exact-head` to the actual PR head SHA. The verifier fetches `source.txt` and `witness.json` from that head, binds the witness to its first parent and the source digest, and requires `PASS`. GitHub Actions is the status source, but the owner can administer this repository and workflow.

## Falsifiers and observations

1. Initial PR has a `FAIL` witness: exact-head status fails; merge must remain blocked.
2. Replace witness with `PASS`, correct parent and source digest: status passes on new head. One required distinct approval should still block merge.
3. A further changed head leaves the prior green status stale; its own status must fail or be absent. Merge remains blocked.
4. Attempt self-approval and direct push to protected `main`; both must be rejected. Do not merge.
5. Read back active ruleset, check context/source, PR merge state, commit statuses and API errors. Any missing rule or inconclusive API result is an unrun/failed card, not success.

## Open gate

The positive case requiring a separate authorized reviewer principal and a scientifically valid exact-head witness is UNRUN. A GitHub approval alone also does not attest that a reviewer read the pinned method, actual Codex task/tool trace, source digests and claim-level reasoning. A separately controlled witness/check route and a distinct authenticated principal remain necessary.
