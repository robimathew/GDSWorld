from pathlib import Path

# Directory to save snippets
component_dir = Path("./prompt_snippets/components")
component_dir.mkdir(parents=True, exist_ok=True)

# Rewriting each snippet into its own file based on prior prompts
individual_snippets = {
    "accordion.txt": '''Use the accordion component to help users navigate content on long pages.

Example:
<div class="govuk-accordion" data-module="govuk-accordion" id="accordion-default">
  <div class="govuk-accordion__section">
    <div class="govuk-accordion__section-header">
      <h2 class="govuk-accordion__section-heading">
        <button type="button" class="govuk-accordion__section-button" id="accordion-default-heading-1">
          Section 1
        </button>
      </h2>
    </div>
    <div id="accordion-default-content-1" class="govuk-accordion__section-content" aria-labelledby="accordion-default-heading-1">
      <p class="govuk-body">Content for section 1.</p>
    </div>
  </div>
</div>
''',

    "back-link.txt": '''Use the back link component to let users return to the previous page.

Example:
<a href="#" class="govuk-back-link">Back</a>
''',

    "breadcrumbs.txt": '''Use breadcrumbs to help users understand where they are within a service.

Example:
<div class="govuk-breadcrumbs">
  <ol class="govuk-breadcrumbs__list">
    <li class="govuk-breadcrumbs__list-item"><a class="govuk-breadcrumbs__link" href="#">Home</a></li>
    <li class="govuk-breadcrumbs__list-item">Page</li>
  </ol>
</div>
''',

    "button.txt": '''Use the button component for form submissions and actions.

Example:
<button class="govuk-button" data-module="govuk-button">Continue</button>
''',

    "character-count.txt": '''Use the character count component for long text input with a character limit.

Example:
<div class="govuk-form-group">
  <label class="govuk-label" for="more-detail">Can you provide more detail?</label>
  <textarea class="govuk-textarea" id="more-detail" name="more-detail" rows="5" aria-describedby="more-detail-info"></textarea>
  <div id="more-detail-info" class="govuk-hint">You can enter up to 200 characters</div>
</div>
''',

    "checkboxes.txt": '''Use checkboxes to let users select multiple options from a list.

Example:
<div class="govuk-form-group">
  <fieldset class="govuk-fieldset">
    <legend class="govuk-fieldset__legend">Select your interests</legend>
    <div class="govuk-checkboxes">
      <div class="govuk-checkboxes__item">
        <input class="govuk-checkboxes__input" id="interest-sports" name="interests" type="checkbox" value="sports">
        <label class="govuk-label govuk-checkboxes__label" for="interest-sports">Sports</label>
      </div>
      <div class="govuk-checkboxes__item">
        <input class="govuk-checkboxes__input" id="interest-music" name="interests" type="checkbox" value="music">
        <label class="govuk-label govuk-checkboxes__label" for="interest-music">Music</label>
      </div>
    </div>
  </fieldset>
</div>
'''
}

# Write each snippet into its own file
for filename, content in individual_snippets.items():
    (component_dir / filename).write_text(content, encoding="utf-8")

"./prompt_snippets/components"
