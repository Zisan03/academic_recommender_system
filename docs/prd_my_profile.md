# Product Requirements Document (PRD)

# SmartLearn AI – Module: My Profile Enhancement

**Version:** 1.0  
**Status:** Under Review  
**Target Module:** My Profile (`/accounts/profile/`)  
**Development Methodology:** Incremental (One File at a Time)  

---

## 1. Module Overview

### 1.1 Purpose
The **My Profile** tab serves as the student's central academic dashboard and identity hub within SmartLearn AI. While a preliminary profile template (`accounts/profile.html`) exists in the codebase, it is currently disconnected from the sidebar navigation (`href="#"`) and lacks deep integration with the AI recommendation scoring history and saved study materials.

### 1.2 Objectives
* Wire the sidebar navigation to seamlessly open the student's academic profile.
* Upgrade the profile interface into a structured, multi-section dashboard (Academic Overview, AI Score Progression, and Saved/Recent Materials).
* Display transparent metrics regarding the student's assigned Machine Learning dataset mapping and identified weak topics.
* Provide an intuitive bookmarking / saved study materials view without altering stable database schemas.

---

## 2. Compliance with Development Rules (`guidelines.md`)

* **Rule 1 — One File at a Time:** Modifications will proceed strictly file-by-file (`sidebar.html` $\rightarrow$ `views.py` $\rightarrow$ `profile.html`), verifying via `runserver` after each replacement.
* **Rule 4 — Backend & Schema Stability (Critical Decision):**
  * To comply with locked database schemas, **no new `SavedResource` database model will be created**.
  * Instead, "Saved Resources" will be supported via **Local Storage / Session-based bookmarks** or by highlighting frequently viewed items from `ResourceInteraction`. This ensures zero risk to the ML pipeline or database stability.

---

## 3. Functional Requirements

### 3.1 Academic Profile Header & Overview
* Display student identity banner: Username, Email, Department, and Academic Level.
* Showcase ML Dataset Mapping ID (`dataset_student_id`) clearly to explain how the offline AI recommendation model identifies the student.

### 3.2 AI Recommendation Insights Section
* Display AI Recommendation statistics calculated directly from the ML engine:
  * **Total Recommendations Available:** Count of generated resources tailored to the student.
  * **Primary Weak Topic:** The specific academic area (e.g., Calculus, Statistics) targeted by the hybrid recommendation model.
  * **Model Type Badge:** "Hybrid Collaborative + Content-Based ML".

### 3.3 Recently Viewed & Bookmarked Resources Section
* Display a tabbed or side-by-side view showing:
  * **Recent Activity:** Top 5 most recently interacted learning resources from `ResourceInteraction`.
  * **Bookmarked Materials:** Quick-access list of study items bookmarked by the student during their session.

---

## 4. Technical Architecture & Files Affected

### 4.1 Navigation & Routing
1. **`templates/partials/sidebar.html` [MODIFY]**
   * Change line 58 from `<a href="#">` to `<a href="{% url 'profile' %}" class="{% if '/accounts/profile' in request.path %}active{% endif %}">`.

### 4.2 Backend View Enhancement
2. **`accounts/views.py` [MODIFY]**
   * Enhance `profile_view(request)` to calculate comprehensive recommendation stats and pass structured context to the template.
   * Ensure robust fallback handling if `StudentProfile` attributes (department, level) are default or blank.

### 4.3 Template Refactoring
3. **`templates/accounts/profile.html` [MODIFY]**
   * Refactor layout using CSS grid to create clean UI cards:
     * Card 1: Student Academic Profile Details.
     * Card 2: AI Recommendation & Weak Topic Diagnostics.
     * Card 3: Interactive Activity & Bookmarks list.
   * Apply styling consistent with `dashboard.css` and `base.css` (glassmorphism headers, gradient icons, pill badges).

---

## 5. Step-by-Step Execution Plan (One-File Workflow)

* **Step 1:** Modify `templates/partials/sidebar.html` to enable the "My Profile" sidebar link and active state highlighting. Test navigation.
* **Step 2:** Modify `accounts/views.py` (`profile_view`) to include full recommendation count and diagnostic stats in context. Verify server check.
* **Step 3:** Replace `templates/accounts/profile.html` with the upgraded multi-card layout and bookmarking UI.
* **Step 4:** Perform browser testing: verify responsive grid behavior on mobile and tablet viewports.

---

## 6. Definition of Done
* [ ] Clicking "My Profile" in the sidebar routes to `/accounts/profile/` and highlights the navigation icon.
* [ ] Student department, level, and dataset ID render accurately from the database.
* [ ] AI recommendation count and weak topic statistics match the ML model predictions.
* [ ] Recent activity links route correctly to resource detail pages.
* [ ] No database schema changes or backend regressions introduced.
