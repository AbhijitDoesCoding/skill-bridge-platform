# Hackathon Challenge: AI-Adaptive Onboarding Engine

---

## 1. Problem Statement
[cite_start]Current corporate onboarding often utilizes static, "one-size-fits-all" curricula, resulting in significant inefficiencies[cite: 3]. [cite_start]Experienced hires waste time on known concepts, while beginners may be overwhelmed by advanced modules[cite: 4].

[cite_start]**The Challenge:** Build an AI-driven, adaptive learning engine that parses a new hire's current capabilities (via resume or diagnostic) and dynamically maps an optimized, personalized training pathway to reach role-specific competency[cite: 5].

---

## 2. Minimum Required Features
To be eligible for judging, your solution must demonstrate:
* [cite_start]**Intelligent Parsing:** Extraction of skills and experience levels from a Resume and a target Job Description[cite: 9].
* [cite_start]**Dynamic Mapping:** Generation of a personalized learning pathway that addresses the specific "skill gap" identified[cite: 10].
* [cite_start]**Functional Interface:** A minimal web-based UI allowing users to upload documents (Resume/JD) and visualize their custom training roadmap[cite: 11].

---

## 3. Submission Requirements
All participating teams must provide the following three deliverables:

### A. Public GitHub Repository
* [cite_start]**Source Code:** Fully documented and reproducible code[cite: 15].
* [cite_start]**README.md:** Must include setup instructions, a list of dependencies, and a high-level overview of the logic used for skill-gap analysis[cite: 17].
* [cite_start]**Dockerization:** A Dockerfile to ensure judges can run your environment seamlessly (optional but encouraged)[cite: 18].

### B. Video Demonstration
* [cite_start]**Duration:** 2-3 minutes[cite: 20].
* [cite_start]**Content:** A concise walkthrough of the end-to-end user journey, showcasing the UI and how the pathway adapts to different inputs[cite: 21].

### C. Technical Presentation (The "5-Slide Deck")
[cite_start]Your presentation must be strictly limited to 5 slides using the following structure[cite: 23]:
1.  [cite_start]**Solution Overview:** Value proposition and specific problem-solving approach[cite: 24].
2.  [cite_start]**Architecture & Workflow:** System design, data flow, and UI/UX logic[cite: 25].
3.  [cite_start]**Tech Stack & Models:** Detailed list of LLMs, embedding models, and frameworks used[cite: 26].
4.  [cite_start]**Algorithms & Training:** Deep dive into skill-extraction logic and the "Adaptive Pathing" algorithm (e.g., Graph-based or Knowledge Tracing)[cite: 27].
5.  [cite_start]**Datasets & Metrics:** Disclosure of all public datasets and internal metrics used to validate efficiency[cite: 28, 29].

---

## 4. Data & Model Compliance
* [cite_start]**Transparency:** Use of public datasets (e.g., O*NET, LinkedIn Skills, Kaggle) is permitted, but all datasets and open-source models (e.g., Llama 3, BERT, Mistral) must be explicitly cited[cite: 36, 37].
* [cite_start]**Originality:** While pre-trained models are encouraged, the **"Adaptive Logic"** (how the system decides what to teach next) must be your original implementation[cite: 38].

---

## 5. Evaluation Criteria
| Criteria | Weight | Description |
| :--- | :--- | :--- |
| **Technical Sophistication** | 20% | [cite_start]Accuracy of skill-extraction and complexity of the recommendation model[cite: 40]. |
| **Grounding & Reliability** | 15% | [cite_start]Zero hallucinations; strict adherence to the provided course catalog[cite: 41]. |
| **Reasoning Trace** | 10% | [cite_start]Provision of a reasoning trace feature[cite: 42]. |
| **Product Impact** | 10% | [cite_start]Effectiveness in reducing redundant training time[cite: 43]. |
| **User Experience** | 15% | [cite_start]Clarity of the learning pathway and functional usability of the UI[cite: 44]. |
| **Cross-Domain Scalability** | 10% | [cite_start]Ability to generalize across diverse job categories[cite: 45]. |
| **Communication & Docs** | 20% | [cite_start]Quality and polish of the GitHub Readme, Demo Video, and Presentation[cite: 47]. |

> [cite_start]**Note:** Exceptional technical solutions must be matched by clear communication; a high-quality presentation and well-documented repository are essential for a winning submission[cite: 48, 49].
