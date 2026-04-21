# Girl Math Product Status

## Current Status
- Project is active.
- Core local implementation work is ahead of remote and not yet live-verified.
- Main external blocker: repo/deploy access for publish.

## Implemented Locally
- VIP pass creation
- Existing pass open/load flow
- Email-based pass recovery
- Request/event history backed by `pass_events`
- Worker/admin search and load tools
- Additive SQLite migration for legacy DBs
- Automated tests for core flows and Streamlit smoke render

## Verified Locally
- Create pass flow works
- Recover by email works
- Admin load works
- Event history writes correctly
- Automated test suite passes locally

## Known External Blockers
- Push/deploy access is not working from the current session
- Live deployment remains unverified until publish access is restored

## Source of Truth Rules Going Forward
- Every requested feature should be added here when accepted
- Each item should be marked as one of: Requested, In Progress, Implemented Locally, Live, Blocked
- Any deploy blocker should be logged here immediately

## Feature Ledger
### Implemented Locally
- Request history / event log
- Email recovery
- Worker/admin tools
- Automated tests for DB migration, create/recover/search/history, admin load, and Streamlit smoke render

### Blocked
- Push latest commits upstream
- Verify live deployment after publish

### Missing Reconstruction
- The full prior locked feature-request list has not yet been fully reconstructed into this document
- Next step: recover the remaining requested items from chat/repo context and add them here explicitly
