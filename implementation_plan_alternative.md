# Add Alternative Image Generation Provider

The user wants an alternative to Hugging Face tokens. We will implement **Pollinations.ai** as a secondary (or primary) provider because it is free, high-quality, and does not require an API token.

## Proposed Changes

### [Component] User Views

#### [MODIFY] [views.py](file:///c:/Users/arthi/OneDrive/Desktop/PROJECT/TexttoImageGeneration/users/views.py)
- Refactor `test_text_to_image` to support multiple providers.
- Implement Pollinations logic: `https://image.pollinations.ai/prompt/{prompt}`.
- Provide a UI toggle (optional) or automatic fallback if HF fails.

## Verification Plan

### Manual Verification
1. Test generating an image using the new provider.
2. Confirm the image is saved to the media directory.
