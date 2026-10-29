# Atlas: Chief of Staff Webpage Concept

> Working draft. Add ideas anywhere; delete what doesn't fit.

## 1. Vision

**One-line pitch:**
Atlas, my chief of staff (COS), keeps me on track through my VR training work, logs what I do each day, and asks me questions so it always knows where I am in the pipeline.

**Core idea:**
- Task pipeline for building VR training experiences in Unity
- The COS keeps me on track and keeps a running note of what I'm doing throughout the day
- The COS prompts me with questions to work out where I am in the pipeline

## 2. Audience

- **Primary user:** Me, working on VR training experiences in Unity
- **Secondary users:**
- **What they're trying to get done:** Stay on track, keep a record of the day, always know the current pipeline stage
- **Biggest struggle:** Getting pulled between tasks

## 3. Goals

| Goal | Why it matters | How we'll know it works |
|------|----------------|--------------------------|
| Stay on track | I get pulled between tasks | |
| Daily activity log | | |
| Know where I am in the pipeline | | |
| Understand where I am in the project each week | | |

## 4. Core Features

- [ ] **Task pipeline:** each task moves through brief, design, build, test, review and push; lots of tasks in Unity build
- [ ] **Daily log:** running notes of what I'm working on through the day
- [ ] **Check-in prompts:** COS asks questions to understand my current pipeline position
- [ ] **Stay-on-track nudges:** keeps me focused on the current stage, and helps when I get pulled onto something else

- [ ] **Weekly reflection:** at the end of each week, Atlas gives me a digest plus a reflection questionnaire (see section 7)

### Feature notes
_Expand on any feature here._

## 5. Pipeline Stages

Every task follows the full pipeline:

1. Brief
2. Design
3. Build
4. Test
5. Review
6. Push

**Notes:**
- Most of my work is in the Unity build stage, so I'll be adding many tasks there compared to the other stages
- Each task has its own stage, so many tasks can sit in build at once

## 6. COS Check-ins

**When it checks in:**
- At set times: morning, midday, end of day
- Whenever I change task or stage
- After long gaps with no updates

**Tone:** Firm but friendly

**What it should ask:**

- "What are you working on right now?"
- "Which stage is this task in?"
- "Anything blocked?"
-

## 7. Weekly Reflection

At the end of each week Atlas gives me:

1. **A digest** of the topics and tasks I covered and completed that week
2. **A reflection questionnaire** I answer to get a grasp on where I am in the project and what I need to work on next

**How Atlas uses my answers:**
- Prompts me on next tasks
- Keeps me on track in the following week

**Questionnaire questions:**
_What should it ask?_

-
-
-

**Digest contents:**
-

**Open details:**
- Which day and time does the weekly reflection arrive?
- Where do I answer it, and where are past reflections kept?

## 8. Page Structure

1. **Hero / header:**
2. **Main content:**
3. **Secondary sections:**
4. **Footer / contact:**

## 9. Content

- **Key messages:**
- **Tone and voice:** Atlas is firm but friendly
- **Copy ideas:**

## 10. Look and Feel

- **Style direction:**
- **Colors / typography:**
- **References and inspiration:**

## 11. Open Questions

- What are the real stages of the pipeline?
- What exactly are the set check-in times?
- How long a gap counts as "long" before it prompts me?
- What usually pulls me between tasks?
- How do I review the daily log?

## 12. Raw Ideas

-
-
-

## 13. Build Decisions

- **Where I use it:** Browser on my computer
- **How Atlas learns what I'm doing:** A mix of me typing quick updates, Atlas asking me questions, and pulling from my tools (calendar, Git, etc.)
- **Where data is stored:** Only on my own device (logs, reflections, digests)
- **Model:** Probably a cloud API (agent options to research: Hermes, OpenClaw, others)

**To decide:**
- Which tools does Atlas pull from?
- What text gets sent to the cloud API for prompts and digests, and what stays on my device?
- Which agent or framework do I use? (Research Hermes, OpenClaw, others)

## 14. Next Steps

- [ ]
- [ ]
