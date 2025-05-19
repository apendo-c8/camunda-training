# Part 1 - BPMN Basics

In this assignment, you’ll evolve a simple image production process into a more advanced version by adding a sub-process with decision logic. You will begin with a boilerplate BPMN file located in the **part-01-bpmn-basics/starter** folder and use the **Camunda Web Modeler** to complete your work.

---

## ⏳ Time Available

You have approximately **15 minutes** available to complete all activities in Part 1, including modeling, testing, and exploring your BPMN process.

---

⚠️ **Note**: If you’re short on time or prefer not to model the process from scratch, you can skip the modeling and programming steps and jump directly to Play, Deploy, or Execute using the pre-built artifact provided in the final/ folder.

---

## 📁 Files

- `part-01-bpmn-basics/starter/p1s-image-production-process.bpmn`  
  → This is your **starting point**: a basic process that includes model upload and image rendering steps.

---

## 🎯 Learning Goals

By completing this assignment, you will learn how to:

- Extend a BPMN process using **sub-processes**
- Model decisions using **exclusive gateways**
- Use and configure **service tasks** effectively

---

## ✅ Instructions

### 1. Open the Starter BPMN File

Upload `p1s-image-production-process.bpmn` to your dedicated training folder in the **Camunda Web Modeler**.  
Take a moment to explore the process, which currently includes:

- A **Start Event**
- A **Service Task** for uploading a model
- A **Receive Task** for waiting for the rendered image
- An **End Event**

> **Note:**  
> The first task ("Upload Model") is an **orchestrated task**, meaning it triggers the production of a model. This can either be carried out directly by the job worker or delegated to a backend service through the worker.  
>  
> The "Render Image" step is a **receive task**, which waits for an external event to signal that image rendering is complete.  
>  
> This highlights a key principle: in this process, we are primarily **tracking the flow** of external work, rather than **managing** or **performing** the work inside the process itself.

### 2. Add a Sub-Process for Image Enhancement

In the **Camunda Web Modeler**, activate the **Space Tool** from the palette to create some room between the "Render Image" step and the final end event. Then insert a **Task** element (also found in the palette) into the newly created space.

1. Click on the **Change element** icon and select **"Sub-Process (collapsed)"**.
2. Label the sub-process: **"Enhance Image"**.
3. This sub-process will later be expanded to contain decision logic for whether or not to enhance the image.

### 3. Model the Decision Logic Inside the Sub-Process

Inside the sub-process, perform the following steps:

1. **Expand** the sub-process to start modeling inside it.
2. Add a **Start Event**.
3. Add an **Exclusive Gateway** and label it:  
   ➔ **"Should the image be enhanced?"**
4. From the gateway, create two branches:
   - **Yes path**:  
     ➔ Lead to a **Service Task** labeled **"Enhance Image"**,  
     ➔ Then connect it to a new, **unlabeled Exclusive Gateway**.
   - **No path**:  
     ➔ Connect directly to the same **unlabeled Exclusive Gateway**.
5. Connect the **unlabeled Exclusive Gateway** to an **End Event** labeled:  
   ➔ **"High-Quality Image Achieved"**.
6. On the **Yes path** sequence flow:
   - Set it as a **Condition Expression**.
   - Use the expression:  
     ➔ `imageRenderingQuality < 0.7`
7. On the **No path** sequence flow:
   - Click on the **Change Type** icon.
   - Set it as the **Default Flow**.
8. Select the **"Enhance Image"** service task:
   - Set its **Job Type** to:  
     ➔ `image_enhancement`
     
---

## 🎮 Using Play to Debug Your Diagram

In Camunda, **Play** is a built-in tool that allows you to deploy, test, and debug your BPMN models directly within the Web Modeler.

Follow these steps to test your process:

1. Click on the **Play** tab (next to **Design** and **Implement**).
2. Select the **Training Cluster**.
3. Wait for the model to be deployed.
4. Click on the **three dots** next to the blue play button and select **"Edit variables and start instance"**.
5. Insert the following JSON document into the variables field:
    ```json
    {
      "modelId": "mid-1"
    }
    ```
6. Click on **Create instance** to start a new instance of your process model.
7. Click on the **blue checkmark button** to complete the **Upload Model** service task manually.
8. The next step is to **notify the process** that the rendering system has completed its work by sending a **message** to the process engine.
9. Click on the **three dots** next to the envelope icon and select **"Edit variables and publish message"**.
10. Insert the following JSON document into the variables field:
    ```json
    {
      "imageId": "iid-1",
      "imageRenderingQuality": 0.6
    }
    ```
11. Set the **Message Correlation Key** to match the model ID:
    ```
    mid-1
    ```

    > ℹ️ **Note:** In BPMN, *message correlation* ensures that a published message reaches the correct waiting process instance.  
    > The correlation key acts like a unique ID to link the message to a specific running instance.  
    > If no process instance is waiting with a matching correlation key, the message is ignored or held, depending on configuration.

12. Publish the message to correlate it with the correct process instance.
13. Finally, enter your sub-process and manually complete the **Enhance Image** service task by selecting **Edit variables and complete job**.
14. Insert the following JSON document into the variables field:
    ```json
    {
      "imageEnhancementQuality": 0.8
    }
    ```
15. Click **Complete job** and check out the instance variables.
---

> ✅ At this point, you have successfully tested and debugged your enhanced BPMN model using Play!  

> ➕ To explore the process further, try starting another instance with a different `imageRenderingQuality` value that takes the **alternative path** through the sub-process.

> 🎯 If you have time left, feel free to explore Play even further — try rewinding the process, adding new variables, or changing existing values to see how the flow reacts.

---

## 🛠 Required Tool

- [Camunda Web Modeler](https://camunda.com/download/modeler/)

---

## 🏁 Outcome

By the end of this exercise, you’ll have transformed a linear BPMN model into a more dynamic, realistic process using decision logic and reusable modeling structures.

**Great job and happy modeling! 🎉**