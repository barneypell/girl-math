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
- Separate worker/admin page linked from the main customer page
- Worker/admin search, load, and VIP approve/reject tools
- VIP approval workflow with pending and rejected states
- Fixed the customer-side VIP request button regression caused by widget state updates after render
- Additive SQLite migration for legacy DBs
- Monthly VIP pricing with Friday discount logic
- Separate saved Spa Treatments and Weekly Comics selections
- Consumable spa add-ons tracked separately from included spa treatments
- Worker/admin summary that separates included VIP items from paid add-ons
- Graphic icon rendering for name-tag extras
- Automated tests for core flows and Streamlit smoke render

## Verified Locally
- Create pass flow works
- Recover by email works
- Admin page renders separately from the customer page
- Admin load works
- VIP requests stay pending until approved by admin
- VIP request button click path works without throwing a Streamlit error page
- Event history writes correctly
- Pricing summary logic works for Friday and non-Friday cases
- Automated test suite passes locally at 7/7

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
- Separate admin tools page and main-page link
- VIP approval and rejection workflow
- Monthly VIP pricing with Friday discount logic
- Separate Spa Treatments and Weekly Comics sections
- Paid consumable spa add-on tracking
- Worker summary for included items vs paid add-ons
- Graphic name-tag extras
- Automated tests for DB migration, create/recover/search/history, VIP approval flow, pricing summary logic, admin load, and Streamlit smoke render

### Blocked
- Push latest commits upstream
- Verify live deployment after publish

### Missing Reconstruction
- Comic rendering still needs to be rebuilt around Alexandra's original layouts
- The remaining roadmap from Barney's full feature summary still needs to be staged explicitly
