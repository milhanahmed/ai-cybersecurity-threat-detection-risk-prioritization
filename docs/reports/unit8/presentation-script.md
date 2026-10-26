# Capstone Presentation Script
AI Assisted Cybersecurity Threat Detection and Risk Prioritization
Milhan Ahmed Mustafa
MSIT 5910 Unit 8

## Rehearsal and delivery plan
Use 14 slides, including the title, overview, summary, and references. The target is approximately 13 minutes, including deliberate pauses and the live demonstration. Speak the narration only; the screen directions and setup notes are not spoken. Rehearse once with a timer and aim to finish between 12 and 14 minutes. Keep your face visible when introducing the problem and closing. Look toward the camera after explaining each visual, and use the pointer only to identify the component or result being discussed. The script accompanies the final report and the delivered local source revision. It does not describe the public baseline as already updated.

## Slide 1 Title 0:00 to 0:30
Screen direction: Show the project title, your name, course, university, and supervisor. Face the camera and pause briefly before beginning.

Good day, Dr. Sirisha and everyone reviewing this presentation. I am Milhan Ahmed Mustafa, and my capstone is an AI-assisted cybersecurity threat detection and risk prioritization prototype for small and medium-sized organizations. I will explain the problem, demonstrate the working application, show the corrections made after Week 7, and discuss what the evaluation does and does not establish.

## Slide 2 Overview and abstract 0:30 to 1:10
Screen direction: Show the workflow and three findings: integrated prototype, corrected input and access checks, unresolved real-world model validity.

The project combines structured event input, machine-learning classification, explainable priority scoring, persistent storage, and a browser dashboard. The final local revision addresses the six validation and access failures identified during Week 7. All thirty-three final software tests pass, and the browser workflow works with configured analyst credentials. However, independent benchmark evaluation reveals that software correctness is different from detection quality. The application is a controlled academic demonstration; it is not ready to make operational security decisions using real organizational data.

## Slide 3 Problem objectives and scope 1:10 to 2:00
Screen direction: Show the problem and three objectives: integrate the pipeline, verify behavior, communicate limitations.

The business problem is deciding which security events deserve investigation when analyst time is limited. My objective was to build a traceable pathway from a structured event to a stored investigation priority. The prototype accepts a small supported event vocabulary and considers severity and business impact alongside model output. It supports human investigation rather than automatically blocking a user or device. The scope includes implementation, regression testing, local performance measurement, and a maintenance plan. Live telemetry connectors, representative analyst acceptance, and production deployment are outside the completed scope. This boundary prevents a successful demonstration from being mistaken for a validated operational detector.

## Slide 4 Architecture and methodology 2:00 to 2:55
Screen direction: Show Figure 3.2 from the final report. Trace the sequence from the dashboard to authentication, validation, model, scoring, and database.

FastAPI coordinates the processing sequence. A protected request first passes the analyst credential dependency and the request model. Accepted values are normalized, four classifier features are constructed, and logistic regression returns a label and confidence. A separate scoring function computes priority, then SQLite stores the result. The dashboard refreshes authenticated history after a successful analysis. Each responsibility is kept in a separate module. This structure helped locate the Week 7 gaps and test corrections without rewriting the classifier. The health endpoint remains public and reveals only basic availability. The architecture diagram describes the delivered local revision, while the report retains earlier milestone evidence for comparison.

## Slide 5 Algorithms and design choices 2:55 to 3:50
Screen direction: Show the risk-scoring code and the request-validation snippet. Cite the report sources in a small footer.

The classifier uses DictVectorizer and logistic regression trained on six synthetic examples. This is a small baseline, not a newly developed intrusion-detection algorithm. The risk function assigns forty percent to severity, thirty percent to confidence, and thirty percent to business impact. Scores below fifty are Low, scores from fifty to below seventy-five are Medium, and scores of seventy-five or more are High. A limitation is that confidence refers to the winning class, even when that class is benign. I have preserved that policy in this revision and documented why it needs independent validation. The final request model now checks domain values instead of trusting browser controls alone.

## Slide 6 Demonstration setup 3:50 to 4:50
Screen direction: Switch to the running application at a clean localhost address. Show the environment summary, not secret values. Keep the terminal ready with the test command.

For this demonstration, I am using the delivered local Python application with FastAPI, scikit-learn, and SQLite. The evidence run used Python three point twelve. Analyst credentials are configured through environment variables, and I do not display the password. The application rejects access when credentials are missing or incorrect, and it fails closed when configuration is absent. The browser is connected to localhost using synthetic data. HTTP Basic authentication here is a demonstration control; an external deployment would require HTTPS and stronger identity management. I have already started the application and signed in so that we can focus on the main workflow.

## Slide 7 Demonstration of valid analysis 4:50 to 5:45
Screen direction: Enter a fresh event identifier. Use login_failure, eight failed attempts, known bad IP one, privilege one, severity 0.9, impact 0.8. Click Analyze and point to output and history. Allow about 20 seconds for these actions.

I will submit a suspicious login example. The result is suspicious classification with confidence zero point nine one four one, a risk score of eighty-seven point four two, and High priority. The same identifier appears in the history table, demonstrating that the request passed through the interface, backend, classifier, scoring module, and database. This is genuine application output. The result is useful as an integration example, but one plausible classification does not establish real-world detection accuracy. The next part of the demonstration shows what happens when the input does not meet the contract.

## Slide 8 Demonstration of validation and access control 5:45 to 6:50
Screen direction: Replace the identifier with spaces and submit. Show the visible message. Then show the recorded closure-response output and authentication test result; do not expose credentials. Allow 25 seconds for the actions.

A whitespace-only identifier is now rejected by the dashboard with a clear message. The backend independently rejects invalid identifiers, timestamps, negative counts, nonbinary indicators, and unsupported categories with status four twenty-two. This protection matters because callers can bypass browser controls. Anonymous history access returns four oh one, and analysis and dashboard access are also protected. The recorded closure output connects each old failure to its new response. I am distinguishing these implemented corrections from broader security requirements: this single-account control does not yet provide role separation, multifactor authentication, or production auditability.

## Slide 9 Demonstration of safe display and tests 6:50 to 8:05
Screen direction: Submit a harmless identifier containing literal bold tags and point to the tags displayed as text. Switch to the test output showing 33 passed. Allow 25 seconds for the actions.

The history display now creates cells and assigns textContent instead of inserting event values as HTML. Here, a harmless identifier containing markup is displayed literally. The screenshot and browser observation verify that particular behavior; they do not replace a complete security assessment. The final automated run reports thirty-three passing tests and one framework deprecation warning. The suite includes the original core behavior and new validation, authentication, configuration, and display checks. Temporary database paths isolate the negative tests. The warning remains a dependency-maintenance concern. Importantly, test-suite success tells us that specified software behaviors work under these conditions; it does not measure how accurately the classifier recognizes real attacks.

## Slide 10 Stability and persistence findings 8:05 to 9:15
Screen direction: Return to the presentation. Show the final latency summary and persistence evidence, clearly labeled local TestClient measurements.

The final stability experiment sent one hundred authenticated sequential requests. Every request succeeded, and the database gained exactly one hundred records. A fresh process retrieved the last identifier, demonstrating persistence beyond the original process. Mean latency was approximately one point two seven seven milliseconds, and the nearest-rank ninety-fifth percentile was approximately one point six four five milliseconds. These measurements exclude network latency, TLS, concurrent users, and external identity systems. I therefore do not describe them as production capacity. They also do not establish backup restoration or crash recovery. Those require separate failure experiments and operational acceptance criteria.

## Slide 11 Independent model evaluation 9:15 to 10:15
Screen direction: Show Figure 5.2 and the two confusion matrices. Label the offline candidate clearly.

Independent evaluation used the legacy NSL-KDD benchmark. Because the existing event model does not accept native network features, I documented a lossy adapter and evaluated the frozen model separately. It detected only one of twelve thousand eight hundred and thirty-three attack records. That finding prevents me from generalizing the earlier synthetic success rate. A separate logistic-regression candidate used the native features, training only on the published training subset. After excluding test feature vectors that also appeared in training, it achieved about seventy-five point five six percent accuracy and sixty-two point five seven percent recall. That candidate is offline and is not the model running in this dashboard.

## Slide 12 Limitations maintenance and future work 10:15 to 11:15
Screen direction: Show three next priorities: representative data and features, operational security, and analyst evaluation.

The central remaining limitation is model validity. An independent legacy benchmark is still not representative contemporary SME telemetry, and the native candidate still missed thousands of attacks. Future work should obtain authorized representative records, define labels and feature provenance, separate training and evaluation over time, and validate decision thresholds. The scoring policy also needs review. Operational work includes managed identities, HTTPS, rate limits, audit records, backup restoration, and external load testing. The maintenance plan assigns daily monitoring, weekly issue review, monthly dependency and regression checks, and quarterly recovery exercises. Intended analysts should assess the workflow through realistic tasks before adoption.

## Slide 13 Summary and professional contribution 11:15 to 12:00
Screen direction: Show the completed pipeline, the corrected regressions, and the remaining evidence gap. Face the camera for the closing statement.

My contribution is a reproducible integration and evaluation process. The final prototype demonstrates protected input, classification, transparent scoring, persistence, and safer display. Instructor feedback led to implemented corrections and passing regressions. The independent experiment also showed why a successful prototype must not be presented as a proven detector. The innovation here is the traceable combination of analysis and organizational priority, rather than a new machine-learning algorithm. The project demonstrates my ability to investigate defects, communicate limitations, and plan maintainable improvements. Thank you for reviewing my capstone; I welcome questions about the architecture, demonstration, or evaluation boundaries.

## Slide 14 References 12:00 to 12:20
Screen direction: Display a readable reference slide using the shortened author-year citations listed below. Include clickable full references in the presentation notes or supporting report. Do not read every URL aloud.

The report provides the complete references and links for the research, frameworks, implementation guidance, and benchmark provenance used in this project. The supporting source and evidence archive enables reviewers to trace the software changes and measured results. This concludes my presentation.

## Preparation notes not presented as additional slides
Before recording, extract the supporting archive, create a virtual environment, install the requirements, configure CYBER_USERNAME and CYBER_PASSWORD in your shell, and use a fresh synthetic database. Start Uvicorn on 127.0.0.1 port 8000, visit the clean localhost address, and enter the configured credentials through the browser prompt. Do not put credentials in the URL, recording, report, or repository. Keep the regression output and closure JSON ready so the demonstration does not depend on typing long commands during recording. Use the supplied source rather than the unchanged public baseline.

Test command: python -m pytest tests -v
Start command: uvicorn src.api.app:app --host 127.0.0.1 --port 8000
Health check: http://127.0.0.1:8000/health
Dashboard: http://127.0.0.1:8000/
If the live demonstration fails, describe the actual problem and show the dated evidence capture as a recorded run. Do not describe a screenshot as a currently running demonstration. Keep narration within 10 to 15 minutes; the plan targets 12 minutes 20 seconds with additional room for natural pauses. The final rehearsal, not the word count alone, determines timing.

## Reference list for slide 14 and presenter notes
Canadian Institute for Cybersecurity. (n.d.). ISCX NSL-KDD dataset 2009. https://www.unb.ca/cic/datasets/nsl.html
FastAPI. (n.d.). HTTP Basic Auth. https://fastapi.tiangolo.com/advanced/security/http-basic-auth/
MDN contributors. (n.d.). Node textContent property. https://developer.mozilla.org/en-US/docs/Web/API/Node/textContent
Pascoe, C., Quinn, S., & Scarfone, K. (2024). The NIST cybersecurity framework (CSF) 2.0. National Institute of Standards and Technology. https://doi.org/10.6028/NIST.CSWP.29
Sommer, R., & Paxson, V. (2010). Outside the closed world: On using machine learning for network intrusion detection. In 2010 IEEE Symposium on Security and Privacy (pp. 305–316). IEEE. https://doi.org/10.1109/SP.2010.25
Tabassi, E. (2023). Artificial intelligence risk management framework (AI RMF 1.0). National Institute of Standards and Technology. https://doi.org/10.6028/NIST.AI.100-1
