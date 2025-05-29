# SankalpiQ – Building Tomorrow, Today

## Overview

**SankalpiQ** is a modular, AI-powered multi-agent system designed to assist NGOs in streamlining their outreach, onboarding, data collection, and volunteer engagement operations. The system leverages language models, automation frameworks, and communication APIs to create a fully autonomous support infrastructure that reduces manual workload and improves impact efficiency.

---

## Problem Statement

Non-Governmental Organizations (NGOs) often operate with limited resources and heavy manual workloads, particularly in areas like:

- Volunteer onboarding
- Blood donation campaigns
- Event response coordination
- Public outreach
- Certification and communication

Manual operations result in delays, data inconsistencies, and increased operational costs. There is a critical need for an automated, intelligent system to streamline these workflows across languages and regions.

---

## Solution

**SankalpiQ** orchestrates multiple AI agents to automate:

- Voice-based onboarding and information capture
- Real-time WhatsApp and email-based communication
- Dynamic certificate generation
- Multilingual conversational assistance
- Emergency detection and campaign triggering via news scraping

This system helps NGOs better manage their volunteer base, improve donor relationships, and respond faster to public needs.

---

## Use Case Example: Blood Donation Drive

**Scenario:** A college student, Aakash, sees an NGO helpline poster and decides to register as a donor.

**Flow:**

1. Aakash calls the NGO number.
2. The **Info Calling Agent** collects his details (name, blood group, email).
3. Aakash asks questions about the NGO and next camp date, answered by the **LLM Agent**.
4. A confirmation message is sent via the **WhatsApp Agent**.
5. The **Email Agent** sends onboarding details and donation guidance.
6. A **Certificate Agent** automatically sends a digital volunteer certificate.
7. In the future, if a news article reports a local emergency, the **Scraper Agent** triggers a broadcast to all nearby donors.

---

## Multi-Agent System Architecture

| Module                  | Agent Used            | Functionality                                          |
|-------------------------|------------------------|--------------------------------------------------------|
| Data Collection         | Info Calling Agent     | Voice-based volunteer registration                     |
| Query Resolution        | LLM Agent              | Multilingual answers to NGO-related questions          |
| Confirmation Messaging  | WhatsApp Agent         | Real-time follow-ups and reminders                     |
| Email Communication     | Cold Email Agent       | Onboarding, updates, and campaign details              |
| Certificate Generation  | Certificate Agent      | Auto-generates volunteer/donor certificates            |
| Campaign Outreach       | Purpose-Based Agent    | Bulk messaging and event reminders                     |
| Event Monitoring        | Scraper Agent          | News-driven campaign automation                        |
| Donations Management    | Donation Agent         | Voice-based donation facilitation and information      |

---

## Project Modules

### 1. Info Calling Agent
- Collects user information via phone
- Multilingual support (Hindi/English)
- Data saved in Google Sheets or database

### 2. LLM Calling Agent
- Answers general queries about the NGO and its services
- Supports Hindi and English
- Uses Gemini 1.5 or GPT-3.5

### 3. WhatsApp Automation Agent
- Sends personalized messages post-call
- Reminders and campaign invites

### 4. Cold Email Agent
- Sends onboarding and campaign summary emails
- Segmented email targeting (volunteers, donors)

### 5. Certificate Agent
- Auto-generates participation and onboarding certificates
- Delivers via WhatsApp and email

### 6. Donation Agent
- Handles donation pledges and information via voice
- Sends UPI/bank details and confirmation messages

### 7. Scraper Agent
- Scrapes real-time local news for emergencies or events
- Triggers workflows or broadcast messages accordingly

---

## Metrics for Success

| Metric                         | Target                         |
|-------------------------------|--------------------------------|
| Average Response Time         | < 5 seconds                    |
| Registration Accuracy         | > 95%                          |
| WhatsApp Message Open Rate    | > 80%                          |
| Email Open Rate               | > 40%                          |
| Certificate Delivery Rate     | 100%                           |
| Volunteer Retention Increase  | 2x within 30 days              |
| Emergency Response Trigger    | Within 10 minutes of detection |

---

## Real-World Relevance

A 2021 report during the COVID-19 pandemic highlighted major delays in NGO responses due to manual data collection and communication gaps. SankalpiQ addresses these limitations with intelligent automation, ensuring faster and more reliable outreach and support during critical times.

---

## Tech Stack



