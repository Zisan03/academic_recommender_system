# Product Requirements Document (PRD)

# SmartLearn AI – Hybrid Machine Learning Academic Recommendation System

**Version:** 1.0
**Project Status:** Active Development
**Development Methodology:** Incremental (One File at a Time)
**Framework:** Django + Python + Hybrid Machine Learning

---

# 1. Project Overview

## Product Name

**SmartLearn AI**

## Product Vision

SmartLearn AI is an intelligent academic recommendation platform that provides personalized learning resources to students using a Hybrid Machine Learning recommendation engine combined with Explainable AI (XAI). The system aims to improve learning outcomes by recommending relevant academic materials based on students' profiles, learning behavior, and interaction history.

---

# 2. Project Objectives

### Primary Objectives

* Develop a web-based academic recommendation platform using Django.
* Integrate a Hybrid Machine Learning recommendation engine.
* Deliver personalized learning resources.
* Provide Explainable AI (SHAP) to justify recommendations.
* Offer a modern, user-friendly dashboard for students.

### Secondary Objectives

* Track learning activities.
* Analyze student progress.
* Provide resource management.
* Support future scalability for administrators and institutions.

---

# 3. Technology Stack

## Backend

* Python 3.13
* Django
* SQLite (Development)
* PostgreSQL/MySQL (Production)

## Machine Learning

* Scikit-learn
* Pandas
* NumPy
* Surprise (Collaborative Filtering)
* XGBoost
* SHAP

## Frontend

* HTML5
* CSS3
* Bootstrap 5
* JavaScript
* Font Awesome
* Google Fonts (Poppins)

---

# 4. Development Rules

## Rule 1 — One File at a Time

Only one file will be modified during each development iteration.

### Workflow

1. Generate one complete file.
2. Replace the existing file.
3. Run the Django server.
4. Test the affected feature.
5. Confirm functionality.
6. Proceed to the next file.

**No multiple-file changes in a single iteration.**

---

## Rule 2 — Protect Stable Features

Working features must remain untouched unless a confirmed blocking issue requires modification.

The following components are considered stable:

* Recommendation Engine
* Machine Learning Models
* Database Models
* Dataset Import Pipeline

---

## Rule 3 — Test After Every Change

Every file replacement must be validated.

### Command

```bash
python manage.py runserver
```

Testing should include:

* Visual inspection
* Browser console
* Django terminal logs
* CSS rendering
* Navigation
* Feature functionality

Development proceeds only after successful validation.

---

## Rule 4 — Backend Stability

The backend architecture is locked.

The following are **not** to be modified unless absolutely necessary:

* Recommendation algorithms
* Machine Learning pipeline
* Database schema
* Model relationships
* Dataset loading
* Recommendation calculations

Development efforts should focus on integration and user interface enhancements.

---

## Rule 5 — Feature Completion Before Polish

Development priority is:

1. Functionality
2. Integration
3. User Experience
4. Visual Polish

No redesigns before functional completion.

---

# 5. Product Modules

## Core Modules

### Authentication

Status: ✅ Complete

Features:

* Login
* Logout
* Registration
* User sessions

---

### Student Profile

Status: ✅ Complete

Features:

* Personal information
* Department
* Academic level
* Learning interests

---

### Recommendation Engine

Status: ✅ Complete

Features:

* Content-Based Filtering
* Collaborative Filtering
* Hybrid recommendation scoring
* AI confidence score

---

### Resource Database

Status: ✅ Complete

Features:

* Resource storage
* Categories
* Metadata
* Search support

---

### Recommendation Dashboard

Status: In Progress

Features:

* Personalized recommendations
* Weak topic detection
* AI confidence
* Learning insights

---

# 6. Development Roadmap

## Phase 1 — Backend

**Status:** Complete

Completed components:

* Django setup
* Authentication
* Student profile
* Recommendation engine
* Dataset import
* Resource database
* Recommendation API
* Recommendation dashboard backend

---

## Phase 2 — Frontend Integration

**Status:** In Progress

### Base Layout

Status: Complete

Components:

* Base template
* Navigation bar
* Sidebar
* Footer
* Global styling

---

### Dashboard

Status: Current Sprint

Objectives:

* Integrate dashboard with base layout
* Apply dashboard styling
* Resolve CSS issues
* Improve responsiveness

---

### Resources Module

Status: Pending

Planned features:

* Resource list
* Resource details
* Download functionality
* External links
* Search and filtering

---

### Profile Module

Status: Pending

Planned features:

* Student information
* Learning statistics
* Recommendation history
* Saved resources

---

### Learning Activity

Status: Pending

Planned features:

* Activity timeline
* Recently viewed resources
* Study history
* Progress tracking

---

### Settings

Status: Pending

Planned features:

* Profile updates
* Password management
* Theme preferences
* Notification settings

---

## Phase 3 — Explainable AI

Status: Pending

Features:

* Recommendation explanations
* SHAP visualizations
* Confidence indicators
* Similar student insights
* Recommendation reasoning

---

## Phase 4 — Analytics

Status: Pending

Features:

* Learning progress charts
* Weak topic analysis
* Resource usage statistics
* Recommendation performance
* AI accuracy metrics

---

## Phase 5 — Administration

Status: Pending

Features:

* Resource management
* Student management
* Dataset updates
* Model retraining
* System monitoring
* Activity logs

---

## Phase 6 — UI Polish

Status: Pending

Tasks:

* Responsive optimization
* Animations
* Consistent typography
* Color refinement
* Accessibility improvements
* Performance optimization

---

## Phase 7 — Documentation

Status: Pending

Deliverables:

* Chapter Four
* Chapter Five
* User manual
* Installation guide
* Deployment guide
* GitHub repository cleanup
* System screenshots

---

# 7. Current Sprint

## Sprint 2.2 — Dashboard Refactoring

### Objective

Ensure the recommendation dashboard integrates seamlessly with the new application layout and styling system.

### Current Tasks

* Fix dashboard layout
* Verify CSS loading
* Validate template inheritance
* Ensure responsive rendering
* Connect dashboard to global design system

### Investigation Focus

Potential causes of styling issues:

* `base.html`
* `dashboard.css`
* `base.css`
* Missing Bootstrap
* Incorrect CSS selectors
* Static file configuration
* Template inheritance

---

# 8. Development Workflow

Every task follows this sequence:

1. Select one target file.
2. Review the existing implementation.
3. Identify the root cause of any issue.
4. Generate a complete replacement for that file.
5. Replace the file in the project.
6. Run the development server.
7. Test the affected functionality.
8. If successful, mark the task complete and proceed to the next file.

No parallel modifications are permitted.

---

# 9. Definition of Done

A feature is considered complete only when:

* Functionality works as intended.
* No backend regressions are introduced.
* Styling is correctly applied.
* Responsive behavior is verified.
* Django server reports no errors.
* Browser console is free of critical issues.
* The feature integrates cleanly with the existing application.

---

# 10. Current Project Status

| Phase                | Status         | Progress |
| -------------------- | -------------- | -------- |
| Backend Development  | ✅ Complete     | 100%     |
| Frontend Integration | 🔄 In Progress | ~60%     |
| Explainable AI       | ⏳ Pending      | 0%       |
| Analytics            | ⏳ Pending      | 0%       |
| Administration       | ⏳ Pending      | 0%       |
| UI Polish            | ⏳ Pending      | 0%       |
| Documentation        | ⏳ Pending      | 0%       |

---

# 11. Immediate Next Action

**Current Sprint:** Dashboard Refactoring

**Next File:** `static/css/dashboard.css`

The immediate objective is to verify that the dashboard-specific styles are correctly loaded and applied. Once the dashboard is stable and validated, the sprint will be closed and development will proceed to the **Resources Module** following the one-file-at-a-time workflow.
