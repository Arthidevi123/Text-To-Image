# Implementation Plan - Fix Registration Form Visibility

The user reported that the registration form is not looking good and fields are not fully visible on mobile. The current 2-column layout and large internal padding are causing fields to become cramped and cut off on narrow screens.

## User Review Required

> [!IMPORTANT]
> I will be switching the registration form to a **single-column layout** for tablet and mobile devices (below 992px). This ensures that every field has the full width of the container, making them easier to read and fill out.

## Proposed Changes

### UI Enhancements

#### [MODIFY] [UserRegister.html](file:///c:/Users/arthi/OneDrive/Desktop/PROJECT/TexttoImageGeneration/assets/templates/UserRegister.html)
- **Breakpoints**: Change the grid breakpoint from `768px` to `992px`.
- **Card Padding**: Reduce mobile padding to `20px 15px` to maximize usable space.
- **Input Spacing**: Adjust the internal padding of input fields for better readability on small screens.
- **Button Sizing**: Ensure the "Create Free Account" button is perfectly centered and full-width on mobile.
- **Form Grid**: Refine the `form-grid` gap and column spans to prevent overflow.

## Verification Plan

### Manual Verification
- Test various mobile device widths to verify that:
    1. All labels are fully visible.
    2. Input boxes are wide enough for data entry.
    3. The "Create Free Account" button is fully visible and clickable.
    4. The background "Orbs" do not interfere with form readability.
