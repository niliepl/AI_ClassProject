# AI_ClassProject
This repository contains my AI course projects, including a rule-based scholarship eligibility expert system and class activities implemented using Microsoft Power Automate.

## 📌 Rule-Based Scholarship Eligibility Expert System

### 📖 Project Overview

This project presents a **Rule-Based Scholarship Eligibility Expert System** designed to automate and standardize the evaluation of university scholarship applications. Built using **SWI-Prolog** as the reasoning engine and **Python** for interface and data visualization, the system evaluates student eligibility based on academic performance, financial need, co-curricular involvement, leadership roles, disciplinary status and special circumstances.

The system aims to address the limitations of manual scholarship evaluation, which is often time-consuming, inconsistent and prone to subjective judgment. By applying deterministic rule-based AI, the system ensures **fairness, transparency and explainability** in decision-making.

---

### 🎯 Objectives

* Model academic, financial, and co-curricular scholarship criteria using a structured knowledge base
* Develop a **Prolog-based inference engine** to classify scholarship eligibility
* Provide **clear eligibility outcomes with explanation traces**
* Support both **student-facing queries** and **officer-level batch evaluation**
* Visualize trends and distributions using Python analytics

---

### 🧠 System Features

* **Multi-criteria evaluation** across:

  * Academic performance (CGPA, credit hours)
  * Financial background (income group, dependents, employment)
  * Co-curricular activities & leadership
  * Special circumstances (health challenges, hardship)
* **Eligibility classification**:

  * Full Scholarship
  * Partial Scholarship
  * Not Eligible
* **Confidence scoring** for decision reliability
* **Explainable AI output** with reasoning trails
* **Two system modes**:

  * **Student Mode** – check eligibility using email
  * **Officer Mode** – batch processing and analytics dashboard

---

### 🏗️ System Architecture

* **SWI-Prolog**

  * Core decision-making engine
  * Knowledge base of IF–THEN rules
  * Inference and explanation generation
* **Python**

  * User interface (Tkinter)
  * CSV data handling
  * Data visualization and analytics

---

### 📊 Key Results

* Tested on **52 real student profiles**
* **100% decision consistency** across repeated runs
* Average batch processing time: **~157 ms**
* Throughput: **331 students/second**
* Scholarship awards issued only to candidates with:

  * Tier 1 academic performance
  * High or urgent financial need
  * Strong or outstanding activity involvement
* High confidence for awarded decisions (up to **100% confidence**)

---

### ✅ Why Rule-Based AI?

Unlike black-box machine learning models, this system prioritizes:

* **Transparency**
* **Explainability**
* **Policy compliance**
* **Institutional trust**

This makes it well-suited for high-stakes educational decision-making such as financial aid allocation.

---

### 🔮 Future Enhancements

* Web-based deployment
* Integration with live university databases
* Institutional pilot testing with scholarship officers
* Extension to other educational decision-support systems

---

### 🛠️ Tech Stack

* **SWI-Prolog** – Knowledge-based reasoning
* **Python** – Interface, batch processing, visualization
* **Tkinter** – GUI
* **CSV / Pandas / Matplotlib** – Data handling & analytics

---

## 📂 Project Files

- **main_app.py** – Main source code for the UTP Scholarship Management System  
- **scholarship_results.csv** – Processed scholarship results (input data file)  
- **scholarship_rules.pl** – Prolog rules file used for eligibility processing  
- **student_responses.csv** – Raw student responses (used to generate results)  
- **visualize.py** – Standalone script for generating result visualizations

---

## ▶️ How to Run the Program

1. **Install required dependencies**  
   Make sure you have Python 3.8+ installed. Then install the required Python packages:  

   ```bash
   pip install pandas matplotlib seaborn tk

**Note:** `tk` (Tkinter) is included with most Python installations by default. If you encounter errors, ensure Tkinter is installed.

2. **Install SWI-Prolog**
   The system uses a Prolog backend for scholarship processing. Download and install SWI-Prolog from:
   [Download Here](https://www.swi-prolog.org/Download.html)

   Make sure `swipl` is added to your system PATH so it can be executed from the terminal.

3. **Prepare project files**
   Download the following files and make sure are in the same directory: [Download File & Code Here](https://github.com/niliepl/AI_ClassProject/tree/main/Schorlaship_Sys) 
   * `main_app.py`

   * `scholarship_rules.pl`

   * `student_responses.csv`

   > Optional: `scholarship_results.csv` will be generated after processing.

4. **Run the application**
   Open a terminal in the project directory and run:

   ```bash
   python main_app.py
   ```

   This will launch the GUI for the **UTP Scholarship Management System**.

5. **Using the GUI**

   * **Welcome Tab:** Choose your role – Student or Officer, or view Analytics.
   * **Student Portal:** Enter your email to check scholarship eligibility results.
   * **Officer Portal:** Upload student responses (`.csv`) and process with Prolog AI. View summary and detailed results.
   * **Analytics Dashboard:** Generate charts to visualize scholarship distribution, confidence scores, and evaluation breakdowns.

---

## 📁 Other Relevant Files

In addition to the main project files, the repository also includes supporting documents for reference and presentation:

- [**Project Report**](https://github.com/niliepl/AI_ClassProject/blob/main/Others%20Relevant%20Documents/AI%20REPORT_G37.pdf) – Detailed report documenting the project objectives, methodology, implementation and results.  
- [**Presentation Slides**](https://drive.google.com/file/d/14xQhCi0-5KRvgVhhsEi8SvxZLr2UcXxT/view?usp=sharing) – Slides used for project demonstration and presentations.  
- [**Flowchart**](https://drive.google.com/file/d/14xQhCi0-5KRvgVhhsEi8SvxZLr2UcXxT/view?usp=sharing) – Visual representation of the system workflow and logic for easier understanding.

---

## 🤖 RPA Exercise: Automated Student Assignment Processing

This project demonstrates the use of **Robotic Process Automation (RPA)** using **Microsoft Power Automate** to automate student assignment submissions.

### 🎯 Objective

To reduce manual workload, improve accuracy, and ensure consistent documentation in handling student assignments.

### ✨ Key Features

* Automatic submission date comparison (on-time / late)
* Standardized folder structure and file naming
* Conditional email notifications to students
* Real-time tracking and status updates using Excel

### 🔄 Workflow Overview

1. **Trigger**: Microsoft Forms submission
2. **Data Processing**:

   * Extract and store data in Excel
   * Compare submission date with due date
   * Send confirmation or late notification email
3. **File Management**:

   * Auto-generate standardized file name
   * Save files into organized folders
4. **Tracking**:

   * Update email status in Excel automatically

---

## 📂 Project Files

* [**LeePeiLin_20251120152827**](https://github.com/niliepl/AI_ClassProject/tree/main/LeePeiLin_20251120152827)
  Exported Microsoft Power Automate flow for automated student assignment processing.

* [**AI_RPA.pdf**](https://github.com/niliepl/AI_ClassProject/blob/main/AI_RPA.pdf)
  Project report explaining the objective, workflow design, features and outcomes of the RPA solution.

---

## ▶️ How to Run the Program

1. Download  **LeePeiLin_20251120152827**.
2. Log in to **Microsoft Power Automate**.
3. Go to **My flows** → **Import**.
4. Upload the extracted flow package.
5. Reconfigure required connections:

   * Microsoft Forms
   * Outlook (Email)
   * OneDrive / SharePoint
   * Excel Online
6. Update:

   * Assignment **due date**
   * Target **folder path** for file storage
7. Turn on the flow.
8. Submit a test response via the **Microsoft Forms Assignment Submission Portal** to verify:

   * File creation
   * Email notification (on-time / late)
   * Excel status update
