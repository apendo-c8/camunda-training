# Part 2 – Worker Basics

In this assignment, you will extend a simple image production process by connecting a Python job worker to the **Image Enhancement** sub-process in your BPMN model.

You will start with a BPMN file and a boilerplate Python script located in the folder:  
📁 `part-02-worker-basics/starter`

---

## ⏳ Time Available

You have approximately **30 minutes** to complete the exercise.

If you finish early:
- ➕ Add an **outcome mapping** (e.g. quality status) to the BPMN model.

---

## 📁 Files

- `part-02-worker-basics/starter/p2s-image-production-process.bpmn`  
  → Your starting point BPMN model.

- `part-02-worker-basics/starter/p2s-image-enhancement.py`  
  → Your Python starter script to build the worker.

---

## 🎯 Learning Goals

By completing this exercise, you will learn to:

- Use **Camunda input mappings**
- Implement and run a **Python Job Worker**
- Connect a worker to **Camunda 8**
- Observe how workers dynamically impact the process

---

## ✅ Instructions

### 1. Open the BPMN Process

- Upload the file `p2s-image-production-process.bpmn` to your Camunda **Web Modeler**
- Open it and locate the **Image Enhancement** service task

---

### 2. Add Variable Mapping

1. Select the **Image Enhancement** task  
2. In the **Details** panel, scroll to the **Inputs** section  
3. Click **Create** and enter:
   - **Local variable name:** `imageIdentity`
   - **Assignment type:** Expression
   - **Assignment value:** `imageId`

✅ This maps the incoming variable `imageId` to a local variable `imageIdentity` for the worker.

---
### 3. Complete the Python Job Worker

Open the file `p2s-image-enhancement.py` in **VS Code**. You will see a working script that connects to your Camunda cluster, but it doesn’t yet define what the worker should do.

Follow these steps to complete the job worker:

---

#### 🧩 Step 1 – Register a job worker function

Inside the `run_worker()` function, locate the `# TODO` comment.  
This is where we register a new job handler by writing a Python function and attaching it to the worker.

Add the following:

    @worker.task(task_type="image_enhancement")
    async def enhance_image(job: Job):

This tells the Camunda engine:
> “Whenever a job of type `image_enhancement` appears, call this function to handle it.”

---

#### 🧩 Step 2 – Read input variables from the job

Inside the `enhance_image` function, add these lines to fetch input variables from the process instance:

    image_id = job.variables.get("imageIdentity", "unknown")
    quality = job.variables.get("imageRenderingQuality", 0)

This extracts two variables:
- `imageIdentity`: which we set earlier via input mapping in the BPMN
- `imageRenderingQuality`: the current quality of the image (a number)

---

#### 🧩 Step 3 – Enhance the quality

Now simulate the image enhancement by increasing the quality by `0.2`, but make sure it doesn’t exceed `1.0`:

    enhanced_quality = min(quality + 0.2, 1.0)

This simple logic represents the business action taken by your worker.

---

#### 🧩 Step 4 – Print trace output

(Optional but helpful) Add print statements to understand what’s happening when the job runs:

    print(f"\n📸 Enhancing image: {image_id}")
    print(f"🔍 Original quality: {quality}")
    print(f"✅ Enhanced quality: {enhanced_quality}")

---

#### 🧩 Step 5 – Return variables to the process

Finally, return the result back to the BPMN process like this:

    return {"imageEnhancementQuality": enhanced_quality}

This sets a new variable in the process instance, which downstream tasks can use.

---

#### ✅ Your full function should now look like this:

    @worker.task(task_type="image_enhancement")
    async def enhance_image(job: Job):
        image_id = job.variables.get("imageIdentity", "unknown")
        quality = job.variables.get("imageRenderingQuality", 0)

        print(f"\n📸 Enhancing image: {image_id}")
        print(f"🔍 Original quality: {quality}")

        enhanced_quality = min(quality + 0.2, 1.0)
        print(f"✅ Enhanced quality: {enhanced_quality}")

        return {"imageEnhancementQuality": enhanced_quality}

---

💾 Save the file and run it from the terminal:

    python p2s-image-enhancement.py

Leave it running — it will wait for jobs from Camunda to pick up.

---

## 🚀 Deploy Your Process Diagram

- In the **Camunda Web Modeler**, deploy your updated BPMN model to your training cluster

---

## ▶️ Execute Your Process Diagram

Follow the steps below to test your process with live workers:

1. Open **Camunda Operate** and go to the **Processes** tab.
2. Confirm that your **Image Production Process** is deployed.
3. Open a terminal window and navigate to the `part-02-worker-basics/starter` folder.
4. Start the image enhancement worker:
    ```
    python p2s-image-enhancement.py
    ```
5. Open a second terminal window and navigate to the `python/windows` folder.
6. Start the job runner:
    ```
    python part-02-runner-online.py
    ```
7. Ensure both workers have started successfully and are connected to the cluster.
8. Open a third terminal window and navigate to the `clients` folder inside the `python` directory.
9. Start a new process instance:
    ```
    python start-image-production-process.py mid-1
    ```
10. Send the image rendering message to the process instance:
    ```
    python send-image-rendering-message.py mid-1 iid-1 0.6
    ```
11. Check the printouts in the terminal windows and observe the process path in **Camunda Operate**.

> 💡 **Tip:**  
> Try using different values for `imageRenderingQuality` (e.g., `0.4`, `0.9`) to explore how the process behaves under different conditions.

---

> ✅ Success! You’ve connected your BPMN model to a real job worker.

---

## 🛠 Required Tools

- [Camunda Web Modeler](https://modeler.cloud.camunda.io/)
- [VS Code](https://code.visualstudio.com/)
- [Python 3.x](https://www.python.org/)
- Required packages:

    pip install pyzeebe==4.5.0 python-dotenv

---

## 🏁 Outcome

By completing this assignment, you've:

- Mapped input variables to a service task  
- Implemented your first Python worker using `pyzeebe`  
- Connected BPMN execution to real backend logic

**Great job and happy modeling! 🎉**