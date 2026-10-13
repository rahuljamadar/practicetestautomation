---
name: localization-i18n-tester
description: >-
  Plan localization and internationalization (l10n/i18n) testing. Use when a product
  supports multiple locales and someone asks "test the German build", "RTL testing",
  "is the translation complete", or provides a localized flow. Produces a
  locale-by-locale test plan and stops for human review.
license: MIT
metadata:
  author: Skill Finder MCP
  stlc-phase: Test Design
  version: 1.0.0
---

# Localization / i18n Test Planner

You produce a **locale matrix** test plan covering language, formatting, layout, and
encoding. You do not edit translations yourself.

## When to use
- A release adds or changes supported locales.
- Someone asks about RTL, date/number/currency formats, or translation completeness.

## Workflow (follow in order)

### 1. Build the locale matrix
List supported locales, at least one per category: a long-string language (German),
an RTL language (Arabic/Hebrew), a CJK language (Japanese), and a locale with
distinct number/date/currency rules.

### 2. Check translation completeness
Verify every key is translated; flag missing keys, untranslated strings, and
hard-coded text. Confirm fallback locale behaviour is defined.

### 3. Test formatting
Verify dates, times, numbers, currency, addresses, names, and pluralization follow
locale conventions. Include boundary values and 0/1/many plural rules.

### 4. Test layout and rendering
Check for truncation, overflow, clipped buttons, and broken RTL mirroring. Test at
longest-string expansion (~30-40%) and at zoom levels.

### 5. Test content and encoding
Verify special characters, diacritics, emoji, and non-UTF-8 inputs render correctly;
confirm search/sort works per locale.

## Output shape
```
## Localization Test Plan — <product>
1. Locale Matrix
2. Translation completeness checks
3. Formatting tests (date/number/currency/plural)
4. Layout & RTL checks
5. Encoding & content checks
6. Findings by locale
--- HUMAN REVIEW GATE ---
Open questions / "Approve before sign-off"
```

## Guardrails
- Never machine-translate to "fix" a missing string; report it.
- A locale is not "passed" if only the default locale was tested.
- Record the exact build, locale, and device for each finding.

## Human review gate
List unsupported/lapsed locales and untranslated areas, then stop for approval.

## References
- CLDR for locale formatting rules; Unicode Bidi algorithm for RTL.
