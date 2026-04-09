# Implementation Plan - Conditional Bottom Navigation

The user requested to hide the bottom navigation icons on the landing page and only show them after a user has logged in.

## User Review Required

> [!NOTE]
> I will implement this by checking for a valid user session in the base template. The bottom navigation bar will only render if `request.session.id` is present.

## Proposed Changes

### Template & Layout Enhancements

#### [MODIFY] [base.html](file:///c:/Users/arthi/OneDrive/Desktop/PROJECT/TexttoImageGeneration/assets/templates/base.html)
- **Conditional Nav**: Wrap the `.mobile-bottom-nav` container in a Django template `{% if %}` block that checks for `request.session.id`.
- **Dynamic Footer Spacing**: Update the footer styles so the extra `70px` bottom margin (which creates space for the nav icons) is only applied when the user is logged in. This prevents an empty gap at the bottom of the landing and login pages.

## Verification Plan

### Manual Verification
- **Scenario 1**: Open the landing page (`index/`) as an unauthenticated user and verify the bottom nav is hidden and there is no extra white space at the bottom.
- **Scenario 2**: Log in as a user and verify the bottom nav appears and the layout is correctly padded.
- **Scenario 3**: Visit the Login/Register pages and verify the bottom nav remains hidden.
