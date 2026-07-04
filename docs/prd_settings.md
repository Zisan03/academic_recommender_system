# Product Requirements Document (PRD)

# SmartLearn AI – Module: Settings Tab

**Version:** 1.0  
**Status:** Under Review  
**Target Module:** Settings (`/accounts/settings/`)  
**Development Methodology:** Incremental (One File at a Time)  

---

## 1. Module Overview

### 1.1 Purpose
The **Settings** module provides students with a dedicated control panel to manage their personal academic profile attributes, account credentials, and interface preferences. Keeping profile data (Department, Academic Level, Age) up-to-date is vital for ensuring the recommendation engine understands the student's academic context.

### 1.2 Objectives
* Allow students to edit their academic profile attributes (Department, Academic Level, Age) seamlessly.
* Provide basic account management (email updates and password modification guidance).
* Offer customizable UI preferences (e.g., interface theme selection and recommendation alert toggles).
* Deliver clear, visual success/error feedback upon form submission.

---

## 2. Compliance with Development Rules (`guidelines.md`)

* **Rule 1 — One File at a Time:** Development will execute sequentially: `forms.py` $\rightarrow$ `views.py` $\rightarrow$ `urls.py` $\rightarrow$ `settings.html` $\rightarrow$ `sidebar.html`. Each step must pass `runserver` validation.
* **Rule 4 — Backend Stability:** Updating `StudentProfile` attributes (`department`, `level`, `age`) utilizes standard Django ORM `save()` operations on existing columns. No changes will be made to database tables or relationships.

---

## 3. Functional Requirements

### 3.1 Academic Profile Settings Form
* Provide editable fields for the student's profile:
  * **Department:** Dropdown or text input (e.g., Computer Science, Electrical Engineering, Mathematics, Physics, Business Administration).
  * **Academic Level:** Dropdown selection (`100 Level`, `200 Level`, `300 Level`, `400 Level`, `500 Level`, `Postgraduate`).
  * **Age:** Integer input (optional/nullable).
* Upon form submission, update the `StudentProfile` record in SQLite and flash a success banner: *"Your academic profile has been successfully updated!"*

### 3.2 User Account & Security Settings
* Provide editable fields for standard Django User attributes:
  * **Username:** Read-only (display only for identity verification).
  * **Email Address:** Editable text field.
* Provide a direct link / action trigger for password modification.

### 3.3 Application Preferences (UI Toggles)
* Include visual toggle switches for application settings:
  * **Email Notifications:** Toggle for receiving weekly AI recommendation digests.
  * **Study Reminders:** Toggle for browser activity reminder alerts.
  * **Interface Theme:** Selector for Dark Mode / Light Mode styling preference.

---

## 4. Technical Architecture & Files Affected

### 4.1 Django Forms Definition
1. **`accounts/forms.py` [MODIFY]**
   * Create `StudentProfileUpdateForm(forms.ModelForm)` bound to `StudentProfile` (fields: `department`, `level`, `age`).
   * Create `UserUpdateForm(forms.ModelForm)` bound to `User` (fields: `email`).
   * Add Bootstrap form classes (`form-control`, `form-select`) to form widget attributes.

### 4.2 Backend View & Routing
2. **`accounts/views.py` [MODIFY]**
   * Implement `@login_required` view `settings_view(request)`.
   * Handle `GET` (instantiate forms with current user/profile instances) and `POST` (validate forms, save updates, and attach `messages.success`).

3. **`accounts/urls.py` [MODIFY]**
   * Add URL pattern: `path("settings/", settings_view, name="settings")`.

### 4.3 Frontend Template & Navigation
4. **`templates/accounts/settings.html` [NEW]**
   * Extend `base.html`.
   * Design a multi-card layout with clear section headers (`<i class="fa-solid fa-user-gear"></i> Academic Profile`, `<i class="fa-solid fa-shield-halved"></i> Security`, `<i class="fa-solid fa-sliders"></i> Preferences`).
   * Style input fields, select dropdowns, and submit buttons using global design system variables (`--primary`, `--radius`, `--shadow`).

5. **`templates/partials/sidebar.html` [MODIFY]**
   * Update line 67 from `href="#"` to `href="{% url 'settings' %}"`.
   * Apply conditional class `{% if '/accounts/settings' in request.path %}active{% endif %}`.

---

## 5. Step-by-Step Execution Plan (One-File Workflow)

* **Step 1:** Modify `accounts/forms.py` to add `StudentProfileUpdateForm` and `UserUpdateForm`. Test for import errors.
* **Step 2:** Modify `accounts/views.py` to implement `settings_view` handling form rendering and saving. Test server stability.
* **Step 3:** Modify `accounts/urls.py` to register the `/settings/` route.
* **Step 4:** Create `templates/accounts/settings.html` with styled form inputs and preference toggles.
* **Step 5:** Modify `templates/partials/sidebar.html` to activate the "Settings" sidebar link.
* **Step 6:** Manual browser test: change department from "Computer Science" to "Mathematics", save, and verify update persists on both Profile and Settings pages.

---

## 6. Definition of Done
* [ ] Visiting `/accounts/settings/` displays the student's current department, academic level, and email populated in form inputs.
* [ ] Submitting profile updates successfully saves to the database and displays a confirmation alert.
* [ ] Updated attributes immediately reflect on the "My Profile" tab.
* [ ] Sidebar "Settings" link routes correctly and highlights when active.
* [ ] Zero database schema modifications or backend regressions introduced.
