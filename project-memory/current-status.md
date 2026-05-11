# Girl Math Current Status

## Verified Done
- Shared pass creation works.
- Open existing pass by code works.
- Email recovery works.
- Request history / event logging exists.
- Worker/admin tools are split onto a separate page.
- Main customer page links to the admin page.
- VIP request and approval workflow works.
- VIP request button regression was fixed and tested.
- Monthly VIP pricing now shows the standard $8 price and the Friday $5 discount logic.
- Spa Treatments and Weekly Comics are now separate saved sections in the UI and data model.
- Comics Corner was removed from spa treatment choices.
- Consumable spa services are tracked as paid add-ons.
- Worker/admin view now shows included VIP items separately from paid add-ons.
- Name tag extras now render as graphic icons instead of text labels.

## Most Recent Verified Signals
- Barney confirmed that the VIP request and approval workflow seems to work.
- Latest local fix commit for the VIP request button: `160352a` (`Fix VIP request button state update`).
- Local test suite now verifies DB migration, create / recover / search / history, VIP approval flow, pricing summary logic, admin load, and Streamlit smoke coverage at 7/7 passing.

## Suspected / Open UI Issue
- Barney reported that snack and treatment menu options were not showing in one session view.
- Local reproduction did not show those controls missing after create, request, or approval.
- Most likely explanation is a stale page/session render issue, but this is not fully closed until it is either reproduced or cleared in production.

## Open Work
- Rebuild comic rendering around Alexandra's original layouts, while preserving words and positioning.
- Build a fuller project roadmap from Barney's remaining feature summary.
- Reconfirm in a fresh production session whether the earlier snack / treatment visibility report is fully gone.

## Next Recommended Steps
1. Reconfirm whether the snack / treatment visibility issue persists after refresh or reopen.
2. Replace the placeholder comic strip with Alexandra-faithful layout rendering.
3. Build the remaining roadmap from Barney's feature summary and stage the next product pass.
