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

## Most Recent Verified Signals
- Barney confirmed that the VIP request and approval workflow seems to work.
- Latest local fix commit for the VIP request button: `160352a` (`Fix VIP request button state update`).
- Local test suite was expanded and last verified passing at 6/6.

## Suspected / Open UI Issue
- Barney reported that snack and treatment menu options were not showing in one session view.
- Local reproduction did not show those controls missing after create, request, or approval.
- Most likely explanation is a stale page/session render issue, but this is not fully closed until it is either reproduced or cleared in production.

## Open Work
- Implement the monthly pricing and Friday discount logic in the product.
- Separate Spa Treatments from Weekly Comics in both UI and product logic.
- Remove Comics Corner from spa treatment selections.
- Render actual graphic extras on the name tag instead of text labels.
- Rebuild comic rendering around Alexandra's original layouts, while preserving words and positioning.
- Improve worker/admin view to clearly separate included items from paid add-ons.
- Build a fuller project roadmap from Barney's remaining feature summary.

## Next Recommended Steps
1. Reconfirm whether the snack / treatment visibility issue persists after refresh or reopen.
2. Implement pricing and inclusion logic.
3. Split spa and comics sections cleanly.
4. Upgrade name-tag rendering and comic rendering against Alexandra's art.
