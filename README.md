# AI Project Recommendation System 🌟

An interactive AI-powered system that recommends personalized project ideas based on users' skills, interests, and goals. This project leverages the **CrewAI** framework to orchestrate multiple AI agents, each specialized in a particular aspect of the recommendation process. 🚀

---

## Table of Contents 📋

- [Introduction](#introduction-ℹ️)
- [Features](#features-✨)
- [Architecture](#architecture-🏗️)
- [Installation](#installation-🛠️)
- [Usage](#usage-🚀)
- [Project Structure](#project-structure-📂)
- [Contributing](#contributing-🤝)
- [License](#license-📜)
- [Contact](#contact-📞)

---

## Introduction ℹ️

The AI Project Recommendation System is designed to help users discover project ideas tailored to their unique profiles. By leveraging a team of AI agents, the system engages users in a natural conversation to gather information about their background, skills, interests, and constraints.

It then analyzes this data, generates a list of suitable project ideas, ranks them based on relevance and feasibility, and presents the top recommendations in an actionable format. 🎯

This system is ideal for **students, professionals, and hobbyists** looking to undertake meaningful projects aligned with their goals. Built with extensibility in mind, it uses the **CrewAI** framework to manage a collaborative team of AI agents powered by **Google's Gemini API**. 🌐

---

## Features ✨

- **Interactive Onboarding**: Conversationally gathers user profile info. 🤝  
- **Profile Analysis**: Structures and validates data into a machine-readable profile. 📊  
- **Project Idea Generation**: Generates ideas based on profile + real-time trends. 💡  
- **Project Ranking**: Uses relevance, feasibility, and impact for scoring. 🏆  
- **Presentation**: Clearly communicates recommendations with explanations. 🎯  
- **Extensibility**: Easily integrate new tools/agents. 🛠️  
- **Logging and Saving**: Stores data in `project_recommendation_output`. 💾  

---

## Architecture 🏗️

The system is built using the **CrewAI** framework, orchestrating specialized AI agents:

- **User Onboarder**: Collects user input via natural conversation. 🗣️  
- **User Profile Analyst**: Analyzes and validates the profile. 🔍  
- **Project Generator**: Generates project ideas. 🚀  
- **Project Ranker**: Ranks ideas by relevance, feasibility, and impact. 📈  
- **Presentation Specialist**: Presents top ideas in an actionable format. 📝  

Agents operate **sequentially**, passing data forward. Powered by **Gemini API** via `langchain-google-genai` and supports external services like **Serper** for enhanced search. ⚙️

---

## Installation 🛠️

### 1. Clone the Repository 📥

git clone https://github.com/naakaarafr/ai-project-recommendation-system.git
cd ai-project-recommendation-system
2. Install Dependencies 📦
Ensure Python 3.8+ is installed, then:

bash
Copy
Edit
pip install -r requirements.txt
3. Set Up Environment Variables 🔑
Create a .env file in the root:

ini
Copy
Edit
GOOGLE_API_KEY=your_google_api_key
SERPER_API_KEY=your_serper_api_key
Replace with your actual API keys. These can be obtained from Google Cloud and Serper.dev respectively.

4. Verify Configuration ✅
bash
Copy
Edit
python config.py
This will confirm that your API keys are properly set.

Usage 🚀
Start an interactive session:

bash
Copy
Edit
python main.py
Flow:

Welcome message 👋

Onboarding questions ❓

skip — Skip current question ⏭️

back — Go to previous question ⏮️

quit — Exit the session 🚪

Profile Analysis 📋

Project Idea Generation 💡

Ranking & Presentation 🏅

Session data is saved in the project_recommendation_output/ folder. 📂

Alternative: Run the crew directly with predefined input:

bash
Copy
Edit
python crew.py
Project Structure 📂
graphql
Copy
Edit
ai-project-recommendation-system/
├── main.py                        # Entry point for the interactive system 🚀
├── crew.py                        # Defines the CrewAI workflow 🧠
├── agents.py                      # AI agents and their roles 🤖
├── tasks.py                       # Agent-specific tasks 📝
├── tools.py                       # Custom tools (e.g., GitHub search) 🛠️
├── config.py                      # Config & API key handling ⚙️
├── requirements.txt               # Python dependencies 📋
├── project_recommendation_output/ # Output directory 💾
└── README.md                      # Project documentation 📘
Contributing 🤝
Contributions are welcome! Here's how:

Fork the repo 🍴

Create a new branch 🌿

bash
Copy
Edit
git checkout -b feature/your-feature-name
Make changes, commit with clear messages ✍️

Push to your fork 📤

bash
Copy
Edit
git push origin feature/your-feature-name
Open a pull request 📬

Follow PEP 8 and include tests where appropriate. ✅

License 📜
This project is licensed under the MIT License. See the LICENSE file for details.

Contact 📞
For questions or feedback, reach out:

GitHub: naakaarafr 👤

Email: divvyanshkudesiaa1@gmail.com 📧

Feel free to open an issue or get in touch!

Happy coding, and enjoy discovering your next project with the AI Project Recommendation System! 🎉✨
