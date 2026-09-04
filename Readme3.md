Multi Issue Bangla Customer Complaint Dataset

1. Dataset Title

Multi-Issue Detection from Bangla Customer Complaints: An Annotated Dataset for Multilabel Text Classification


2.Dataset Overview

This dataset contains 4,096 customer complaints written in the Bangla language. The dataset was collected from public platforms like -social media posts and customer feedback Websites.

Each complaint is annotated with one or more of 8 predefined issue categories, for this it is  a multilabel classification dataset.

1.Total Complaints:4,096
2.Language:Bangla
3.Number of Labels:8
4.Dataset Type:Multilabel
5.Single-Label Complaints:3,026 (73.88%)
6.Multi-Label Complaints:1,070 (26.12%)


## 3. Dataset Creation

The dataset was created through the following process:

1. **Data Collection:** Bangla customer complaint texts were collected from social media pages and online platforms of Bangladeshi service organizations.
2. **Data Preparation:** Complaints were cleaned and assigned unique identifiers. Irrelevant or non-complaint texts were removed.
3. **Annotation Guideline:** A detailed annotation guideline was prepared defining all 8 issue categories, including label definitions, examples, and annotation rules.
4. **Independent Annotation:** Three annotators independently annotated each complaint following the finalized guideline.
5. **Agreement Analysis:** Inter-annotator agreement was calculated to assess annotation consistency.
6. **Disagreement Resolution:** Cases of disagreement among the annotators were reviewed and resolved according to the agreed annotation procedure.
7. **Final Annotated Dataset:** The resolved annotations were compiled into the final dataset.

---

## 4. Labels

The dataset uses the following 8 official issue categories:

* **Billing:** Complaints related to incorrect charges, overpricing, unexpected deductions, or payment-related financial disputes.
* **Refund:** Complaints where the customer has not received a refund, or where a refund was delayed or denied.
* **Delivery:** Complaints about delayed, missing, or incorrect delivery of products.
* **Customer_Service:** Complaints about unresponsive, unhelpful, or poor support from the service provider's customer care team.
* **Product_Quality:** Complaints about receiving damaged, incorrect, substandard, or misrepresented products.
* **Account:** Complaints related to login issues, account access problems, voucher or discount application failures, or account management difficulties.
* **Technical:** Complaints about app crashes, bugs, payment gateway errors, or other software/technical malfunctions.
* **Network:** Complaints about connectivity issues, network outages, or service unavailability related to network infrastructure.


---

## 5. Annotation Process

* Three annotators independently annotated all 4,096 complaints.
* Each annotator followed the finalized annotation guideline throughout the process.
* Inter-annotator agreement was calculated after the independent annotation was completed.
* Cases of genuine disagreement among the annotators were carefully reviewed.
* Final label decisions were made according to the agreed annotation procedure described in the guideline.

---

## 6. Dataset Structure

The final dataset, `Final_Annotated_Dataset.csv`, contains the following columns:

* **`Complaint_ID:`** A unique numeric identifier assigned to every complaint.
* **`Complaint_Text:`** The original Bangla text of the customer complaint.
* **`Final_Label:`** The final label(s) assigned to the complaint after annotation and disagreement resolution. Multiple labels are separated by a semicolon (`;`).

---

## 7. Multiple Labels

When a complaint contains more than one issue, all applicable labels are included in the `Final_Label` column and separated by a semicolon (`;`).

**Example:**

```text
Delivery;Refund
```

This means that the complaint has been identified as containing both a **Delivery** issue and a **Refund** issue.

**Example with three labels:**

```text
Customer_Service;Billing;Refund
```

This means that the complaint contains **Customer_Service**, **Billing**, and **Refund** issues simultaneously.

---

## 8. Files Included

The dataset package contains the following files:

* **`Final_Annotated_Dataset.csv:`** The complete annotated dataset containing all 4,096 complaints and their final labels.
* **`Data_Dictionary.xlsx:`** Describes each column in the dataset, including data types and examples.
* **`Annotation_Guideline.pdf:`** The finalized guideline used by all three annotators during the annotation process.
* **`README.md:`** This file provides guidance on understanding and using the dataset.

---

## 9. Data Usage

This dataset can be used by researchers and practitioners for the following purposes:

* Training and evaluating **multilabel text classification** models for Bangla customer complaints.
* Developing **natural language processing (NLP)** tools for low-resource Bangla language data.
* Studying **customer complaint patterns** in Bangladeshi service industries.
* Benchmarking **multilabel classification** approaches on real-world Bangla social media text.

Researchers using this dataset are encouraged to cite the associated *Data in Brief* manuscript.
