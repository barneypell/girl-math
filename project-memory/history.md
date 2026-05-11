# Girl Math Project History

## Repo / Delivery History
- Initial work established the shared-pass model and live app.
- Later work added pass recovery, request history, and worker/admin tooling.
- Product status tracking was added in the repo.
- Automated tests were added for DB migration, create / recover / search / history, admin load, and Streamlit smoke coverage.
- Admin tools were later moved off the main page and onto a separate admin view.
- VIP was changed from automatic unlock to explicit admin approval.
- A customer-side VIP request regression was found from a live error screenshot, reproduced locally, fixed, tested, and pushed live.
- The next product pass migrated the app from the old combined spa/comics placeholder menu to separate saved Spa Treatments and Weekly Comics sections, added Friday pricing logic, tracked consumable spa add-ons separately, upgraded the worker summary, and switched name-tag extras from text labels to graphic icons.

## Commit Milestones Called Out During This Workstream
- `ca4fff4` — add pass recovery, history, and admin tools.
- `e4dd448` — add automated tests for Girl Math flows.
- `6672f67` — add Girl Math product status tracker.
- `4cc72ae` — split admin page and add VIP approval flow.
- `160352a` — fix VIP request button state update.

## Verification History
- Local tests were repeatedly run during implementation.
- Live app verification confirmed separate customer and admin page structure.
- Barney later confirmed the VIP request and approval workflow seems to work.
- The pricing / section split pass was verified locally with the automated suite at 7/7 passing.

## Project Direction Shift
- The project moved from simple pass management toward a richer product with membership pricing logic, included-vs-paid service logic, stronger worker/admin clarity, and art-faithful rendering.
