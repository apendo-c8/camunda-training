
## 1. Simple Comparison (Decision Logic)

>**Explanation:**
> "This shows a basic comparison. We check if `imageRenderingQuality` is at least 0.7. This is typical for decision tables or gateway conditions."

```feel
imageRenderingQuality >= 0.7
```

**Context JSON:**

```json
{ "imageRenderingQuality": 0.8 }
```

*Result: true*

---

## 2. List Mapping (Iteration with `for`)

>**Explanation:**
> "Here, we loop through all the thumbnails and build a new list. Notice how FEEL uses 1-based indexing for lists."

```feel
for x in 1..count(thumbnails) return thumbnails[x]
```

**Context JSON:**

```json
{ "thumbnails": ["a.png", "b.png", "c.png"] }
```

*Result: \["a.png", "b.png", "c.png"]*

---

## 3. If-Else Expression (Classification)

>**Explanation:**
> "With FEEL's if-else, we classify a quality score. Try changing the input to see when it becomes 'high' or 'low'."

```feel
if quality > 0.8 then "high" else "low"
```

**Context JSON:**

```json
{ "quality": 0.9 }
```

*Result: "high"*

---

## 4. Type Conversion Example

>**Explanation:**
> "If you need to convert between types in FEEL, you can use functions like `string()`, `number()`, or `date()`."

Convert a number to a string:

```feel
string(myNumber)
```

**Context JSON:**

```json
{ "myNumber": 123.45 }
```

*Result: "123.45"*

Convert a string to a number:

```feel
number(myStringNumber)
```

**Context JSON:**

```json
{ "myStringNumber": "42" }
```

*Result: 42*


## 5. Working with Lists

>**Explanation:**
> "Here are some list operations: count, sum, and min."

```feel
count(myValues)
```

**Context JSON:**

```json
{ "myValues": [10, 20, 30] }
```

*Result: 3*

```feel
sum(myValues)
```

**Context JSON:**

```json
{ "myValues": [10, 20, 30] }
```

*Result: 60*

```feel
min(myValues)
```

**Context JSON:**

```json
{ "myValues": [10, 20, 30] }
```

*Result: 10*

---

## 6. String Manipulation

>**Explanation:**
> "You can transform strings, for example converting to upper case."

```feel
upper case(myText)
```

**Context JSON:**

```json
{ "myText": "feel is nice" }
```

*Result: "FEEL IS NICE"*

---

## 7. Input/Output Mapping Example

>**Explanation:**
> "You can map variables between process steps. For example, mapping `order.amount` to a new variable."

```feel
order.amount
```

**Context JSON:**

```json
{ "order": { "amount": 123.45 } }
```

*Result: 123.45*

---

## 8. Null Check

>**Explanation:**
> "Handle missing data by checking for null."

```feel
if variable != null then variable else "not set"
```

**Context JSON:**

```json
{ "variable": null }
```

*Result: "not set"*

---

## 9. Filtering a List

>**Explanation:**
> "Filter items from a list using a lambda expression."

```feel
scores[item > 5]
```

**Context JSON:**

```json
{ "scores": [1, 3, 7, 10] }
```

*Result: \[7, 10]*

---

## 10. Date and Time

>**Explanation:**
> "This checks if the due date has already passed by comparing it to today's date using FEEL."

```feel
date(dueDate) < today()

```

**Context JSON:**

```json
{ "dueDate": "2024-05-10" }
```

*Result: true*

---

## 11. Boolean Expressions for Gateways

>**Explanation:**
> "Logical expressions combine conditions, useful in gateways and decisions."

```feel
order.status = "APPROVED" and order.amount > 100
```

**Context JSON:**

```json
{ "order": { "status": "APPROVED", "amount": 150 } }
```

*Result: true*

---

## 12. Object Construction

>**Explanation:**
> "You can build a new context object with variables and computed fields."

```feel
{ "id": order.id, "status": "COMPLETE", "completedAt": now() }

```

**Context JSON:**

```json
{ "order": { "id": 42 } }
```

*Result: Context with id, status, completedAt (current time)*

---



## 13. Array Access

>**Explanation:**
> "Here, we get the second item from a list stored in a variable, and as we learned before, FEEL uses 1-based indexing for lists"

```feel
myList[2]
```

**Context JSON:**

```json
{ "myList": ["a", "b", "c"] }
```

*Result: "b"*

>**Explanation:**
> "You can also use a variable for the index. This example selects an item based on the value of `idx`."

```feel
myList[idx]
```

**Context JSON:**

```json
{ "myList": ["x", "y", "z"], "idx": 3 }
```

*Result: "z"*

---

## Prompts for FEEL Copilot

---

**Write a FEEL expression that checks if a list of orders contains any order over 1000.**

**Context:**

```json
{ "orders": [320, 455, 1200, 700] }
```

---

**How do I sum all values in a list variable in FEEL?**

**Context:**

```json
{ "myList": [3, 8, 4, 15] }
```

---

**Give me a FEEL expression to classify a risk score into low, medium, or high.**

**Context:**

```json
{ "risk": 71 }
```

---

**How do I map an object list to a list of just the orderNumbers in FEEL?**

**Context:**

```json
{
  "orders": [
    { "orderNumber": "A100", "amount": 120 },
    { "orderNumber": "B200", "amount": 250 }
  ]
}
```

---

**Show a FEEL if-else that outputs 'ok' if two variables are equal, else 'error'.**

**Context:**

```json
{ "a": 15, "b": 20 }
```

---

**What FEEL function can I use to get today’s date?**

**Context:**

```json
{}
```

---



