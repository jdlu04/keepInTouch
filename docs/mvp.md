# Keep in Touch (KiT) MVP

## Table of Contents

1. [Overview](#overview)
2. [Problem Statement](#problem-statement)
3. [Solution](#solution)
4. [Goals](#goals)
5. [Non-Goals](#non-goals)
6. [Target Users](#target-users)
7. [Team](#team)
8. [Tech Stack](#tech-stack)
9. [Core Features](#core-features)
10. [Application Sitemap](#application-sitemap)
11. [Core User Flow](#core-user-flow)
12. [Database Design](#database-design)
13. [Development Timeline](#development-timeline)
14. [Competitive Analysis](#competitive-analysis)

---

# Overview

**Keep in Touch (KiT)** is a relationship management application designed to help users maintain meaningful connections with friends, family, classmates, mentors, coworkers, and professional contacts.

Unlike traditional contact applications that only store basic information, KiT focuses on actively maintaining relationships through:

- Visual relationship mapping
- Interaction tracking
- Relationship strength measurement
- Personalized reminders

The goal of KiT is to help users understand their social network, remember important details about people, and build stronger relationships over time.

---

# Problem Statement

Maintaining relationships requires effort, but people often lose touch with important connections due to busy schedules, distance, and the lack of a centralized system for managing personal relationships.

Current solutions have several limitations:

- Contact applications only store basic information such as names and phone numbers.
- Calendar apps provide reminders but lack relationship context.
- Professional CRMs are focused on sales, customers, and business workflows.
- Existing personal CRM tools often resemble spreadsheets or databases rather than meaningful relationship tools.

People need a way to organize, visualize, and maintain relationships beyond simply storing contact information.

---

# Solution

Keep in Touch provides a people-focused relationship management experience through a visual relationship map.

The application allows users to:

- Visualize their network of relationships through interactive nodes and connections.
- Store important details about contacts.
- Track previous interactions and conversations.
- Measure relationship strength based on engagement.
- Receive reminders for important moments and follow-ups.

By combining contact management with relationship intelligence, KiT helps users be more intentional about maintaining connections.

---

# Goals

## MVP Goals

The MVP will focus on building the foundation of relationship management.

Key goals include:

- Create and manage personal contacts.
- Visualize relationships through an interactive relationship map.
- Allow users to log interactions with contacts.
- Track relationship strength based on activity.
- Provide reminders for important dates and follow-ups.
- Create an intuitive mobile-first experience.

---

# Non-Goals

The MVP will intentionally exclude features that require additional complexity:

- AI-generated conversation starters.
- Automated social media syncing.
- Calendar integrations.
- Messaging functionality.
- Group collaboration features.
- Advanced analytics and relationship insights.
- Business sales pipeline features.

These features may be considered for future versions.

---

# Target Users

Keep in Touch is designed for individuals who want to intentionally maintain their relationships.

Potential users include:

- Students managing friendships and academic connections.
- Recent graduates maintaining alumni networks.
- Professionals staying connected with mentors and coworkers.
- Individuals managing long-distance friendships and family relationships.
- Community members maintaining meaningful connections.

Unlike traditional CRM users, KiT users are not managing customers. They are managing relationships.

---

# Team

We are Computer Science students and recent graduates from **The City College of New York (CUNY).**

| Name | Role |
|------|------|
| Sehr Abrar | Backend Engineer |
| Nirath Hussan | Frontend Engineer / UI Designer |
| Judy Liu | Backend Engineer / UI Designer |
| Lily Minchala | Frontend Engineer / UI Designer |

---

# Tech Stack

| Layer | Technology | Purpose |
|------|------------|---------|
| Frontend | React Native (Expo) | Cross-platform app (web + iOS + Android) |
| Backend / API | FastAPI (Python) | REST API and **all business logic** — auth, relationship scoring, reminders |
| Database | PostgreSQL (hosted on Supabase) | Data storage; Supabase is used only as a managed Postgres host |
| ORM / Migrations | SQLAlchemy + Alembic | Schema defined in Python; versioned migrations |
| Authentication | FastAPI + JWT (email + password) | Passwords hashed with bcrypt; JWT access tokens issued on login |
| Version Control | Git & GitHub | Collaboration and source control |

> **On the backend:** the app talks to a **FastAPI (Python)** server over HTTP.
> FastAPI owns all business logic and authentication and is the only thing that
> touches the database. PostgreSQL is hosted on Supabase, but only as a managed
> database — Supabase's auto-generated API, Row-Level Security, and Auth are
> **not** used. This keeps the logic in our own Python code and works the same
> for web and native (both just make HTTP calls to the API).

---

# Core Features

## Home: Relationship Map

The Home page serves as the main visualization of the user's network.

Contacts are represented as nodes, while relationships between contacts are represented as edges.

### Features

- Interactive relationship graph.
- View connections between contacts.
- Visualize relationship strength.
- Add new contacts.
- View contact details by selecting a node.
- Relationship strength legend.

### Relationship Visualization

The relationship map uses visual indicators:

- **Nodes:** represent individuals.
- **Edges:** represent relationships between individuals.
- **Node size:** represents relationship strength.
- **Colors:** represent relationship categories.

---

# Contacts

The Contacts page provides a centralized directory for managing relationships.

### Features

- View all contacts.
- Search contacts.
- Filter contacts by category.
- Favorite important contacts.
- Edit contact information.
- Delete contacts.

---

# Contact Profile

Each contact has a detailed profile containing relationship information.

## Overview

Stores important personal details:

- Name.
- Location.
- Relationship type.
- Phone number.
- Email.
- Social media.
- Important dates.

## Timeline

Tracks previous interactions:

- Calls.
- Messages.
- Meetings.
- Events.
- Notes from conversations.

## Notes

Allows users to store important information:

- Personal preferences.
- Interests.
- Memories.
- Important details.

## Connections

Displays related relationships:

- Shared connections.
- Relationship category.
- Connection strength.

---

# Add Contact

Users can create new contacts by entering:

- Name.
- Location.
- Relationship category.
- Contact information.
- Birthday.
- Anniversary.
- Important dates.
- Reminder preferences.
- Relationship color category.

---

# Reminders

The Reminders page helps users maintain relationships proactively.

### Features

- Upcoming reminders.
- Due today reminders.
- Birthday reminders.
- Anniversary reminders.
- Follow-up reminders.
- Gift reminders.
- Completed reminders.
- Notification preferences.

---

# Settings

The Settings page manages user preferences.

### Features

## Reminder Preferences

- Enable or disable reminders.
- Customize notification settings.

## Relationship Categories

Users can organize relationships using categories such as:

- Family.
- Friends.
- Classmates.
- Coworkers.
- Mentors.

## Account Settings

- Manage profile information.
- Update application preferences.

---

# Application Sitemap

```text
Keep in Touch
│
├── Home
│   ├── Relationship Map
│   ├── Connection Details
│   └── Add Contact
│
├── Contacts
│   ├── Contact Directory
│   ├── Search & Filter
│   └── Contact Profile
│       ├── Overview
│       ├── Timeline
│       ├── Notes
│       ├── Connections
│       └── Reminders
│
├── Reminders
│   ├── Due Today
│   ├── Upcoming Check-ins
│   ├── Birthdays & Milestones
│   └── Completed Reminders
│
└── Settings
    ├── Reminder Preferences
    ├── Relationship Categories
    ├── Notification Settings
    └── Account Settings
```

---

# Core User Flow

```text
User Opens App
        │
        ▼
Relationship Map Homepage
        │
        ├───────────────┐
        ▼               ▼
   Add Contact      Select Contact
        │               │
        ▼               ▼
 Save Contact     View Profile
                        │
                        ▼
                Log Interaction
                        │
                        ▼
          Update Relationship Strength
                        │
                        ▼
             Generate Reminders
```

---

# Database Design

## Contact

Stores user contact information.

| Field | Description |
|------|-------------|
| id | Unique contact identifier |
| name | Contact name |
| relationship | Relationship category |
| location | Contact location |
| phone | Phone number |
| email | Email address |
| socialMedia | Social media links |
| squadColor | Visual grouping color |

---

## Interaction

Stores relationship history.

| Field | Description |
|------|-------------|
| id | Unique interaction identifier |
| contactId | Associated contact |
| type | Interaction type |
| date | Date of interaction |
| notes | Interaction details |

---

## Reminder

Stores upcoming relationship events.

| Field | Description |
|------|-------------|
| id | Unique reminder identifier |
| contactId | Associated contact |
| title | Reminder description |
| dueDate | Reminder date |
| completed | Completion status |

---

## Relationship Connection

Stores relationships between contacts.

| Field | Description |
|------|-------------|
| sourceContact | Starting contact |
| destinationContact | Connected contact |
| relationshipType | Connection type |
| strength | Relationship score |

---

# Development Timeline

| Week | Dates | Focus | Deliverables |
|------|-------|-------|--------------|
| Week 1 | June 17 - June 23 | Ideation & Problem Definition | Define problem, identify users, research competitors, establish relationship strength concept |
| Week 2 | June 24 - June 30 | Product Planning | Finalize sitemap, user flows, MVP scope, high-fidelity mockups, backend research |
| Week 3 | July 1 - July 7 | UI Design & Architecture | Complete UI designs, relationship map design, database schema |
| Week 4 | July 8 - July 14 | Backend & Frontend Setup | Initialize React Native, FastAPI, Supabase, navigation, static screens |
| Week 5 | July 15 - July 21 | Core Feature Development | Contact management, interaction logging, profiles, relationship logic |
| Week 6 | July 22 - July 28 | Relationship Map & Reminders | Build graph visualization, reminders system, backend integration |
| Week 7 | July 29 - August 4 | Optimization & UX Polish | Improve UX, refine relationship scoring, fix bugs, optimize performance |
| Week 8 | August 5 | Testing & Demo Preparation | End-to-end testing, final polish, product walkthrough |

---

# Competitive Analysis

| Product | Focus | Limitations |
|--------|-------|-------------|
| Dex | Personal CRM | Limited visualization and relationship mapping |
| Mesh | Personal CRM | Primarily document-based organization |
| Monica | Personal CRM | Limited free features and complex interface |
| Folk | Professional CRM | Designed for networking and business workflows |
| Attio | Business CRM | Focused on sales and company relationships |

## Differentiation

Most existing CRM products are designed around business relationships, sales pipelines, and customer management.

Keep in Touch focuses on **personal relationship maintenance** by providing:

- A visual relationship map.
- Relationship strength tracking.
- Interaction history.
- Personalized reminders.
- A people-first CRM experience.

KiT is designed to help users stay connected with the people who matter most.