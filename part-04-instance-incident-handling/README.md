# Part 4 - Instance Incident Handling

In this assignment, you will handle **technical errors** thrown from a job worker.

---

## ⏳ Time Available

You have approximately **20 minutes** to complete all activities in Part 4.

---

⚠️ **Note**: If you’re short on time or prefer not to model the process from scratch, you can skip the modeling and programming steps and jump directly to Play, Deploy, or Execute using the pre-built artifact provided in the final/ folder.

---

## 📁 Files

- `part-04-instance-incident-handling/starter/p4s-image-production-process.bpmn`  
  → Your **starting point**: a basic process that includes model upload and image rendering steps.

---

## 🎯 Learning Goals

By completing this assignment, you will:

- Understand how Camunda handles technical incidents during process execution  
- Simulate and analyze recoverable and non-recoverable errors  
- Use **Camunda Operate** to inspect incidents and **Camunda Web Modeler** to enhance your process  
- Modify your BPMN model to implement proper incident-handling strategies

---

## ✅ Instructions

### 1. Open the Starter BPMN File

- Upload `p4s-image-production-process.bpmn` to your dedicated training folder in the **Camunda Web Modeler**.
- Open the file and locate the **Model Uploading** service task.

---

### 2. Task Configuration – Retries

- Click on the **Model Uploading** service task.
- In the properties panel, locate the **Retries** field under the task definition.
- Note: If the field is empty, the default value is **3** retries.
  > This means the job will automatically be retried up to 3 times by the engine before an incident is raised.
- For the purpose of this exercise, you can explicitly set the value to **3** to ensure consistent behavior during testing.

---

## 🚀 Deploy Your Process Diagram

- In the **Camunda Web Modeler**, click **Deploy** to push your updated BPMN model to your training cluster.

---

## ▶️ Execute Your Process Diagram with Incidents

### 1. Incident with Recoverable Error

1. Open a terminal window.
2. Navigate to the `python/windows` folder.
3. Start the job worker using:
   ```bash
   python part-04-runner-online.py
   ```
4. Ensure the worker starts correctly and connects to the cluster.
5. Open another terminal and navigate to the `clients` folder inside the `python` directory.
6. Start a process instance using:
   ```bash
   python start-image-production-process.py mid_1
   ```
7. Observe the repeating outputs in the job worker terminal:
   ```
   📦 Received modelId: mid_1
   ❌ Invalid modelId format! Expected: mid-<number>
   ⚠️ Exception caught: Invalid modelId format. Expected: mid-<number>
   ```

   > In **Pyzeebe 4.5.0**, you cannot directly set `retries = 0` within the job worker code to stop further retries. This behavior aligns with Zeebe’s design — the engine decrements retries automatically when a job fails.

   > To explicitly set retries to zero, you must use the **Zeebe REST API**.

8. Open **Camunda Operate** and locate your process instance that caused the incident.
9. The incident reason will show:
   ```
   Failed to run task model_uploading. Reason: Invalid modelId format. Expected: mid-<number>
   ```
10. In the **Variables** panel, find `modelId` and click the **edit (✏️) icon**.
11. Change the value to a valid format (e.g., `mid-1`).
12. Click **Retry Incident** to resume the process.
13. Observe the successful output in the worker terminal:
    ```
    📦 Received modelId: mid-1
    ✅ Model with modelId 'mid-1' was successfully uploaded.
    ```
14. To finish the instance, run:
    ```bash
    python send-image-rendering-message.py mid-1 iid-1 0.8
    ```

---

### 2. Incident with Non-Recoverable Error

> ⚠️ Stop the job workers first: `ctrl+C`

1. Open a terminal window.
2. Navigate to the `python/windows` folder.
3. Start the job worker using:
   ```bash
   python part-04-runner-offline.py
   ```
4. Open another terminal and navigate to the `clients` folder.
5. Start a process instance:
   ```bash
   python start-image-production-process.py mid-1
   ```
6. Observe output like:
   ```
    📦 Simulating backend upload for modelId: mid-1
    🔁 Zeebe-reported retries remaining: 3
    ⚠️ Exception caught: Backend is offline.
    🔁 Remaining retries: 2
    ⏳ Setting backoff to 2000 ms

    📦 Simulating backend upload for modelId: mid-1
    🔁 Zeebe-reported retries remaining: 2
    ⚠️ Exception caught: Backend is offline.
    🔁 Remaining retries: 1
    ⏳ Setting backoff to 4000 ms

    📦 Simulating backend upload for modelId: mid-1
    🔁 Zeebe-reported retries remaining: 1
    ⚠️ Exception caught: Backend is offline.
    🔁 Remaining retries: 0
    ⏳ Setting backoff to 8000 ms
   ```

   > This simulates a persistent backend failure. Zeebe retries the job 3 times with exponential backoff. When retries reach 0, an incident is raised.

   > Refer to `model-uploading-offline.py` to understand how a job worker can dynamically set backoff durations and handle retry exhaustion.

7. Open **Camunda Operate** and inspect the incident.
8. Stop the offline worker: `ctrl+C`
9. Start the recoverable worker:
   ```bash
   python part-04-runner-online.py
   ```
10. Retry the incident in Operate.
11. Finalize the process:
    ```bash
    python send-image-rendering-message.py mid-1 iid-1 0.8
    ```
---

✅ You’ve now simulated both recoverable and non-recoverable errors using Python job workers.

> ➕ Continue below for advanced usage of **REST API-based incident handling**.

---

### 3. Incident with Recoverable Error Using REST API

> ⚠️ Stop the job workers first: `ctrl+C`

1. In Bruno, get an access token from `authentication/Get Access Token`.
2. Run `Create Fault Image Production Instance` with:
    ```json
    "modelId": "mid_1"
    ```
3. Open **Camunda Operate** and find the paused instance.
4. In Bruno, run `Activate Image Uploading Jobs`.

    > **Activation = job claimed by worker**. It must be activated before any action like failing or completing it.

5. Within 10 seconds, run:
    ```json
    {
      "retries": 0,
      "errorMessage": "Use the correct model identity format.",
      "retryBackOff": 0,
      "variables": {}
    }
    ```

    > **Explanation:** The job is failed, and retries are set to zero, causing an incident to be raised immediately.

6. In Operate, fix the variable (`modelId`) and retry the incident.
7. Re-activate the job.
8. Observe token advancing to next task.
9. Cancel the process when done.

---

## 🛠 Required Tools

- [Camunda Web Modeler](https://camunda.com/download/modeler/)
- [VS Code](https://code.visualstudio.com/)
- [Python 3.x](https://www.python.org/downloads/)
- [Bruno API Client](https://www.usebruno.com/)
- [Camunda Operate](https://docs.camunda.io/docs/components/operate/)

---

## 🏁 Outcome

By the end of this exercise, you will have transformed a basic BPMN process into a **resilient, incident-aware workflow**, fully capable of handling recoverable and non-recoverable errors using both workers and the Zeebe REST API.

**Great job and happy modeling! 🎉**