# Product Requirements Document (PRD)

# SmartLearn AI – Module: Learning Activity Tab

**Version:** 1.0  
**Status:** Under Review  
**Target Module:** Learning Activity (`/resources/activity/`)  
**Development Methodology:** Incremental (One File at a Time)  

---

## 1. Module Overview

### 1.1 Purpose
The **Learning Activity** module provides students with an interactive, chronological timeline of their academic study history. It tracks user engagement across all study materials (Videos, PDFs, Practice exercises), recording timestamps, categorization badges, and cumulative study statistics.

### 1.2 Objectives
* Visualize student interaction history in a clean, modern timeline format.
* Quantify study habits by displaying total resources viewed and breakdown by academic topic.
* Provide quick re-access to previously viewed study materials.
* Encourage continuous learning through gamified visual metrics.

---

## 2. Compliance with Development Rules (`guidelines.md`)

* **Rule 1 — One File at a Time:** Only one file (`views.py`, `urls.py`, or `activity.html`) will be created/modified per iteration, followed immediately by testing via `python manage.py runserver`.
* **Rule 2 & Rule 4 — Backend & Schema Stability:** The backend database schema is locked. This module will **strictly utilize the existing `ResourceInteraction` model** (`resources_app/models.py`) and `StudentProfile` model. No database migrations or schema alterations will be performed.

---

## 3. Functional Requirements

### 3.1 Activity Timeline Display
* Fetch all `ResourceInteraction` records associated with the authenticated user (`request.user.studentprofile`).
* Display items ordered by `viewed_at` descending (most recent first).
* For each interaction, render:
  * Resource Title and Topic Badge (Algebra, Calculus, Programming, Statistics).
  * Difficulty Badge (Beginner, Intermediate, Advanced) and Resource Type Icon (Video play icon, PDF document icon, Practice exercise icon).
  * Exact formatted timestamp (e.g., "July 4, 2026 - 18:45").
  * Action button: "Re-open Resource →".

### 3.2 Engagement Statistics Header
* Compute and display high-level metrics at the top of the tab:
  * **Total Interactions:** Cumulative number of study resources viewed.
  * **Top Subject:** The topic category with the highest interaction count.
  * **Active Streak / Status:** Current learning activity status.

### 3.3 Empty State Handling
* If the student has zero recorded interactions, render an inviting empty state card with:
  * Illustration / Icon (`fa-folder-open` or `fa-book-reader`).
  * Encouraging message: *"No learning activity recorded yet. Explore your AI recommendations to start building your study streak!"*
  * Call-to-action button linking to `{% url 'recommendations' %}`.

---

## 4. Technical Architecture & Files Affected

### 4.1 Backend Routing & Logic
1. **`resources_app/views.py` [MODIFY]**
   * Implement `@login_required` view `resource_activity(request)`.
   * Query: `ResourceInteraction.objects.filter(student__user=request.user).select_related('resource').order_by('-viewed_at')`.
   * Aggregate stats and pass `context = {"interactions": ..., "total_views": ..., "top_topic": ...}`.

2. **`resources_app/urls.py` [MODIFY]**
   * Add URL pattern: `path("activity/", resource_activity, name="activity")`.

### 4.2 Frontend Template & Styling
3. **`templates/resources/activity.html` [NEW]**
   * Extend `base.html`.
   * Use CSS grid/flexbox styled with design system variables (`--primary`, `--secondary`, `--card`, `--shadow`).
   * Include responsive breakpoints for mobile (`< 768px`) and tablet (`< 992px`).

4. **`templates/partials/sidebar.html` [MODIFY]**
   * Update the Learning Activity link from `href="#"` to `href="{% url 'activity' %}"`.
   * Apply conditional class `{% if '/activity' in request.path %}active{% endif %}`.

---

## 5. Step-by-Step Execution Plan (One-File Workflow)

* **Step 1:** Modify `resources_app/views.py` to add `resource_activity` view function. Verify server stability.
* **Step 2:** Modify `resources_app/urls.py` to register the `/activity/` route. Verify no routing errors.
* **Step 3:** Create `templates/resources/activity.html` template with full timeline styling and empty state.
* **Step 4:** Modify `templates/partials/sidebar.html` to activate the sidebar link.
* **Step 5:** Final verification in browser (click resource, verify new interaction appears on timeline).

---

## 6. Definition of Done
* [ ] Visiting `/resources/activity/` displays the authenticated student's true interaction history.
* [ ] Clicking a study resource on `/resources/` and returning to `/resources/activity/` reflects the new interaction immediately.
* [ ] Sidebar "Learning Activity" link is highlighted when active.
* [ ] Zero database migrations or backend regressions introduced.
* [ ] Django server logs zero console or rendering errors.
