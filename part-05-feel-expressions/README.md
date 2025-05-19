# Part 1 - FEEL Expressions

In this assignment, you’ll evolve the image production process into a more complete version by adding a multi-instance service task and a FEEL expression mapping image to a common collection to iterate over. You will begin with a boilerplate BPMN file located in the **part-05-feel-expression/starter** folder and use the **Camunda Web Modeler** to complete your work.

---

## ⏳ Time Available

You have approximately **20 minutes** available to complete all activities in Part 5, including modeling, testing, and exploring your BPMN process.

---

⚠️ **Note**: If you’re short on time or prefer not to model the process from scratch, you can skip the modeling and programming steps and jump directly to Play, Deploy, or Execute using the pre-built artifact provided in the final/ folder.

---

## 📁 Files

- `part-05-feel-expression/starter/p5s-image-production-process.bpmn`  
  → This is your **starting point**: a basic process that includes model upload and image rendering steps.

---

## 🎯 Learning Goals

By completing this assignment, you will learn how to:

- Use FEEL expressions to dynamically generate a collection for iteration  
- Model sequential multi-instance service tasks  
- Configure input and output mapping within multi-instance tasks  

---

## ✅ Instructions

### 1. Open the Starter BPMN File

- Upload `p5s-image-production-process.bpmn` to your dedicated training folder in the **Camunda Web Modeler**.

---

### 2. Add a Sequential Multi-instance for Asset Storage

In the **Camunda Web Modeler**, activate the **Space Tool** from the palette to create some room between the "Produce Thumbnails" step and the final end events. Then insert a **Task** element (also found in the palette) into the newly created space.

1. Click on the **Change element** icon and select **"Service Task"** and label it **Store Asset**.  
2. Set its **Job Type** to:  
     ➔ `asset_storage`
3. Click on the **Change element** icon again and select **Sequential Multi-instance** from the upper-right corner of the popup dialog.  
4. Expand the **Properties** panel and locate the **Multi-instance** section.  
 
    > ℹ️ **Note:**  
    > The Multi-instance section contains four fields:  
    > - **Input collection** – the list of values to iterate over.  
    > - **Input element** – the name of the variable used for each item in the collection during iteration.  
    > - **Output collection** – the name of the array that will store the results of each iteration.  
    > - **Output element** – the name of the variable used to return the result of each individual iteration.  

5. In the **Input collection** field, insert this FEEL expression:  
   ```javascript
   for x in 1..(count(thumbnailIds) + 1) return if x = 1 then imageId else thumbnailIds[x - 1]
   ```

    > ℹ️ **Note:**  
    > This expression builds a dynamic list that starts with the main `imageId`, followed by all the `thumbnailIds`.  
    > `x` ranges from 1 to the total count of thumbnails plus one.  
    > If `x` is 1, it returns the `imageId`.  
    > Otherwise, it retrieves the corresponding thumbnail ID by subtracting one from `x`.

6. In **Input element**, enter `imageId`.  
    > This defines the loop variable name. Each iteration of the multi-instance task will use `imageId` to represent the current value from the collection.

7. In **Output collection**, enter `assetIds`.  
    > After each iteration, the result (e.g. a stored asset reference) is collected into the `assetIds` array.

8. In **Output element**, enter `assetId`.  
    > This is the name of the variable returned by each instance of the task and added to the `assetIds` list.

---

## 🚀 Deploy Your Process Diagram

- In the **Camunda Web Modeler**, click **Deploy** to push your updated BPMN model to your training cluster.

---

## ▶️ Execute Your Process Diagram

### 1. Multi-instance Service Task with FEEL Expression

1. Open a terminal window.  
2. Navigate to the `python/windows` folder.  
3. Start the job worker using:  
   `python part-05-runner.py`  
4. Ensure the worker starts correctly and connects to the cluster.  
5. Open another terminal and navigate to the `clients` folder inside the `python` directory.  
6. Start a process instance using:  
   `python start-image-production-process.py mid-1`  
7. Send the rendering message:  
   `python send-image-rendering-message.py mid-1 iid-1 0.8`  
8. Watch the printout from your workers:  
    ```
    💾 Received asset: iid-1
    📦 Stored asset as: iid-1

    💾 Received asset: tid-1
    📦 Stored asset as: tid-1

    💾 Received asset: tid-2
    📦 Stored asset as: tid-2

    💾 Received asset: tid-3
    📦 Stored asset as: tid-3
    ```
9. Go to Operate and select Finished Instances and click on the one that was just completed.  
10. Extend the Variables panel and watch the `assetIds` list, which now includes all images that were stored as assets.

---

> ✅ At this point, you have successfully modeled and executed a process with a multi-instance task using FEEL expressions!

> ➕ To explore the process further, try changing the multi-instance task to **parallel** instead of sequential. Then monitor how all service task instances run simultaneously.

---

## 🛠 Required Tool

- [Camunda Web Modeler](https://camunda.com/download/modeler/)

---

## 🏁 Outcome

By the end of this exercise, you’ll have transformed a linear BPMN model into a more dynamic, realistic process using decision logic and reusable modeling structures.

**Great job and happy modeling! 🎉**