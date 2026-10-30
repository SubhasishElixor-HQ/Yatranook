# MASTER PROMPT — YATRANOOK PRODUCTION-GRADE FRONTEND UI DESIGN AND DEVELOPMENT

## 1. Your Role

Act as a Senior UI/UX Designer, Product Designer, Frontend Architect, React Developer, Design System Engineer, and Accessibility Specialist.

Your task is to design and develop a complete, professional, production-oriented frontend for **Yatranook — An AI-Powered Intelligent Tourism Assistant for Odisha**.

Do not create a simple landing page, static dashboard, generic AI chatbot, or collection of disconnected UI screens.

Build a complete, interactive travel-planning application that provides a smooth experience from the first user interaction to destination discovery, personalized itinerary generation, budget management, route visualization, trip saving, and supported external booking and navigation handoffs.

The interface must feel like a real commercial travel-tech product that could be presented to users, startup evaluators, investors, and tourism stakeholders.

Prioritize excellent user experience, clean architecture, responsive design, accessibility, consistency, performance, and maintainable frontend code.

---

## 2. Project Vision

**Product:** Yatranook

**Tagline:** Discover More. Plan Smarter. Travel Better.

Yatranook is an AI-powered tourism platform initially focused on Odisha, India.

Its objective is to help travelers transform a simple travel idea into a practical, personalized, budget-aware, and geographically optimized journey.

A traveler should be able to say:

"I am starting from Bhubaneswar. I have ₹2,000. I want to explore temples, beaches, nature, and local food. Suggest a one-day trip."

Yatranook should help the traveler:

1. Provide a starting location.
2. Select a state, city, or destination.
3. Describe interests and preferences.
4. Enter a realistic travel budget.
5. Discover suitable destinations.
6. Find nearby attractions.
7. Compare cheapest, fastest, and balanced routes.
8. Generate a day-wise itinerary.
9. See estimated trip expenses.
10. Modify the itinerary conversationally.
11. Save and manage the trip.
12. Access supported booking services.
13. Open directions to planned destinations.

The frontend must make this workflow understandable and effortless.

---

## 3. Mandatory Technology Stack

Use the following frontend stack:

| Technology | Purpose |
|---|---|
| React | UI development |
| TypeScript | Type safety |
| Vite | Development and production build |
| Tailwind CSS | Styling and responsive layouts |
| React Router | Routing and navigation |
| TanStack Query | API requests, caching, server state |
| Zustand | Shared client-side state when appropriate |
| React Hook Form | Form handling |
| Zod | Input and schema validation |
| Axios or Fetch | Backend communication |
| Lucide React | Consistent icons |
| Map integration | Interactive maps and route visualization |
| Vitest | Unit and component testing |
| React Testing Library | Component behavior testing |
| Playwright | End-to-end testing |

Use stable, compatible versions of dependencies.

Do not introduce unnecessary frontend frameworks or state-management libraries.

---

# 4. BRAND IDENTITY AND DESIGN DIRECTION

Create a distinctive, premium visual identity for Yatranook.

The design should combine:

- Modern travel technology.
- Intelligent AI assistance.
- Indian tourism and cultural identity.
- Premium travel-platform aesthetics.
- Clean and professional SaaS-style structure.

### Color Palette

Use a consistent design system.

| Design Element | Preferred Color |
|---|---|
| Main background | White `#FFFFFF` |
| Secondary background | Very light blue-gray `#F8FAFC` |
| Primary navy | `#142D4E` |
| Primary blue | `#2563EB` |
| Teal accent | `#0D9488` |
| Subtle saffron accent | `#F59E0B` |
| Main text | `#172033` |
| Secondary text | `#64748B` |
| Borders | `#E2E8F0` |
| Success | `#15803D` |
| Warning | `#D97706` |
| Error | `#DC2626` |

Use colors consistently and meaningfully.

Do not make the interface overly colorful.

### Visual Style

- Clean white backgrounds.
- Deep navy headings.
- Blue and teal accents.
- Subtle borders.
- Soft and restrained shadows.
- Rounded cards.
- Consistent spacing.
- Clear typography.
- Premium destination photography.
- Beautiful map visualizations.
- Carefully structured content.

Avoid:
- Excessive gradients.
- Excessive shadows.
- Too many colors.
- Overcrowded dashboards.
- Giant empty spaces.
- Oversized headings.
- Generic template-like layouts.
- Random icon usage.
- Inconsistent border radii.
- Unnecessary animations.

### Typography

Use a modern readable sans-serif font, such as Inter or an equivalent suitable typeface.

Establish a typography system for:

- Page titles.
- Section headings.
- Card titles.
- Body text.
- Labels.
- Supporting descriptions.
- Buttons.
- Financial values.
- Map labels.

Ensure appropriate contrast and readability on desktop and mobile.

---

# 5. COMPLETE APPLICATION STRUCTURE

Create a complete application with the following major areas.

## A. Public Website

### Page 1 — Landing Page

Create a premium, high-converting Yatranook homepage.

Sections:

1. Navigation bar.
2. Hero section.
3. Main conversational travel-search interface.
4. Popular Odisha destinations.
5. How Yatranook works.
6. Key product capabilities.
7. Featured experiences.
8. Why choose Yatranook.
9. How AI-assisted travel planning works.
10. Frequently asked questions.
11. Footer.

### Hero Section

Main headline:

**Your Journey Starts With One Conversation.**

Supporting text:

"Discover destinations, plan smarter itineraries, manage your budget, and explore with an AI-powered travel companion."

Primary CTA:

**Plan My Trip**

Secondary CTA:

**Explore Destinations**

Design the hero with an attractive Odisha travel photograph, a subtle map graphic, and a realistic Yatranook conversational interface preview.

Do not overload the hero with multiple competing cards.

### Travel Search Interface

Create an attractive input area containing:

- Starting location.
- Destination or state.
- Travel dates.
- Budget.
- Number of travelers.
- Interests.

Allow travelers to start planning through conversation rather than forcing them to complete a long form.

---

## B. Application Dashboard

### Page 2 — Main Dashboard

The dashboard should help a user start planning, discover destinations, and continue existing trips.

Include:

**Welcome Section**

"Where would you like to explore today?"

**Quick Actions**
- Plan a trip.
- Explore destinations.
- Find nearby attractions.
- View saved trips.

**Current and Upcoming Trips**

Display:
- Destination.
- Travel dates.
- Budget.
- Itinerary status.
- Next planned activity.

**Recommended Destinations**

Display visually attractive destination cards.

**Travel Planning Assistant**

A clear entry point into conversational trip planning.

**Recently Viewed**

Show previously explored destinations where user data is available.

Keep the dashboard useful rather than filling it with meaningless statistics.

---

# 6. AI CONVERSATIONAL TRAVEL PLANNING

This is the most important frontend experience.

### Page 3 — AI Travel Planner

Build an elegant, conversational interface.

It should feel like interacting with a knowledgeable human travel planner, not a generic chatbot.

### Layout

Desktop:

- Left: Main conversation area.
- Right: Trip context and selected preferences.
- Optional map or destination preview when relevant.

Mobile:

- Conversation takes priority.
- Trip context is accessible through a collapsible panel.
- Controls remain easy to use.

### Conversation Flow

The assistant should progressively ask for missing information.

**Question 1: Starting Location**

"Where are you starting your journey?"

Options:
- Use my current location.
- Enter location manually.

Never access precise location without explicit user permission.

**Question 2: Destination**

"Where would you like to travel?"

Options:
- Select a destination.
- Choose a state.
- Discover places near me.
- Suggest the best places within my budget.

**Question 3: Budget**

"What is your total travel budget?"

Include:
- Custom amount input.
- Total trip budget / per-person budget.
- Group size.

Support Indian currency formatting.

Valid low budgets must not produce an arbitrary minimum-budget error.

**Question 4: Travel Preferences**

Use selectable preference chips:

- Temples.
- Beaches.
- Nature.
- Wildlife.
- Historical places.
- Adventure.
- Food.
- Photography.
- Relaxation.
- Cultural experiences.

**Question 5: Trip Duration**

Ask how many hours or days the user has available.

### Chat Interface Components

- User and assistant messages.
- Message timestamps where useful.
- Typing indicator.
- Suggested responses.
- Quick action chips.
- Destination cards inside conversations.
- Itinerary preview cards.
- Source references.
- Error and retry states.
- Edit preferences action.
- Clear trip context action.

The assistant should retain previously entered information throughout the trip-planning session.

Do not ask for the same starting location, budget, or destination repeatedly unless the user changes it.

### Important Interaction

User:

"I have ₹1,500. Suggest a one-day trip from Bhubaneswar."

The interface must not respond with a rigid validation error.

Instead, show an assistant response with affordable destination options and an explanation of the estimated travel costs.

---

# 7. DESTINATION DISCOVERY

### Page 4 — Explore Odisha

Create a visually rich destination-discovery experience.

Include:

- Search bar.
- State and city filters.
- Destination categories.
- Popular destinations.
- Nearby destinations.
- Lesser-known places.
- Featured attractions.
- Destination collections.

Category chips:

- Temples.
- Beaches.
- Heritage.
- Nature.
- Wildlife.
- Culture.
- Local Food.
- Adventure.

Destination cards should contain:

- Attractive image.
- Destination name.
- Location.
- Category.
- Short description.
- Distance from the selected origin when available.
- Relevant visitor information.
- View details action.

Support responsive grid layouts.

### Page 5 — Destination Details

Create an individual page for every destination.

Include:

1. Large destination image.
2. Destination name.
3. Location.
4. Description.
5. Historical and cultural information.
6. Attractions nearby.
7. Map.
8. Estimated visiting duration.
9. Available visitor information.
10. Relevant tourism sources.
11. Add to itinerary action.
12. Plan a trip around this place action.

Clearly distinguish verified information from estimated or unavailable information.

Do not invent ratings, visitor counts, fees, opening hours, or reviews.

---

# 8. SMART ROUTE PLANNER

### Page 6 — Route Optimization

Create a high-quality interactive route-planning page.

Show an interactive map with numbered destination markers and connected route lines.

Include a route summary panel.

Display four planning modes:

1. Cheapest Route.
2. Fastest Route.
3. Shortest Distance.
4. Balanced Route — Recommended.

Show:

- Starting point.
- Destination sequence.
- Distance between stops.
- Estimated travel time.
- Transportation mode.
- Estimated transportation cost when available.
- Return journey.

Use an understandable map layout.

The route and ordered stops displayed in the itinerary must always match.

Support editing:

- Add a destination.
- Remove a destination.
- Reorder stops.
- Change travel mode.
- Optimize again.

When actual routing data is not available, show an appropriate unavailable or illustrative status rather than fake directions.

### Map Design

Use:

- Numbered markers.
- Route polylines.
- Start and destination markers.
- Selected-stop highlighting.
- Distance and time labels where appropriate.
- Map legend.
- Route controls.
- Expandable map view.

Make the map visually central without allowing it to overwhelm the rest of the page.

---

# 9. BUDGET PLANNER

### Page 7 — Budget Management

Build a modern, understandable trip budget interface.

Include:

- Total available budget.
- Estimated total cost.
- Remaining budget.
- Budget status.
- Category-wise expense breakdown.
- Estimated versus actual spending.
- Alternative affordable plans.

Expense categories:

- Transportation.
- Accommodation.
- Food.
- Entry fees.
- Activities.
- Local travel.
- Miscellaneous.

Use charts or progress indicators only when they improve understanding.

### Over-Budget Experience

When an itinerary exceeds the budget, display:

**Your current plan is above your budget. Let's optimize it.**

Offer:
- Lower-cost alternatives.
- Shorter route.
- Fewer destinations.
- More affordable transport.
- Nearby attractions.
- Reduced accommodation expense.

Actions:

- Optimize budget.
- Show cheaper destinations.
- Shorten the trip.
- Customize itinerary.

Do not simply display a red error message.

The cost calculations must come from backend data and deterministic application logic.

---

# 10. ITINERARY AND TRIP MANAGEMENT

### Page 8 — Generated Itinerary

Create a beautiful day-wise itinerary.

Each day should display:

- Day number.
- Date.
- Starting location.
- Ordered destination stops.
- Arrival time estimates.
- Activity duration.
- Travel time.
- Distance.
- Meal breaks.
- Rest periods.
- Expenses.
- Return location.

Use a timeline layout with numbered circles and connecting lines.

Actions:
- Edit.
- Add stop.
- Remove stop.
- Reorder.
- Recalculate.
- Save trip.
- Share where supported.

### Page 9 — Trip Details Dashboard

Display a complete saved trip with:

- Trip overview.
- Selected destinations.
- Itinerary.
- Map.
- Budget.
- Actual expenses.
- Saved checklist.
- Relevant reservation status.
- Useful information.

Distinguish confirmed bookings from recommended services and uncompleted booking actions.

### Page 10 — My Trips

Show:

- Upcoming trips.
- Ongoing trips.
- Completed trips.
- Saved drafts.

Use tabs and clear trip cards.

Allow users to open, edit, duplicate, or delete their own trips according to appropriate permissions.

---

# 11. BOOKING AND TRAVEL SERVICES

### Page 11 — Accommodation and Activities

When supported by real backend integrations, display provider options for:

- Accommodation.
- Activities.
- Local experiences.
- Tours.
- Transportation.

Each result should show available information such as:

- Price.
- Provider.
- Location.
- Facilities.
- Availability.
- Cancellation conditions.
- Source freshness.

Add clear review and continue actions.

The booking confirmation UI must only show a confirmed status after receiving and verifying a real provider confirmation.

If an integration is unavailable, provide a clearly labeled external handoff instead.

Do not create fake booking functionality that only changes a button into "Confirmed."

---

# 12. ACCOUNT AND SETTINGS

### Page 12 — Profile and Preferences

Create:

- User profile.
- Travel interests.
- Preferred language.
- Currency preferences.
- Saved locations.
- Privacy settings.
- Location permissions.
- Notification preferences.
- Account security.
- Data management.

Allow users to control their saved travel preferences.

---

# 13. GLOBAL APPLICATION LAYOUT

Build a reusable application shell.

### Desktop Navigation

Use a premium sidebar or top-navigation structure with:

- Dashboard.
- AI Planner.
- Explore.
- My Trips.
- Saved Places.
- Settings.

The planner should remain easy to access.

### Mobile Navigation

Use a mobile-first navigation system.

Prioritize:
- Home.
- Explore.
- Plan.
- Trips.
- Profile.

Ensure maps, cards, conversations, and forms adapt correctly to narrow screens.

Do not simply shrink the desktop interface.

---

# 14. DESIGN SYSTEM AND REUSABLE COMPONENTS

Create a centralized design system.

### Layout Components

- AppShell.
- Sidebar.
- Navbar.
- PageHeader.
- MainContainer.
- ContentSection.
- ResponsiveGrid.

### Input Components

- TextInput.
- LocationSearch.
- BudgetInput.
- DatePicker.
- Select.
- MultiSelect.
- PreferenceChip.
- FormField.

### Travel Components

- DestinationCard.
- DestinationImage.
- AttractionCard.
- NearbyPlaces.
- TripCard.
- ItineraryTimeline.
- RouteStop.
- RouteSummary.
- BudgetBreakdown.
- ExpenseCard.
- BookingCard.
- TravelChecklist.

### AI Components

- ChatPanel.
- MessageBubble.
- AssistantTypingIndicator.
- SuggestionChip.
- TripContextPanel.
- ItineraryPreview.
- SourceCitation.
- AIErrorState.

### Map Components

- InteractiveMap.
- DestinationMarker.
- RoutePolyline.
- MapLegend.
- RouteControls.
- MapLoadingState.

Use reusable components rather than duplicating interface code across pages.

Centralize design tokens for color, spacing, typography, shadows, and border radius.

---

# 15. FRONTEND PROJECT STRUCTURE

Inspect the existing repository first.

If starting from an empty project, use a maintainable feature-based structure similar to:

```text
apps/web/
├── public/
│   ├── images/
│   └── icons/
│
├── src/
│   ├── app/
│   │   ├── App.tsx
│   │   ├── router.tsx
│   │   └── providers.tsx
│   │
│   ├── assets/
│   ├── components/
│   │   ├── ui/
│   │   ├── layout/
│   │   ├── maps/
│   │   └── shared/
│   │
│   ├── features/
│   │   ├── auth/
│   │   ├── dashboard/
│   │   ├── assistant/
│   │   ├── locations/
│   │   ├── destinations/
│   │   ├── discovery/
│   │   ├── trips/
│   │   ├── itineraries/
│   │   ├── budget/
│   │   ├── routes/
│   │   ├── maps/
│   │   └── bookings/
│   │
│   ├── hooks/
│   ├── lib/
│   │   ├── api/
│   │   ├── formatting/
│   │   └── utilities/
│   │
│   ├── providers/
│   ├── schemas/
│   ├── stores/
│   ├── types/
│   ├── styles/
│   └── tests/
│
├── .env.example
├── package.json
├── tsconfig.json
├── vite.config.ts
└── ...
```

Adapt the structure to the existing codebase. Do not create duplicate routes or components where equivalent implementations already exist.

Each feature should own its components, hooks, types, schemas, and API integrations where appropriate.

---

# 16. API INTEGRATION WITH FASTAPI

The React application must communicate with the FastAPI backend using a centralized, typed API layer.

Organize API clients for:

- Authentication.
- Locations.
- Destinations.
- Discovery.
- Assistant.
- Trips.
- Itineraries.
- Budgets.
- Routes.
- Maps.
- Bookings.

Use:

- Typed request and response models.
- Authentication-aware requests.
- TanStack Query caching.
- Loading and error states.
- Retry behavior where appropriate.
- Request cancellation where useful.
- API timeouts.
- Consistent error handling.

Expected API groups may include:

```text
/api/v1/auth
/api/v1/users
/api/v1/locations
/api/v1/destinations
/api/v1/discovery
/api/v1/assistant
/api/v1/trips
/api/v1/itineraries
/api/v1/budgets
/api/v1/routes
/api/v1/bookings
```

Use the actual backend OpenAPI schema to define types wherever possible.

Do not invent backend endpoints and assume they exist.

If the backend is incomplete, isolate missing functionality behind typed interfaces and clearly identify what needs backend implementation.

---

# 17. FRONTEND INTERACTIVITY REQUIREMENTS

Every visible control must perform a meaningful action.

Implement:

- Navigation.
- Search.
- Filters.
- Sorting.
- Conversation submission.
- Suggested chat responses.
- Location selection.
- Budget input.
- Preference selection.
- Date selection.
- Destination selection.
- Map interactions.
- Itinerary editing.
- Route recalculation.
- Trip saving.
- Expense updates.
- Booking handoff where supported.

Do not create decorative buttons that do nothing.

Use appropriate dialogs, drawers, popovers, confirmation states, and toast notifications.

Keep input state controlled and validated.

Preserve relevant trip state while navigating between related screens.

---

# 18. RESPONSIVE DESIGN

Design and test all pages across:

### Mobile
Approximately 360–430 px widths.

### Tablet
Approximately 768–1024 px widths.

### Desktop
Approximately 1280–1440 px widths.

### Large Desktop
Approximately 1600 px and above.

Pay particular attention to:

- Chat layouts.
- Destination card grids.
- Maps.
- Route side panels.
- Itinerary timelines.
- Budget charts.
- Navigation.
- Tables and dialogs.

The interface should never have unintended horizontal overflow, overlapping text, clipped controls, or unreadable labels.

---

# 19. ACCESSIBILITY AND UX QUALITY

Follow accessible design principles.

Implement:

- Keyboard navigation.
- Visible focus indicators.
- Proper labels.
- Semantic HTML.
- Appropriate ARIA attributes.
- Sufficient color contrast.
- Accessible dialogs.
- Screen-reader-friendly status messages.
- Descriptive icon labels.
- Touch-friendly controls.

Add appropriate:

- Loading skeletons.
- Empty states.
- Error states.
- Retry actions.
- Success feedback.
- Confirmation dialogs.
- Helpful validation messages.

Use animations sparingly and respect reduced-motion preferences.

---

# 20. FRONTEND PERFORMANCE AND PRODUCTION QUALITY

Optimize the frontend using:

- Code splitting.
- Lazy-loaded routes.
- Reusable components.
- Optimized images.
- Responsive image sizes.
- Efficient query caching.
- Debounced search.
- Controlled state updates.
- Bundle-size awareness.
- Appropriate error boundaries.

Consider SEO for public landing and destination pages.

Do not expose backend secrets or API keys in frontend environment variables.

Public frontend configuration may contain only values intended to be visible to users.

---

# 21. TESTING REQUIREMENTS

Use Vitest, React Testing Library, and Playwright.

Test:

### Component Tests
- Navigation.
- Inputs.
- Cards.
- Chat components.
- Route controls.
- Budget displays.

### Feature Tests
- Travel request creation.
- Progressive conversation.
- Location entry.
- Destination discovery.
- Budget validation.
- Itinerary rendering.
- Trip editing.
- API error handling.

### Accessibility Tests
- Keyboard interaction.
- Form labels.
- Dialog behavior.
- Semantic structure.

### End-to-End Tests

Test a continuous user journey:

1. Open Yatranook.
2. Start travel planning.
3. Enter Bhubaneswar as the starting location.
4. Choose Odisha as the travel region.
5. Enter ₹2,000 as the total budget.
6. Select temples, beaches, and nature.
7. Receive destination suggestions.
8. Select an itinerary.
9. View its budget and route.
10. Modify a destination.
11. Recalculate the plan.
12. Save the trip.
13. Open directions through a supported map action.

Use API mocks for frontend tests when the real backend or external provider is unavailable.

Never mark a real booking or navigation capability as verified merely because its frontend mock works.

---

# 22. IMPLEMENTATION WORKFLOW

Work in the following phases.

## Phase 1 — Existing Frontend Audit

- Inspect the existing repository.
- Review package.json and dependencies.
- Inspect current routes and components.
- Understand the existing frontend design.
- Identify broken or incomplete screens.
- Check how FastAPI APIs are currently connected.
- Preserve existing working features.

## Phase 2 — Design System

- Establish color tokens.
- Establish typography.
- Establish spacing.
- Establish reusable components.
- Establish responsive breakpoints.
- Define navigation and application layout.

## Phase 3 — Main Application

Build the dashboard, landing page, navigation, and responsive application shell.

## Phase 4 — AI Travel Planner

Build the complete conversational travel-planning experience and context interface.

## Phase 5 — Destinations and Maps

Build destination discovery, destination details, nearby attraction cards, and route visualization.

## Phase 6 — Itinerary and Budget

Build itinerary timelines, route summaries, budget breakdowns, and editing interactions.

## Phase 7 — Trip and Booking Management

Build saved trips, trip details, booking handoffs, and navigation actions according to backend capability.

## Phase 8 — API Integration

Connect all supported frontend features to the real FastAPI backend through typed API services.

## Phase 9 — Testing and Refinement

Fix layout issues, responsiveness problems, validation errors, accessibility issues, and broken interactions.

## Phase 10 — Production Build

Run linting, TypeScript checks, frontend tests, end-to-end tests, and production build verification.

Do not skip a phase's verification before moving to dependent functionality.

---

# 23. ACCEPTANCE CRITERIA

The frontend is acceptable only when:

1. It has a consistent, professional Yatranook brand.
2. Every major page has a completed, intentional design.
3. The application works across mobile, tablet, and desktop.
4. The travel-planning conversation is intuitive.
5. The user can enter a starting location manually or through permission-based geolocation.
6. The user can discover destinations.
7. The budget interface accepts valid low budgets.
8. Destination cards communicate useful information.
9. Itinerary screens display ordered stops clearly.
10. Maps correspond to the same route as the itinerary.
11. Budget totals are based on backend values rather than invented frontend calculations.
12. Saved trips are connected to the backend when implemented.
13. Booking actions use an actual provider integration or transparent external handoff.
14. Every visible button performs its advertised action.
15. Loading, empty, error, and success states exist.
16. No overlapping text, clipped components, or broken layouts remain.
17. TypeScript checks pass.
18. Linting passes.
19. Automated tests pass.
20. The production build succeeds.

---

# 24. FINAL DELIVERABLES

Provide:

1. Complete frontend architecture.
2. Full page and route inventory.
3. Yatranook design system.
4. Reusable component library.
5. Responsive React application.
6. AI travel-planning interface.
7. Destination discovery interface.
8. Interactive map and route interface.
9. Itinerary interface.
10. Budget and expense interface.
11. Saved trips and trip-management interface.
12. Booking handoff interface where applicable.
13. Typed FastAPI integration layer.
14. Frontend test suite.
15. Updated README.
16. Environment configuration example.
17. Production build verification.
18. List of frontend features that still depend on backend implementation.

### FINAL INSTRUCTION

Build Yatranook as a polished, modern, premium, production-oriented travel-tech product.

The result should not look like a generic AI dashboard or an ordinary travel website.

The central experience must be a human-like intelligent travel planner that seamlessly connects conversation, destination discovery, maps, routes, budgets, itineraries, and supported travel services.

Make every screen visually consistent, every important interaction functional, every component maintainable, and every integration honest about its actual implementation status.

**Yatranook — Discover More. Plan Smarter. Travel Better.**