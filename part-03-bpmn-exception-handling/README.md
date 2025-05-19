# Part 3 - Exception Handling

In this assignment, you will extend the image production process by adding intermediate events that catch a **timeout** and a **business error** thrown from a job worker.

You will start with a boilerplate Python script located in the **part-03-exception-handling/starter** folder and use **VS Code** to complete your work.

---

## ⏳ Time Available

You have approximately **30 minutes** to complete all activities in Part 3, including programming, deployment, and executing your BPMN process.

---

⚠️ **Note**: If you’re short on time or prefer not to model the process from scratch, you can skip the modeling and programming steps and jump directly to Play, Deploy, or Execute using the pre-built artifact provided in the final/ folder.

---

## 📁 Files

- `part-03-exception-handling/starter/p3s-image-production-process.bpmn`  
  → Your **starting point**: a basic process that includes model upload and image rendering steps.  
- `part-03-exception-handling/starter/p3s-thumbnails-production.py`  
  → A **starter Python script** that logs and returns thumbnails for an image. You will extend it to simulate and throw a business error.

---

## 🎯 Learning Goals

By completing this assignment, you will:

- Learn how to model **Timer Intermediate Events** to catch timeouts  
- Learn how to model **Error Intermediate Events** to catch business errors  
- Modify a Python Job Worker to simulate error conditions  
- Understand how exceptions are handled and routed in BPMN  

---

## ✅ Instructions

### 1. Open the Starter BPMN File

- Upload the file `p3s-image-production-process.bpmn` to your dedicated training folder in the **Camunda Web Modeler** and open it.

---

### 2. Add a Timer Intermediate Event

1. Extend the process to catch a **timeout** if the **Render Image** Receive Task takes too long to receive a message  
2. Attach a **Boundary Timer Event** to the **Render Image** Receive Task  
3. Set the **Duration** to `PT30S` (30 seconds)  
   - The duration must follow the **ISO 8601 duration format**, where `P` stands for "Period" and `T` introduces the time section. Example: `PT30S` = 30 seconds  
4. From the Timer Event, connect the flow to an **Exclusive Gateway** inserted immediately after the **Start Event**

---

### 3. Add an Error Intermediate Event

1. Attach a **Boundary Error Event** to the **Produce Thumbnails** service task  
2. In the Error section of the element properties panel, select **"Create new ..."**  
3. Set the **Name** to `ThumbnailProductionError`  
4. Set the **Error Code** to `thumbnail-production-error`  
5. Connect the Boundary Error Event to an **End Event** labeled **"Image Production Failed"**

---

### 4. Complete the Python Job Worker

1. Open the `p3s-thumbnails-production.py` script in **VS Code**  
2. Modify the `produce_thumbnails()` function to simulate a business rule violation:
   - If `imageRenderingQuality` is below `0.7` and `imageEnhancementQuality` is also below `0.7`, raise an error.
   - Otherwise, generate and return a list of thumbnail IDs.

   Example:

       if rendering_quality < 0.7 and enhancement_quality < 0.7:
           print("🎯 Throwing BPMN Error: thumbnail-production-error – Image quality insufficient for thumbnails")
           raise Exception("Image quality insufficient for thumbnails!")

3. Add a custom exception handler:
   - This function will be triggered when the above exception is raised.
   - It will forward the error to Camunda as a BPMN error using `set_error_status()`.

   Example:

       async def example_exception_handler(exception: Exception, job: Job, job_controller: JobController) -> None:
           print(f"⚠️ Error occurred during task {job.type}")
           print(f"❌ {exception}")
           await job_controller.set_error_status(
               message="Image quality insufficient for thumbnails",
               error_code="thumbnail-production-error"
           )

4. Assign the exception handler to the task:

       @worker.task(task_type="thumbnails_production", exception_handler=example_exception_handler)
       async def produce_thumbnails(job: Job):
           ...

---

## 🚀 Deploy Your Process Diagram

- In the **Camunda Web Modeler**, deploy your updated BPMN model to your training cluster

---

## ▶️ Execute Your Process Diagram

### 1. Exception handling caused by a Timeout

1. Open a terminal window and navigate to the `part-03-bpmn-exception-handling/starter` folder.
2. Start the image enhancement worker:
    `python p3s-thumbnails-production.py`
3. Open a second terminal window and navigate to the `python/windows` folder.
4. Start the job worker using:
   `python part-03-runner.py`
5. Ensure the worker starts correctly and connects to the cluster.
6. Open another terminal and navigate to the `clients` folder inside the `python` directory.
7. Start a process instance using:
   `python start-image-production-process.py mid-1`
8. Wait 30 seconds and go to Operate and open your process instance.
9. In the instance history, notice the `30 s` record which indicates that the timer event was triggered and the path pointing back to the gateway was taken.
   > The process diagram also shows how many times the service task was triggered.
11. To finish the instance, run:
   `python send-image-rendering-message.py mid-1 iid-1 0.8`

---

### 2. Exception handling caused by an Error

> ⚠️ Stop the job workers first: `ctrl+C`

1. Open a terminal window and navigate to the `part-03-bpmn-exception-handling/starter` folder.
2. Start the image enhancement worker:
    `python p3s-thumbnails-production.py`
3. Open a second terminal window and navigate to the `python/windows` folder.
4. Start the job worker using:
   `python part-03-runner.py`
5. Ensure the worker starts correctly and connects to the cluster.
6. Open another terminal and navigate to the `clients` folder inside the `python` directory.
7. Start a process instance using:
   `python start-image-production-process.py mid-1`
8. To continue the instance, run:
   `python send-image-rendering-message.py mid-1 iid-1 0.4`

   > The value `0.4` indicates low image quality. After enhancement, it becomes `0.6`, which still falls below the 0.7 threshold, triggering a business error.

9. Go to Operate and verify the path taken.
10. Watch the printout from your worker:

       📦 Thumbnails Production Worker in action with variables: {'imageId': 'iid-1', 'modelId': 'mid-1', 'imageRenderingQuality': 0.4, 'imageEnhancementQuality': 0.6000000000000001}
       🖼️ Processing image: iid-1
       🔍 Rendering: 0.4, Enhancement: 0.6000000000000001, Thumbnails: 3
       🎯 Throwing BPMN Error: thumbnail-production-error – Image quality insufficient for thumbnails
       ⚠️ Error occurred during task thumbnails_production
       ❌ Image quality insufficient for thumbnails!

---

✅ At this point, you have successfully extended your BPMN model to handle timeouts and errors using a connected Python Job Worker!

➕ Bonus: If you have time left, try handling additional failure scenarios or introduce escalation paths.

---

## 🛠 Required Tools

- Camunda Web Modeler  
- VS Code  
- Python 3.x

---

## 🏁 Outcome

By the end of this exercise, you will have transformed a simple BPMN model into a **fault-tolerant and resilient process**, capable of handling real-world exception scenarios dynamically through a Python Job Worker.

**Great job and happy modeling! 🎉**