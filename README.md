# 🎓 Alumni Nexus

**Alumni Nexus** is a professional networking and mentorship platform designed to bridge the gap between current engineering students and college graduates [cite: 1.1]. It transforms a static database into an active community hub where seniors can give back and juniors can find a clear path to their future careers [cite: 1.1].

## 🌟 The Vision
I built this project because I noticed how difficult it was for juniors, especially in branches like **ECE**, to connect with seniors who have already "made it" in the industry [cite: 1.1]. This platform provides a specialized, centralized space for mentorship and job referrals within our college ecosystem [cite: 1.1].

## 🛠️ Tech Stack
* **Frontend:** [Streamlit](https://streamlit.io/) (Python framework) [cite: 1.1]
* **Backend:** Python logic with Session State management [cite: 1.1]
* **Database:** MySQL for persistent storage of user profiles and job postings [cite: 1.1]

## ✨ Key Features
* **Live Networking Dashboard:** Interactive cards for quick navigation to the directory or referral hub [cite: 1.1].
* **Smart Directory Search:** Find alumni by name or branch, with a dedicated toggle to highlight available **Mentors** [cite: 1.1].
* **Referral Board:** A community-driven space where alumni post job and internship links directly for students [cite: 1.1].
* **Real-time Analytics:** A live counter on the home page showing total registered alumni, providing immediate social proof [cite: 1.1].
* **Professional Profiles:** Users can manage their bio, LinkedIn presence, and mentorship status via a secure form [cite: 1.1].

## 🚀 How to Run Locally
1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/yourusername/alumni-nexus.git
    cd alumni-nexus
    ```
2.  **Install Dependencies:**
    ```bash
    pip install streamlit mysql-connector-python pandas
    ```
3.  **Database Setup:**
    * Create a MySQL database named `alumni_nexus`.
    * Ensure your `database.py` file has the correct `host`, `user`, and `password`.
4.  **Run the App:**
    ```bash
    streamlit run app.py
    ```

## 🏗️ Engineering Challenges
During development, I faced and resolved several technical hurdles, including:
* **State Persistence:** Managing user sessions across different "pages" using Streamlit's `session_state` [cite: 1.1].
* **Data Integrity:** Implementing defensive coding with `.get()` methods to prevent app crashes from missing database fields [cite: 1.1].
* **UI/UX Logic:** Designing a custom dashboard with `st.columns` and custom CSS to match a professional enterprise look [cite: 1.1].

---
Built with ❤️ by **P Divyansh** | ECE Department | [cite: 1.1]
